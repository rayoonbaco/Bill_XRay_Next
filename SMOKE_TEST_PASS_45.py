from pathlib import Path
import json,sys,unittest
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from src.teacher_gate import grade

def run_tests():
    suite=unittest.TestLoader().loadTestsFromName('tests.test_pass45_teacher_gate')
    result=unittest.TextTestRunner(verbosity=1).run(suite)
    return result.wasSuccessful()

def main():
    print('='*72); print(' BILL X-RAY NEXT - PASS 45 SMOKE CAST'); print(' FRESH BILL A-GRADE TRIAL'); print('='*72); print()
    print('YOUR DUTIES THIS PASS')
    print('  1. Run ONE_CLICK_PASS_45.bat from this project folder.')
    print('  2. Read the CLEAR / NEEDS REVIEW result.')
    print('  3. If CLEAR, open START_BILL_XRAY_PUBLIC.bat and click CHIPS.')
    print('  4. Read the 30-second version, then the essay, then CHECK MY HOMEWORK.')
    print('  5. Grade it like a teacher: did a cryptic law become understandable without becoming false?')
    print()
    print('WHAT THIS PASS MUST PROVE')
    print('  - A fresh fourth law can enter the public product without redesigning the product around it.')
    print('  - Different dollar figures keep their legal nouns: appropriation, loan principal, tax credit.')
    print('  - The essay discovers one human thesis instead of dumping sections.')
    print('  - Every paragraph is traceable to official enacted-law receipts.')
    print('  - A teacher-style quality gate grades meaning, evidence, clarity, synthesis, and restraint.')
    print()
    ok=run_tests(); g=grade('chips')
    print(); print('TEACHER GRADE')
    print(f"  CHIPS essay: {g['score']}/100 -> {g['grade']}")
    print(f"  Long-form words: {g['story_word_count']}")
    print(f"  30-second words: {g['short_word_count']}")
    print(f"  Homework receipts: {g['receipt_count']}")
    for c in g['criteria']:
        mark='PASS' if c['ok'] else 'FAIL'; print(f"  [{mark}] {c['name']}: {c['earned']}/{c['points']} - {c['note']}")
    art=ROOT/'artifacts'; art.mkdir(exist_ok=True)
    (art/'pass45_teacher_grade.json').write_text(json.dumps(g,indent=2),encoding='utf-8')
    cast=[
        'BILL X-RAY NEXT - PASS 45 SMOKE CAST',
        'FRESH BILL A-GRADE TRIAL',
        f"CHIPS essay: {g['score']}/100 -> {g['grade']}",
        f"Long-form words: {g['story_word_count']}",
        f"30-second words: {g['short_word_count']}",
        f"Homework receipts: {g['receipt_count']}",
    ] + [f"[{'PASS' if c['ok'] else 'FAIL'}] {c['name']}: {c['earned']}/{c['points']} - {c['note']}" for c in g['criteria']]
    (art/'SMOKE_CAST_PASS_45.txt').write_text('\n'.join(cast)+'\n',encoding='utf-8')
    print(); print('HUMAN THESIS CHECK')
    print('  The public shorthand is "chip subsidies."')
    print('  The essay should reveal a more precise bargain: multiple financing tools, public-money restrictions,')
    print('  a 10-year foreign-expansion guardrail, a 25% investment credit, and a much larger science agenda.')
    print()
    if ok and g['grade']=='A':
        print('CLEAR: PASS 45 completed. The fresh-bill essay and homework clear the automated A-grade gate.')
        return 0
    print('NEEDS REVIEW: PASS 45 did not earn an A. Do not ship the new public story yet.'); return 1
if __name__=='__main__': raise SystemExit(main())
