"""Content-addressed, resumable journal of model requests and responses."""
import json
import time

from . import evidence_quality as quality
from .common import sha as digest, strict_json, write as write_json
from .evidence import character_candidates, character_reference
from .evidence_quality import schema_errors
from .inference import streamed_chat
from .stages import exact_coverage, schema_for


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
        if stage == 'verify':
            entry = data['claims'][0]
            proposal = entry['claim']
            original = data.get('original_comment') or '\n'.join(u['text'] for u in proposal['evidence'])
            reference = character_reference(original)
            candidates = character_candidates(original, reference)
            # Confidence flags, model names and source URLs are not premises for
            # entailment. Keep the original text separate from the proposal.
            qualification = proposal.get('evidence_quality')
            data = {'original_evidence': original,
                'proposed_claim': {key: proposal[key] for key in ('character', 'target', 'direction', 'recommendation')},
                'naming_reference': [e for e in reference if e['canonical_name'] in candidates],
                'claim_id': ids[0]}
            data['proposed_claim']['parameters'] = [
                {key: parameter[key] for key in ('metric', 'current', 'proposed', 'delta', 'unit')}
                for parameter in proposal['parameters']]
            if qualification:
                # Show source spans and original annotation semantics, never a
                # passed-quality flag, emotion ratio or model confidence.
                data['selected_source_segments'] = [{k: s[k] for k in
                    ('evidence_id', 'start', 'end', 'quote')} for s in qualification['selected_segments']]
                data['selected_source_points'] = [{k: p[k] for k in
                    ('point_id', 'segment_ids', 'character_literal', 'mechanic_literal', 'stance', 'direction')}
                    for p in qualification['selected_points']]
        schema = schema_for(stage, ids, data)
        payload = {'model': model, 'messages': [
            {'role': 'system', 'content': self.prompts[stage][language]},
            {'role': 'user', 'content': json.dumps({**data, 'response_schema': schema}, ensure_ascii=False)}],
            'format': schema, 'stream': True, 'keep_alive': '10m',
            'options': {'temperature': 0, 'seed': 42, 'num_ctx': 8192,
                        'num_predict': 4096 if stage == 'extract' else 256}}
        if stage == 'quality':
            policy = self.quality_policy or quality.load_policy()
            payload['options'].update(num_predict=policy['num_predict'], num_ctx=policy['num_ctx'])
        payload['options'].update(self.runtime_options)
        cache_payload = {**payload, 'stream': False}
        if self.quality_identity is not None:
            cache_payload['pipeline_quality_identity'] = self.quality_identity
        # Streaming is a transport choice; preserve existing semantic-request
        # cache identities from non-streaming runs.
        identity = digest(json.dumps(cache_payload, sort_keys=True, ensure_ascii=False).encode())
        folder = self.folder / 'requests' / stage / identity
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
                if stage in ('relevance', 'retrieval_review'):
                    parsed = {'decisions': [{'comment_id': identity, 'related': status == 'related',
                        'uncertain': status == 'uncertain', 'reason': 'Ordered model status: ' + status}
                        for identity, status in zip(ids, parsed['decisions'])]}
                elif stage == 'quality':
                    errors.extend(quality.validate_annotation(parsed, data['source'], data['comments'][0]['units']))
                elif stage == 'verify':
                    status = parsed['support']
                    parsed = {'verdicts': [{'claim_id': ids[0], 'supported': status == 'supported',
                        'support_status': status, 'scope': 'selected_quality_segments_with_original_context' if data.get('selected_source_segments') else 'full_original_comment',
                        'reason': 'Model source-support status: ' + status}]}
                else:
                    parsed = {'assessments': [{'comment_id': identity, **assessment,
                        'disposition': 'extracted' if assessment['claims'] else 'no_supported_character_claim'}
                        for identity, assessment in parsed['assessments'].items()]}
                    if not exact_coverage(parsed['assessments'], 'comment_id', ids):
                        errors.append('Missing or duplicated item IDs')
        except (ValueError, KeyError, TypeError) as exc:
            errors.append(str(exc))
        if result.get('error'):
            errors.append(result['error'])
        if result.get('done') is not True or result.get('done_reason') != 'stop':
            errors.append('Incomplete generation')
        write_json(folder / 'validation.json', {'errors': errors, 'schema': schema})
        return parsed if not errors else None, {'request_id': identity, 'errors': errors,
            'elapsed_seconds': response.get('elapsed_seconds', 0)}
