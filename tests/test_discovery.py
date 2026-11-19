import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
from scripts.discover import collect, candidate_from_repo, MAX_PER_RUN

NOW = datetime(2026, 11, 19, 8, 15, tzinfo=ZoneInfo("Asia/Shanghai"))

class DiscoveryTests(unittest.TestCase):
    def test_demo_is_not_verified_preview(self):
        repo = {
            "id": 1, "html_url": "https://github.com/example/demo",
            "full_name": "example/demo", "homepage": "https://example.org/demo",
            "license": {"spdx_id": "MIT"},
        }
        entry = candidate_from_repo(repo, "UI-01", "daily", NOW.isoformat())
        self.assertEqual(entry["demo_url"], "https://example.org/demo")
        self.assertIsNone(entry["preview_url"])
        self.assertFalse(entry["preview_verified"])
        self.assertFalse(entry["source_verified"])
        self.assertFalse(entry["license_verified"])
        self.assertFalse(entry["reproduced"])

    def test_cap_and_permanent_dedup_across_runs(self):
        repo_list = [
            {"id": i, "html_url": f"https://github.com/example/motion-{i}",
             "full_name": f"example/motion-{i}", "description": "test"}
            for i in range(30)
        ]
        with tempfile.TemporaryDirectory() as d:
            api = lambda topic, token, pool: repo_list
            first = collect(Path(d), api=api, now=NOW)
            second = collect(Path(d), api=api, now=NOW)
            third = collect(Path(d), api=api, now=NOW)
            self.assertEqual(first["new_candidates"], MAX_PER_RUN)
            self.assertEqual(second["new_candidates"], 6)
            self.assertEqual(third["new_candidates"], 0)
            day = Path(d) / "daily" / "2026-11-19.jsonl"
            self.assertEqual(len(day.read_text(encoding="utf-8").splitlines()), 30)

    def test_provider_error_reported(self):
        def failing_api(topic, token, pool):
            raise RuntimeError("rate-limited")
        with tempfile.TemporaryDirectory() as d:
            result = collect(d, api=failing_api, now=NOW)
            self.assertEqual(result["new_candidates"], 0)
            self.assertEqual(len(result["errors"]), 4)

    def test_reject_bad_urls(self):
        entry = candidate_from_repo(
            {"html_url": "file:///etc/passwd", "id": 2},
            "UI-01", "daily", NOW.isoformat())
        self.assertIsNone(entry)

if __name__ == "__main__":
    unittest.main()
