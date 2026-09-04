from pathlib import Path
import json, unittest
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from src.teacher_gate import grade

def load_data():
    raw=(ROOT/'public'/'data.js').read_text(encoding='utf-8').strip()
    return json.loads(raw[len('window.BXR_DATA = '):-1])

class SB1570PublicCase(unittest.TestCase):
    def test_case_is_selectable(self):
        html=(ROOT/'public'/'index.html').read_text(encoding='utf-8')
        self.assertIn('data-bill="sb1570"',html)

    def test_story_traces_to_receipts(self):
        bill=load_data()['sb1570']; ids={r['id'] for r in bill['receipts']}
        for paragraph in bill['story']:
            self.assertTrue(paragraph['support_fact_ids'])
            self.assertTrue(set(paragraph['support_fact_ids']) <= ids)

    def test_authority_is_not_misrepresented_as_demand(self):
        bill=load_data()['sb1570']
        public=' '.join([bill['short'],bill['dek']]+[p['text'] for p in bill['story']]).lower()
        self.assertIn('not a project',public)
        self.assertIn('no public owner is required',public)
        self.assertIn('permission is a fact',public)

    def test_high_risk_details_are_preserved(self):
        bill=load_data()['sb1570']; all_text=json.dumps(bill)
        for token in ['14 days','30%','$12 million','appearance of impropriety','every six months']:
            self.assertIn(token,all_text)

    def test_municipal_school_threshold_difference_is_disclosed(self):
        receipt=next(r for r in load_data()['sb1570']['receipts'] if r['id']=='small_projects')
        self.assertIn('differs at exactly $12 million',receipt['limits'][0])

    def test_teacher_release_gate_is_a(self):
        result=grade('sb1570')
        self.assertGreaterEqual(result['score'],93)
        self.assertEqual(result['grade'],'A')

    def test_business_lens_is_exclusive_to_sb1570(self):
        lens=(ROOT/'public'/'business-lens.js').read_text(encoding='utf-8')
        app=(ROOT/'public'/'app.js').read_text(encoding='utf-8')
        self.assertIn('bill_id:"sb1570"',lens)
        self.assertIn("id==='sb1570'",app)
        self.assertNotIn('tcja:',lens); self.assertNotIn('ira:',lens); self.assertNotIn('aca:',lens); self.assertNotIn('chips:',lens)

    def test_public_files_are_private_name_free(self):
        public='\n'.join(p.read_text(encoding='utf-8',errors='ignore') for p in (ROOT/'public').glob('*') if p.is_file()).lower()
        for forbidden in ['performance services','psi pursuit','tom terry','ray gomez']:
            self.assertNotIn(forbidden,public)

    def test_sb1570_transformation_is_not_chips(self):
        examples=(ROOT/'public'/'transformation-examples.js').read_text(encoding='utf-8')
        sb=examples.split('sb1570:example(',1)[1]
        self.assertIn('Public Act 103-0491',sb)
        self.assertIn('municipality may enter into design-build contracts',sb.lower())
        self.assertNotIn('$75,000,000,000',sb)

if __name__=='__main__': unittest.main()
