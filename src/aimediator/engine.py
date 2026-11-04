"""Full-corpus retrieval, relevance agreement, bilingual extraction and source audit.

Dependencies: Python 3.9+, numpy, local Ollama. All requests and raw responses are
content-addressed and resumable; model-written quotes are never trusted.
"""
import argparse
import copy
from collections import Counter, defaultdict
from datetime import datetime, timezone
from functools import partial
import json
from pathlib import Path
import re
import time
import urllib.request

import numpy as np
from . import evidence_quality as quality
from . import glossary_vectors
from .common import sha as digest, strict_json, write as write_json
from .resources import anchors
POS, NEG = anchors()
from .balance_policy import (POLICY_PATH, load_policy, term_matches, identity_alias_allowed,
                            numeric_request_supported, triage_retrieval, retrieval_review_agrees,
                            direction_action_conflicts, attributed_candidates)

from .resources import asset_path, glossary, module_path
from .schema import BOOL, NULL_STRING, STRING, arr, obj
from .evidence import (CLAIM, PARAMETER, character_candidates, character_reference, evidence_units,
                       ground_claim, numeric_tokens)
ROOT = Path.cwd()
VERSION = 'balance-evidence-v2'


def api(base, endpoint, payload=None):
    data = None if payload is None else json.dumps(payload, ensure_ascii=False).encode()
    request = urllib.request.Request(base + endpoint, data=data,
                                     headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(request, timeout=1800) as response:
        return json.load(response)


def repeated_claim(output, allowed_ids):
    scopes = [(match.start(), match.group(1)) for match in
              re.finditer(r'(?<!\\)"([^"]+)"\s*:', output) if match.group(1) in allowed_ids]
    seen = set()
    decoder = json.JSONDecoder()
    for match in re.finditer(r'\{\s*"character"\s*:', output):
        try:
            claim, _ = decoder.raw_decode(output, match.start())
        except ValueError:
            continue
        parents = [identity for position, identity in scopes if position < match.start()]
        if not parents:
            continue
        signature = (parents[-1], json.dumps(claim, sort_keys=True, ensure_ascii=False))
        if signature in seen:
            return True
        seen.add(signature)
    return False


def streamed_chat(base, payload, partial_path, timeout=1800):
    request = urllib.request.Request(base + '/api/chat',
        data=json.dumps(payload, ensure_ascii=False).encode(), headers={'Content-Type': 'application/json'})
    parts, last, whitespace = [], {}, 0
    with partial_path.open('w', encoding='utf-8') as log, urllib.request.urlopen(request, timeout=timeout) as response:
        for line in response:
            if not line.strip():
                continue
            chunk = json.loads(line)
            fragment = chunk.get('message', {}).get('content', '')
            parts.append(fragment)
            log.write(fragment)
            log.flush()
            whitespace = whitespace + len(fragment) if fragment and fragment.isspace() else 0
            last = chunk
            if whitespace > 256:
                last = {**chunk, 'done': False, 'done_reason': 'whitespace_loop'}
                break
            if 'assessments' in payload['format']['properties']:
                assessment_schema = payload['format']['properties']['assessments']
                if assessment_schema.get('type') == 'object':
                    allowed = set(assessment_schema['properties'])
                    identities = [key for key in re.findall(r'(?<!\\)"([^"]+)"\s*:', ''.join(parts)) if key in allowed]
                else:
                    identities = re.findall(r'(?<!\\)"comment_id"\s*:\s*"([^"]+)"', ''.join(parts))
                if len(identities) != len(set(identities)):
                    last = {**chunk, 'done': False, 'done_reason': 'duplicate_comment_loop'}
                    break
                if assessment_schema.get('type') == 'object' and repeated_claim(''.join(parts), allowed):
                    last = {**chunk, 'done': False, 'done_reason': 'duplicate_claim_loop'}
                    break
            if chunk.get('done'):
                break
    return {**last, 'message': {'role': 'assistant', 'content': ''.join(parts)}}


def schema_for(stage, ids, data=None):
    identity = {'type': 'string', 'enum': ids}
    if stage in ('relevance', 'retrieval_review'):
        return obj({'decisions': {**arr({'enum': ['related', 'unrelated', 'uncertain']}),
                                  'minItems': len(ids), 'maxItems': len(ids)}})
    if stage == 'quality':
        return quality.annotation_schema(ids)
    if stage == 'extract':
        records = {r['comment_id']: r for r in data['comments']} if data else {}
        properties = {}
        for record_id in ids:
            claim = copy.deepcopy(CLAIM)
            claims = arr(claim)
            if data and 'allowed_quality_points' in records[record_id]:
                allowed_points = records[record_id]['allowed_quality_points']
                claim['properties']['quality_point_ids'] = {**arr({'type': 'string',
                    'enum': [r['point_id'] for r in allowed_points]}), 'minItems': 1, 'maxItems': 1}
                claim['required'].append('quality_point_ids')
                if not allowed_points:
                    claims['maxItems'] = 0
            if data:
                text = '\n'.join(u['text'] for u in records[record_id]['units'])
                unit_ids = [u['evidence_id'] for u in records[record_id]['units']]
                parameters = claim['properties']['parameters']['items']['properties']
                numeric_values = list(dict.fromkeys(numeric_tokens(text) + re.findall(r'[一二三四五六七八九十百千万]+', text)))
                deltas = re.findall(r'\bby\s+([+-]?\d+(?:\.\d+)?%?)|(?:加|减|增加|减少|降低|提高)\s*([+-]?\d+(?:\.\d+)?%?|[一二三四五六七八九十百千万]+)', text, re.I)
                delta_values = list(dict.fromkeys(value for pair in deltas for value in pair if value))
                units = list(dict.fromkeys(re.findall(r'(?:\d+(?:\.\d+)?|[一二三四五六七八九十百千万]+)\s*(frames?\b|points?\b|seconds?\b|bars?\b|%|帧|点|秒|格)', text, re.I)))
                for key in ('current', 'proposed'):
                    parameters[key] = {'type': ['string', 'null'], 'enum': [None] + numeric_values}
                parameters['delta'] = {'type': ['string', 'null'], 'enum': [None] + delta_values}
                parameters['unit'] = {'type': ['string', 'null'], 'enum': [None] + units}
                # No legal requested value or delta means no valid numerical
                # parameter can exist; do not let decoding emit null-only ones.
                if not numeric_values and not delta_values:
                    claim['properties']['specificity'] = {'enum': ['qualitative_only']}
                    claim['properties']['parameters']['maxItems'] = 0
                if unit_ids:
                    evidence_property = {'type': 'string', 'enum': unit_ids}
                    claim['properties']['evidence_ids'] = {**arr(evidence_property), 'minItems': 1}
                    claim['properties']['parameters']['items']['properties']['evidence_id'] = evidence_property
                allowed = character_candidates(text, data['character_normalization_reference'])
                allowed, _ = attributed_candidates(text, data['character_normalization_reference'], allowed)
                if allowed:
                    claim['properties']['character'] = {'type': 'string', 'enum': allowed}
                else:
                    claims['maxItems'] = 0
            properties[record_id] = obj({'claims': claims})
        return obj({'assessments': obj(properties)})
    if len(ids) != 1:
        raise ValueError('Semantic audits require exactly one proposal')
    return obj({'support': {'type': 'string', 'enum': ['supported', 'unsupported', 'uncertain']}})


def schema_errors(value, schema, path='$'):
    return quality.schema_errors(value, schema, path)


def exact_coverage(rows, key, expected):
    return Counter(r[key] for r in rows) == Counter(expected)


def relevance_agrees(retrieved, review):
    return retrieval_review_agrees(retrieved, review)


def batches(rows, count=12, chars=18000):
    batch, size = [], 0
    for row in rows:
        length = len(json.dumps(row, ensure_ascii=False))
        if batch and (len(batch) >= count or size + length > chars):
            yield batch
            batch, size = [], 0
        batch.append(row)
        size += length
    if batch:
        yield batch


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


def retrieve(rows, base, folder, model, embedding_config=None, api_transport=None, embed_transport=None):
    instruction = 'Instruct: Retrieve the description matching the topic and intent of this Street Fighter 6 player comment.\nQuery: '
    texts = POS + NEG + [instruction + r['text_original'] for r in rows]
    matrices = []
    for start in range(0, len(texts), 8):
        batch = texts[start:start + 8]
        cache_identity = {'model': model, 'texts': batch}
        if embedding_config:
            cache_identity['endpoint'] = embedding_config['url']
        identity = digest(json.dumps(cache_identity, ensure_ascii=False).encode())
        path = folder / 'embeddings' / (identity + '.json')
        if path.exists():
            record = json.loads(path.read_text(encoding='utf-8'))
        else:
            if embedding_config:
                vectors, usage = (embed_transport or glossary_vectors.embed)(embedding_config, batch)
                result = {'embeddings': vectors.tolist()}
            else:
                result = (api_transport or api)(base, '/api/embed', {'model': model, 'input': batch,
                                               'truncate': False, 'keep_alive': '10m'})
            record = {'model': model, 'texts': batch, 'embeddings': result['embeddings']}
            write_json(path, record)
        matrix = np.asarray(record['embeddings'], dtype=np.float32)
        if matrix.ndim != 2 or len(matrix) != len(batch) or not np.isfinite(matrix).all():
            raise ValueError('Invalid embedding matrix')
        norm = np.linalg.norm(matrix, axis=1, keepdims=True)
        if (norm == 0).any():
            raise ValueError('Zero embedding vector')
        matrices.append(matrix / norm)
        print(f'Embedding {min(start + 8, len(texts))}/{len(texts)}', flush=True)
    vectors = np.concatenate(matrices)
    similarities = vectors[20:] @ vectors[:20].T
    decisions = []
    for row, scores in zip(rows, similarities):
        positive = float(np.sort(scores[:10])[-3:].mean())
        negative = float(np.sort(scores[10:])[-3:].mean())
        order = np.argsort(-scores)
        decisions.append({'comment_id': row['record_id'], 'language': row['language'],
            'positive_score': positive, 'negative_score': negative, 'margin': positive - negative,
            'retrieval_related': positive > negative,
            'references': [{'topic_id': ('P' + str(int(i) + 1) if i < 10 else 'N' + str(int(i) - 9)),
                            'text': (POS + NEG)[int(i)], 'cosine': float(scores[i]),
                            'class': 'related' if i < 10 else 'unrelated'} for i in order[:4]]})
    write_json(folder / 'retrieval.json', decisions)
    return decisions


def aggregate(claims, quality_enforced=False):
    grouped = {}
    for claim in claims:
        if quality_enforced and ((claim.get('evidence_quality') or {}).get('mode') != 'enforce'
                or (claim.get('evidence_quality') or {}).get('route') != 'mechanism_evidence'
                or not (claim.get('semantic_audit') or {}).get('supported')):
            continue
        if claim['character'] is None or claim['direction'] not in (('buff', 'nerf', 'keep', 'unclear') if quality_enforced else ('buff', 'nerf')):
            continue
        if claim.get('character_identity', {}).get('normalization_status') == 'source_literal_unverified':
            continue
        # Preserve nuanced recommendations instead of performing an unverified model merge.
        key = (claim['character'], claim['direction'], claim.get('target')) if quality_enforced else (claim['character'], claim['direction'])
        group = grouped.setdefault(key, {'character': key[0], 'direction': key[1],
                                         'comment_ids': set(), 'recommendations': []})
        if quality_enforced:
            group['topic'] = key[2]
        group['comment_ids'].add(claim['comment_id'])
        group['recommendations'].append(claim)
    result = []
    for key in sorted(grouped, key=lambda k: tuple(v or '' for v in k)):
        group = grouped[key]
        group['comment_ids'] = sorted(group['comment_ids'])
        group['supporting_comment_count'] = len(group['comment_ids'])
        result.append(group)
    return result


def quality_source_counts(records, accepted):
    """Unique source sets, including overlap; no player identity is inferred."""
    general = {q['comment_id'] for q in records if any(r['route'] == 'opinion_only' for r in q['routing'])}
    concrete = {c['comment_id'] for c in accepted if (c.get('evidence_quality') or {}).get('mode') == 'enforce'}
    return {'opinion_comment_ids': sorted(general), 'audited_mechanism_comment_ids': sorted(concrete),
            'union_comment_ids': sorted(general | concrete), 'union_count': len(general | concrete),
            'overlap_comment_ids': sorted(general & concrete), 'categories_overlap': True}


def build_full_coverage(rows, decisions, routes, models, quality_records, coverage,
                        accepted, quarantine, quality_mode, args):
    extraction = {c['comment_id']: c for c in coverage}
    all_languages = {route['language'] for route in routes.values()}
    selected_languages = {routes[m]['language'] for m in models}
    result = []
    for row in rows:
        cid, lang = row['record_id'], row['language']
        d, q, e = decisions.get(cid), quality_records.get(cid), extraction.get(cid)
        if lang not in all_languages:
            status = 'unsupported_language'
        elif lang not in selected_languages:
            status = 'unselected_language'
        elif not d or not d['agreement']:
            status = 'relevance_pending_or_failed' if not d or d['model_related'] is None or d.get('model_uncertain') else 'relevance_rejected'
            if d and d.get('retrieval_triage') == 'unrelated':
                status = 'relevance_rejected'
        elif getattr(args, 'relevance_only', False):
            status = 'relevance_only_complete'
        elif quality_mode != 'off' and not q:
            status = 'quality_pending'
        elif getattr(args, 'quality_only', False):
            status = 'quality_failed' if q['status'] == 'failed' else 'quality_completed'
        elif e:
            status = 'extraction_failed' if e['disposition'] == 'generation_failed' else 'extraction_completed'
        elif q and quality_mode == 'enforce':
            status = 'quality_failed' if q['status'] == 'failed' else 'quality_routed_without_extraction'
        else:
            status = 'extraction_pending'
        result.append({'comment_id': cid, 'language': lang, 'status': status,
            'relevance': 'admitted' if d and d['agreement'] else 'not_admitted',
            'quality_status': q['status'] if q else 'not_assessed' if quality_mode == 'off' else 'pending' if d and d['agreement'] else 'not_applicable',
            'routes_present': q['routes_present'] if q else [],
            'extraction': e, 'audited_accepted_claims': sum(c['comment_id'] == cid for c in accepted),
            'quarantined_claims': sum(c['comment_id'] == cid for c in quarantine),
            'source_review': 'pending_external_review' if any(c['comment_id'] == cid for c in accepted) else 'not_applicable'})
    return result


def validate_modes(args):
    mode = getattr(args, 'evidence_quality', 'off')
    if getattr(args, 'relevance_only', False) and (mode != 'off' or getattr(args, 'quality_only', False)):
        raise ValueError('--relevance-only requires --evidence-quality off and cannot use --quality-only')
    if getattr(args, 'quality_only', False) and mode == 'off':
        raise ValueError('--quality-only requires --evidence-quality shadow or enforce')
    return mode


def run(args, *, api_transport=None, chat_transport=None, embed_transport=None, retrieval_service=None):
    quality_mode = validate_modes(args)
    quality_policy = quality.load_policy() if quality_mode != 'off' else None
    folder = args.out.resolve()
    folder.mkdir(parents=True, exist_ok=True)
    source = args.dataset.read_bytes()
    rows = [json.loads(line) for line in source.decode().splitlines() if line.strip()]
    if len({r['record_id'] for r in rows}) != len(rows):
        raise ValueError('Dataset has duplicate record IDs')
    routing = json.loads((asset_path('configs/local-language-routing.json')).read_text(encoding='utf-8'))
    routes = routing['models']
    models = [args.model] if args.model else list(routes)
    tags = (api_transport or api)(args.base_url, '/api/tags')['models']
    installed = {m['name']: m['digest'] for m in tags}
    embedding_config = None
    if getattr(args, 'embedding_provider', 'ollama') == 'configured':
        embedding_config = glossary_vectors.config(args.env_file)
        args.embedding_model = embedding_config['model']
    missing_models = sorted(set(models + ([] if embedding_config else [args.embedding_model])) - set(installed))
    if missing_models:
        raise ValueError('Required local models unavailable: ' + ', '.join(missing_models))
    prompt_names = {'relevance': 'relevance', 'retrieval_review': 'retrieval-review',
                    'extract': 'summarize-balance', 'verify': 'verify-balance'}
    if quality_mode != 'off':
        prompt_names['quality'] = 'evidence-quality'
    prompts = {stage: {lang: (asset_path(f'prompts/{name}.{lang}.txt')).read_text(encoding='utf-8')
                       for lang in ('en', 'zh')} for stage, name in prompt_names.items()}
    if quality_mode == 'enforce':
        for lang in ('en', 'zh'):
            prompts['extract'][lang] += '\n' + (asset_path(f'prompts/quality-extract.{lang}.txt')).read_text(encoding='utf-8')
            prompts['verify'][lang] += '\n' + (asset_path(f'prompts/quality-verify.{lang}.txt')).read_text(encoding='utf-8')
    quality_identity = {'mode': quality_mode, 'policy': quality_policy,
        'runner_sha256': digest(module_path('engine.py').read_bytes()),
        'model_digests': {m: installed[m] for m in models},
        'glossary_sha256': digest((asset_path('data/glossary.json')).read_bytes()),
        'policy_module_sha256': digest((module_path('balance_policy.py')).read_bytes()),
        'review_policy_sha256': digest(POLICY_PATH.read_bytes()),
        'prompts_sha256': digest(json.dumps(prompts, sort_keys=True, ensure_ascii=False).encode()),
        'module_sha256': digest((module_path('evidence_quality.py')).read_bytes()),
        'schema_sha256': digest(json.dumps(quality.annotation_schema(['COMMENT_ID']), sort_keys=True).encode())}
    identity = {'version': VERSION, 'dataset_sha256': digest(source),
        'shared_code_sha256': {p.name: digest(p.read_bytes()) for p in sorted(module_path('engine.py').parent.glob('*.py'))},
        'models': {m: installed[m] for m in models}, 'embedding_model': args.embedding_model,
        'embedding_digest': None if embedding_config else installed[args.embedding_model], 'routing': routing,
        'glossary_sha256': digest((asset_path('data/glossary.json')).read_bytes()),
        'script_sha256': digest(module_path('engine.py').read_bytes()),
        'policy_module_sha256': digest((module_path('balance_policy.py')).read_bytes()),
        'review_policy_sha256': digest(POLICY_PATH.read_bytes()),
        'mode': 'relevance_only' if getattr(args, 'relevance_only', False) else 'quality_only' if getattr(args, 'quality_only', False) else 'full_pipeline',
        'evidence_quality': quality_identity,
        'anchor_sha256': digest(json.dumps([POS, NEG], ensure_ascii=False).encode()),
        'prompts': {stage: {lang: digest(t.encode()) for lang, t in pair.items()}
                    for stage, pair in prompts.items()}}
    if embedding_config:
        identity['embedding_service'] = {'provider': 'configured', 'endpoint': embedding_config['url'],
            'model': embedding_config['model'], 'model_digest': None,
            'limitation': 'Configured remote embedding model has no locally verifiable weight digest.'}
    if getattr(args, 'num_gpu', None) is not None:
        identity['runtime_options'] = {'num_gpu': args.num_gpu}
    manifest_path = folder / 'manifest.json'
    if manifest_path.exists():
        if json.loads(manifest_path.read_text(encoding='utf-8'))['identity'] != identity:
            raise ValueError('Run inputs/code/models changed; use a new output directory')
    else:
        write_json(manifest_path, {'identity': identity, 'dataset': str(args.dataset.resolve()),
            'created_at_utc': datetime.now(timezone.utc).isoformat(),
            'retrieval': {'positive_anchors': POS, 'negative_anchors': NEG,
                'score': 'mean top-3 cosine per class', 'pass': 'positive > negative',
                'agreement': 'retrieval pass AND same-language model related AND not uncertain'}})
        write_json(folder / 'source-snapshot.json', rows)
        write_json(folder / 'prompt-snapshot.json', prompts)
        write_json(folder / 'review-policy-snapshot.json', load_policy())
        write_json(folder / 'quality-policy-snapshot.json', quality_policy)
        (folder / 'quality-module-snapshot.py').write_bytes((module_path('evidence_quality.py')).read_bytes())
        (folder / 'runner-snapshot.py').write_bytes(module_path('engine.py').read_bytes())
        (folder / 'policy-module-snapshot.py').write_bytes((module_path('balance_policy.py')).read_bytes())
    runner_factory = Runner if chat_transport is None else partial(Runner, chat_transport=chat_transport)
    if retrieval_service is None:
        retrieval_service = retrieve if api_transport is None and embed_transport is None else partial(
            retrieve, api_transport=api_transport, embed_transport=embed_transport)
    return process(args, rows, routing, models, prompts, quality_identity,
                   quality_policy, identity, embedding_config, runner_factory, retrieval_service)


def process(args, rows, routing, models, prompts, quality_identity, quality_policy,
            identity, embedding_config=None, runner_factory=Runner, retrieval_service=retrieve):
    """Shared orchestration with explicit inputs and injected inference boundaries."""
    folder, routes = args.out.resolve(), routing['models']
    quality_mode = args.evidence_quality
    by_id = {r['record_id']: r for r in rows}
    eligible = [r for r in rows if any(routes[m]['language'] == r['language'] for m in models)]
    retrieval = retrieval_service(eligible, args.base_url, folder, args.embedding_model, embedding_config)
    runner = runner_factory(args.base_url, folder, prompts, quality_identity, quality_policy)
    runner.runtime_options = identity.get('runtime_options', {})
    quality_records = {}
    trace, claims, quarantine, coverage = [], [], [], []
    decisions = {d['comment_id']: {**d, 'model_related': None, 'agreement': False} for d in retrieval}
    for decision in decisions.values():
        status, reasons = triage_retrieval(decision, by_id[decision['comment_id']]['text_original'],
                                           load_policy()['retrieval_borderline_margin'])
        decision.update(retrieval_triage=status, retrieval_triage_reasons=reasons)
    reference = character_reference()
    characters = {e['canonical_name'] for e in reference}
    for model in models:
        language = routes[model]['language']
        language_rows = [d for d in decisions.values() if d['language'] == language]
        queued = [d for d in language_rows if d['retrieval_triage'] == 'review_queue']
        cached = runner.cached_single_ids(model, language, 'retrieval_review')
        review_batches = [[d] for d in queued if d['comment_id'] in cached]
        review_batches += list(batches([d for d in queued if d['comment_id'] not in cached], count=8, chars=10000))
        for batch in review_batches:
            data = {'comments': [{'comment_id': d['comment_id'], 'text': by_id[d['comment_id']]['text_original'],
                                  'retrieved_topics': d['references']} for d in batch]}
            parsed, meta = runner.generate(model, language, 'retrieval_review', data, [d['comment_id'] for d in batch])
            trace.append({'model': model, 'stage': 'retrieval_review', **meta})
            reviewed = {d['comment_id']: d for d in parsed['decisions']} if parsed else {}
            for decision in batch:
                item = reviewed.get(decision['comment_id'], {})
                decision.update(retrieval_review_related=item.get('related'),
                                retrieval_review_uncertain=item.get('uncertain', True),
                                initial_retrieval_review_related=item.get('related'),
                                initial_retrieval_review_uncertain=item.get('uncertain', True))
                if len(batch) > 1 and (item.get('related') is not True or item.get('uncertain') is not False):
                    record_id = decision['comment_id']
                    single = {'comments': [{'comment_id': record_id, 'text': by_id[record_id]['text_original'],
                                            'retrieved_topics': decision['references']}]}
                    retry, meta = runner.generate(model, language, 'retrieval_review', single, [record_id])
                    trace.append({'model': model, 'stage': 'retrieval_review', 'refinement': True, **meta})
                    result = retry['decisions'][0] if retry else {}
                    decision.update(retrieval_review_related=result.get('related'),
                                    retrieval_review_uncertain=result.get('uncertain', True))
        candidates = [d for d in language_rows if d['retrieval_related'] or (
            d.get('retrieval_review_related') is True and d.get('retrieval_review_uncertain') is False)]
        for batch in batches(candidates, count=8, chars=10000):
            data = {'comments': [{'comment_id': d['comment_id'],
                'text': by_id[d['comment_id']]['text_original'], 'retrieved_topics': d['references']} for d in batch]}
            parsed, meta = runner.generate(model, language, 'relevance', data, [d['comment_id'] for d in batch])
            trace.append({'model': model, 'stage': 'relevance', **meta})
            if parsed:
                for item in parsed['decisions']:
                    decisions[item['comment_id']].update(model_related=item['related'],
                        model_uncertain=item['uncertain'], model_reason=item['reason'],
                        agreement=relevance_agrees(decisions[item['comment_id']], item))
        # Recheck every rejection alone: short ordered arrays can still drift
        # semantically across comments. Preserve the initial result for review.
        for decision in candidates:
            decision['initial_model_related'] = decision['model_related']
            decision['initial_model_uncertain'] = decision.get('model_uncertain')
            decision['refinement_performed'] = False
            if decision['agreement']:
                continue
            decision['refinement_performed'] = True
            record_id = decision['comment_id']
            data = {'comments': [{'comment_id': record_id, 'text': by_id[record_id]['text_original'],
                                  'retrieved_topics': decision['references']}]}
            parsed, meta = runner.generate(model, language, 'relevance', data, [record_id])
            trace.append({'model': model, 'stage': 'relevance_refinement', **meta})
            if parsed:
                item = parsed['decisions'][0]
                decision.update(model_related=item['related'], model_uncertain=item['uncertain'],
                    model_reason=item['reason'], agreement=relevance_agrees(decision, item))
        write_json(folder / 'relevance.json', list(decisions.values()))
        write_json(folder / 'review-queue.json', [d for d in decisions.values()
                   if d['retrieval_triage'] == 'review_queue' and not d['agreement']])
        if getattr(args, 'relevance_only', False):
            continue
        selected = [by_id[d['comment_id']] for d in decisions.values()
                    if d['language'] == language and d['agreement']]
        # Evidence units contain the entire original text in order. Do not send
        # a second copy of the full text, which wastes context and GPU memory.
        write_json(folder / 'full-pipeline-coverage.json', build_full_coverage(rows, decisions, routes, models, quality_records, coverage, [], quarantine, quality_mode, args))
        if quality_mode != 'off':
            for row in selected:
                record_id = row['record_id']
                units = evidence_units(row['text_original'])
                attempts = []
                result = None
                for attempt in range(quality_policy['max_attempts']):
                    data = {'comments': [{'comment_id': record_id, 'units': units}],
                        'source': row, 'language': language,
                        'character_normalization_reference': character_reference(row['text_original']),
                        'quality_contract': quality_identity, 'attempt': attempt + 1}
                    # A retry is a new request/cache identity. Failed cached
                    # attempt 1 cannot masquerade as a fresh attempt 2.
                    parsed, meta = runner.generate(model, language, 'quality', data, [record_id])
                    trace.append({'model': model, 'stage': 'quality', 'comment_id': record_id,
                                  'attempt': attempt + 1, **meta})
                    if parsed is not None:
                        result = quality.qualify(parsed, row, units, quality_policy)
                        if result['errors']:
                            meta = {**meta, 'errors': result['errors']}
                        else:
                            attempts.append(meta)
                            break
                    attempts.append(meta)
                    result = None
                record = result or quality.failed_record(row, units, attempts, quality_policy)
                record.update(attempts=attempts, model=model, observation_only=quality_mode == 'shadow')
                quality_records[record_id] = record
                write_json(folder / 'evidence-quality.json', list(quality_records.values()))
                write_json(folder / 'full-pipeline-coverage.json', build_full_coverage(rows, decisions, routes, models, quality_records, coverage, [], quarantine, quality_mode, args))
                write_json(folder / 'request-trace.json', trace)
            if getattr(args, 'quality_only', False):
                continue
        prepared = [{'comment_id': r['record_id'], 'units': evidence_units(r['text_original'])}
                    for r in selected]
        if quality_mode == 'enforce':
            prepared = [{**r, 'allowed_quality_points': quality.allowed_points(quality_records[r['comment_id']])}
                        for r in prepared if quality.allowed_points(quality_records[r['comment_id']])]
        extraction_queue = list(batches(prepared, count=4, chars=9000 if language == 'en' else 4000))
        while extraction_queue:
            batch = extraction_queue.pop(0)
            parsed, meta = runner.generate(model, language, 'extract',
                {'comments': batch, 'character_normalization_reference': character_reference('\n'.join(by_id[r['comment_id']]['text_original'] for r in batch))},
                [r['comment_id'] for r in batch])
            trace.append({'model': model, 'stage': 'extract', **meta})
            if not parsed:
                if len(batch) > 1:
                    extraction_queue[0:0] = [[item] for item in batch]
                    continue
                coverage.extend({'comment_id': r['comment_id'], 'model': model,
                                 'disposition': 'generation_failed', 'claims_generated': 0} for r in batch)
                continue
            for assessment in parsed['assessments']:
                record_id = assessment['comment_id']
                coverage.append({'comment_id': record_id, 'model': model,
                    'disposition': assessment['disposition'], 'claims_generated': len(assessment['claims'])})
                consistent = (assessment['disposition'] == 'extracted') == bool(assessment['claims'])
                for i, claim in enumerate(assessment['claims']):
                    errors, enriched = ground_claim(claim, by_id[record_id], characters)
                    if quality_mode == 'enforce':
                        quality_errors, qualification = quality.bind_claim(claim, quality_records[record_id],
                            character_reference(by_id[record_id]['text_original']))
                        errors.extend(quality_errors)
                        if enriched is not None:
                            enriched['evidence_quality'] = qualification
                    if not consistent:
                        errors.append('Disposition and claims disagree')
                    envelope = {'claim_id': record_id + ':' + str(i + 1), 'comment_id': record_id,
                                'model': model, 'claim': enriched or claim}
                    if errors:
                        quarantine.append({**envelope, 'stage': 'source_binding', 'errors': errors})
                    else:
                        claims.append(envelope)
            write_json(folder / 'extraction-coverage.json', coverage)
            write_json(folder / 'claims-before-audit.json', claims)
            write_json(folder / 'quarantined-claims.json', quarantine)
        # Audit in a separate context, with original spans, never the generator's rationale.
        pending = [c for c in claims if c['model'] == model]
        for batch in batches(pending, count=1):
            parsed, meta = runner.generate(model, language, 'verify',
                {'claims': batch, 'original_comment': by_id[batch[0]['comment_id']]['text_original']},
                                           [c['claim_id'] for c in batch])
            trace.append({'model': model, 'stage': 'verify', **meta})
            verdicts = {v['claim_id']: v for v in parsed['verdicts']} if parsed else {}
            for entry in batch:
                verdict = verdicts.get(entry['claim_id'])
                entry['audit'] = verdict
                if verdict is None or not verdict['supported']:
                    quarantine.append({**entry, 'stage': 'semantic_audit',
                        'errors': [verdict['reason'] if verdict else 'Audit failed; fail closed']})
            write_json(folder / 'audit-progress.json', claims)
            write_json(folder / 'quarantined-claims.json', quarantine)
    accepted = [{**e['claim'], 'claim_id': e['claim_id'], 'comment_id': e['comment_id'],
                 'model': e['model'], 'semantic_audit': e['audit']} for e in claims
                if (e.get('audit') or {}).get('supported')]
    summary = {'version': VERSION, 'input_comments': len(rows),
        'mode': identity['mode'],
        'input_languages': dict(Counter(r['language'] for r in rows)),
        'routed_comments': len(eligible), 'unsupported_or_unselected_language': len(rows) - len(eligible),
        'retrieval_related': sum(d['retrieval_related'] for d in decisions.values()),
        'retrieval_review_queued': sum(d['retrieval_triage'] == 'review_queue' for d in decisions.values()),
        'retrieval_review_rescues': sum(d['agreement'] and not d['retrieval_related'] for d in decisions.values()),
        'agreement_related': sum(d['agreement'] for d in decisions.values()),
        'relevance_refinements': sum(d.get('refinement_performed', False) for d in decisions.values()),
        'relevance_refinement_rescues': sum(d.get('refinement_performed', False) and d['agreement'] for d in decisions.values()),
        'assessed_comments': len(coverage), 'generated_claims': sum(c['claims_generated'] for c in coverage),
        'accepted_claims': len(accepted), 'quarantined_claims': len(quarantine),
        'source_numeric_accepted': sum(c['specificity'] == 'source_numeric' for c in accepted),
        'qualitative_only_accepted': sum(c['specificity'] == 'qualitative_only' for c in accepted),
        'failed_requests': sum(bool(t['errors']) for t in trace),
        'final_generation_failed_comments': sum(c['disposition'] == 'generation_failed' for c in coverage),
        'by_language': {lang: {'input': sum(r['language'] == lang for r in rows),
            'retrieval_related': sum(d['language'] == lang and d['retrieval_related'] for d in decisions.values()),
            'agreement_related': sum(d['language'] == lang and d['agreement'] for d in decisions.values()),
            'accepted_claims': sum(by_id[c['comment_id']]['language'] == lang for c in accepted)} for lang in ('en', 'zh')},
        'limitations': ['Automated semantic audit uses the same language-routed model in a separate context; not human ground truth.',
            'Retrieval prototypes and threshold are reused from the earlier experiment; no held-out relevance labels exist for the full corpus.',
            'Source binding proves quotation provenance, not gameplay truth or patch applicability.',
            'Semantic audit reads the full original comment; selected citations can still need additional context.',
            'Coverage accounts for every admitted comment; completeness of individual concerns still requires human review.',
            'No numerical targets are invented; qualitative comments cannot supply exact engineering values.']}
    unsupported = [{'comment_id': r['record_id'], 'language': r['language'],
                    'reason': 'No configured language route'} for r in rows if r not in eligible]
    report = {'summary': summary, 'character_adjustments': aggregate(accepted, quality_mode == 'enforce'),
        'release_status': 'requires_source_review_and_versioned_game_data',
        'unresolved_identity_claims': [c for c in accepted if c.get('character_identity', {}).get('normalization_status') == 'source_literal_unverified'],
        'other_supported_claims': [c for c in accepted if c['character'] is None or c['direction'] not in ('buff', 'nerf')],
        'coverage': coverage, 'unsupported_languages': unsupported}
    report['report_schema_version'] = 'balance-report-v3' if quality_mode == 'enforce' else VERSION
    report['evidence_quality_mode'] = quality_mode
    report['quality_assessment'] = 'enforced' if quality_mode == 'enforce' else 'observation_only' if quality_mode == 'shadow' else 'quality_not_assessed'
    full_coverage = build_full_coverage(rows, decisions, routes, models, quality_records, coverage,
                                        accepted, quarantine, quality_mode, args)
    write_json(folder / 'full-pipeline-coverage.json', full_coverage)
    report['full_pipeline_coverage'] = full_coverage
    if quality_mode != 'off':
        records = list(quality_records.values())
        routed = [{**r, 'source_url': q['source_url'], 'content_sha256': q['content_sha256'],
                   'quality_status': q['status'], 'language': q['language'], 'model': q.get('model'),
                   'policy_version': q['policy_version'], 'errors': q['errors'],
                   'quality_request_ids': [a['request_id'] for a in q.get('attempts', [])],
                   'observation_only': quality_mode == 'shadow'}
                  for q in records for r in q['routing']]
        opinions = quality.summarize_opinions(records, character_reference('\n'.join(r['text_original'] for r in rows)))
        systems = [r for r in routed if r['route'] == 'system_evidence']
        review = [r for r in routed if r['route'] == 'review']
        exclusions = [r for r in routed if r['route'] == 'exclude']
        quality_summary = {'mode': quality_mode, 'comments_assessed': len(records),
            'completed': sum(q['status'] == 'completed' for q in records),
            'failed': sum(q['status'] == 'failed' for q in records),
            'route_comment_counts': {route: len({r['comment_id'] for r in routed if r['route'] == route}) for route in quality.ROUTES},
            'route_item_counts': dict(Counter(r['route'] for r in routed)),
            'counting_note': 'Mixed comments overlap across routes; never sum groups as players.',
            'source_counts': quality_source_counts(records, accepted),
            'accuracy_validation': 'not_established; deterministic checks are not semantic accuracy'}
        for name, value in [('evidence-quality', records), ('quality-routing', routed),
                ('quality-review-queue', review), ('quality-summary', quality_summary),
                ('opinion-summary', opinions), ('system-feedback', systems), ('quality-exclusions', exclusions)]:
            write_json(folder / (name + '.json'), value)
        if quality_mode == 'enforce':
            report.update(opinion_summary=opinions, system_feedback=systems,
                          quality_review_queue=review, quality_exclusions=exclusions)
        else:
            report['quality_observation_artifacts'] = ['quality-summary.json', 'opinion-summary.json', 'system-feedback.json']
    write_json(folder / 'relevance.json', list(decisions.values()))
    write_json(folder / 'validated-claims.json', accepted)
    write_json(folder / 'quarantined-claims.json', quarantine)
    write_json(folder / 'request-trace.json', trace)
    write_json(folder / 'summary.json', summary)
    write_json(folder / 'balance-report.json', report)
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dataset', type=Path, default=ROOT / 'data/raw/feedback/20261015-expanded/screened/records.jsonl')
    parser.add_argument('--out', type=Path, default=ROOT / 'runs/balance-quality-v1')
    parser.add_argument('--model', choices=['qwen2.5:7b', 'llama3.1:latest'])
    parser.add_argument('--embedding-model', default='qwen3-embedding:8b')
    parser.add_argument('--embedding-provider', choices=['ollama', 'configured'], default='ollama')
    parser.add_argument('--env-file', type=Path, default=ROOT / '.env')
    parser.add_argument('--num-gpu', type=int, help='Explicit Ollama GPU layer count; 0 requests CPU inference')
    parser.add_argument('--base-url', default='http://127.0.0.1:11434')
    parser.add_argument('--evidence-quality', choices=['off', 'shadow', 'enforce'], default='off')
    parser.add_argument('--quality-only', action='store_true', help='Stop after quality annotation; requires shadow/enforce')
    parser.add_argument('--relevance-only', action='store_true', help='Complete retrieval and relevance gates without extraction')
    args = parser.parse_args()
    try:
        validate_modes(args)
    except ValueError as exc:
        parser.error(str(exc))
    run(args)


if __name__ == '__main__':
    main()
