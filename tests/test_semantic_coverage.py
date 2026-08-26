import json, tempfile, unittest
from pathlib import Path
from src.semantic_coverage import build_coverage
from src.human_story_engine import build_story

ROOT=Path(__file__).resolve().parents[1]

class SemanticCoverageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.coverage=build_coverage(ROOT/'sources'/'tcja.txt','TCJA')

    def test_broad_coverage_without_holds(self):
        self.assertGreaterEqual(self.coverage['fact_count'],30)
        self.assertEqual(self.coverage['hold_count'],0)
        self.assertGreaterEqual(len(self.coverage['category_counts']),7)

    def test_every_fact_has_receipt_and_limits_field(self):
        for f in self.coverage['facts']:
            self.assertTrue(f['evidence_excerpt'].strip())
            self.assertGreaterEqual(f['source_start_line'],1)
            self.assertGreaterEqual(f['source_end_line'],f['source_start_line'])
            self.assertGreaterEqual(f['confidence'],0.95)
            self.assertEqual(f['status'],'COURT_CLEARED_DIRECT')
            self.assertIsInstance(f['limits'],list)

    def test_direct_lane_does_not_claim_motive_or_distribution(self):
        text=' '.join(f['statement'].lower() for f in self.coverage['facts'])
        for forbidden in ('corrupt','wasteful','because congress wanted','benefits the rich','hurts the poor','saves taxpayers'):
            self.assertNotIn(forbidden,text)

    def test_key_human_facts_exist(self):
        ids={f['fact_id'] for f in self.coverage['facts']}
        required={'rates_window','child_credit_amount','qbi_20_percent','corporate_rate','salt_cap','interest_limit','oz_definition','oz_180_days'}
        self.assertTrue(required.issubset(ids))

    def test_expanded_story_has_real_substrate(self):
        with tempfile.TemporaryDirectory() as td:
            cov=Path(td)/'coverage.json'; out=Path(td)/'story.json'
            cov.write_text(json.dumps(self.coverage),encoding='utf-8')
            p=build_story(ROOT/'artifacts'/'tcja_pass39_truth_court.json',out,cov)
            self.assertGreaterEqual(p['supported_fact_count'],30)
            self.assertGreaterEqual(p['word_count'],800)
            self.assertLessEqual(p['word_count'],1300)
            self.assertEqual(p['release_readiness'],'STORY_READY_FOR_HUMAN_GATE')
            self.assertIn('Opportunity Zones',p['story'])
            self.assertIn('21%',p['story'])

if __name__=='__main__': unittest.main()
