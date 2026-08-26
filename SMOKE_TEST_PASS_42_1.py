from pathlib import Path
import sys
import unittest

from src.reality_stack import build_pass421

ROOT = Path(__file__).resolve().parent
ART = ROOT / 'artifacts'
payload = build_pass421(
    ART / 'pass42_claim_vs_law.json',
    ROOT / 'sources/aca_reality_stack_sources.json',
    ART / 'pass42_1_reality_stack.json',
)
loader = unittest.TestLoader()
suite = loader.discover(str(ROOT / 'tests'), pattern='test_reality_stack.py')
result = unittest.TextTestRunner(verbosity=1).run(suite)

print('\n' + '=' * 72)
print(' BILL X-RAY NEXT - PASS 42.1 SMOKE CAST')
print(' REALITY STACK')
print('=' * 72)
print('\nYOUR DUTIES THIS PASS')
print('  1. Read the layered ACA example below.')
print('  2. Ask whether rhetoric, law, implementation, and outcome still feel visibly different.')
print('  3. Check that the machine never turns later outcomes into something Congress literally wrote.')
print('  4. Check that a missing court lane says NOT LOADED rather than pretending no case exists.')
print('  5. Send the full smoke cast and your reaction back to the team.')
print('\nWHAT THIS PASS MUST PROVE')
print('  - A law is only one layer of policy reality.')
print('  - Agency implementation may add operating rules without rewriting the statute.')
print('  - Official reviews and observed outcomes may test the promise without proving simple causation.')
print('  - Missing evidence is labeled missing; outside commentary is not allowed to outrank primary sources.')
print(f"\nFOCUSED CHECKS: {result.testsRun-len(result.errors)-len(result.failures)}/{result.testsRun} passed")

print('\n--------------------- REALITY STACK ---------------------')
for lane in payload['lanes']:
    print(f"\n[{lane['lane']}] {lane['question']}")
    print(' STATUS:', lane['status'])
    print(' SAFE CONCLUSION:', lane['safe_conclusion'])
    if lane['source_ids']:
        print(' SOURCES:', ', '.join(lane['source_ids']))
    print(' CANNOT CONCLUDE:')
    for x in lane['cannot_conclude']:
        print('   -', x)

print('\n--------------------- HUMAN ANSWER ----------------------')
print('PUBLIC CLAIM')
print(' ', payload['public_answer']['rhetoric'])
print('\nWHAT CONGRESS WROTE')
print(' ', payload['public_answer']['law'])
print('\nWHAT AGENCIES DID')
print(' ', payload['public_answer']['implementation'])
print('\nWHAT OFFICIAL REVIEWERS LATER FOUND')
print(' ', payload['public_answer']['official_review'])
print('\nWHAT THE MARKET RECORD SHOWED')
print(' ', payload['public_answer']['observed_outcome'])
print('\nBOTTOM LINE')
print(' ', payload['public_answer']['bottom_line'])
print('----------------------------------------------------------')
print('\nMACHINE VERDICT:', payload['release_readiness'])
print('HUMAN GATE: Did this give you MORE reality without blurring what came from Congress, regulators, reviewers, and later outcomes?')

cast_lines = [
    'PASS 42.1 CLEAR' if result.wasSuccessful() else 'PASS 42.1 NEEDS REVIEW',
    f"tests={result.testsRun-len(result.errors)-len(result.failures)}/{result.testsRun}",
    'lanes=' + str(len(payload['lanes'])),
    'causation=' + payload['gap_analysis']['causation_status'],
    'readiness=' + payload['release_readiness'],
]
(ART / 'SMOKE_CAST_PASS_42_1.txt').write_text('\n'.join(cast_lines), encoding='utf-8')
if not result.wasSuccessful():
    sys.exit(1)
print('\n' + '=' * 72)
print(' CLEAR - PASS 42.1 ENGINE PASSED - RAY REALITY GATE REQUIRED')
print('=' * 72)
