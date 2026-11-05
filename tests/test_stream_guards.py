"""Incremental stream loop guards keep the stop decisions and content of the full rescans (plan step U1.3).

``old_streamed_chat`` and ``old_repeated_claim`` are copies of
``inference.streamed_chat`` and ``inference.repeated_claim`` before U1.3
(commit ``a1c034e``). Both run on the same synthetic streams through a fake
response object instead of the network.
"""
import json
from pathlib import Path
import re
import sys
import tempfile
import unittest
import urllib.request
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from aimediator import inference


def old_repeated_claim(output, allowed_ids):
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


def old_streamed_chat(base, payload, partial_path, timeout=1800):
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
                if assessment_schema.get('type') == 'object' and old_repeated_claim(''.join(parts), allowed):
                    last = {**chunk, 'done': False, 'done_reason': 'duplicate_claim_loop'}
                    break
            if chunk.get('done'):
                break
    return {**last, 'message': {'role': 'assistant', 'content': ''.join(parts)}}


class FakeResponse:
    """A streamed /api/chat response: one JSON line per chunk, the last one done."""

    def __init__(self, chunks):
        lines = [{'model': 'fake', 'message': {'role': 'assistant', 'content': c}, 'done': False} for c in chunks]
        lines.append({'model': 'fake', 'message': {'role': 'assistant', 'content': ''}, 'done': True,
                      'done_reason': 'stop', 'eval_count': len(chunks)})
        self.lines = [json.dumps(line, ensure_ascii=False).encode() + b'\n' for line in lines]
        self.lines.insert(1, b'\n')

    def __enter__(self):
        return iter(self.lines)

    def __exit__(self, *exc):
        return False


def keyed_format(ids):
    return {'type': 'object', 'properties': {'assessments': {'type': 'object', 'properties': {i: {} for i in ids}}}}


def claim(number, character='Ryu'):
    return {'character': character, 'target': 'Drive Rush %d' % number, 'direction': 'nerf',
            'recommendation': 'Reduce the advantage of move %d on block, it is too safe.' % number,
            'specificity': 'qualitative_only', 'parameters': [], 'evidence_ids': ['E%d' % number], 'uncertain': False}


def extraction_output(ids, claims_per_comment, repeat=None):
    """The text of an extraction answer; ``repeat`` = (comment index, claim index) repeats one claim."""
    assessments = {}
    for index, cid in enumerate(ids):
        claims = [claim(index * 100 + n) for n in range(claims_per_comment)]
        if repeat and repeat[0] == index:
            claims.insert(repeat[1] + 1, dict(claims[repeat[1]]))
        assessments[cid] = {'claims': claims}
    return json.dumps({'assessments': assessments}, ensure_ascii=False)


def chunks_of(text, size):
    return [text[i:i + size] for i in range(0, len(text), size)]


def samples():
    """(name, format, output) for the synthetic streams."""
    ids = ['steam:1', 'steam:2', 'bili:3', 'bili:4']
    keyed = keyed_format(ids)
    array = {'type': 'object', 'properties': {'assessments': {'type': 'array'}}}
    duplicate_key = extraction_output(ids, 1)[:-2] + ', "steam:2": {"claims": []}}}'
    same_claim_other_comment = json.dumps({'assessments': {'steam:1': {'claims': [claim(1)]},
                                                           'steam:2': {'claims': [claim(1)]}}})
    escaped = json.dumps({'assessments': {'steam:1': {'claims': [dict(claim(1), recommendation='"steam:1": x')]},
                                          'steam:2': {'claims': []}}})
    return [
        ('normal', keyed, extraction_output(ids, 2)),
        ('normal-zh', keyed, json.dumps({'assessments': {'bili:3': {'claims': [claim(7, '隆')]}}}, ensure_ascii=False)),
        ('duplicate-key', keyed, duplicate_key),
        ('duplicate-claim', keyed, extraction_output(ids, 2, repeat=(1, 0))),
        ('same-claim-other-comment', keyed, same_claim_other_comment),
        ('escaped-key-in-text', keyed, escaped),
        ('array-normal', array, '{"assessments":[{"comment_id":"a","x":1},{"comment_id":"b"}]}'),
        ('array-duplicate', array, '{"assessments":[{"comment_id":"a"},{"comment_id" : "a"}]}'),
        ('whitespace', keyed, '{"assessments": {' + ' ' * 300 + '}}'),
        ('whitespace-short', keyed, '{"assessments": {' + ' ' * 200 + '"steam:1": {"claims": []}}}'),
        ('quality', {'type': 'object', 'properties': {'segments': {}}}, '{"segments": [], "x": "' + ' ' * 10 + '"}'),
        ('malformed', keyed, '{"assessments": {"steam:1": {"claims": [{"character": "Ryu" "x"}, {"character": "Ken"}]}}}'),
    ]


class StreamGuardTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.partial = Path(temp.name) / 'partial-output.txt'

    def run_both(self, payload, chunks):
        results = []
        for function in (old_streamed_chat, inference.streamed_chat):
            with patch.object(urllib.request, 'urlopen', return_value=FakeResponse(chunks)):
                result = function('http://fixture.invalid', payload, self.partial)
            results.append((result, self.partial.read_text(encoding='utf-8')))
        return results

    def test_same_stop_decision_and_content_at_every_chunking(self):
        reasons = {}
        for name, schema, output in samples():
            payload = {'model': 'fake', 'messages': [], 'format': schema, 'stream': True}
            sizes = (4, 1, 2, 3, 5, 7, 16, len(output)) if len(output) <= 400 else (4, 9, 16, len(output))
            chunkings = [chunks_of(output, size) for size in sizes]
            if len(output) <= 400:  # every chunk boundary position
                chunkings += [[output[:k], output[k:]] for k in range(1, len(output))]
            for chunks in chunkings:
                old, new = self.run_both(payload, chunks)
                self.assertEqual(new, old, (name, [len(c) for c in chunks]))
                reasons.setdefault(name, old[0]['done_reason'])
        self.assertEqual(reasons, {
            'normal': 'stop', 'normal-zh': 'stop', 'duplicate-key': 'duplicate_comment_loop',
            'duplicate-claim': 'duplicate_claim_loop', 'same-claim-other-comment': 'stop',
            'escaped-key-in-text': 'stop', 'array-normal': 'stop', 'array-duplicate': 'duplicate_comment_loop',
            'whitespace': 'whitespace_loop', 'whitespace-short': 'stop', 'quality': 'stop', 'malformed': 'stop'})

    def test_large_outputs_keep_the_stop_decision(self):
        ids = ['c%d' % n for n in range(4)]
        for claims, repeat in ((8, (3, 6)), (8, (0, 0))):
            output = extraction_output(ids, claims, repeat)
            payload = {'model': 'fake', 'messages': [], 'format': keyed_format(ids), 'stream': True}
            old, new = self.run_both(payload, chunks_of(output, 4))
            self.assertEqual(new, old)
            self.assertEqual(new[0]['done_reason'], 'duplicate_claim_loop' if repeat else 'stop')

    def test_repeated_claim_is_unchanged(self):
        ids = {'c0', 'c1', 'c2', 'c3'}
        for repeat in (None, (0, 0), (2, 3)):
            output = extraction_output(sorted(ids), 5, repeat)
            for end in range(0, len(output), 13):
                self.assertEqual(inference.repeated_claim(output[:end], ids), old_repeated_claim(output[:end], ids))


if __name__ == '__main__':
    unittest.main()
