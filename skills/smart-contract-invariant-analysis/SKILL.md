---
name: smart-contract-invariant-analysis
description: "Model smart-contract/state-machine invariants for balances, ownership, conservation, authorization, accounting, liveness, upgrade state, and external-call assumptions. Use as the root skill before contract fuzzing or bug-specific analysis."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Smart Contract Invariant Analysis

Perform any dynamic validation only in an authorized, owned lab or equivalent explicitly scoped test environment.

## When to use

Use for EVM-like or other smart-contract systems, especially protocols with multiple contracts, asset accounting, roles, queues, auctions, vaults, bridges, or upgradeable state.

## Preconditions

1. Use source and a local fork/test chain or explicit audit scope.
2. Pin compiler, bytecode/source revision, deployment configuration, and external dependency assumptions.
3. Use test tokens/accounts; do not transact with real funds.

## Workflow

1. Enumerate assets, privileged roles, trust boundaries, external dependencies, upgrade/admin paths, and state-machine phases.
2. Write explicit invariants: conservation, ownership, solvency, monotonic counters, one-time actions, access control, bounded debt, claim uniqueness, state transition legality.
3. Map every public/external entrypoint to invariants it can affect and required pre/postconditions.
4. Identify external calls/oracles/tokens/hooks that can violate ordering or assumptions.
5. Turn invariants into property tests or symbolic/fuzz assertions on a local chain where feasible.
6. Treat invariant violation as observed evidence; root-cause and economic consequence require separate validation.

## Evidence contract

Record contract/config revision, invariant statement, reachable entry sequence, pre/post state, synthetic asset/account context, and reproducible violation. A suspicious pattern without invariant break remains a hypothesis.

## Causal smart-contract-invariant model

Treat every promoted finding as one causal tuple:

`protocol/system identity + local chain/environment identity/generation + deployment/configuration identity/generation + contract-set identity/generation + contract/code revision identity + invariant identity/version + invariant domain/scope + actor/account identity/generation + role/authorization state generation + asset/accounting domain identity + state snapshot/block/transaction generation + entrypoint/operation identity + call/transition sequence identity + pre-state identity + required precondition + external dependency/assumption identity/generation + state-write/commit identity + post-state identity + invariant predicate + expected invariant result + observed invariant result + first invalid transition/state delta + violation witness identity + downstream protocol/accounting consumer identity + effective invariant-break capability + bounded result + receipt/result`.

The proof must identify the invariant, its domain and observation point, the reachable local transition sequence, and the first committed state transition after which the predicate becomes false.

Preserve these distinctions explicitly:

- suspicious pattern != invariant violation;
- invariant violation != exploitable economic loss;
- local property failure != production reachability;
- reachable entrypoint != reachable violating state;
- state change != invalid state transition;
- balance difference != conservation failure without accounting-domain binding;
- asset balance != protocol accounting balance by assumption;
- token transfer success != protocol solvency;
- share-price movement != accounting violation by itself;
- temporary imbalance != terminal invariant break when the protocol explicitly permits transient state;
- precondition failure != postcondition violation;
- revert != invariant preservation proof;
- event emission != state commitment;
- storage write != committed protocol state by itself;
- duplicate-looking identifier != uniqueness violation without generation/domain binding;
- counter decrease != monotonicity violation when reset/epoch semantics permit it;
- role possession != authorization invariant violation;
- stale role state != current authority without generation binding;
- external call exists != reentrancy root cause;
- callback reachability != invariant violation;
- oracle value change != external-data trust defect by itself;
- synthetic price movement != market-manipulation proof;
- upgradeability != invariant failure;
- storage-layout change != invariant failure without upgrade transition proof;
- gas difference != liveness failure;
- bounded local progress delay != permanent liveness failure;
- fuzz counterexample != root cause until minimized and replayed;
- symbolic path != runtime reachability by assumption;
- mainnet-like fork state != authorization to transact on live systems;
- local synthetic accounting consequence != real financial loss.

All dynamic validation remains local/owned/test-chain or explicitly authorized. Use synthetic accounts/tokens/assets, bounded balances, fake dependencies, deterministic state snapshots, property assertions, shadow ledgers, and reversible local state.

## Protocol, deployment, contract, and state generations

Track independently:

- protocol/system identity;
- local chain/environment identity/generation;
- protocol generation when a reset, epoch, or deployment changes the state universe;
- deployment/configuration identity/generation and deployment generation;
- contract-set identity/generation;
- contract/code revision identity;
- state generation and state snapshot/block/transaction generation;
- actor/account generation;
- role/authorization state generation;
- asset/accounting epoch generation;
- external dependency generation;
- queue/claim/auction/vault phase generation where relevant.

A stable contract address, symbol, role label, storage slot, or asset name does not collapse state, protocol, or deployment generations.

## Invariant identity and domain binding

Every invariant must record:

- invariant identity/version;
- plain-language statement;
- formal/executable invariant predicate where feasible;
- invariant domain/scope;
- contract set and state variables included;
- asset/accounting domain;
- actor/role scope;
- phase/epoch scope;
- allowed transient exceptions;
- required preconditions;
- expected postconditions;
- observation point at which the invariant must hold.

Conservation, solvency, ownership, authorization consistency, uniqueness, monotonicity, bounded debt, one-time action, legal state transition, queue/accounting coherence, and bounded-progress/liveness properties must each name their exact domain.

An invariant evaluated at the wrong observation point is not a valid violation witness.

## Entrypoint, actor, and transition binding

For each candidate violation bind:

1. actor/account identity/generation and current role state;
2. entrypoint/operation identity;
3. transaction/call generation;
4. pre-state identity and required precondition;
5. call/transition sequence identity;
6. ordered state writes/transitions;
7. first invalid transition/state delta;
8. state-write/commit identity;
9. commit/terminal point;
10. post-state identity and receipt/result.

Entrypoint reachability alone does not prove the actor can reach the violating state.

## Asset, accounting, and conservation binding

For accounting invariants distinguish:

- external token/native-asset balance;
- internal ledger balance;
- share/unit supply;
- debt/credit position;
- reserve/backing value;
- pending/unsettled liability;
- fees, dust, and rounding domain;
- escrow/queue balances;
- per-user versus global totals;
- current epoch/round.

Write the conservation or solvency equation explicitly, including permitted tolerance. Balance difference != conservation failure without accounting-domain binding.

Use synthetic assets and bounded values only.

## External dependency and assumption binding

For tokens, hooks, oracles, bridges, queues, callbacks, and other contracts record:

- external dependency identity/generation;
- documented assumption;
- exact return/state semantics;
- trust/authenticity assumption;
- timing/ordering assumption;
- failure/revert semantics;
- protocol state and consumer that use the result.

The invariant profile records the dependency assumption. If the root cause is callback/reentrancy ordering, stale external data, randomness, authorization, or upgrade state, route that causal mechanism to its owning profile while retaining the final invariant witness here.

External call exists != reentrancy root cause. Oracle value change != external-data trust defect by itself.

## Reachability, witness, and bounded consequence binding

A promoted violation witness must include:

- deterministic initial state;
- bounded synthetic actor/assets;
- exact entry/transition sequence;
- state snapshot before;
- first invalid transition;
- state snapshot after;
- invariant predicate before/after;
- expected invariant result;
- observed invariant result;
- violation witness identity;
- downstream protocol/accounting consumer identity;
- effective invariant-break capability;
- bounded result;
- receipt/result.

Prefer read-only state snapshots, property assertions, synthetic accounting markers, fake claims, local queue entries, or reversible test balances. Do not infer asset theft, governance takeover, cross-chain consequence, or real financial loss beyond the bounded local witness.

## Smart-contract invariant evidence ladder

Use SCI0–SCI5 exactly:

- **SCI0 — Invariant surface mapped.** Contract set, assets, roles, phases, external assumptions, entrypoints, state variables, and candidate invariants are identified.
- **SCI1 — State/invariant divergence observed.** A repeatable state, accounting, role, uniqueness, phase, or progress divergence exists but a reachable invariant violation is not yet bound.
- **SCI2 — Controlled invariant mismatch.** A deterministic local fixture proves a documented invariant or transition pre/postcondition can be violated under controlled state.
- **SCI3 — Reachable inert invariant violation.** A bounded local transaction/call sequence reaches a post-state where the explicit invariant predicate is false using synthetic accounts/assets and no real-value consequence.
- **SCI4 — Bounded reversible protocol effect.** A synthetic balance/share/claim/queue/phase marker or reversible local state transition is causally bound to the exact protocol/invariant/actor/transition tuple.
- **SCI5 — Regression-verified causal invariant proof.** SCI4 plus complete deployment/state/invariant/actor/asset provenance, first-invalid-transition trace, external-assumption binding, meaningful counterfactuals, eliminated alternative explanations, receipt/result binding, and remediation replay.

Static smells, property-test failures, fuzz cases, reverts, event logs, local balance changes, or synthetic markers cannot skip missing causal bindings.

## Counterfactual invariant controls

Hold deployment, actor, intended operation, and invariant definition constant while changing one causal variable:

- correct versus omitted ledger update;
- current versus stale claim/epoch generation;
- phase transition with versus without required settlement state;
- solvency predicate including versus omitting pending liabilities;
- current versus stale external dependency generation;
- original versus remediated state transition.

Random fuzzing or transaction reordering is not a causal counterfactual unless it isolates the state transition under test.

## Alternative explanations

Before SCI4 or SCI5 reject:

- the observed state is explicitly permitted transient state;
- accounting equation omitted documented fees, dust, rounding, escrow, or pending amounts;
- reset/epoch semantics permit identifier or counter reuse;
- role/authorization semantics explain the state without violating the stated invariant;
- the transaction reverted and no violating state committed;
- an event/log differs from committed state;
- property harness observes the wrong revision/deployment;
- external dependency mock violates its documented contract;
- callback/reentrancy ordering independently causes the violation;
- external-data/oracle trust independently causes the violation;
- upgrade/storage-layout behavior independently causes the violation;
- receipt belongs to another chain reset, deployment, transaction, or state generation.

Any unresolved material alternative caps evidence at SCI2.

Keep callback/reentrant call-stack causality with `smart-contract-reentrancy-state-analysis`, proxy/upgrade causality with `smart-contract-upgradeability-analysis`, external-data trust with `oracle-and-external-data-trust-analysis`, authorization semantics with the authorization profiles, and machine numeric representation errors with the bounds/integer profile.

## Evidence ceiling

Apply the narrowest supported level:

- invariant/state surface only: SCI0 maximum;
- state or accounting divergence without a reachable false predicate: SCI1 maximum;
- deterministic invariant mismatch without final reachable post-state witness: SCI2 maximum;
- reachable inert false predicate with synthetic state: SCI3 maximum;
- bounded reversible protocol/accounting effect: SCI4 maximum;
- only complete deployment/state/invariant/transition/dependency provenance, counterfactuals, receipts, and remediation replay reaches SCI5.

Do not promote static smells, fuzz failures, reverts, events, local balance deltas, or synthetic markers into stronger claims without the missing causal bindings.

## Stop conditions

Stop if testing requires mainnet transactions, manipulating real oracle markets, or interacting with third-party deployed contracts outside scope.

## Output

```text
protocol/contracts:
roles/assets:
invariants:
entrypoints/state phases:
external assumptions:
property/reproducer:
pre/post state:
evidence status:
```
