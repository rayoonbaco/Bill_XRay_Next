from __future__ import annotations
import json, subprocess, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parent
ART=ROOT/'artifacts'

def run(cmd):
    p=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True)
    if p.stdout: print(p.stdout.strip())
    if p.returncode:
        if p.stderr: print(p.stderr.strip())
        raise SystemExit(p.returncode)

run([sys.executable,'src/semantic_coverage.py','sources/tcja.txt','--bill-id','TCJA','--out','artifacts/tcja_pass40_1_semantic_coverage.json'])
run([sys.executable,'src/human_story_engine.py','--court','artifacts/tcja_pass39_truth_court.json','--coverage','artifacts/tcja_pass40_1_semantic_coverage.json','--out','artifacts/tcja_pass40_1_human_story.json'])

suite=unittest.defaultTestLoader.discover(str(ROOT/'tests'),pattern='test_semantic_coverage.py')
result=unittest.TextTestRunner(verbosity=1).run(suite)
if not result.wasSuccessful(): raise SystemExit(1)

cov=json.loads((ART/'tcja_pass40_1_semantic_coverage.json').read_text(encoding='utf-8'))
story=json.loads((ART/'tcja_pass40_1_human_story.json').read_text(encoding='utf-8'))
cast=f'''========================================================================
 BILL X-RAY NEXT - PASS 40.1 SMOKE CAST
 SEMANTIC COVERAGE EXPANSION
========================================================================

YOUR DUTIES THIS PASS
  1. Run ONE_CLICK_PASS_40_1.bat from this project folder.
  2. Read the coverage verdict and the entire human story below.
  3. Judge the story as a HUMAN: do you finally understand the shape of TCJA?
  4. Send the full smoke cast back to the team.

WHAT THIS PASS MUST PROVE
  - Bill X-Ray can widen human meaning without weakening the evidence gate.
  - Direct statutory facts may join before/after facts when the enacted text itself is enough.
  - Every added fact keeps an exact source receipt and explicit limits.
  - The Human Story Engine has enough truth to choose from instead of padding two facts.
  - Humor and satire are STILL forbidden; understanding comes first.

PASS 40.1 COVERAGE
  Direct statutory facts cleared: {cov['fact_count']}
  Human categories: {len(cov['category_counts'])}
  Held for missing anchors: {cov['hold_count']}
  Story facts actually used: {story['supported_fact_count']}
  Story word count: {story['word_count']}
  Readiness: {story['release_readiness']}

--------------------- I READ THE BILL ---------------------
{story['story']}
-----------------------------------------------------------

MACHINE VERDICT: {story['release_readiness']}
DIAGNOSIS: {story['diagnosis']}

HUMAN GATE
  Do NOT ask whether this is stylish enough yet.
  Ask whether you can now explain the main shape of this law to another person.
  If yes, the substrate is finally broad enough and the Editorial Intelligence Room may begin.
  If no, we expand meaning again before touching voice.

CLEAR: PASS 40.1 completed. This CLEAR means the semantic substrate is broad,
receipt-backed, and ready for a human comprehension verdict. It does NOT mean
this is the final Bill X-Ray essay.
========================================================================
'''
(ART/'SMOKE_CAST_PASS_40_1.txt').write_text(cast,encoding='utf-8')
print(cast)
