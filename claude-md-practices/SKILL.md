---
name: claude-md-practices
description: Standard for writing lean agent instructions (CLAUDE.md, AGENTS.md, .claude/rules/*.md, .Codex/rules/*.md). Use when writing or editing agent instruction files, project trackers, or migrating rules.
---

## Operating principle

Every line in an agent-loaded file (`CLAUDE.md`, `AGENTS.md`, `.claude/rules/*.md`, `.Codex/rules/*.md`) must be
**load-bearing**: would an agent get this wrong without this line, on a
typical task in this repo? No — cut it, push it to an on-demand rule file, or
trust exploration. All rules below are this test applied to a specific case.

## Rules

- **No prose, no tables in agent-loaded files.** Flat bullets only. Tables are
  fine in `.claude/project/*.md` or `.Codex/project/*.md` trackers — there, a row is a tracked item
  with a status field, i.e. data, not exposition.
- **Omit volatile detail** — hyperparameter values, exact counts, dates, PR
  numbers, run counts. If code/config/manuscript already carries the value,
  don't shadow it in a rule file.
- **Omit the inferable** — standard directory layout, common library usage.
  Trust exploration over spelling it out.
- **No glob-loading.** Instruction files (`CLAUDE.md` / `AGENTS.md`) have no `.mdc`-style conditional loading.
  Instead: a few always-active `@import`s, plus a plain-bullet index of the
  rest ("read `X.md` when doing Y") — read on demand, never auto-loaded.
- **Changelog entries are milestones, not commits.** 1-3 lines. If an entry
  names a specific function, file, or formula, that content belongs in the
  commit body, not the changelog — git log already carries it.
- **No volatile numbers in illustrative examples.** Abstract phrasing
  ("run count increases") over a real snapshot value ("195→201") — the
  example outlives the number.
- **Single source of truth.** One fact lives in one file; every other
  agent-loaded file links to it rather than restating it.
- **Rules vs. registries are different homes.** `.claude/rules/` and `.Codex/rules/` hold stable
  instructions that rarely change. `.claude/project/*.md` and `.Codex/project/*.md` hold trackers
  expected to change — tables belong there.
- **Plain-heading frontmatter for new or migrated rule files.** No Cursor-era
  YAML (`description`/`globs`/`alwaysApply`) — that shape existed for
  glob-based auto-loading, which flat markdown files don't do.

## Exemption

`README.md` is human-facing GitHub onboarding, not agent-loaded. Restating a
pointer there that also lives in `CLAUDE.md` or `AGENTS.md` is not a single-source-of-truth
violation — don't gut a README to satisfy this skill.
