"""Recovery may reuse key-order variants, never changed model inputs or failed output."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import run_balance_analysis as m
import resume_quality_screening_local as recovery


class RecoveryTests(unittest.TestCase):
    def check_cache(self, change=None, reuse=True):
        with tempfile.TemporaryDirectory() as temp:
            runner = m.Runner('unused', Path(temp), {'quality': {'en': 'rules'}}, {}, {'num_ctx': 16384, 'num_predict': 8192})
            data = {'source': {'record_id': 'test', 'text_original': 'Original'}, 'attempt': 1}
            schema = m.schema_for('quality', ['test'], data)
            user = {'attempt': 1, 'source': {'text_original': 'Original', 'record_id': 'test'}, 'response_schema': schema}
            payload = {'model': 'local', 'options': {'seed': 42, 'temperature': 0, 'num_predict': 8192, 'num_ctx': 16384},
                       'messages': [{'role': 'system', 'content': 'rules'}, {'role': 'user', 'content': json.dumps(user)}], 'format': schema}
            validation = {'errors': []}
            if change == 'text':
                user['source']['text_original'] = 'Changed'; payload['messages'][1]['content'] = json.dumps(user)
            if change == 'options': payload['options']['num_ctx'] = 8192
            if change == 'failed': validation['errors'] = ['Incomplete generation']
            cached = Path(temp) / 'requests/quality/cached'
            m.write_json(cached / 'request.json', payload)
            m.write_json(cached / 'response.json', {'response': {'done': True, 'done_reason': 'stop'}})
            m.write_json(cached / 'validation.json', validation)
            with patch.object(recovery, 'original_generate', return_value=({}, {'request_id': 'cached' if reuse else 'new'})) as generate:
                parsed, meta = recovery.generate(runner, 'local', 'en', 'quality', data, ['test'])
                supplied = generate.call_args.args[4]
                self.assertEqual(supplied, data)
                self.assertEqual(meta.get('recovered_by') is not None, reuse)
                self.assertEqual(list(supplied), ['attempt', 'source'] if reuse else ['source', 'attempt'])

    def test_effective_request_preserves_all_values(self):
        with tempfile.TemporaryDirectory() as temp:
            payload = {'options': {'num_ctx': 16384}, 'messages': [
                {'role': 'system', 'content': 'rules'},
                {'role': 'user', 'content': json.dumps({'source': {'text': '原文'}, 'language': 'zh', 'quality_contract': {'a': 1}})}]}
            before = copy.deepcopy(payload)
            with patch.object(recovery, 'original_stream', return_value={'done': True}) as streamed:
                recovery.stream('unused', payload, Path(temp) / 'partial-output.txt')
            effective = streamed.call_args.args[1]
            self.assertEqual(payload, before)
            self.assertEqual(json.loads(effective['messages'][1]['content']), json.loads(payload['messages'][1]['content']))
            self.assertEqual(next(iter(json.loads(effective['messages'][1]['content']))), 'quality_contract')
            self.assertEqual(effective['options'], {'num_ctx': 16384, 'num_gpu': 0})

    def test_reordered_identical_json_is_reused(self): self.check_cache()
    def test_changed_source_cannot_be_reused(self): self.check_cache('text', False)
    def test_changed_context_cannot_be_reused(self): self.check_cache('options', False)
    def test_failed_validation_cannot_be_reused(self): self.check_cache('failed', False)


if __name__ == '__main__': unittest.main()
