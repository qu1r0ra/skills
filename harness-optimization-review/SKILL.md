---
name: harness-optimization-review
description: Review owner-maintained global Claude Code and Codex assets for effective use, instruction conflicts, context cost, and reversible optimization.
---

# Global harness optimization review

Review global Claude Code and Codex setup. Follow the current repository's
review, privacy, delivery and durable-context contracts. This skill supplies
no authorization to inspect a whole user profile or change host configuration.
Keep repository-local instructions and vendor-managed internals outside the
edit corpus. Read [vendor sources](references/vendor-sources.md) for each
in-scope harness before evaluating loading, precedence, settings or features.

## 1. Bound the inventory

Declare the review's purpose, allowed read and edit effects, both harnesses'
availability and installed versions, and the repository receipt destination.
Before reading asset contents, list exact authorized absolute paths (expand
home/config overrides), asset type, harness, canonical source, projection or
link target, edit owner, and read/edit/excluded status. Directory authorization
must name its bounded descendants or selection rule; extend scope only with
owner authorization. Treat missing paths and unavailable harnesses as gaps.

Candidate locations to resolve against current docs and local metadata include
Claude's user instructions/rules, personal skills/agents, user settings and
their hook references, user-scoped MCP definitions and plugin configuration;
Codex's global instructions, personal skills/agents, config and referenced hook,
MCP or plugin configuration where supported. These are discovery categories,
not a fixed path allowlist. Include configured alternate homes and shared
sources only when authorized; follow links to establish ownership before
inspection. Read credential-bearing configurations through a metadata-only
view: key names, configured presence, scope and reference type; never emit,
copy into model context, or persist credential values. If safe extraction is
unavailable, mark that surface unreviewed.

**Done when:** every proposed read/edit has an exact bounded authorized path
and owner; repository content, generated projections, upstream sources and
vendor internals are classified; unavailable areas have explicit limitations.

## 2. Establish effective behavior

Fetch current official vendor docs during this run and record URLs, access
date, applicable version and the claims they support. Establish actual loading,
precedence, merge rules, overrides and supported features separately for each
harness. Local flags, policy and active host may differ from documented defaults.
If docs or effective-state evidence are unavailable, defer conclusions needing
them. Preserve the distinct meanings of each harness's security controls.

Inspect the bounded corpus for observed usefulness, conflicting/stale guidance,
duplication, loading/context overhead, discoverability and effective use of
skills/agents, settings, hooks, MCP/plugins, unnecessary or missed capabilities,
and retention/backup practices. Prefer demonstrated friction or usage evidence;
record hypotheses as hypotheses and unknown usage as unknown. Retention review
uses metadata and owner policy, never session/private-history bulk ingestion.
Consume completed architecture, Environment, security, document or skill audit
findings as optional evidence; their full audits and schedules stay independent.

**Done when:** every authorized surface has findings or an explicit no-change/
unreviewed disposition; each behavior claim has current official support and
local evidence or a named uncertainty.

## 3. Decide recommendations

For each recommendation record evidence, expected benefit, tradeoffs, exact
edit owner/source, verification and rollback route, and disposition: retain,
authorized edit, defer, or reject. Consolidate only after proving ownership and
effective precedence. Edit canonical sources; generated projections follow
their owner's generation/sync workflow. Protected upstream skills follow their
updater, with local preferences in an authorized wrapper. Apply repository
standing sync rules when they exist. No useful changes is a valid outcome.

Security, permission/approval rules, sandboxing, execution policy, credential
handling, and installing or enabling capabilities each need a separate explicit
owner decision on the concrete proposal. A general optimization authorization
does not cover them. Record rationale and alternatives; leave them pending
until authorized. Hook changes affecting execution or data flow use this gate.

**Done when:** every finding has a disposition and every proposed mutation is
within the stated authorization or held for its separate owner decision.

## 4. Apply authorized reversible changes

Before ordinary bounded edits, establish restorable version history or a
protected local snapshot of the exact affected assets and record its safe
reference. Keep secret-bearing backups outside repository/model context under
their owning protection policy; metadata-only inspection never authorizes
copying credential values. Preserve unrelated changes. Apply at canonical
owners, regenerate/sync through their documented route, and use proportionate
syntax, loading and representative behavior checks. Reload or execute hooks/
tools only within the authorized effects. Verify intended behavior and preserved
controls; roll back failed edits or leave a documented deferred proposal.

**Done when:** each attempted change has a verified result or verified rollback;
each untested surface is a limitation rather than a success claim.

## 5. Record completion

Write a sanitized dated receipt in the selected repository: purpose and exact
asset coverage (use safe aliases when paths identify private data), versions,
official sources/access dates, ownership/precedence findings, limitations,
recommendations and dispositions, authorization references, changes and snapshot
references, verification/rollback results, deferred owner decisions, and the
next useful follow-up. Exclude credentials, raw private configuration and
transcript content. Distinguish complete, partial and blocked coverage; record
an evidenced no-change result when applicable. Follow repository delivery rules.

A reminder is an invitation to invoke this review. Its delivery, scheduler
success and occurrence completion prove no review execution. Complete an
occurrence only through its owning contract after owner agreement.

**Done when:** the durable receipt accounts for every in-scope asset and finding,
reports pending decisions and gaps, and distinguishes review completion from
reminder state.
