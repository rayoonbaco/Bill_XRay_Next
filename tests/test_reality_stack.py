import json
import tempfile
import unittest
from pathlib import Path

from src.reality_stack import build_pass421, LANE_ORDER

ROOT = Path(__file__).resolve().parents[1]
CLAIM_MAP = ROOT / 'artifacts/pass42_claim_vs_law.json'
REGISTRY = ROOT / 'sources/aca_reality_stack_sources.json'


class RealityStackTests(unittest.TestCase):
    def build(self):
        td = tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)
        return build_pass421(CLAIM_MAP, REGISTRY, Path(td.name) / 'out.json')

    def test_all_reality_lanes_exist_and_stay_separate(self):
        p = self.build()
        self.assertEqual([x['lane'] for x in p['lanes']], LANE_ORDER)
        self.assertEqual(len({x['lane'] for x in p['lanes']}), len(LANE_ORDER))

    def test_missing_court_lane_does_not_claim_no_case_exists(self):
        p = self.build()
        court = next(x for x in p['lanes'] if x['lane'] == 'COURT_INTERPRETATION')
        self.assertEqual(court['status'], 'NO_SOURCE_LOADED')
        self.assertTrue(any('no relevant case exists' in x.lower() for x in court['cannot_conclude']))

    def test_source_authority_is_not_flattened(self):
        p = self.build()
        sources = p['source_registry']['sources']
        lanes = {x['lane'] for x in sources}
        self.assertIn('RHETORIC', lanes)
        self.assertIn('ENACTED_LAW', lanes)
        self.assertIn('IMPLEMENTATION', lanes)
        self.assertIn('OFFICIAL_ANALYSIS', lanes)
        self.assertIn('OBSERVED_OUTCOME', lanes)
        for source in sources:
            self.assertTrue(source['supported_meaning'])
            self.assertTrue(source['limits'])
            self.assertTrue(source.get('url') or source.get('local_source'))

    def test_bottom_line_preserves_causation_limit(self):
        p = self.build()
        bottom = p['public_answer']['bottom_line'].lower()
        self.assertIn('not enough to say', bottom)
        self.assertIn('caused', bottom)
        self.assertEqual(p['gap_analysis']['causation_status'], 'NOT_ESTABLISHED_BY_THIS_STACK')

    def test_reality_stack_does_not_collapse_to_true_false(self):
        p = self.build()
        joined = json.dumps(p['public_answer']).lower()
        self.assertNotIn('true/false', joined)
        self.assertNotIn('lied', joined)
        self.assertNotIn('deceived', joined)
        self.assertNotIn('fraud', joined)

    def test_minimum_primary_stack_loaded(self):
        p = self.build()
        by_lane = {x['lane']: x for x in p['lanes']}
        for lane in ('RHETORIC', 'ENACTED_LAW', 'IMPLEMENTATION'):
            self.assertEqual(by_lane[lane]['status'], 'EVIDENCE_LOADED')
            self.assertTrue(by_lane[lane]['source_ids'])


if __name__ == '__main__':
    unittest.main()
