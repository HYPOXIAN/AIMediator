"""Ollama HTTP calls and injected production transports with durable finite attempt budgets."""
import bisect
import json
import re
import urllib.request
from urllib.error import HTTPError
import numpy as np
from . import glossary_vectors
from .common import Failure, canonical, read, sha, strict_json, write


def api(base, endpoint, payload=None):
    data = None if payload is None else json.dumps(payload, ensure_ascii=False).encode()
    request = urllib.request.Request(base + endpoint, data=data,
                                     headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(request, timeout=1800) as response:
        return json.load(response)


def claim_pattern(claim_key):
    """Return the pattern of the start of a claim object whose first property is ``claim_key``."""
    return re.compile(r'\{\s*"' + re.escape(claim_key) + r'"\s*:')


def claim_key(assessment_schema):
    """Return the first property of the claim items of a keyed assessments schema, or None.

    The path is ``properties[<comment ID>].properties.claims.items.properties`` (plan 4.3,
    U5.1): claim objects are recognized by the first property the schema asks for, so
    the guard follows the claim order of the request without importing ``evidence``.
    """
    if assessment_schema.get('type') != 'object':
        return None
    for comment in assessment_schema.get('properties', {}).values():
        claims = comment.get('properties', {}).get('claims', {}) if isinstance(comment, dict) else {}
        properties = claims.get('items', {}).get('properties') if isinstance(claims, dict) else None
        if properties:
            return next(iter(properties))
    return None


def repeated_claim(output, allowed_ids, first_key):
    """Return whether two complete claims (objects starting with ``first_key``) under the same comment key are equal."""
    scopes = [(match.start(), match.group(1)) for match in
              re.finditer(r'(?<!\\)"([^"]+)"\s*:', output) if match.group(1) in allowed_ids]
    seen = set()
    decoder = json.JSONDecoder()
    for match in claim_pattern(first_key).finditer(output):
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


_KEY = re.compile(r'(?<!\\)"([^"]+)"\s*:')
_COMMENT_ID = re.compile(r'(?<!\\)"comment_id"\s*:\s*"([^"]+)"')


class _LoopGuard:
    """Duplicate-comment and duplicate-claim checks over a growing output, scanning only what is new.

    A match of each pattern, once complete, does not change when the output grows,
    and an attempt that reaches the end of the output leaves no complete match after
    it. Resuming each scan at the end of its last match therefore finds the matches
    of a full scan, and the results equal ``re.findall`` and ``repeated_claim`` over
    the whole output.
    """

    def __init__(self, assessment_schema):
        self.keyed = assessment_schema.get('type') == 'object'
        self.allowed = set(assessment_schema['properties']) if self.keyed else None
        key = claim_key(assessment_schema)
        self.claim_pattern = None if key is None else claim_pattern(key)
        self.identities, self.position = set(), 0
        self.scope_starts, self.scope_keys = [], []
        self.claim_position, self.pending, self.signatures = 0, [], set()
        self.decoder = json.JSONDecoder()

    def duplicate_identity(self, output):
        """Return whether the comment identities seen so far hold a duplicate."""
        duplicate = False
        for match in (_KEY if self.keyed else _COMMENT_ID).finditer(output, self.position):
            self.position = match.end()
            identity = match.group(1)
            if self.keyed:
                if identity not in self.allowed:
                    continue
                self.scope_starts.append(match.start())
                self.scope_keys.append(identity)
            duplicate = duplicate or identity in self.identities
            self.identities.add(identity)
        return duplicate

    def repeated_claim(self, output):
        """Return whether two complete claims under the same comment key are equal; call after duplicate_identity.

        Claims are the objects that start with the first claim property of the request's
        schema (``claim_key``); a schema without claim items has no claims to compare.
        """
        if self.claim_pattern is None:
            return False
        for match in self.claim_pattern.finditer(output, self.claim_position):
            self.claim_position = match.end()
            self.pending.append(match.start())
        pending, repeated = [], False
        for start in self.pending:
            try:
                claim, _ = self.decoder.raw_decode(output, start)
            except ValueError:
                pending.append(start)
                continue
            # Every key match before a complete claim is complete, so its parents are final.
            parents = bisect.bisect_left(self.scope_starts, start)
            if not parents:
                continue
            signature = (self.scope_keys[parents - 1], json.dumps(claim, sort_keys=True, ensure_ascii=False))
            repeated = repeated or signature in self.signatures
            self.signatures.add(signature)
        self.pending = pending
        return repeated


def streamed_chat(base, payload, partial_path, timeout=1800):
    request = urllib.request.Request(base + '/api/chat',
        data=json.dumps(payload, ensure_ascii=False).encode(), headers={'Content-Type': 'application/json'})
    output, last, whitespace, guard = '', {}, 0, None
    with partial_path.open('w', encoding='utf-8') as log, urllib.request.urlopen(request, timeout=timeout) as response:
        for line in response:
            if not line.strip():
                continue
            chunk = json.loads(line)
            fragment = chunk.get('message', {}).get('content', '')
            output += fragment
            log.write(fragment)
            log.flush()
            whitespace = whitespace + len(fragment) if fragment and fragment.isspace() else 0
            last = chunk
            if whitespace > 256:
                last = {**chunk, 'done': False, 'done_reason': 'whitespace_loop'}
                break
            if 'assessments' in payload['format']['properties']:
                if guard is None:
                    guard = _LoopGuard(payload['format']['properties']['assessments'])
                if guard.duplicate_identity(output):
                    last = {**chunk, 'done': False, 'done_reason': 'duplicate_comment_loop'}
                    break
                if guard.keyed and guard.repeated_claim(output):
                    last = {**chunk, 'done': False, 'done_reason': 'duplicate_claim_loop'}
                    break
            if chunk.get('done'):
                break
    return {**last, 'message': {'role': 'assistant', 'content': output}}



class Transport:
    provenance = 'live_local_generation'

    def __init__(self, cfg, key=None, folder=None):
        self.cfg, self.key, self.folder = cfg, key, folder

    def _json(self, url, payload=None, headers=None, timeout=None):
        data = canonical(payload) if payload is not None else None
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json', **(headers or {})})
        with urllib.request.urlopen(req, timeout=timeout or self.cfg['request_timeout']) as response:
            return strict_json(response.read().decode('utf-8'))

    def tags(self):
        return self._json(self.cfg['base_url'] + '/api/tags', timeout=self.cfg['connection_timeout'])

    def version(self):
        """Return the service's /api/version answer, or None when the service has no such endpoint (HTTP 404)."""
        try:
            return self._json(self.cfg['base_url'] + '/api/version', timeout=self.cfg['connection_timeout'])
        except HTTPError as exc:
            if exc.code == 404:
                return None
            raise Failure(3, 'Service/model probe unavailable (HTTP %d)' % exc.code) from None
        except (OSError, ValueError, KeyError, TypeError) as exc:
            raise Failure(3, 'Service/model probe unavailable (' + type(exc).__name__ + ')') from None

    def _durable(self, directory, request, call, attempts=1):
        """Reserve each attempt before I/O; a crash consumes its finite budget."""
        write(directory / 'request.json', request)
        for index in range(1, attempts + 1):
            slot = directory / ('attempt-%d.json' % index)
            if slot.exists():
                item = read(slot)
                if item['state'] == 'completed':
                    return item['result']
                continue
            write(slot, {'state': 'started', 'attempt': index, 'request_sha256': sha(canonical(request))})
            try:
                result = call()
            except KeyboardInterrupt:
                write(slot, {'state': 'interrupted', 'attempt': index, 'reason': 'user_interruption'})
                raise
            except (OSError, ValueError, KeyError, TypeError) as exc:
                # Never persist remote bodies, headers, URLs or credential-bearing exceptions.
                write(slot, {'state': 'failed', 'attempt': index, 'reason': type(exc).__name__})
                continue
            write(slot, {'state': 'completed', 'attempt': index, 'result': result})
            return result
        raise Failure(5, 'Persistent request attempt budget exhausted; start a new run for another bounded trial')

    def api(self, base, endpoint, payload=None):
        request = {'base_url': base, 'endpoint': endpoint, 'payload': payload}
        if not self.folder:
            return self._json(base + endpoint, payload, timeout=self.cfg['connection_timeout'])
        directory = self.folder / 'requests' / 'embedding' / sha(canonical(request))
        return self._durable(directory, request, lambda: self._json(base + endpoint, payload))

    def embed(self, cfg, texts):
        request = {'endpoint': cfg['url'], 'model': cfg['model'], 'input': texts, 'encoding_format': 'float'}
        def call():
            result = self._json(cfg['url'], {'model': cfg['model'], 'input': texts, 'encoding_format': 'float'},
                                {'Authorization': 'Bearer ' + self.key})
            rows = result.get('data', [])
            if len(rows) != len(texts) or sorted(r.get('index', -1) for r in rows) != list(range(len(texts))):
                raise ValueError('Missing or duplicate embedding indexes')
            rows.sort(key=lambda r: r['index'])
            vectors = glossary_vectors.normalize([r['embedding'] for r in rows])
            return {'vectors': vectors.tolist(), 'usage': result.get('usage', {})}
        if self.folder:
            result = self._durable(self.folder / 'requests' / 'embedding' / sha(canonical(request)), request, call, 4)
        else:
            result = call()
        return np.asarray(result['vectors'], dtype=np.float32), result['usage']

    def chat(self, base, payload, partial_path):
        directory = partial_path.parent / 'transport-attempts'
        request = {'base_url': base, 'payload': payload}
        try:
            return self._durable(directory, request,
                lambda: streamed_chat(base, payload, partial_path, timeout=self.cfg['request_timeout']))
        except Failure:
            return {'done': False, 'done_reason': 'attempt_budget_exhausted',
                    'message': {'content': ''}, 'error': 'Persistent transport attempt budget exhausted'}


def service_version(transport):
    """Return the service version string of a transport, or None when the service does not report one."""
    answer = transport.version()
    if answer is None:
        return None
    if not isinstance(answer, dict) or not isinstance(answer.get('version'), str):
        raise Failure(3, 'Service/model probe unavailable (ValueError)')
    return answer['version']


def probe(cfg, transport, require_embedding=True):
    """Availability only: no chat, substitution, downloads or local mutation."""
    try:
        installed = {r['name']: r['digest'] for r in transport.tags()['models']}
        wanted = list(cfg['routing']['models'])
        if cfg['embedding']['provider'] == 'ollama':
            wanted.append(cfg['embedding']['model'])
        missing = sorted(set(wanted) - set(installed))
        if missing:
            raise Failure(3, 'Required local models unavailable: ' + ', '.join(missing))
        if require_embedding:
            if cfg['embedding']['provider'] == 'configured':
                transport.embed({'url': cfg['embedding']['endpoint'], 'model': cfg['embedding']['model']}, ['SF6 balance diagnostic'])
            else:
                result = transport.api(cfg['base_url'], '/api/embed', {'model': cfg['embedding']['model'],
                                       'input': ['SF6 balance diagnostic'], 'truncate': False, 'keep_alive': '10m'})
                matrix = glossary_vectors.normalize(result['embeddings'])
                if len(matrix) != 1:
                    raise ValueError('Invalid probe row count')
        return installed
    except Failure:
        raise
    except HTTPError as exc:
        raise Failure(3, 'Service/model probe unavailable (HTTP %d)' % exc.code) from None
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise Failure(3, 'Service/model probe unavailable (' + type(exc).__name__ + ')') from None
