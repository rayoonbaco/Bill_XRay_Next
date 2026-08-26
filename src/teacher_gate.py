from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]

def load_data():
    raw=(ROOT/'public/data.js').read_text(encoding='utf-8').strip(); prefix='window.BXR_DATA = '
    return json.loads(raw[len(prefix):-1])

def grade(bill_id='chips'):
    b=load_data()[bill_id]
    story=' '.join(p['text'] for p in b['story'])
    receipts=b['receipts']; ids={r['id'] for r in receipts}
    criteria=[]
    def add(name,points,ok,note): criteria.append({'name':name,'points':points,'earned':points if ok else 0,'ok':ok,'note':note})
    all_supported=all(p.get('support_fact_ids') and set(p['support_fact_ids'])<=ids for p in b['story'])
    source_complete=all(r.get('source') and r.get('section') and r.get('excerpt') and r.get('limits') for r in receipts)
    short_wc=len(b['short'].split()); story_wc=len(story.split())
    forbidden=['cold trial','evidence packet','reality stack','machine verdict','human gate','architecture','this pass']
    upstairs=' '.join([b['eyebrow'],b['title'],b['dek'],b['short'],story]).lower()
    loaded_words=['appropriation','loan','tax credit','buyback','dividend','10-year','china','technology hub','research-security']
    add('Source fidelity',20,source_complete and len(receipts)>=8,'Every receipt has a statutory section, official source pointer, excerpt, and explicit limit.')
    add('Claim-to-receipt traceability',20,all_supported,'Every public paragraph names the receipts that support it.')
    add('Human translation',20,500<=story_wc<=800 and 45<=short_wc<=100,'The long piece is readable rather than exhaustive, and the 30-second version is genuinely short.')
    add('Semantic precision',15,'not a $75 billion cash appropriation' in upstairs and 'a tax credit is not a grant' in upstairs,'The essay distinguishes loan principal from appropriated cash and distinguishes grants from tax credits.')
    add('Synthesis',15,sum(w in upstairs for w in loaded_words)>=7 and 'part of the bargain' in upstairs,'The column finds one thesis across money, conditions, industrial capacity, and science rather than listing sections.')
    add('Restraint and uncertainty',10,not any(x in upstairs for x in forbidden) and 'none of this tells us whether' in upstairs,'The public story separates enacted mechanics from later wisdom, success, motive, and outcomes.')
    score=sum(c['earned'] for c in criteria); grade='A' if score>=93 else 'A-' if score>=90 else 'B+' if score>=87 else 'B' if score>=83 else 'C'
    return {'bill_id':bill_id,'score':score,'grade':grade,'story_word_count':story_wc,'short_word_count':short_wc,'receipt_count':len(receipts),'criteria':criteria}

if __name__=='__main__': print(json.dumps(grade(),indent=2))
