# -*- coding: utf-8 -*-
# Generate a print-ready HTML for the RC-oscillator (MagTile) project.
# Tile cards are drawn at EXACTLY 1.5 in so they register to real 1.5" tiles.

C = dict(blue="#0052CC", blued="#0747A6", ink="#172B4D", sub="#5E6C84",
         line="#DFE1E6", red="#DE350B", amber="#FF991F", purple="#6554C0",
         copper="#B7602F", green="#36B37E", cell="#F4F8FF", redbg="#FFEBE6")

# ---- tile card SVGs (viewBox 0 0 150 150) -------------------------------
def frame(inner, fill=C["cell"], stroke=C["blue"]):
    return (f'<svg viewBox="0 0 150 150" class="tsvg">'
            f'<rect x="4" y="4" width="142" height="142" rx="14" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="2.5"/>{inner}</svg>')

def edge(side, label, color):
    # small colored edge bar + label
    if side == "N":  bar=f'<line x1="45" y1="10" x2="105" y2="10" stroke="{color}" stroke-width="5"/>'; t=f'<text x="75" y="26" text-anchor="middle" class="el" fill="{color}">{label}</text>'
    if side == "S":  bar=f'<line x1="45" y1="140" x2="105" y2="140" stroke="{color}" stroke-width="5"/>'; t=f'<text x="75" y="132" text-anchor="middle" class="el" fill="{color}">{label}</text>'
    if side == "W":  bar=f'<line x1="10" y1="45" x2="10" y2="105" stroke="{color}" stroke-width="5"/>'; t=f'<text x="16" y="78" text-anchor="start" class="el" fill="{color}">{label}</text>'
    if side == "E":  bar=f'<line x1="140" y1="45" x2="140" y2="105" stroke="{color}" stroke-width="5"/>'; t=f'<text x="134" y="78" text-anchor="end" class="el" fill="{color}">{label}</text>'
    return bar + t

def t_power():
    inner = (edge("N","+3V",C["red"]) + edge("S","GND",C["ink"]) +
             '<text x="75" y="70" text-anchor="middle" font-size="34">\U0001F50B</text>'
             f'<text x="75" y="96" text-anchor="middle" class="tv" fill="{C["ink"]}">CR2032</text>'
             f'<text x="75" y="112" text-anchor="middle" class="ts">3 V power</text>')
    return frame(inner)

def t_inverter():
    inner = (edge("N","+V",C["red"]) + edge("S","GND",C["ink"]) +
             edge("W","IN",C["blued"]) + edge("E","OUT",C["purple"]) +
             f'<path d="M52 55 L52 95 L96 75 Z" fill="#fff" stroke="{C["ink"]}" stroke-width="2.5"/>'
             f'<path d="M63 70 h7 v6 h7 M63 80 h7 v-6 h7" fill="none" stroke="{C["blue"]}" stroke-width="1.4"/>'
             f'<circle cx="102" cy="75" r="6" fill="#fff" stroke="{C["ink"]}" stroke-width="2.5"/>'
             f'<text x="75" y="120" text-anchor="middle" class="ts">74LVC1G14</text>')
    return frame(inner)

def zig(x0,x1,y,col):
    # horizontal zigzag resistor between x0..x1 at y
    n=6; import_=""; pts=[]
    seg=(x1-x0)/(n)
    up=True
    pts.append((x0,y))
    for i in range(n):
        x=x0+seg*(i+0.5)
        pts.append((x, y-8 if up else y+8)); up=not up
    pts.append((x1,y))
    p=" ".join(f"{px:.1f},{py:.1f}" for px,py in pts)
    return f'<polyline points="{p}" fill="none" stroke="{col}" stroke-width="3"/>'

def t_res(name, val, col=None):
    col = col or C["ink"]
    inner = (edge("W","",col) + edge("E","",col) +
             f'<line x1="10" y1="75" x2="40" y2="75" stroke="{col}" stroke-width="3"/>'+
             zig(40,110,75,col)+
             f'<line x1="110" y1="75" x2="140" y2="75" stroke="{col}" stroke-width="3"/>'
             f'<text x="75" y="48" text-anchor="middle" class="tv" fill="{col}">{name}</text>'
             f'<text x="75" y="112" text-anchor="middle" class="tvb" fill="{col}">{val}</text>')
    return frame(inner)

def t_cap():
    col=C["amber"]
    inner = (edge("N","",C["ink"]) + edge("S","GND",C["ink"]) +
             f'<line x1="75" y1="10" x2="75" y2="60" stroke="{C["ink"]}" stroke-width="3"/>'
             f'<line x1="52" y1="60" x2="98" y2="60" stroke="{col}" stroke-width="5"/>'
             f'<line x1="52" y1="74" x2="98" y2="74" stroke="{col}" stroke-width="5"/>'
             f'<text x="105" y="58" class="tv" fill="{col}">+</text>'
             f'<line x1="75" y1="74" x2="75" y2="140" stroke="{C["ink"]}" stroke-width="3"/>'
             f'<text x="75" y="112" text-anchor="middle" class="tvb" fill="{col}">C1 10µF</text>')
    return frame(inner)

def t_led():
    col=C["red"]
    inner = (edge("N","in",C["ink"]) + edge("S","−",C["ink"]) +
             f'<line x1="75" y1="10" x2="75" y2="52" stroke="{C["ink"]}" stroke-width="3"/>'
             f'<polygon points="58,52 92,52 75,82" fill="{col}"/>'
             f'<line x1="58" y1="86" x2="92" y2="86" stroke="{C["ink"]}" stroke-width="3"/>'
             f'<path d="M95 50 l10 -8 M100 58 l10 -8" stroke="{col}" stroke-width="2"/>'
             f'<line x1="75" y1="86" x2="75" y2="140" stroke="{C["ink"]}" stroke-width="3"/>'
             f'<text x="75" y="112" text-anchor="middle" class="tvb" fill="{col}">LED (red)</text>')
    return frame(inner)

def t_wire_straight(role=""):
    inner = (f'<line x1="75" y1="8" x2="75" y2="142" stroke="{C["ink"]}" stroke-width="5"/>'
             f'<text x="75" y="126" text-anchor="middle" class="ts">{role}</text>')
    return frame(inner)

def t_wire_elbow(role=""):
    # elbow from N to E (rotate visually is fine; label tells role)
    inner = (f'<polyline points="75,8 75,75 142,75" fill="none" stroke="{C["ink"]}" '
             f'stroke-width="5" stroke-linejoin="round" stroke-linecap="round"/>'
             f'<text x="60" y="126" text-anchor="middle" class="ts">{role}</text>')
    return frame(inner)

def t_wire_T(role=""):
    inner = (f'<line x1="8" y1="75" x2="142" y2="75" stroke="{C["ink"]}" stroke-width="5"/>'
             f'<line x1="75" y1="75" x2="75" y2="142" stroke="{C["ink"]}" stroke-width="5"/>'
             f'<circle cx="75" cy="75" r="7" fill="{C["blue"]}"/>'
             f'<text x="75" y="126" text-anchor="middle" class="ts">{role}</text>')
    return frame(inner)

# ---- the tile set for the single-inverter blinker (matches the floorplan) ----
CARDS = [
    ("Power",        t_power()),
    ("Inverter",     t_inverter()),
    ("R1 feedback",  t_res("R1", "120 kΩ", C["purple"])),
    ("R2 LED limit", t_res("R2", "330 Ω")),
    ("Capacitor",    t_cap()),
    ("LED",          t_led()),
    ("T — IN node",   t_wire_T("IN")),
    ("T — OUT node",  t_wire_T("OUT")),
    ("Elbow",        t_wire_elbow("elbow")),
    ("Elbow",        t_wire_elbow("elbow")),
    ("Elbow",        t_wire_elbow("elbow")),
    ("Straight — GND", t_wire_straight("GND")),
]

cards_html = "\n".join(
    f'<div class="card"><div class="tile">{svg}</div><div class="cap">{name}</div></div>'
    for name, svg in CARDS)

# schematic (compact redraw of the single-inverter oscillator)
SCHEM = f'''<svg viewBox="0 0 640 300" class="schem" role="img" aria-label="RC oscillator schematic">
  <line x1="110" y1="170" x2="110" y2="56" stroke="{C['purple']}" stroke-width="2.5"/>
  <line x1="110" y1="56" x2="205" y2="56" stroke="{C['purple']}" stroke-width="2.5"/>
  <polyline points="205,56 213,48 227,64 241,48 255,64 269,48 283,64 291,56" fill="none" stroke="{C['purple']}" stroke-width="2.5"/>
  <line x1="291" y1="56" x2="380" y2="56" stroke="{C['purple']}" stroke-width="2.5"/>
  <line x1="380" y1="56" x2="380" y2="170" stroke="{C['purple']}" stroke-width="2.5"/>
  <text x="248" y="40" text-anchor="middle" font-size="12" font-weight="700" fill="{C['purple']}">R1 120kΩ (feedback)</text>
  <path d="M210 135 L210 205 L292 170 Z" fill="{C['cell']}" stroke="{C['ink']}" stroke-width="2.5"/>
  <path d="M228 163 h11 v9 h11 M228 177 h11 v-9 h11" fill="none" stroke="{C['blue']}" stroke-width="1.6"/>
  <circle cx="300" cy="170" r="8" fill="#fff" stroke="{C['ink']}" stroke-width="2.5"/>
  <line x1="110" y1="170" x2="210" y2="170" stroke="{C['ink']}" stroke-width="2.5"/>
  <circle cx="110" cy="170" r="4.5" fill="{C['blue']}"/>
  <text x="96" y="164" text-anchor="end" font-size="11.5" font-weight="700" fill="{C['blued']}">IN</text>
  <line x1="308" y1="170" x2="380" y2="170" stroke="{C['ink']}" stroke-width="2.5"/>
  <circle cx="380" cy="170" r="4.5" fill="{C['purple']}"/>
  <text x="388" y="165" font-size="11.5" font-weight="700" fill="#403294">OUT</text>
  <line x1="250" y1="135" x2="250" y2="96" stroke="{C['red']}" stroke-width="2.5"/>
  <polygon points="250,86 245,98 255,98" fill="{C['red']}"/>
  <text x="250" y="80" text-anchor="middle" font-size="11" font-weight="700" fill="{C['red']}">+3V</text>
  <line x1="250" y1="205" x2="250" y2="270" stroke="{C['ink']}" stroke-width="2.5"/>
  <line x1="110" y1="170" x2="110" y2="215" stroke="{C['amber']}" stroke-width="2.5"/>
  <line x1="88" y1="215" x2="132" y2="215" stroke="{C['amber']}" stroke-width="3.5"/>
  <line x1="88" y1="227" x2="132" y2="227" stroke="{C['amber']}" stroke-width="3.5"/>
  <line x1="110" y1="227" x2="110" y2="270" stroke="{C['amber']}" stroke-width="2.5"/>
  <text x="80" y="200" text-anchor="end" font-size="11" font-weight="700" fill="#B8620F">C1 10µF</text>
  <line x1="380" y1="170" x2="410" y2="170" stroke="{C['ink']}" stroke-width="2.5"/>
  <polyline points="410,170 418,162 432,178 446,162 460,178 474,162 482,170" fill="none" stroke="{C['ink']}" stroke-width="2.5"/>
  <line x1="482" y1="170" x2="520" y2="170" stroke="{C['ink']}" stroke-width="2.5"/>
  <text x="446" y="154" text-anchor="middle" font-size="11" font-weight="700" fill="{C['ink']}">R2 330Ω</text>
  <line x1="520" y1="170" x2="520" y2="206" stroke="{C['ink']}" stroke-width="2.5"/>
  <polygon points="506,206 534,206 520,230" fill="{C['red']}"/>
  <line x1="506" y1="232" x2="534" y2="232" stroke="{C['ink']}" stroke-width="2.5"/>
  <text x="548" y="220" font-size="11" font-weight="700" fill="{C['red']}">LED</text>
  <line x1="520" y1="232" x2="520" y2="270" stroke="{C['ink']}" stroke-width="2.5"/>
  <line x1="90" y1="270" x2="545" y2="270" stroke="{C['ink']}" stroke-width="3"/>
  <text x="551" y="274" font-size="11" font-weight="700" fill="{C['ink']}">GND</text>
</svg>'''

# ---- assembled solution floorplan (reuse the exact SVG from index.html) ----
# Namespace its internal CSS classes so they don't collide with the page styles.
_idx = open("/Users/boren_wang/repos/magtile-circuits/docs/index.html").read()
_i = _idx.index('<svg viewBox="0 0 780 520"')
_j = _idx.index('</svg>', _i) + len('</svg>')
SOLUTION_SVG = _idx[_i:_j]
for _a, _b in (("cell","fcell"), ("fb","ffb"), ("lab","flab"),
               ("tt","ftt"), ("sm","fsm"), ("w","fw")):
    SOLUTION_SVG = SOLUTION_SVG.replace("." + _a + "{", "." + _b + "{")
    SOLUTION_SVG = SOLUTION_SVG.replace('class="' + _a + '"', 'class="' + _b + '"')

PAGE3 = f'''<div class="page">
  <h1>\U00002705 Solution — snap the tiles into the blinker</h1>
  <p class="sub">The twelve cut-outs from the previous page, connected on the grid so the built patch reads exactly like the schematic — this layout <b>is</b> the 1-second oscillator.</p>
  <h2>Assembled floorplan</h2>
  <div class="floorbox">{SOLUTION_SVG}</div>
  <div class="row">
    <div class="col">
      <div class="box tip">
        <div class="lab">✅ How the nets route</div>
        <b>Feedback (purple):</b> IN → elbow up → <b>R1 120 kΩ</b> → elbow down → OUT.
        <b>IN node (T):</b> joins the inverter input, C1 top, and the feedback return.
        <b>OUT node (T):</b> joins the inverter output, the feedback, and R2.
        <b>C1</b> drops IN → GND; <b>R2 → LED</b> drops OUT → GND.
      </div>
    </div>
    <div class="col">
      <div class="box note">
        <div class="lab">\U0001F50C Power delivery</div>
        +3 V / GND are drawn as the outer rails so the signal paths stay clear, but are physically delivered from the <b>Layer-2 VCC/GND plane</b>: every tile taps power from a rail tile below through a via — never by competing for a signal edge.
      </div>
    </div>
  </div>
  <div class="foot">MagTile Circuits · borenw.github.io/magtile-circuits · Page 38 of Bo’s Engineering Curriculum</div>
</div>'''

HTML = f'''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<title>MagTile RC Oscillator — Printable</title>
<style>
  @page {{ size: Letter; margin: 0.5in; }}
  * {{ box-sizing: border-box; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
  html,body {{ margin:0; color:{C['ink']};
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; }}
  h1 {{ font-size:20px; margin:0 0 2px; color:{C['blued']}; }}
  h2 {{ font-size:14px; margin:14px 0 4px; color:{C['blued']};
        border-left:4px solid {C['blue']}; padding-left:8px; }}
  .sub {{ color:{C['sub']}; font-size:11px; margin:0 0 6px; }}
  .page {{ page-break-after: always; }}
  .page:last-child {{ page-break-after: auto; }}
  .schem {{ width:100%; max-height:2.6in; display:block; border:1px solid {C['line']}; border-radius:6px; }}
  .floorbox {{ border:1px solid {C['line']}; border-radius:6px; padding:8px; margin:6px 0; }}
  .floorbox svg {{ width:100%; height:auto; max-height:5in; display:block; }}
  ol {{ font-size:11.5px; line-height:1.5; margin:4px 0 4px 18px; padding:0; }}
  ol li {{ margin:2px 0; }}
  .row {{ display:flex; gap:12px; align-items:flex-start; }}
  .col {{ flex:1; }}
  .box {{ border:1px solid {C['line']}; border-radius:6px; padding:7px 10px; font-size:11px; margin:6px 0; }}
  .tip {{ background:#E3FCEF; border-color:#ABF5D1; }}
  .note {{ background:#EAE6FF; border-color:#C0B6F2; }}
  .lab {{ font-weight:800; font-size:10px; letter-spacing:.05em; text-transform:uppercase; margin-bottom:2px; }}
  table {{ border-collapse:collapse; width:100%; font-size:10.5px; margin-top:4px; }}
  th,td {{ border:1px solid {C['line']}; padding:3px 6px; text-align:left; }}
  th {{ background:{C['blue']}; color:#fff; }}
  /* --- cut-out cards --- */
  .cut-head {{ display:flex; justify-content:space-between; align-items:flex-end; }}
  .ruler {{ display:flex; align-items:center; gap:6px; font-size:9.5px; color:{C['sub']}; }}
  .ruler .bar {{ width:1in; height:8px; border:1.5px solid {C['ink']}; border-top:none; }}
  .grid {{ display:flex; flex-wrap:wrap; gap:0.28in; margin-top:10px; }}
  .card {{ width:1.5in; }}
  .tile {{ width:1.5in; height:1.5in; border:1.4px dashed {C['sub']}; border-radius:2px;
           padding:0; overflow:hidden; }}
  .tsvg {{ width:100%; height:100%; display:block; }}
  .cap {{ font-size:8.5px; text-align:center; color:{C['sub']}; margin-top:2px; }}
  .tv {{ font-size:15px; font-weight:800; }}
  .tvb {{ font-size:12px; font-weight:800; }}
  .ts {{ font-size:9px; fill:{C['sub']}; }}
  .el {{ font-size:11px; font-weight:700; }}
  .foot {{ font-size:9.5px; color:{C['sub']}; margin-top:10px; border-top:1px solid {C['line']}; padding-top:5px; }}
</style></head><body>

<div class="page">
  <h1>\U0001F9E9 MagTile Circuits — Project 2: Be a Time Master</h1>
  <p class="sub">1-second LED blinker · single 74LVC1G14 Schmitt-trigger RC oscillator · 3 V CR2032 · printable build sheet</p>

  <h2>The circuit</h2>
  {SCHEM}

  <div class="row">
    <div class="col">
      <h2>Part 1 — Build the 1-second blink</h2>
      <ol>
        <li>Lay the <b>power rails</b>: \U0001F50B tile at the left, +3 V on top, GND on the bottom.</li>
        <li>Drop the <b>inverter</b> in the center — IN faces left, OUT faces right.</li>
        <li>Run the <b>feedback</b> across the top: elbow → <b>R1 120 kΩ</b> → elbow back down to OUT. Put a <b>T</b> at IN and at OUT.</li>
        <li>Hang <b>C1 10 µF</b> from the IN node down to GND.</li>
        <li>From OUT, go through <b>R2 330 Ω</b> → elbow → <b>LED</b> → GND.</li>
        <li>Power up. The LED should blink about <b>once per second</b> (“one-Mississippi”).</li>
      </ol>
    </div>
    <div class="col">
      <h2>Why it’s one second</h2>
      <table>
        <tr><th>Quantity</th><th>Value</th></tr>
        <tr><td>τ = R1·C1</td><td>1.20 s</td></tr>
        <tr><td>Schmitt factor k</td><td>0.83</td></tr>
        <tr><td>Period T = τ·k</td><td>≈ 1.0 s</td></tr>
        <tr><td>Blink rate</td><td>≈ 1 Hz</td></tr>
      </table>
      <div class="box note">
        <div class="lab">\U0001F3AF Part 2 — make it blink faster</div>
        Get it to <b>2 blinks per second</b>. Hint: the period is <b>τ = R1 × C1</b> — which one tile do you shrink?
      </div>
      <div class="box tip">
        <div class="lab">✅ Answer</div>
        Halve <b>either</b> tile: R1 120 kΩ → <b>62 kΩ</b>, or C1 10 µF → <b>4.7 µF</b>. Bigger = slower. R2 only sets brightness.
      </div>
    </div>
  </div>
  <div class="foot">MagTile Circuits · borenw.github.io/magtile-circuits · Page 38 of Bo’s Engineering Curriculum</div>
</div>

<div class="page">
  <div class="cut-head">
    <div>
      <h1>✂️ Cut-out tiles — 1.5 in</h1>
      <p class="sub">Each dashed square is exactly 1.5&nbsp;in to match your tiles. Cut on the dashed lines and lay them out to match the schematic.</p>
    </div>
    <div class="ruler"><span>print-scale check &rarr;</span><div><div class="bar"></div>1 inch</div></div>
  </div>
  <div class="grid">
    {cards_html}
  </div>
  <div class="foot">Print at <b>100% / Actual size</b> (no “fit to page”). Verify the 1-inch bar above measures 1 inch, then the tiles are true 1.5 in. · borenw.github.io/magtile-circuits</div>
</div>

{PAGE3}

</body></html>'''

import os
_OUT = os.path.dirname(os.path.abspath(__file__))
open(os.path.join(_OUT, "rc_printable.html"), "w").write(HTML)
print("wrote rc_printable.html", len(HTML), "bytes,", len(CARDS), "cards")
