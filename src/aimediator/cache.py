"""Content-addressed cache of model responses and embeddings shared across runs (plan 4.6, UP-D09)."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .common import sha, write


def chat_key(payload: dict[str, Any], model_digest: str | None, service_version: str | None,
             request_context: dict[str, Any] | None = None) -> str:
    """Return the shared key of a chat request: the payload with stream false, the model digest and the service version.

    The run identity is not part of it. request_context (the quality attempt) is, when given, because two
    attempts may send the same bytes and must not share one answer.
    """
    material = {'payload': {**payload, 'stream': False}, 'model_digest': model_digest,
                'service_version': service_version}
    if request_context is not None:
        material['request_context'] = request_context
    return sha(json.dumps(material, sort_keys=True, ensure_ascii=False).encode())


def embedding_key(model: str, endpoint: str | None, text: str, model_digest: str | None) -> str:
    """Return the shared key of one embedded text: model, endpoint, text and model digest."""
    return sha(json.dumps({'model': model, 'endpoint': endpoint, 'text': text, 'model_digest': model_digest},
                          sort_keys=True, ensure_ascii=False).encode())


def storable(response: dict[str, Any]) -> bool:
    """Return whether a journaled response may enter the cache: a finished generation without an error."""
    result = response.get('response') if isinstance(response, dict) else None
    return isinstance(result, dict) and result.get('done') is True and result.get('done_reason') == 'stop' \
        and not result.get('error') and isinstance(result.get('message'), dict)


class SharedCache:
    """Responses under chat/<key[:2]>/<key>/ and embedding records under embedding/<key[:2]>/<key>.json."""

    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)

    def _chat(self, key: str) -> Path:
        return self.root / 'chat' / key[:2] / key

    def lookup(self, key: str, request: dict[str, Any] | None = None) -> dict[str, Any] | None:
        """Return the stored response of a key, or None when it is missing, unreadable or for another request."""
        folder = self._chat(key)
        try:
            response = json.loads((folder / 'response.json').read_text(encoding='utf-8'))
            stored = json.loads((folder / 'request.json').read_text(encoding='utf-8'))
        except (OSError, ValueError):
            return None
        if request is not None and stored != request:
            return None
        return response if storable(response) else None

    def store(self, key: str, request: dict[str, Any], response: dict[str, Any]) -> None:
        """Store a finished response under its key; other responses are not stored."""
        if not storable(response):
            return
        folder = self._chat(key)
        write(folder / 'request.json', request)
        write(folder / 'response.json', response)

    def _embedding(self, key: str) -> Path:
        return self.root / 'embedding' / key[:2] / (key + '.json')

    def lookup_embedding(self, key: str) -> dict[str, Any] | None:
        """Return the stored embedding record of a key, or None."""
        try:
            return json.loads(self._embedding(key).read_text(encoding='utf-8'))
        except (OSError, ValueError):
            return None

    def store_embedding(self, key: str, record: dict[str, Any]) -> None:
        """Store one embedding record (model, text and vector) under its key."""
        write(self._embedding(key), record)
