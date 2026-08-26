from pathlib import Path
import re, unittest
ROOT=Path(__file__).resolve().parents[1]
DATA=(ROOT/'public'/'data.js').read_text(encoding='utf-8')
TRANS=(ROOT/'public'/'transformation.js').read_text(encoding='utf-8')
APP=(ROOT/'public'/'app.js').read_text(encoding='utf-8')
CSS=(ROOT/'public'/'styles.css').read_text(encoding='utf-8')

class LaunchFinish(unittest.TestCase):
    def test_four_bills_remain(self):
        for key in ['"tcja"','"ira"','"aca"','"chips"']:
            self.assertIn(key,DATA)
    def test_synthesis_reveal_uses_real_tcja_counts(self):
        for token in ['"1,402"','"40"','"33"','"14"','"660"']:
            self.assertIn(token,TRANS)
    def test_reveal_is_rendered(self):
        self.assertIn('synthesis-reveal',APP)
        self.assertIn('WHAT AI HAD TO HOLD',APP)
        self.assertIn('WHAT YOU HAVE TO HOLD',APP)
    def test_public_truth_court_name_removed_from_ladder(self):
        self.assertNotIn('5. TRUTH COURT',TRANS)
        self.assertIn('CHALLENGE THE CONCLUSION',TRANS)
    def test_aca_backstage_label_removed(self):
        self.assertNotIn('Reality Stack keeps',DATA)
    def test_launch_doctrine_present(self):
        self.assertIn("The machine carries the complexity so the reader doesn't have to.",TRANS)
        self.assertIn('Understanding first. Argument afterward.',TRANS)
    def test_editorial_forge_did_not_remove_receipts(self):
        self.assertGreaterEqual(DATA.count('"receipts"'),4)
        self.assertIn('support_fact_ids',DATA)
    def test_styles_for_reveal_exist(self):
        self.assertIn('.synthesis-metrics',CSS)
        self.assertIn('.complexity-compare',CSS)

if __name__=='__main__': unittest.main()
