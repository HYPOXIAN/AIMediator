"""Content-addressed, resumable journal of model requests and responses."""
import json
import time

from .common import sha as digest, strict_json, write as write_json
from .evidence_quality import schema_errors
from .inference import streamed_chat
from .stages import normalize, options, prepare, schema_for


class Runner:
    def __init__(self, base, folder, prompts, quality_identity=None, quality_policy=None, chat_transport=None, progress=None):
        self.base, self.folder, self.prompts = base, folder, prompts
        self.quality_identity = quality_identity
        self.quality_policy = quality_policy
        self.runtime_options = {}
        self.progress = progress
        self.chat_transport = chat_transport

    def cached_single_ids(self, model, language, stage):
        identities = set()
        for path in (self.folder / 'requests' / stage).glob('*/response.json'):
            request = json.loads((path.parent / 'request.json').read_text(encoding='utf-8'))
            validation = path.parent / 'validation.json'
            if request['model'] != model or request['messages'][0]['content'] != self.prompts[stage][language]:
                continue
            if not validation.exists() or json.loads(validation.read_text(encoding='utf-8'))['errors']:
                continue
            comments = json.loads(request['messages'][1]['content']).get('comments', [])
            if len(comments) == 1:
                identities.add(comments[0]['comment_id'])
        return identities

    def generate(self, model, language, stage, data, ids):
        if self.progress is not None:
            self.progress(stage, ids, None)
        parsed, metadata = self._generate(model, language, stage, data, ids)
        if self.progress is not None:
            self.progress(stage, ids, bool(parsed))
        return parsed, metadata

    def _generate(self, model, language, stage, data, ids):
        data = prepare(stage, data, ids)
        schema = schema_for(stage, ids, data)
        payload = {'model': model, 'messages': [
            {'role': 'system', 'content': self.prompts[stage][language]},
            {'role': 'user', 'content': json.dumps({**data, 'response_schema': schema}, ensure_ascii=False)}],
            'format': schema, 'stream': True, 'keep_alive': '10m',
            'options': options(stage, self.quality_policy)}
        payload['options'].update(self.runtime_options)
        cache_payload = {**payload, 'stream': False}
        if self.quality_identity is not None:
            cache_payload['pipeline_quality_identity'] = self.quality_identity
        # Streaming is a transport choice; preserve existing semantic-request
        # cache identities from non-streaming runs.
        identity = digest(json.dumps(cache_payload, sort_keys=True, ensure_ascii=False).encode())
        folder = self.folder / 'requests' / stage / identity
        response = self._response(model, stage, ids, folder, payload)
        if stage == 'quality' and (not isinstance(response, dict) or
                not isinstance(response.get('response'), dict)):
            response = {'elapsed_seconds': 0, 'response': {'done': False,
                'done_reason': 'invalid_response', 'message': {'content': ''}, 'error': 'Malformed response envelope'}}
        result = response['response']
        if stage == 'quality' and not isinstance(result.get('message'), dict):
            result = {**result, 'message': {'content': ''}, 'error': 'Malformed message envelope'}
        errors, parsed = [], None
        try:
            parsed = strict_json(result['message']['content'])
            errors = schema_errors(parsed, schema)
            if not errors:
                parsed, errors = normalize(stage, parsed, ids, data)
        except (ValueError, KeyError, TypeError) as exc:
            errors.append(str(exc))
        if result.get('error'):
            errors.append(result['error'])
        if result.get('done') is not True or result.get('done_reason') != 'stop':
            errors.append('Incomplete generation')
        write_json(folder / 'validation.json', {'errors': errors, 'schema': schema})
        return parsed if not errors else None, {'request_id': identity, 'errors': errors,
            'elapsed_seconds': response.get('elapsed_seconds', 0)}

    def _response(self, model, stage, ids, folder, payload):
        """Return the journaled response of a request, calling the transport only when none is saved."""
        request_path = folder / 'request.json'
        response_path = folder / 'response.json'
        if response_path.exists():
            try:
                response = json.loads(response_path.read_text(encoding='utf-8'))
            except (ValueError, OSError) as exc:
                if stage != 'quality':
                    raise
                response = {'elapsed_seconds': 0, 'response': {'done': False,
                    'done_reason': 'invalid_cache', 'message': {'content': ''},
                    'error': 'Unreadable cached response: ' + str(exc)}}
        else:
            write_json(request_path, payload)
            print(f'{stage}: {model}, {len(ids)} items', flush=True)
            start = time.monotonic()
            if stage == 'quality' and (folder / 'partial-output.txt').exists():
                partial = folder / 'partial-output.txt'
                index = 1
                while (folder / f'interrupted-partial-{index}.txt').exists():
                    index += 1
                partial.rename(folder / f'interrupted-partial-{index}.txt')
            try:
                result = (self.chat_transport or streamed_chat)(self.base, payload, folder / 'partial-output.txt')
            except (OSError, ValueError) as exc:
                if stage != 'quality':
                    raise
                # A failed transport is a durable attempt, not a missing comment.
                result = {'done': False, 'done_reason': 'transport_error',
                          'message': {'content': ''}, 'error': type(exc).__name__ + ': ' + str(exc)}
            response = {'elapsed_seconds': time.monotonic() - start, 'response': result}
            write_json(response_path, response)
        return response
