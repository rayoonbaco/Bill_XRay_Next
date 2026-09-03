from pathlib import Path
import json, re, unittest
ROOT=Path(__file__).resolve().parents[1]
PUB=ROOT/'public'

def load_data():
    raw=(PUB/'data.js').read_text(encoding='utf-8').strip()
    prefix='window.BXR_DATA = '
    assert raw.startswith(prefix) and raw.endswith(';')
    return json.loads(raw[len(prefix):-1])

class PublicProductTests(unittest.TestCase):
    def test_public_files_exist(self):
        for name in ['index.html','styles.css','app.js','data.js','business-lens.js','transformation-examples.js']:
            self.assertTrue((PUB/name).exists(), name)

    def test_first_surface_is_small(self):
        h=(PUB/'index.html').read_text(encoding='utf-8')
        self.assertEqual(h.count('data-bill='),5)
        self.assertEqual(h.count('id="homeworkButton"'),1)
        self.assertIn('THE 30-SECOND VERSION',h)
        self.assertIn('aria-hidden="true"',h)
        for backstage in ['ROSETTA GRAMMAR','TRUTH COURT','ATOMIC EVENTS','INVESTIGATION SCORE','PROVENANCE CLASS']:
            self.assertNotIn(backstage,h.upper())

    def test_three_public_stories_have_receipts(self):
        d=load_data()
        self.assertEqual(set(d),{'tcja','ira','aca','chips','sb1570'})
        for key,b in d.items():
            self.assertTrue(b['title'])
            self.assertTrue(b['short'])
            self.assertGreaterEqual(len(b['story']),4,key)
            self.assertGreaterEqual(len(b['receipts']),1,key)

    def test_evidence_stays_behind_one_path(self):
        h=(PUB/'index.html').read_text(encoding='utf-8')
        js=(PUB/'app.js').read_text(encoding='utf-8')
        self.assertEqual(h.count('CHECK MY HOMEWORK'),1)
        self.assertEqual(js.count("q('#homeworkButton').addEventListener('click',openDrawer)"),1)
        self.assertIn("q('#homework').classList.add('open')",js)
        self.assertIn("q('#homework').classList.remove('open')",js)

    def test_receipts_are_from_cleared_artifacts(self):
        d=load_data()
        tcja=json.loads((ROOT/'artifacts/tcja_pass41_1_column.json').read_text(encoding='utf-8'))
        ira=json.loads((ROOT/'artifacts/pass43_generalization_trial.json').read_text(encoding='utf-8'))
        aca=json.loads((ROOT/'artifacts/pass42_1_reality_stack.json').read_text(encoding='utf-8'))
        self.assertEqual(len(d['tcja']['receipts']),tcja['selected_fact_count'])
        self.assertEqual(len(d['ira']['receipts']),ira['selected_fact_count'])
        loaded_aca=sum(len(x.get('source_ids',[])) for x in aca['lanes'])
        self.assertEqual(len(d['aca']['receipts']),loaded_aca)
        self.assertEqual(len(d['chips']['receipts']),9)
        self.assertEqual(len(d['sb1570']['receipts']),13)

    def test_launchers_live_in_root(self):
        self.assertTrue((ROOT/'ONE_CLICK_PASS_44.bat').exists())
        self.assertTrue((ROOT/'START_BILL_XRAY_PUBLIC.bat').exists())

if __name__=='__main__': unittest.main()
