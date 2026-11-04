import argparse
import collections
import datetime as dt
import email.utils
import hashlib
import fcntl
import json
import os
from pathlib import Path
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src'))
from aimediator.common import write as write_json
from aimediator.resources import workspace_root
from aimediator.collection.client import HOSTS, Client, Halt, RestrictedRedirect, load_youtube_key, retry_delay, utc_now
from aimediator.collection.store import Store

ROOT = workspace_root()
STATE = workspace_root() / "runs/state"  # collector lock and HTTP state; runtime state stays out of data/ (RULES.md P1)


def guess_language(text):
    if re.search(r"[\u3040-\u30ff]", text):
        return "ja"
    if re.search(r"[\uac00-\ud7af]", text):
        return "ko"
    if len(re.findall(r"[\u4e00-\u9fff]", text)) >= 2:
        return "zh"
    if len(re.findall(r"\b[A-Za-z]+\b", text)) >= 3:
        return "en"
    return "und"


def timestamp(value):
    return dt.datetime.fromtimestamp(int(value), dt.timezone.utc).isoformat() if value else None


def steam(client, store, settings):
    for language, goal in settings["targets"].items():
        key = "steam:" + language
        state = store.state["streams"].setdefault(key, {"cursor": "*", "done": False})
        while store.count("steam", language) < goal and not state["done"]:
            params = {"appid": store.config["app_id"], "languages": [settings["languages"][language]], "filter": 1, "review_type": 0, "purchase_type": 1, "filter_offtopic_activity": False, "num_per_page": min(100, goal - store.count("steam", language)), "cursor": state["cursor"]}
            if store.config["date_start"] and store.config["date_end"]:
                params.update(date_range_start=int(dt.datetime.fromisoformat(store.config["date_start"]).timestamp()), date_range_end=int(dt.datetime.fromisoformat(store.config["date_end"]).timestamp()))
            response = client.get("https://api.steampowered.com/IUserReviewsService/GetAppReviews/v1/", {"input_json": json.dumps(params)}, "steam", settings)
            data = response.get("response", response)
            if "reviews" not in data:
                raise Halt("Steam response schema changed; no cursor advanced")
            before = len(store.rows)
            for item in data["reviews"]:
                author = item.get("author", {})
                steam_id = author.get("steamid")
                url = f"https://steamcommunity.com/profiles/{steam_id}/recommended/{store.config['app_id']}/" if steam_id else f"https://store.steampowered.com/app/{store.config['app_id']}/#app_reviews_hash"
                raw_lang = item.get("language", "unknown")
                normalized = {"english": "en", "schinese": "zh", "tchinese": "zh"}.get(raw_lang, "und")
                store.add("steam", item["recommendationid"], item.get("review", ""), normalized, url, content_type="user_review", language_method="platform_label_unverified", language_original=raw_lang, created_at_utc=timestamp(item.get("timestamp_created")), updated_at_utc=timestamp(item.get("timestamp_updated")), voted_up=item.get("voted_up"), votes_up=item.get("votes_up"), playtime_at_review_minutes=author.get("playtime_at_review"), query_language=language, access_method="official_public_api", source_type="observed", retrieval_order="recent", context={"app_id": store.config["app_id"], "title": "Street Fighter 6"})
            cursor = data.get("cursor")
            state["done"] = not data["reviews"] or not cursor or cursor == state["cursor"] or len(store.rows) == before
            state["stop_reason"] = "no_progress_or_exhausted" if state["done"] else None
            state["cursor"] = cursor
            store.save()
            print(json.dumps({"platform": "steam", "language": language, "saved": store.count("steam", language), "goal": goal}), flush=True)


def bluesky(client, store, settings):
    token = os.environ.get("BLUESKY_ACCESS_TOKEN")
    endpoint = "https://bsky.social/xrpc/app.bsky.feed.searchPosts" if token else "https://public.api.bsky.app/xrpc/app.bsky.feed.searchPosts"
    headers = {"Authorization": "Bearer " + token} if token else {}
    for language, queries in settings["queries"].items():
        for query in queries:
            key = "bluesky:" + language + ":" + query
            state = store.state["streams"].setdefault(key, {"cursor": None, "done": False})
            while store.count("bluesky", language) < settings["targets"][language] and not state["done"]:
                params = {"q": query, "lang": language, "sort": "latest", "limit": 100}
                if state["cursor"]:
                    params["cursor"] = state["cursor"]
                for name, field in [("since", "date_start"), ("until", "date_end")]:
                    if store.config[field]:
                        params[name] = store.config[field]
                data = client.get(endpoint, params, "bluesky", settings, headers=headers)
                if "posts" not in data:
                    raise Halt("Bluesky response schema changed; no cursor advanced")
                before = len(store.rows)
                for item in data["posts"]:
                    record = item.get("record", {})
                    text = record.get("text", "")
                    tags = record.get("langs", [])
                    lang = "zh" if any(x.startswith("zh") for x in tags) else "en" if "en" in tags else guess_language(text)
                    uri = item["uri"]
                    parts = uri.split("/")
                    url = f"https://bsky.app/profile/{parts[2]}/post/{parts[-1]}"
                    store.add("bluesky", uri, text, lang, url, content_type="post", language_method="author_label_unverified" if tags else "script_heuristic_unverified", language_original=tags, created_at_utc=record.get("createdAt"), parent_id=record.get("reply", {}).get("parent", {}).get("uri"), root_id=record.get("reply", {}).get("root", {}).get("uri"), like_count=item.get("likeCount"), access_method="official_api", source_type="observed", retrieval_order="latest", discovery_query=query)
                cursor = data.get("cursor")
                state["done"] = not data["posts"] or not cursor or cursor == state["cursor"] or len(store.rows) == before
                state["cursor"] = cursor
                store.save()
                print(json.dumps({"platform": "bluesky", "language": language, "saved": store.count("bluesky", language)}), flush=True)


def youtube(client, store, settings):
    key = os.environ.get("YOUTUBE_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        raise Halt("Missing YOUTUBE_API_KEY; no YouTube request sent")
    headers = {"X-Goog-Api-Key": key}
    video_ids = list(settings["video_ids"])
    cache = store.state.setdefault("youtube_videos", [])
    if not cache and not video_ids:
        candidates = []
        for query in settings["queries"]:
            search_params = {"part": "snippet", "type": "video", "maxResults": 10, **query}
            if settings.get("search_order"):
                search_params["order"] = settings["search_order"]
            data = client.get("https://www.googleapis.com/youtube/v3/search", search_params, "youtube", settings, headers, cost=100)
            group = [{"id": item["id"]["videoId"], "title": item["snippet"]["title"], "discovery_query": query["q"]} for item in data.get("items", [])]
            candidates.append(group)
        for index in range(max(map(len, candidates), default=0)):
            for group in candidates:
                if index < len(group) and group[index]["id"] not in {x["id"] for x in cache}:
                    cache.append(group[index])
        cache[:] = cache[:settings["max_videos"]]
        store.save()
    videos = [{"id": i, "title": None, "discovery_query": "provided_video_id"} for i in video_ids] if video_ids else cache
    for video in videos[:settings["max_videos"]]:
        if store.complete("youtube"):
            break
        video_id = video["id"]
        state = store.state["streams"].setdefault("youtube:" + video_id, {"cursor": None, "done": False, "pages": 0})
        while not state["done"] and state["pages"] < 3 and not store.complete("youtube"):
            params = {"part": "snippet", "videoId": video_id, "maxResults": 100, "order": "time", "textFormat": "plainText"}
            if state["cursor"]:
                params["pageToken"] = state["cursor"]
            data = client.get("https://www.googleapis.com/youtube/v3/commentThreads", params, "youtube", settings, headers, cost=1)
            if "items" not in data:
                raise Halt("YouTube response schema changed; no cursor advanced")
            before = len(store.rows)
            for item in data["items"]:
                top = item["snippet"]["topLevelComment"]
                snippet = top["snippet"]
                text = snippet.get("textOriginal", snippet.get("textDisplay", ""))
                expires = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(days=30)).isoformat()
                store.add("youtube", top["id"], text, guess_language(text), f"https://www.youtube.com/watch?v={video_id}&lc={top['id']}", content_type="video_comment", language_method="script_heuristic_unverified", language_original=None, video_id=video_id, created_at_utc=snippet.get("publishedAt"), updated_at_utc=snippet.get("updatedAt"), like_count=snippet.get("likeCount"), total_reply_count=item["snippet"].get("totalReplyCount"), reply_coverage="top_level_only", access_method="official_data_api", source_type="observed", refresh_or_delete_by_utc=expires, analysis_status="not_analyzed", context=video, retrieval_order="time")
            cursor = data.get("nextPageToken")
            state["done"] = not data["items"] or not cursor or cursor == state["cursor"] or len(store.rows) == before
            state["cursor"] = cursor
            state["pages"] += 1
            store.state["youtube_quota_used"] = settings["quota_used"]
            store.save()
            print(json.dumps({"platform": "youtube", "video_id": video_id, "saved": sum(r["platform"] == "youtube" for r in store.rows)}), flush=True)


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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=ROOT / "configs/feedback-collection.json")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--env-file", type=Path)
    parser.add_argument("--platforms", nargs="+", choices=["steam", "bluesky", "youtube"], default=["steam", "bluesky", "youtube"])
    args = parser.parse_args()
    if args.env_file:
        try:
            load_youtube_key(args.env_file)
        except (OSError, ValueError):
            parser.error("Unable to load a valid YOUTUBE_API_KEY from the specified local file; no values displayed")
    STATE.mkdir(parents=True, exist_ok=True)
    lock = (STATE / "feedback-collector.lock").open("a", encoding="utf-8")
    try:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            parser.error("Another collector is running in this project")
        config = json.loads(args.config.read_text(encoding="utf-8"))
        output = args.output or ROOT / "data/raw/feedback" / dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        store = Store(output, config)
        client = Client(STATE / "feedback-http-state.json")
        statuses = {}
        interrupted = False
        try:
            for platform in ("steam", "bluesky", "youtube"):
                settings = config[platform]
                if platform not in args.platforms or not settings["enabled"]:
                    statuses[platform] = "not_selected"
                    continue
                if store.complete(platform):
                    statuses[platform] = "target_already_reached"
                    continue
                settings["quota_used"] = store.state.get("youtube_quota_used", 0) if platform == "youtube" else 0
                try:
                    {"steam": steam, "bluesky": bluesky, "youtube": youtube}[platform](client, store, settings)
                    statuses[platform] = "target_reached" if store.complete(platform) else "partial_or_exhausted"
                except Halt as error:
                    statuses[platform] = str(error)
                    print(platform + ": " + str(error), flush=True)
                finally:
                    if platform == "youtube":
                        store.state["youtube_quota_used"] = settings.get("quota_used", 0)
                    store.save()
        except KeyboardInterrupt:
            interrupted = True
            statuses[platform] = "interrupted; resume with the same output directory"
            store.save()
        finally:
            export(store, statuses, client)
        return 130 if interrupted else 0 if all(store.complete(p) for p in args.platforms if config[p]["enabled"]) else 2
    finally:
        lock.close()


if __name__ == "__main__":
    sys.exit(main())
