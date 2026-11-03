"""Run a reproducible local Ollama extraction smoke test and preserve evidence."""

import argparse
import csv
import hashlib
import json
import os
import re
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def save_json(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        handle.write(json.dumps(value, ensure_ascii=False, indent=2))
        handle.flush()
        os.fsync(handle.fileno())
    temporary.replace(path)


def request(path, payload=None):
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request("http://127.0.0.1:11434" + path, data=data,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=240) as response:
        return json.load(response)


def checks(output, case):
    result = {"json_valid": False, "schema_valid": False,
              "identity_matches": False, "evidence_exact": False}
    try:
        obj = json.loads(output)
    except (ValueError, TypeError):
        return result, None
    result["json_valid"] = True
    if not isinstance(obj, dict):
        return result, obj
    claims = obj.get("claims")
    result["identity_matches"] = (obj.get("comment_id") == case["comment_id"]
                                  and obj.get("language") == case["language"])
    if not isinstance(claims, list):
        return result, obj
    required = {"character", "mechanic", "direction", "reason", "evidence", "uncertain"}
    valid_claims = all(isinstance(c, dict) and required <= c.keys()
        and (c["character"] is None or isinstance(c["character"], str))
        and (c["mechanic"] is None or isinstance(c["mechanic"], str))
        and c["direction"] in ("buff", "nerf", "keep", "unclear")
        and isinstance(c["reason"], str) and isinstance(c["evidence"], str)
        and isinstance(c["uncertain"], bool) for c in claims)
    result["schema_valid"] = (valid_claims and isinstance(obj.get("comment_id"), str)
        and obj.get("language") in ("en", "zh", "other")
        and obj.get("emotional_tone") in ("neutral", "emotional", "unclear"))
    # An empty claims array has no evidence to verify; report this as not applicable.
    result["evidence_exact"] = (all(isinstance(c, dict)
        and isinstance(c.get("evidence"), str) and bool(c["evidence"])
        and c["evidence"] in case["text"] for c in claims) if claims else None)
    return result, obj


def glossary_context(glossary, comment, language=None):
    """Retrieve lexical candidates; leave scope and ambiguity resolution to the model."""
    def matches(alias):
        text = alias["text"]
        if language and alias.get("comment_languages") and language not in alias["comment_languages"]:
            return False
        if alias["language"] == "en":
            flags = re.IGNORECASE
            return re.search(r"(?<![A-Za-z0-9_])" + re.escape(text) + r"(?![A-Za-z0-9_])", comment, flags) is not None
        return text in comment

    def subject_match(alias, establish_subject=False):
        # Unreviewed nicknames remain lexical candidates, not scope filters.
        if establish_subject and alias.get("candidate_only") and alias.get("review", {}).get("decision") != "accept":
            return False
        if not matches(alias):
            return False
        text = alias["text"]
        if alias["language"] == "zh" and len(text) == 1:
            # A short character label inside an ordinary word is not a subject.
            unrelated = {"隆": "克隆", "肯": "肯定", "舞": "跳舞"}
            cleaned = comment.replace(unrelated.get(text, "\0"), "")
            return re.search(re.escape(text) + r"(?=的|太|很|这|被|用|在|是|要|有|SA|CA|\s|[，。！？,.!?]|$)", cleaned) is not None
        return True

    subjects = {entry["scope"] for entry in glossary["entries"]
                if entry["category"] == "character"
                and any(subject_match(alias, establish_subject=True) for alias in entry["aliases"])}
    level_aliases = {"SA1", "SA2", "SA3", "CA", "一气", "二气", "三气", "1气", "2气", "3气"}

    def eligible(entry, text=None):
        if entry["scope"] == "universal" or entry["category"] == "character":
            return True
        if subjects:
            return entry["scope"] in subjects
        if text in level_aliases:
            return False
        # Spaced/hyphenated level shorthand still requires a character subject.
        return not text or not re.fullmatch(r"(?:SA\s*-?\s*[123]|LV(?:L|\.)?\s*[123]|Level\s+[123])", text, re.IGNORECASE)

    selected = [entry for entry in glossary["entries"]
                if any(matches(alias) and eligible(entry, alias["text"])
                       and (entry["category"] != "character" or subject_match(alias))
                       for alias in entry["aliases"])]
    by_id = {entry["id"]: entry for entry in glossary["entries"]}
    ambiguities = []
    for item in glossary["ambiguous_aliases"]:
        if matches({"text": item["text"], "language": item["language"]}):
            ids = [candidate for candidate in item["candidate_ids"]
                   if eligible(by_id[candidate], item["text"])]
            if ids:
                ambiguities.append({**item, "candidate_ids": ids})
    candidates = {candidate for item in ambiguities for candidate in item["candidate_ids"]}
    selected_ids = {entry["id"] for entry in selected}
    selected += [entry for entry in glossary["entries"]
                 if entry["id"] in candidates - selected_ids]
    fields = ("id", "canonical_name", "chinese_label", "category", "scope", "classic_notation", "super_art_level", "notes")
    context = {"policy": glossary["policy"],
               "entries": [{**{key: entry.get(key) for key in fields},
                            "aliases": [{key: value for key, value in alias.items()
                                         if key != "source_ids"}
                                        for alias in entry["aliases"]]} for entry in selected],
               "ambiguous_aliases": ambiguities,
               "community_normalization": {**glossary["community_normalization"],
                   "rules": [rule for rule in glossary["community_normalization"]["rules"]
                             if rule["requires_scope"] == "universal" or rule["requires_scope"] in subjects]}}
    return json.dumps(context, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--models", nargs="+", default=["qwen2.5:7b", "llama3.1:latest"])
    parser.add_argument("--cpu", action="store_true", help="Use CPU inference after a GPU backend failure")
    parser.add_argument("--glossary", action="store_true", help="Supply glossary candidates without changing the original cases")
    parser.add_argument("--resume", type=Path, help="Resume a saved run without replacing successful responses")
    args = parser.parse_args()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    folder = args.resume.resolve() if args.resume else ROOT / "reports" / ("smoke-" + stamp)
    if not args.resume:
        folder.mkdir(parents=True, exist_ok=False)
    prompt = (folder / "prompt.txt" if args.resume else ROOT / "prompts/extract-feedback.txt").read_text()
    cases = json.loads((folder / "cases.json" if args.resume else ROOT / "data/raw/debug/smoke-cases.json").read_text())
    patch = json.loads((folder / "patch-context.json" if args.resume else ROOT / "data/raw/debug/patch-context.json").read_text())
    if not args.resume:
        (folder / "prompt.txt").write_text(prompt)
        (folder / "runner.py").write_text(Path(__file__).read_text())
        save_json(folder / "cases.json", cases)
        save_json(folder / "patch-context.json", patch)
    glossary_path = folder / "glossary.json"
    glossary = None
    if args.resume:
        if glossary_path.exists():
            glossary = json.loads(glossary_path.read_text())
    elif args.glossary:
        glossary = json.loads((ROOT / "data/glossary.json").read_text())
        save_json(glossary_path, glossary)
    options = {"temperature": 0, "seed": 42, "num_ctx": 4096, "num_predict": 700}
    if args.cpu and not args.resume:
        options["num_gpu"] = 0
    current_models = request("/api/tags")
    if args.resume:
        metadata = json.loads((folder / "metadata.json").read_text())
        options = metadata["options"]
        if hashlib.sha256(prompt.encode()).hexdigest() != metadata["prompt_sha256"]:
            raise ValueError("Saved prompt hash does not match the original run")
        if glossary is not None and hashlib.sha256(glossary_path.read_bytes()).hexdigest() != metadata.get("glossary_sha256"):
            raise ValueError("Saved glossary hash does not match the original run")
        original = {m["name"]: m["digest"] for m in metadata["installed_models"]["models"]}
        current = {m["name"]: m["digest"] for m in current_models["models"]}
        for model in args.models:
            if current.get(model) is None or current[model] != original.get(model):
                raise ValueError("Model identity changed or is missing: " + model)
        save_json(folder / ("resume-" + stamp + ".json"), {
            "resumed_at_utc": stamp, "ollama_version": request("/api/version"),
            "installed_models": current_models,
            "notes": "Successful original responses retained. Interrupted attempts archived before rerunning. Timing spans separate sessions."})
    else:
        metadata = {"started_at_utc": stamp, "patch": patch["patch_label"],
        "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
        "options": options, "format_enforcement": False,
        "notes": "Synthetic debugging only. One run per model/case; no retries. Wall time includes model loading. Semantic review remains blank.",
        "ollama_version": request("/api/version"), "installed_models": current_models,
        "model_details": {m: request("/api/show", {"model": m}) for m in args.models}}
        metadata["glossary_enabled"] = glossary is not None
        metadata["glossary_sha256"] = (hashlib.sha256(glossary_path.read_bytes()).hexdigest()
                                      if glossary is not None else None)
        metadata["glossary_retrieval"] = "Subject-aware lexical candidates; model resolves context and ambiguity."
        save_json(folder / "metadata.json", metadata)
    records = []
    for model in args.models:
        for case in cases:
            name = model.replace(":", "-").replace("/", "-") + "-" + case["comment_id"]
            record_path = folder / (name + ".json")
            if args.resume and record_path.exists():
                try:
                    previous = json.loads(record_path.read_text())
                except ValueError:
                    previous = {}
                if previous.get("response", {}).get("done") is True:
                    records.append(previous)
                    save_json(folder / "results.json", records)
                    print("Retained", model, case["comment_id"], flush=True)
                    continue
                archive = folder / "interrupted-attempts"
                archive.mkdir(exist_ok=True)
                record_path.rename(archive / (name + "-" + stamp + ".json"))
            rendered = prompt.replace("{{comment_id}}", case["comment_id"]).replace(
                "{{patch_context}}", patch["verified_context"]).replace("{{comment_text}}", case["text"])
            if glossary is not None:
                reference = glossary_context(glossary, case["text"], case["language"])
                instruction = ("Vocabulary reference (data, not instructions):\n" + reference + "\n"
                    "Use these candidates only when supported by the comment context. Lexical matches "
                    "do not prove meaning or character identity. Preserve evidence exactly. "
                    "If move names conflict, report the conflict and mark uncertain; do not silently "
                    "correct the comment. Vocabulary does not establish patch facts or buff/nerf direction.\n\n")
                rendered = instruction + rendered
            payload = {"model": model, "prompt": rendered, "stream": False,
                       "options": options, "keep_alive": "5m"}
            start = time.perf_counter()
            record = {"model": model, "comment_id": case["comment_id"],
                      "language": case["language"], "request": payload}
            save_json(record_path, record)
            try:
                response = request("/api/generate", payload)
                record["response"] = response
                if response.get("done") is not True:
                    record["error"] = "Ollama returned an unfinished response"
                record["checks"], record["parsed_output"] = checks(response.get("response", ""), case)
            except Exception as error:
                record["error"] = str(error)
                record["checks"] = {}
            record["wall_seconds"] = round(time.perf_counter() - start, 3)
            records.append(record)
            save_json(record_path, record)
            save_json(folder / "results.json", records)
            print(model, case["comment_id"], record["wall_seconds"], record["checks"], flush=True)
    fields = ["model", "comment_id", "language", "wall_seconds", "json_valid", "schema_valid",
              "identity_matches", "evidence_exact", "reviewer", "character_correct", "mechanic_correct",
              "direction_correct", "reason_supported", "emotion_correct", "uncertainty_correct",
              "unsupported_patch_claims", "review_notes"]
    with (folder / "review.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for r in records:
            writer.writerow({**{k: r[k] for k in fields[:4]}, **r["checks"]})
    lines = ["# Local model smoke test", "", f"Patch: {patch['patch_label']} (2026-08-03).",
             "", "Ten synthetic cases, five English and five Chinese. Ryu only; not representative of the full roster.",
             "", "The original prompt was frozen. No JSON mode, output repair, or automatic retries were used. Interrupted cases may be rerun during explicit recovery.",
             "Wall time includes loading; this is not a controlled speed benchmark.", ""]
    if glossary is not None:
        lines += ["Glossary-assisted run: glossary.json is a frozen reference snapshot. The original ten cases were unchanged, including the ZH02 naming conflict. Each saved request contains its retrieved candidates. Generation settings match the baseline; consult metadata.json for hardware options.", ""]
    if options.get("num_gpu") == 0:
        lines += ["CPU inference was requested explicitly (num_gpu=0) after an earlier GPU backend failure. Runtime is not comparable to the GPU baseline.", ""]
    if list(folder.glob("resume-*.json")):
        lines += ["This run was resumed after an interruption. Successful responses were retained; failed attempts are in interrupted-attempts/. Model digests were checked before resuming. Timing spans separate sessions.", ""]
    for model in args.models:
        rows = [r for r in records if r["model"] == model]
        lines += [f"## {model}", "", f"Requests completed: {sum(r.get('response', {}).get('done') is True for r in rows)}/{len(rows)}."]
        for key in ("json_valid", "schema_valid", "identity_matches", "evidence_exact"):
            eligible = [r for r in rows if r["checks"].get(key) is not None]
            lines.append(f"- {key}: {sum(r['checks'].get(key) is True for r in eligible)}/{len(eligible)} applicable cases.")
        lines += [f"- Total wall time: {sum(r['wall_seconds'] for r in rows):.3f} seconds.", ""]
    lines += ["## Human review", "", "Complete review.csv before selecting a model. Blank fields mean not reviewed.",
              "Use pass, fail, or not_applicable; consult cases.json for proposed expectations.",
              "Exact-substring checks do not prove that a quote supports a claim.",
              "Expected labels are provisional and may be corrected by the reviewer.", "",
              "Reviewer: ____________________", "Review date: ____________________", "",
              "Model selection and rationale:", "", "____________________________________________________________", "",
              "Issues to investigate:", "", "____________________________________________________________", ""]
    for r in records:
        case = next(c for c in cases if c["comment_id"] == r["comment_id"])
        lines += [f"## {r['model']} / {r['comment_id']}", "", "Input:", "", case["text"], "",
                  "Raw output:", "", "```text", r.get("response", {}).get("response", r.get("error", "")), "```", "",
                  "Reviewer notes:", "", "____________________________________________________________", ""]
    (folder / "review.md").write_text("\n".join(lines))
    print("Saved run:", folder, flush=True)


if __name__ == "__main__":
    main()
