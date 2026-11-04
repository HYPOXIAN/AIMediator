"""Embedding retrieval of comments against the packaged topic anchors."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

import numpy as np
from . import glossary_vectors
from .common import sha as digest, write as write_json
from .inference import api
from .resources import anchors


def retrieve(rows: list[dict[str, Any]], base: str, folder: Path, model: str,
             embedding_config: dict[str, Any] | None = None,
             api_transport: Callable[..., dict[str, Any]] | None = None,
             embed_transport: Callable[..., tuple[Any, Any]] | None = None,
             log: Callable[[str], None] | None = None) -> list[dict[str, Any]]:
    """Embed the anchors and comments, cached under embeddings/, score each comment and write retrieval.json."""
    instruction = 'Instruct: Retrieve the description matching the topic and intent of this Street Fighter 6 player comment.\nQuery: '
    positive_anchors, negative_anchors = anchors()
    topics = positive_anchors + negative_anchors
    texts = topics + [instruction + r['text_original'] for r in rows]
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
        if log is not None:
            log(f'Embedding {min(start + 8, len(texts))}/{len(texts)}')
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
    return decisions
