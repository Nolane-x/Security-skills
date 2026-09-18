# Smart Contract Reentrancy-State Operator Runbook

Use this runbook only on local/owned test chains, isolated forks with no live transaction capability, benchmark/CTF fixtures, simulated environments, or explicitly authorized audit deployments. Use depth-1 synthetic callbacks by default, fake hook tokens, bounded test balances, deterministic state snapshots, read-only observers, shadow ledgers, and reversible local state. Do not deploy attack contracts against live protocols, move real assets, use unbounded recursion, or perform gas/resource griefing.

## Attack surface

Map:

- protocol/deployment and contract revisions;
- invariant identity and shared state domain;
- outer transaction and entrypoint;
- external-call sites and callback targets;
- callback trigger mechanisms;
- reentrant entrypoints;
- call-frame and reentry generations;
- transient state visible during callback;
- locks/guards and their scopes;
- cross-function/cross-contract shared state;
- hook-enabled token paths;
- read-only observers;
- outer continuation and final commit.

## Hypothesis matrix

| Hypothesis | Safe oracle | Control |
| --- | --- | --- |
| callback consumes transient accounting through another function | depth-1 synthetic callback and shadow ledger | same outer flow with state committed before callback |
| per-function guard misses shared invariant | local fake callback into a second guarded/unprotected entrypoint | invariant-scoped guard blocks both paths |
| token hook fires before balance commit | fake hook token returns inert marker and re-enters once | non-hook token or pre-call balance commit |
| read-only callback observes transient share state | read-only observer plus local mock consumer | consumer revalidates after callback before protected decision |

## Outer-transaction/call-frame/callback-generation trace

Record:

- protocol/deployment generation;
- contract/code revision;
- invariant identity/version;
- outer actor;
- outer transaction generation;
- outer entrypoint;
- outer call frame;
- pre-call state generation;
- external-call site;
- callee/callback target generation;
- callback trigger;
- reentry generation/depth;
- reentrant call frame;
- transient state generation;
- outer continuation and commit generation.

Same transaction is not the same call frame or logical state generation.

## External-call/callback/reentrant-entry trace

Capture:

1. outer entrypoint and preconditions;
2. exact external call;
3. writes completed before the call;
4. deferred writes;
5. callback target and trigger;
6. callback authority/capability;
7. reentrant entrypoint and parameters;
8. reentry depth/generation;
9. state/authorization visible to the reentrant frame;
10. outer continuation after callback return.

A callback that cannot reach the claimed reentrant entrypoint is not a reentrancy witness.

## Transient-state/update-ordering trace

Record:

- shared invariant and state fields;
- expected update ordering;
- actual pre-call writes;
- deferred post-call writes;
- transient state generation;
- predicate visible during callback;
- first reentrant operation consuming transient state;
- observed callback/interleaving ordering;
- final committed state.

Separate a permitted transient state from one that becomes security-relevant through a protected consumer.

## Lock/guard/invariant-scope trace

Record:

- lock/guard identity/generation;
- entered state;
- functions/contracts covered;
- invariant scope/domain;
- cross-function coverage;
- cross-contract coverage;
- read-only observer coverage if relevant;
- reset/release point;
- outer/reentrant observations.

Lock presence is not proof that the complete invariant is protected.

## Cross-function/cross-contract/hook/read-only trace

Classify the path:

- same-function;
- cross-function;
- cross-contract;
- token/asset hook;
- fallback/receive;
- dispatcher/multicall;
- proxy/delegate context;
- read-only observer;
- dependency callback through another contract.

For read-only paths, record the consumer that trusts the transient read. Observation alone is not a protected effect.

## Outer-continuation/commit/duplicate-effect trace

After callback return capture:

- outer continuation identity;
- stale assumptions reused;
- checks repeated or omitted;
- remaining accounting/claim/share/debt writes;
- idempotency or duplicate-effect controls;
- final commit;
- post-state;
- invariant result;
- bounded downstream consumer effect;
- receipt/result.

If the outer frame revalidates and commits a correct final state, do not promote the callback path beyond the evidence.

## Controlled validation

Use:

- local test chains with deterministic resets;
- synthetic caller/callback contracts;
- callback depth capped to one unless a deeper bounded level is necessary for a specific invariant;
- fake hook tokens with fixed behavior;
- synthetic balances/shares/claims;
- shadow ledgers;
- deterministic state snapshots;
- read-only observers and mock consumers;
- reversible local markers.

Recommended sequence:

1. freeze deployment, state, actor, invariant, and callback target;
2. establish a non-callback or correctly ordered positive control;
3. enable exactly one callback path;
4. record outer pre-call state and guard state;
5. trigger one bounded callback;
6. record reentrant entry and state observed;
7. locate the first protected consumer accepting transient state;
8. trace outer continuation and final commit;
9. apply the minimal ordering/guard/revalidation fix;
10. replay from the same snapshot.

## False-positive controls

Eliminate:

- callback cannot reach the target entrypoint;
- transient state is explicitly safe;
- shared invariant is incorrectly defined;
- outer continuation revalidates;
- duplicate marker belongs to another transaction;
- guard scope intentionally excludes the callback path;
- fake token/callback violates its documented contract;
- read-only observation is never consumed;
- generic concurrency independently explains the behavior;
- oracle/external-data state independently explains it;
- upgrade/proxy state independently explains it;
- authorization explicitly permits the reentrant operation.

## Counterfactual reentrancy controls

Hold deployment, invariant, actor, callback target, and outer operation constant while changing one variable:

- commit state before versus after external call;
- per-function guard versus invariant-scoped guard;
- callback enabled versus disabled;
- reentrant entry allowed versus denied;
- transient read consumed versus revalidated;
- outer continuation trusts stale assumption versus rechecks state.

Do not treat generic recursion-depth changes or random transaction order as causal controls.

## Alternative explanations

Before SCR4/SCR5 explicitly reject:

- callback cannot reach the claimed entrypoint;
- intermediate state is intentionally exposed;
- invariant allows the observation;
- outer frame prevents final wrong commit;
- duplicate effect is from another generation;
- guard coverage is correct for the actual state domain;
- mock callee violates its intended semantics;
- underlying invariant specification is wrong;
- generic concurrency is the real cause;
- oracle/external-data state is the real cause;
- upgrade/proxy state is the real cause;
- authorization independently allows the action;
- receipt belongs to another chain reset/deployment/callback generation.

Unresolved material alternatives cap evidence at SCR2.

## Evidence capture

Capture one tuple:

`protocol/system identity + local chain/environment identity/generation + deployment/configuration identity/generation + contract-set identity/generation + contract/code revision identity + invariant identity/version + outer actor/account identity + outer transaction/call generation + outer entrypoint identity + call-frame/stack generation + pre-call state generation + external-call site identity + external callee/callback target identity/generation + callback authority/capability + callback trigger identity + reentrant entrypoint identity + reentry generation/depth + lock/guard identity/generation + lock scope/domain + transient state identity/generation + expected update/commit ordering + observed callback/interleaving ordering + cross-function/cross-contract path identity + read-only observer identity where relevant + outer-call continuation identity + final commit/terminal point + post-state identity + expected invariant result + observed invariant result + first reentrant causal divergence + downstream protocol/accounting consumer identity + effective reentrancy-state capability + bounded result + receipt/result`

Useful artifacts include call traces, state snapshots, guard-state receipts, callback-generation markers, shadow-ledger diffs, read-only observer outputs, and remediation replay receipts.

## Evidence promotion and ceiling

### SCR0 — Reentrancy surface mapped

External calls, callbacks, reentrant entries, transient state, guards, shared invariants, and outer continuations are known.

### SCR1 — Callback/order divergence observed

A repeatable callback, reentry, transient-state, lock-scope, or continuation divergence exists without protected downstream acceptance.

### SCR2 — Controlled reentrancy-policy mismatch

A deterministic local fixture proves update-order, guard-scope, or callback-state policy can be violated by one bounded reentrant path.

### SCR3 — Inert reentrant wrong-state acceptance

A synthetic reentrant frame or read-only observer is accepted against transient/wrong-generation state by a protected local consumer.

### SCR4 — Bounded reversible reentrant effect

A synthetic balance/share/claim/queue marker, duplicate inert effect, or reversible local transition is bound to the exact outer-call/callback/reentry/guard/state tuple.

### SCR5 — Regression-verified causal reentrancy proof

SCR4 plus complete outer/reentrant frame provenance, callback trigger, transient-state/guard-scope trace, first reentrant causal divergence, outer-continuation/commit binding, meaningful counterfactuals, eliminated alternatives, receipt/result binding, and remediation replay.

Evidence ceiling rules:

- surface only: SCR0 maximum;
- divergence without protected acceptance: SCR1 maximum;
- controlled mismatch without final acceptance: SCR2 maximum;
- inert wrong-state acceptance: SCR3 maximum;
- bounded reversible effect: SCR4 maximum;
- complete causal proof plus regression: SCR5.

## Remediation checks

Replay the exact local snapshot and verify:

1. state needed by the callback path is committed before exposure or otherwise safely isolated;
2. guard scope matches the full invariant domain;
3. cross-function and cross-contract paths are covered where required;
4. hook callbacks cannot consume stale/transient accounting;
5. read-only consumers revalidate current state before protected use;
6. outer continuation does not trust stale pre-callback assumptions;
7. positive controls remain functional;
8. negative controls remain denied or harmless;
9. callback depth remains bounded and deterministic;
10. receipts prove the fixed state/guard/callback generations.

Prefer the smallest ordering, invariant-scoped guard, revalidation, or callback-isolation fix that removes the causal divergence.
