---
name: find-docs-qu1r0ra
description: Use when an AIOS library documentation lookup or third-party library code change needs current docs. Prefer the Context7 CLI when shell access is available; use connected MCP tools when CLI is unavailable or a better fit.
---

# Context7 for AIOS

Use this route for library documentation questions in AIOS and before editing
code that depends on a third-party library. Read the protected
[`find-docs`](../find-docs/SKILL.md) for library selection, version matching,
query wording, and result limits. This wrapper owns route choice.

1. Form a specific, secret-free query about the API, configuration, or version
   behavior needed for the task. Keep it to one concept unless the concepts
   must be understood together. Complete when the library, version, and
   question are clear enough to retrieve matching documentation.
2. Prefer the upstream Context7 CLI flow when shell and Node/npm are already
   available. Follow `find-docs` for its commands, mandatory library-resolution
   step, result interpretation, and call limit. CLI + Skills and MCP are both
   supported Context7 routes. The CLI can be a lower-overhead fit when the
   harness already exposes shell, but this is not a measured token saving:
   harnesses vary in MCP discovery and schema loading, and retrieved docs use
   model context either way. Complete when the result matches the requested
   library and version.
3. Use connected Context7 MCP tools when CLI is unavailable, blocked, or a
   better fit for the harness. Tool names vary; discover the exposed tools.
   Reuse a known, version-matched library ID when the tool accepts it; otherwise
   resolve the library once, then query its docs. Complete when the result
   matches the requested library and version.
4. If neither Context7 route is available or it has no matching entry, use the
   library's official documentation. State which route supplied the answer;
   for a code change, record any fallback in the handoff. Complete when the
   answer is grounded in retrieved documentation or the missing source is
   reported.
