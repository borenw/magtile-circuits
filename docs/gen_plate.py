#!/usr/bin/env python3
"""Generate MagTile rubbing plates (STL/3MF), QR codes, and isometric previews.

Each plate carries a circuit schematic in raised relief (a pencil-rubbing / frottage
master) plus a QR code that opens the matching browser game. One spec per plate; the
tile specs mirror docs/plate_game.js so the plate and the game read identically.

    python3 gen_plate.py            # build all plates into docs/

Deps: trimesh, shapely, numpy, segno, lxml, manifold3d, matplotlib.
"""
import math, os
import numpy as np
import trimesh
from trimesh.creation import extrude_polygon, box
from shapely.geometry import LineString, Polygon, Point, box as sbox
from shapely.ops import unary_union
import segno

DOCS = os.path.dirname(os.path.abspath(__file__))
MARGIN=4.0; QR_SIZE=40.0; BAND=48.0
BASE_H=2.0; RELIEF=1.2; WIRE=3.0; DETAIL=2.4

# ---------------- per-cell schematic geometry (mm) ----------------
def cell_shapes(cx, cy, half, spec):
    """Return list of (geometry, width|None) for one tile spec {e,c,touch}."""
    S=[]; e=spec.get('e',[]); c=spec.get('c','none')
    def E(w):  # edge midpoint
        return {'top':(cx,cy+half),'bottom':(cx,cy-half),'left':(cx-half,cy),'right':(cx+half,cy)}[w]
    def lead(w,to=None,width=WIRE): S.append((LineString([E(w),to or (cx,cy)]),width))
    def dot(r=2.4): S.append((Point(cx,cy).buffer(r,resolution=20),None))

    if c in ('none','node'):
        for w in e: lead(w)
        if c=='node' or len(e)>=3: dot()
    elif c=='res':
        if 'left' in e and 'right' in e:
            lead('left',(cx-12,cy)); lead('right',(cx+12,cy))
            S.append((LineString([(cx-12,cy),(cx-9,cy+8),(cx-3,cy-8),(cx+3,cy+8),(cx+9,cy-8),(cx+12,cy)]),DETAIL))
        else:
            lead('top',(cx,cy+12)); lead('bottom',(cx,cy-12))
            S.append((LineString([(cx,cy+12),(cx+8,cy+9),(cx-8,cy+3),(cx+8,cy-3),(cx-8,cy-9),(cx,cy-12)]),DETAIL))
    elif c=='cap':
        for w in e:
            if w!='bottom': lead(w)
        S.append((LineString([(cx,cy),(cx,cy-4)]),WIRE))
        S.append((LineString([(cx-7,cy-4),(cx+7,cy-4)]),DETAIL))
        S.append((LineString([(cx-7,cy-9),(cx+7,cy-9)]),DETAIL))
        S.append((LineString([(cx,cy-9),E('bottom')]),WIRE))
        dot()
        if spec.get('touch'):
            S.append((LineString([(cx,cy),(cx+12,cy+12)]),DETAIL))          # antenna trace
            pad=sbox(cx+10,cy+10,cx+half-2,cy+half-2)
            S.append((pad.buffer(1.2).difference(pad.buffer(-1.2)),None))    # pad outline
    elif c=='inv':
        lead('left',(cx-12,cy))
        S.append((Polygon([(cx-12,cy-12),(cx-12,cy+12),(cx+10,cy)]).buffer(0),None))
        S.append((Point(cx+13,cy).buffer(3.2,resolution=20).difference(Point(cx+13,cy).buffer(1.6,resolution=20)),None))
        S.append((LineString([(cx+16,cy),E('right')]),WIRE))
        S.append((LineString([(cx,cy-4),E('bottom')]),WIRE))
    elif c=='piezo':
        S.append((Point(cx,cy).buffer(10,resolution=32).difference(Point(cx,cy).buffer(7,resolution=32)),None))
        S.append((Point(cx,cy).buffer(3.2,resolution=20),None))
        S.append((LineString([(cx,cy+10),E('top')]),DETAIL))
        S.append((LineString([(cx-10,cy),E('left')]),DETAIL))
        for rr in (13,16):
            a=np.linspace(-0.6,0.6,12)
            S.append((LineString([(cx+rr*math.cos(t),cy+rr*math.sin(t)) for t in a]),1.6))
    elif c=='led':
        for w in e: lead(w)
        S.append((Polygon([(cx-10,cy+4),(cx+10,cy+4),(cx,cy-10)]).buffer(0),None))  # diode triangle (points down)
        S.append((LineString([(cx-10,cy-13),(cx+10,cy-13)]),DETAIL))                 # cathode bar
        for dx in (0,6):
            S.append((LineString([(cx+9+dx,cy+9),(cx+15+dx,cy+15)]),1.4))            # light rays
    elif c=='batt':
        for w in e: lead(w)
        S.append((LineString([(cx-8,cy+9),(cx-8,cy-9)]),DETAIL))                     # long plate
        S.append((LineString([(cx,cy+4),(cx,cy-4)]),4.0))                            # short plate
        S.append((LineString([(cx+8,cy+9),(cx+8,cy-9)]),DETAIL))                     # long plate
    elif c=='gnd':
        for w in e: lead(w)
        S.append((LineString([(cx,cy),(cx,cy-6)]),WIRE))
        S.append((LineString([(cx-10,cy-8),(cx+10,cy-8)]),DETAIL))
        S.append((LineString([(cx-6,cy-13),(cx+6,cy-13)]),DETAIL))
        S.append((LineString([(cx-2,cy-17),(cx+2,cy-17)]),DETAIL))
    return S

# ---------------- build one plate ----------------
def build_plate(spec):
    rows,cols,CELL=spec['rows'],spec['cols'],spec['cell']
    GRID_W=cols*CELL; GRID_H=rows*CELL
    PLATE_W=GRID_W+2*MARGIN
    PLATE_H=MARGIN+GRID_H+BAND
    GRID_YTOP=PLATE_H-MARGIN
    shapes=[]
    for i,tile in enumerate(spec['solution']):
        r,c=divmod(i,cols)
        cx=MARGIN+(c+0.5)*CELL; cy=GRID_YTOP-(r+0.5)*CELL
        shapes+=cell_shapes(cx,cy,CELL/2,tile)
    # grid frame
    frame=sbox(MARGIN,GRID_YTOP-GRID_H,MARGIN+GRID_W,GRID_YTOP)
    shapes.append((frame.buffer(1.2).difference(frame.buffer(-1.2)),None))
    # QR
    mat=segno.make(spec['url'],error='m').matrix; n=len(mat); ms=QR_SIZE/n
    qx0=(PLATE_W-QR_SIZE)/2; qy1=MARGIN+QR_SIZE
    for i,row in enumerate(mat):
        for j,v in enumerate(row):
            if v:
                x=qx0+j*ms; y=qy1-(i+1)*ms
                shapes.append((sbox(x,y,x+ms*1.02,y+ms*1.02),None))
    # relief 2D
    polys=[]
    for geom,w in shapes:
        polys.append(geom if w is None else geom.buffer(w/2.0,cap_style=2,join_style=1))
    relief2d=unary_union(polys).buffer(0.02).buffer(-0.02)
    # mesh
    meshes=[box(extents=[PLATE_W,PLATE_H,BASE_H])]; meshes[0].apply_translation([PLATE_W/2,PLATE_H/2,BASE_H/2])
    geoms=list(relief2d.geoms) if relief2d.geom_type=='MultiPolygon' else [relief2d]
    for g in geoms:
        if g.area<1e-4: continue
        g=g.buffer(0.002).buffer(-0.002)
        m=extrude_polygon(g,height=RELIEF+0.6); m.apply_translation([0,0,BASE_H-0.6]); m.merge_vertices()
        meshes.append(m)
    try: plate=trimesh.boolean.union(meshes,engine='manifold')
    except Exception as ex: print('  union fallback:',ex); plate=trimesh.util.concatenate(meshes)
    o3=os.path.join(DOCS,spec['name']+'.3mf'); os.path.join(DOCS,spec['name']+'.stl')
    plate.export(o3); plate.export(os.path.join(DOCS,spec['name']+'.stl'))
    segno.make(spec['url'],error='m').save(os.path.join(DOCS,spec['name']+'_qr.svg'),scale=1,border=2,dark='#12233f')
    render_preview(relief2d,PLATE_W,PLATE_H,os.path.join(DOCS,spec['name']+'_preview.png'))
    print(f"  {spec['name']}: {PLATE_W:.0f}x{PLATE_H:.0f}mm  verts={len(plate.vertices)} watertight={plate.is_watertight}")

# ---------------- isometric preview ----------------
def render_preview(relief,W,H,out):
    import matplotlib; matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.path import Path
    from matplotlib.patches import PathPatch, Polygon as MplPoly
    ZT=6.0; CT=math.cos(math.radians(30)); ST=math.sin(math.radians(30))
    iso=lambda x,y,z:((x-y)*CT,(x+y)*ST+z)
    def pp(shape,z):
        v=[];co=[]
        def ring(cs):
            pts=[iso(px,py,z) for px,py in cs]; v.extend(pts)
            co.extend([Path.MOVETO]+[Path.LINETO]*(len(pts)-2)+[Path.CLOSEPOLY])
        ring(list(shape.exterior.coords))
        for h in shape.interiors: ring(list(h.coords))
        return Path(v,co)
    fig,ax=plt.subplots(figsize=(7.2,6),dpi=170); ax.set_aspect('equal'); ax.axis('off')
    c=[(0,0),(W,0),(W,H),(0,H)]
    top=[iso(x,y,ZT) for x,y in c]; bot=[iso(x,y,0) for x,y in c]
    ax.add_patch(MplPoly([bot[0],bot[1],top[1],top[0]],closed=True,fc='#9AACC4',ec='#7d90ab',lw=1))
    ax.add_patch(MplPoly([bot[1],bot[2],top[2],top[1]],closed=True,fc='#B4C2D6',ec='#7d90ab',lw=1))
    ax.add_patch(MplPoly(top,closed=True,fc='#EEF3FA',ec='#7d90ab',lw=1.2))
    for g in (list(relief.geoms) if relief.geom_type=='MultiPolygon' else [relief]):
        if g.area<1e-3: continue
        ax.add_patch(PathPatch(pp(g,ZT+0.2),fc='#15263f',ec='none'))
    ax.add_patch(MplPoly([iso(x+3,y-3,-0.2) for x,y in c],closed=True,fc='#00000018',ec='none',zorder=-5))
    xs=[p[0] for p in top+bot]; ys=[p[1] for p in top+bot]
    ax.set_xlim(min(xs)-8,max(xs)+8); ax.set_ylim(min(ys)-10,max(ys)+10); ax.invert_yaxis()
    plt.tight_layout(pad=0.2); plt.savefig(out,transparent=True,bbox_inches='tight',pad_inches=0.05); plt.close()

# ---------------- plate specs (mirror plate_game.js) ----------------
BASE_URL='https://borenw.github.io/magtile-circuits/'
PLATES=[
 {'name':'master_of_time_plate','rows':3,'cols':3,'cell':36.0,'url':BASE_URL+'game.html','solution':[
    {'e':['bottom','right']},{'e':['left','right'],'c':'res'},{'e':['left','bottom']},
    {'e':['top','right','bottom'],'c':'cap'},{'e':['left','right','bottom'],'c':'inv'},{'e':['left','top','bottom'],'c':'node'},
    {'e':['top','right']},{'e':['left','right','top'],'c':'node'},{'e':['top','left'],'c':'piezo'}]},
 {'name':'make_it_bright_plate','rows':2,'cols':2,'cell':44.0,'url':BASE_URL+'bright.html','solution':[
    {'e':['right','bottom'],'c':'batt'},{'e':['left','bottom'],'c':'led'},
    {'e':['top','right']},{'e':['top','left']}]},
 {'name':'stay_grounded_plate','rows':3,'cols':3,'cell':36.0,'url':BASE_URL+'grounded.html','solution':[
    {'e':['bottom','right']},{'e':['left','right'],'c':'res'},{'e':['left','bottom']},
    {'e':['top','right','bottom'],'c':'cap','touch':True},{'e':['left','right','bottom'],'c':'inv'},{'e':['left','top','bottom'],'c':'node'},
    {'e':['top','right'],'c':'gnd'},{'e':['left','right','top'],'c':'node'},{'e':['top','left'],'c':'piezo'}]},
]
if __name__=='__main__':
    for s in PLATES:
        print('building',s['name']); build_plate(s)
    print('done')
