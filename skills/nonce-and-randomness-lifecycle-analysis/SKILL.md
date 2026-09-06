---
name: nonce-and-randomness-lifecycle-analysis
description: "Analyze nonce, IV, salt, token, identifier, and cryptographic randomness generation/lifecycle for uniqueness, unpredictability, persistence, fork/restart behavior, scope, counters, and concurrency. Use to prove reuse/collision conditions with synthetic traces."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Nonce And Randomness Lifecycle Analysis

Perform any dynamic validation only in an authorized, owned lab or equivalent explicitly scoped test environment.

## When to use

Use when security depends on unique nonces/IVs, random challenges/tokens, salts, sequence numbers, generated IDs, or RNG state across processes/devices/restarts.

## Preconditions

1. Use synthetic keys/tokens and a controlled build.
2. Pin RNG source, OS/runtime, process/fork model, persistence and concurrency settings.
3. Do not collect or expose real session tokens.

## Workflow

1. For each value, classify requirement: uniqueness, unpredictability, non-repetition per key, freshness, or merely collision resistance.
2. Trace generation source, state seeding, counters, serialization/persistence, reset/restart/fork behavior, and scope (per key/session/device/tenant).
3. Review width/truncation/encoding conversions and counter wrap.
4. Stress concurrency/fork/restart with synthetic runs and collect only non-sensitive generated values.
5. Measure duplicate/reuse conditions deterministically where possible; avoid statistical overclaiming from small samples.
6. Tie any reuse to the exact primitive/protocol security requirement rather than declaring all duplicates exploitable.

## Evidence contract

Record value class, required property, generator/state scope, synthetic trace, duplicate/reuse condition, and affected cryptographic construction. A weak-looking RNG API name is insufficient without tracing actual state/use.

## Stop conditions

Stop before logging real tokens/nonces tied to production secrets or performing large-scale prediction attacks against live systems.

## Output

```text
value type:
required property:
generator/state scope:
restart/fork/concurrency behavior:
synthetic trace:
reuse/collision condition:
protocol consequence:
evidence status:
```
