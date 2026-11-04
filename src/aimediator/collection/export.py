"""Export of a collection run: summary, request log, language and platform views, and the review sheet."""
import collections
import json

from ..common import write as write_json
from .client import utc_now


def export(store, statuses, client):
    counts = {platform: dict(collections.Counter(r["language"] for r in store.rows if r["platform"] == platform)) for platform in ["steam", "bluesky", "youtube"]}
    totals = dict(collections.Counter(r["language"] for r in store.rows))
    summary = {"updated_at_utc": utc_now(), "counts": counts, "total_by_language": totals, "total_records": len(store.rows), "statuses": statuses, "requests_this_invocation": dict(client.calls), "content_filtering": False, "patch_filtering": False, "language_labels": "Platform/author labels and script heuristics are provisional, not manual verification", "youtube_policy": "Collection only; refresh/delete non-authorized API data within 30 days. No model analysis or derived metrics performed.", "network_guarantee": "Conservative budgets reduce load but cannot guarantee freedom from IP restrictions."}
    write_json(store.directory / "summary.json", summary)
    log_path = store.directory / "request-log.json"
    previous_events = json.loads(log_path.read_text(encoding="utf-8")) if log_path.exists() else []
    write_json(log_path, previous_events + client.events)
    for language in ("en", "zh"):
        path = store.directory / ("english.jsonl" if language == "en" else "chinese.jsonl")
        with path.open("w", encoding="utf-8") as stream:
            for row in store.rows:
                if row["language"] == language:
                    stream.write(json.dumps(row, ensure_ascii=False) + "\n")
    for platform in ("steam", "bluesky", "youtube"):
        source_rows = [row for row in store.rows if row["platform"] == platform]
        if source_rows:
            with (store.directory / (platform + ".jsonl")).open("w", encoding="utf-8") as stream:
                for row in source_rows:
                    stream.write(json.dumps(row, ensure_ascii=False) + "\n")
    lines = ["# Feedback Collection Run", "", "Original text retained; no semantic, sentiment, patch, or character filtering performed.", "", f"Total records: {len(store.rows)}. Provisional English: {totals.get('en', 0)}. Provisional Chinese: {totals.get('zh', 0)}.", ""]
    for platform, status in statuses.items():
        lines += [f"## {platform}", "", f"Status: {status}", f"Language counts: {json.dumps(counts[platform], ensure_ascii=False)}", ""]
    lines += ["## Human review", "", "Reviewer:", "Decision:", "Language count verification:", "Patch applicability:", "Notes:", "", "API access and conservative rate limits do not guarantee complete coverage or prevent all network restrictions. No claim is made that all records are substantive game reviews. Source URLs can identify their original public authors. Record provenance and retention limits in the dataset's manifest.json (RULES.md P1)."]
    (store.directory / "review.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)
