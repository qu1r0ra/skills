---
name: find-docs-qu1r0ra
description: Use for library-specific documentation questions in AIOS or before editing code that depends on a third-party library. Prefer connected Context7 MCP tools.
---

# Context7 for AIOS

Use this route for library-specific documentation questions in AIOS and before
editing code that depends on a third-party library. Read the protected
[`find-docs`](../find-docs/SKILL.md) for library selection, version matching,
query wording, and result limits. This wrapper owns the tool route.

1. Form a specific query about the API, configuration, or version behavior
   needed for the task. Keep secrets and private source text out of the query.
   Complete when the library and question are explicit.
2. Discover the connected Context7 MCP tools. When both library resolution and
   documentation query are available, resolve the library name to an ID (unless
   the user supplied an ID), then query that ID. Tool names vary by harness;
   use the exposed Context7 capabilities rather than a hard-coded invocation
   syntax. Complete when the result matches the requested library and version.
3. If the MCP route is unavailable, use an already available Context7 CLI with
   the upstream skill's two-command procedure. If the CLI would require an
   installation or Context7 has no matching entry, use the library's official
   documentation. State which route supplied the answer; for a code change,
   record any fallback in the handoff. Complete when the answer is grounded in
   the retrieved documentation or the missing source is reported.
