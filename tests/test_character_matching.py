"""Character matching keeps its results with cached patterns and a memoized reference (plan step U1.2).

The functions below are copies of ``balance_policy.term_matches`` and
``attributed_candidates`` and of ``evidence.character_reference`` and
``character_candidates`` as they were before U1.2 (commit ``678307e``).
"""
import copy
from pathlib import Path
import re
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from aimediator import balance_policy, evidence
from aimediator.balance_policy import identity_alias_allowed, load_policy
from aimediator.common import read
from aimediator.resources import asset_path, glossary
from behavior_lock import screening_texts


def old_term_matches(term, text):
    if not term:
        return False
    if re.search('[A-Za-z]', term):
        return re.search(r'(?<![A-Za-z])' + re.escape(term) + r'(?![A-Za-z])', text, re.I) is not None
    return term in text


def old_character_reference(text=''):
    reference = [{'canonical_name': e['canonical_name'], 'chinese_label': e.get('chinese_label'),
             'aliases': [{k: a[k] for k in ('text', 'candidate_only', 'requires_context', 'context_note') if k in a}
                         for a in e['aliases'] if old_term_matches(a['text'], text) and identity_alias_allowed(a['text'])]}
            for e in glossary()['entries'] if e['category'] == 'character']
    reference.extend(copy.deepcopy(load_policy()['source_literal_characters']))
    return reference


def old_character_candidates(text, reference):
    return [entry['canonical_name'] for entry in reference
            if any(old_term_matches(term, text) for term in evidence.character_terms(entry))]


def old_attributed_candidates(text, reference, candidates):
    terms = {e['canonical_name']: list(dict.fromkeys(t for t in
             [e['canonical_name'], e.get('chinese_label')] + [a['text'] for a in e['aliases']]
             if t and old_term_matches(t, text))) for e in reference if e['canonical_name'] in candidates}
    units = re.split(r'\r?\n+|[。!?！？]+|\.(?=\s|$)', text)
    cosmetic = r'\b(?:cute|costumes?|outfits?|looks?|skins?|roster|lineup|where.?s|poster|teeth|white.washed)\b|外观|衣服|服装|皮肤|好看|可爱|阵容|客串|联动'
    strength = r'\b(?:buff|nerf|weak|strong|overpowered|underpowered|broken|unbalanced|damage|frames?|startup|recovery)\b|加强|削弱|太强|太弱|强度|伤害|帧|平衡|无敌|赖'
    excluded = {}
    for name, aliases in terms.items():
        mentions = [unit for unit in units if any(old_term_matches(t, unit) for t in aliases)]
        if mentions and all(re.search(cosmetic, unit, re.I) and not re.search(strength, unit, re.I) for unit in mentions):
            excluded[name] = 'explicit_cosmetic_or_roster_only_mentions'
    for actor, actor_terms in terms.items():
        for victim, victim_terms in terms.items():
            if actor == victim:
                continue
            for a in actor_terms:
                for v in victim_terms:
                    relation = re.search(re.escape(a) + r'(?:的)?(?:一招|一拳|一脚|一套)给(?:我)?' + re.escape(v) + r'(?:打|造成)', text)
                    relation = relation or re.search(re.escape(a) + r'\s+(?:hits?|grabs?|damages?)\s+(?:my\s+)?' + re.escape(v) + r'\b', text, re.I)
                    independent = re.search(r'(?:加强|削弱|buff\s+|nerf\s+)' + re.escape(v), text, re.I) or re.search(re.escape(v) + r'.{0,12}(?:太强|太弱|需要加强|需要削弱|too weak|too strong)', text, re.I)
                    if relation and not independent and len(re.findall(re.escape(v), text, re.I)) == 1:
                        excluded[victim] = 'explicit_recipient_not_attack_subject'
    return [name for name in candidates if name not in excluded], excluded


def texts():
    """Every text_original of the tracked evaluation sets and the packaged fixtures, plus '' and one joined text."""
    found = screening_texts() + [c['source']['text_original'] for c in read(asset_path('fixtures/cases.json'))]
    return found + ['', '\n'.join(found[-38:])]


class CharacterMatchingTests(unittest.TestCase):
    def test_new_functions_equal_the_copies_before_u1_2(self):
        values = texts()
        self.assertEqual(len(values), 350 + 38 + 2)
        candidates_seen = 0
        for repeat in range(2):  # the second pass reads the memoized references
            for text in values:
                reference = evidence.character_reference(text)
                expected = old_character_reference(text)
                self.assertEqual(reference, expected, text)
                candidates = evidence.character_candidates(text, reference)
                self.assertEqual(candidates, old_character_candidates(text, expected), text)
                self.assertEqual(balance_policy.attributed_candidates(text, reference, candidates),
                                 old_attributed_candidates(text, expected, candidates), text)
                candidates_seen += len(candidates)
        self.assertGreater(candidates_seen, 200)

    def test_term_matches_equals_the_copy_on_glossary_terms(self):
        terms = [t for e in glossary()['entries'] if e['category'] == 'character'
                 for t in evidence.character_terms(e)] + ['', None, 'C.Viper', 'A.K.I.', 'ryu', '隆']
        samples = ['Ryu and Ken', 'RYU!', 'ryuu', 'c.viper is strong', '隆太强了', 'akira', 'A.K.I. needs buff', '']
        for term in terms:
            for text in samples:
                self.assertEqual(balance_policy.term_matches(term, text), old_term_matches(term, text), (term, text))

    def test_memoized_reference_hands_out_new_objects(self):
        first = evidence.character_reference('Ryu 隆')
        first[0]['aliases'].append({'text': 'mutated'})
        first[-1]['canonical_name'] = 'mutated'
        second = evidence.character_reference('Ryu 隆')
        self.assertEqual(second, old_character_reference('Ryu 隆'))
        self.assertIsNot(first, second)
        self.assertTrue(all(a is not b for a, b in zip(first, second)))


if __name__ == '__main__':
    unittest.main()
