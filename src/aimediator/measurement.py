"""Measure run requests, claim outcomes and extraction positions; materialize evaluation inputs.

Reads CLI runs, legacy runs and archived runs without writing to them. Missing
response counters stay None, never zero. No network and no model.
"""
from collections import Counter
from datetime import datetime
import json
from pathlib import Path
import statistics

from .common import read, sha, strict_json
from .quality_scoring import proportion

STAGES = ('relevance', 'retrieval_review', 'quality', 'extract', 'verify')
COUNTERS = (('prompt_tokens', 'prompt_eval_count', 1), ('cached_tokens', 'prompt_eval_cached_count', 1),
            ('output_tokens', 'eval_count', 1), ('prefill_seconds', 'prompt_eval_duration', 1e9),
            ('decode_seconds', 'eval_duration', 1e9), ('load_seconds', 'load_duration', 1e9))
METRICS = ('prompt_tokens', 'cached_tokens', 'uncached_tokens', 'output_tokens', 'prefill_seconds', 'decode_seconds',
           'load_seconds', 'elapsed_seconds')
NESTED = ('comments[].units[].text', 'comments[].text', 'comments[].retrieved_topics')


def _number(value):
    return value if isinstance(value, (int, float)) and not isinstance(value, bool) else None


def _optional(folder, name, default):
    path = folder / name
    return read(path) if path.exists() else default


def _chars(value):
    """Characters of a value as it appears in a user message (json.dumps, ensure_ascii False)."""
    return len(json.dumps(value, ensure_ascii=False))


def _text(value):
    """Characters of a text part itself, without JSON quotes and escapes; other values as in _chars."""
    return len(value) if isinstance(value, str) else _chars(value)


def _stat(values):
    values = [v for v in values if v is not None]
    if not values:
        return {'count': 0, 'sum': None, 'mean': None, 'median': None, 'max': None}
    return {'count': len(values), 'sum': sum(values), 'mean': sum(values) / len(values),
            'median': statistics.median(values), 'max': max(values)}


def _time(text):
    if not isinstance(text, str):
        return None
    return datetime.fromisoformat(text[:-1] + '+00:00' if text.endswith('Z') else text)


def run_info(folder):
    """Return the run's name, format (cli or legacy), timestamps and wall time from the manifest and run state."""
    folder = Path(folder)
    manifest = _optional(folder, 'manifest.json', {})
    state = _optional(folder, 'run-state.json', {})
    created, updated = manifest.get('created_at_utc'), state.get('updated_at_utc')
    start, end = _time(created), _time(updated)
    return {'name': folder.name,
            'format': 'cli' if manifest.get('schema_version') == 'aimediator-run-v1' else 'legacy',
            'created_at_utc': created, 'updated_at_utc': updated, 'run_state': state.get('run_state'),
            'stage': state.get('stage'),
            'wall_seconds': (end - start).total_seconds() if start and end else None}


def _composition(request):
    messages = request.get('messages') or []
    system = next((m.get('content') or '' for m in messages if m.get('role') == 'system'), '')
    user_text = next((m.get('content') or '' for m in messages if m.get('role') == 'user'), '')
    try:
        user = strict_json(user_text)
    except ValueError:
        user = None
    user = user if isinstance(user, dict) else {}
    comments = [c for c in user.get('comments') or [] if isinstance(c, dict)]
    nested = {
        'comments[].units[].text': sum(_text(u['text']) for c in comments for u in c.get('units') or []
                                       if isinstance(u, dict) and 'text' in u),
        'comments[].text': sum(_text(c['text']) for c in comments if 'text' in c),
        'comments[].retrieved_topics': sum(_chars(c['retrieved_topics']) for c in comments if 'retrieved_topics' in c)}
    return {'system_prompt': len(system), 'format': _chars(request['format']) if 'format' in request else 0,
            'user_message': len(user_text), 'user_keys': {k: _chars(v) for k, v in user.items()}, 'nested': nested}


def request_record(directory):
    """Return the measured fields of one request directory requests/<stage>/<id>/."""
    directory = Path(directory)
    request = read(directory / 'request.json')
    response = _optional(directory, 'response.json', None)
    result = response.get('response') if isinstance(response, dict) else None
    result = result if isinstance(result, dict) else {}
    validation = _optional(directory, 'validation.json', None)
    provenance = _optional(directory, 'transport-provenance.json', None)
    reused = (directory / 'reuse-provenance.json').exists() or (
        isinstance(provenance, dict) and provenance.get('kind') != 'fresh_inference')
    values = {}
    for name, key, scale in COUNTERS:
        value = _number(result.get(key))
        values[name] = None if value is None else value / scale
    prompt, cached = values['prompt_tokens'], values['cached_tokens']
    values['uncached_tokens'] = prompt - cached if prompt is not None and cached is not None else None
    values['elapsed_seconds'] = _number(response.get('elapsed_seconds')) if isinstance(response, dict) else None
    if response is None:
        done_reason = 'no_response'
    else:
        done_reason = result.get('done_reason') if isinstance(result.get('done_reason'), str) else 'absent'
    return {'stage': directory.parent.name, 'model': request.get('model'), 'request_id': directory.name,
            'reused': reused, 'done_reason': done_reason,
            'validation_errors': None if validation is None else len(validation.get('errors') or []),
            'values': values, 'composition': _composition(request)}


def request_records(folder):
    """Return the records of every request directory of the measured stages, in stage and name order.

    requests/embedding/ is not a chat stage, and the transport-attempts/ folders inside a request directory are not
    requests, so neither is read.
    """
    records = []
    for stage in STAGES:
        root = Path(folder) / 'requests' / stage
        if root.is_dir():
            records.extend(request_record(d) for d in sorted(root.iterdir())
                           if d.is_dir() and (d / 'request.json').exists())
    return records


def _mean_composition(records):
    count = len(records)
    parts = [r['composition'] for r in records]
    keys = {}
    for part in parts:
        for key in part['user_keys']:
            keys.setdefault(key, None)
    return {'requests': count,
            'system_prompt': sum(p['system_prompt'] for p in parts) / count,
            'format': sum(p['format'] for p in parts) / count,
            'user_message': sum(p['user_message'] for p in parts) / count,
            'user_keys': {k: {'requests': sum(k in p['user_keys'] for p in parts),
                              'mean': sum(p['user_keys'].get(k, 0) for p in parts) / count} for k in keys},
            'nested': {k: sum(p['nested'][k] for p in parts) / count for k in NESTED}}


def _group(records):
    fresh = [r for r in records if not r['reused']]
    reused = [r for r in records if r['reused']]
    return {'requests': len(records), 'fresh': len(fresh), 'reused': len(reused),
            'done_reason': dict(sorted(Counter(r['done_reason'] for r in records).items())),
            'with_validation_errors': sum(bool(r['validation_errors']) for r in records),
            'without_validation': sum(r['validation_errors'] is None for r in records),
            'fresh_metrics': {m: _stat([r['values'][m] for r in fresh]) for m in METRICS},
            'reused_metrics': {m: _stat([r['values'][m] for r in reused]) for m in METRICS},
            'composition': _mean_composition(records)}


def request_metrics(folder):
    """Per stage, for all models and per model: counts, done reasons, validation errors, token, time and
    composition statistics of the run's requests, plus the run's wall time.

    Token and time statistics are kept apart for fresh and reused requests. A request is reused when its
    transport-provenance.json has a kind other than fresh_inference or when a reuse-provenance.json exists.
    Composition is the mean number of characters per request: the system prompt and the user message as sent,
    format and each top-level user key as JSON text, and the nested text parts (unit and comment text) without
    their JSON quotes; retrieved_topics as JSON text.
    """
    records = request_records(folder)
    stages = {}
    for stage in STAGES:
        group = [r for r in records if r['stage'] == stage]
        if group:
            models = sorted({str(r['model']) for r in group})
            stages[stage] = {'all': _group(group),
                             'models': {m: _group([r for r in group if str(r['model']) == m]) for m in models}}
    return {'schema_version': 'aimediator-request-metrics-v1', 'run': run_info(folder), 'stages': stages}


def comment_languages(folder):
    """Map comment IDs to languages from the source snapshot, relevance and coverage artifacts of a run."""
    folder = Path(folder)
    languages = {}
    for name, key in (('source-snapshot.json', 'record_id'), ('relevance.json', 'comment_id'),
                      ('full-pipeline-coverage.json', 'comment_id')):
        for row in _optional(folder, name, []):
            if isinstance(row, dict) and key in row and row.get('language') is not None:
                languages[row[key]] = row['language']
    return languages


def claim_entries(folder):
    """Return (accepted, generated) claim lists of a run as {comment_id, character, direction, outcome, ...}.

    Generated claims are the validated ones plus the quarantined ones that carry a claim object.
    """
    folder = Path(folder)
    accepted = [{'comment_id': c.get('comment_id'), 'character': c.get('character'), 'direction': c.get('direction'),
                 'outcome': 'accepted'} for c in _optional(folder, 'validated-claims.json', [])]
    quarantined = []
    for entry in _optional(folder, 'quarantined-claims.json', []):
        claim = entry.get('claim')
        if not isinstance(claim, dict):
            continue
        binding = entry.get('stage') == 'source_binding'
        quarantined.append({'comment_id': entry.get('comment_id'), 'character': claim.get('character'),
                            'direction': claim.get('direction'),
                            'outcome': 'binding_quarantined' if binding else 'audit_rejected',
                            'errors': entry.get('errors') or [],
                            'status': None if binding else ((entry.get('audit') or {}).get('support_status')
                                                            or 'audit_failed')})
    return accepted, accepted + quarantined


def _outcome_counts(claims):
    counts = Counter(c['outcome'] for c in claims)
    audited = len(claims) - counts['binding_quarantined']
    return {'generated': len(claims), 'binding_quarantined': counts['binding_quarantined'], 'audited': audited,
            'audit_rejected': counts['audit_rejected'], 'accepted': counts['accepted'],
            'audit_rejection': proportion(counts['audit_rejected'], audited)}


def _quality(records):
    attempted = [q for q in records if q.get('attempts')]
    first_valid = sum(not (q['attempts'][0].get('errors') or []) for q in attempted)
    return {'comments': len(records),
            'status': dict(sorted(Counter(str(q.get('status')) for q in records).items())),
            'first_attempt_valid': proportion(first_valid, len(attempted)),
            'attempts': {'total': sum(len(q.get('attempts') or []) for q in records),
                         'per_comment': dict(sorted(Counter(str(len(q.get('attempts') or [])) for q in records).items()))},
            'attempt_errors': dict(Counter(e for q in records for a in q.get('attempts') or []
                                           for e in a.get('errors') or []).most_common()),
            'route_comments': dict(sorted(Counter(r for q in records for r in q.get('routes_present') or []).items())),
            'route_items': dict(sorted(Counter(r.get('route') for q in records for r in q.get('routing') or []).items()))}


def claim_outcomes(folder):
    """Generated, binding-quarantined (by error), audit-rejected (by status) and accepted claims, overall, by language
    and by language and direction; coverage status and extraction disposition counts; quality first-attempt
    validity, attempts and route counts."""
    folder = Path(folder)
    languages = comment_languages(folder)
    _, generated = claim_entries(folder)
    by_language, by_direction = {}, {}
    for language in sorted({str(languages.get(c['comment_id'], 'unknown')) for c in generated}):
        group = [c for c in generated if str(languages.get(c['comment_id'], 'unknown')) == language]
        by_language[language] = _outcome_counts(group)
        by_direction[language] = {d: _outcome_counts([c for c in group if str(c['direction']) == d])
                                  for d in sorted({str(c['direction']) for c in group})}
    coverage = _optional(folder, 'full-pipeline-coverage.json', [])
    extraction = _optional(folder, 'extraction-coverage.json', [])
    return {'schema_version': 'aimediator-claim-outcomes-v1', 'run': folder.name,
            'claims': _outcome_counts(generated),
            'binding_errors': dict(Counter(e for c in generated if c['outcome'] == 'binding_quarantined'
                                           for e in c['errors']).most_common()),
            'audit_status': dict(sorted(Counter(c['status'] for c in generated
                                                if c['outcome'] == 'audit_rejected').items())),
            'by_language': by_language, 'by_language_direction': by_direction,
            'coverage_status': dict(sorted(Counter(str(c.get('status')) for c in coverage).items())),
            'extraction_dispositions': dict(sorted(Counter(str(c.get('disposition')) for c in extraction).items())),
            'quality': _quality(_optional(folder, 'evidence-quality.json', []))}


def _lines(path):
    return [line for line in Path(path).read_bytes().decode('utf-8').splitlines() if line.strip()]


def set_items(set_dir):
    """Return the (ID, content hash, split) items of an evaluation set, in the set's order.

    Reads labels.jsonl (comment_id with content_sha256 or source_sha256) or ids.json (record_id, content_sha256), and
    checks the file against the labels_sha256 or ids_sha256 of the set's manifest when it records one.
    """
    set_dir = Path(set_dir)
    manifest = _optional(set_dir, 'manifest.json', {})
    labels, ids = set_dir / 'labels.jsonl', set_dir / 'ids.json'
    if labels.exists() and ids.exists():
        raise ValueError('Evaluation set has both labels.jsonl and ids.json')
    if labels.exists():
        path, key, rows = labels, 'labels_sha256', [strict_json(line) for line in _lines(labels)]
    elif ids.exists():
        path, key, rows = ids, 'ids_sha256', read(ids)
    else:
        raise ValueError('Evaluation set has no labels.jsonl or ids.json')
    if key in manifest and manifest[key] != sha(path.read_bytes()):
        raise ValueError('Evaluation set file differs from its manifest: ' + path.name)
    items, seen = [], set()
    for row in rows:
        identity = row.get('comment_id', row.get('record_id'))
        content = row.get('content_sha256', row.get('source_sha256'))
        if not isinstance(identity, str) or not isinstance(content, str):
            raise ValueError('Evaluation set row lacks an ID or a content hash')
        if identity in seen:
            raise ValueError('Duplicate ID in evaluation set: ' + identity)
        seen.add(identity)
        items.append((identity, content, row.get('split')))
    return items


def materialize(set_dir, dataset, split=None):
    """Return the input JSONL bytes of an evaluation set: the dataset rows, unchanged, in the set's order.

    Raises ValueError when the dataset differs from the source_dataset_sha256 of the set's manifest, when a row is
    missing, or when the SHA-256 of a row's text_original differs from the stored content hash.
    """
    dataset = Path(dataset)
    manifest = _optional(Path(set_dir), 'manifest.json', {})
    if 'source_dataset_sha256' in manifest and manifest['source_dataset_sha256'] != sha(dataset.read_bytes()):
        raise ValueError('Dataset differs from the source dataset of the evaluation set')
    items = set_items(set_dir)
    if split is not None:
        if any(s is None for _, _, s in items):
            raise ValueError('Evaluation set has no splits')
        items = [item for item in items if item[2] == split]
        if not items:
            raise ValueError('Evaluation set has no rows in split ' + split)
    rows = {}
    for line in _lines(dataset):
        record_id = strict_json(line)['record_id']
        if record_id in rows:
            raise ValueError('Duplicate record_id in dataset: ' + record_id)
        rows[record_id] = line
    out = []
    for identity, content, _ in items:
        if identity not in rows:
            raise ValueError('Row missing from dataset: ' + identity)
        if sha(strict_json(rows[identity])['text_original'].encode('utf-8')) != content:
            raise ValueError('Content hash differs: ' + identity)
        out.append(rows[identity])
    return ('\n'.join(out) + '\n').encode('utf-8')


def _position_metrics(labels, accepted, generated, admitted):
    scored = [l for l in labels if not l.get('uncertain')]
    positions = {l['comment_id']: {(p['character'], p['direction']) for p in l.get('positions') or []}
                 for l in scored}
    uncertain = {l['comment_id'] for l in labels if l.get('uncertain')}

    def correct(claims):
        claims = [c for c in claims if c['comment_id'] in positions]
        return sum((c['character'], c['direction']) in positions[c['comment_id']] for c in claims), len(claims)

    found = {(c['comment_id'], c['character'], c['direction']) for c in accepted if c['comment_id'] in positions}
    every = [(cid, *p) for cid, items in positions.items() for p in items]
    admitted_positions = [p for p in every if p[0] in admitted]
    return {'comments': len(scored),
            'admitted_comments': sum(cid in admitted for cid in positions),
            'precision_accepted': proportion(*correct(accepted)),
            'precision_generated': proportion(*correct(generated)),
            'recall': proportion(sum(p in found for p in every), len(every)),
            'recall_admitted': proportion(sum(p in found for p in admitted_positions), len(admitted_positions)),
            'uncertain': {'comments': len(uncertain),
                          'accepted_claims': sum(c['comment_id'] in uncertain for c in accepted),
                          'generated_claims': sum(c['comment_id'] in uncertain for c in generated)}}


def score_positions(folder, labels, split=None):
    """Score a run's claims against comment-level (character, direction) position labels, overall and by language.

    A claim is correct when its character and direction equal one labeled position of its comment. Precision is
    over accepted and over generated claims; recall is over all labeled positions and over the positions of
    admitted comments (relevance.json agreement), found by accepted claims, each position counted once. Comments
    labeled uncertain are excluded from both and counted apart; labeled comments absent from the run are not
    scored. Intervals are Wilson 95 % (quality_scoring.proportion).
    """
    folder, labels = Path(folder), Path(labels)
    path = labels / 'labels.jsonl' if labels.is_dir() else labels
    rows = [strict_json(line) for line in _lines(path)]
    if split is not None:
        rows = [r for r in rows if r.get('split') == split]
    present = set(comment_languages(folder))
    scored = [r for r in rows if r['comment_id'] in present]
    admitted = {d['comment_id'] for d in _optional(folder, 'relevance.json', []) if d.get('agreement') is True}
    accepted, generated = claim_entries(folder)
    result = {'schema_version': 'aimediator-position-scores-v1', 'run': folder.name,
              'labels': path.parent.name if path.name == 'labels.jsonl' else path.name, 'split': split,
              'labeled_comments': len(rows), 'absent_from_run': len(rows) - len(scored),
              'overall': _position_metrics(scored, accepted, generated, admitted), 'by_language': {}}
    for language in sorted({str(r.get('language')) for r in scored}):
        group = [r for r in scored if str(r.get('language')) == language]
        result['by_language'][language] = _position_metrics(group, accepted, generated, admitted)
    return result
