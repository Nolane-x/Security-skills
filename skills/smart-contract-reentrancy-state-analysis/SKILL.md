---
name: smart-contract-reentrancy-state-analysis
description: "Analyze contract external calls and callbacks for state-ordering, lock scope, cross-function/cross-contract reentrancy, hook-enabled tokens, read-only callbacks, and invariant exposure. Use invariant-driven local tests rather than exploit scripts."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Smart Contract Reentrancy State Analysis

Perform any dynamic validation only in an authorized, owned lab or equivalent explicitly scoped test environment.

## When to use

Use when contracts call untrusted contracts/tokens/hooks before completing state updates, share accounting across functions, or assume callback-free transfers.

## Preconditions

1. Use a local test chain with synthetic callback contracts/tokens.
2. Identify the invariant and state transition expected around each external call.
3. Do not deploy attack contracts against live protocols.

## Workflow

1. List every external call/callback point and state that remains transiently inconsistent at that point.
2. Map which public/external functions are callable during the callback and whether locks cover the entire invariant, not only one function.
3. Consider token hooks, fallback/receive, multicall, cross-contract callbacks, view/read-only dependencies, and proxy/delegate context separately.
4. Construct benign callback test contracts that re-enter only enough to assert invariant/state behavior.
5. Test cross-function and cross-contract paths with positive/negative controls and bounded recursion.
6. Distinguish reentrancy reachability from exploitable accounting/authorization impact.

## Evidence contract

Record external call, pre-callback state, reentrant entry, invariant expected/observed, bounded synthetic sequence, and resulting accounting/authorization difference.

## Causal smart-contract-reentrancy model

Treat every promoted finding as one causal tuple:

`protocol/system identity + local chain/environment identity/generation + deployment/configuration identity/generation + contract-set identity/generation + contract/code revision identity + invariant identity/version + outer actor/account identity + outer transaction/call generation + outer entrypoint identity + call-frame/stack generation + pre-call state generation + external-call site identity + external callee/callback target identity/generation + callback authority/capability + callback trigger identity + reentrant entrypoint identity + reentry generation/depth + lock/guard identity/generation + lock scope/domain + transient state identity/generation + expected update/commit ordering + observed callback/interleaving ordering + cross-function/cross-contract path identity + read-only observer identity where relevant + outer-call continuation identity + final commit/terminal point + post-state identity + expected invariant result + observed invariant result + first reentrant causal divergence + downstream protocol/accounting consumer identity + effective reentrancy-state capability + bounded result + receipt/result`.

A callback or external call is only attack surface until the exact reentrant frame, transient state generation, guard scope, and downstream protected consumer are bound.

Preserve these distinctions explicitly:

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

All dynamic validation remains local/owned/test-chain or explicitly authorized. Use synthetic callback contracts/tokens, normally depth-1 bounded recursion, fake assets, deterministic snapshots, inert markers, read-only observers, shadow ledgers, and reversible local state.

## Outer transaction, call-frame, and callback generations

Track independently:

- protocol/system identity and deployment/configuration generation;
- contract-set and code revision;
- invariant identity/version inherited from the root invariant analysis;
- outer actor/account identity;
- outer transaction/call generation;
- outer entrypoint identity;
- call-frame/stack generation;
- pre-call state generation;
- external-call site identity;
- callee/callback target identity/generation;
- callback trigger identity;
- reentry generation/depth;
- reentrant entrypoint;
- lock/guard identity/generation;
- transient state generation;
- outer-call continuation identity;
- final commit/terminal generation.

Same transaction != same logical state generation, and same function name != same call frame.

## External-call, callback, and reentrant-entry binding

For every candidate path bind:

1. outer entrypoint and preconditions;
2. exact external-call site identity;
3. state writes completed before the call;
4. state writes deferred until after return;
5. external callee/callback target;
6. callback authority/capability;
7. callback trigger mechanism;
8. reentrant entrypoint identity and parameters;
9. reentry generation/depth;
10. state/authorization observed by the reentrant frame;
11. outer continuation after callback return.

A callback that cannot reach a relevant reentrant entrypoint cannot establish reentrancy-state causality.

## Transient-state and update-ordering binding

Bind:

- invariant identity/version;
- transient state identity/generation;
- intended update/commit ordering;
- actual writes before external call;
- writes deferred until callback return;
- predicate visible during callback;
- first reentrant operation consuming that state;
- observed callback/interleaving ordering;
- outer continuation and final commit.

The key causal question is whether a reentrant frame can act on a state generation that the protocol assumes is not externally observable or actionable.

## Lock, guard, and invariant-scope binding

Record:

- lock/guard identity/generation;
- entered/not-entered state;
- protected functions/contracts;
- lock scope/domain;
- invariant domain intended to be protected;
- whether cross-function paths are covered;
- whether cross-contract shared-state paths are covered;
- whether read-only observers are covered where relevant;
- reset/release point;
- outer and reentrant frame observations.

Lock present != protected invariant. A per-function guard may leave a cross-function invariant exposed.

## Cross-function, cross-contract, hook, and read-only lineage

Treat separately:

- same-function reentry;
- cross-function reentry;
- cross-contract shared-state reentry;
- token/asset hook callback;
- fallback/receive callback;
- multicall or dispatcher nesting;
- proxy/delegate context;
- read-only callback/observer;
- external dependency callback that re-enters through another contract.

For read-only reentrancy, a transient read remains low-level evidence until a downstream local consumer uses that read for a protected decision or state transition.

## Outer continuation, commit, and duplicate-effect binding

After callback return record:

- outer-call continuation identity;
- assumptions reused from pre-callback state;
- checks repeated or omitted;
- remaining state writes;
- accounting/claim/share/debt updates;
- idempotency or duplicate-effect controls;
- final commit/terminal point;
- post-state identity;
- expected invariant result;
- observed invariant result;
- downstream protocol/accounting consumer;
- bounded result and receipt/result.

A reachable callback may be harmless when the outer frame revalidates current state and commits a correct final state.

## Smart-contract reentrancy evidence ladder

Use SCR0–SCR5 exactly:

- **SCR0 — Reentrancy surface mapped.** External calls, callback mechanisms, reentrant entrypoints, transient state, guards, shared invariants, and outer continuations are mapped.
- **SCR1 — Callback/order divergence observed.** A repeatable callback, reentry, transient-state, lock-scope, or outer-continuation divergence exists without a protected downstream acceptance.
- **SCR2 — Controlled reentrancy-policy mismatch.** A deterministic local fixture proves that a documented update-ordering, guard-scope, or callback-state invariant can be violated by one bounded reentrant path.
- **SCR3 — Inert reentrant wrong-state acceptance.** A synthetic reentrant frame or read-only observer is accepted against transient/wrong-generation state by the protected local consumer.
- **SCR4 — Bounded reversible reentrant effect.** A synthetic balance/share/claim/queue marker, duplicate inert effect, or reversible local transition is causally bound to the exact outer-call/callback/reentry/guard/state tuple.
- **SCR5 — Regression-verified causal reentrancy proof.** SCR4 plus complete outer/reentrant frame provenance, callback trigger, transient-state and guard-scope trace, first reentrant causal divergence, outer-continuation/commit binding, meaningful counterfactuals, eliminated alternative explanations, receipt/result binding, and remediation replay.

External-call presence, callback logs, guard absence, hook support, local reverts, state deltas, or synthetic markers cannot skip missing causal bindings.

## Counterfactual reentrancy controls

Hold deployment, actors, callback target, invariant, and bounded fixture constant while changing one causal variable:

- commit relevant state before versus after external call;
- guard scoped to one function versus the shared invariant domain;
- callback enabled versus same callee with callback disabled;
- reentrant entrypoint allowed versus denied;
- read-only transient value consumed versus ignored or revalidated;
- outer continuation revalidates current state versus trusts pre-callback assumptions.

Changing generic recursion depth or unrelated transaction order is not sufficient for SCR5.

## Alternative explanations

Before SCR4 or SCR5 reject:

- callback cannot reach the claimed reentrant entrypoint;
- transient state is explicitly permitted and safe to expose;
- invariant permits the intermediate observation;
- outer continuation revalidates and prevents wrong commit;
- duplicate-looking effect belongs to another transaction/generation;
- guard scope intentionally excludes a state domain not shared by the callback path;
- callback mock violates documented token/callee semantics;
- the underlying invariant was specified incorrectly;
- generic concurrency, not smart-contract callback-stack semantics, explains the behavior;
- external-data/oracle state independently explains the result;
- upgrade/proxy/storage-layout behavior independently explains the path;
- authorization independently grants the reentrant operation;
- receipt belongs to another deployment, chain reset, transaction, or callback generation.

Any unresolved material alternative caps evidence at SCR2.

Keep invariant definition/accounting-domain proof in `smart-contract-invariant-analysis`, generic scheduler interleavings in `concurrency-race-analysis`, and upgrade/proxy causality in `smart-contract-upgradeability-analysis`.

## Evidence ceiling

Apply the narrowest supported level:

- mapped external-call/callback surface only: SCR0 maximum;
- callback/reentry/order divergence without protected acceptance: SCR1 maximum;
- controlled update-order/guard-scope mismatch without final acceptance: SCR2 maximum;
- inert wrong-state acceptance by a bounded local consumer: SCR3 maximum;
- bounded reversible reentrant state effect: SCR4 maximum;
- only complete outer/reentrant/guard/transient-state/continuation provenance plus counterfactuals, receipts, and remediation replay reaches SCR5.

Do not promote callback logs, guard absence, hook support, local reverts, state deltas, or synthetic markers into stronger claims without the missing causal bindings.

## Stop conditions

Stop before live-chain interaction, gas/resource griefing beyond local bounds, or moving real assets.

## Output

```text
call site:
transient state:
reentrant entries:
lock/update ordering:
synthetic callback sequence:
invariant result:
evidence status:
```
