# Wave 10 Profile #38 — Smart Contract Invariant Causal Depth Design

**Date:** 2026-09-18  
**Base authority:** `main@aa5d7dfff1d3bdc59b6d90633ede6bc0f747e568`  
**Canonical skill:** `smart-contract-invariant-analysis`

## Purpose

Promote `smart-contract-invariant-analysis` into the thirty-eighth CI-enforced operator-depth profile without changing routing, graph, packs, benchmark authority, agent-eval authority, superiority-court authority, or workflow semantics.

This is the root smart-contract reasoning profile. It owns explicit protocol invariants and the causal chain from a reachable local state transition to a violated invariant. It does not absorb callback/reentrancy causality owned by profile #39 or proxy/upgrade causality owned by profile #40.

## Causal model

Every promoted finding must bind one reconstructable tuple:

`protocol/system identity + local chain/environment identity/generation + deployment/configuration identity/generation + contract-set identity/generation + contract/code revision identity + invariant identity/version + invariant domain/scope + actor/account identity/generation + role/authorization state generation + asset/accounting domain identity + state snapshot/block/transaction generation + entrypoint/operation identity + call/transition sequence identity + pre-state identity + required precondition + external dependency/assumption identity/generation + state-write/commit identity + post-state identity + invariant predicate + expected invariant result + observed invariant result + first invalid transition/state delta + violation witness identity + downstream protocol/accounting consumer identity + effective invariant-break capability + bounded result + receipt/result`

A suspicious pattern, revert, arithmetic anomaly, event, state delta, or property-test failure is not by itself a validated protocol invariant break. Promotion requires the explicit invariant, the state domain it covers, a reachable transition sequence, deterministic pre/post state, and the first causal transition that makes the predicate false.

## Required distinctions

Preserve explicitly:

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

All dynamic validation remains on local/owned/test chains or explicitly authorized audit deployments with test accounts, synthetic tokens/assets, bounded balances, fake external dependencies, read-only state snapshots, and reversible local state.

## Protocol, deployment, contract, and state generations

Track independently:

- protocol/system identity;
- local chain/environment identity and reset generation;
- deployment/configuration generation;
- contract-set identity/generation;
- contract/code revision;
- storage/state snapshot generation;
- block/transaction generation;
- actor/account generation;
- role/authorization generation;
- asset/accounting epoch generation;
- external dependency generation;
- queue/claim/auction/vault phase generation where relevant.

A stable contract address, symbol, role label, storage slot, or asset name does not collapse state or deployment generations.

## Invariant identity and domain binding

Every invariant must have:

- invariant identity/version;
- plain-language statement;
- formal or executable predicate where feasible;
- state variables and contract set included;
- asset/accounting domain;
- actor/role scope;
- protocol phase/epoch where applicable;
- allowed transient exceptions;
- required preconditions;
- expected postconditions;
- observation point at which the invariant must hold.

Examples include conservation, solvency, ownership, authorization consistency, uniqueness, monotonicity, bounded debt, one-time action, legal state transition, queue/accounting coherence, and bounded-progress/liveness properties.

An invariant must be evaluated at the correct observation point. A protocol that intentionally enters transient intermediate state during one local transaction should not be labeled broken until the documented commit/terminal point is reached.

## Entrypoint, actor, and transition binding

For each candidate violation record:

1. actor/account identity and current role state;
2. entrypoint/operation identity;
3. transaction/call generation;
4. required pre-state and preconditions;
5. ordered call/transition sequence;
6. each state-write or logical transition;
7. first transition after which the invariant predicate becomes false;
8. commit/terminal point;
9. final post-state and receipt.

Entrypoint reachability is not enough. Bind the actor and exact state generation to the transition that violates the invariant.

## Asset, accounting, and conservation binding

For accounting invariants distinguish:

- external token/native-asset balance;
- internal ledger balance;
- share/unit supply;
- debt/credit position;
- reserve/backing value;
- pending/unsettled amount;
- fees/dust/rounding domain;
- escrow/queue balances;
- per-user versus global totals;
- current epoch/round.

Define the conservation or solvency equation explicitly and state permitted rounding/tolerance. A balance delta is meaningful only relative to the complete accounting domain and observation point.

Use synthetic tokens and bounded test values. Do not move real assets.

## External dependency and assumption binding

For tokens, hooks, oracles, bridges, queues, callbacks, and other contracts record:

- dependency identity/generation;
- assumed behavior;
- exact return/state semantics;
- trust or authenticity assumption;
- timing/ordering assumption;
- failure/revert semantics;
- protocol state that consumes the dependency result.

This root profile records the assumption required by the invariant. If the actual root cause is stale external data, callback/reentrancy ordering, randomness lifecycle, authorization, or upgrade state, route the causal subproblem to its owning profile while keeping the final invariant witness here.

## Reachability, witness, and bounded consequence binding

A promoted witness must include:

- deterministic initial state;
- bounded synthetic actor/assets;
- exact entry/transition sequence;
- state snapshot before;
- first invalid transition;
- state snapshot after;
- invariant predicate before/after;
- downstream protocol/accounting consumer;
- effective invariant-break capability;
- bounded result;
- receipt/result.

Prefer state snapshots, property assertions, synthetic accounting markers, fake claims, local queue entries, or reversible test balances. Do not infer economic loss, asset theft, governance takeover, or cross-chain consequence beyond the bounded local witness.

## Smart-contract invariant evidence ladder

Use SCI0–SCI5 exactly:

- **SCI0 — Invariant surface mapped.** Contract set, assets, roles, phases, external assumptions, entrypoints, state variables, and candidate invariants are identified.
- **SCI1 — State/invariant divergence observed.** A repeatable state, accounting, role, uniqueness, phase, or progress divergence exists but a reachable invariant violation is not yet bound.
- **SCI2 — Controlled invariant mismatch.** A deterministic local fixture proves a documented invariant or transition pre/postcondition can be violated under controlled state.
- **SCI3 — Reachable inert invariant violation.** A bounded local transaction/call sequence reaches a post-state where the explicit invariant predicate is false using synthetic accounts/assets and no real-value consequence.
- **SCI4 — Bounded reversible protocol effect.** A synthetic balance/share/claim/queue/phase marker or reversible local state transition is causally bound to the exact protocol/invariant/actor/transition tuple.
- **SCI5 — Regression-verified causal invariant proof.** SCI4 plus complete deployment/state/invariant/actor/asset provenance, first-invalid-transition trace, external-assumption binding, meaningful counterfactuals, eliminated alternatives, receipt/result binding, and remediation replay.

Static smells, property-test failures, fuzz cases, reverts, event logs, local balance changes, or synthetic markers cannot skip missing causal bindings.

## Deterministic benign review cases

Freeze at least:

1. `conservation-ledger-supply-divergence` — a synthetic vault/accounting fixture updates internal ledger and issued units inconsistently so a formal conservation equation fails at the commit point.
2. `claim-uniqueness-epoch-generation-reuse` — a local claim identifier/claimed-state generation is incorrectly reused across an epoch transition, violating one-time/uniqueness semantics.
3. `phase-transition-skips-required-accounting-state` — a toy auction/queue/vault phase advances without a required accounting/settlement predicate being true.
4. `solvency-accounting-domain-omits-pending-liability` — a synthetic solvency check omits a bounded pending liability generation, so the post-state passes a partial check while the complete invariant fails.

No real tokens, mainnet transactions, public protocols, oracle manipulation, or attack contracts are required.

## Counterfactual requirements

Change exactly one causal variable while holding deployment, actor, and intended operation constant, such as:

- correct versus omitted ledger update;
- current versus stale claim/epoch generation;
- phase transition with versus without required settlement state;
- solvency predicate including versus omitting the pending-liability domain;
- current versus stale external assumption generation;
- original versus remediated state transition.

Generic fuzzing or random transaction order is not sufficient for SCI5 without isolating the causal state transition.

## Alternative explanations

Before SCI4/SCI5 eliminate:

- the observed state is an explicitly permitted transient state;
- accounting equation omits documented fees, dust, rounding, escrow, or pending amounts;
- reset/epoch semantics intentionally permit counter or identifier reuse;
- role/authorization semantics explain the state without violating the stated invariant;
- transaction reverted and no violating post-state committed;
- event/log differs from committed storage;
- property harness observes the wrong contract/revision/deployment;
- external dependency mock violates its documented contract;
- reentrancy/callback ordering independently causes the violation;
- oracle/external-data trust independently causes the violation;
- upgrade/storage-layout behavior independently causes the violation;
- receipt belongs to another chain reset, deployment, transaction, or state generation.

Any unresolved material alternative caps evidence at SCI2.

## Ownership boundaries

- `smart-contract-invariant-analysis` owns explicit protocol invariant identity, domain, state-transition causality, accounting/conservation/solvency equations, reachable local witness, and bounded consequence.
- `smart-contract-reentrancy-state-analysis` owns callback/reentrant call-stack and lock/update-ordering causality.
- `smart-contract-upgradeability-analysis` owns proxy/implementation/admin, storage-layout, initializer, selector, and upgrade-transition causality.
- `oracle-and-external-data-trust-analysis` owns source/round/freshness/normalization/fallback trust.
- authorization profiles own role/policy authorization semantics when that is the root cause.
- arithmetic profiles own machine numeric representation errors; this profile owns the protocol accounting invariant they may violate.

## Expected repository scope

1. `README.md`
2. `docs/operator-depth-contract.md`
3. `docs/superpowers/plans/2026-09-18-wave10-smart-contract-invariant-depth.md`
4. `docs/superpowers/specs/2026-09-18-wave10-smart-contract-invariant-depth-design.md`
5. `operator-depth/profiles.json`
6. `skills/smart-contract-invariant-analysis/SKILL.md`
7. `skills/smart-contract-invariant-analysis/references/operator-review-cases.json`
8. `skills/smart-contract-invariant-analysis/references/operator-runbook.md`
9. `tests/test_smart_contract_invariant_depth.py`
10. `tests/test_template_expression_boundary_depth.py` only if CI proves its exact global-count assertion is the sole extensibility defect.

Do not change `skill.meta.json`, graph edges, packs, routing domains, benchmark authority, agent-eval authority, superiority-court authority, or workflow semantics.

## Success criterion

Profile #38 is complete only when the merge tree contains exactly 38 profiles, exactly one valid `smart-contract-invariant-analysis` entry, SCI0–SCI5 is published, exact-head and post-merge CI are fully GREEN, merge parents are verified, and final scope remains bounded to the intended paths.
