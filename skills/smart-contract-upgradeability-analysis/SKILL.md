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
