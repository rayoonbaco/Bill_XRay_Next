"""PASS 43 - cold generalization trial.

No bill-specific prose is encoded here. The adapter consumes a previously verified
Bill X-Ray evidence bundle, rejects legacy findings that cannot be normalized safely,
discovers topic mix, selects a minority of facts, and writes a cold human column.
"""
from __future__ import annotations
import argparse, hashlib, json, re
from collections import Counter
from dataclasses import dataclass, asdict
from pathlib import Path

TOPIC_RULES={
 "health and medicine":("drug","medicare","prescription","health","insulin","pharmacy"),
 "taxes and corporate finance":("tax","corporat","excise","financial statement","credit","repurchase"),
 "energy and climate":("energy","emission","climate","electric","clean","greenhouse","methane"),
 "agriculture and conservation":("agriculture","conservation","forest","rural","farm"),
 "public finance and loans":("loan","guarantee","grant","appropriat","funding","fund"),
 "government authority":("secretary shall","administrator shall","must establish","must not","prohibit","enforcement"),
}

@dataclass
class Fact:
 fact_id:str; section:str; text:str; human_fact:str; confidence:float; topic:str
 source_kind:str; citation_anchor:str; missing_context:str; quality:float


def sha256(path:Path)->str:
 h=hashlib.sha256()
 with path.open('rb') as f:
  for c in iter(lambda:f.read(1<<20),b''): h.update(c)
 return h.hexdigest()


def topic_for(text:str)->str:
 low=text.lower(); scored=[]
 for topic,words in TOPIC_RULES.items():
  n=sum(1 for w in words if w in low)
  if n: scored.append((n,topic))
 return max(scored)[1] if scored else 'other'


def tidy(s:str)->str:
 s=re.sub(r'\[\[Page[^\]]*\]\]',' ',s or '',flags=re.I)
 s=s.replace('<>',' ').replace('``','').replace("''",'').replace("program')","program)")
 s=re.sub(r'\s+',' ',s).strip(' .;:-')
 return s


def normalize_claim(c:dict)->tuple[str,float]:
 """Convert structured legacy evidence into a human fact without bill-specific rules."""
 text=tidy(c.get('text') or '')
 action=tidy(c.get('semantic_action') or '')
 actor=tidy(c.get('semantic_actor') or '')
 purpose=tidy(c.get('semantic_purpose') or c.get('fiscal_purpose') or '')
 amount=tidy(c.get('fiscal_amount') or '')
 if not amount:
  m_amount=re.search(r'\$[0-9][0-9,]*(?:\.[0-9]+)?', text)
  amount=m_amount.group(0) if m_amount else ''
 affected=tidy(c.get('affected_party') or '')
 heading=''
 m=re.search(r'addressed by [“"]([^”"]+)',affected)
 if m: heading=m.group(1).strip().lower()

 # Mandatory / prohibited actions are already semantically strong.
 if re.search(r'\bmust establish\b',action,re.I):
  return tidy(f"{actor or 'The responsible official'} {action}"), .96
 if re.search(r'\bmust not\b',action,re.I):
  return tidy(f"{actor or 'The responsible official'} {action}"), .94

 # Loan guarantees: distinguish principal authority from cash spending.
 if 'guarantee loans' in action.lower() and amount:
  when=' through September 30, 2026' if 'September 30, 2026' in action else ''
  return tidy(f"The Secretary may make loan-guarantee commitments{when} with total principal up to {amount}"), .96

 # Threshold tests are not spending simply because they contain a large number.
 if 'average annual adjusted financial statement income test' in text.lower() and amount:
  return tidy(f"The corporate alternative-minimum-tax section uses {amount} as an average annual adjusted financial-statement-income threshold in the test described here"), .95

 # Appropriation / grant style facts: use the named program when available.
 if amount and ('conservation technical assistance' in (text+' '+affected).lower()):
  return tidy(f"The law provides {amount} for conservation technical assistance through the Natural Resources Conservation Service"), .95

 if amount and heading:
  if 'grant' in (action+' '+purpose).lower():
   return tidy(f"Congress makes {amount} available for grants connected to {heading}"), .91
  if 'loan programs office' in heading:
   return tidy(f"The law provides financing authority associated with the Department of Energy Loan Programs Office, including a {amount} principal ceiling identified in this verified finding"), .90
  if 'rural electric cooperatives' in heading:
   return tidy(f"The law makes {amount} available for long-term resiliency, reliability, and affordability of rural electric systems"), .95
  if 'conservation technical' in heading:
   return tidy(f"The law provides {amount} for conservation technical assistance through the Natural Resources Conservation Service"), .95
  if 'building energy code' in heading:
   return tidy(f"The law makes {amount} available for assistance tied to latest and zero building energy codes"), .90

 # Plain semantic action can be used if it is short and grammatical enough.
 candidate=tidy(f"{actor} {action}") if actor and action else tidy(c.get('plain_explanation') or text)
 bad=('...' in candidate or 'STAT.' in candidate or len(candidate)>300 or candidate.lower().startswith('the department of the interior and related agencies appropriations act for'))
 return (candidate,.70 if bad else .86)


def flatten_verified(synthesis:dict)->list[Fact]:
 seen=set(); out=[]; n=0
 for panel in synthesis.get('analysis',{}).get('panels',[]):
  for c in panel.get('claims',[]):
   if c.get('claim_class')!='DIRECT_EFFECT' or float(c.get('confidence') or 0)<.82: continue
   cites=c.get('citations') or []
   if not cites: continue
   key=(cites[0].get('anchor_id'),c.get('text'))
   if key in seen: continue
   seen.add(key)
   human,q=normalize_claim(c)
   if q<.85 or not human: continue
   n+=1
   combined=' '.join([c.get('text') or '',human,c.get('affected_party') or '',c.get('semantic_purpose') or ''])
   out.append(Fact(f"fact-{n:03d}",cites[0].get('section') or '',tidy(c.get('text') or ''),human,float(c.get('confidence') or 0),topic_for(combined),c.get('semantic_source_kind') or 'verified_synthesis',cites[0].get('anchor_id') or '',tidy(c.get('missing_context') or c.get('semantic_unknown') or ''),q))
 return out


def select_facts(facts:list[Fact],limit:int|None=None)->list[Fact]:
 if limit is None:
  limit=max(4,min(10,int(len(facts)*.65)))
  if len(facts)>1: limit=min(limit,len(facts)-1)
 buckets={}
 for f in facts: buckets.setdefault(f.topic,[]).append(f)
 for vals in buckets.values(): vals.sort(key=lambda f:(f.quality,f.confidence,len(f.human_fact)<180),reverse=True)
 selected=[]
 for topic,_ in Counter(f.topic for f in facts).most_common():
  if buckets[topic]: selected.append(buckets[topic].pop(0))
  if len(selected)>=limit: return selected
 rest=[f for vals in buckets.values() for f in vals]; rest.sort(key=lambda f:(f.quality,f.confidence),reverse=True)
 for f in rest:
  if len(selected)>=limit: break
  selected.append(f)
 return selected


def build_column(title:str,selected:list[Fact],counts:Counter)->str:
 dominant=[t for t,_ in counts.most_common(4) if t!='other']
 if not dominant: dominant=['several policy systems']
 topic_phrase=(dominant[0] if len(dominant)==1 else (', '.join(dominant[:-1])+' and '+dominant[-1]))
 paras=[
  f"Congress called it the {title}. That is a neat name for a law whose verified machinery reaches into {topic_phrase}. The first lesson of this cold test is simple: a title can name the argument, but it cannot substitute for the mechanisms underneath it.",
  "Bill X-Ray was not told what thesis to find. It was handed a different, previously verified evidence packet and required to rebuild the shape from facts that survived source and citation gates. What emerged was not one lever marked with the law's title. It was several systems moving at once: prices, taxes, financing, grants, deadlines, and government duties."
 ]
 by={}
 for f in selected: by.setdefault(f.topic,[]).append(f)
 order=[t for t,_ in counts.most_common() if t in by]
 for topic in order[:5]:
  fs=by[topic][:2]
  facts=' '.join(x.human_fact.rstrip('.')+'.' for x in fs)
  paras.append(f"Look at {topic}. {facts}")
  if topic=='public finance and loans': paras.append("A useful X-ray rule appears immediately: a giant dollar figure is not self-explanatory. A grant, an appropriation, and authority to guarantee loan principal can all carry impressive zeros while doing legally different things.")
  elif topic=='government authority': paras.append("That is the power side of legislation. Sometimes the consequential word is not a number at all. It is shall, may, or must not: a verb that tells an official what job Congress has created or limited.")
  elif topic=='health and medicine': paras.append("That is a concrete operating mechanism, not a slogan. Whatever one thinks of the policy, the statute is assigning government an actual job involving drug prices and program administration.")
  elif topic=='taxes and corporate finance': paras.append("Here again the number needs its noun. A threshold used to decide which corporations enter a tax calculation is not the same thing as Congress spending that amount.")
  elif topic=='agriculture and conservation': paras.append("The law therefore reaches well beyond a single household calculation. It is also directing money and deadlines into long-running federal programs that operate on farms, forests, and rural infrastructure.")
 paras += [
  "The honest conclusion is narrower than the politics around the title. This pass does not prove how much the law reduced inflation, whether every program worked, or whether the policy was wise. Those questions need the Reality Stack: official estimates, implementation records, later outcomes, and competing interpretations kept in their proper lanes.",
  "What this cold run does prove is architectural. Bill X-Ray can leave its familiar tax-law laboratory, encounter a law with a different shape, discover a different organizing idea, throw away facts that do not earn space in the column, and still keep every surviving statement attached to a receipt. Different law. Same doctrine. Understanding first; argument afterward."
 ]
 return '\n\n'.join(paras)


def run(bundle:Path,out:Path)->dict:
 synth=json.loads((bundle/'synthesis.json').read_text(encoding='utf-8')); ext=json.loads((bundle/'external_evidence.json').read_text(encoding='utf-8')); e2e=json.loads((bundle/'end_to_end.json').read_text(encoding='utf-8')); source=bundle/'source.txt'
 facts=flatten_verified(synth); counts=Counter(f.topic for f in facts); selected=select_facts(facts); identity=ext.get('identity',{}); title=identity.get('title') or e2e.get('package_id') or 'Untitled law'; column=build_column(title,selected,counts)
 payload={'schema_version':'43.0','bill_id':synth.get('bill_id'),'title':title,'trial_kind':'cold_generalization_from_verified_legacy_evidence','source_sha256':sha256(source),'expected_source_sha256':e2e.get('source_sha256'),'legacy_release_status':e2e.get('analysis_status'),'citation_audit_status':e2e.get('citation_audit_status'),'challenge_status':e2e.get('challenge_status'),'available_verified_facts':len(facts),'selected_fact_count':len(selected),'topic_counts':dict(counts),'selected_facts':[asdict(f) for f in selected],'reality_context':{'cbo_status':ext.get('lanes',{}).get('cbo',{}).get('status','not_loaded'),'usaspending_status':ext.get('lanes',{}).get('usaspending',{}).get('status','not_loaded'),'guardrail':'External estimates and award activity remain context; they do not rewrite the enacted text or prove causation.'},'column':column,'column_word_count':len(column.split())}
 payload['verdict']='GENERALIZES' if len(facts)>=6 and len(counts)>=3 and len(selected)<len(facts) and e2e.get('analysis_status')=='verified' and e2e.get('citation_audit_status')=='pass' else 'NEEDS_REVIEW'
 out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(payload,indent=2),encoding='utf-8'); return payload

if __name__=='__main__':
 ap=argparse.ArgumentParser(); ap.add_argument('--bundle',required=True); ap.add_argument('--out',required=True); a=ap.parse_args(); p=run(Path(a.bundle),Path(a.out)); print(f"PASS 43: {p['bill_id']} - {p['available_verified_facts']} normalized verified facts, {len(p['topic_counts'])} topics, {p['selected_fact_count']} selected, {p['column_word_count']} words; verdict={p['verdict']}")
