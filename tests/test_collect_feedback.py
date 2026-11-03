import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import urllib.error

SPEC = importlib.util.spec_from_file_location("collector", Path(__file__).resolve().parents[1] / "scripts/collect_feedback.py")
m = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(m)


class CollectorTests(unittest.TestCase):
    def test_env_loader_reads_only_the_requested_key_without_shell_execution(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / ".env"
            key = "A" * 39
            path.write_text('OTHER_SECRET=not_loaded\nexport YOUTUBE_API_KEY="' + key + '" # local\n')
            with patch.dict(m.os.environ, {}, clear=True):
                m.load_youtube_key(path)
                self.assertEqual(m.os.environ["YOUTUBE_API_KEY"], key)
                self.assertNotIn("OTHER_SECRET", m.os.environ)

    def test_env_loader_rejects_duplicate_and_shell_values_without_leaking(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / ".env"
            for value in ['YOUTUBE_API_KEY=$(malicious)\n', 'YOUTUBE_API_KEY=' + 'A' * 39 + '\nYOUTUBE_API_KEY=' + 'B' * 39]:
                path.write_text(value)
                with self.assertRaises(ValueError) as result:
                    m.load_youtube_key(path)
                self.assertNotIn(value, str(result.exception))

    def test_retry_after_seconds_and_http_date(self):
        self.assertEqual(m.retry_delay("120", 0), 120)
        self.assertEqual(m.retry_delay("Thu, 01 Jan 1970 00:02:00 GMT", 0), 120)
        self.assertEqual(m.retry_delay(None, 0), 3600)

    def test_language_labels_are_only_heuristic(self):
        self.assertEqual(m.guess_language("This game needs work"), "en")
        self.assertEqual(m.guess_language("这个游戏的角色"), "zh")
        self.assertEqual(m.guess_language("日本語のゲーム"), "ja")
        self.assertEqual(m.guess_language("lol"), "und")

    def test_stable_ids_deduplicate_without_semantic_filter(self):
        with tempfile.TemporaryDirectory() as directory:
            config = {"target_patch_context": "unverified", "steam": {"targets": {"en": 1}}}
            store = m.Store(Path(directory), config)
            self.assertTrue(store.add("steam", "1", "advertisement or unrelated text", "en", "https://example.org"))
            self.assertFalse(store.add("steam", "1", "same record", "en", "https://example.org"))
            self.assertTrue(store.add("steam", "2", "advertisement or unrelated text", "en", "https://example.org"))
            store.save()
            restored = m.Store(Path(directory), config)
            self.assertEqual(len(restored.rows), 2)
            self.assertEqual(restored.rows[0]["text_original"], "advertisement or unrelated text")
            self.assertEqual(restored.rows[0]["decision"], "")

    def test_changed_configuration_cannot_resume_silently(self):
        with tempfile.TemporaryDirectory() as directory:
            store = m.Store(Path(directory), {"target_patch_context": "A"})
            store.save()
            with self.assertRaises(ValueError):
                m.Store(Path(directory), {"target_patch_context": "B"})

    def test_429_stops_and_persists_cooldown_without_retry(self):
        with tempfile.TemporaryDirectory() as directory:
            client = m.Client(Path(directory) / "http.json")
            error = urllib.error.HTTPError("https://api.steampowered.com/", 429, "Too Many Requests", {"Retry-After": "120"}, io.BytesIO())
            with patch.object(client.opener, "open", side_effect=error) as opened:
                with self.assertRaises(m.Halt):
                    client.get("https://api.steampowered.com/test", {}, "steam", {"interval_seconds": 0, "max_requests": 5})
                with self.assertRaises(m.Halt):
                    client.get("https://api.steampowered.com/test", {}, "steam", {"interval_seconds": 0, "max_requests": 5})
                self.assertEqual(opened.call_count, 1)
            self.assertGreater(json.loads(client.path.read_text())["api.steampowered.com"]["blocked_until"], m.time.time())

    def test_secret_does_not_enter_request_log_on_403(self):
        with tempfile.TemporaryDirectory() as directory:
            client = m.Client(Path(directory) / "http.json")
            error = urllib.error.HTTPError("https://www.googleapis.com/test?key=SECRET", 403, "Forbidden SECRET", {}, io.BytesIO())
            with patch.object(client.opener, "open", side_effect=error):
                with self.assertRaises(m.Halt):
                    client.get("https://www.googleapis.com/test", {}, "youtube", {"interval_seconds": 0, "max_requests": 5, "quota_budget": 500}, headers={"X-Goog-Api-Key": "SECRET"}, cost=1)
            self.assertNotIn("SECRET", json.dumps(client.events))

    def test_steam_page_saved_before_cursor_resume(self):
        class FakeClient:
            def get(self, endpoint, params, platform, settings):
                return {"response": {"reviews": [{"recommendationid": "42", "language": "english", "review": "raw text", "timestamp_created": 1}], "cursor": "next"}}
        with tempfile.TemporaryDirectory() as directory:
            config = {"target_patch_context": "unverified", "app_id": 1364780, "date_start": None, "date_end": None, "steam": {"targets": {"en": 1}, "languages": {"en": "english"}}}
            store = m.Store(Path(directory), config)
            m.steam(FakeClient(), store, config["steam"])
            restored = m.Store(Path(directory), config)
            self.assertEqual(restored.state["streams"]["steam:en"]["cursor"], "next")
            self.assertEqual(restored.rows[0]["source_id"], "42")

    def test_youtube_missing_key_sends_no_network_request(self):
        with patch.dict(m.os.environ, {}, clear=True):
            with self.assertRaisesRegex(m.Halt, "Missing YOUTUBE_API_KEY"):
                m.youtube(None, None, {})

    def test_persisted_daily_quota_blocks_a_new_invocation(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "http.json"
            day = m.dt.datetime.now(m.ZoneInfo("America/Los_Angeles")).date().isoformat()
            path.write_text(json.dumps({"www.googleapis.com": {"quota_day": day, "quota_units_reserved": 500}}))
            client = m.Client(path)
            with patch.object(client.opener, "open") as opened:
                with self.assertRaisesRegex(m.Halt, "daily YouTube quota"):
                    client.get("https://www.googleapis.com/test", {}, "youtube", {"interval_seconds": 0, "max_requests": 5, "quota_budget": 500}, cost=1)
                opened.assert_not_called()

    def test_redirect_does_not_forward_credentials_to_other_host(self):
        request = m.urllib.request.Request("https://www.googleapis.com/test", headers={"X-Goog-Api-Key": "SECRET"})
        with self.assertRaises(m.Halt):
            m.RestrictedRedirect().redirect_request(request, None, 302, "Found", {}, "https://other.example/test")


if __name__ == "__main__":
    unittest.main()
