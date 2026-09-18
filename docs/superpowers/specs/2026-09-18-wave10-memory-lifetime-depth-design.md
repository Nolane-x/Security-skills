# Wave 10 Profile #25 — Memory Lifetime Causal Depth Design

**Date:** 2026-09-18  
**Base authority:** `main@52796d72dd1a4d2094b433e14f2b51302a7c40b6`  
**Canonical skill:** `memory-lifetime-analysis`

## Purpose

Promote the existing canonical `memory-lifetime-analysis` skill into the twenty-fifth CI-enforced operator-depth profile without creating a duplicate memory-safety capability.

The profile must deepen causal lifetime reasoning. A sanitizer report, crash, freed address, stale-looking handle, refcount anomaly, or reused allocation is not by itself proof of a security-relevant lifetime violation. Evidence must bind one logical object/resource identity through acquisition, ownership/alias state, invalidation/destruction, reuse generation, asynchronous work, final consumer, bounded consequence, and remediation.

## Scope

This is a bounded depth promotion of an existing canonical skill.

Production behavior is limited to:

- deepening `skills/memory-lifetime-analysis/SKILL.md`;
- adding `references/operator-runbook.md`;
- adding deterministic benign `references/operator-review-cases.json`;
- adding exactly one operator-depth registry entry;
- adding one dedicated profile #25 test;
- minimally repairing the profile #24 global-count assertion if it still freezes the registry at exactly 24;
- publishing README and operator-depth-contract documentation only after behavioral GREEN.

No changes are intended to:

- `skill.meta.json`;
- graph edges;
- packs;
- routing domains;
- benchmark fixtures or thresholds;
- cross-agent evaluation authority;
- superiority-court authority;
- workflow semantics.

## Relationship to adjacent canonical skills

This profile owns lifetime causality, not every memory-safety root cause.

- `bounds-and-integer-analysis` owns arithmetic/range root causes.
- `type-confusion-analysis` owns runtime/type-identity invariant failures.
- `concurrency-race-analysis` owns unsafe interleavings and happens-before gaps.
- `sanitizer-guided-memory-analysis` owns instrumentation-assisted observation.
- `exploitability-triage` owns downstream impact assessment after a validated primitive.
- `memory-lifetime-analysis` owns the proof that a logically dead, duplicated, retired, or wrong-generation reference is consumed under the wrong lifetime authority.

## Causal memory-lifetime model

The canonical chain is:

`logical object/resource identity -> allocation/acquisition generation -> owner and alias set -> retain/borrow/refcount state -> invalidation/retirement event -> destruction/release generation -> address/handle reuse generation -> asynchronous callback/work-item identity -> final consumer identity -> effective stale/double-use capability -> bounded result/receipt -> lifecycle generation`

A profile claim must preserve every material identity and generation relevant to the hypothesis.

## Required distinctions

The skill and runbook must make these separations explicit:

- address/handle equality != logical object identity;
- allocation success != ownership authority;
- borrowed reference != retained ownership;
- alias reachability != lifetime validity;
- refcount nonzero != correct ownership provenance;
- object invalidated != memory necessarily freed;
- memory freed != stale alias necessarily consumed;
- memory reused != proof the stale reference reached the new object;
- callback queued != callback authorized after retirement;
- cancellation requested != queued work revoked;
- destructor executed != every alias cleared;
- double release signal != security-relevant effect;
- sanitizer report != complete causal lifetime proof;
- crash != exploitability;
- stale-read marker != arbitrary code execution;
- result success != receipt/result binding.

## Identity and lifetime model

Each bounded experiment records at minimum:

- logical object/resource fixture identity;
- allocation/acquisition site and generation;
- primary owner and ownership-transfer state;
- borrowed/retained/weak/global/cache/callback aliases;
- retain/release/refcount transitions when applicable;
- invalidation/retirement event;
- destruction/free/close/unmap generation;
- address/handle reuse generation when applicable;
- callback/work-item/task identity and enqueue generation;
- cancellation/teardown/error-path state;
- final consumer identity;
- effective capability exercised using the reference;
- bounded result and correlated receipt;
- remediation generation.

## Invariants

### ML-I1 — Logical identity binding

A reference valid for logical object generation N must not be treated as authority for a later object merely because an address, slot, or handle value is reused.

### ML-I2 — Ownership/alias binding

Each use or release must be justified by the current owner/borrow/retain contract for that exact object generation.

### ML-I3 — Invalidation convergence

Retirement, close, cancellation, container removal, or equivalent invalidation must revoke aliases and queued work according to the documented lifetime boundary.

### ML-I4 — Single release authority

Exactly the documented owner/release path may consume a release responsibility; retries, error paths, callbacks, and teardown must not duplicate it.

### ML-I5 — Async generation binding

Queued callbacks, futures, completions, iterators, or worker items must revalidate object/lifecycle generation before consuming retired state.

### ML-I6 — Result provenance

A bounded marker or read-only state transition proves only the exact object/alias/generation/consumer tuple captured by its receipt.

## Evidence ladder — ML0 through ML5

### ML0 — Lifetime surface mapped

Constructors/acquisition, owners, aliases, release paths, callbacks, consumers, and teardown/lifecycle transitions are enumerated. No violation is claimed.

### ML1 — Lifetime divergence observed

A reproducible alias, refcount, ownership, invalidation, reuse, or generation divergence is observed, but final wrong-lifetime acceptance is not established.

### ML2 — Lifetime-policy mismatch

A controlled experiment demonstrates that a stale, duplicate, retired, or wrong-generation reference survives a lifetime policy boundary. This is not yet a final consumer consequence.

### ML3 — Inert wrong-lifetime acceptance

The final synthetic consumer accepts the wrong-lifetime reference and exposes only an inert/read-only oracle.

### ML4 — Bounded reversible lifetime effect

A bounded reversible owner-controlled marker, synthetic object transition, or read-only result is causally bound to the exact object/alias/release/reuse/consumer generation tuple.

### ML5 — Regression-verified causal lifetime proof

ML4 plus complete object identity, allocation/acquisition generation, ownership/alias provenance, invalidation/destruction trace, reuse generation where relevant, callback/work-item identity, refcount state, final consumer, effective capability, lifecycle evidence, counterfactuals, eliminated alternative explanations, receipt/result binding, and remediation regression.

Sanitizer output, a free/access stack pair, a crash, address reuse, refcount underflow, queued callback, or stale-looking pointer cannot skip missing causal bindings.

## Counterfactual strategy

Each case changes one material causal variable while holding others stable.

Examples:

- same callback/work item, current versus retired object generation;
- same numeric address/handle value, original versus deliberately reused logical object generation;
- same release path, one versus duplicated ownership responsibility;
- same completion event, before versus after cancellation/teardown generation;
- same alias, retained versus borrowed contract;
- same stale reference with inert consumer versus consumer fenced by generation check.

If two authoritative variables change, split the experiment before promoting evidence.

## Alternative explanations

Before ML4/ML5, explicitly eliminate:

- stale logs or receipts from a neighboring run;
- allocator poisoning/quarantine artifact mistaken for production lifetime behavior;
- harness-owned alias not present in the target;
- sanitizer instrumentation materially changing timing or retention;
- intended resurrection or documented retain semantics;
- address reuse without stale-reference consumption;
- duplicate cleanup that is idempotent by contract;
- cancellation that intentionally permits completion;
- unrelated concurrent object using the same numeric handle;
- debug-only delayed destruction;
- crash before the hypothesized final consumer;
- a concurrency bug whose lifetime consequence has not been independently bound.

If a material alternative remains plausible, evidence stays at or below ML2.

## Deterministic benign review cases

At least these four case IDs are required:

1. `stale-callback-after-retirement`
   - same synthetic callback across current and retired object generations;
   - inert counter/marker only;
   - proves whether queued work revalidates lifecycle generation.

2. `address-reuse-object-identity-confusion`
   - deterministic synthetic slot/handle reuse with two logical objects;
   - read-only consumer;
   - proves numeric identity reuse is not mistaken for object authority.

3. `duplicate-release-refcount-generation`
   - synthetic owner/retain/release ledger;
   - no real allocator corruption;
   - proves duplicated release responsibility or stale refcount generation is rejected.

4. `cancellation-completion-teardown-race`
   - deterministic barriers around cancel/complete/teardown;
   - inert completion sink;
   - proves retired work cannot consume the destroyed generation.

Every case includes positive and negative controls, explicit stop condition, remediation oracle, counterfactual, alternative explanation, ML evidence level and ML evidence ceiling.

## Runbook methodology

Required sections include the common operator-depth sections plus:

- Object identity and allocation-generation trace
- Ownership and alias trace
- Retain, borrow, and refcount trace
- Invalidation and destruction trace
- Address and handle reuse trace
- Callback and asynchronous-work trace
- Cancellation, teardown, and error-path trace
- Final consumer and effective capability trace
- Counterfactual controls
- Alternative explanations
- Evidence promotion and ceiling

## Safety boundary

Dynamic validation is restricted to:

- local/owned/sandboxed/explicitly authorized builds;
- synthetic object pools, handles, slots, refcount ledgers, callbacks, queues, and work items;
- inert counters/markers and read-only synthetic consumers;
- deterministic barriers and bounded reversible state;
- sanitizers/debug traces only when they do not expand impact.

Explicitly out of scope:

- unrelated production processes or hosts;
- production credentials/secrets;
- persistence;
- arbitrary code execution as a proof requirement;
- privilege escalation as a proof requirement;
- weaponized heap shaping;
- destructive memory corruption;
- malware;
- evasion;
- unauthorized targets.

## TDD and release gates

1. Commit this design.
2. Commit the implementation plan.
3. Add the dedicated #25 test before production artifacts.
4. Open a Draft PR at the exact test-first SHA.
5. Require RED with existing gates green and only intended new profile semantics failing.
6. Implement SKILL/runbook/review-cases/registry and only the minimal prior-profile count compatibility fix if required.
7. Do not change the dedicated #25 test after valid RED.
8. Require full behavioral 9/9 GREEN.
9. After behavioral GREEN, change only README and operator-depth contract.
10. Prove post-behavioral delta is exactly two paths.
11. Require exact-head 9/9 GREEN.
12. Fresh-check main/base/head/scope/mergeability.
13. Guarded merge with `expected_head_sha`.
14. Require post-merge 9/9 GREEN on the exact merge SHA.
15. Verify registry/README/contract directly on the merge tree.
16. Record closure provenance.

## Success criteria

Profile #25 is complete only when the merge-tree registry has exactly 25 profiles with one valid `memory-lifetime-analysis` entry, README and operator-depth contract publish ML0–ML5 semantics, exact-head and post-merge CI are fully green, and closure provenance is recorded without claiming external-system superiority.
