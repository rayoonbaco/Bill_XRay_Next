import json, tempfile, unittest
from pathlib import Path
from src.columnist import build_column

ROOT = Path(__file__).resolve().parents[1]
COVER = ROOT / 'artifacts/tcja_pass40_1_semantic_coverage.json'

class ColumnistTests(unittest.TestCase):
    def test_column_has_one_thesis_and_selects_hard(self):
        with tempfile.TemporaryDirectory() as td:
            p = build_column(COVER, Path(td)/'column.json')
            self.assertTrue(p['thesis'])
            self.assertGreaterEqual(p['selected_fact_count'], 8)
            self.assertLessEqual(p['selected_fact_count'], 15)
            self.assertLess(p['selected_fact_count'], p['available_fact_count'])

    def test_first_three_paragraph_hook_contract(self):
        with tempfile.TemporaryDirectory() as td:
            p = build_column(COVER, Path(td)/'column.json')
            first3 = p['paragraphs'][:3]
            self.assertEqual(len(first3), 3)
            self.assertLessEqual(sum(x['word_count'] for x in first3), 260)
            self.assertTrue(any(x['kind'] in ('WIT','SYNTHESIS','ANALOGY') for x in first3))
            joined = ' '.join(x['text'].lower() for x in first3)
            self.assertIn('tax', joined)
            self.assertTrue(('clock' in joined) or ('headline' in joined) or ('expiration' in joined))

    def test_every_paragraph_is_supported(self):
        with tempfile.TemporaryDirectory() as td:
            p = build_column(COVER, Path(td)/'column.json')
            selected = set(p['selected_fact_ids'])
            for row in p['paragraphs']:
                self.assertTrue(row['support_fact_ids'])
                self.assertTrue(set(row['support_fact_ids']).issubset(selected))

    def test_column_is_column_length_and_not_accusatory(self):
        with tempfile.TemporaryDirectory() as td:
            p = build_column(COVER, Path(td)/'column.json')
            self.assertGreaterEqual(p['word_count'], 650)
            self.assertLessEqual(p['word_count'], 1000)
            text = p['story'].lower()
            for word in ('corrupt','bribe','scam','fraud','theft','stole','pork'):
                self.assertNotIn(word, text)

    def test_column_does_not_march_through_all_categories(self):
        with tempfile.TemporaryDirectory() as td:
            p = build_column(COVER, Path(td)/'column.json')
            # The columnist must omit at least half the available facts.
            self.assertLessEqual(p['selected_fact_count'], p['available_fact_count'] // 2)
            self.assertEqual(p['release_readiness'], 'COLUMN_READY_FOR_RAY_GATE')

if __name__ == '__main__':
    unittest.main()
