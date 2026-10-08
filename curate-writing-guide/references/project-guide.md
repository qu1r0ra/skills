# Project guide

The project guide is self-contained: the project's agents follow it without the bank. Write it at `docs/writing-guide.md`, or at the project's own docs convention when it has one. Then add one pointer line to the project's agent instructions (`AGENTS.md` or `CLAUDE.md`) that names the guide and the situation that calls for it, never this skill.

## Sections

1. **Use case:** the summary from Frame.
2. **Precedence:** `requirement` > `authoritative guideline` > `empirical` > `convention` > `preference`. A higher grade wins a conflict.
3. **Rules:** every rule from the entry, grouped by grade, each with its grade. Add the quoted passage under each `authoritative guideline` rule.
4. **Humanizer:** `on` by default. Set it `off` only when the author chose so in the grill.
   - **Collisions:** list each rule that conflicts with a Humanizer pattern (read `agent-skills/skills/humanizer/SKILL.md`) and say which wins. A `requirement` or `authoritative guideline` rule wins; a `convention` or `preference` rule yields to Humanizer.
   - **Protection:** Humanizer never rewrites a `requirement` or `authoritative guideline` rule's wording or its effect, even to remove a tell.
5. **Deviation rule:** the author may deviate from a `convention` or `preference` rule with a one-line reason in the draft. A deviation from a `requirement` or `authoritative guideline` rule needs the author's explicit approval for that passage.
6. **Provenance:** the bank entry slug, its revision (the latest `checked_on` among the entry's sources, as `Revision: YYYY-MM-DD`), and a link to the wiki entry as `qu1r0raOS-wikis/writing/guides/<slug>.md`.
7. **Existing instructions:** a table of the style rules the project already carries (prose rules in `AGENTS.md` or `CLAUDE.md`, `rules/` files, style skills), one row per rule: *absorbed* (the guide now holds it), *kept* (a process rule, not style), or *retired* (removed from its file). Repoint or delete any pointer to a missing file or skill. Edit an existing instruction file only with the author's permission. Revise deletes the table once the author confirms every row is settled.

## Usage index

After writing the guide, add its line to `usage/projects.md` (project name, then the guide's repo-relative path, as plain text).
