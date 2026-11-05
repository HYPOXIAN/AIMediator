"""Clause segmentation of evidence units (plan 4.2, step U4.1, ALG-01)."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from aimediator.common import read
from aimediator.evidence import SEGMENTATION_VERSION, clause_segments, evidence_units
from aimediator.resources import asset_path
from behavior_lock import screening_texts


def texts(original):
    return [s['text'] for s in clause_segments(evidence_units(original))]


class ClauseSegments(unittest.TestCase):
    def assert_partition(self, original):
        units = evidence_units(original)
        segments = clause_segments(units)
        by_unit = {u['evidence_id']: u for u in units}
        previous_end, covered = 0, set()
        for unit in units:
            ids = [s['segment_id'] for s in segments if s['evidence_id'] == unit['evidence_id']]
            self.assertEqual(ids, ['%s.%d' % (unit['evidence_id'], k + 1) for k in range(len(ids))])
            self.assertTrue(ids or not unit['text'].strip())
        for segment in segments:
            unit = by_unit[segment['evidence_id']]
            self.assertEqual(set(segment), {'segment_id', 'evidence_id', 'text', 'start', 'end'})
            self.assertTrue(unit['start'] <= segment['start'] < segment['end'] <= unit['end'])
            self.assertGreaterEqual(segment['start'], previous_end)
            self.assertEqual(segment['text'], original[segment['start']:segment['end']])
            self.assertEqual(segment['text'], segment['text'].strip())
            previous_end = segment['end']
            covered.update(range(segment['start'], segment['end']))
        expected = {i for u in units for i in range(u['start'], u['end']) if not original[i].isspace()}
        self.assertEqual(expected - covered, set())
        return segments

    def test_every_tracked_text_is_partitioned(self):
        corpus = screening_texts() + [c['source']['text_original'] for c in read(asset_path('fixtures/cases.json'))]
        self.assertEqual(len(corpus), 388)
        for original in corpus:
            with self.subTest(original=original[:40]):
                self.assert_partition(original)

    def test_split_points(self):
        self.assertEqual(SEGMENTATION_VERSION, 'clause-v1')
        self.assertEqual(texts('Ryu is strong, but slow; fix: it'), ['Ryu is strong,', 'but slow;', 'fix:', 'it'])
        self.assertEqual(texts('隆太强了，削弱一下；伤害：太高、太快'), ['隆太强了，', '削弱一下；', '伤害：', '太高、', '太快'])
        self.assertEqual(texts('no split point here'), ['no split point here'])
        self.assertEqual(texts('a,,, b'), ['a,,,', 'b'])
        self.assertEqual(texts(',start'), [',', 'start'])

    def test_digits_numbers_and_move_notation(self):
        self.assertEqual(texts('damage 1,000 to 1.5x'), ['damage 1,000 to 1.5x'])
        self.assertEqual(texts('at 1:30, 2MP is +2 on block'), ['at 1:30,', '2MP is +2 on block'])
        self.assertEqual(texts('frames 5, 6 and 7'), ['frames 5,', '6 and 7'])
        self.assertEqual(texts('５，０００点'), ['５，０００点'])
        self.assertEqual(texts('2MP,2HP'), ['2MP,', '2HP'])

    def test_scripts_emoji_marks_and_line_endings(self):
        original = 'Ken 太强了，nerf him 👍🏽, café; done'
        self.assertEqual(texts(original), ['Ken 太强了，', 'nerf him 👍🏽,', 'café;', 'done'])
        self.assertEqual(texts('a,́b'), ['a,́', 'b'])
        segments = self.assert_partition('first line, here\r\nsecond, line\r\n')
        self.assertEqual([(s['segment_id'], s['text']) for s in segments],
                         [('E1.1', 'first line,'), ('E1.2', 'here'), ('E2.1', 'second,'), ('E2.2', 'line')])
        self.assertEqual(segments[2]['start'], len('first line, here\r\n'))
        self.assert_partition(original)

    def test_empty_whitespace_and_punctuation_only_units(self):
        self.assertEqual(clause_segments([]), [])
        self.assertEqual(clause_segments(evidence_units('')), [])
        self.assertEqual(clause_segments([{'evidence_id': 'E1', 'text': '', 'start': 0, 'end': 0}]), [])
        self.assertEqual(clause_segments([{'evidence_id': 'E1', 'text': ' , ', 'start': 3, 'end': 6}]),
                         [{'segment_id': 'E1.1', 'evidence_id': 'E1', 'text': ',', 'start': 4, 'end': 5}])
        self.assertEqual(texts('，，，'), ['，，，'])
        self.assertEqual(texts('!!!'), ['!!!'])


if __name__ == '__main__':
    unittest.main()
