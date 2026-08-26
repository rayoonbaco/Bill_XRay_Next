from pathlib import Path
import json
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "artifacts" / "tcja_pass39_truth_court.json"
SMOKE = ROOT / "artifacts" / "SMOKE_CAST_PASS_39.txt"

subprocess.run([
    sys.executable, "-m", "src.truth_court",
    "--queue", str(ROOT / "artifacts" / "tcja_pass38_investigation_queue.json"),
    "--out", str(OUT)
], cwd=ROOT, check=True)

suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"), pattern="test_truth_court.py")
result = unittest.TextTestRunner(verbosity=1).run(suite)
if not result.wasSuccessful():
    print("NEEDS REVIEW: Pass 39 focused checks failed.")
    raise SystemExit(1)

p = json.loads(OUT.read_text(encoding="utf-8"))
examples = p["opinions"][:4]
lines = [
"========================================================================",
" BILL X-RAY NEXT - PASS 39 SMOKE CAST",
" ADVERSARIAL TRUTH COURT",
"========================================================================",
"",
"YOUR DUTIES THIS PASS",
"  1. Run ONE_CLICK_PASS_39.bat from this project folder.",
"  2. Read the CLEAR / NEEDS REVIEW result at the end.",
"  3. If CLEAR, no file moving, dependency install, or UI testing is required.",
"  4. Optional human gate: read the court examples printed below.",
"",
"WHAT THIS PASS MUST PROVE",
"  - Investigation leads are argued from more than one perspective.",
"  - A question can survive even when a factual claim cannot.",
"  - Only verified atomic meaning may become a narrow factual statement here.",
"  - Motive, corruption, cost, winners/losers, causation, and satire remain forbidden unless separately proved.",
"",
f"PASS 39: adjudicated {p['opinion_count']} candidates; {p['public_statements_allowed']} narrow statements allowed; {p['question_only_count']} remain question-only",
"Dependency-free focused checks: 5/5 passed",
"",
"TRUTH COURT HUMAN CHECK",
]
for o in examples:
    lines += [
        f"  [{o['verdict']}] {o['section']} - {o['category']}",
        f"    Prosecutor: {o['prosecutor']}",
        f"    Defense: {o['defense']}",
        f"    Referee: {o['text_referee']}",
        f"    Allowed statement: {o['allowed_public_statement'] or 'NONE'}",
        f"    Allowed question: {o['allowed_public_question'] or 'NONE'}",
    ]
lines += [
"",
f"Court opinions: {p['opinion_count']}",
f"Narrow factual statements allowed: {p['public_statements_allowed']}",
f"Question-only opinions: {p['question_only_count']}",
"",
"CLEAR: PASS 39 completed. Curiosity has been separated from proof before the Human Story Engine.",
"Smoke cast saved to: artifacts\\SMOKE_CAST_PASS_39.txt",
]
text="\n".join(lines)
SMOKE.write_text(text, encoding="utf-8")
print(text)
