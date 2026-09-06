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
