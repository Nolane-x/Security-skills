---
name: smart-contract-upgradeability-analysis
description: "Analyze proxy/implementation/admin upgrade mechanisms, initializer state, storage layout, selector routing, ownership transfer, beacon/diamond-like composition, and upgrade invariants. Use local deployments to verify state/policy transitions."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Smart Contract Upgradeability Analysis

## When to use

Use for proxy-based or modular upgradeable contracts, implementation registries, beacons, diamonds/facets, governance upgrades, or migration initializers.

## Preconditions

1. Use source plus a local test deployment mirroring intended proxy/admin configuration.
2. Pin compiler/storage-layout artifacts, current and candidate implementation revisions, and governance/admin roles.
3. Use synthetic admin/user accounts only.

## Workflow

1. Map proxy type, implementation/admin storage slots or registry, delegatecall boundaries, fallback/selector routing, and upgrade authorization.
2. Compare storage layouts/types/packing across upgrades and identify inherited/gap assumptions.
3. Check initializer/reinitializer guards and whether implementation/proxy instances can be initialized in unintended contexts.
4. Model governance/timelock/multisig path to implementation change and emergency bypasses.
5. Test local upgrades/downgrades with synthetic state and assert critical invariants/roles/asset accounting persist.
6. Review selector/facet collisions and stale implementation interfaces for unintended reachable functions.

## Evidence contract

Record proxy/admin model, implementation revisions, storage-layout diff, authorization path, local pre/post state, and invariant controls. Upgradeability itself is not a vulnerability.

## Causal smart-contract-upgradeability model

Treat every promoted finding as one causal tuple:

`protocol/system identity + local chain/environment identity/generation + deployment/proxy identity/generation + proxy model + proxy/admin/governance identity/generation + current implementation identity/generation + candidate implementation identity/generation + implementation code revision + implementation registry/beacon/facet-set identity/generation + upgrade proposal/operation identity/generation + authorization path identity/generation + timelock/multisig/governance state generation + implementation/admin slot or registry identity + selector/fallback routing identity/generation + delegatecall/context identity + storage-layout identity/version + storage slot/type/packing identity + initializer/reinitializer identity/generation + initialized-version state + upgrade hook/migration identity/generation + pre-upgrade state snapshot + upgrade commit identity + post-upgrade state snapshot + rollback/downgrade identity/generation + invariant/result identity + downstream proxy consumer identity + effective upgradeability capability + bounded result + receipt/result`.

The proof must identify the exact upgrade transition and generation mismatch that changes behavior, authority, state interpretation, or reachable interface.

Preserve these distinctions explicitly:

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

All dynamic validation remains local/owned/test-chain or explicitly authorized. Use synthetic admin/user accounts, local proxies/implementations, fake governance/timelocks, inert selector markers, bounded storage values, read-only snapshots, and reversible upgrade/downgrade transitions.

## Proxy, implementation, governance, and lifecycle generations

Track independently:

- protocol/system identity;
- local chain/environment identity/generation;
- proxy generation and deployment/proxy identity/generation;
- proxy model;
- proxy/admin/governance identity/generation;
- implementation generation, including current implementation identity/generation and candidate implementation identity/generation;
- implementation code revision;
- implementation registry/beacon/facet-set identity/generation;
- governance generation, proposal/upgrade operation generation, and timelock/multisig/governance state generation;
- rollback/downgrade identity/generation;
- initializer/reinitializer version generation;
- migration generation.

A stable address, proxy name, selector, implementation registry key, or governance role label does not collapse these generations.

## Upgrade authorization and commit binding

For every candidate upgrade record:

1. initiating principal/admin/governance identity;
2. authorization path identity/generation;
3. authorization policy and current governance generation;
4. proposal/upgrade operation identity/generation;
5. multisig/timelock/governance state generation;
6. candidate implementation identity and implementation code revision;
7. pre-upgrade active implementation generation;
8. implementation/admin slot or registry identity;
9. exact registry/beacon/facet update;
10. upgrade hook/migration if any;
11. upgrade commit identity and activation point;
12. post-upgrade active implementation generation;
13. receipt/result.

Upgrade authorization != upgrade correctness. Governance proposal != committed implementation change. Upgrade event != committed implementation/state change.

## Storage-layout and state-interpretation binding

Capture this chain:

`proxy storage slot -> pre-upgrade variable/type/layout identity -> candidate variable/type/layout identity -> delegatecall code consumer -> post-upgrade interpreted state -> downstream proxy consumer`.

For each changed field record:

- storage-layout identity/version;
- storage slot/type/packing identity;
- slot and byte offset;
- type/width/packing;
- inheritance/layout lineage;
- mapping/array/struct root where relevant;
- reserved storage-gap assumptions;
- pre-upgrade semantic owner;
- candidate semantic owner;
- exact value before upgrade;
- interpreted value after upgrade;
- first downstream consumer.

Storage-layout diff != storage corruption without state-slot interpretation mismatch. Compiler layout metadata != runtime storage proof by itself. Promotion requires a concrete state interpretation mismatch or preserved-layout proof on synthetic local state.

## Initializer, reinitializer, and migration binding

Record:

- proxy initialization generation;
- implementation initialization state;
- initializer/reinitializer identity/generation;
- initialized-version state;
- caller authorization;
- one-time/version guard generation;
- upgrade hook/migration identity/generation;
- migration preconditions;
- state writes;
- upgrade commit point;
- post-migration state;
- replay/re-entry behavior;
- receipt/result.

Implementation instance uninitialized != proxy instance uninitialized. Proxy initialized != new implementation/reinitializer state valid by assumption. A reinitializer callable in one generation is not automatically unauthorized or replayable in another.

## Selector, fallback, beacon, and facet routing binding

Record:

- incoming selector or fallback condition;
- selector/fallback routing identity/generation;
- proxy routing rule generation;
- admin-call special routing where relevant;
- selector-to-facet/implementation mapping generation;
- implementation registry/beacon/facet-set identity/generation;
- beacon identity/generation;
- delegate target identity;
- delegatecall/context identity;
- storage context;
- final function consumer.

Selector collision != reachable unintended function without routing proof. Facet added != selector ownership conflict by itself. A routing mismatch becomes security-relevant only when the actual generation directs a reachable call to an unintended consumer under a prohibited context.

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

Record the invariant/result identity, downstream proxy consumer identity, effective upgradeability capability, bounded result, and receipt/result.

Use `smart-contract-invariant-analysis` for the generic invariant predicate and final protocol consequence. This profile owns the upgrade-specific causal path that makes the post-upgrade state or behavior differ.

## Smart-contract upgradeability evidence ladder

Use SCU0–SCU5 exactly:

- **SCU0 — Upgrade surface mapped.** Proxy model, implementations, admin/governance path, storage layout, initializer state, routing, beacon/facets, migration, rollback, and upgrade invariants are identified.
- **SCU1 — Upgrade-generation divergence observed.** A repeatable implementation, layout, initializer, selector, governance, migration, or rollback generation divergence exists without final wrong-context behavior or state interpretation.
- **SCU2 — Controlled upgrade invariant mismatch.** A deterministic local upgrade proves a documented layout, initializer, routing, governance, migration, or rollback invariant can be violated.
- **SCU3 — Inert wrong-context upgrade effect.** A read-only or inert synthetic proxy consumer observes a wrong field interpretation, wrong selector target, repeated initializer state, stale implementation behavior, or illegal migration state after the controlled upgrade.
- **SCU4 — Bounded reversible upgrade effect.** A synthetic role/balance/state/selector/migration marker or reversible local proxy-state transition is causally bound to the exact proxy/implementation/layout/initializer/routing/upgrade tuple.
- **SCU5 — Regression-verified causal upgradeability proof.** SCU4 plus complete proxy/implementation/governance/layout/initializer/routing/migration provenance, first harmful upgrade transition, meaningful counterfactuals, eliminated alternative explanations, receipt/result binding, and remediation replay.

Layout diffs, upgrade events, initializer availability, selector listings, local state deltas, or synthetic markers cannot skip missing causal bindings.

## Counterfactual upgradeability controls

Hold proxy state and operation intent constant while changing one causal variable:

- compatible versus incompatible storage layout;
- current versus stale initialized-version state;
- intended versus conflicting selector-table generation;
- rollback with versus without state rollback/migration compatibility;
- same candidate implementation under current versus stale governance generation;
- same candidate implementation with migration hook fixed versus unfixed.

Generic implementation swaps or arbitrary fuzzing are not causal counterfactuals unless they isolate the exact upgrade transition.

## Alternative explanations

Before SCU4 or SCU5 reject:

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

Keep generic protocol-invariant ownership with `smart-contract-invariant-analysis`, callback/reentrant ordering with `smart-contract-reentrancy-state-analysis`, authorization-root defects with authorization profiles, and generic naming/canonicalization with the namespace profile.

## Evidence ceiling

Apply the narrowest supported level:

- mapped upgrade surface only: SCU0 maximum;
- generation/layout/routing divergence without wrong-context effect: SCU1 maximum;
- deterministic upgrade invariant mismatch without final consumer: SCU2 maximum;
- inert/read-only wrong-context proxy effect: SCU3 maximum;
- bounded reversible upgrade effect: SCU4 maximum;
- only complete proxy/implementation/governance/layout/initializer/routing/migration provenance, counterfactuals, receipts, and remediation replay reaches SCU5.

Do not promote layout diffs, initializer availability, upgrade events, selector listings, local state changes, or synthetic markers into stronger claims without the missing causal bindings.

## Stop conditions

Stop before interacting with production governance/admin keys or proposing live upgrades without authorized deployment procedures.

## Output

```text
proxy model:
admin/governance path:
implementation revisions:
storage layout changes:
initializer state:
local upgrade controls:
invariant result:
evidence status:
```
