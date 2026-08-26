import json, tempfile, unittest
from pathlib import Path
from src.editorial_room import build_room
from src.editorial_story import build_story

ROOT=Path(__file__).resolve().parents[1]
COVER=ROOT/'artifacts/tcja_pass40_1_semantic_coverage.json'

class EditorialRoomTests(unittest.TestCase):
    def test_room_supports_every_move(self):
        with tempfile.TemporaryDirectory() as td:
            p=build_room(COVER,Path(td)/'room.json')
            self.assertGreaterEqual(p['selected_fact_count'],20)
            self.assertGreaterEqual(p['editorial_move_count'],6)
            for m in p['accepted_editorial_moves']:
                self.assertTrue(m['support_fact_ids'])
                self.assertFalse(m['missing_support'])
    def test_no_dangerous_accusation_language(self):
        with tempfile.TemporaryDirectory() as td:
            p=build_room(COVER,Path(td)/'room.json')
            text=' '.join(m['text'].lower() for m in p['accepted_editorial_moves'])
            for w in ('corrupt','bribe','scam','fraud','steal','theft','pork'):
                self.assertNotIn(w,text)
    def test_story_has_traceable_editorial_ledger(self):
        with tempfile.TemporaryDirectory() as td:
            room=Path(td)/'room.json'; story=Path(td)/'story.json'
            rp=build_room(COVER,room); sp=build_story(room,story)
            fact_ids={f['fact_id'] for f in rp['selected_facts']}
            self.assertGreaterEqual(sp['word_count'],700)
            self.assertLessEqual(sp['word_count'],1200)
            self.assertEqual(sp['release_readiness'],'EDITORIAL_READY_FOR_RAY_GATE')
            for row in sp['sentence_ledger']:
                self.assertTrue(row['support_fact_ids'])
                self.assertTrue(set(row['support_fact_ids']).issubset(fact_ids))
    def test_voice_is_original_not_named_author_imitation(self):
        with tempfile.TemporaryDirectory() as td:
            room=Path(td)/'room.json'; story=Path(td)/'story.json'
            build_room(COVER,room); sp=build_story(room,story)
            voice=sp['voice'].lower()
            for name in ('twain','steinbeck','hemingway','thompson','voltaire'):
                self.assertNotIn(name,voice)

if __name__=='__main__': unittest.main()
