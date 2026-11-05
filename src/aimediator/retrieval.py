"""Embedding retrieval of comments against the packaged topic anchors."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

import numpy as np
from . import glossary_vectors
from .common import sha as digest, write as write_json
from .inference import api
from .resources import anchors, asset_path

BATCH = 32


def text_identity(model: str, endpoint: str | None, text: str) -> str:
    """Return the file name stem of one embedding record: the SHA-256 of model, endpoint and text."""
    return digest(json.dumps({'model': model, 'endpoint': endpoint, 'text': text},
                             sort_keys=True, ensure_ascii=False).encode())


def embedding_key(model: str, endpoint: str | None, text: str, model_digest: str | None) -> str:
    """Return the shared-cache key of one embedded text: model, endpoint, text and model digest."""
    return digest(json.dumps({'model': model, 'endpoint': endpoint, 'text': text, 'model_digest': model_digest},
                             sort_keys=True, ensure_ascii=False).encode())


def near_duplicate_clusters(ids: list[str], vectors: Any, threshold: float, block: int = 512) -> list[dict[str, Any]]:
    """Return the single-linkage clusters of comments whose unit vectors have a cosine at or above threshold.

    Each cluster (at least two comments) holds its sorted `comment_ids`, the linking `pairs` (the two IDs
    and the cosine, rounded to 6 places) and `members` with each member's highest cosine to another member;
    clusters are ordered by their first comment ID (plan 4.9, U6.5, UP-D14).
    """
    parent = list(range(len(ids)))

    def root(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i
    pairs = []
    for start in range(0, len(ids), block):
        scores = vectors[start:start + block] @ vectors.T
        for offset, row in enumerate(scores):
            i = start + offset
            for j in np.nonzero(row >= threshold)[0]:
                j = int(j)
                if j > i:
                    pairs.append((i, j, round(float(row[j]), 6)))
                    parent[root(j)] = root(i)
    groups = {}
    for i in range(len(ids)):
        groups.setdefault(root(i), []).append(i)
    best = {}
    for i, j, cosine in pairs:
        best[i] = max(best.get(i, cosine), cosine)
        best[j] = max(best.get(j, cosine), cosine)
    clusters = []
    for members in groups.values():
        if len(members) < 2:
            continue
        inside = set(members)
        clusters.append({'comment_ids': sorted(ids[i] for i in members),
            'max_cosine': max(c for i, j, c in pairs if i in inside),
            'members': [{'comment_id': ids[i], 'max_cosine': best[i]} for i in sorted(members, key=lambda k: ids[k])],
            'pairs': [{'comment_ids': sorted((ids[i], ids[j])), 'cosine': c}
                      for i, j, c in sorted(pairs, key=lambda p: sorted((ids[p[0]], ids[p[1]]))) if i in inside]})
    clusters.sort(key=lambda c: c['comment_ids'][0])
    for number, cluster in enumerate(clusters, 1):
        cluster['cluster_id'] = 'D' + str(number)
    return [{'cluster_id': c.pop('cluster_id'), **c} for c in clusters]


def retrieve(rows: list[dict[str, Any]], base: str, folder: Path, model: str,
             embedding_config: dict[str, Any] | None = None,
             api_transport: Callable[..., dict[str, Any]] | None = None,
             embed_transport: Callable[..., tuple[Any, Any]] | None = None,
             log: Callable[[str], None] | None = None, shared_cache: Any = None,
             model_digest: str | None = None) -> list[dict[str, Any]]:
    """Embed the anchors and comments, one record per text under embeddings/, score each comment, write retrieval.json.

    A record is embeddings/<SHA-256 of model, endpoint and text>.json with the model, the text and its vector.
    Only texts without a record are embedded, in batches of BATCH in input order; a shared cache (plan 4.6,
    UP-D09) supplies records keyed with the model digest before the service is asked, and keeps new ones.
    """
    instruction = 'Instruct: Retrieve the description matching the topic and intent of this Street Fighter 6 player comment.\nQuery: '
    positive_anchors, negative_anchors = anchors()
    topics = positive_anchors + negative_anchors
    texts = topics + [instruction + r['text_original'] for r in rows]
    endpoint = embedding_config['url'] if embedding_config else base
    records, missing, queued = {}, [], set()
    for text in texts:
        if text in records or text in queued:
            continue
        path = folder / 'embeddings' / (text_identity(model, endpoint, text) + '.json')
        if path.exists():
            records[text] = json.loads(path.read_text(encoding='utf-8'))
            continue
        shared = shared_cache.lookup_embedding(embedding_key(model, endpoint, text, model_digest)) \
            if shared_cache is not None else None
        if shared is not None and shared.get('model') == model and shared.get('text') == text:
            record = {'model': model, 'text': text, 'vector': shared['vector']}
            write_json(path, record)
            records[text] = record
        else:
            missing.append(text)
            queued.add(text)
    for start in range(0, len(missing), BATCH):
        batch = missing[start:start + BATCH]
        if embedding_config:
            vectors, usage = (embed_transport or glossary_vectors.embed)(embedding_config, batch)
            result = {'embeddings': vectors.tolist()}
        else:
            result = (api_transport or api)(base, '/api/embed', {'model': model, 'input': batch,
                                           'truncate': False, 'keep_alive': '10m'})
        if not isinstance(result.get('embeddings'), list) or len(result['embeddings']) != len(batch):
            raise ValueError('Invalid embedding matrix')
        for text, vector in zip(batch, result['embeddings']):
            record = {'model': model, 'text': text, 'vector': vector}
            write_json(folder / 'embeddings' / (text_identity(model, endpoint, text) + '.json'), record)
            if shared_cache is not None:
                shared_cache.store_embedding(embedding_key(model, endpoint, text, model_digest), record)
            records[text] = record
        if log is not None:
            log(f'Embedding {min(start + BATCH, len(missing))}/{len(missing)}')
    matrix = np.asarray([records[text]['vector'] for text in texts], dtype=np.float32)
    if matrix.ndim != 2 or len(matrix) != len(texts) or not np.isfinite(matrix).all():
        raise ValueError('Invalid embedding matrix')
    norm = np.linalg.norm(matrix, axis=1, keepdims=True)
    if (norm == 0).any():
        raise ValueError('Zero embedding vector')
    matrices = [matrix / norm]
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
                            'text': topics[int(i)], 'cosine': float(scores[i]),
                            'class': 'related' if i < 10 else 'unrelated'} for i in order[:4]]})
    write_json(folder / 'retrieval.json', decisions)
    policy = json.loads(asset_path('configs/balance-review-policy.json').read_text(encoding='utf-8'))
    threshold = policy['near_duplicate_cosine']
    write_json(folder / 'near-duplicates.json', {'schema_version': 'near-duplicates-v1',
        'policy_version': policy['version'], 'near_duplicate_cosine': threshold, 'linkage': 'single',
        'comments': len(rows), 'note': 'Annotation only: no admission, claim or report count changes.',
        'clusters': near_duplicate_clusters([r['record_id'] for r in rows], vectors[20:], threshold)})
    return decisions
