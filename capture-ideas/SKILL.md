---
name: capture-ideas
description: "Capture one or more vague idea seeds for later without turning them into a spec, ticket, schedule, or implementation."
disable-model-invocation: true
---

# Capture Ideas

Use this skill when the user wants to get one or more vague ideas out of their head while deliberately leaving the design unresolved. The skill is a low-friction capture boundary, not an analysis or planning flow.

## Process

1. Treat the user's current message as the source capture. Preserve its wording; add only short neutral titles and bounded seed wording needed to separate independently reviewable ideas. If no idea text is present, ask for one sentence and nothing more. Completion means the source capture is ready for validation or the user has been asked only for the missing sentence.
2. Identify the `qu1r0raOS` control-plane root by locating its `AGENTS.md` and `qu1r0raOS-workspace`. Write only into the authoritative OKF Ideas bundle at `qu1r0raOS-workspace/AIOS/Ideas`. If the root cannot be identified, ask for a destination instead of creating an inbox elsewhere. Completion means the canonical root and Ideas bundle path are identified, or capture is paused with no file written.
3. Read `governance/privacy-policy.yaml` and run the repository's deterministic `scan_text` secret-pattern scan with JWT and payment checks enabled against the source capture and every proposed seed. Persist only clean content. If the scan finds a hard exclusion or cannot be run, keep the raw text out of the bundle and ask the user for a sanitized version or a working repository environment. Completion means every proposed persisted value has a clean scan result, or no raw text has been persisted and the blocking reason is reported.
4. Decide whether the source contains one or multiple independently reviewable subjects. Keep one idea when the message has one subject with several implementation details. When it contains multiple subjects, draft one neutral title and one bounded seed for each subject. Completion means the one-item fast path is identified or a proposed split is ready to show the user.
5. For a proposed split, show every title and seed and wait for exactly one explicit choice: `confirm`, `edit`, `keep as one`, or `cancel`. On `edit`, apply only the user's bounded corrections and ask for final confirmation before writing. Persist nothing while the split is awaiting confirmation. Completion means one confirmed atomic set is available, the user chose to keep one seed, or capture was cancelled with no write.
6. Persist into `qu1r0raOS-workspace/AIOS/Ideas` using the CLI commands below. For a single idea, use `qu1r0raOS ideas capture`. For a confirmed split (compound capture), use `qu1r0raOS ideas compound-capture` with a temporary JSON file describing the children. Default maturity is `seed` and lifecycle is `captured`. Any non-default maturity (`exploratory`, `partially_designed`, `specified`) or attached `--artifact` requires explicit `--confirm`; without confirmation, capture fails atomically and writes zero files. Completion means the OKF Ideas bundle atomically records the new idea(s) along with provenance links, catalog, and derived transaction log.
7. Stop after the idea or ideas are saved. Leave requirements, boundaries, acceptance criteria, architecture, schedule, ownership, and implementation unresolved. Report the bundle path, capture ID when compound, and idea IDs and titles. Completion means no specification, ticket, schedule, implementation, or downstream flow was created.

## Commands

For a single idea capture:

```powershell
uv run qu1r0raOS ideas capture --root <control-plane-root> `
  --title "<short neutral title>" `
  --content "<the user's original wording>" `
  [--maturity <seed|exploratory|partially_designed|specified>] `
  [--artifact <path-to-artifact>] `
  [--confirm]
```

For a compound capture (multi-subject split):

```powershell
uv run qu1r0raOS ideas compound-capture --root <control-plane-root> `
  --message "<the user's untouched original wording>" `
  --ideas-json <path-to-children-json> `
  [--confirm]
```

Where `--ideas-json` contains an array of objects with `title`, `content`, and optional `tags`, `maturity`, or `description`.

## Bundle shape

Each idea is persisted as an OKF concept document in `qu1r0raOS-workspace/AIOS/Ideas/ideas/idea_<lowercase UUID4 hex>.md`:

```markdown
---
type: idea
title: <short neutral title>
description: <summary or initial line>
tags: []
status: draft
sources: []
generated: false
verified: false
idea_id: idea_<lowercase UUID4 hex>
maturity: seed
lifecycle: captured
captured_at: YYYY-MM-DDTHH:MM:SS+08:00
related_ideas: []
capture: null
history:
  - action: captured
    recorded_at: YYYY-MM-DDTHH:MM:SS+08:00
    lifecycle: captured
---

# <short neutral title>

<the user's original wording>
```

For a compound capture, `capture` contains
`/captures/capture_<lowercase UUID4 hex>.md`, and `related_ideas` contains the
sibling idea links.

## Identity and title policy

- Ideas use opaque lowercase UUID4 identities. The filename stem and `idea_id` frontmatter must be identical.
- Compound captures use opaque lowercase UUID4 identities. The filename stem and `capture_id` frontmatter must be identical, and child links must use canonical idea paths.
- Sources use `source_<full lowercase SHA-256 hex>`. The filename stem, `source_id`, and `sha256` metadata must agree. Identical bytes reuse one source identity; changed bytes create a new source identity and retain the earlier revision.
- Raw artifacts use `source_<sha256>__<sanitized original filename>` and are referenced by exactly one source document.
- Titles are independent human-readable metadata in conceptual sentence case. Do not encode capture dates, lifecycle states, or other mutable labels in filenames or titles.
- Do not invent aliases, redirects, legacy filenames, or title-derived identities. A migration may record old-to-new mappings only in its migration history.

When the user is ready to act on an entry, let them use `review-ideas` or explicitly choose a next flow (`grill-qu1r0ra`, `to-spec-qu1r0ra`, `to-tickets`, or `wayfinder`). This skill does not invoke those flows automatically.
