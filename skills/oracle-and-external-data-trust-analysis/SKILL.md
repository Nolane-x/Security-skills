---
name: oracle-and-external-data-trust-analysis
description: "Analyze smart-contract oracle and external-data trust: source diversity, freshness, decimals/units, heartbeat, aggregation, fallback, sequencer status, cross-chain messages, and economic dependency. Use synthetic/local feed perturbations only."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Oracle And External Data Trust Analysis

Perform any dynamic validation only in an authorized, owned lab or equivalent explicitly scoped test environment.

## When to use

Use when contract state/actions depend on price feeds, randomness beacons, bridge messages, off-chain signatures, keepers, sequencer status, time, or external protocol state.

## Preconditions

1. Use local/forked test feeds and synthetic data.
2. Document source identities, update cadence, decimals/units, fallback hierarchy, and trust assumptions.
3. Do not manipulate live markets or production oracle feeds.

## Workflow

1. Map each external datum to source, authentication, freshness, unit/decimal conversion, aggregation, and consuming invariant.
2. Check stale/zero/negative/extreme values, source disagreement, missing rounds, sequencer downtime, timestamp/round ordering, and fallback transitions.
3. Trace cross-chain or signed data through domain/chain/contract/function binding and replay controls.
4. Use bounded synthetic feed perturbations to test liquidation/accounting/state-transition thresholds locally.
5. Check whether fallback or emergency paths weaken source diversity or freshness guarantees.
6. Separate oracle-input acceptance from economic exploitability; quantify only within synthetic/local model.

## Evidence contract

Record source/config, synthetic value/round/timestamp, validation performed, consuming invariant, and observed local state consequence. Price manipulability claims require evidence beyond code-level trust assumptions.

## Stop conditions

Stop before live price manipulation, real cross-chain message injection, or transactions that could affect third-party funds.

## Output

```text
oracle/source model:
auth/freshness/units:
fallback hierarchy:
synthetic perturbation:
consuming invariant:
local consequence:
evidence status:
```
