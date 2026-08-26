from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
TRANS=(ROOT/'public'/'transformation.js').read_text(encoding='utf-8')
APP=(ROOT/'public'/'app.js').read_text(encoding='utf-8')
class FourSignatures(unittest.TestCase):
    def test_four_signatures_exist(self):
        for key in ['tcja:{','ira:{','aca:{','chips:{']:
            self.assertIn(key,TRANS)
    def test_signature_tracks_current_bill(self):
        self.assertIn('transformation.synthesis[current]',APP)
    def test_tcja_real_pipeline_survives(self):
        for token in ['"1,402"','"40"','"33"','"14"','"660"']:
            self.assertIn(token,TRANS)
    def test_ira_real_cold_trial_counts(self):
        for token in ['"10"','"4"','"6"','"447"']:
            self.assertIn(token,TRANS)
    def test_aca_signature_is_lane_based(self):
        self.assertIn('evidence lanes kept separate',TRANS)
        self.assertIn('missing lanes silently invented',TRANS)
        self.assertIn('A missing lane stays missing.',TRANS)
    def test_chips_signature_is_mechanism_based(self):
        for token in ['$50B','$6B','$75B','25%','10 years']:
            self.assertIn(token,TRANS)
    def test_each_human_hold_is_unique(self):
        for title in ['The Tax Cut With More Than One Clock.','One Title, Several Machines.','“Keep Your Doctor” — What the Record Actually Supports.','The Chip Subsidy With a Leash.']:
            self.assertIn(title,TRANS)
if __name__=='__main__': unittest.main()
