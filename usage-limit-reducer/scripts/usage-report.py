#!/usr/bin/env python3
"""
Local Claude Code token-usage report.

Reads ~/.claude/projects/*/*.jsonl (written by Claude Code on every turn) and
prints a breakdown by model, project, and day. No network calls — everything
stays on disk.

Usage:
    python3 usage-report.py                  # last 7 days, all projects
    python3 usage-report.py --days 1         # today-ish
    python3 usage-report.py --days 30
    python3 usage-report.py --project /path  # scope to one cwd
    python3 usage-report.py --json           # machine-readable output

Prices below are the public API list prices as of writing; they are estimates
for relative comparison, not a bill. Claude Code subscription plans don't bill
per-token, so treat the $ figure as "what this would cost on the API."
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Per-million-token list prices (USD). Update as Anthropic publishes new ones.
PRICES = {
    # (input, output, cache_write_5m, cache_read)
    "claude-opus-4":          (15.0, 75.0, 18.75, 1.50),
    "claude-opus-4-1":        (15.0, 75.0, 18.75, 1.50),
    "claude-opus-4-5":        (15.0, 75.0, 18.75, 1.50),
    "claude-opus-4-6":        (15.0, 75.0, 18.75, 1.50),
    "claude-opus-4-7":        (15.0, 75.0, 18.75, 1.50),
    "claude-sonnet-4":        (3.0, 15.0, 3.75, 0.30),
    "claude-sonnet-4-5":      (3.0, 15.0, 3.75, 0.30),
    "claude-sonnet-4-6":      (3.0, 15.0, 3.75, 0.30),
    "claude-haiku-4-5":       (1.0, 5.0, 1.25, 0.10),
    "claude-3-5-sonnet":      (3.0, 15.0, 3.75, 0.30),
    "claude-3-5-haiku":       (0.80, 4.0, 1.0, 0.08),
}


def price_for(model: str) -> tuple[float, float, float, float]:
    if not model:
        return (0.0, 0.0, 0.0, 0.0)
    key = model.lower()
    # strip date suffix like "-20251001"
    for known in PRICES:
        if key.startswith(known):
            return PRICES[known]
    return (0.0, 0.0, 0.0, 0.0)


def iter_jsonl(paths):
    for p in paths:
        try:
            with open(p, "r", encoding="utf-8", errors="replace") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        yield json.loads(line)
                    except json.JSONDecodeError:
                        continue
        except OSError:
            continue


def _zero_row():
    return {
        "input": 0, "output": 0, "cache_read": 0, "cache_write": 0,
        "turns": 0, "cost": 0.0,
    }


def collect(projects_dir: Path, cutoff: datetime, project_filter: str | None):
    totals = _zero_row()
    by_model = defaultdict(_zero_row)
    by_project = defaultdict(_zero_row)
    by_day = defaultdict(_zero_row)

    files = list(projects_dir.glob("*/*.jsonl"))
    for rec in iter_jsonl(files):
        msg = rec.get("message") or {}
        usage = msg.get("usage")
        if not usage:
            continue
        ts = rec.get("timestamp")
        if ts:
            try:
                when = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            except ValueError:
                when = None
        else:
            when = None
        if when and when < cutoff:
            continue
        cwd = rec.get("cwd") or "(unknown)"
        if project_filter and project_filter not in cwd:
            continue
        model = msg.get("model") or "(unknown)"
        day = when.date().isoformat() if when else "(no date)"

        inp = usage.get("input_tokens", 0) or 0
        out = usage.get("output_tokens", 0) or 0
        cr = usage.get("cache_read_input_tokens", 0) or 0
        cw = usage.get("cache_creation_input_tokens", 0) or 0

        pin, pout, pcw, pcr = price_for(model)
        cost = (inp * pin + out * pout + cw * pcw + cr * pcr) / 1_000_000

        for bucket in (totals, by_model[model], by_project[cwd], by_day[day]):
            bucket["input"] += inp
            bucket["output"] += out
            bucket["cache_read"] += cr
            bucket["cache_write"] += cw
            bucket["turns"] += 1
            bucket["cost"] += cost

    return totals, dict(by_model), dict(by_project), dict(by_day)


def fmt_tokens(n: int) -> str:
    if n >= 1_000_000:
        return f"{n/1_000_000:.2f}M"
    if n >= 1_000:
        return f"{n/1_000:.1f}K"
    return str(n)


def print_row(label: str, row: dict, width: int = 40):
    total_in = row["input"] + row["cache_read"] + row["cache_write"]
    cache_pct = (row["cache_read"] / total_in * 100) if total_in else 0.0
    print(
        f"  {label[:width]:<{width}} "
        f"turns={row['turns']:>5}  "
        f"in={fmt_tokens(row['input']):>7}  "
        f"out={fmt_tokens(row['output']):>7}  "
        f"cache_r={fmt_tokens(row['cache_read']):>7} ({cache_pct:4.1f}%)  "
        f"cache_w={fmt_tokens(row['cache_write']):>7}  "
        f"~${row['cost']:>7.2f}"
    )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--project", type=str, default=None, help="substring match on cwd")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--projects-dir", type=str, default=None, help="Path to projects log directory")
    args = ap.parse_args()

    candidate_dirs = []
    if args.projects_dir:
        candidate_dirs.append(Path(args.projects_dir))
    else:
        for p in [Path.home() / ".claude" / "projects", Path.home() / ".codex" / "projects", Path.home() / ".gemini" / "antigravity"]:
            if p.exists():
                candidate_dirs.append(p)

    if not candidate_dirs:
        default_p = Path.home() / ".claude" / "projects"
        print(f"No AI agent log directories found (checked {default_p}, ~/.codex/projects, etc.)", file=sys.stderr)
        return 1

    projects_dir = candidate_dirs[0]

    cutoff = datetime.now(timezone.utc) - timedelta(days=args.days)
    totals, by_model, by_project, by_day = collect(projects_dir, cutoff, args.project)

    if args.json:
        print(json.dumps({
            "window_days": args.days,
            "totals": totals,
            "by_model": by_model,
            "by_project": by_project,
            "by_day": by_day,
        }, indent=2))
        return 0

    total_in = totals["input"] + totals["cache_read"] + totals["cache_write"]
    cache_pct = (totals["cache_read"] / total_in * 100) if total_in else 0.0

    print(f"Claude Code usage — last {args.days} day(s)")
    if args.project:
        print(f"Filter: project contains {args.project!r}")
    print("-" * 72)
    print(f"Turns:        {totals['turns']:,}")
    print(f"Input:        {fmt_tokens(totals['input'])} fresh  +  "
          f"{fmt_tokens(totals['cache_read'])} cache-read  +  "
          f"{fmt_tokens(totals['cache_write'])} cache-write")
    print(f"Output:       {fmt_tokens(totals['output'])}")
    print(f"Cache hit:    {cache_pct:.1f}% of input tokens came from cache")
    print(f"Estimated $:  ~${totals['cost']:.2f} (API list prices; subscription is flat)")
    print()

    def top(d, n=8):
        return sorted(d.items(), key=lambda kv: kv[1]["cost"], reverse=True)[:n]

    if by_model:
        print("By model (top by cost):")
        for name, row in top(by_model):
            print_row(name, row, width=36)
        print()
    if by_project:
        print("By project (top by cost):")
        for name, row in top(by_project):
            print_row(name, row, width=50)
        print()
    if by_day:
        print("By day:")
        for name, row in sorted(by_day.items()):
            print_row(name, row, width=12)
        print()

    # Heuristic callouts
    print("Heuristics:")
    if totals["turns"] and cache_pct < 60:
        print(f"  - Cache hit is {cache_pct:.1f}% — low. You may be starting fresh chats too often, "
              f"or editing files in ways that bust cache. Batch related work in one session.")
    else:
        print(f"  - Cache hit is {cache_pct:.1f}% — healthy.")
    opus_cost = sum(r["cost"] for m, r in by_model.items() if "opus" in m.lower())
    if totals["cost"] and opus_cost / totals["cost"] > 0.5:
        print(f"  - Opus is {opus_cost/totals['cost']*100:.0f}% of spend. "
              f"Consider Haiku (/model claude-haiku-4-5) for simple edits, renames, drafts.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
