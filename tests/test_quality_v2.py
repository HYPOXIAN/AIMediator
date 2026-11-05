"""Evidence-quality-v2 schema, validation and conversion to v1 (plan 4.2, step U4.3, ALG-01, ALG-02)."""
import copy
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from aimediator import evidence_quality as quality
from aimediator.common import read
from aimediator.evidence import clause_segments, evidence_units
from aimediator.fixture_transport import v2_annotation
from aimediator.resources import asset_path

LABEL = ('{"type": "object", "properties": {"scope": {"type": "string", "enum": ["character_balance", '
         '"system_balance", "unrelated", "uncertain"]}, "content_kind": {"type": "string", "enum": ["pure_emotion", '
         '"general_opinion", "concrete_feedback", "other", "uncertain"]}, "emotional_tone": {"type": "boolean"}, '
         '"reason_code": {"type": "string", "enum": ["empty_venting", "general_strength", '
         '"concrete_mechanic_condition", "system_feedback", "price_cosmetic_network", "quoted_emotion", '
         '"missing_context", "ambiguous_sarcasm", "unrelated_topic", "concrete_positive", "explicit_request", '
         '"uncertain_attribution"]}}, "required": ["scope", "content_kind", "emotional_tone", "reason_code"], '
         '"additionalProperties": false}')
SCHEMA = ('{"type": "object", "properties": {"comment_id": {"type": "string", "enum": ["c1"]}, '
          '"segment_labels": {"type": "object", "properties": {"E1.1": ' + LABEL + ', "E1.2": ' + LABEL + '}, '
          '"required": ["E1.1", "E1.2"], "additionalProperties": false}, "information_points": {"type": "array", '
          '"items": {"type": "object", "properties": {"point_id": {"type": "string", "minLength": 1}, '
          '"segment_ids": {"type": "array", "items": {"type": "string", "enum": ["E1.1", "E1.2"]}, "minItems": 1, '
          '"uniqueItems": true}, "scope": {"type": "string", "enum": ["character_balance", "system_balance", '
          '"uncertain"]}, "detail_level": {"type": "string", "enum": ["general", "concrete", "uncertain"]}, '
          '"stance": {"type": "string", "enum": ["explicit_request", "strength_assessment", "observation", '
          '"uncertain"]}, "direction": {"type": "string", "enum": ["buff", "nerf", "keep", "unclear"]}, '
          '"character_literal": {"type": ["string", "null"], "enum": [null, "Ken"]}, "mechanic_literal": '
          '{"type": ["string", "null"], "minLength": 1}}, "required": ["point_id", "segment_ids", "scope", '
          '"detail_level", "stance", "direction", "character_literal", "mechanic_literal"], '
          '"additionalProperties": false}}}, "required": ["comment_id", "segment_labels", "information_points"], '
          '"additionalProperties": false}')


def sample():
    row = {'record_id': 'c1', 'language': 'en', 'text_original': 'Ken is strong, his fireball is too fast. Ryu is fine'}
    units = evidence_units(row['text_original'])
    segments = clause_segments(units)
    label = {'scope': 'character_balance', 'content_kind': 'concrete_feedback',
             'emotional_tone': False, 'reason_code': 'concrete_mechanic_condition'}
    annotation = {'comment_id': 'c1', 'segment_labels': {s['segment_id']: dict(label) for s in segments},
                  'information_points': [{'point_id': 'P1', 'segment_ids': ['E1.1', 'E1.2'],
                                          'scope': 'character_balance', 'detail_level': 'concrete',
                                          'stance': 'strength_assessment', 'direction': 'nerf',
                                          'character_literal': 'Ken', 'mechanic_literal': 'fireball'}]}
    return row, units, segments, annotation


class QualityV2(unittest.TestCase):
    def test_schema_property_order_is_pinned(self):
        segments = clause_segments(evidence_units('Ken is strong, nerf'))
        self.assertEqual(json.dumps(quality.annotation_schema_v2('c1', segments, ['Ken'])), SCHEMA)

    def test_character_literals_are_source_text_by_first_occurrence(self):
        self.assertEqual(quality.character_literals('KEN beats Ryu, ken again'), ['KEN', 'Ryu', 'ken'])
        self.assertEqual(quality.character_literals('no fighter here'), [])

    def test_valid_annotation_converts_into_valid_v1(self):
        row, units, segments, annotation = sample()
        self.assertEqual([s['segment_id'] for s in segments], ['E1.1', 'E1.2', 'E2.1'])
        self.assertEqual(quality.validate_annotation_v2(annotation, row, segments, units), [])
        v1 = quality.to_v1_annotation(annotation, segments, row['text_original'])
        self.assertEqual(quality.validate_annotation(v1, row, units), [])
        self.assertEqual([(s['segment_id'], s['quote'], s['start'], s['end']) for s in v1['segments']],
                         [('E1.1', 'Ken is strong,', 0, 14), ('E1.2', 'his fireball is too fast.', 15, 40),
                          ('E2.1', 'Ryu is fine', 41, 52)])
        self.assertEqual(list(v1['segments'][0]), ['segment_id', 'evidence_id', 'start', 'end', 'quote', 'scope',
                                                   'content_kind', 'emotional_tone', 'reason_code'])
        record = quality.qualify(v1, row, units)
        self.assertEqual(record['status'], 'completed')
        self.assertEqual([(r['point_id'], r['route']) for r in record['routing']],
                         [('P1', 'mechanism_evidence'), (None, 'review')])

    def test_structure_errors(self):
        row, units, segments, annotation = sample()
        missing = copy.deepcopy(annotation)
        del missing['segment_labels']['E2.1']
        extra = copy.deepcopy(annotation)
        extra['segment_labels']['E1.1']['quote'] = 'Ken'
        wrong = copy.deepcopy(annotation)
        wrong['segment_labels']['E1.2']['scope'] = 'everything'
        offsets = copy.deepcopy(annotation)
        offsets['segments'] = []
        self.assertEqual(quality.validate_annotation_v2(missing, row, segments, units), ['$.segment_labels: missing keys'])
        self.assertEqual(quality.validate_annotation_v2(extra, row, segments, units),
                         ['$.segment_labels.E1.1: extra keys'])
        self.assertEqual(quality.validate_annotation_v2(wrong, row, segments, units),
                         ['$.segment_labels.E1.2.scope: value outside enum'])
        self.assertEqual(quality.validate_annotation_v2(offsets, row, segments, units), ['$: extra keys'])
        self.assertEqual(quality.validate_annotation_v2({**annotation, 'comment_id': 'c2'}, row, segments, units),
                         ['$.comment_id: value outside enum'])
        duplicate = copy.deepcopy(annotation)
        duplicate['information_points'].append(copy.deepcopy(duplicate['information_points'][0]))
        self.assertEqual(quality.validate_annotation_v2(duplicate, row, segments, units), ['Duplicate point IDs'])

    def test_foreign_segment_ids(self):
        row, units, segments, annotation = sample()
        foreign = copy.deepcopy(annotation)
        foreign['information_points'][0]['segment_ids'] = ['E1.1', 'E9.1']
        self.assertEqual(quality.validate_annotation_v2(foreign, row, segments, units),
                         ['$.information_points[0].segment_ids[1]: value outside enum'])
        foreign['information_points'][0]['segment_ids'] = ['E1.1', 'E1.1']
        self.assertEqual(quality.validate_annotation_v2(foreign, row, segments, units),
                         ['$.information_points[0].segment_ids: duplicate items'])

    def test_literals_outside_the_selected_segments(self):
        row, units, segments, annotation = sample()
        absent = copy.deepcopy(annotation)
        absent['information_points'][0]['segment_ids'] = ['E1.2']
        self.assertEqual(quality.validate_annotation_v2(absent, row, segments, units),
                         ['Literal absent from selected spans: character_literal'])
        absent['information_points'][0].update(segment_ids=['E1.1'], mechanic_literal='uppercut')
        self.assertEqual(quality.validate_annotation_v2(absent, row, segments, units),
                         ['Literal absent from selected spans: mechanic_literal'])
        unknown = copy.deepcopy(annotation)
        unknown['information_points'][0]['character_literal'] = 'Guile'
        self.assertEqual(quality.validate_annotation_v2(unknown, row, segments, units),
                         ['$.information_points[0].character_literal: value outside enum'])

    def test_fixture_round_trip_keeps_the_v1_routing(self):
        # v2 answers derived from the fixtures, converted back and routed by the unchanged qualify.
        for case in read(asset_path('fixtures/cases.json')):
            row = case['source']
            text = row['text_original']
            units = evidence_units(text)
            segments = clause_segments(units)
            with self.subTest(case=case['case_id']):
                v2 = v2_annotation(case['annotation'], text)
                self.assertEqual(quality.schema_errors(v2, quality.annotation_schema_v2(
                    row['record_id'], segments, quality.character_literals(text))), [])
                self.assertEqual(quality.validate_annotation_v2(v2, row, segments, units), [])
                converted = quality.qualify(quality.to_v1_annotation(v2, segments, text), row, units)
                original = quality.qualify(case['annotation'], row, units)
                self.assertEqual(converted['status'], original['status'])
                self.assertEqual(converted['routes_present'], original['routes_present'])
                self.assertEqual(converted['routes_present'], sorted(case['expected_routes']))
                self.assertEqual([(r['point_id'], r['route'], r['reason']) for r in converted['routing'] if r['point_id']],
                                 [(r['point_id'], r['route'], r['reason']) for r in original['routing'] if r['point_id']])
                self.assertEqual({(r['route'], r['reason']) for r in converted['routing'] if not r['point_id']},
                                 {(r['route'], r['reason']) for r in original['routing'] if not r['point_id']})
                for key in ('emotion_weight', 'full_weight', 'emotion_ratio', 'high_emotion_warning',
                            'emotion_only', 'point_counts'):
                    self.assertEqual(converted[key], original[key], key)


if __name__ == '__main__':
    unittest.main()
