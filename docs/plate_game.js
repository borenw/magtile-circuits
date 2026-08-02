/* MagTile plate game engine — spec-driven tiles + config-driven puzzle.
   A tile spec: {e:[edges], c:component, k:accent, label, touch}
   edges ∈ top|right|bottom|left ; component ∈
   none|node|res|cap|inv|piezo|led|batt|touch|gnd                         */
(function(global){
const E={top:[60,0],right:[120,60],bottom:[60,120],left:[0,60]};
function key(s){return (s.c||'none')+'|'+[...(s.e||[])].sort().join(',')+(s.touch?'|t':'');}

function draw(spec,ghost){
  const col=ghost?'var(--ghost)':'var(--wire)', w=8, e=spec.e||[], c=spec.c||'none';
  const acc=(x)=>ghost?'var(--ghost)':x;
  const lead=(edge,to=[60,60],cc=col,ww=w)=>{const[x,y]=E[edge];
    return `<path d="M${x} ${y} L${to[0]} ${to[1]}" fill="none" stroke="${cc}" stroke-width="${ww}" stroke-linecap="round"/>`;};
  const dot=(cc)=>`<circle cx="60" cy="60" r="7" fill="${ghost?'var(--ghost)':cc}"/>`;
  let g=`<svg viewBox="0 0 120 120" role="img" aria-label="${c}">`;
  const has=(x)=>e.includes(x);

  if(c==='none'||c==='node'){
    for(const ed of e) g+=lead(ed);
    if(c==='node'||e.length>=3) g+=dot(acc(spec.k||'#0052CC'));
  }
  else if(c==='res'){
    const horiz=has('left')&&has('right');
    if(horiz){ g+=`<path d="M0 60 L40 60" stroke="${col}" stroke-width="${w}" stroke-linecap="round" fill="none"/>`
      +`<polyline points="40,60 46,48 54,72 62,48 70,72 78,48 82,60" fill="none" stroke="${col}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"/>`
      +`<path d="M82 60 L120 60" stroke="${col}" stroke-width="${w}" stroke-linecap="round" fill="none"/>`;}
    else{ g+=`<path d="M60 0 L60 40" stroke="${col}" stroke-width="${w}" stroke-linecap="round" fill="none"/>`
      +`<polyline points="60,40 48,46 72,54 48,62 72,70 48,78 60,82" fill="none" stroke="${col}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"/>`
      +`<path d="M60 82 L60 120" stroke="${col}" stroke-width="${w}" stroke-linecap="round" fill="none"/>`;}
  }
  else if(c==='cap'){                       // IN node: leads (not bottom) + cap on bottom leg
    for(const ed of e){ if(ed!=='bottom') g+=lead(ed); }
    g+=`<path d="M60 60 L60 78" stroke="${col}" stroke-width="${w}" fill="none" stroke-linecap="round"/>`
      +`<line x1="42" y1="80" x2="78" y2="80" stroke="${col}" stroke-width="${w}" stroke-linecap="round"/>`
      +`<line x1="42" y1="92" x2="78" y2="92" stroke="${col}" stroke-width="${w}" stroke-linecap="round"/>`
      +`<path d="M60 92 L60 120" stroke="${col}" stroke-width="${w}" fill="none" stroke-linecap="round"/>`
      +dot(acc('#0052CC'));
    if(spec.touch){                          // touch antenna pad on the RC node
      const tc=ghost?'var(--ghost)':'#974F0C';
      g+=`<path d="M60 60 L98 22" stroke="${tc}" stroke-width="4" stroke-dasharray="5 4" fill="none"/>`
        +`<rect x="84" y="6" width="30" height="24" rx="6" fill="none" stroke="${tc}" stroke-width="4"/>`
        +`<text x="99" y="24" font-size="15" text-anchor="middle">✋</text>`;
    }
  }
  else if(c==='inv'){
    g+=`<path d="M0 60 L44 60" stroke="${col}" stroke-width="${w}" stroke-linecap="round" fill="none"/>`
      +`<path d="M44 34 L44 86 L88 60 Z" fill="#fff" stroke="${col}" stroke-width="6" stroke-linejoin="round"/>`
      +`<circle cx="94" cy="60" r="7" fill="#fff" stroke="${col}" stroke-width="6"/>`
      +`<path d="M101 60 L120 60" stroke="${col}" stroke-width="${w}" stroke-linecap="round" fill="none"/>`
      +`<path d="M60 76 L60 120" stroke="${col}" stroke-width="${w}" stroke-linecap="round" fill="none"/>`;
  }
  else if(c==='piezo'){
    g+=`<path d="M60 0 L60 40" stroke="${col}" stroke-width="${w}" stroke-linecap="round" fill="none"/>`
      +`<path d="M0 60 L40 60" stroke="${col}" stroke-width="${w}" stroke-linecap="round" fill="none"/>`
      +`<circle cx="60" cy="60" r="20" fill="none" stroke="${col}" stroke-width="6"/>`
      +`<circle cx="60" cy="60" r="9" fill="${acc('#DE350B')}"/>`
      +`<path d="M84 44 q10 16 0 32" fill="none" stroke="${acc('#DE350B')}" stroke-width="4" stroke-linecap="round"/>`
      +`<path d="M92 38 q16 22 0 44" fill="none" stroke="${acc('#DE350B')}" stroke-width="4" stroke-linecap="round"/>`;
  }
  else if(c==='led'){
    for(const ed of e) g+=lead(ed);
    g+=`<polygon points="46,48 74,48 60,72" fill="${acc('#DE350B')}"/>`
      +`<line x1="46" y1="76" x2="74" y2="76" stroke="${col}" stroke-width="6" stroke-linecap="round"/>`
      +`<path d="M78 42 l10 -9 M84 50 l10 -9" stroke="${acc('#DE350B')}" stroke-width="4" stroke-linecap="round"/>`;
  }
  else if(c==='batt'){
    for(const ed of e) g+=lead(ed);
    const bc=col;
    g+=`<line x1="48" y1="42" x2="48" y2="78" stroke="${bc}" stroke-width="6"/>`     // long plate +
      +`<line x1="60" y1="52" x2="60" y2="68" stroke="${bc}" stroke-width="9"/>`      // short plate
      +`<line x1="72" y1="42" x2="72" y2="78" stroke="${bc}" stroke-width="6"/>`
      +`<text x="40" y="34" font-size="16" font-weight="800" fill="${acc('#DE350B')}">+</text>`;
  }
  else if(c==='gnd'){                        // explicit ground pad
    for(const ed of e) g+=lead(ed);
    g+=`<path d="M60 60 L60 74" stroke="${col}" stroke-width="${w}" stroke-linecap="round"/>`
      +`<line x1="40" y1="76" x2="80" y2="76" stroke="${col}" stroke-width="6" stroke-linecap="round"/>`
      +`<line x1="47" y1="86" x2="73" y2="86" stroke="${col}" stroke-width="6" stroke-linecap="round"/>`
      +`<line x1="54" y1="96" x2="66" y2="96" stroke="${col}" stroke-width="6" stroke-linecap="round"/>`;
  }
  return g+'</svg>';
}

function shuffle(a,seed){let s=seed||7;for(let i=a.length-1;i>0;i--){s=(s*1103515245+12345)&0x7fffffff;const j=s%(i+1);[a[i],a[j]]=[a[j],a[i]];}return a;}

function build(mount,cfg){
  const sol=cfg.solution, N=sol.length, sz=cfg.cellPx||('var(--sz)');
  mount.innerHTML=`
    <div class="bar">
      <span class="count">Placed: <b class="score">0</b> / ${N}</span>
      <span class="grow"></span>
      <button class="hint" aria-pressed="false">💡 Show labels</button>
      <button class="reset">↺ Reset</button>
    </div>
    <div class="stage">
      <div class="boardwrap">
        <div class="rail v">＋3&nbsp;V</div>
        <div class="board"></div>
        <div class="rail g">GND ⏚</div>
      </div>
      <div class="tray">
        <h2>Tile tray</h2>
        <p>${cfg.trayNote||'Drag a tile onto its square — or tap a tile, then tap a square.'}</p>
        <div class="tiles"></div>
        <div class="win"><h2>${cfg.winTitle||'⚡ It works!'}</h2><p>${cfg.winMsg||''}</p></div>
        <div class="touchpad">
          <div class="pad">👆 Hold &amp; slide — “touch the node”<br><small>your body adds capacitance → the pitch bends</small></div>
          <button class="sound" aria-pressed="false">🔈 Sound: off</button>
        </div>
      </div>
    </div>`;
  const grid=mount.querySelector('.board'), tray=mount.querySelector('.tiles');
  const scoreEl=mount.querySelector('.score');
  const cpx=cfg.cellPx?cfg.cellPx+'px':'var(--sz)';
  grid.style.gridTemplateColumns=`repeat(${cfg.cols},${cpx})`;
  grid.style.gridTemplateRows=`repeat(${cfg.rows},${cpx})`;
  document.documentElement.style.setProperty('--sz','112px');
  let placed=0, picked=null;

  const cells=[];
  function paintGhosts(){
    grid.innerHTML=''; cells.length=0;
    sol.forEach((s,i)=>{const c=document.createElement('div');
      c.className='cell'; c.style.width=cpx; c.style.height=cpx;
      c.dataset.key=key(s); c.innerHTML=draw(s,true); grid.appendChild(c); cells.push(c);});
  }
  let order;
  function buildTray(){
    tray.innerHTML='';
    order=shuffle([...Array(N).keys()], cfg.seed);
    order.forEach(i=>{const s=sol[i];const t=document.createElement('div');
      t.className='tile'; t.dataset.key=key(s); t.draggable=true;
      t.innerHTML=draw(s,false)+`<span class="nm">${s.label||''}</span>`; tray.appendChild(t);});
  }
  function findTile(k){return [...tray.querySelectorAll('.tile')].find(t=>t.dataset.key===k);}
  function place(t,c){
    if(c.classList.contains('filled'))return false;
    if(t.dataset.key!==c.dataset.key){c.classList.add('bad');setTimeout(()=>c.classList.remove('bad'),350);return false;}
    c.classList.remove('drop');c.classList.add('filled');
    c.innerHTML=draw(sol[cells.indexOf(c)],false);
    t.remove();placed++;scoreEl.textContent=placed;
    if(picked===t)picked=null;
    if(placed===N)win();
    return true;
  }
  tray.addEventListener('click',e=>{const t=e.target.closest('.tile');if(!t)return;
    if(picked===t){picked.classList.remove('sel');picked=null;return;}
    if(picked)picked.classList.remove('sel');picked=t;t.classList.add('sel');});
  grid.addEventListener('click',e=>{const c=e.target.closest('.cell');if(!c||!picked)return;
    if(!place(picked,c)&&picked)picked.classList.remove('sel');});
  let dragKey=null;
  tray.addEventListener('dragstart',e=>{const t=e.target.closest('.tile');if(!t)return;
    dragKey=t.dataset.key;t.classList.add('drag');e.dataTransfer.setData('text/plain',dragKey);});
  tray.addEventListener('dragend',e=>{const t=e.target.closest('.tile');if(t)t.classList.remove('drag');});
  grid.addEventListener('dragover',e=>{e.preventDefault();const c=e.target.closest('.cell');
    if(c&&!c.classList.contains('filled'))c.classList.add('drop');});
  grid.addEventListener('dragleave',e=>{const c=e.target.closest('.cell');if(c)c.classList.remove('drop');});
  grid.addEventListener('drop',e=>{e.preventDefault();const c=e.target.closest('.cell');if(!c||!dragKey)return;
    const t=findTile(dragKey);c.classList.remove('drop');if(t)place(t,c);dragKey=null;});
  let ptTile=null,ghostEl=null;
  tray.addEventListener('pointerdown',e=>{if(e.pointerType==='mouse')return;
    const t=e.target.closest('.tile');if(!t)return;ptTile=t;ghostEl=t.cloneNode(true);
    ghostEl.className='tile drag-ghost';document.body.appendChild(ghostEl);mv(e);t.setPointerCapture(e.pointerId);});
  tray.addEventListener('pointermove',e=>{if(ptTile)mv(e);});
  tray.addEventListener('pointerup',e=>{if(!ptTile)return;
    const el=document.elementFromPoint(e.clientX,e.clientY),c=el&&el.closest('.cell');
    if(c)place(ptTile,c);if(ghostEl){ghostEl.remove();ghostEl=null;}ptTile=null;});
  function mv(e){if(ghostEl){ghostEl.style.left=e.clientX+'px';ghostEl.style.top=e.clientY+'px';}}

  mount.querySelector('.hint').addEventListener('click',e=>{
    const on=document.body.classList.toggle('hint-off')===false;e.currentTarget.setAttribute('aria-pressed',on);});
  mount.querySelector('.reset').addEventListener('click',()=>{
    placed=0;picked=null;scoreEl.textContent=0;
    mount.querySelector('.win').classList.remove('show');
    mount.querySelector('.touchpad').classList.remove('show');stopTone();
    paintGhosts();buildTray();});

  /* Web Audio touch-theremin */
  let actx=null,osc=null,gain=null,soundOn=false; const BASE=(cfg.tone&&cfg.tone.base)||2700;
  const soundBtn=mount.querySelector('.sound'), pad=mount.querySelector('.pad');
  function startTone(){if(!actx)actx=new (global.AudioContext||global.webkitAudioContext)();
    osc=actx.createOscillator();gain=actx.createGain();osc.type='square';osc.frequency.value=BASE;
    gain.gain.value=0.06;osc.connect(gain);gain.connect(actx.destination);osc.start();}
  function stopTone(){if(osc){try{osc.stop();}catch(_){}}osc=null;soundOn=false;
    if(soundBtn){soundBtn.setAttribute('aria-pressed',false);soundBtn.textContent='🔈 Sound: off';}}
  soundBtn.addEventListener('click',e=>{soundOn=!soundOn;
    if(soundOn){startTone();e.currentTarget.setAttribute('aria-pressed',true);e.currentTarget.textContent='🔊 Sound: on';}
    else stopTone();});
  function bend(ev){if(!osc)return;const r=pad.getBoundingClientRect();
    const x=Math.min(1,Math.max(0,((ev.clientX??r.left)-r.left)/r.width));
    osc.frequency.setTargetAtTime(BASE*Math.pow(0.28,x),actx.currentTime,0.02);}
  function unbend(){if(osc)osc.frequency.setTargetAtTime(BASE,actx.currentTime,0.05);}
  pad.addEventListener('pointerdown',e=>{pad.setPointerCapture(e.pointerId);bend(e);});
  pad.addEventListener('pointermove',e=>{if(e.buttons||e.pointerType!=='mouse')bend(e);});
  pad.addEventListener('pointerup',unbend);pad.addEventListener('pointerleave',unbend);

  function win(){mount.querySelector('.win').classList.add('show');
    if(cfg.tone!==false)mount.querySelector('.touchpad').classList.add('show');
    cells.forEach((c,i)=>setTimeout(()=>c.style.filter='drop-shadow(0 0 6px #00A870)',i*70));}

  paintGhosts();buildTray();
}
global.PlateGame={draw,key,build};
})(window);
