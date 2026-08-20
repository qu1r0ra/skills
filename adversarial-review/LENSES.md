# Adversarial Review Challenge Lenses

Standard challenge lenses for the generalized `adversarial-review` skill. The parent agent extracts the 1–2 relevant lens sections based on payload type and injects them directly into the isolated subagent's challenge block.

---

## Lens: architecture-spec

Apply when reviewing architectural proposals, system designs, ADRs, schemas, API contracts, or skill definitions.

### Focus Probes
1. **Invariant Breaches & Contract Drift**: Does this proposal violate core system constraints, existing architectural patterns, or interface contracts?
2. **Untrusted Data & Isolation Boundaries**: Does this proposal handle external/imported content with clear boundary sanitization, preventing unintended code/prompt injection or state pollution?
3. **Unstated Assumptions & Lifecycle Gaps**: What assumptions regarding state persistence, lifecycles, concurrency, or failure recovery are taken for granted without an explicit mechanism?
4. **Premature Abstraction & Over-Engineering**: Does this introduce unnecessary layers, indirection, metadata fields, or extensibility hooks that solve hypothetical future problems at the expense of simplicity?
5. **Irreversibility & Migration Traps**: If this design proves inadequate, what is the blast radius and cost of reversing or refactoring it? Are migration and deprecation paths defined?
6. **Ergonomic Friction**: How cumbersome will this design be for developers or autonomous agents to maintain, extend, and conform to over time?

### Falsification Heuristic
Construct a concrete edge-case system state, concurrent sequence, or payload that breaks invariant guarantees, causes deadlock, or leaks state across isolation boundaries.

---

## Lens: code-diff

Apply when reviewing code changes, pull requests, refactors, or new modules across any language/stack.

### Focus Probes
1. **Concurrency & Race Conditions**: Does this code handle re-entrancy, async execution order, or shared mutable state safely?
2. **Input Sanitization & Injection Hazards**: Are external inputs, file paths, shell arguments, and environment variables sanitized against traversal, injection, or unexpected types?
3. **Unhandled Error Paths & Boundary Conditions**: What happens on empty inputs, malformed data, filesystem/network timeouts, missing permissions, or invalid states?
4. **Backward Compatibility & Regression Traps**: Does this break existing caller contracts, CLI interfaces, schema validators, or serialization formats without migration handling?
5. **Performance Traps & Resource Leaks**: Are there unbounded memory allocations, quadratic loops, unclosed handles/connections, or blocking operations in fast paths?
6. **Testing Blind Spots**: Are accompanying tests purely confirmatory (happy-path) rather than probing error branches, edge conditions, and failure modes?

### Falsification Heuristic
Provide a minimal reproduction snippet, failing test case, or input payload that triggers an unhandled exception, state corruption, resource leak, or regression.

---

## Lens: plan-workflow

Apply when reviewing implementation plans, sysadmin runbooks, migration steps, remote-access setups, or multi-step execution recipes.

### Focus Probes
1. **Dependency Ordering Hazards**: Are prerequisites accurately ordered, or are tasks scheduled before their underlying infrastructure, data structures, or credentials exist?
2. **Unverified Critical Paths**: Which steps in the plan lack concrete, checkable verification gates (unit tests, CLI sanity checks, or live smoke tests) before declaring success?
3. **Premature Completion Temptations**: Does the plan permit declaring victory based solely on file creation or syntax compliance rather than runtime behavioral validation?
4. **Rollback & Blast-Radius Deficits**: If an intermediate step fails catastrophically, can the system cleanly recover, or will it be left in a half-configured, unrecoverable state?
5. **Operational & Environment Assumptions**: What implicit assumptions are made about environment state (e.g., active user sessions, screen locking, power sleep states, network NAT traversal, background service persistence, auth tokens)?
6. **Context Overload & Step Sprawl**: Does the plan overload execution context with unbounded tool dumps instead of targeted inspection and focused subagent delegation?

### Falsification Heuristic
Identify an execution failure scenario where an intermediate step fails, unhandled environment state causes silent failure, or missing verification allows a critical defect to slip through.

---

## Lens: research-claim

Apply when reviewing research syntheses, technical evaluations, benchmarking reports, or evidence-backed findings.

### Focus Probes
1. **Citation & Provenance Validity**: Are claims backed by authoritative primary sources and verifiable facts, or do they rely on secondary interpretations and circular reasoning?
2. **Confirmation Bias & Omitted Counter-Evidence**: Does the synthesis selectively present supporting facts while ignoring known counter-examples, trade-offs, or competing approaches?
3. **Over-Generalization**: Are conclusions drawn from narrow benchmarks, synthetic tests, or specific scenarios inappropriately generalized to broad architectural rules?
4. **Stale Information**: Do the underlying findings reflect outdated software versions, superseded APIs, or deprecated platform behaviors?
5. **Ambiguous Terminology**: Are key terms used equivocally or in conflict with established industry/domain definitions?

### Falsification Heuristic
Cite a specific counter-example, primary documentation section, or reproducible benchmark that directly contradicts or undermines the asserted claim.
