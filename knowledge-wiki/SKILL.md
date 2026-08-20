---
name: knowledge-wiki
description: Set up or maintain a persistent, compounding knowledge base (an OKF bundle) from a growing collection of source documents. Use when the user wants to build a "knowledge graph," "wiki," or "knowledge base" over papers/articles/transcripts/notes; when they ask to "ingest" a new source into an existing one; when they ask to "lint" or health-check a wiki for staleness/contradictions/orphans; or when a repo already contains an OKF-shaped bundle (root index.md with okf_version, concept files with `type:` frontmatter) and the user asks you to query or extend it.
---

A knowledge wiki is a **compounding artifact**: each source you ingest doesn't just get indexed for later retrieval, it gets *compiled into* the existing structure — updating pages, strengthening or contradicting prior claims, filling in cross-references — so re-reading everything from scratch is never required to answer a question.

## The three layers

1. **Raw sources** — the immutable collection (PDFs, articles, transcripts). Source of truth; the wiki never edits these, only reads from them.
2. **The bundle** — the wiki itself: a directory of markdown files with YAML frontmatter, conformant to the Open Knowledge Format (OKF, see Reference below). You own this layer entirely.
3. **The schema** — this skill plus the project's own CLAUDE.md / AGENTS.md / rules files. It records domain-specific conventions (naming, node templates, what counts as a "finding" vs a "gap") and should co-evolve with the user as the domain's needs become clear. Don't try to author the domain schema yourself on the first pass — propose it, then let usage refine it.

## Setting up a new bundle

1. Pick a bundle root (often `kg/` or `wiki/` inside the repo, not the repo root, so it stays distinguishable from code). Create `index.md` there with `okf_version: "0.1"` in frontmatter — this is the only place frontmatter belongs in an `index.md`.
2. Decide the top-level concept types for the domain (e.g. Paper/Method/Concept/Finding/Gap, or Entity/Event/Theme for a book wiki) and scaffold one subdirectory per type, each with its own `index.md`.
3. Create a bundle-root `log.md` for the chronological history (see Reference — Log files).
4. Write down the domain's node shape (required sections per type) somewhere durable — a rules file the agent will reload, not just this conversation.

## Ingest (adding one source)

1. Read the raw source (never hand-edit it).
2. Extract the key claims, entities, and relationships worth keeping.
3. Write or update the concept page(s) — a single source can touch many pages: a new page for the source itself, updates to existing entity/concept pages it bears on, new cross-references.
4. Update every affected `index.md` (add the new entry with its one-line description).
5. Append an entry to the nearest `log.md`, dated `YYYY-MM-DD`, prefixed with a consistent bold tag (`**Ingest**`, `**Update**`) so the log stays greppable.
6. Prefer staying involved per-source over batch-ingesting many sources unsupervised, unless the user asks for the latter — the value of this pattern comes from checking each update lands correctly, not from throughput.

## Query (answering a question against the wiki)

1. Read the relevant `index.md` first to find candidate pages — this is the retrieval mechanism; no vector store is needed at moderate scale (~100s of pages).
2. Drill into the candidate concept pages, following cross-links as needed.
3. Synthesize an answer with citations back to concept pages (and through them, to raw sources).
4. If the answer itself is valuable — a comparison, an analysis, a connection the user asked to work out — offer to file it back into the wiki as a new concept page (e.g. under `findings/` or `comparisons/`) rather than letting it evaporate into chat history. This is what makes exploration compound instead of just accumulate.

## Lint (health-checking an existing wiki)

Run this periodically or when asked to review the wiki. Check for:
- Contradictions between pages (a new source's claim conflicts with an older page that hasn't been updated).
- Stale claims a newer source has superseded.
- Orphan pages with no inbound links.
- Concepts mentioned repeatedly in prose but lacking their own page.
- Missing cross-references between pages that clearly relate.
- Data gaps a targeted web search or a new source could fill.

There is typically no validator tool — verify with grep over frontmatter (`type:` present) and link targets (every `/path/to.md` resolves to a real file), per the OKF conformance rules below.

## Reference: OKF conformance (v0.1)

Full spec: `SPEC.md` at the root of a repo that has adopted it, if present; otherwise these are the load-bearing rules:

- **Bundle** = a directory tree of markdown files. `index.md` and `log.md` are reserved filenames (defined meaning, not concept pages) and may appear at any level.
- Every non-reserved `.md` file needs a YAML frontmatter block with a non-empty **`type`** field (required) — this is the only hard requirement for conformance. `title`, `description`, `resource` (canonical URI of the underlying asset, if any), `tags`, and `timestamp` (ISO 8601) are recommended but optional.
- **Links**: bundle-absolute (`/methods/fedavg.md`, relative to bundle root) are preferred over relative paths, since they survive files being moved between subdirectories. A link asserts a relationship; its kind is conveyed by surrounding prose, not the link syntax. Broken links are tolerated, not errors — they may just mark not-yet-written pages.
- **`index.md`** bodies have no frontmatter (except the bundle-root `okf_version` declaration) and list entries as `- [Title](path) - one-line description`, grouped under headings.
- **`log.md`** bodies are date-headed (`## YYYY-MM-DD`), newest first, with bulleted entries.
- **Citations**: a `# Citations` section at the bottom of a concept page, numbered, linking to the external/raw sources backing its claims.
- Consumers (including you, reading the bundle later) must tolerate unknown `type` values, missing optional fields, and broken links gracefully — don't treat these as reasons to reject or "fix" a bundle wholesale.
