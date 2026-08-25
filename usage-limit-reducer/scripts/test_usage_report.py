#!/usr/bin/env python3
"""
Tests for usage-report.py.

Runs against a synthetic ~/.claude/projects layout in a temp dir so real
logs aren't touched. Run directly: `python3 test_usage_report.py`.
"""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).parent
SCRIPT = HERE / "usage-report.py"

# Load the hyphenated module so we can call its functions directly.
spec = importlib.util.spec_from_file_location("usage_report", SCRIPT)
usage_report = importlib.util.module_from_spec(spec)
spec.loader.exec_module(usage_report)


def _ts(offset_hours: float = 0) -> str:
    t = datetime.now(timezone.utc) - timedelta(hours=offset_hours)
    return t.isoformat().replace("+00:00", "Z")


def _assistant(model: str, cwd: str, offset_hours: float = 0,
               input_tokens: int = 100, output_tokens: int = 50,
               cache_read: int = 1000, cache_write: int = 200) -> dict:
    return {
        "type": "assistant",
        "cwd": cwd,
        "timestamp": _ts(offset_hours),
        "message": {
            "role": "assistant",
            "model": model,
            "usage": {
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "cache_read_input_tokens": cache_read,
                "cache_creation_input_tokens": cache_write,
            },
        },
    }


def _user(cwd: str, offset_hours: float = 0) -> dict:
    # No `usage` field — should be ignored by collect().
    return {
        "type": "user",
        "cwd": cwd,
        "timestamp": _ts(offset_hours),
        "message": {"role": "user", "content": "hi"},
    }


def _write_jsonl(path: Path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")


class PriceTests(unittest.TestCase):
    def test_haiku_price(self):
        self.assertEqual(usage_report.price_for("claude-haiku-4-5"),
                         (1.0, 5.0, 1.25, 0.10))

    def test_opus_price_with_date_suffix(self):
        # The model string in real logs has a date suffix — prefix match should still work.
        self.assertEqual(usage_report.price_for("claude-opus-4-7-20260101"),
                         (15.0, 75.0, 18.75, 1.50))

    def test_sonnet_46_price(self):
        self.assertEqual(usage_report.price_for("claude-sonnet-4-6"),
                         (3.0, 15.0, 3.75, 0.30))

    def test_unknown_model_zero(self):
        self.assertEqual(usage_report.price_for("some-future-model"),
                         (0.0, 0.0, 0.0, 0.0))

    def test_empty_model_zero(self):
        self.assertEqual(usage_report.price_for(""), (0.0, 0.0, 0.0, 0.0))


class FormatTests(unittest.TestCase):
    def test_fmt_tokens(self):
        self.assertEqual(usage_report.fmt_tokens(42), "42")
        self.assertEqual(usage_report.fmt_tokens(1500), "1.5K")
        self.assertEqual(usage_report.fmt_tokens(2_500_000), "2.50M")


class CollectTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.projects_dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def _run(self, days: int = 7, project_filter: str | None = None):
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        return usage_report.collect(self.projects_dir, cutoff, project_filter)

    def test_empty_dir(self):
        totals, by_model, by_project, by_day = self._run()
        self.assertEqual(totals["turns"], 0)
        self.assertEqual(totals["cost"], 0.0)
        self.assertEqual(by_model, {})

    def test_basic_aggregation(self):
        _write_jsonl(self.projects_dir / "-proj-a" / "s1.jsonl", [
            _user("/proj/a"),
            _assistant("claude-opus-4-7", "/proj/a", input_tokens=10, output_tokens=20,
                       cache_read=1000, cache_write=500),
            _assistant("claude-haiku-4-5", "/proj/a", input_tokens=5, output_tokens=15,
                       cache_read=800, cache_write=100),
        ])
        totals, by_model, by_project, by_day = self._run()

        self.assertEqual(totals["turns"], 2, "user records without usage must be skipped")
        self.assertEqual(totals["input"], 15)
        self.assertEqual(totals["output"], 35)
        self.assertEqual(totals["cache_read"], 1800)
        self.assertEqual(totals["cache_write"], 600)

        # Per-model should NOT leak totals (regression test for the defaultdict(lambda: dict(totals)) bug).
        self.assertEqual(by_model["claude-opus-4-7"]["turns"], 1)
        self.assertEqual(by_model["claude-opus-4-7"]["input"], 10)
        self.assertEqual(by_model["claude-haiku-4-5"]["turns"], 1)
        self.assertEqual(by_model["claude-haiku-4-5"]["input"], 5)

        # Sanity: per-model turns sum to totals
        self.assertEqual(sum(r["turns"] for r in by_model.values()), totals["turns"])
        # Same for input
        self.assertEqual(sum(r["input"] for r in by_model.values()), totals["input"])

    def test_buckets_sum_to_totals(self):
        # Two projects, two models, two days — every breakdown should sum to the grand total.
        _write_jsonl(self.projects_dir / "-proj-a" / "s1.jsonl", [
            _assistant("claude-opus-4-7", "/proj/a", offset_hours=1,
                       input_tokens=10, output_tokens=20, cache_read=100, cache_write=50),
            _assistant("claude-haiku-4-5", "/proj/a", offset_hours=25,
                       input_tokens=30, output_tokens=40, cache_read=200, cache_write=60),
        ])
        _write_jsonl(self.projects_dir / "-proj-b" / "s1.jsonl", [
            _assistant("claude-opus-4-7", "/proj/b", offset_hours=2,
                       input_tokens=5, output_tokens=7, cache_read=50, cache_write=10),
        ])
        totals, by_model, by_project, by_day = self._run(days=7)

        self.assertEqual(totals["turns"], 3)
        for bucket, name in [(by_model, "model"), (by_project, "project"), (by_day, "day")]:
            self.assertEqual(
                sum(r["turns"] for r in bucket.values()), totals["turns"],
                f"{name} turns don't sum to total",
            )
            self.assertEqual(
                sum(r["input"] for r in bucket.values()), totals["input"],
                f"{name} input tokens don't sum to total",
            )
            self.assertEqual(
                sum(r["output"] for r in bucket.values()), totals["output"],
                f"{name} output tokens don't sum to total",
            )

    def test_days_cutoff_excludes_old(self):
        _write_jsonl(self.projects_dir / "-p" / "s.jsonl", [
            _assistant("claude-opus-4-7", "/p", offset_hours=1),         # in window
            _assistant("claude-opus-4-7", "/p", offset_hours=24 * 10),   # 10 days old
        ])
        totals, _, _, _ = self._run(days=7)
        self.assertEqual(totals["turns"], 1, "records older than --days must be excluded")

    def test_project_filter(self):
        _write_jsonl(self.projects_dir / "-p" / "s.jsonl", [
            _assistant("claude-opus-4-7", "/projects/keeper"),
            _assistant("claude-opus-4-7", "/projects/other"),
        ])
        totals, _, by_project, _ = self._run(project_filter="keeper")
        self.assertEqual(totals["turns"], 1)
        self.assertEqual(list(by_project.keys()), ["/projects/keeper"])

    def test_cost_calculation(self):
        # Opus: in=15, out=75, cache_write=18.75, cache_read=1.50 per million
        # 1M in, 1M out, 0, 0 → $15 + $75 = $90
        _write_jsonl(self.projects_dir / "-p" / "s.jsonl", [
            _assistant("claude-opus-4-7", "/p",
                       input_tokens=1_000_000, output_tokens=1_000_000,
                       cache_read=0, cache_write=0),
        ])
        totals, _, _, _ = self._run()
        self.assertAlmostEqual(totals["cost"], 90.0, places=4)

    def test_malformed_jsonl_line_ignored(self):
        path = self.projects_dir / "-p" / "s.jsonl"
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w") as f:
            f.write("this is not json\n")
            f.write(json.dumps(_assistant("claude-opus-4-7", "/p")) + "\n")
            f.write("{malformed\n")
        totals, _, _, _ = self._run()
        self.assertEqual(totals["turns"], 1, "malformed lines must be skipped, valid ones kept")


class CliTests(unittest.TestCase):
    """Exercise the script end-to-end via subprocess."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.projects_dir = Path(self.tmp.name)
        _write_jsonl(self.projects_dir / "-p" / "s.jsonl", [
            _assistant("claude-opus-4-7", "/p", offset_hours=1,
                       input_tokens=100, output_tokens=200, cache_read=900, cache_write=50),
        ])

    def tearDown(self):
        self.tmp.cleanup()

    def _run(self, *extra):
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--projects-dir", str(self.projects_dir), *extra],
            capture_output=True, text=True, check=False,
        )

    def test_text_output_has_headers(self):
        r = self._run("--days", "7")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("Claude Code usage", r.stdout)
        self.assertIn("By model", r.stdout)
        self.assertIn("Heuristics:", r.stdout)

    def test_json_output_is_valid(self):
        r = self._run("--days", "7", "--json")
        self.assertEqual(r.returncode, 0, r.stderr)
        parsed = json.loads(r.stdout)
        self.assertEqual(parsed["totals"]["turns"], 1)
        self.assertIn("by_model", parsed)

    def test_missing_projects_dir_exits_nonzero(self):
        r = subprocess.run(
            [sys.executable, str(SCRIPT), "--projects-dir", "/definitely/does/not/exist"],
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(r.returncode, 1)
        self.assertIn("No Claude Code logs", r.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
