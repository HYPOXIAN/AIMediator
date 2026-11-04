"""Resumable record store of a collection run: records, checkpoint and configuration snapshot."""
import hashlib
import json
import os

from ..common import write as write_json
from .client import utc_now


class Store:
    def __init__(self, directory, config):
        self.directory = directory
        directory.mkdir(parents=True, exist_ok=True)
        self.config = config
        signature = hashlib.sha256(json.dumps(config, sort_keys=True).encode()).hexdigest()
        self.path = directory / "records.jsonl"
        self.rows = [json.loads(line) for line in self.path.read_text(encoding="utf-8").splitlines()] if self.path.exists() else []
        self.ids = {row["record_id"] for row in self.rows}
        state_path = directory / "checkpoint.json"
        self.state = json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else {"config_hash": signature, "streams": {}, "started_at": utc_now(), "youtube_quota_used": 0}
        if self.state["config_hash"] != signature:
            raise ValueError("Configuration changed; use a new output directory")
        if not (directory / "config-snapshot.json").exists():
            write_json(directory / "config-snapshot.json", config)

    def count(self, platform, language):
        return sum(r["platform"] == platform and r["language"] == language for r in self.rows)

    def complete(self, platform):
        return all(self.count(platform, lang) >= n for lang, n in self.config[platform]["targets"].items())

    def add(self, platform, source_id, text, language, source_url, **metadata):
        identity = f"{platform}:{source_id}"
        if identity in self.ids:
            return False
        self.ids.add(identity)
        self.rows.append({"record_id": identity, "platform": platform, "source_id": str(source_id), "text_original": text, "language": language, "source_url": source_url, "retrieved_at_utc": utc_now(), "target_patch_context": self.config["target_patch_context"], "patch_relevance": "unreviewed", "content_review": "not_performed", "reviewer": "", "decision": "", "notes": "", **metadata})
        return True

    def save(self):
        temporary = self.path.with_suffix(".jsonl.tmp")
        with temporary.open("w", encoding="utf-8") as stream:
            for row in self.rows:
                stream.write(json.dumps(row, ensure_ascii=False) + "\n")
            stream.flush()
            os.fsync(stream.fileno())
        temporary.replace(self.path)
        write_json(self.directory / "checkpoint.json", self.state)
