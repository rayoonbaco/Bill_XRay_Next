import json, re, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

class TransformationLadderTests(unittest.TestCase):
    def setUp(self):
        self.html=(ROOT/'public/index.html').read_text(encoding='utf-8')
        self.js=(ROOT/'public/app.js').read_text(encoding='utf-8')
        self.data=(ROOT/'public/transformation.js').read_text(encoding='utf-8')
        self.css=(ROOT/'public/styles.css').read_text(encoding='utf-8')

    def test_one_transformation_doorway(self):
        self.assertEqual(self.html.count('id="transformationButton"'),1)
        self.assertIn('HOW THIS BECAME HUMAN',self.html)

    def test_overlay_hidden_until_requested(self):
        self.assertIn('id="transformation" class="transformation" aria-hidden="true"',self.html)
        self.assertIn('.transformation.open',self.css)

    def test_real_chips_provision_is_used(self):
        self.assertIn('SEC. 102(a)(2)(B)',self.data)
        self.assertIn('$6,000,000,000',self.data)
        self.assertIn('$75,000,000,000',self.data)

    def test_semantic_distinction_survives(self):
        self.assertIn('loan principal is not the same legal thing as a cash appropriation',self.data.lower())
        self.assertIn("not a $75 billion cash appropriation",self.data.lower())

    def test_ladder_has_eight_stages(self):
        stages=re.findall(r'stage: "([1-8]\. [^"]+)"',self.data)
        self.assertEqual(len(stages),8)

    def test_finished_sentence_keeps_receipt(self):
        self.assertIn('GovInfo - Public Law 117-167 - p. 8 - lines 417-428',self.data)
        self.assertIn('Nothing was removed from the truth. Only from the difficulty.',self.data)

    def test_existing_public_contract_remains(self):
        self.assertEqual(self.html.count('id="homeworkButton"'),1)
        for bill in ('tcja','ira','aca','chips'):
            self.assertIn(f'data-bill="{bill}"',self.html)

if __name__=='__main__': unittest.main()
