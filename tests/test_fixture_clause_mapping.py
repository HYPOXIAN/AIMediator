"""Every fixture annotation maps onto clause segments (plan 4.2, step U4.2).

A case maps when every v1 segment is a union of whole clause segments; the
derived labels are the v1 segment's labels, and the points keep their
segment sets. FixtureTransport derives its v2 answers from this mapping.
"""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from aimediator.common import read
from aimediator.evidence import clause_segments, evidence_units
from aimediator.resources import asset_path

LABELS = ('scope', 'content_kind', 'emotional_tone', 'reason_code')


def covering_clauses(segment, clauses, text):
    """Return the clause IDs that make up a v1 segment, or None when a clause crosses its edges or text is left over."""
    inside = [c for c in clauses if segment['start'] <= c['start'] and c['end'] <= segment['end']]
    crossing = [c for c in clauses if c['start'] < segment['end'] and segment['start'] < c['end'] and c not in inside]
    covered = {i for c in inside for i in range(c['start'], c['end'])}
    needed = {i for i in range(segment['start'], segment['end']) if not text[i].isspace()}
    if crossing or not inside or not needed <= covered:
        return None
    return [c['segment_id'] for c in inside]


class FixtureClauseMapping(unittest.TestCase):
    def test_all_fixture_cases_map_onto_clause_segments(self):
        cases = read(asset_path('fixtures/cases.json'))
        self.assertEqual(len(cases), 38)
        unmapped, clause_total = [], 0
        for case in cases:
            text = case['source']['text_original']
            clauses = clause_segments(evidence_units(text))
            clause_total += len(clauses)
            annotation = case['annotation']
            members = {s['segment_id']: covering_clauses(s, clauses, text) for s in annotation['segments']}
            if any(ids is None for ids in members.values()):
                unmapped.append(case['case_id'])
                continue
            # Every clause belongs to exactly one v1 segment and takes its labels.
            owners = [sid for sid, ids in members.items() for _ in ids]
            self.assertEqual(sorted(i for ids in members.values() for i in ids),
                             sorted(c['segment_id'] for c in clauses), case['case_id'])
            self.assertEqual(len(owners), len(clauses), case['case_id'])
            labels = {cid: {k: s[k] for k in LABELS} for s in annotation['segments'] for cid in members[s['segment_id']]}
            self.assertEqual(list(labels), [c['segment_id'] for c in clauses], case['case_id'])
            for point in annotation['information_points']:
                derived = [cid for sid in point['segment_ids'] for cid in members[sid]]
                self.assertEqual(len(derived), len(set(derived)), case['case_id'])
                self.assertTrue(derived)
                self.assertEqual({s for s in members if set(members[s]) & set(derived)}, set(point['segment_ids']))
        self.assertEqual(unmapped, [])
        self.assertEqual(sum(len(c['annotation']['segments']) for c in cases), 124)
        self.assertGreaterEqual(clause_total, 124)

    def test_a_crossing_clause_does_not_map(self):
        text = 'Ryu is strong, nerf him'
        clauses = clause_segments(evidence_units(text))
        self.assertEqual(covering_clauses({'start': 0, 'end': 23}, clauses, text), ['E1.1', 'E1.2'])
        self.assertIsNone(covering_clauses({'start': 0, 'end': 6}, clauses, text))
        self.assertIsNone(covering_clauses({'start': 0, 'end': 23}, clauses[:1], text))


if __name__ == '__main__':
    unittest.main()
