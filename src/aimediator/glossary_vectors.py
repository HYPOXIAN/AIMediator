"""Build and search a local, cosine-similarity glossary index (requires numpy)."""
import argparse
import json
import os
from pathlib import Path
import sys
import time
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import numpy as np

from .common import sha as digest, write as write_json
from .config import embedding_endpoint, env_values
from .resources import asset_path
ROOT = Path.cwd()
DEFAULT_INDEX = ROOT / 'data/processed/glossary-vectors'
QUERY_INSTRUCTION = 'Instruct: Retrieve the Street Fighter 6 glossary concept matching this query, preserving character and move qualifiers.\nQuery: '


def config(env_path):
    values = env_values(env_path) if env_path and env_path.exists() else {}
    def get(key):
        value = os.environ.get(key) or values.get(key)
        if not value:
            raise ValueError(f'Missing configuration: {key}')
        return value
    return {'url': embedding_endpoint(get('EMBEDDING_API_URL')),
            'model': get('EMBEDDING_MODEL'), 'key': get('EMBEDDING_API_KEY')}


def document(entry):
    # Include every alias, but keep its provenance and restrictions attached.
    fields = ('id', 'scope', 'category', 'canonical_name', 'chinese_label',
              'classic_notation', 'super_art_level', 'notes', 'aliases')
    return json.dumps({k: entry[k] for k in fields if k in entry}, ensure_ascii=False, sort_keys=True)


def normalize(vectors):
    matrix = np.asarray(vectors, dtype=np.float32)
    if matrix.ndim != 2 or not matrix.shape[1] or not np.isfinite(matrix).all():
        raise ValueError('Embedding response must be a finite 2D matrix')
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    if (norms == 0).any():
        raise ValueError('Embedding response contains a zero vector')
    return matrix / norms


def embed(cfg, texts):
    payload = json.dumps({'model': cfg['model'], 'input': texts, 'encoding_format': 'float'}).encode()
    for attempt in range(4):
        try:
            req = Request(cfg['url'], data=payload, headers={
                'Authorization': 'Bearer ' + cfg['key'], 'Content-Type': 'application/json'})
            with urlopen(req, timeout=180) as response:
                result = json.load(response)
            break
        except HTTPError as exc:
            # Never print response bodies or request headers, which can contain secrets.
            if exc.code not in (408, 429, 500, 502, 503, 504) or attempt == 3:
                raise RuntimeError(f'Embedding API returned HTTP {exc.code}') from None
        except (URLError, TimeoutError):
            if attempt == 3:
                raise RuntimeError('Embedding API connection failed (network or timeout)') from None
        time.sleep(2 ** attempt)
    rows = result.get('data', [])
    if len(rows) != len(texts) or sorted(row.get('index', -1) for row in rows) != list(range(len(texts))):
        raise ValueError('Embedding response has missing or duplicate row indexes')
    rows.sort(key=lambda row: row['index'])
    matrix = normalize([row['embedding'] for row in rows])
    return matrix, result.get('usage', {})


def build(args, cfg):
    source_bytes = args.source.read_bytes()
    glossary = json.loads(source_bytes)
    entries = glossary['entries']
    if not entries or len({e['id'] for e in entries}) != len(entries):
        raise ValueError('Glossary must have nonempty, unique entry IDs')
    texts = [document(e) for e in entries]
    identity = digest(json.dumps({'source': digest(source_bytes), 'texts': texts,
                                 'model': cfg['model'], 'endpoint': cfg['url']}, sort_keys=True).encode())
    out = args.index
    cache = out / 'batches' / identity
    cache.mkdir(parents=True, exist_ok=True)
    matrices = []
    for start in range(0, len(entries), args.batch_size):
        batch = texts[start:start + args.batch_size]
        # Content-addressed cache makes changes in batch size safe to resume.
        key = digest(json.dumps(batch, ensure_ascii=False).encode())
        path = cache / (key + '.npy')
        if path.exists():
            matrix = np.load(path, allow_pickle=False)
            if len(matrix) != len(batch):
                raise ValueError('Cached batch row count mismatch')
            matrix = normalize(matrix)
        else:
            matrix, usage = embed(cfg, batch)
            with path.with_suffix('.tmp').open('wb') as handle:
                np.save(handle, matrix, allow_pickle=False)
            path.with_suffix('.tmp').replace(path)
            write_json(path.with_suffix('.json'), {'start': start, 'count': len(batch), 'usage': usage})
        matrices.append(matrix)
        print(f'Embedded {min(start + len(batch), len(entries))}/{len(entries)} entries', flush=True)
    matrix = np.concatenate(matrices)
    # Publish immutable version before updating the active pointer.
    version = out / 'versions' / identity
    version.mkdir(parents=True, exist_ok=True)
    with (version / 'vectors.npy').open('wb') as handle:
        np.save(handle, matrix, allow_pickle=False)
    write_json(version / 'records.json', [{'entry': e, 'embedding_text': t} for e, t in zip(entries, texts)])
    write_json(version / 'context.json', {k: v for k, v in glossary.items() if k != 'entries'})
    manifest = {'version': 1, 'built_at_utc': datetime.now(timezone.utc).isoformat(),
                'identity': identity, 'source': str(args.source.resolve()), 'source_sha256': digest(source_bytes),
                'model': cfg['model'], 'endpoint': cfg['url'], 'entry_count': len(entries),
                'alias_count': sum(len(e['aliases']) for e in entries), 'dimensions': matrix.shape[1],
                'dtype': 'float32', 'metric': 'cosine', 'normalized': True,
                'all_aliases_included': True, 'query_instruction': QUERY_INSTRUCTION,
                'vectors_sha256': digest((version / 'vectors.npy').read_bytes()),
                'records_sha256': digest((version / 'records.json').read_bytes())}
    write_json(version / 'manifest.json', manifest)
    write_json(out / 'current.json', {'identity': identity})
    print(json.dumps({'index': str(out), 'entries': len(entries), 'dimensions': matrix.shape[1]}, ensure_ascii=False))


def search(args, cfg):
    pointer = json.loads((args.index / 'current.json').read_text(encoding='utf-8'))
    version = args.index / 'versions' / pointer['identity']
    manifest = json.loads((version / 'manifest.json').read_text(encoding='utf-8'))
    if cfg['model'] != manifest['model'] or cfg['url'] != manifest['endpoint']:
        raise ValueError('Query model/endpoint differs from the index; rebuild or restore configuration')
    for name in ('vectors', 'records'):
        file = version / ('vectors.npy' if name == 'vectors' else 'records.json')
        if digest(file.read_bytes()) != manifest[name + '_sha256']:
            raise ValueError(f'Index integrity check failed: {name}')
    matrix = np.load(version / 'vectors.npy', allow_pickle=False)
    records = json.loads((version / 'records.json').read_text(encoding='utf-8'))
    query, _ = embed(cfg, [manifest['query_instruction'] + args.query])
    if query.shape[1] != matrix.shape[1]:
        raise ValueError('Query and index embedding dimensions differ')
    scores = matrix @ query[0]
    order = np.argsort(-scores)
    results = []
    for i in order:
        entry = records[int(i)]['entry']
        if args.scope and entry['scope'] not in (args.scope, 'universal'):
            continue
        results.append({'score': float(scores[i]), 'entry': entry})
        if len(results) >= args.top_k:
            break
    print(json.dumps({'query': args.query, 'results': results}, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--env', type=Path, default=ROOT / '.env')
    parser.add_argument('--index', type=Path, default=DEFAULT_INDEX)
    sub = parser.add_subparsers(dest='command', required=True)
    b = sub.add_parser('build')
    b.add_argument('--source', type=Path, default=asset_path('data/glossary.json'))
    b.add_argument('--batch-size', type=int, default=32)
    q = sub.add_parser('search')
    q.add_argument('query')
    q.add_argument('--top-k', type=int, default=5)
    q.add_argument('--scope')
    args = parser.parse_args()
    if getattr(args, 'batch_size', 1) < 1 or getattr(args, 'top_k', 1) < 1:
        parser.error('batch-size and top-k must be positive')
    cfg = config(args.env)
    if args.command == 'build':
        build(args, cfg)
    else:
        search(args, cfg)


if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, ValueError, OSError, KeyError) as exc:
        print(f'Error: {exc}', file=sys.stderr)
        sys.exit(1)
