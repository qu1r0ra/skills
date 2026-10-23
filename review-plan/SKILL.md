---
name: review-plan
description: Send a plan or drafted spec to a separate reviewer, then disposition each finding before it is specified or ticketed.
disable-model-invocation: true
---

Review a plan or drafted spec through a separate reviewer, then revise the artifact on its findings.

1. **Name the artifact.** Decide whether it is a **plan** (a design after grilling, with no spec yet) or a **spec** (a drafted spec). **Done when:** the artifact's text or path and its type are stated.

2. **Brief the reviewer.** The brief is self-contained: the artifact, the settled decisions (from grilling or the spec), the check for its type, and the output format. Mark each settled decision "do not re-argue; flag only with concrete evidence." For a plan, check for gaps against the settled decisions, unstated assumptions, and open decisions. For a spec, check the template sections and test-seam decisions. Ask for ranked findings, at most 400 words, read-only. **Done when:** the brief has all four parts.

3. **Dispatch round 1.** Route to the **Plan reviewer** role and use the supported subagent mechanism under the rules and harness mechanics in [model-routing](../../../docs/agents/model-routing.md). Use a native subagent when it can select the routed provider, model, and effort. In T3, use `delegate_task` for cross-provider work or when native subagents cannot run the routed model; give each review round a fresh task and its own `clientRequestId`. On other harnesses, follow the matching adapter. If no available mechanism can meet the route, stop and report the blocked lane. **Done when:** the reviewer's findings are back, or the skill has stopped on a reported blocked lane.

4. **Disposition every finding.** Give each finding exactly one disposition:
   - **accept**: revise the artifact;
   - **reject**: state the reason;
   - **escalate**: the choice belongs to the user.

   **Done when:** every finding has one disposition.

5. **Decide round 2.** A change is **material** when it alters a decision, scope, or requirement; wording and structure changes are not. Run round 2 only when an accepted change is material. Round 2 is a new dispatch with the revised artifact, the prior findings, and the dispositions. Its findings get dispositions too, but no round 3 follows. **Done when:** round 2 is dispositioned, or skipped with the reason stated.

6. **Close out.** Report a table of finding, disposition, and reason. List every rejection so the user can overrule it, and every escalation. An escalation blocks the next step until the user answers. Then name the next step: a plan goes to `/to-spec-qu1r0ra`; a spec is revised in place and republished through that skill's validation. This skill publishes nothing. **Done when:** the table and escalation list are in the message and the next step is named.
