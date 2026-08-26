from pathlib import Path
import json, subprocess, sys, unittest
from src.editorial_room import build_room
from src.editorial_story import build_story
ROOT=Path(__file__).resolve().parent
ART=ROOT/'artifacts'
room=build_room(ART/'tcja_pass40_1_semantic_coverage.json',ART/'tcja_pass41_editorial_room.json')
story=build_story(ART/'tcja_pass41_editorial_room.json',ART/'tcja_pass41_editorial_story.json')
loader=unittest.TestLoader(); suite=loader.discover(str(ROOT/'tests'),pattern='test_editorial_room.py'); result=unittest.TextTestRunner(verbosity=1).run(suite)
print('\n'+'='*72)
print(' BILL X-RAY NEXT - PASS 41 SMOKE CAST')
print(' EDITORIAL INTELLIGENCE ROOM')
print('='*72)
print('\nYOUR DUTIES THIS PASS')
print('  1. Read the editorial choices and the full essay below.')
print('  2. Judge it as a HUMAN: would you voluntarily keep reading?')
print('  3. Ask whether the wit clarifies or merely performs.')
print('  4. Send the full smoke cast and your reaction back to the team.')
print('\nWHAT THIS PASS MUST PROVE')
print('  - The editor can omit facts without losing the law\'s basic shape.')
print('  - Synthesis, analogy, and wit are traceable to cleared facts.')
print('  - Humor cannot create accusations, motives, or new factual claims.')
print('  - The result sounds like an original human editorial, not an analytics report.')
print(f"\nPASS 41 ROOM: {room['selected_fact_count']} selected facts; {room['editorial_move_count']} accepted editorial moves; {len(room['rejected_editorial_moves'])} rejected")
print(f"PASS 41 STORY: {story['word_count']} words; {story['facts_used_count']} facts used; {story['editorial_moves_used_count']} editorial moves used")
print(f"Focused checks: {result.testsRun - len(result.errors) - len(result.failures)}/{result.testsRun} passed")
print('\nEDITORIAL ROOM CHECK')
for m in room['accepted_editorial_moves']:
    print(f"  [{m['kind']}] {m['text']}")
print('\n--------------------- I READ THE BILL ---------------------')
print(story['story'])
print('-----------------------------------------------------------')
print('\nMACHINE VERDICT:',story['release_readiness'])
print('HUMAN GATE: Does this finally feel like somebody understood the bill and then explained it, rather than a machine reciting extracted facts?')
cast='\n'.join([
 'PASS 41 CLEAR' if result.wasSuccessful() else 'PASS 41 NEEDS REVIEW',
 f"story_words={story['word_count']}",f"facts_used={story['facts_used_count']}",f"editorial_moves={story['editorial_moves_used_count']}",
 'readiness='+story['release_readiness']])
(ART/'SMOKE_CAST_PASS_41.txt').write_text(cast,encoding='utf-8')
if not result.wasSuccessful(): sys.exit(1)
print('\n'+'='*72); print(' CLEAR - PASS 41 ENGINE PASSED - RAY HUMAN GATE REQUIRED'); print('='*72)
