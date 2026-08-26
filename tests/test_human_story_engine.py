import json, tempfile, unittest
from pathlib import Path
from src.human_story_engine import build_story
ROOT=Path(__file__).resolve().parents[1]
class TestHumanStory(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(); self.out=Path(self.tmp.name)/'story.json'; self.p=build_story(ROOT/'artifacts/tcja_pass39_truth_court.json',self.out)
 def tearDown(self): self.tmp.cleanup()
 def test_only_court_cleared_facts_counted(self): self.assertEqual(self.p['supported_fact_count'],2)
 def test_no_final_readiness_on_thin_packet(self): self.assertEqual(self.p['release_readiness'],'NOT_FINAL_EDITORIAL')
 def test_human_labels(self):
  self.assertIn('child tax credit',self.p['story']); self.assertIn('estate and gift tax exclusion',self.p['story'])
 def test_questions_labeled(self): self.assertIn('Those are questions, not conclusions.',self.p['story'])
 def test_no_accusatory_language(self):
  low=self.p['story'].lower()
  for x in ['corrupt','bribe','fraud','pork','scam']: self.assertNotIn(x,low)
 def test_artifact_written(self): self.assertTrue(self.out.exists())
if __name__=='__main__': unittest.main()
