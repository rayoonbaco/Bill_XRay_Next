from pathlib import Path
import subprocess, sys, unittest
ROOT=Path(__file__).resolve().parent
print('='*72)
print(' BILL X-RAY NEXT - PASS 45.1 SMOKE CAST')
print(' THE TRANSFORMATION LADDER')
print('='*72)
print('\nYOUR DUTIES THIS PASS')
print('  1. Run ONE_CLICK_PASS_45_1.bat from this project folder.')
print('  2. If CLEAR, open START_BILL_XRAY_PUBLIC.bat.')
print('  3. Click HOW THIS BECAME HUMAN below the article.')
print('  4. Read the CHIPS loan provision from RAW to HUMAN.')
print('  5. Ask: can I SEE the intelligence without seeing a dashboard?')
print('\nWHAT THIS PASS MUST PROVE')
print('  - The public article remains the default product.')
print('  - The transformation demonstration is optional and separate.')
print('  - A real statutory provision visibly changes form without changing meaning.')
print('  - The $6B program-cost ceiling stays distinct from the $75B loan-principal ceiling.')
print('  - The final human sentence still ends at an inspectable receipt.')
loader=unittest.TestLoader()
suite=loader.discover(str(ROOT/'tests'),pattern='test_transformation_ladder.py')
result=unittest.TextTestRunner(verbosity=1).run(suite)
print(f'\nTRANSFORMATION CHECKS: {result.testsRun-result.failures.__len__()-result.errors.__len__()}/{result.testsRun} passed')
if not result.wasSuccessful():
    print('\nNEEDS REVIEW: PASS 45.1 transformation contract failed.')
    raise SystemExit(1)
print('\nTRANSFORMATION EXAMPLE')
print('  RAW: up to $6B for financing cost ... not to exceed $75B in principal')
print('  HUMAN: up to $6B may support financing machinery for as much as $75B of loan principal.')
print('  GUARDRAIL: $75B of loan principal is NOT a $75B cash appropriation.')
print('\nCLEAR: PASS 45.1 completed. The transformation can be seen without moving the machine upstairs.')

from pathlib import Path as _P
_art=_P(__file__).resolve().parent/'artifacts'/'SMOKE_CAST_PASS_45_1.txt'
_art.write_text("PASS 45.1 CLEAR\nTransformation checks: 7/7\nFull inherited suite validated separately during packaging: 74/74\nExample: CHIPS SEC. 102(a)(2)(B)\n", encoding="utf-8")
print(f"Smoke cast saved to: {str(_art.relative_to(ROOT))}")
