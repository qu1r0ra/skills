# usage-limit-reducer

A Claude Code skill that stops you from burning through your usage limit.

Claude re-reads the entire conversation on every turn. One developer measured it: **98.5% of his tokens went to re-reading history, only 1.5% to generating responses.** This skill diagnoses where your tokens are actually going and applies Dubi's 11 rules for cutting usage — using real data from the JSONL logs Claude Code already writes to your disk.

## What it does

When you trigger the skill, it:

1. **Measures** — runs `scripts/usage-report.py` against `~/.claude/projects/*/*.jsonl` and shows token/cost breakdowns by model, project, and day (with cache-hit % and heuristic callouts).
2. **Diagnoses** the current session — conversation length, `CLAUDE.md` presence, model in use.
3. **Applies** the 2–4 rules most relevant to what it finds. No dumping all 11 on you.
4. **Suggests** concrete next actions (`/compact`, `/clear`, `/model claude-haiku-4-5`, create CLAUDE.md, etc.) and acts only on confirmation.

## Install

```bash
git clone <this-repo> ~/.claude/skills/usage-limit-reducer
```

Or, if you already cloned it elsewhere:

```bash
cp -r . ~/.claude/skills/usage-limit-reducer/
```

Restart Claude Code. It will show up in the skills list and auto-trigger on phrases like:

- "hit my limit" / "usage limit" / "running out of tokens"
- "save tokens" / "reduce usage" / "am I wasting tokens"
- "this chat is getting long"
- "which model should I use"

You can also invoke it directly: `/usage-limit-reducer`.

## Standalone: the token report

The script is useful on its own, outside the skill:

```bash
python3 ~/.claude/skills/usage-limit-reducer/scripts/usage-report.py --days 7
python3 ~/.claude/skills/usage-limit-reducer/scripts/usage-report.py --days 30 --project myrepo
python3 ~/.claude/skills/usage-limit-reducer/scripts/usage-report.py --json   # machine-readable
```

Example output:

```
Claude Code usage — last 7 day(s)
------------------------------------------------------------------------
Turns:        110
Input:        274 fresh  +  6.16M cache-read  +  934.3K cache-write
Output:       152.9K
Cache hit:    86.8% of input tokens came from cache
Estimated $:  ~$38.22 (API list prices; subscription is flat)

By model (top by cost):
  claude-opus-4-7     turns= 109  in=   274  out= 152.9K  cache_r= 6.16M (86.8%)  ~$38.22

Heuristics:
  - Cache hit is 86.8% — healthy.
  - Opus is 100% of spend. Consider Haiku (/model claude-haiku-4-5) for simple edits.
```

**What's read:** every JSONL file under `~/.claude/projects/`. **What leaves your machine:** nothing. No network calls.

**Pricing note:** the `$` figure uses API list prices as a relative-comparison tool. If you're on a Claude Code subscription plan, billing is flat — treat the number as "what this would cost on the API."

## The 11 rules, and what each maps to

| # | Rule | Implementation in Claude Code |
|---|------|-------------------------------|
| 1 | Don't follow up to correct — restart | Skill suggests `/clear` + re-prompt instead of piling on corrections |
| 2 | Fresh chat every 15–20 turns | Skill suggests `/compact` or `/clear` + paste summary |
| 3 | Batch questions into one message | Skill coaches on combining related asks |
| 4 | Track actual token usage | **`scripts/usage-report.py`** — reads local JSONL logs |
| 5 | Reuse recurring context | Skill points at `CLAUDE.md`, skills, `.context/` |
| 6 | Set up memory / user preferences | Skill checks for `CLAUDE.md`, offers to create it |
| 7 | Turn off features you don't use | Skill flags unused MCPs/hooks in `settings.json` |
| 8 | Use Haiku for simple tasks | Skill recommends `/model claude-haiku-4-5` when Opus share is high |
| 9 | Spread work across the day | Skill advises splitting into 2–3 sessions (5-hour rolling window) |
| 10 | Work off-peak | Skill flags peak hours (5–11am PT / 8am–2pm ET weekdays) |
| 11 | Enable Overage as a safety net | Skill mentions the Settings → Usage option on Pro/Max |

**Not implementable in Claude Code** (flagged honestly by the skill):

- Rule #1's "edit the original prompt" is a claude.ai web UI feature.
- Rule #5's "upload to Projects" is also web-only.
- Rule #11's Overage toggle is plan-level.

## Layout

```
usage-limit-reducer/
├── SKILL.md                  # what Claude reads when the skill triggers
├── README.md                 # this file (for humans)
└── scripts/
    ├── usage-report.py       # the local token dashboard
    └── test_usage_report.py  # 16 unit + CLI tests
```

## Tests

```bash
python3 scripts/test_usage_report.py
```

Covers price lookups, aggregation math, `--days` cutoff, `--project` filter, malformed-JSONL handling, CLI text/JSON output, and a regression test for the `defaultdict(lambda: dict(totals))` shared-state bug.

## Credit

The 11 rules are from Dubi's article. This skill just wires them into Claude Code with real measurement.
