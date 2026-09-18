# Wave 10 Profile #39 — Smart Contract Reentrancy-State Causal Depth Design

**Date:** 2026-09-19  
**Base authority:** `main@21bd3afcb6672dbaec58db79574a0a9822f8e8e1`  
**Canonical skill:** `smart-contract-reentrancy-state-analysis`

## Purpose

Promote `smart-contract-reentrancy-state-analysis` into the thirty-ninth CI-enforced operator-depth profile without changing routing, graph, packs, benchmark authority, agent-eval authority, superiority-court authority, or workflow semantics.

The profile owns callback/reentrant execution causality around smart-contract external calls: transient state exposure, call-stack and callback generations, cross-function/cross-contract reentry, lock scope, update ordering, hook-enabled token callbacks, read-only callback consumption, and outer-call continuation after reentry. It does not own the protocol invariant definition itself (#38), generic thread/task scheduling races (#26), or proxy/implementation/storage-layout upgrade causality (#40).

## Causal model

Every promoted finding must bind one reconstructable tuple:

`protocol/system identity + local chain/environment identity/generation + deployment/configuration identity/generation + contract-set identity/generation + contract/code revision identity + invariant identity/version + outer actor/account identity + outer transaction/call generation + outer entrypoint identity + call-frame/stack generation + pre-call state generation + external-call site identity + external callee/callback target identity/generation + callback authority/capability + callback trigger identity + reentrant entrypoint identity + reentry generation/depth + lock/guard identity/generation + lock scope/domain + transient state identity/generation + expected update/commit ordering + observed callback/interleaving ordering + cross-function/cross-contract path identity + read-only observer identity where relevant + outer-call continuation identity + final commit/terminal point + post-state identity + expected invariant result + observed invariant result + first reentrant causal divergence + downstream protocol/accounting consumer identity + effective reentrancy-state capability + bounded result + receipt/result`

A mere external call or callback is attack surface. Promotion requires proof that the callback can re-enter a relevant path while the exact state/guard generation is transient, that the outer and reentrant frames interact with one invariant domain, and that a downstream state/consumer accepts a wrong intermediate or duplicated effect.

## Required distinctions

Preserve explicitly:

- external call != reentrancy;
- callback reachability != harmful reentrancy;
- reentrant entrypoint reachability != invariant violation;
- invariant violation != exploitable economic loss;
- same-function recursion != unauthorized reentrancy by assumption;
- callback before return != state-ordering defect by itself;
- transient state != invalid terminal state when explicitly permitted;
- checks-effects-interactions heuristic != proof of safety or defect;
- lock present != protected invariant;
- per-function lock != cross-function invariant lock;
- lock acquired != correct lock scope;
- reentrancy guard bypass != complete exploitability;
- token hook support != vulnerability;
- fallback/receive callback != asset-loss proof;
- multicall nesting != reentrancy by itself;
- cross-contract callback != cross-contract invariant break without shared-state binding;
- read-only callback != read-only reentrancy defect until a consumer trusts transient state;
- view function call != harmless by assumption when its result drives another state transition;
- delegatecall/proxy context != reentrancy root cause by assumption;
- callback contract code execution != authority over protocol state;
- callback depth > 1 != stronger evidence by itself;
- gas exhaustion != reentrancy proof;
- revert != proof that no transient observation occurred;
- event emission != committed state;
- duplicate-looking state delta != duplicate effect without generation/commit binding;
- local bounded accounting divergence != real financial loss;
- synthetic callback marker != arbitrary control flow;
- local test-chain exploitability != production reachability;
- fuzzed callback sequence != root cause until minimized and replayed;
- concurrency race != smart-contract reentrancy unless call-stack callback semantics are the causal mechanism.

All dynamic validation remains local/owned/test-chain or explicitly authorized. Use synthetic callback contracts/tokens, bounded recursion (normally depth 1), fake assets, deterministic snapshots, inert markers, read-only observers, and reversible local state.

## Outer transaction, call-frame, and callback generations

Track independently:

- protocol/deployment generation;
- contract/code revision;
- outer actor/account identity;
- outer transaction generation;
- outer entrypoint identity;
- outer call-frame/stack generation;
- state generation before the external call;
- external-call site identity;
- callee/callback target generation;
- callback trigger identity;
- reentry generation/depth;
- reentrant entrypoint;
- lock/guard generation;
- transient state generation;
- outer continuation generation;
- commit/terminal generation.

Do not collapse “same transaction”, “same contract”, or “same function” into one state generation. Reentrant frames can share transaction identity while observing different logical transition phases.

## External-call, callback, and reentrant-entry binding

For each candidate path record:

1. outer entrypoint and preconditions;
2. exact external-call site;
3. state writes completed before the call;
4. state writes intentionally deferred until after return;
5. callee/callback target;
6. callback trigger mechanism: hook, fallback/receive, explicit callback, cross-contract call, token receiver, or equivalent;
7. reentrant entrypoint and parameters;
8. reentry depth/generation;
9. state and authorization observed by the reentrant frame;
10. outer frame continuation after callback returns.

A callback that cannot reach a relevant reentrant entry is not a reentrancy defect.

## Transient-state and update-ordering binding

Bind:

- invariant identity from profile #38;
- transient state fields and generation;
- intended update ordering;
- actual pre-call writes;
- deferred post-call writes;
- state predicate visible during callback;
- first reentrant operation that consumes the transient state;
- outer continuation and final commit.

The central causal question is whether a reentrant frame can act on a state generation that the protocol assumes is not externally observable or actionable at that point.

## Lock, guard, and invariant-scope binding

Record:

- guard/lock identity;
- guard generation or entered/not-entered state;
- functions/contracts covered;
- invariant domain intended to be protected;
- whether nested read-only paths are covered;
- whether cross-function or cross-contract paths bypass the scope;
- reset/release point;
- outer and reentrant frame observations.

Lock present != protected invariant. A per-function guard may be correct for one function and insufficient for a cross-function invariant spanning multiple entrypoints.

## Cross-function, cross-contract, hook, and read-only lineage

Treat separately:

- same-function reentry;
- cross-function reentry;
- cross-contract shared-state reentry;
- token/asset hook callback;
- fallback/receive callback;
- multicall/nested dispatcher;
- proxy/delegate context;
- read-only callback/observer;
- callback into an external dependency that re-enters through another contract.

For read-only reentrancy, a transient read is only an observed divergence until a bounded downstream consumer uses that read to make a protected decision or state transition.

## Outer continuation, commit, and duplicate-effect binding

After callback return, bind:

- outer frame continuation identity;
- state checks repeated or omitted;
- remaining writes;
- accounting/claim/share/debt updates;
- idempotency/duplicate-effect controls;
- final commit/terminal point;
- post-state and invariant result;
- downstream consumer and receipt.

A reentrant call may be reachable but harmless if the outer continuation revalidates current state and commits a correct final state.

## Smart-contract reentrancy evidence ladder

Use SCR0–SCR5 exactly:

- **SCR0 — Reentrancy surface mapped.** External calls, callback mechanisms, reentrant entrypoints, transient state, guards, shared invariants, and outer continuations are mapped.
- **SCR1 — Callback/order divergence observed.** A repeatable callback, reentry, transient-state, lock-scope, or outer-continuation divergence exists without a protected downstream acceptance.
- **SCR2 — Controlled reentrancy-policy mismatch.** A deterministic local fixture proves that a documented update-ordering, guard-scope, or callback-state invariant can be violated by one bounded reentrant path.
- **SCR3 — Inert reentrant wrong-state acceptance.** A synthetic reentrant frame or read-only observer is accepted against transient/wrong-generation state by the protected local consumer.
- **SCR4 — Bounded reversible reentrant effect.** A synthetic balance/share/claim/queue marker, duplicate inert effect, or reversible local transition is causally bound to the exact outer-call/callback/reentry/guard/state tuple.
- **SCR5 — Regression-verified causal reentrancy proof.** SCR4 plus complete outer/reentrant frame provenance, callback trigger, transient-state and guard-scope trace, first reentrant causal divergence, outer-continuation/commit binding, meaningful counterfactuals, eliminated alternatives, receipt/result binding, and remediation replay.

External-call presence, callback logs, guard absence, hook support, local reverts, state deltas, or synthetic markers cannot skip missing causal bindings.

## Deterministic benign review cases

Freeze at least:

1. `cross-function-callback-consumes-transient-accounting-state` — outer synthetic withdrawal exposes transient accounting before an inert callback re-enters a second function sharing the same invariant.
2. `per-function-guard-misses-cross-function-invariant` — a guard covers the outer function but a second function touching the same shadow ledger remains callable during the callback.
3. `hook-enabled-token-callback-before-balance-commit` — a fake hook token triggers a depth-1 callback before internal synthetic balance state is committed.
4. `read-only-callback-observer-consumes-transient-share-state` — a read-only callback sees a transient synthetic share/accounting value and a local mock consumer uses it for a bounded protected decision.

No attack deployment against live protocols, real asset movement, unbounded recursion, gas griefing, or public-chain transaction is required.

## Counterfactual requirements

Change exactly one causal variable while holding deployment, actors, callback target, and invariant constant, such as:

- commit relevant state before versus after external call;
- guard scoped to one function versus the shared invariant domain;
- callback enabled versus same callee with callback disabled;
- reentrant entrypoint allowed versus denied while outer flow is otherwise identical;
- read-only transient value consumed versus ignored/revalidated;
- outer continuation revalidates current state versus trusts pre-callback assumptions.

Generic recursion depth changes or random transaction order are not sufficient for SCR5 unless they isolate the causal callback/state edge.

## Alternative explanations

Before SCR4/SCR5 eliminate:

- callback cannot reach the claimed reentrant entrypoint;
- transient state is documented and safe to expose;
- invariant permits the intermediate observation;
- outer continuation revalidates and prevents wrong commit;
- duplicate-looking effect belongs to another transaction/generation;
- guard scope intentionally excludes a state domain not shared with the callback path;
- callback mock violates the documented token/callee contract;
- accounting invariant itself was specified incorrectly;
- generic concurrency/race semantics, not smart-contract callback stack semantics, explain the behavior;
- oracle/external-data state independently explains the consumer result;
- upgrade/proxy/storage-layout behavior independently explains the path;
- authorization state independently grants the reentrant operation;
- receipt belongs to another deployment, chain reset, or callback generation.

Any unresolved material alternative caps evidence at SCR2.

## Ownership boundaries

- `smart-contract-reentrancy-state-analysis` owns external-call/callback/reentrant-frame causality, transient state, guard scope, cross-function/cross-contract path binding, and outer continuation after callback.
- `smart-contract-invariant-analysis` owns the protocol invariant identity, accounting domain, and final invariant witness.
- `concurrency-race-analysis` owns generic thread/task/scheduler interleavings outside smart-contract callback semantics.
- `smart-contract-upgradeability-analysis` owns proxy/implementation/storage-layout/initializer/governance transition causality.
- authorization and external-data profiles own those roots when they independently explain the behavior.

## Expected repository scope

1. `README.md`
2. `docs/operator-depth-contract.md`
3. `docs/superpowers/plans/2026-09-19-wave10-smart-contract-reentrancy-depth.md`
4. `docs/superpowers/specs/2026-09-19-wave10-smart-contract-reentrancy-depth-design.md`
5. `operator-depth/profiles.json`
6. `skills/smart-contract-reentrancy-state-analysis/SKILL.md`
7. `skills/smart-contract-reentrancy-state-analysis/references/operator-review-cases.json`
8. `skills/smart-contract-reentrancy-state-analysis/references/operator-runbook.md`
9. `tests/test_smart_contract_reentrancy_depth.py`
10. `tests/test_smart_contract_invariant_depth.py` only if CI proves its exact global-count assertion is the sole extensibility defect.

Do not change `skill.meta.json`, graph edges, packs, routing domains, benchmark authority, agent-eval authority, superiority-court authority, or workflow semantics.

## Success criterion

Profile #39 is complete only when the merge tree contains exactly 39 profiles, exactly one valid `smart-contract-reentrancy-state-analysis` entry, SCR0–SCR5 is published, exact-head and post-merge CI are fully GREEN, merge parents are verified, and final scope remains bounded to the intended paths.
