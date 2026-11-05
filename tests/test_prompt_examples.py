"""Authored synthetic examples of the extraction prompts (plan 4.3, step U5.3, UP-D11).

Each example is one line of input units (`<n>. E1 "..." E2 "..."`) and one line with the expected entry of
`assessments` (`=> {...}`). The expected entry must be valid under the response schema that the pipeline builds
for the example's own text, every claim must name a declared subject, and each example stays under 400 characters.
"""
import json
from pathlib import Path
import re
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from aimediator import evidence, stages
from aimediator.resources import asset_path
from aimediator.schema import schema_errors

MARKERS = {'en': 'Synthetic examples, authored for this prompt (not real comments).',
           'zh': '合成示例（为本提示编写，并非真实评论）。'}


def examples(language):
    text = asset_path('prompts/summarize-balance.%s.txt' % language).read_text(encoding='utf-8')
    head, marker, tail = text.partition(MARKERS[language])
    assert marker, language
    lines = tail.splitlines()[1:]
    result = []
    for units_line, answer_line in zip(lines[0::2], lines[1::2]):
        match = re.match(r'(\d+)\. (E1 ".*")$', units_line)
        assert match and answer_line.startswith('=> '), (units_line, answer_line)
        units = re.findall(r'(E\d+) "(.*?)"(?= E\d+ "|$)', match.group(2))
        result.append((units_line + '\n' + answer_line, units, json.loads(answer_line[3:])))
    return head, result


class PromptExampleTests(unittest.TestCase):
    def test_examples_are_marked_last_and_sized(self):
        counts = {}
        for language in ('en', 'zh'):
            head, items = examples(language)
            counts[language] = len(items)
            self.assertNotIn('=> {', head)
            for block, _units, _answer in items:
                self.assertLess(len(block), 400, block)
        self.assertEqual(counts, {'en': 3, 'zh': 5})

    def test_expected_entries_are_valid_for_their_own_text(self):
        kinds = []
        for language, joiner in (('en', ' '), ('zh', '')):
            for _block, units, answer in examples(language)[1]:
                text = joiner.join(t for _i, t in units)
                built = evidence.evidence_units(text)
                self.assertEqual([(u['evidence_id'], u['text']) for u in built], units)
                data = {'comments': [{'comment_id': 'example', 'units': built}],
                        'character_normalization_reference': evidence.character_reference(text)}
                schema = stages.schema_for('extract', ['example'], data)
                self.assertEqual(schema_errors({'assessments': {'example': answer}}, schema), [], text)
                self.assertLessEqual({c['character'] for c in answer['claims']}, set(answer['subjects']))
                kinds.append((language, tuple(c['direction'] for c in answer['claims']),
                              tuple(c['uncertain'] for c in answer['claims'])))
        # Empty answers (a review that only mentions fighters, a system complaint next to a name), a conditional
        # threat (nerf), and in Chinese an unclear, uncertain position and a general complaint (qualitative nerf).
        self.assertEqual(kinds, [('en', (), ()), ('en', ('nerf',), (False,)), ('en', (), ()),
                                 ('zh', (), ()), ('zh', ('nerf',), (False,)), ('zh', (), ()),
                                 ('zh', ('unclear',), (True,)), ('zh', ('nerf',), (False,))])


if __name__ == '__main__':
    unittest.main()
