"""Prepare unannotated development labels for a CLI evaluation demonstration."""
import argparse
import hashlib
import json
from pathlib import Path
import re

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("input", type=Path)
parser.add_argument("output", type=Path)
args = parser.parse_args()
rows = [json.loads(line) for line in args.input.read_text(encoding="utf-8").splitlines() if line.strip()]
labels = []
for row in rows:
    text = row["text_original"]
    labels.append({
        "comment_id": row["record_id"], "language": row["language"],
        "text_original": text, "source_url": row.get("source_url"),
        "content_sha256": hashlib.sha256(text.encode()).hexdigest(),
        "cluster_id": hashlib.sha256(re.sub(r"\W+", "", text.casefold()).encode()).hexdigest(),
        "split": "development", "source_stage": "raw_pre_screen",
        "reviewer_type": "unlabeled", "relevance": None, "segments": None,
        "points": None, "point_matches": None,
        "notes": "CLI demonstration only; unannotated, not ground truth.",
    })
with args.output.open("x", encoding="utf-8") as stream:
    json.dump(labels, stream, ensure_ascii=False, indent=2)
    stream.write("\n")
