from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
FOUNDATION = "https://www.ilga.gov/Legislation/PublicActs/PrinterFriendly/103-0491"
AMENDMENT = "https://www.ilga.gov/Legislation/PublicActs/PrinterFriendly/104-0395"


def load_public_data():
    raw = (ROOT / "public" / "data.js").read_text(encoding="utf-8").strip()
    return json.loads(raw[len("window.BXR_DATA = "):-1])


class SB1570CurrentLawRegression(unittest.TestCase):
    def test_visible_status_and_both_official_sources(self):
        bill = load_public_data()["sb1570"]
        self.assertEqual(bill["current_law_status"], "CURRENT LAW CHECKED THROUGH P.A. 104-0395")
        urls = {item["url"] for item in bill["source_links"]}
        self.assertEqual(urls, {FOUNDATION, AMENDMENT})

        app = (ROOT / "public" / "app.js").read_text(encoding="utf-8")
        html = (ROOT / "public" / "index.html").read_text(encoding="utf-8")
        self.assertIn("renderCurrentLawSources", app)
        self.assertIn('id="currentLawSources"', html)
        self.assertIn("current==='sb1570' ? data.sb1570.source_links", app)
        self.assertIn("current==='sb1570' ? renderCurrentLawSources(data.sb1570)", app)

    def test_municipal_single_response_rule_is_complete(self):
        bill = load_public_data()["sb1570"]
        receipt = next(r for r in bill["receipts"] if r["id"] == "shortlist")
        text = json.dumps(receipt).lower()
        for required in ["two to six", "only one phase i response", "single respondent", "discretion", "best interest", "104-0395"]:
            self.assertIn(required, text)
        self.assertIn(FOUNDATION.lower(), text)
        self.assertIn(AMENDMENT.lower(), text)

    def test_school_only_error_cannot_return(self):
        files = [
            ROOT / "public" / "data.js",
            ROOT / "public" / "business-lens.js",
            ROOT / "public" / "transformation.js",
            ROOT / "sources" / "sb1570_public_act_receipts.json",
        ] + list((ROOT / "PSI_SB1570_HANDOFF").glob("*"))
        corpus = "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in files if p.is_file()).lower()
        forbidden = [
            "single-respondent option appears in the school provision, not the municipal provision",
            "school districts have a limited one-respondent exception",
            "school rules allow a narrow one-respondent path",
            "school single-respondent rules captured",
        ]
        for phrase in forbidden:
            self.assertNotIn(phrase, corpus)
        self.assertIn("single-response option is not a school-only distinction", corpus)

    def test_business_lens_states_ordinary_rule_and_exception(self):
        lens = (ROOT / "public" / "business-lens.js").read_text(encoding="utf-8").lower()
        for required in ["ordinary municipal phase ii shortlist", "two to six", "only one phase i response", "best interest", "104-0395", FOUNDATION.lower(), AMENDMENT.lower()]:
            self.assertIn(required, lens)

    def test_machine_readable_sources_and_rule(self):
        source = json.loads((ROOT / "sources" / "sb1570_public_act_receipts.json").read_text(encoding="utf-8"))
        rules = json.loads((ROOT / "PSI_SB1570_HANDOFF" / "STATUTORY_RULES.json").read_text(encoding="utf-8"))
        machine = json.loads((ROOT / "PSI_SB1570_HANDOFF" / "BUSINESS_DEVELOPMENT_LENS_MACHINE.json").read_text(encoding="utf-8"))
        self.assertEqual(source["current_law_checked_through"], "Public Act 104-0395")
        self.assertIn("single respondent", rules["municipal_shortlist"]["rule"].lower())
        self.assertEqual(machine["current_law"]["municipal_amendment"], "104-0395")

    def test_other_four_cases_do_not_gain_current_law_banner(self):
        data = load_public_data()
        for bill_id in ("tcja", "ira", "aca", "chips"):
            self.assertNotIn("current_law_status", data[bill_id])
            self.assertNotIn("source_links", data[bill_id])


if __name__ == "__main__":
    unittest.main()
