"""Strict UTF-8 persistence and public failures."""
from __future__ import annotations

from typing import Any, NoReturn
import hashlib
import json
import os
from pathlib import Path
import math


def strict_json(raw: str | bytes) -> Any:
    """Parse JSON text, rejecting duplicate keys and non-finite numbers with ValueError."""
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError("Duplicate JSON key: " + key)
            result[key] = value
        return result
    def reject(value: str) -> NoReturn:
        raise ValueError("Non-finite JSON value: " + value)
    def number(value: str) -> float:
        parsed = float(value)
        if not math.isfinite(parsed):
            return reject(value)
        return parsed
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=reject, parse_float=number)


class Failure(Exception):
    """A public failure that carries the CLI exit code and the message shown to the user."""

    def __init__(self, code: int, message: str) -> None:
        self.code, self.message = code, message
        super().__init__(message)


def canonical(value: Any) -> bytes:
    """Return the canonical UTF-8 JSON bytes of a value: sorted keys, compact separators, no NaN."""
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8')


def sha(value: bytes) -> str:
    """Return the hexadecimal SHA-256 digest of bytes."""
    return hashlib.sha256(value).hexdigest()


def read(path: str | Path) -> Any:
    """Read a UTF-8 JSON file with strict_json."""
    return strict_json(Path(path).read_text(encoding='utf-8'))


def write(path: str | Path, value: Any) -> None:
    """Write a value as indented UTF-8 JSON through a synced temporary file, creating missing parents."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + '.tmp')
    with temp.open('w', encoding='utf-8') as f:
        f.write(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n')
        f.flush()
        os.fsync(f.fileno())
    temp.replace(path)


def new_path(path: str | Path, source: str | Path | None = None) -> Path:
    """Resolve an output path that does not exist yet, lies apart from the source run and has a writable parent."""
    path = Path(path).resolve()
    if path.exists():
        raise Failure(4, 'Output already exists; choose a new path')
    if source:
        source = Path(source).resolve()
        if path == source or source in path.parents or path in source.parents:
            raise Failure(4, 'Derived output must be separate from the source run')
    parent = path.parent
    while not parent.exists():
        parent = parent.parent
    if not parent.is_dir() or not os.access(parent, os.W_OK | os.X_OK):
        raise Failure(2, 'Output parent is not writable')
    return path


def input_rows(raw: bytes) -> list[dict[str, Any]]:
    """Parse UTF-8 JSONL input into rows with unique record IDs, or raise Failure(2)."""
    rows, seen = [], set()
    try:
        lines = raw.decode('utf-8').splitlines()
    except UnicodeError:
        raise Failure(2, 'Input must be UTF-8 JSONL') from None
    for line_no, line in enumerate(lines, 1):
        if not line.strip():
            continue
        try:
            row = strict_json(line)
            if not isinstance(row, dict):
                raise ValueError()
            for key in ('record_id', 'text_original', 'language'):
                if not isinstance(row.get(key), str) or not row[key].strip():
                    raise ValueError()
            if row['record_id'] in seen:
                raise ValueError()
        except (ValueError, TypeError):
            raise Failure(2, 'Invalid input at line %d: strict JSON object, nonempty string fields and unique record_id required' % line_no) from None
        seen.add(row['record_id'])
        rows.append(row)
    if not rows:
        raise Failure(2, 'Input dataset is empty')
    if not any(r['language'] in ('en', 'zh') for r in rows):
        raise Failure(2, 'No input records have a supported en/zh route')
    return rows
