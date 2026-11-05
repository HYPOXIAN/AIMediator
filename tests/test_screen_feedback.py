import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'src'))
from aimediator.collection import screening


def row(text):
    return {'record_id':'fixture:1','text_original':text}


class ScreeningTests(unittest.TestCase):
    def test_explicit_positive_and_negative_balance_both_survive(self):
        for text in ['The characters are very balanced.', 'Ryu is too strong, nerf him.', '请加强JP，伤害太低了', '好平衡']:
            self.assertEqual(screening.classify(row(text))[0],'keep',text)

    def test_pricing_does_not_hide_balance_in_mixed_review(self):
        self.assertEqual(screening.classify(row('DLC is expensive. Ryu needs a nerf.'))[0],'keep')
        self.assertEqual(screening.classify(row('DLC costs too much money.'))[0],'exclude')

    def test_keyword_in_editing_or_visual_context_is_not_balance(self):
        for text in ['Top tier editing skills there!', 'The best balance between nostalgia and modern visuals.', 'Please buff the graphics.']:
            self.assertEqual(screening.classify(row(text))[0],'exclude',text)

    def test_generic_praise_and_new_player_accessibility_are_excluded(self):
        for text in ['Great game!', 'I love Modern controls because they make the game accessible.', '选择这款游戏很不错', '上手简单，连招很爽']:
            self.assertEqual(screening.classify(row(text))[0],'exclude',text)

    def test_mechanic_fairness_is_retained(self):
        for text in ['Throw loops are unfair.', 'Modern controls allow unfair one button supers.', '斗气防住还打白血，伤害太高了']:
            self.assertEqual(screening.classify(row(text))[0],'keep',text)

    def test_world_tour_difficulty_and_connection_only_are_excluded(self):
        for text in ['World Tour bosses are too strong and deal too much damage.', 'The ranked matchmaking has terrible ping and disconnects.']:
            self.assertEqual(screening.classify(row(text))[0],'exclude',text)

    def test_ambiguous_bare_mechanic_is_review_not_auto_keep(self):
        self.assertEqual(screening.classify(row('Drive impact'))[0],'review')

    def test_other_game_only_discussion_is_excluded(self):
        self.assertEqual(screening.classify(row('Tekken is an unbalanced game.'))[0],'exclude')

    def test_boundary_override_requires_unchanged_source_text(self):
        original=row('visual topic');override={'fixture:1':{'text_sha256':hashlib.sha256(original['text_original'].encode()).hexdigest(),'decision':'exclude','reason':'presentation'}}
        self.assertEqual(screening.classify(original,override)[3],'agent_boundary_review')
        with self.assertRaises(ValueError):
            screening.classify(row('edited visual topic'),override)

    def test_overlapping_views_are_deduplicated_and_original_files_unchanged(self):
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder);source=json.dumps(row('Ryu needs a nerf.'))+'\n'
            (p/'records.jsonl').write_text(source, encoding='utf-8');(p/'english.jsonl').write_text(source, encoding='utf-8')
            union,members,hashes=screening.load_sources(p)
            self.assertEqual(len(union),1)
            self.assertEqual(len(members),2)
            self.assertEqual((p/'records.jsonl').read_text(encoding='utf-8'),source)
            self.assertEqual(hashes['records.jsonl'],hashlib.sha256(source.encode()).hexdigest())

    def test_language_correction_rebuilds_cross_language_views_without_editing_raw(self):
        with tempfile.TemporaryDirectory() as directory:
            folder=Path(directory);source=folder/'raw';source.mkdir();output=folder/'screened'
            original={'record_id':'fixture:cn','text_original':'请加强隆，伤害太低了','language':'en','platform':'steam','source_url':'https://example.org'}
            raw=json.dumps(original,ensure_ascii=False)+'\n'
            (source/'records.jsonl').write_text(raw, encoding='utf-8');(source/'english.jsonl').write_text(raw, encoding='utf-8');(source/'chinese.jsonl').write_text('', encoding='utf-8')
            overrides=folder/'overrides.json';overrides.write_text(json.dumps({'entries':[]}), encoding='utf-8')
            corrections=folder/'languages.json';corrections.write_text(json.dumps({'entries':[{'record_id':original['record_id'],'language':'zh','reason':'Original text is Chinese.','text_sha256':hashlib.sha256(original['text_original'].encode()).hexdigest()}]}),encoding='utf-8')
            with patch('builtins.print'):
                screening.main(['--input',str(source),'--output',str(output),'--overrides',str(overrides),'--language-corrections',str(corrections)])
            self.assertEqual((output/'english.jsonl').read_text(encoding='utf-8'),'')
            corrected=json.loads((output/'chinese.jsonl').read_text(encoding='utf-8'))
            self.assertEqual(corrected['language'],'zh')
            self.assertEqual(corrected['coarse_screening']['language_correction']['original_label'],'en')
            self.assertEqual(corrected['text_original'],original['text_original'])
            self.assertEqual((source/'records.jsonl').read_text(encoding='utf-8'),raw)

    def test_conflicting_overlapping_copies_fail_loudly(self):
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)
            (p/'records.jsonl').write_text(json.dumps(row('original'))+'\n', encoding='utf-8')
            (p/'english.jsonl').write_text(json.dumps(row('edited'))+'\n', encoding='utf-8')
            with self.assertRaises(ValueError):
                screening.load_sources(p)



class CoarseV2PatternTests(unittest.TestCase):
    """Screening coarse-v2 (pipeline upgrade U6.4, LNK-03, UP-D13): patterns generated from the glossary."""

    def test_version_and_terms_file(self):
        self.assertEqual(screening.VERSION, 'coarse-v2')
        terms = json.loads(screening.TERMS_PATH.read_text(encoding='utf-8'))
        for key in ('char_zh', 'mechanic', 'excluded_glossary_entries', 'excluded_glossary_terms'):
            self.assertTrue(terms[key], key)
            self.assertTrue(all(isinstance(t.get('reason'), str) and t['reason'] for t in terms[key]), key)
        self.assertTrue(all(t['kind'] in ('latin_word', 'cjk') for t in terms['mechanic']))

    def test_character_pattern_reads_the_glossary(self):
        from aimediator.resources import glossary
        entries = [e for e in glossary()['entries'] if e['category'] == 'character']
        for entry in entries:
            if not any('a' <= c.lower() <= 'z' for c in entry['chinese_label']):  # JP's label is Latin: _char_en
                self.assertTrue(screening._char_zh().search(entry['chinese_label']), entry['id'])
        # A supplemental traditional-script name still matches.
        self.assertTrue(screening._char_zh().search('傑米太強了'))

    def test_mechanic_pattern_reads_the_glossary_with_reviewed_exclusions(self):
        mech = screening._mech()
        for text in ('Drive Parry', 'drive-parry', 'perfect parry', '完美招架', 'Punish Counter', 'damage scaling',
                     'perfect parries', '白血'):
            self.assertTrue(mech.search(text), text)
        for text in ('I play on PC', 'Modern controls', 'classic', '启动游戏', '发生了什么', 'Drive Impactful'):
            self.assertFalse(mech.search(text), text)

    def test_glossary_mechanic_with_a_claim_is_kept(self):
        self.assertEqual(screening.classify(row('Drive Parry is too strong and unfair.'))[0], 'keep')
        self.assertEqual(screening.classify(row('Drive Parry'))[0], 'review')

if __name__=='__main__':
    unittest.main()
