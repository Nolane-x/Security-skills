# Wave 10 Profile #26 — Concurrency Race Depth Design

## Objective

Promote `concurrency-race-analysis` into the twenty-sixth CI-enforced operator-depth profile without duplicating `memory-lifetime-analysis`, `authorization-boundary-analysis`, sanitizer observation, protocol-state reasoning, or exploitability triage.

The profile must turn “timing-sensitive bug” into a causal proof over exact actor identities, shared-state generation, scheduler/interleaving state, synchronization edges, check/use epochs, cancellation/teardown transitions, final consumer identity, bounded effect, and remediation ordering.

## Why this profile is next

Profile #25 closed lifetime identity/ownership/generation reasoning. The highest-value adjacent gap is the ordering layer that can invalidate otherwise correct ownership or authorization assumptions. `concurrency-race-analysis` is reused across memory-safety, kernel/browser/sandbox, virtualization, protocol, and smart-contract packs, so deepening it adds orthogonal causal semantics rather than another domain-specific checklist.

## Ownership boundary

This profile owns unsafe interleavings and missing/insufficient happens-before relations.

Neighbor responsibilities remain separate:

- `memory-lifetime-analysis` owns logical object lifetime, ownership, alias, reuse, callback, and stale-generation authority.
- `authorization-boundary-analysis` owns principal/resource/action policy decisions.
- `sanitizer-guided-memory-analysis` owns instrumentation-assisted observation.
- `protocol-state-machine-analysis` owns legal protocol-state transitions independent of scheduling.
- `exploitability-triage` owns downstream impact after a validated primitive.
- `concurrency-race-analysis` owns the proof that two or more actors can reach a forbidden shared-state transition because required ordering, atomicity, serialization, revalidation, or cancellation synchronization is absent or ineffective.

## Causal concurrency model

Every promoted finding must bind this tuple:

`shared invariant + shared object/state identity + state generation + actor identities + actor operation generations + scheduler/executor identity + synchronization primitive/epoch + precondition/check observation + interfering transition + use/commit transition + happens-before relation + cancellation/teardown generation + final consumer + effective concurrent capability + bounded result + receipt`

A race claim is incomplete unless the exact forbidden interleaving is stated and the missing or ineffective ordering edge is identified.

## Required distinctions

The profile must explicitly preserve:

- data race != higher-level race;
- atomic access != atomic invariant;
- lock present != protected operation;
- thread/task overlap != harmful interleaving;
- timing correlation != causal schedule;
- TOCTOU window != demonstrated stale decision use;
- cancellation requested != work revoked;
- queue order != execution order unless guaranteed;
- retry overlap != duplicate effect unless final consumer proves it;
- deadlock/livelock != safety violation;
- sanitizer race report != complete causal concurrency proof;
- crash != exploitability.

## Concurrency evidence ladder — CR0 through CR5

### CR0 — Surface mapped

Actors, shared states, synchronization primitives, queues/executors, lifecycle transitions, and candidate invariants are enumerated. No race is claimed.

### CR1 — Ordering divergence observed

A reproducible ordering, generation, visibility, ownership, cancellation, or revalidation divergence is observed, but a forbidden final transition is not yet established.

### CR2 — Controlled synchronization-policy mismatch

A deterministic barrier/schedule experiment demonstrates that the documented ordering/atomicity/revalidation contract can be violated under a specific interleaving.

### CR3 — Inert wrong-order acceptance

The final synthetic/read-only consumer accepts stale, duplicated, or otherwise wrong-order state under the controlled interleaving.

### CR4 — Bounded reversible concurrent effect

A bounded reversible owner-controlled marker, synthetic state transition, duplicate inert action, or read-only result is causally bound to the exact actors/interleaving/generation/synchronization tuple.

### CR5 — Regression-verified causal concurrency proof

CR4 plus complete actor/state/generation provenance, scheduler/executor identity, synchronization and happens-before trace, check/use or transition ordering, lifecycle/cancellation state, final consumer, counterfactual schedules, eliminated alternative explanations, receipt/result binding, and remediation regression.

No sanitizer output, trace timestamp, sleep-based reproduction, queue log, lock acquisition log, crash, or flaky failure may skip missing causal bindings.

## Invariants

### CR-I1 — Shared-state identity

Every actor observation and mutation must bind to the same logical shared-state generation before an interleaving is promoted.

### CR-I2 — Required ordering

The invariant must state the minimal required happens-before/serialization/revalidation edge. “Needs a lock” is not specific enough.

### CR-I3 — Check/use generation

When a decision is separated from its use, the consumed state must be proven to be the same authorized/current generation or explicitly revalidated.

### CR-I4 — Single-effect authority

Retries, completions, callbacks, competing workers, or cancellation paths must not produce duplicate final effects unless the contract explicitly allows idempotent repetition.

### CR-I5 — Cancellation/teardown convergence

Cancellation, shutdown, invalidation, timeout, and teardown generations must converge so retired work cannot commit through a stale execution epoch.

### CR-I6 — Result provenance

A bounded result proves only the exact actor/interleaving/state/synchronization tuple captured by its receipt.

## Deterministic benign review cases

At least these four scenarios are required:

1. `check-use-generation-race`
   - two synthetic actors;
   - explicit barrier between check and use;
   - one actor changes the guarded generation;
   - inert/read-only final consumer proves whether revalidation occurs.

2. `duplicate-completion-single-effect`
   - competing synthetic completion paths;
   - controlled barrier makes both observe pre-commit state;
   - inert ledger proves whether exactly one effect is committed.

3. `cancellation-commit-epoch-race`
   - synthetic cancellation and completion actors;
   - deterministic lifecycle epoch transition;
   - bounded sink proves retired work cannot commit after cancellation generation.

4. `publication-initialization-order-race`
   - synthetic publisher/reader;
   - explicit publication barrier controls visibility;
   - read-only structured marker proves whether partially initialized state becomes consumable.

Every case must include positive and negative controls, an explicit stop condition, remediation oracle, counterfactual schedule, alternative-explanation check, and CR evidence level/ceiling.

## Runbook methodology

The runbook must include the six common operator-depth sections plus:

- Shared invariant and state-generation trace
- Actor and operation-generation trace
- Synchronization and happens-before trace
- Check/use and commit-point trace
- Queue, executor, and publication trace
- Cancellation, retry, and teardown trace
- Final consumer and single-effect trace
- Deterministic schedule control
- Counterfactual schedules
- Alternative explanations
- Evidence promotion and ceiling

## Safety boundary

Dynamic validation is restricted to local, owned, sandboxed, benchmark/CTF, simulated, or explicitly authorized environments.

Preferred mechanisms:

- synthetic actors/tasks;
- deterministic barriers and scheduler hooks;
- mock queues/executors;
- fake ledgers and inert action sinks;
- read-only structured fixtures;
- bounded reversible owner-controlled markers;
- instrumentation used only for observation, not impact escalation.

Explicitly out of scope as proof requirements:

- uncontrolled production stress;
- unrelated production systems;
- denial-of-service;
- destructive corruption;
- arbitrary code execution;
- privilege escalation;
- persistence;
- credential theft;
- malware;
- evasion;
- unauthorized targets.

## Registry and release constraints

- Preserve 83 canonical skills and 20 packs.
- Keep `operator-depth/profiles.json` schema version 2.
- Do not modify `skill.meta.json`, graph edges, packs, routing domains, benchmark authority, agent-eval authority, superiority-court authority, or workflow semantics.
- Commit the dedicated #26 test before production artifacts and do not weaken it after valid RED.
- After behavioral GREEN, only `README.md` and `docs/operator-depth-contract.md` may change before exact-head verification.
- Final intended scope is nine paths unless the previous profile contains a stale exact global-count assertion, in which case one minimal compatibility-test edit is permitted.

## Completion criteria

Profile #26 is complete only when:

1. the dedicated test first produces intentional RED;
2. the canonical skill, runbook, review cases, and registry satisfy the frozen causal contract;
3. full behavioral CI is 9/9 GREEN;
4. public docs publish profile #26 and CR0–CR5 only after behavioral GREEN;
5. exact-head CI is 9/9 GREEN;
6. guarded merge lands the exact reviewed head;
7. post-merge CI is 9/9 GREEN;
8. merge-tree verification confirms exactly one `concurrency-race-analysis` profile and no unintended graph/pack/evaluation/workflow change.
