from pathlib import Path
import sys
import unittest

from src.claim_law_mapper import build_pass42

ROOT = Path(__file__).resolve().parent
ART = ROOT / 'artifacts'
result_map = build_pass42(
    ROOT / 'sources/aca_keep_doctor_claim.json',
    ROOT / 'sources/aca_claim_law_excerpt.txt',
    ART / 'tcja_pass40_1_semantic_coverage.json',
    ART / 'pass42_claim_vs_law.json',
)
loader = unittest.TestLoader()
suite = loader.discover(str(ROOT / 'tests'), pattern='test_claim_law_mapper.py')
result = unittest.TextTestRunner(verbosity=1).run(suite)

aca = result_map['aca_keep_doctor']
tcja = result_map['tcja_child_credit']
print('\n' + '=' * 72)
print(' BILL X-RAY NEXT - PASS 42 SMOKE CAST')
print(' CLAIM VS LAW MAPPER')
print('=' * 72)
print('\nYOUR DUTIES THIS PASS')
print('  1. Read the ACA claim map below as a citizen, not as a fact-check referee.')
print('  2. Ask whether the machine separates the political sentence from what the statute actually guarantees.')
print('  3. Check that it does NOT jump to TRUE/FALSE, motive, or later real-world outcomes.')
print('  4. Send the full smoke cast and your reaction back to the team.')
print('\nWHAT THIS PASS MUST PROVE')
print('  - A public claim can be decomposed into legal promises that can actually be tested.')
print('  - Supporting language, limiting language, and missing guarantees stay separate.')
print('  - A true-sounding headline can be supported yet incomplete.')
print('  - A broad political promise can exceed the guarantee in the statutory machinery without being turned into an accusation.')
print(f"\nFOCUSED CHECKS: {result.testsRun-len(result.errors)-len(result.failures)}/{result.testsRun} passed")
print('\n--------------------- THEY SAID THIS ---------------------')
print('CLAIM:', aca['public_render']['claim'])
print('\nWHAT THE LAW ACTUALLY SUPPORTS')
for x in aca['public_render']['what_the_law_does_protect']:
    print('  -', x)
print('\nWHAT THE REVIEWED PROVISIONS DO NOT ESTABLISH')
for x in aca['public_render']['what_the_law_does_not_establish']:
    print('  -', x)
print('\nBILL X-RAY ANSWER')
print(' ', aca['public_render']['law_answer'])
print('\nHUMAN CONCLUSION')
print(' ', aca['public_render']['human_conclusion'])
print('\nMACHINE CLASSIFICATION:', aca['verdict']['classification'])
print('\nWHAT THIS IS NOT A VERDICT ON')
for x in aca['verdict']['not_a_verdict_on']:
    print('  -', x)
print('----------------------------------------------------------')
print('\nCONTROL EXAMPLE - A HEADLINE THAT IS TRUE BUT INCOMPLETE')
print('CLAIM:', tcja['public_render']['claim'])
print('ANSWER:', tcja['public_render']['law_answer'])
print('CLASSIFICATION:', tcja['verdict']['classification'])
print('\nMACHINE VERDICT:', aca['release_readiness'])
print('HUMAN GATE: Did this make the law/promise gap understandable without telling you what political opinion to hold?')

cast_lines = [
    'PASS 42 CLEAR' if result.wasSuccessful() else 'PASS 42 NEEDS REVIEW',
    'aca_classification=' + aca['verdict']['classification'],
    'tcja_control=' + tcja['verdict']['classification'],
    f'tests={result.testsRun-len(result.errors)-len(result.failures)}/{result.testsRun}',
    'readiness=' + aca['release_readiness'],
]
(ART / 'SMOKE_CAST_PASS_42.txt').write_text('\n'.join(cast_lines), encoding='utf-8')
if not result.wasSuccessful():
    sys.exit(1)
print('\n' + '=' * 72)
print(' CLEAR - PASS 42 ENGINE PASSED - RAY CLAIM MAP GATE REQUIRED')
print('=' * 72)
