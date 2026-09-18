# Smart Contract Invariant Operator Runbook

Use this runbook only on local/owned test chains, isolated forks with no live transaction capability, benchmark/CTF fixtures, simulated environments, or explicitly authorized audit deployments. Use synthetic accounts, test tokens, bounded balances, fake dependencies, deterministic snapshots, read-only state inspection, and reversible local state. Do not transact with real funds or manipulate public protocols, live oracle markets, governance, bridges, or third-party deployed contracts outside scope.

## Attack surface

Map:

- protocol/system and protocol generation;
- local chain/environment and reset generation;
- deployment generation and configuration;
- contract set and code revisions;
- roles, actors, assets, accounting domains, phases, queues, claims, and epochs;
- public/external entrypoints and state transitions;
- external dependencies and assumptions;
- invariant identities, predicates, domains, and observation points;
- final protocol/accounting consumers.

## Hypothesis matrix

| Hypothesis | Safe oracle | Control |
| --- | --- | --- |
| internal ledger and issued units diverge | synthetic test-chain accounting predicate over bounded test balances | correct ledger/supply update preserves conservation |
| claim uniqueness leaks across epoch generation | fake claim IDs and read-only claimed-state receipt | epoch-scoped claim generation prevents duplicate acceptance |
| phase advances before required settlement state | toy phase machine and shadow accounting predicate | required settlement transition occurs before phase commit |
| solvency check omits pending liability | synthetic pending-liability ledger and read-only solvency predicate | complete accounting domain includes pending liability |

## Protocol/deployment/state-generation trace

Record:

- protocol/system identity and protocol generation;
- local chain/environment identity/reset generation;
- deployment/configuration identity and deployment generation;
- contract-set identity/generation;
- contract/code revision;
- state generation and exact state snapshot/block/transaction generation;
- actor/account generation;
- role/authorization generation;
- asset/accounting epoch generation;
- external-dependency generation;
- phase/queue/claim generation where relevant.

A stable address or symbol is not a stable deployment or state generation.

## Invariant/domain/observation-point trace

For every invariant record:

- invariant identity/version;
- plain-language statement;
- executable predicate where feasible;
- state and contracts in scope;
- asset/accounting domain;
- actor/role scope;
- phase/epoch scope;
- allowed transient states;
- preconditions and postconditions;
- exact observation point.

Evaluate conservation, solvency, uniqueness, monotonicity, ownership, authorization consistency, one-time actions, and legal phase transitions only at their documented observation points.

## Entrypoint/actor/transition trace

Capture:

1. actor/account and role generation;
2. entrypoint/operation;
3. transaction/call identity;
4. pre-state and required precondition;
5. ordered transition sequence;
6. each logical state write;
7. first transition after which the invariant becomes false;
8. commit/terminal point;
9. post-state;
10. deterministic receipt.

Reachability of the entrypoint is not enough; prove reachability of the violating post-state.

## Asset/accounting/conservation trace

For accounting invariants distinguish:

- external test-token/native balance;
- internal ledger;
- share/unit supply;
- debt/credit;
- reserve/backing;
- pending liability;
- fees/dust/rounding;
- escrow/queue amounts;
- per-user/global totals;
- epoch/round.

Write the conservation or solvency equation, its units, and permitted tolerance. Use bounded synthetic values only.

## External-dependency/assumption trace

Capture:

- external dependency identity/generation;
- documented assumption;
- return/state semantics;
- trust/authenticity state;
- ordering/timing assumption;
- revert/failure behavior;
- protocol state consuming the result.

If reentrancy, oracle trust, randomness, authorization, or upgrade mechanics are the true root cause, route that mechanism to the owning profile and keep only the invariant consequence here.

## Reachability/witness/bounded-consequence trace

Capture:

- deterministic initial state;
- synthetic actor/assets;
- exact entry sequence;
- pre-state snapshot;
- first invalid transition;
- post-state snapshot;
- invariant predicate before/after;
- violation witness identity;
- downstream protocol/accounting consumer;
- effective invariant-break capability;
- bounded result;
- receipt/result.

Prefer read-only snapshots, assertion failures, shadow ledgers, fake claims, synthetic queue entries, and reversible test balances.

## Controlled validation

Use:

- local test chains reset from deterministic genesis/snapshot;
- synthetic accounts and roles;
- test tokens or in-memory asset models;
- bounded deposits/debts/shares/claims;
- fake oracle/token/bridge/dependency contracts with fixed behavior;
- property assertions and shadow accounting models;
- deterministic state snapshots before and after each transition;
- bounded transaction/call sequences.

Recommended sequence:

1. freeze deployment/configuration and initial state;
2. state the invariant formally;
3. establish a passing positive control;
4. establish a negative control that does not reach the target state;
5. alter one causal transition variable;
6. locate the first state delta that falsifies the predicate;
7. bind the false predicate to the final protocol/accounting consumer;
8. apply the minimal state-transition/accounting fix;
9. replay from the identical snapshot;
10. capture before/after receipts.

## False-positive controls

Eliminate:

- documented transient intermediate state;
- omitted fee/dust/rounding/escrow/pending domains;
- intentional epoch resets or claim reuse semantics;
- transaction revert with no committed bad state;
- event/log disagreement with storage;
- wrong deployment or code revision in the harness;
- fake dependency violating its contract;
- reentrancy as independent root cause;
- oracle/external-data trust as independent root cause;
- upgrade/storage-layout change as independent root cause;
- receipt from a different chain reset or transaction generation.

## Counterfactual invariant controls

Hold deployment, actor, intended operation, and invariant definition constant while changing one variable:

- omitted versus correct ledger update;
- stale versus current claim/epoch generation;
- phase transition before versus after required settlement;
- partial versus complete solvency accounting domain;
- stale versus current external dependency generation;
- original versus remediated state transition.

Generic fuzzing is discovery, not a causal counterfactual.

## Alternative explanations

Before SCI4/SCI5 explicitly reject:

- transient state is permitted until a later commit point;
- accounting equation omitted a documented domain;
- reset/epoch semantics explain reuse;
- role/authorization semantics explain the state;
- transaction did not commit;
- logs differ from storage;
- harness uses wrong deployment/revision;
- fake dependency violates its contract;
- callback/reentrancy causality explains the break;
- oracle/external-data causality explains the break;
- upgrade/storage-layout causality explains the break;
- receipt belongs to another generation.

Any unresolved material alternative caps evidence at SCI2.

## Evidence capture

Capture one tuple:

`protocol/system identity + local chain/environment identity/generation + deployment/configuration identity/generation + contract-set identity/generation + contract/code revision identity + invariant identity/version + invariant domain/scope + actor/account identity/generation + role/authorization state generation + asset/accounting domain identity + state snapshot/block/transaction generation + entrypoint/operation identity + call/transition sequence identity + pre-state identity + required precondition + external dependency/assumption identity/generation + state-write/commit identity + post-state identity + invariant predicate + expected invariant result + observed invariant result + first invalid transition/state delta + violation witness identity + downstream protocol/accounting consumer identity + effective invariant-break capability + bounded result + receipt/result`

Useful artifacts include deployment manifests, state snapshots, invariant predicates, bounded transaction traces, shadow-ledger equations, property receipts, state diffs, and remediation replay results.

## Evidence promotion and ceiling

### SCI0 — Invariant surface mapped

Contracts, assets, roles, phases, dependencies, entrypoints, state variables, and candidate invariants are known.

### SCI1 — State/invariant divergence observed

A repeatable state, accounting, role, uniqueness, phase, or progress divergence exists without a reachable invariant violation.

### SCI2 — Controlled invariant mismatch

A deterministic local fixture proves an invariant or transition pre/postcondition can be violated under controlled state.

### SCI3 — Reachable inert invariant violation

A bounded local call sequence reaches a post-state where the explicit invariant predicate is false using synthetic accounts/assets.

### SCI4 — Bounded reversible protocol effect

A synthetic balance/share/claim/queue/phase marker or reversible local state transition is bound to the exact protocol/invariant/actor/transition tuple.

### SCI5 — Regression-verified causal invariant proof

SCI4 plus complete deployment/state/invariant/actor/asset provenance, first-invalid-transition trace, external-assumption binding, meaningful counterfactuals, eliminated alternatives, receipt/result binding, and remediation replay.

Evidence ceiling rules:

- mapped surface only: SCI0 maximum;
- divergence without reachable false predicate: SCI1 maximum;
- controlled mismatch without final witness: SCI2 maximum;
- reachable inert false predicate: SCI3 maximum;
- bounded reversible protocol effect: SCI4 maximum;
- complete causal proof plus regression: SCI5.

## Remediation checks

Replay the exact local snapshot and verify:

1. the invariant predicate is evaluated at the correct observation point;
2. the causal transition now preserves the predicate;
3. accounting equations include all required domains;
4. epoch/claim generations remain isolated;
5. phase changes require documented settlement/preconditions;
6. external assumptions are explicitly checked or bounded;
7. positive controls still succeed;
8. negative controls still fail safely;
9. property/fuzz replay no longer produces the minimized witness;
10. deterministic receipts bind the fixed state generation.

Prefer the smallest accounting, state-transition, precondition, generation-binding, or dependency-check fix that restores the invariant.
