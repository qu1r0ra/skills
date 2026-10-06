# Codex harness adapter

Operational rules when running under the Codex harness.

## Implementation workers

Read the active AIOS checkout's `docs/agents/model-routing.md` before every
dispatch. Use the actual child-worker API with explicit `model` and reasoning
effort controls for exploration, implementation, merging, and repair roles.
In the collaboration API, these are `model` and `reasoning_effort`; use a fresh
or bounded context fork when a full-history fork cannot accept overrides.
Check the current API's selectors and effort support before dispatch.

Give writing workers their exact worktree and integration base; launching a
worker does not itself establish Git isolation. Exploration may return notes
for the parent to save. Implementation and merger workers return commits and
verification evidence; one writer owns the integration checkout at a time.
Record the resolved model and effort, including any blocked lane. Continue
through parent-owned integration, review, and delivery.

## Independent review

Use the harness's actual leaf-subagent primitive for code review. Reviewers are
read-only leaf workers: they do not create tasks, chats, threads, forks,
worktrees, branches, handoffs, or further reviewers.

In Codex, use a true subagent worker when available; visible Codex tasks,
chats, forks, and threads are not reviewer substitutes. If the worker is
unavailable, preserve that review lane as blocked and record the unavailable
worker; the parent may continue deterministic verification but cannot claim the
missing independent review.

## Reviewer configuration

Read `docs/agents/model-routing.md` before dispatching. For each Standards or
Spec review and re-review, pass the exact model and effort pair listed there
for Codex, using the worker API's explicit model and reasoning-effort controls.

If the pinned pair is unavailable or rejected, preserve the affected review
lane as blocked rather than substituting another selector. Record the resolved
model and effort for every dispatched worker.

Completion: every dispatched review worker resolves to the exact Codex pair
listed in `model-routing.md`, and its resolved values are recorded.
