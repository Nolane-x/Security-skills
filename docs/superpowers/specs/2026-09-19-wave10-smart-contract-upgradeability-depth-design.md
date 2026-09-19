# Wave 10 Profile #40 — Smart Contract Upgradeability Causal Depth Design

**Date:** 2026-09-19  
**Base authority:** `main@004cd6299e8c76904f2634625af2213492488482`  
**Canonical skill:** `smart-contract-upgradeability-analysis`

## Purpose

Promote `smart-contract-upgradeability-analysis` into the fortieth and final planned Wave 10 operator-depth profile without changing routing, graph, packs, benchmark authority, agent-eval authority, superiority-court authority, or workflow semantics.

This profile owns upgrade-specific causality: proxy/implementation/admin generations, selector routing and delegate context, storage-layout compatibility, initializer/reinitializer state, governance/timelock/multisig authorization paths, beacon/diamond/facet composition, implementation rollback/downgrade state, and the exact upgrade transition that changes reachable behavior or corrupts protocol state. It does not absorb generic protocol invariant ownership from profile #38 or callback/reentrancy ordering from profile #39.

## Causal model

Every promoted finding must bind one reconstructable tuple:

`protocol/system identity + local chain/environment identity/generation + deployment/proxy identity/generation + proxy model + proxy/admin/governance identity/generation + current implementation identity/generation + candidate implementation identity/generation + implementation code revision + implementation registry/beacon/facet-set identity/generation + upgrade proposal/operation identity/generation + authorization path identity/generation + timelock/multisig/governance state generation + implementation/admin slot or registry identity + selector/fallback routing identity/generation + delegatecall/context identity + storage-layout identity/version + storage slot/type/packing identity + initializer/reinitializer identity/generation + initialized-version state + upgrade hook/migration identity/generation + pre-upgrade state snapshot + upgrade commit identity + post-upgrade state snapshot + rollback/downgrade identity/generation + invariant/result identity + downstream proxy consumer identity + effective upgradeability capability + bounded result + receipt/result`

The proof must identify the exact upgrade transition and generation mismatch that changes behavior, authority, state interpretation, or reachable interface. A proxy pattern, unusual storage diff, initializer function, selector collision, or powerful admin role is only attack surface until the candidate implementation transition and its bounded consequence are causally bound.

## Required distinctions

Preserve explicitly:

- upgradeability != vulnerability;
- upgrade authorization != upgrade correctness;
- admin role possession != unauthorized upgrade;
- governance proposal != committed implementation change;
- timelock queued != timelock executed;
- implementation deployed != proxy upgraded;
- proxy implementation slot value != active behavior without routing/delegate binding;
- implementation address equality != implementation code-generation equality;
- same proxy address != same implementation generation;
- delegatecall exists != storage corruption;
- storage-layout diff != storage corruption without state-slot interpretation mismatch;
- slot collision != harmful collision without consumer evidence;
- reserved storage gap change != corruption by itself;
- added variable != incompatible layout by itself;
- compiler layout metadata != runtime storage proof by itself;
- initializer exists != initialization flaw;
- implementation instance uninitialized != proxy instance uninitialized;
- proxy initialized != new implementation/reinitializer state valid by assumption;
- reinitializer callable != unauthorized or repeated state mutation without version/policy proof;
- disabled initializer != all initialization paths disabled;
- selector collision != reachable unintended function without routing proof;
- facet added != selector ownership conflict by itself;
- stale implementation ABI != reachable stale implementation;
- implementation self-call != proxy-context delegatecall by assumption;
- implementation function success != proxy-context success;
- upgrade hook success != state migration correctness;
- migration state change != invariant break;
- rollback possible != rollback unsafe;
- downgrade != vulnerability without version/invariant consequence;
- emergency bypass exists != unauthorized bypass;
- multisig threshold != effective signer authorization without signer/epoch binding;
- governance vote result != execution authority without execution-path binding;
- upgrade event != committed implementation/state change;
- storage write != active implementation switch without final consumer proof;
- local synthetic state corruption != real asset loss;
- local admin control != production governance compromise;
- invariant violation after upgrade != upgrade root cause until transition/layout/initializer causality is established;
- reentrancy after upgrade != upgradeability root cause unless the upgrade introduced the relevant call/order semantics.

All dynamic validation remains on local/owned/test-chain or explicitly authorized deployments using synthetic admin/user accounts, local proxies/implementations, bounded state, fake timelocks/governance, read-only storage snapshots, inert selector markers, and reversible upgrade/downgrade transitions.

## Proxy, implementation, governance, and lifecycle generations

Track independently:

- protocol/system identity;
- local chain/environment reset generation;
- proxy/deployment identity/generation;
- proxy model: transparent, UUPS-like, beacon, diamond/facet, registry-driven, or equivalent;
- current implementation identity/generation;
- candidate implementation identity/generation;
- implementation code revision/hash;
- admin/governance identity/generation;
- proposal/upgrade operation generation;
- timelock queue/execution generation;
- multisig signer-set/threshold generation;
- beacon/implementation registry generation;
- facet set/selector table generation;
- rollback/downgrade generation;
- initializer/reinitializer version generation;
- migration generation.

A stable address, proxy name, selector, implementation registry key, or governance role label does not collapse these generations.

## Upgrade authorization and commit binding

For every candidate upgrade record:

1. initiating principal/admin/governance identity;
2. authorization policy and generation;
3. proposal/upgrade operation identity;
4. multisig/timelock/governance state;
5. candidate implementation identity/code revision;
6. pre-upgrade active implementation generation;
7. exact slot/registry/beacon/facet update;
8. upgrade hook/migration call if any;
9. commit/activation point;
10. post-upgrade active implementation generation;
11. receipt/result.

Authorization path correctness and implementation correctness are separate. An authorized upgrade can still violate storage or initialization invariants, while an invalid authorization path is owned by the relevant authorization profile.

## Storage-layout and state-interpretation binding

Capture the state interpretation chain:

`proxy storage slot -> pre-upgrade variable/type/layout identity -> candidate variable/type/layout identity -> delegatecall code consumer -> post-upgrade interpreted state -> downstream protocol consumer`

For each changed field record:

- storage slot and offset;
- type/width/packing;
- inheritance/layout lineage;
- mapping/array/struct root where relevant;
- reserved gap assumptions;
- pre-upgrade semantic owner;
- candidate semantic owner;
- exact value before upgrade;
- interpreted value after upgrade;
- first downstream consumer.

A metadata diff is not enough. Promotion requires a concrete state interpretation mismatch or preserved-layout proof on a synthetic local state.

## Initializer, reinitializer, and migration binding

Record:

- proxy initialization generation;
- implementation initialization state;
- initializer/reinitializer function identity;
- initialized-version state;
- caller authorization;
- one-time/version guard generation;
- migration hook identity/generation;
- preconditions;
- state writes;
- commit point;
- post-migration state;
- replay/re-entry behavior;
- receipt/result.

Keep proxy instance and implementation instance initialization distinct. A callable reinitializer is not a defect if policy intentionally permits that exact version transition for the current principal and state.

## Selector, fallback, beacon, and facet routing binding

For transparent/UUPS/fallback/diamond/beacon systems record:

- incoming selector or fallback condition;
- proxy routing rule generation;
- admin-call special routing where relevant;
- selector-to-facet/implementation mapping generation;
- beacon identity/generation;
- delegate target identity;
- delegatecall context;
- storage context;
- final function consumer.

Selector collision becomes security-relevant only when the actual routing generation directs a reachable call to an unintended consumer under a prohibited context.

## Upgrade invariant and bounded consequence binding

Bind the upgrade transition to explicit post-upgrade invariants:

- critical roles preserved;
- ownership/admin semantics preserved;
- balances/accounting preserved;
- storage values remain semantically equivalent;
- initialization version is legal;
- expected entrypoints remain reachable;
- prohibited selectors remain unreachable;
- upgrade authorization remains intact;
- rollback/downgrade contract is respected;
- migration completes exactly once where required.

Use profile #38 for the general invariant predicate and final protocol consequence. This profile owns the upgrade-specific causal path that makes the post-upgrade state or behavior differ.

## Smart-contract upgradeability evidence ladder

Use SCU0–SCU5 exactly:

- **SCU0 — Upgrade surface mapped.** Proxy model, implementations, admin/governance path, storage layout, initializer state, routing, beacon/facets, migration, rollback, and upgrade invariants are identified.
- **SCU1 — Upgrade-generation divergence observed.** A repeatable implementation, layout, initializer, selector, governance, migration, or rollback generation divergence exists without final wrong-context behavior or state interpretation.
- **SCU2 — Controlled upgrade invariant mismatch.** A deterministic local upgrade proves a documented layout, initializer, routing, governance, migration, or rollback invariant can be violated.
- **SCU3 — Inert wrong-context upgrade effect.** A read-only or inert synthetic proxy consumer observes a wrong field interpretation, wrong selector target, repeated initializer state, stale implementation behavior, or illegal migration state after the controlled upgrade.
- **SCU4 — Bounded reversible upgrade effect.** A synthetic role/balance/state/selector/migration marker or reversible local proxy-state transition is causally bound to the exact proxy/implementation/layout/initializer/routing/upgrade tuple.
- **SCU5 — Regression-verified causal upgradeability proof.** SCU4 plus complete proxy/implementation/governance/layout/initializer/routing/migration provenance, first harmful upgrade transition, meaningful counterfactuals, eliminated alternatives, receipt/result binding, and remediation replay.

Layout diffs, upgrade events, initializer availability, selector listings, local state deltas, or synthetic markers cannot skip missing causal bindings.

## Deterministic benign review cases

Freeze at least:

1. `storage-layout-slot-reinterpreted-after-upgrade` — a local proxy holds a synthetic value whose slot/type semantics change in the candidate implementation, producing a deterministic read-only wrong interpretation.
2. `reinitializer-version-replayed-after-upgrade` — a local upgrade leaves initialized-version state inconsistent so a bounded synthetic reinitializer transition can be repeated or invoked under the wrong generation.
3. `selector-routing-generation-targets-unintended-facet` — a local diamond/facet or proxy selector table update routes an inert selector marker to the wrong synthetic target.
4. `rollback-restores-code-but-not-migrated-state-generation` — a local downgrade/rollback restores the prior implementation code while leaving migration state incompatible with the restored implementation generation.

No production admin keys, live governance proposals, real assets, live deployments, or public protocol interaction are required.

## Counterfactual requirements

Change exactly one causal variable while holding proxy state and operation intent constant, such as:

- compatible versus incompatible storage layout;
- current versus stale initialized-version state;
- intended versus conflicting selector-table generation;
- rollback with versus without state rollback/migration compatibility;
- authorized upgrade with identical candidate but different governance generation;
- same candidate implementation with migration hook fixed versus unfixed.

Generic implementation swaps or arbitrary fuzzing are insufficient for SCU5 without isolating the causal upgrade transition.

## Alternative explanations

Before SCU4/SCU5 eliminate:

- the apparent layout change is intentionally compatible;
- observed value difference comes from expected migration logic;
- the wrong field/value was read from the implementation instance rather than proxy storage;
- selector routing intentionally changed to the observed target;
- admin-special routing explains the call;
- initializer/reinitializer version is intentionally available;
- the transaction reverted and no upgrade committed;
- event/log differs from active implementation state;
- candidate implementation hash/revision differs from the assumed build;
- another governance/proposal generation executed;
- a generic invariant defect predates the upgrade;
- reentrancy/callback ordering independently causes the effect;
- external-data/oracle state independently causes the effect;
- receipt belongs to another proxy/deployment/upgrade generation.

Any unresolved material alternative caps evidence at SCU2.

## Ownership boundaries

- `smart-contract-upgradeability-analysis` owns proxy/implementation/admin generations, upgrade commit, storage-layout interpretation, initializer/reinitializer/migration state, selector/fallback/beacon/facet routing, rollback/downgrade, and upgrade-specific bounded consequences.
- `smart-contract-invariant-analysis` owns the generic protocol invariant statement and final accounting/state invariant.
- `smart-contract-reentrancy-state-analysis` owns callback/reentrant ordering and lock/update causality.
- authorization profiles own who is permitted to initiate/approve an upgrade when authorization itself is the root cause.
- `canonicalization-and-namespace-analysis` owns generic name/identifier resolution if registry naming semantics are the root issue.
- `bounds-and-integer-analysis` and `type-confusion-analysis` own machine numeric or runtime type interpretation defects unrelated to storage-layout upgrade generations.

## Expected repository scope

1. `README.md`
2. `docs/operator-depth-contract.md`
3. `docs/superpowers/plans/2026-09-19-wave10-smart-contract-upgradeability-depth.md`
4. `docs/superpowers/specs/2026-09-19-wave10-smart-contract-upgradeability-depth-design.md`
5. `operator-depth/profiles.json`
6. `skills/smart-contract-upgradeability-analysis/SKILL.md`
7. `skills/smart-contract-upgradeability-analysis/references/operator-review-cases.json`
8. `skills/smart-contract-upgradeability-analysis/references/operator-runbook.md`
9. `tests/test_smart_contract_upgradeability_depth.py`
10. `tests/test_smart_contract_reentrancy_depth.py` only if CI proves its exact global-count assertion is the sole extensibility defect.

Do not change `skill.meta.json`, graph edges, packs, routing domains, benchmark authority, agent-eval authority, superiority-court authority, or workflow semantics.

## Success criterion

Profile #40 is complete only when the merge tree contains exactly 40 profiles, exactly one valid `smart-contract-upgradeability-analysis` entry, SCU0–SCU5 is published, exact-head and post-merge CI are fully GREEN, merge parents are verified, and final scope remains bounded to the intended paths.

Wave 10 then enters closure mode only: overlap audit, 83-skill causal coverage mapping, graph/pack/routing validation, evidence-ladder consistency, deterministic matrices, cross-agent evaluation, superiority court, license completion, and professional README rewrite. No further profile expansion is planned unless the closure audit proves a genuinely distinct uncovered causal domain.
