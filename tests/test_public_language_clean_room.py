from pathlib import Path
import json, unittest
ROOT=Path(__file__).resolve().parents[1]
PUB=ROOT/'public'

def load_data():
    raw=(PUB/'data.js').read_text(encoding='utf-8').strip()
    prefix='window.BXR_DATA = '
    return json.loads(raw[len(prefix):-1])

FORBIDDEN = [
    'cold generalization trial', 'cold trial', 'cold test', 'cold run',
    'evidence packet', 'reality stack', 'this pass', 'source and citation gates',
    'architecture', 'architectural', 'engine', 'human gate', 'machine verdict',
    'bill x-ray was not told', 'previously verified evidence'
]

class PublicLanguageCleanRoomTests(unittest.TestCase):
    def public_text(self, bill):
        parts=[bill.get('eyebrow',''), bill.get('title',''), bill.get('dek',''), bill.get('short','')]
        parts += [p.get('text','') for p in bill.get('story',[])]
        return '\n'.join(parts).lower()

    def test_upstairs_has_no_development_jargon(self):
        data=load_data()
        for key,bill in data.items():
            text=self.public_text(bill)
            for phrase in FORBIDDEN:
                self.assertNotIn(phrase, text, f'{key}: {phrase}')

    def test_public_shell_is_unchanged_in_shape(self):
        data=load_data()
        self.assertEqual(set(data), {'tcja','ira','aca','chips','sb1570'})
        h=(PUB/'index.html').read_text(encoding='utf-8')
        self.assertEqual(h.count('data-bill='), 5)
        self.assertEqual(h.count('CHECK MY HOMEWORK'), 1)
        self.assertIn('THE 30-SECOND VERSION', h)

    def test_receipts_remain_available_downstairs(self):
        data=load_data()
        self.assertEqual(len(data['tcja']['receipts']),14)
        self.assertEqual(len(data['ira']['receipts']),6)
        self.assertEqual(len(data['aca']['receipts']),6)
        self.assertEqual(len(data['chips']['receipts']),9)
        self.assertEqual(len(data['sb1570']['receipts']),13)
        self.assertTrue(data['tcja']['homework_note'])
        self.assertTrue(data['ira']['homework_note'])
        self.assertTrue(data['aca']['homework_note'])
        self.assertTrue(data['chips']['homework_note'])
        self.assertTrue(data['sb1570']['homework_note'])

    def test_ira_public_story_is_citizen_facing(self):
        data=load_data(); text=self.public_text(data['ira'])
        self.assertIn('numbers need nouns', text)
        self.assertIn('loan guarantees are not appropriations', data['ira']['short'].lower())
        self.assertIn('understanding comes before argument', text)

    def test_aca_public_label_is_plain(self):
        data=load_data()
        self.assertEqual(data['aca']['eyebrow'], 'Affordable Care Act · 2010')

if __name__=='__main__':
    unittest.main()
