# Bank entry

The entry is one `guides/<slug>.md` concept under the `writing-v1` profile (`governance/knowledge-profiles/writing-v1.md` owns the source fields). The slug is lowercase kebab-case, from genre and venue or field.

## Frontmatter

```yaml
---
type: guide
title: <Use case title>
description: <One sentence: use case, audience, venue>
tags: [writing, <genre>, <field>]
status: draft
trust: reviewed
sources:
  - url: https://example.org/author-guidelines
    provider: <organization>
    title: <page title>
    grade: requirement
    checked_on: "2026-01-01"
    recheck_by: "2026-07-01"
    supports: <the rule it backs>
    status: verified
---
```

Set `status: stable` after the first successful use. Write `checked_on` and `recheck_by` as quoted `"YYYY-MM-DD"` strings; an unquoted date fails validation. Add `- resource: /sources/src_<id>.md` beside the inline records for a captured exemplar.

## Body

- **Coverage:** `complete` or `partial`, with each blocked lane named.
- **Rules:** one subsection per grade, strongest first. Each rule states the instruction, its source URL, and for an `authoritative guideline` the quoted passage.
- **Techniques:** craft and exemplar technique notes.
- **Open questions:** unresolved items, including unanswered lane questions.
- **Neighbours:** bundle-absolute links to the nearest guides and practices.

## Grades

| Grade | Use when | Recheck |
| --- | --- | --- |
| `requirement` | a venue or institution imposes it | 6 months |
| `authoritative guideline` | a recognised body publishes it | 12 months |
| `convention` | the field's practice shows it | 12 months |
| `empirical` | a study supports it | 24 months |
| `preference` | craft opinion, or the author's choice | 24 months |

A venue or institutional rule has a 6-month recheck even when graded lower. Set `recheck_by` = `checked_on` plus the interval.

## Exemplars

Capture full text only from openly licensed, public-domain, or open-access sources, after scanning the bytes for hard exclusions under `governance/privacy-policy.yaml`. Capture follows `writing-v1.md`: a `sources/src_<32 hex>.md` concept plus the bytes under `raw/`, with its hash. Otherwise keep technique notes, short quotations, and a link. Private exemplars stay in the project that owns them.

## Index and catalog

1. Add one row per applicable key in `guides/index.md` (genre, field, audience, venue).
2. Add or update `practices/<topic>.md` (`type: practice`, with its graded sources) for each lifted rule, and list it in `practices/index.md`.
3. Add the project line to `usage/projects.md`: project name and the repo-relative guide path, both plain text.
4. Regenerate `catalog.json`: every concept `.md` file (not `index.md`, `log.md`, `AGENTS.md`, or `raw/`), sorted and unique.
5. Add one line to `log.md`.
