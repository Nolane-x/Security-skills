# Smart Contract Upgradeability Operator Runbook

Use this runbook only on a local/owned test chain, isolated authorized deployment, benchmark/CTF fixture, or equivalent explicitly scoped environment. Use synthetic admin/user accounts, local proxy/implementation pairs, fake governance/timelocks, inert selector markers, bounded storage values, read-only state snapshots, and reversible upgrade/downgrade transitions. Do not use production governance/admin keys, submit live proposals, move real assets, or alter public protocol state.

## Attack surface

Map:

- proxy model and proxy generation;
- current and candidate implementation generations;
- admin/governance generation and authorization path;
- implementation/admin slot, beacon, registry, or facet-set state;
- selector/fallback routing generation;
- delegatecall context;
- storage layout and state interpretation;
- initializer/reinitializer version state;
- migration/upgrade hooks;
- rollback/downgrade path;
- upgrade invariants and downstream proxy consumers.

## Hypothesis matrix

| Hypothesis | Safe oracle | Control |
| --- | --- | --- |
| storage slot is reinterpreted after upgrade | synthetic bounded slot value and read-only proxy getter | compatible candidate layout preserves value semantics |
| reinitializer generation can be replayed | inert local initialization marker | correct initialized-version guard rejects replay |
| selector table reaches unintended facet | inert selector marker and fake facet targets | intended selector generation reaches documented target |
| rollback restores code but not compatible state | bounded migration marker and read-only getter | rollback with compatible state/migration restores prior semantics |

## Proxy/implementation/governance-generation trace

Record:

- protocol/system identity;
- local test chain reset generation;
- proxy/deployment identity and proxy generation;
- proxy model;
- current implementation generation;
- candidate implementation generation;
- implementation code revision/hash;
- implementation registry/beacon/facet-set generation;
- admin/governance identity and governance generation;
- proposal/operation generation;
- timelock/multisig generation;
- rollback/downgrade generation.

Stable addresses, role labels, or registry keys do not imply stable implementation or governance generations.

## Upgrade-authorization/commit trace

Capture:

1. initiating synthetic admin/governance principal;
2. authorization path and policy generation;
3. proposal/operation identity;
4. timelock/multisig/governance state;
5. candidate implementation code revision;
6. pre-upgrade implementation generation;
7. exact implementation/admin slot, registry, beacon, or facet update;
8. migration/upgrade hook if any;
9. upgrade commit and activation point;
10. post-upgrade implementation generation;
11. receipt/result.

Authorization is separate from correctness. A proposal or event is not the upgrade commit.

## Storage-layout/state-interpretation trace

Capture:

- storage layout identity/version;
- storage slot, byte offset, type, width, and packing;
- inheritance/layout lineage;
- mapping/array/struct root where relevant;
- storage-gap assumptions;
- pre-upgrade semantic owner;
- candidate semantic owner;
- pre-upgrade synthetic value;
- post-upgrade interpreted value;
- delegatecall consumer;
- downstream proxy consumer.

A storage layout diff is not evidence of corruption until the same proxy storage is interpreted incorrectly by the active candidate implementation.

## Initializer/reinitializer/migration trace

Record:

- proxy initialization generation;
- implementation initialization state;
- initializer/reinitializer identity;
- initialized-version state;
- caller authorization;
- one-time/version guard generation;
- migration identity/generation;
- migration preconditions;
- bounded state writes;
- upgrade commit point;
- post-migration state;
- replay/re-entry result.

Keep implementation-instance initialization separate from proxy initialization.

## Selector/fallback/beacon/facet trace

Capture:

- incoming selector or fallback route;
- selector routing generation;
- admin-special fallback behavior;
- selector-to-facet/implementation mapping;
- beacon/registry identity and generation;
- facet-set generation;
- delegate target;
- delegatecall context;
- storage context;
- final function consumer.

A selector collision or facet addition is only surface evidence until the current routing generation reaches an unintended target.

## Upgrade-invariant/bounded-consequence trace

Bind the upgrade transition to explicit invariants:

- critical role/ownership state preserved;
- accounting/state values semantically preserved;
- initialized version legal;
- intended entrypoints reachable;
- prohibited selectors unreachable;
- migration executed exactly once where required;
- rollback/downgrade state compatible;
- upgrade authority remains correct.

Record downstream proxy consumer identity, effective upgradeability capability, bounded result, and receipt/result. Use the general smart-contract invariant profile for protocol-wide invariant semantics; this runbook owns the upgrade-specific transition.

## Controlled validation

Use only:

- local proxy deployments;
- synthetic admin/user accounts;
- two or more local implementation revisions;
- fake timelock/multisig/governance state;
- bounded primitive storage values;
- inert selector/facet markers;
- deterministic storage snapshots;
- read-only proxy getters;
- reversible upgrade/downgrade operations;
- synthetic migration counters or state markers.

Recommended sequence:

1. freeze local deployment and proxy state;
2. capture current implementation, layout, initializer, routing, and governance generations;
3. establish a passing compatible-upgrade control;
4. alter one upgrade-specific causal variable;
5. commit the local upgrade;
6. locate the first wrong state interpretation, initializer state, routing target, or migration result;
7. bind the result to the active proxy consumer;
8. apply the smallest layout/guard/routing/migration fix;
9. restore the original snapshot and replay;
10. capture deterministic receipts.

## False-positive controls

Eliminate:

- intentionally compatible storage layout changes;
- expected migration-induced value changes;
- reads from implementation storage rather than proxy storage;
- intentionally changed selector ownership;
- admin-special routing;
- intentionally available reinitializer version;
- reverted upgrade transaction;
- event/log that differs from active implementation state;
- unexpected candidate build/hash;
- another governance proposal generation;
- invariant defect that predates the upgrade;
- independent reentrancy/callback root cause;
- independent oracle/external-data root cause;
- receipt from a different proxy/deployment/upgrade generation.

## Counterfactual upgradeability controls

Hold proxy state and operation intent constant while changing one variable:

- compatible versus incompatible storage layout;
- current versus stale initialized-version state;
- intended versus conflicting selector mapping;
- rollback with versus without compatible migrated state;
- current versus stale governance generation;
- original versus remediated migration hook.

Generic implementation swaps do not isolate upgrade causality.

## Alternative explanations

Before SCU4/SCU5 explicitly reject:

- layout is compatible despite metadata differences;
- migration intentionally changes the value;
- implementation instance rather than proxy context was inspected;
- routing change is documented;
- admin-special fallback explains the result;
- reinitializer version is intended;
- upgrade did not commit;
- event differs from actual active implementation;
- build/revision mismatch exists;
- another governance operation executed;
- invariant defect predates upgrade;
- reentrancy explains the effect independently;
- external-data state explains the effect independently;
- receipt belongs to another generation.

Any unresolved material alternative caps evidence at SCU2.

## Evidence capture

Capture one tuple:

`protocol/system identity + local chain/environment identity/generation + deployment/proxy identity/generation + proxy model + proxy/admin/governance identity/generation + current implementation identity/generation + candidate implementation identity/generation + implementation code revision + implementation registry/beacon/facet-set identity/generation + upgrade proposal/operation identity/generation + authorization path identity/generation + timelock/multisig/governance state generation + implementation/admin slot or registry identity + selector/fallback routing identity/generation + delegatecall/context identity + storage-layout identity/version + storage slot/type/packing identity + initializer/reinitializer identity/generation + initialized-version state + upgrade hook/migration identity/generation + pre-upgrade state snapshot + upgrade commit identity + post-upgrade state snapshot + rollback/downgrade identity/generation + invariant/result identity + downstream proxy consumer identity + effective upgradeability capability + bounded result + receipt/result`.

Useful artifacts include proxy/admin manifests, implementation hashes, slot snapshots, compiler layout metadata, selector tables, initialized-version state, migration receipts, governance/timelock state, pre/post proxy reads, and remediation replay results.

## Evidence promotion and ceiling

### SCU0 — Upgrade surface mapped

Proxy model, implementations, governance path, storage layout, initializer state, routing, beacon/facets, migration, rollback, and invariants are known.

### SCU1 — Upgrade-generation divergence observed

A repeatable implementation, layout, initializer, selector, governance, migration, or rollback generation divergence exists without final wrong-context behavior.

### SCU2 — Controlled upgrade invariant mismatch

A deterministic local upgrade proves a layout, initializer, routing, governance, migration, or rollback invariant can be violated.

### SCU3 — Inert wrong-context upgrade effect

A read-only or inert synthetic proxy consumer observes a wrong field interpretation, wrong selector target, repeated initializer state, stale implementation behavior, or illegal migration state.

### SCU4 — Bounded reversible upgrade effect

A synthetic role/balance/state/selector/migration marker or reversible local proxy-state transition is bound to the exact upgrade tuple.

### SCU5 — Regression-verified causal upgradeability proof

SCU4 plus complete proxy/implementation/governance/layout/initializer/routing/migration provenance, first harmful upgrade transition, meaningful counterfactuals, eliminated alternatives, receipt/result binding, and remediation replay.

Evidence ceiling rules:

- mapped surface only: SCU0 maximum;
- generation divergence without final effect: SCU1 maximum;
- controlled mismatch without final consumer: SCU2 maximum;
- inert/read-only wrong-context effect: SCU3 maximum;
- bounded reversible upgrade effect: SCU4 maximum;
- complete causal proof plus regression: SCU5.

## Remediation checks

Replay the exact local snapshot and verify:

1. active implementation matches the intended code revision;
2. storage layout preserves semantic state interpretation;
3. initializer/reinitializer version guards are correct;
4. migration executes exactly as intended;
5. selector/fallback/beacon/facet routing reaches intended consumers;
6. governance/timelock/multisig state binds to the committed upgrade;
7. rollback/downgrade restores compatible code and state;
8. upgrade invariants hold after the commit point;
9. positive controls still upgrade successfully;
10. deterministic receipts prove the fix.

Prefer the smallest layout, initialization guard, selector routing, migration, rollback, or upgrade-commit binding fix that restores the intended contract.
