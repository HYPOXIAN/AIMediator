import json
import hashlib
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
import collect_balanced_feedback as b
import run_balance_analysis as m
import numpy as np


def row(i, lang, text, date):
    return {'record_id': str(i), 'language': lang, 'text_original': text,
            'created_at_utc': date, 'platform': 'steam'}


class BalancedCollectionTests(unittest.TestCase):
    def test_no_number_request_cannot_emit_null_only_numeric_parameters(self):
        text = 'Ken hits Ryu too hard. Please nerf Ken.'
        data = {'comments': [{'comment_id': 'one', 'units': m.evidence_units(text)}],
                'character_normalization_reference': m.character_reference(text)}
        c = {'character': 'Ken', 'target': None, 'direction': 'nerf',
             'recommendation': 'Nerf Ken.', 'specificity': 'source_numeric',
             'parameters': [{'metric': 'damage', 'current': None, 'proposed': None,
                 'delta': None, 'unit': None, 'evidence_id': 'E1'}],
             'evidence_ids': ['E1', 'E2'], 'uncertain': False}
        schema = m.schema_for('extract', ['one'], data)
        self.assertTrue(m.schema_errors({'assessments': {'one': {'claims': [c]}}}, schema))
        c.update(specificity='qualitative_only', parameters=[])
        self.assertFalse(m.schema_errors({'assessments': {'one': {'claims': [c]}}}, schema))

    def test_explicit_numeric_target_remains_available(self):
        text = "Please reduce Ryu's Hadoken damage from 600 to 500."
        data = {'comments': [{'comment_id': 'one', 'units': m.evidence_units(text)}],
                'character_normalization_reference': m.character_reference(text)}
        c = {'character': 'Ryu', 'target': 'Hadoken damage', 'direction': 'nerf',
             'recommendation': 'Reduce Hadoken damage from 600 to 500.',
             'specificity': 'source_numeric', 'parameters': [{'metric': 'damage',
                 'current': '600', 'proposed': '500', 'delta': None, 'unit': None,
                 'evidence_id': 'E1'}], 'evidence_ids': ['E1'], 'uncertain': False}
        self.assertFalse(m.schema_errors({'assessments': {'one': {'claims': [c]}}},
            m.schema_for('extract', ['one'], data)))

    def test_newest_unique_relevant_rows_fill_equal_quotas(self):
        rows = [row(1, 'en', 'Nerf Ryu.', '2026-10-01'),
                row(2, 'en', 'Nerf Ryu.', '2026-10-27'),
                row(3, 'en', 'Great video!', '2026-10-28'),
                row(4, 'zh', '请削弱肯', '2026-10-26'),
                row(5, 'en', 'Buff Manon.', '2026-10-25')]
        selected, counts = b.select_balanced(rows, 1)
        self.assertEqual(dict(counts), {'en': 1, 'zh': 1})
        self.assertEqual({r['record_id'] for r in selected}, {'2', '4'})
        self.assertEqual(rows[1]['text_original'], selected[0]['text_original'])

    def test_shortage_is_visible_and_not_padded_with_irrelevance(self):
        selected, counts = b.select_balanced([row(1, 'en', 'Great video!', '2026-10-27')], 300)
        self.assertEqual(selected, [])
        self.assertEqual(counts['zh'], 0)

    def test_language_reviews_preserve_original_and_reject_stale_text(self):
        original = row(1, 'en', '加强曼侬', '2026-10-27')
        review = {'1': {'language': 'zh', 'text_sha256': hashlib.sha256(original['text_original'].encode()).hexdigest()}}
        selected, counts = b.select_balanced([original], 1, review)
        self.assertEqual(counts['zh'], 1)
        self.assertEqual(original['language'], 'en')
        original['text_original'] = 'changed'
        with self.assertRaises(ValueError):
            b.select_balanced([original], 1, review)

    def test_configured_embedding_never_calls_ollama_and_saves_no_key(self):
        cfg = {'url': 'https://embedding.test/v1/embeddings', 'model': 'fixture', 'key': 'SECRET'}
        rows = [row(1, 'en', 'Nerf Ryu.', '2026-10-27')]
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            with patch.object(m.glossary_vectors, 'embed', side_effect=lambda c,t: (np.ones((len(t), 4)), {})) as embed, patch.object(m, 'api') as api:
                result = m.retrieve(rows, '', folder, 'fixture', cfg)
            self.assertEqual(len(result), 1)
            self.assertEqual(embed.call_count, 3)
            api.assert_not_called()
            for f in folder.rglob('*.json'):
                self.assertNotIn('SECRET', f.read_text())

    def test_runtime_options_are_recorded_in_actual_request(self):
        with tempfile.TemporaryDirectory() as temp:
            runner = m.Runner('http://test', Path(temp), {'relevance': {'en': 'test'}})
            runner.runtime_options = {'num_gpu': 0}
            result = {'done': True, 'done_reason': 'stop', 'message': {'content': '{"decisions":["related"]}'}}
            with patch.object(m, 'streamed_chat', return_value=result):
                parsed, meta = runner.generate('fixture', 'en', 'relevance', {'comments': []}, ['one'])
            self.assertFalse(meta['errors'])
            request = json.loads(next(Path(temp).rglob('request.json')).read_text())
            self.assertEqual(request['options']['num_gpu'], 0)


if __name__ == '__main__':
    unittest.main()
