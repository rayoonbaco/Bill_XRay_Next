import json
import tempfile
import unittest
from pathlib import Path

from src.truth_court import adjudicate, run_court

ROOT = Path(__file__).resolve().parents[1]


class TruthCourtTests(unittest.TestCase):
    def test_verified_atomic_event_can_only_support_narrow_statement(self):
        c = {
            "candidate_id":"x", "bill_id":"TCJA", "section":"SEC. 1", "section_heading":"TEST",
            "category":"large_before_after_change", "source_start_line":10, "source_end_line":10,
            "evidence_excerpt":"substituting $2,000 for $1,000", "source_basis":"verified_atomic_meaning_event",
            "why_human_might_care":"This verified before/after event changes Credit amount from $1,000 to $2,000, large enough to deserve context before the final story is written.",
            "question_to_investigate":"Who is affected?", "ordinary_explanations":["Could be a policy reset."], "uncertainty":["Cost unknown."]
        }
        o = adjudicate(c)
        self.assertEqual(o.verdict, "SUPPORTED_NARROWLY")
        self.assertEqual(o.allowed_public_statement, "The bill changes Credit amount from $1,000 to $2,000.")
        self.assertTrue(any("corruption" in x for x in o.forbidden_inferences))

    def test_text_signal_remains_question_only(self):
        c = {
            "candidate_id":"x", "bill_id":"TCJA", "section":"SEC. 1", "section_heading":"TEST",
            "category":"override", "source_start_line":20, "source_end_line":21,
            "evidence_excerpt":"Notwithstanding subsection (a)", "source_basis":"official_bill_text_signal",
            "why_human_might_care":"An override may matter.", "question_to_investigate":"What rule is overridden?",
            "ordinary_explanations":["Overrides are normal drafting tools."], "uncertainty":["Need referenced rule."]
        }
        o = adjudicate(c)
        self.assertEqual(o.verdict, "QUESTION_ONLY")
        self.assertIsNone(o.allowed_public_statement)
        self.assertEqual(o.allowed_public_question, "What rule is overridden?")

    def test_bad_evidence_holds(self):
        c = {"candidate_id":"x", "category":"exception", "source_start_line":0, "source_end_line":0, "evidence_excerpt":""}
        self.assertEqual(adjudicate(c).verdict, "HOLD")

    def test_real_tcja_court_has_no_broad_claims_from_text_signals(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "court.json"
            p = run_court(ROOT / "artifacts" / "tcja_pass38_investigation_queue.json", out)
            self.assertEqual(p["opinion_count"], 40)
            self.assertGreater(p["question_only_count"], 0)
            for o in p["opinions"]:
                if o["category"] != "large_before_after_change":
                    self.assertIsNone(o["allowed_public_statement"])

    def test_every_opinion_has_adversarial_roles_and_receipt(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "court.json"
            p = run_court(ROOT / "artifacts" / "tcja_pass38_investigation_queue.json", out)
            for o in p["opinions"]:
                self.assertTrue(o["prosecutor"])
                self.assertTrue(o["defense"])
                self.assertTrue(o["progressive_reading"])
                self.assertTrue(o["conservative_reading"])
                self.assertTrue(o["text_referee"])
                self.assertTrue(o["citation_referee"])
                self.assertGreater(o["source_start_line"], 0)


if __name__ == "__main__":
    unittest.main()
