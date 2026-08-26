import json, pathlib, sys, unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from src.generalization_trial import run

class GeneralizationTrialTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.out=ROOT/'artifacts'/'pass43_generalization_trial.json'
  cls.p=run(ROOT/'sources'/'ira_legacy_verified',cls.out)
 def test_source_integrity(self): self.assertEqual(self.p['source_sha256'],self.p['expected_source_sha256'])
 def test_legacy_release_is_verified(self): self.assertEqual(self.p['legacy_release_status'],'verified')
 def test_real_diversity(self): self.assertGreaterEqual(self.p['available_verified_facts'],8); self.assertGreaterEqual(len(self.p['topic_counts']),3)
 def test_editor_selects_not_dumps(self): self.assertLess(self.p['selected_fact_count'],self.p['available_verified_facts']); self.assertLessEqual(self.p['selected_fact_count'],14)
 def test_no_causation_shortcut(self): self.assertIn('do not rewrite',self.p['reality_context']['guardrail']); self.assertIn('prove causation',self.p['reality_context']['guardrail'])
 def test_column_is_human_length(self): self.assertGreater(self.p['column_word_count'],350); self.assertLess(self.p['column_word_count'],950)
 def test_no_tcja_or_aca_special_case_in_engine(self):
  src=(ROOT/'src'/'generalization_trial.py').read_text(encoding='utf-8').lower()
  self.assertNotIn('tcja',src); self.assertNotIn('obamacare',src); self.assertNotIn('affordable care act',src)

if __name__=='__main__': unittest.main()
