(function(){
  const data=window.BXR_DATA;
  const transformation=window.BXR_TRANSFORMATION;
  const q=(s)=>document.querySelector(s);
  const qa=(s)=>Array.from(document.querySelectorAll(s));
  const esc=(s)=>String(s??'').replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
  let current='tcja';

  function renderReceipt(r){
    const limits=(r.limits||[]).filter(Boolean).map(x=>`<p class="limit">Limit: ${esc(x)}</p>`).join('');
    const excerpt=r.excerpt?`<details><summary>Show source excerpt</summary><blockquote>${esc(r.excerpt)}</blockquote></details>`:'';
    return `<section class="receipt"><h3>${esc(r.label)}</h3><p class="receipt-meta">${esc(r.section)}${r.heading?' · '+esc(r.heading):''}${r.source?' · '+esc(r.source):''}</p>${limits}${excerpt}</section>`;
  }
  function renderBill(id){
    current=id; const b=data[id];
    q('#eyebrow').textContent=b.eyebrow; q('#story-title').textContent=b.title; q('#dek').textContent=b.dek; q('#short').textContent=b.short;
    q('#story').innerHTML=b.story.map(p=>`<p>${esc(p.text)}</p>`).join('');
    q('#homeworkNote').textContent=b.homework_note;
    q('#receipts').innerHTML=b.receipts.map(renderReceipt).join('');
    qa('.bill-chip').forEach(btn=>btn.classList.toggle('active',btn.dataset.bill===id));
    document.title=`Bill X-Ray — ${b.title}`;
    window.scrollTo({top:0,behavior:'instant'});
  }

  function renderTransformation(){
    const steps=transformation.steps.map((step,i)=>`<section class="ladder-step ${esc(step.tone)}"><div class="ladder-index">${String(i+1).padStart(2,'0')}</div><div><p class="ladder-stage">${esc(step.stage)}</p><h3>${esc(step.title)}</h3><p class="ladder-body">${esc(step.body)}</p><p class="ladder-note">${esc(step.note)}</p></div></section>`).join('');
    const syn=transformation.synthesis[current] || transformation.synthesis.tcja;
    const metrics=syn.metrics.map((m,i)=>`<div class="synthesis-metric"><div class="metric-number">${esc(m.value)}</div><div><p class="metric-label">${esc(m.label)}</p><p class="metric-note">${esc(m.note)}</p></div></div>`).join('');
    const hold=syn.hadToHold.map(x=>`<span>${esc(x)}</span>`).join('');
    q('#transformationBody').innerHTML=`<div class="transformation-intro"><p class="micro-label">REAL EXAMPLE · ${esc(transformation.bill)}</p><h3>${esc(transformation.provision)}</h3><p>${esc(transformation.thesis)}</p></div>${steps}<section class="before-after"><div><p class="micro-label">BEFORE</p><p>${esc(transformation.before)}</p></div><div><p class="micro-label">AFTER</p><p>${esc(transformation.after)}</p></div></section><p class="transformation-closer">${esc(transformation.closer)}</p><section class="synthesis-reveal"><p class="synthesis-eyebrow">${esc(syn.eyebrow)}</p><h3>${esc(syn.title)}</h3><p class="synthesis-intro">${esc(syn.intro)}</p><div class="synthesis-metrics">${metrics}</div><div class="complexity-compare"><div class="complexity-left"><p class="micro-label">WHAT AI HAD TO HOLD</p><div class="complexity-tags">${hold}</div></div><div class="complexity-right"><p class="micro-label">WHAT YOU HAVE TO HOLD</p><blockquote>${esc(syn.humanHold)}</blockquote></div></div><p class="synthesis-doctrine">${esc(syn.doctrine)}</p><p class="synthesis-final">${esc(syn.final)}</p></section>`;
  }
  function openTransformation(){closeDrawer();renderTransformation();q('#transformation').classList.add('open');q('#transformation').setAttribute('aria-hidden','false');q('#transformationButton').setAttribute('aria-expanded','true');q('#scrim').hidden=false;document.body.classList.add('no-scroll');}
  function closeTransformation(){q('#transformation').classList.remove('open');q('#transformation').setAttribute('aria-hidden','true');q('#transformationButton').setAttribute('aria-expanded','false');q('#scrim').hidden=true;document.body.classList.remove('no-scroll');}
  function openDrawer(){q('#homework').classList.add('open');q('#homework').setAttribute('aria-hidden','false');q('#homeworkButton').setAttribute('aria-expanded','true');q('#scrim').hidden=false;}
  function closeDrawer(){q('#homework').classList.remove('open');q('#homework').setAttribute('aria-hidden','true');q('#homeworkButton').setAttribute('aria-expanded','false');q('#scrim').hidden=true;}
  qa('.bill-chip').forEach(btn=>btn.addEventListener('click',()=>{closeDrawer();renderBill(btn.dataset.bill);}));
  q('#homeworkButton').addEventListener('click',openDrawer);q('#closeHomework').addEventListener('click',closeDrawer);
  q('#transformationButton').addEventListener('click',openTransformation);q('#closeTransformation').addEventListener('click',closeTransformation);
  q('#scrim').addEventListener('click',()=>{closeDrawer();closeTransformation();});
  document.addEventListener('keydown',e=>{if(e.key==='Escape'){closeDrawer();closeTransformation();}});
  renderBill(current);
})();
