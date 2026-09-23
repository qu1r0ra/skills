---
name: update-protected-skills
description: Check and refresh explicitly designated upstream skills, or resolve a blocked upstream change. Use when maintaining any skill listed in the protected upstream manifest.
---

# Update Protected Skills

Use the updater at `scripts/manage.py` for skills listed under `protected_upstream.skills` in `.metadata.json`.

## Check and update

1. Run `uv run --no-project python agent-skills/skills/update-protected-skills/scripts/manage.py check` before editing a designated skill. Resolve any reported drift by restoring the adopted source or recording a specific, reasoned exception.
2. Run `uv run --no-project python agent-skills/skills/update-protected-skills/scripts/manage.py preview --skill NAME` to inspect a candidate source diff. Run `uv run --no-project python agent-skills/skills/update-protected-skills/scripts/manage.py update` to fetch each recorded upstream branch and apply eligible changes. Additions and edits are accepted after the critical-severity SkillShare audit passes. File removals, source-path changes, or rewritten history stop for review; after reviewing the exact candidate commit, record approval with `approve --skill NAME --commit SHA --reason "..."` and run `update` again.
3. The updater replaces only changed designated directories, records source revisions and full-directory/file hashes, synchronizes SkillShare targets, checks projection drift, and commits and pushes accepted updates. If publication fails, it keeps the commit and a retry receipt; run `update` again after resolving the remote failure.
4. Read every blocked-change receipt under the updater's local Git metadata directory. Approval of a removed upstream skill keeps its existing canonical directory as a local skill and removes only its upstream designation. Preserve target-local skills while repairing projections through SkillShare's configured sync.

## Boundaries

The manifest is the designation list; same-name matches alone do not qualify. Local behavior belongs in a separate wrapper or fork. An exception must identify the exact skill, current directory hash, and reason, so a later edit invalidates it. A source deletion or rename requires approval tied to the exact fetched commit. Never turn an audit failure, unexplained drift, or missing projection into an accepted update.

The updater runs fixed Git and SkillShare commands with argument arrays and no shell. It treats fetched files as data, accepts only regular files, rejects paths that collide or cannot be represented distinctly on Windows, and audits each changed directory before replacing its canonical copy.
