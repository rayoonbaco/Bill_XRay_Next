from pathlib import Path

from src.legislative_decompiler import decompile_file

TCJA = Path(__file__).resolve().parents[1] / "sources" / "tcja.txt"


def _section(events, section):
    return [event for event in events if event.section == section]


def test_child_credit_is_split_into_atomic_changes():
    events = decompile_file(TCJA, "tcja")
    child = _section(events, "SEC. 11022")
    pairs = {(event.before, event.after) for event in child}
    assert ("$1,000", "$2,000") in pairs
    assert ("$3,000", "$2,500") in pairs
    credit = next(event for event in child if event.before == "$1,000")
    threshold = next(event for event in child if event.before == "$3,000")
    assert "credit amount" in credit.target.lower()
    assert "earned income threshold" in threshold.target.lower()
    assert credit.event_id != threshold.event_id


def test_standard_deduction_is_atomic_but_withholds_filing_status_without_baseline_code():
    events = decompile_file(TCJA, "tcja")
    standard = _section(events, "SEC. 11021")
    pairs = {(event.before, event.after) for event in standard}
    assert ("$4,400", "$18,000") in pairs
    assert ("$3,000", "$12,000") in pairs
    assert all(event.publishable is False for event in standard)
    assert all(event.context_required for event in standard)


def test_corporate_rate_sets_21_percent_but_refuses_to_invent_prior_rate():
    events = decompile_file(TCJA, "tcja")
    corporate = _section(events, "SEC. 13001")
    assert len(corporate) == 1
    event = corporate[0]
    assert event.after == "21%"
    assert event.before is None
    assert event.publishable is False
    assert any("pre-amendment" in item for item in event.context_required)


def test_source_is_bundled_so_project_has_no_sibling_folder_dependency():
    assert TCJA.exists()
    assert "SEC. 11022." in TCJA.read_text(encoding="utf-8")
