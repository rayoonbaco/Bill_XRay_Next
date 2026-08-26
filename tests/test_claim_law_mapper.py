import json
import tempfile
import unittest
from pathlib import Path

from src.claim_law_mapper import build_pass42

ROOT = Path(__file__).resolve().parents[1]
CLAIM = ROOT / 'sources/aca_keep_doctor_claim.json'
ACA = ROOT / 'sources/aca_claim_law_excerpt.txt'
TCJA = ROOT / 'artifacts/tcja_pass40_1_semantic_coverage.json'


class ClaimLawMapperTests(unittest.TestCase):
    def build(self):
        td = tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)
        return build_pass42(CLAIM, ACA, TCJA, Path(td.name) / 'out.json')

    def test_aca_claim_is_not_reduced_to_true_false(self):
        p = self.build()['aca_keep_doctor']
        self.assertEqual(p['verdict']['classification'], 'CLAIM_BROADER_THAN_STATUTORY_GUARANTEE')
        self.assertNotIn('TRUE', p['verdict']['classification'])
        self.assertNotIn('FALSE', p['verdict']['classification'])

    def test_aca_map_preserves_conditions(self):
        p = self.build()['aca_keep_doctor']
        text = json.dumps(p).lower()
        self.assertIn('participating', text)
        self.assertIn('available', text)
        self.assertIn('grandfathered', text)
        self.assertIn('sufficient choice', text)

    def test_no_motive_or_outcome_overreach(self):
        p = self.build()['aca_keep_doctor']
        joined = ' '.join([p['verdict']['short'], p['public_render']['human_conclusion']]).lower()
        for bad in ('lied', 'fraud', 'deceived', 'corrupt', 'caused people to lose'):
            self.assertNotIn(bad, joined)
        self.assertTrue(p['verdict']['not_a_verdict_on'])

    def test_every_aca_clause_has_evidence(self):
        p = self.build()['aca_keep_doctor']
        evidence_ids = {x['evidence_id'] for x in p['law_evidence']}
        for clause in p['claim_clauses']:
            self.assertTrue(clause['evidence_ids'])
            self.assertTrue(set(clause['evidence_ids']).issubset(evidence_ids))

    def test_tcja_true_headline_can_still_be_incomplete(self):
        p = self.build()['tcja_child_credit']
        self.assertEqual(p['verdict']['classification'], 'SUPPORTED_BUT_INCOMPLETE')
        self.assertEqual(set(p['support_fact_ids']), {'child_credit_amount', 'refundable_cap', 'child_ssn'})

    def test_source_anchors_are_real(self):
        p = self.build()['aca_keep_doctor']
        for row in p['law_evidence']:
            self.assertGreater(len(row['evidence_excerpt']), 40)
            self.assertTrue(row['section'])
            self.assertTrue(row['source_path'])


if __name__ == '__main__':
    unittest.main()
