import json
import tempfile
import unittest
from pathlib import Path

from src.investigation_engine import candidates_from_atomic_events, scan_text, write_payload


class InvestigationEngineTests(unittest.TestCase):
    def test_delegation_is_question_not_claim(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / 'bill.txt'
            p.write_text('SEC. 1. TEST.\nThe Secretary shall prescribe rules for this program.\n', encoding='utf-8')
            hits = scan_text(p, 'X')
            self.assertTrue(any(h.category == 'delegated_authority' for h in hits))
            hit = next(h for h in hits if h.category == 'delegated_authority')
            self.assertFalse(hit.public_claim_allowed)
            self.assertTrue(hit.ordinary_explanations)
            self.assertTrue(hit.uncertainty)
            self.assertIn('what decision', hit.question_to_investigate.lower())

    def test_exception_does_not_imply_favoritism(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / 'bill.txt'
            p.write_text('SEC. 2. TEST.\nSpecial rule for certain taxpayers.\n', encoding='utf-8')
            hits = scan_text(p, 'X')
            text = json.dumps([h.__dict__ for h in hits]).lower()
            self.assertNotIn('corrupt', text)
            self.assertNotIn('pork', text)
            self.assertNotIn('favoritism', text.replace('not evidence of favoritism', ''))

    def test_large_atomic_change_requires_context(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / 'events.json'
            p.write_text(json.dumps({'events':[{
                'event_id':'x', 'section':'SEC. 1', 'official_heading':'TEST',
                'semantic_label':'threshold', 'before':'$1,000', 'after':'$10,000',
                'source_start_line':3, 'source_end_line':3, 'evidence_excerpt':'substituting $10,000 for $1,000', 'publishable': True
            }]}), encoding='utf-8')
            rows = candidates_from_atomic_events(p, 'X')
            self.assertEqual(len(rows), 1)
            self.assertFalse(rows[0].public_claim_allowed)
            self.assertTrue(rows[0].uncertainty)
            self.assertIn('who is affected', rows[0].question_to_investigate.lower())


    def test_unresolved_atomic_event_cannot_drive_significance(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / 'events.json'
            p.write_text(json.dumps({'events':[{
                'event_id':'x', 'section':'SEC. 1', 'official_heading':'TEST',
                'semantic_label':'standard deduction', 'before':'$1,000', 'after':'$50,000',
                'source_start_line':3, 'source_end_line':3, 'evidence_excerpt':'x', 'publishable': False
            }]}), encoding='utf-8')
            self.assertEqual(candidates_from_atomic_events(p, 'X'), [])

    def test_real_tcja_payload_has_guardrails_and_diversity(self):
        root = Path(__file__).resolve().parents[1]
        out = root / 'artifacts' / '_test_pass38.json'
        payload = write_payload(root/'sources'/'tcja.txt', root/'artifacts'/'tcja_pass36_atomic_events.json', 'TCJA', out)
        self.assertGreaterEqual(payload['candidate_count'], 15)
        self.assertGreaterEqual(len(payload['category_counts']), 4)
        self.assertEqual(payload['public_claims_allowed'], 0)
        for c in payload['candidates']:
            self.assertTrue(c['ordinary_explanations'])
            self.assertTrue(c['uncertainty'])
            self.assertGreater(c['source_start_line'], 0)
        out.unlink(missing_ok=True)


if __name__ == '__main__':
    unittest.main()
