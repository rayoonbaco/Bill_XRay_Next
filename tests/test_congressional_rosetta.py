from src.congressional_rosetta import explain_text, scan_file
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def ids(text: str):
    return {h.rule_id for h in explain_text(text)}


def test_core_grammar_examples():
    assert "strike_insert" in ids("Section 24 is amended by striking '$1,000' and inserting '$2,000'.")
    assert "notwithstanding" in ids("Notwithstanding section 5, this paragraph shall apply.")
    assert "subject_to" in ids("The credit is allowed subject to paragraph (4).")
    assert "except_as_provided" in ids("Except as provided in paragraph (2), the rule applies.")
    assert "treated_as" in ids("Such child shall be treated as a dependent.")
    assert "for_purposes_of" in ids("For purposes of this subsection, the term means...")
    assert "effective_date" in ids("Effective Date.--The amendment applies after December 31, 2017.")


def test_grammar_never_becomes_public_claim_by_itself():
    hits = explain_text("The Secretary shall prescribe such regulations as necessary.")
    assert hits
    assert any(h.rule_id == "delegated_rulemaking" for h in hits)
    assert all(not h.public_claim_allowed for h in hits)
    assert all(h.context_required for h in hits)


def test_live_tcja_contains_expected_constructs():
    hits = scan_file(ROOT / "sources" / "tcja.txt", "tcja")
    present = {h.rule_id for h in hits}
    assert {"strike_insert", "treated_as", "for_purposes_of", "effective_date", "delegated_rulemaking"} <= present
