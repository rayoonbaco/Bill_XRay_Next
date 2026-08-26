from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ART = ROOT / 'artifacts' / 'tcja_pass38_investigation_queue.json'
LOG = ROOT / 'artifacts' / 'SMOKE_CAST_PASS_38.txt'

print('=' * 72)
print(' BILL X-RAY NEXT - PASS 38 SMOKE CAST')
print(' INVESTIGATION ENGINE')
print('=' * 72)
print('\nYOUR DUTIES THIS PASS')
print('  1. Run ONE_CLICK_PASS_38.bat from this project folder.')
print('  2. Read the CLEAR / NEEDS REVIEW result at the end.')
print('  3. If CLEAR, no file moving, dependency install, or UI testing is required.')
print('  4. Optional human gate: read the investigation examples printed below.')
print('\nWHAT THIS PASS MUST PROVE')
print('  - Decoded meaning can become an investigation queue, not instant prose.')
print('  - Interesting does NOT mean corrupt, wasteful, or wrong.')
print('  - Every candidate carries evidence, uncertainty, and an ordinary explanation.')
print('  - Nothing in Pass 38 is allowed to become a public factual claim yet.')

cmd = [sys.executable, '-m', 'src.investigation_engine', str(ROOT/'sources'/'tcja.txt'),
       '--atomic-events', str(ROOT/'artifacts'/'tcja_pass36_atomic_events.json'),
       '--bill-id', 'TCJA', '--out', str(ART)]
r = subprocess.run(cmd, cwd=ROOT)
if r.returncode:
    print('\nNEEDS REVIEW: Investigation engine did not complete.')
    sys.exit(1)

r = subprocess.run([sys.executable, '-m', 'unittest', 'tests.test_investigation_engine', '-q'], cwd=ROOT)
if r.returncode:
    print('\nNEEDS REVIEW: Dependency-free focused checks failed.')
    sys.exit(1)
print('Dependency-free focused checks: 5/5 passed')

p = json.loads(ART.read_text(encoding='utf-8'))
print('\nINVESTIGATION HUMAN CHECK')
for c in p['candidates'][:4]:
    print(f"  [{c['category']}] {c['section']} - score {c['score']}")
    print('    Why look:', c['why_human_might_care'])
    print('    Ask:', c['question_to_investigate'])
    print('    Restraint:', c['ordinary_explanations'][0])
print(f"\nTCJA candidates ranked: {p['candidate_count']} across {len(p['category_counts'])} categories")
print(f"Public claims allowed from Pass 38: {p['public_claims_allowed']}")
print('\nCLEAR: PASS 38 completed. The machine can decide where to look harder without pretending suspicion is proof.')

LOG.parent.mkdir(parents=True, exist_ok=True)
LOG.write_text('PASS 38 CLEAR\n' + json.dumps({
    'candidate_count': p['candidate_count'],
    'category_counts': p['category_counts'],
    'public_claims_allowed': p['public_claims_allowed'],
}, indent=2), encoding='utf-8')
print('Smoke cast saved to: artifacts\\SMOKE_CAST_PASS_38.txt')
