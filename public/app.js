(function(){
  const data=window.BXR_DATA;
  const transformation=window.BXR_TRANSFORMATION;
  const businessLens=window.BXR_BUSINESS_LENS;
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
    const hasLens=id==='sb1570' && businessLens && businessLens.bill_id==='sb1570';
    q('#businessLensButton').hidden=!hasLens; q('#businessLensHint').hidden=!hasLens;
    qa('.bill-chip').forEach(btn=>btn.classList.toggle('active',btn.dataset.bill===id));
    document.title=`Bill X-Ray — ${b.title}`;
    window.scrollTo({top:0,behavior:'instant'});
  }

  function renderBusinessLens(){
    const lens=businessLens;
    const sections=lens.executive_sections.map(s=>`<section class="lens-section"><p class="micro-label">${esc(s.label)}</p><h3>${esc(s.title)}</h3><p>${esc(s.body)}</p></section>`).join('');
    const clock=lens.opportunity_clock.map(x=>`<section class="clock-card"><p class="clock-period">${esc(x.period)}</p><h3>${esc(x.stage)}</h3><dl><dt>What might be happening</dt><dd>${esc(x.happening)}</dd><dt>Public evidence</dt><dd>${esc(x.evidence)}</dd><dt>Where to look</dt><dd>${esc(x.where)}</dd><dt>What it proves</dt><dd>${esc(x.proves)}</dd><dt>What it does not prove</dt><dd>${esc(x.not_proves)}</dd><dt>Ask next</dt><dd>${esc(x.next_question)}</dd></dl></section>`).join('');
    const prints=lens.fingerprints.map(x=>`<section class="fingerprint"><h3>${esc(x.name)}</h3><p><strong>Observed signals:</strong> ${esc(x.signals)}</p><p><strong>Likely meaning:</strong> ${esc(x.meaning)}</p><p><strong>Alternative explanation:</strong> ${esc(x.alternative)}</p><p><strong>Evidence confidence:</strong> ${esc(x.confidence)}</p><p><strong>Approximate maturity:</strong> ${esc(x.maturity)}</p><p><strong>Next human question:</strong> ${esc(x.next_question)}</p></section>`).join('');
    const radar=lens.qualification_radar.map(x=>`<li><strong>${esc(x.question)}</strong><span>${esc(x.proof)}</span></li>`).join('');
    const spoilers=lens.spoilers.map(x=>`<li>${esc(x)}</li>`).join('');
    const red=lens.red_team.map(x=>`<li>${esc(x)}</li>`).join('');
    const five=lens.five_things.map((x,i)=>`<li><span>${i+1}</span><p>${esc(x)}</p></li>`).join('');
    q('#businessLensBody').innerHTML=`<div class="lens-disclaimer">${esc(lens.disclaimer)}</div><section class="lens-opening"><h3>${esc(lens.premise)}</h3><p>${esc(lens.opening)}</p></section>${sections}<section class="lens-major"><p class="micro-label">WORKING BACKWARD FROM PROCUREMENT</p><h2>The Illinois Opportunity Clock</h2><p class="lens-caveat">${esc(lens.clock_caveat)}</p><div class="clock-grid">${clock}</div></section><section class="lens-major"><p class="micro-label">COMBINATIONS, NOT KEYWORDS</p><h2>Opportunity fingerprints</h2><div class="fingerprint-grid">${prints}</div></section><section class="lens-major golden"><p class="micro-label">THE GOLDEN WINDOW</p><h2>${esc(lens.golden_window.title)}</h2><p>${esc(lens.golden_window.body)}</p><p class="boundary">${esc(lens.golden_window.boundary)}</p></section><section class="lens-split"><div><p class="micro-label">WHAT COULD SPOIL IT?</p><ul>${spoilers}</ul></div><div><p class="micro-label">QUALIFICATION RADAR</p><p class="capability-rule">Capability is not qualification proof.</p><ul class="qualification-list">${radar}</ul></div></section><section class="lens-major"><p class="micro-label">RED TEAM</p><h2>Keep the unknowns visible</h2><ul class="red-team-list">${red}</ul></section><section class="five-things"><p class="micro-label">FINAL EXECUTIVE REDUCTION</p><h2>Five things to know</h2><ol>${five}</ol></section>`;
  }

  function renderTransformation(){
    const ex=(transformation.examples&&transformation.examples[current]) || transformation;
    const steps=ex.steps.map((step,i)=>`<section class="ladder-step ${esc(step.tone)}"><div class="ladder-index">${String(i+1).padStart(2,'0')}</div><div><p class="ladder-stage">${esc(step.stage)}</p><h3>${esc(step.title)}</h3><p class="ladder-body">${esc(step.body)}</p><p class="ladder-note">${esc(step.note)}</p></div></section>`).join('');
    const syn=transformation.synthesis[current] || transformation.synthesis.tcja;
    const metrics=syn.metrics.map((m,i)=>`<div class="synthesis-metric"><div class="metric-number">${esc(m.value)}</div><div><p class="metric-label">${esc(m.label)}</p><p class="metric-note">${esc(m.note)}</p></div></div>`).join('');
    const hold=syn.hadToHold.map(x=>`<span>${esc(x)}</span>`).join('');
    q('#transformationBody').innerHTML=`<div class="transformation-intro"><p class="micro-label">REAL EXAMPLE · ${esc(ex.bill)}</p><h3>${esc(ex.provision)}</h3><p>${esc(ex.thesis)}</p></div>${steps}<section class="before-after"><div><p class="micro-label">BEFORE</p><p>${esc(ex.before)}</p></div><div><p class="micro-label">AFTER</p><p>${esc(ex.after)}</p></div></section><p class="transformation-closer">${esc(ex.closer)}</p><section class="synthesis-reveal"><p class="synthesis-eyebrow">${esc(syn.eyebrow)}</p><h3>${esc(syn.title)}</h3><p class="synthesis-intro">${esc(syn.intro)}</p><div class="synthesis-metrics">${metrics}</div><div class="complexity-compare"><div class="complexity-left"><p class="micro-label">WHAT AI HAD TO HOLD</p><div class="complexity-tags">${hold}</div></div><div class="complexity-right"><p class="micro-label">WHAT YOU HAVE TO HOLD</p><blockquote>${esc(syn.humanHold)}</blockquote></div></div><p class="synthesis-doctrine">${esc(syn.doctrine)}</p><p class="synthesis-final">${esc(syn.final)}</p></section>`;
  }
  function openTransformation(){closeDrawer();renderTransformation();q('#transformation').classList.add('open');q('#transformation').setAttribute('aria-hidden','false');q('#transformationButton').setAttribute('aria-expanded','true');q('#scrim').hidden=false;document.body.classList.add('no-scroll');}
  function closeTransformation(){q('#transformation').classList.remove('open');q('#transformation').setAttribute('aria-hidden','true');q('#transformationButton').setAttribute('aria-expanded','false');q('#scrim').hidden=true;document.body.classList.remove('no-scroll');}
  function openBusinessLens(){closeDrawer();closeTransformation();renderBusinessLens();q('#businessLens').classList.add('open');q('#businessLens').setAttribute('aria-hidden','false');q('#businessLensButton').setAttribute('aria-expanded','true');q('#scrim').hidden=false;document.body.classList.add('no-scroll');}
  function closeBusinessLens(){q('#businessLens').classList.remove('open');q('#businessLens').setAttribute('aria-hidden','true');q('#businessLensButton').setAttribute('aria-expanded','false');q('#scrim').hidden=true;document.body.classList.remove('no-scroll');}
  function openDrawer(){q('#homework').classList.add('open');q('#homework').setAttribute('aria-hidden','false');q('#homeworkButton').setAttribute('aria-expanded','true');q('#scrim').hidden=false;}
  function closeDrawer(){q('#homework').classList.remove('open');q('#homework').setAttribute('aria-hidden','true');q('#homeworkButton').setAttribute('aria-expanded','false');q('#scrim').hidden=true;}
  qa('.bill-chip').forEach(btn=>btn.addEventListener('click',()=>{closeDrawer();renderBill(btn.dataset.bill);}));
  q('#homeworkButton').addEventListener('click',openDrawer);q('#closeHomework').addEventListener('click',closeDrawer);
  q('#transformationButton').addEventListener('click',openTransformation);q('#closeTransformation').addEventListener('click',closeTransformation);
  q('#businessLensButton').addEventListener('click',openBusinessLens);q('#closeBusinessLens').addEventListener('click',closeBusinessLens);
  q('#scrim').addEventListener('click',()=>{closeDrawer();closeTransformation();closeBusinessLens();q('#scrim').hidden=true;});
  document.addEventListener('keydown',e=>{if(e.key==='Escape'){closeDrawer();closeTransformation();closeBusinessLens();q('#scrim').hidden=true;}});
  renderBill(current);
})();
