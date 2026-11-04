"""HTTP client for the official collection endpoints: host allowlist, budgets, cooldowns and redirects."""
import collections
import datetime as dt
import email.utils
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from zoneinfo import ZoneInfo

from ..common import write as write_json

HOSTS = {"api.steampowered.com", "public.api.bsky.app", "bsky.social", "www.googleapis.com"}


def load_youtube_key(path):
    values = []
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        match = re.match(r"^\s*(?:export\s+)?YOUTUBE_API_KEY\s*=\s*(.*?)\s*$", line)
        if not match:
            continue
        value = match.group(1)
        if value[:1] in ('"', "'"):
            quote = value[0]
            end = value.find(quote, 1)
            if end < 0 or (value[end + 1:].strip() and not value[end + 1:].strip().startswith("#")):
                raise ValueError("Invalid quoted YOUTUBE_API_KEY assignment; value not displayed")
            value = value[1:end]
        else:
            value = re.split(r"\s+#", value, maxsplit=1)[0].strip()
        values.append(value)
    if len(values) != 1 or not re.fullmatch(r"[A-Za-z0-9_-]{20,}", values[0]):
        raise ValueError("Expected one nonempty YOUTUBE_API_KEY assignment; value not displayed")
    os.environ["YOUTUBE_API_KEY"] = values[0]


def utc_now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def retry_delay(value, now=None):
    now = time.time() if now is None else now
    try:
        return max(0, float(value))
    except (ValueError, TypeError):
        try:
            return max(0, email.utils.parsedate_to_datetime(value).timestamp() - now)
        except (ValueError, TypeError, AttributeError):
            return 3600


class Halt(Exception):
    pass


class RestrictedRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        original = urllib.parse.urlsplit(req.full_url)
        destination = urllib.parse.urlsplit(newurl)
        if destination.scheme != "https" or destination.hostname != original.hostname:
            raise Halt("Unexpected redirect; request stopped without forwarding credentials")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


class Client:
    def __init__(self, path):
        self.path = path
        self.state = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
        self.opener = urllib.request.build_opener(RestrictedRedirect())
        self.events = []
        self.calls = collections.Counter()

    def get(self, endpoint, params, platform, settings, headers=None, cost=0):
        host = urllib.parse.urlsplit(endpoint).hostname
        if host not in HOSTS or not endpoint.startswith("https://"):
            raise Halt("Endpoint is outside the official host allowlist")
        self.state = json.loads(self.path.read_text(encoding="utf-8")) if self.path.exists() else self.state
        entry = self.state.setdefault(host, {})
        if entry.get("blocked_until", 0) > time.time():
            raise Halt("Host is in a persisted cooldown; no request sent")
        if self.calls[platform] >= settings["max_requests"]:
            raise Halt("Project request budget reached")
        if cost and settings.get("quota_used", 0) + cost > settings["quota_budget"]:
            raise Halt("Project YouTube quota budget reached")
        for attempt in range(3):
            if self.calls[platform] >= settings["max_requests"]:
                raise Halt("Project request budget reached during retry")
            if cost and settings.get("quota_used", 0) + cost > settings["quota_budget"]:
                raise Halt("Project YouTube quota budget reached during retry")
            if cost:
                day = dt.datetime.now(ZoneInfo("America/Los_Angeles")).date().isoformat()
                if entry.get("quota_day") != day:
                    entry.update(quota_day=day, quota_units_reserved=0)
                if entry["quota_units_reserved"] + cost > settings["quota_budget"]:
                    raise Halt("Project daily YouTube quota budget reached; no request sent")
                entry["quota_units_reserved"] += cost
            wait = max(0, entry.get("last_request", 0) + settings["interval_seconds"] - time.time())
            if wait:
                time.sleep(wait)
            self.calls[platform] += 1
            settings["quota_used"] = settings.get("quota_used", 0) + cost
            entry["last_request"] = time.time()
            write_json(self.path, self.state)
            request = urllib.request.Request(endpoint + "?" + urllib.parse.urlencode(params), headers={"User-Agent": "AIMediatorResearch/0.1 (bounded public feedback collection)", "Accept": "application/json", **(headers or {})})
            started = time.time()
            event = {"platform": platform, "host": host, "endpoint": urllib.parse.urlsplit(endpoint).path, "requested_at": utc_now(), "quota_cost": cost}
            self.events.append(event)
            try:
                with self.opener.open(request, timeout=25) as response:
                    data = json.load(response)
                    event["status"] = response.status
                    event["rate_headers"] = {k: v for k, v in response.headers.items() if "ratelimit" in k.lower() or "rate-limit" in k.lower() or k.lower() == "retry-after"}
                    remaining = response.headers.get("ratelimit-remaining", response.headers.get("x-ratelimit-remaining"))
                    if remaining == "0":
                        reset = response.headers.get("ratelimit-reset", response.headers.get("x-ratelimit-reset"))
                        try:
                            reset_time = float(reset)
                            entry["blocked_until"] = max(reset_time, time.time() + 60) if reset_time >= 1000000000 else time.time() + max(reset_time, 60)
                        except (TypeError, ValueError):
                            entry["blocked_until"] = time.time() + 3600
                        write_json(self.path, self.state)
                    return data
            except urllib.error.HTTPError as error:
                event["status"] = error.code
                if error.code in (401, 403, 429):
                    delay = retry_delay(error.headers.get("Retry-After")) if error.code == 429 else 3600
                    entry["blocked_until"] = time.time() + max(delay, 60)
                    entry["reason"] = f"HTTP {error.code}"
                    write_json(self.path, self.state)
                    raise Halt(f"HTTP {error.code}; host stopped and cooldown persisted") from None
                if error.headers.get("Retry-After") is not None:
                    entry["blocked_until"] = time.time() + max(retry_delay(error.headers.get("Retry-After")), 60)
                    write_json(self.path, self.state)
                    raise Halt(f"HTTP {error.code}; Retry-After cooldown persisted") from None
                if error.code not in (500, 502, 503, 504) or attempt == 2:
                    raise Halt(f"HTTP {error.code}; request stopped") from None
            except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError) as error:
                event["status"] = type(error).__name__
                if attempt == 2:
                    raise Halt("Transport or invalid JSON failure after bounded retries") from None
            finally:
                event["elapsed_seconds"] = round(time.time() - started, 3)
                entry["last_request"] = max(entry.get("last_request", 0), time.time())
                write_json(self.path, self.state)
            time.sleep(5 * (2 ** attempt))
        raise Halt("Retry budget exhausted")
