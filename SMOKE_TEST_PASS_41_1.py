from pathlib import Path
import unittest, sys
from src.columnist import build_column

ROOT = Path(__file__).resolve().parent
ART = ROOT / 'artifacts'
column = build_column(ART/'tcja_pass40_1_semantic_coverage.json', ART/'tcja_pass41_1_column.json')
loader = unittest.TestLoader()
suite = loader.discover(str(ROOT/'tests'), pattern='test_columnist.py')
result = unittest.TextTestRunner(verbosity=1).run(suite)

print('\n'+'='*72)
print(' BILL X-RAY NEXT - PASS 41.1 SMOKE CAST')
print(' THE COLUMNIST')
print('='*72)
print('\nYOUR DUTIES THIS PASS')
print('  1. Read ONLY the first three paragraphs once without analyzing them.')
print('  2. Ask: do I genuinely want paragraph four?')
print('  3. Then read the full column and judge whether it has ONE story, not six sections.')
print('  4. Ask whether the wit reveals the law or merely sounds clever.')
print('  5. Send the full smoke cast and your human reaction back to the team.')
print('\nWHAT THIS PASS MUST PROVE')
print('  - The columnist can discard most cleared facts and find one truthful thesis.')
print('  - The first three paragraphs create narrative pull for a non-tax reader.')
print('  - The column no longer marches through the evidence categories.')
print('  - Every paragraph remains traceable to court-cleared facts.')
print('  - Wit may expose complexity; it may not manufacture motive or wrongdoing.')
print(f"\nAVAILABLE CLEARED FACTS: {column['available_fact_count']}")
print(f"FACTS THE COLUMNIST KEPT: {column['selected_fact_count']}")
print(f"FACTS DELIBERATELY LEFT DOWNSTAIRS: {column['omitted_fact_count']}")
print(f"COLUMN WORD COUNT: {column['word_count']}")
print(f"FIRST THREE PARAGRAPHS: {column['hook_gate']['first_three_word_count']} words")
print(f"FOCUSED CHECKS: {result.testsRun-len(result.errors)-len(result.failures)}/{result.testsRun} passed")
print('\nCOLUMNIST THESIS')
print(' ', column['thesis'])
print('\n--------------------- I READ THE BILL ---------------------')
print(column['column_title'])
print(column['dek'])
print()
print(column['story'])
print('-----------------------------------------------------------')
print('\nMACHINE VERDICT:', column['release_readiness'])
print('HUMAN HOOK GATE: After paragraph three, did you WANT paragraph four?')
print('HUMAN STORY GATE: Did this feel like one revealing column rather than an organized tax summary?')
cast = '\n'.join([
    'PASS 41.1 CLEAR' if result.wasSuccessful() else 'PASS 41.1 NEEDS REVIEW',
    f"available_facts={column['available_fact_count']}",
    f"selected_facts={column['selected_fact_count']}",
    f"omitted_facts={column['omitted_fact_count']}",
    f"word_count={column['word_count']}",
    f"hook_words={column['hook_gate']['first_three_word_count']}",
    'readiness='+column['release_readiness'],
])
(ART/'SMOKE_CAST_PASS_41_1.txt').write_text(cast, encoding='utf-8')
if not result.wasSuccessful():
    sys.exit(1)
print('\n'+'='*72)
print(' CLEAR - PASS 41.1 ENGINE PASSED - RAY COLUMNIST GATE REQUIRED')
print('='*72)
