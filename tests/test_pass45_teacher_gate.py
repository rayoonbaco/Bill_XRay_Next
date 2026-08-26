from pathlib import Path
import json,unittest
ROOT=Path(__file__).resolve().parents[1]
import sys; sys.path.insert(0,str(ROOT))
from src.teacher_gate import grade,load_data

class Pass45Tests(unittest.TestCase):
    def test_four_bills_on_public_surface(self):
        data=load_data(); self.assertEqual(set(data),{'tcja','ira','aca','chips'})
        h=(ROOT/'public/index.html').read_text(encoding='utf-8')
        self.assertEqual(h.count('data-bill='),4); self.assertIn('data-bill="chips"',h)
    def test_chips_has_real_receipts(self):
        b=load_data()['chips']; self.assertGreaterEqual(len(b['receipts']),8)
        for r in b['receipts']:
            self.assertTrue(r['id']); self.assertTrue(r['source']); self.assertTrue(r['section']); self.assertTrue(r['excerpt']); self.assertTrue(r['limits'])
    def test_every_paragraph_traces_to_receipts(self):
        b=load_data()['chips']; ids={r['id'] for r in b['receipts']}
        for p in b['story']:
            self.assertTrue(p['support_fact_ids']); self.assertTrue(set(p['support_fact_ids'])<=ids)
    def test_number_nouns_are_not_blended(self):
        b=load_data()['chips']; text=' '.join(p['text'] for p in b['story']).lower()
        self.assertIn('not a $75 billion cash appropriation',text)
        self.assertIn('a tax credit is not a grant',text)
    def test_public_language_stays_upstairs(self):
        b=load_data()['chips']; text=' '.join([b['eyebrow'],b['title'],b['dek'],b['short']]+[p['text'] for p in b['story']]).lower()
        for x in ['cold trial','evidence packet','reality stack','machine verdict','human gate','architecture','this pass']:
            self.assertNotIn(x,text)
    def test_teacher_grade_is_a(self):
        g=grade('chips'); self.assertGreaterEqual(g['score'],93); self.assertEqual(g['grade'],'A')
    def test_one_homework_doorway_remains(self):
        h=(ROOT/'public/index.html').read_text(encoding='utf-8'); self.assertEqual(h.count('CHECK MY HOMEWORK'),1)

if __name__=='__main__': unittest.main()
