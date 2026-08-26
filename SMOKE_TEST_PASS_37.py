from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "sources" / "tcja.txt"
OUT = ROOT / "artifacts" / "tcja_pass37_rosetta_grammar.json"
CAST = ROOT / "artifacts" / "SMOKE_CAST_PASS_37.txt"


def fail(message: str) -> int:
    print(f"\nNEEDS REVIEW: {message}")
    return 1


def main() -> int:
    print("=" * 72)
    print(" BILL X-RAY NEXT - PASS 37 SMOKE CAST")
    print(" CONGRESSIONAL ROSETTA GRAMMAR")
    print("=" * 72)
    print("\nYOUR DUTIES THIS PASS")
    print("  1. Run ONE_CLICK_PASS_37.bat from this project folder.")
    print("  2. Read the CLEAR / NEEDS REVIEW result at the end.")
    print("  3. If CLEAR, no file moving, dependency install, or UI testing is required.")
    print("  4. Optional human gate: read the Rosetta examples printed below.")
    print("\nWHAT THIS PASS MUST PROVE")
    print("  - The engine recognizes recurring Congressional grammar as operations.")
    print("  - Each construct has a safe human explanation plus context requirements.")
    print("  - Grammar recognition alone is NEVER allowed to become a public factual claim.")
    print("  - The Rosetta layer generalizes beyond dollar substitutions.")

    required = [
        ROOT / "docs" / "DOCTRINE.md",
        ROOT / "docs" / "PASS_ROADMAP.md",
        ROOT / "src" / "legislative_decompiler.py",
        ROOT / "src" / "congressional_rosetta.py",
        ROOT / "tests" / "test_congressional_rosetta.py",
        SOURCE,
    ]
    missing = [str(p.relative_to(ROOT)) for p in required if not p.exists()]
    if missing:
        return fail("Missing required full-replacement files: " + ", ".join(missing))

    result = subprocess.run([
        sys.executable, "-m", "src.congressional_rosetta", str(SOURCE),
        "--bill-id", "tcja", "--out", str(OUT),
    ], cwd=ROOT)
    if result.returncode:
        return fail("Congressional Rosetta scan failed.")

    from src.congressional_rosetta import explain_text, scan_file

    def rule_ids(text: str) -> set[str]:
        return {h.rule_id for h in explain_text(text)}

    examples = {
        "strike_insert": "Section 24 is amended by striking '$1,000' and inserting '$2,000'.",
        "notwithstanding": "Notwithstanding section 5, this paragraph shall apply.",
        "subject_to": "The credit is allowed subject to paragraph (4).",
        "except_as_provided": "Except as provided in paragraph (2), the rule applies.",
        "treated_as": "Such child shall be treated as a dependent.",
        "for_purposes_of": "For purposes of this subsection, the term means...",
        "effective_date": "Effective Date.--The amendment applies after December 31, 2017.",
        "delegated_rulemaking": "The Secretary shall prescribe such regulations as necessary.",
    }
    for expected, text in examples.items():
        if expected not in rule_ids(text):
            return fail(f"Grammar rule did not recognize {expected}.")

    live_hits = scan_file(SOURCE, "tcja")
    present = {h.rule_id for h in live_hits}
    required_live = {"strike_insert", "treated_as", "for_purposes_of", "effective_date", "delegated_rulemaking"}
    if not required_live <= present:
        return fail("Live TCJA grammar coverage missing: " + ", ".join(sorted(required_live - present)))
    if any(h.public_claim_allowed for h in live_hits):
        return fail("Truth gate failed: grammar hit was incorrectly allowed to become a public claim.")
    if any(not h.context_required for h in live_hits):
        return fail("Context gate failed: at least one grammar hit omitted context requirements.")

    payload = json.loads(OUT.read_text(encoding="utf-8"))
    if payload["rule_count"] < 10 or payload["hit_count"] < 50:
        return fail("Rosetta catalog or TCJA coverage is unexpectedly small.")

    print("Dependency-free focused checks: 4/4 passed")
    print("\nROSETTA HUMAN CHECK")
    display = [
        ("strike + insert", "Congress is editing an existing rule; retrieve the old rule before explaining the change."),
        ("subject to", "This rule only works within another rule's limits."),
        ("treated as", "Congress is assigning a legal classification; find the consequence before explaining why it matters."),
        ("shall prescribe", "An official must write implementing rules; identify what Congress left for that official to decide."),
    ]
    for source, meaning in display:
        print(f"  {source:18} -> {meaning}")

    top = sorted(payload["rule_counts"].items(), key=lambda kv: kv[1], reverse=True)[:8]
    lines = [
        "BILL X-RAY NEXT - PASS 37 SMOKE CAST",
        "RESULT: CLEAR",
        "",
        "DOCTRINE GATE:",
        "Congressional grammar is decoded into operations, not mistaken for complete human meaning.",
        "No grammar hit is allowed to become a public factual claim by itself.",
        "",
        f"Rosetta rules defined: {payload['rule_count']}",
        f"Grammar uses recognized in TCJA: {payload['hit_count']}",
        f"Construct types found in TCJA: {len(payload['rule_counts'])}",
        f"Public claims allowed from grammar alone: {payload['public_claims_allowed_from_grammar_alone']}",
        "",
        "MOST COMMON CONSTRUCTS:",
    ]
    lines.extend(f"- {name}: {count}" for name, count in top)
    lines += [
        "",
        "HUMAN DUTY:",
        "No manual code or UI testing required for this pass.",
        "Optional: read the four Rosetta examples printed in the console and judge whether they explain the operation without pretending to explain the whole law.",
    ]
    CAST.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"\nTCJA grammar uses recognized: {payload['hit_count']} across {len(payload['rule_counts'])} construct types")
    print("Public claims allowed from grammar alone: 0")
    print("\nCLEAR: PASS 37 completed. The Rosetta layer can decode grammar without confusing grammar for meaning.")
    print(f"Smoke cast saved to: {CAST.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
