---
name: find-docs-qu1r0ra
description: Retrieve current library documentation before answering API questions or changing third-party library code, preferring Context7 CLI with MCP and official-documentation fallbacks.
---

# Find Docs qu1r0ra

Follow [`find-docs`](../find-docs/SKILL.md) for query construction, library
resolution, version selection, and documentation retrieval. Apply the owning
repository's documentation contract when present. This wrapper changes only
route choice and the fallback.

- Prefer upstream's CLI flow when shell and Node/npm are already available.
- Use connected Context7 MCP tools when CLI is unavailable, blocked, or a
  better fit. Discover their names and follow their library-resolution contract.
- If Context7 is unavailable, quota-limited, or lacks a matching entry, retrieve
  the library's official documentation. This replaces upstream's training-data
  fallback. Report the route and reason; for code changes, record the fallback
  in the handoff. Installing tooling or setting up authentication requires
  separate authorization.

Completion: the answer cites retrieved documentation for the requested library
and version, or identifies the unavailable source and remaining uncertainty.
