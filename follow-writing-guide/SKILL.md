---
name: follow-writing-guide
description: Draft or revise a text under a researched writing guide. Invoke by name with a guide path, entry id, or project name.
disable-model-invocation: true
---

# Follow writing guide

Draft or revise text under an existing guide. The guide owns the rules; this skill holds only the procedure. Invoking it is the explicit Humanizer request, and the guide's Humanizer section sets whether it runs.

## Steps

### 1. Resolve

Take the guide from the argument, in this order:

1. A path to a project guide.
2. A wiki entry id: `qu1r0raOS-wikis/writing/guides/<id>.md`.
3. A project name: look it up in `qu1r0raOS-wikis/writing/usage/projects.md`, which gives the guide's repo-relative path.

Read the guide in full. Stop with a message naming what was tried when none resolves.

Done when one guide is read, or the stop message is sent.

### 2. Check currency

Warn the author once, before drafting, when:

- a source in the bank entry is past its `recheck_by` date, or
- the project guide's `Revision:` differs from the latest `checked_on` among the bank entry's sources.

Name the stale item and say that `curate-writing-guide` revises it. Then continue; do not recheck sources.

Done when the warning is sent, or neither condition holds.

### 3. Draft or revise

Write under the guide's rules, with its precedence order settling conflicts. Run Humanizer (`agent-skills/skills/humanizer/SKILL.md`) as the guide's Humanizer section directs, with its collision list and protections.

Done when every rule in the guide is applied or reported as a deviation under step 4.

### 4. Report deviations

List each deviation: rule, grade, and reason.

- An explicit user instruction overrides a `convention` or `preference` rule.
- Against a `requirement` or `authoritative guideline` rule, flag the conflict and ask before proceeding.

Done when every deviation is listed and every conflict with a `requirement` or `authoritative guideline` rule is answered.
