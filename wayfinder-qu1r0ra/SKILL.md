---
name: wayfinder-qu1r0ra
description: "Use Wayfinder for a multi-session AIOS decision effort on the central GitHub issue tracker."
disable-model-invocation: true
---

# Wayfinder for AIOS

Use this wrapper when an AIOS effort needs a shared decision map across agent
sessions. This wrapper owns the AIOS invocation. Read the protected
[`wayfinder`](../wayfinder/SKILL.md) as the reference for the map, frontier,
ticket types, and chart/work sequence.

## AIOS tracker route

1. Read the [central issue tracker contract](../../../docs/agents/issue-tracker.md),
   especially **Wayfinding operations**. For live issue work, also read the
   local `aios-github-tickets` skill. Use the private central GitHub tracker for
   AIOS-owned maps; repository-owned work follows its own tracker. Completion:
   the map's owning tracker and issue shape are identified.
2. Keep Wayfinder's map and child-ticket headings. Add the short AIOS routing
   and verification sections required by the central issue contract. Assign
   the ordinary AIOS lifecycle, domain, target, and work-type labels alongside
   the `wayfinder:*` label. The tracker contract gives the mapping. Completion:
   the draft map and child issues have their required headings and labels.
3. Plan GitHub sub-issues and native dependencies for the visible frontier.
   Preserve the readable blocker reference in each child issue. Identify the
   first open, unblocked, unassigned child in map order, unless the user names
   one. Completion: the draft has a linked frontier and a next-child candidate.
4. Follow **Shaped issue publication** in the central issue tracker contract.
   After an authorized tracker mutation, verify the affected issues and run
   the live read-only tracker validation. When work on the selected child
   begins, claim it first, as upstream Wayfinder requires. Completion: the map
   is a validated unpublished draft, or its child links, blockers, routing
   labels, and decision pointers agree with the live issue state; any child
   being worked is claimed.

Use the upstream `wayfinder` skill directly when the work belongs to another
repository's own tracker.
When an AIOS map clears and the user asks for the buildable spec, hand its
linked decisions to `to-spec-qu1r0ra`.
