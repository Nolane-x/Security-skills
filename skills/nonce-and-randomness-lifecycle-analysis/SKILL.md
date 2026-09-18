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

## Causal randomness-lifecycle model

Treat every promoted nonce/randomness finding as one causal tuple:

`value class + required security property + security scope identity + key/session/device/tenant identity + generator implementation identity/version + generator instance identity/generation + generator state identity/generation + entropy source identity + seed material identity/generation + reseed epoch + process/runtime identity/generation + fork/snapshot/restart identity/generation + counter namespace identity + counter/reservation generation + allocation/synchronization identity + persistence checkpoint identity/generation + raw generated value identity + raw value generation + transform/encoding/truncation identity + final consumed value identity + consumer/cryptographic construction identity + duplicate/reuse/collision relation + effective randomness-lifecycle capability + bounded result + receipt/result`.

The proof must identify the first generator-state, scope, counter, persistence, fork/restart, transform, or reseed transition that violates the required property and then bind the resulting final consumed value to the exact consumer or cryptographic construction.

Preserve these distinctions explicitly:

- duplicate value != vulnerability without a non-repetition requirement in the same security scope;
- repeated nonce under different independent keys != same-key nonce reuse by assumption;
- predictability != repetition;
- repetition != predictability;
- statistical bias != practical prediction;
- small-sample duplicate absence != uniqueness proof;
- small-sample collision != generator-wide collision-rate proof;
- RNG API name != actual entropy/state provenance;
- deterministic generator != insecure generator when deterministic behavior is the intended contract;
- fixed seed in a test fixture != production seed reuse;
- forked process != cloned output stream when child diversification/reseed is proven;
- snapshot restore != nonce reuse when generation/domain separation changes;
- restart state reset != security failure when scope intentionally resets with a new independent key/session;
- counter reset != duplicate consumed value when namespace/key generation changes;
- counter wrap possibility != observed wrap within an affected scope;
- concurrent callers != collision without shared allocator/state evidence;
- reservation overlap != duplicate consumption unless overlapping ranges are actually consumed;
- timestamp input != predictability proof;
- low entropy estimate != recovered/predicted value by itself;
- raw RNG duplicate != final-value duplicate when transforms include unique domain data;
- final display-ID collision != security-token collision when a distinct full value governs security;
- truncation != dangerous collision until consumed security domain and width are bound;
- encoding alias != duplicate underlying random value by assumption;
- same salt != unsafe nonce reuse;
- same IV != nonce misuse unless the primitive/mode requires uniqueness or unpredictability under the bound key;
- sequence-number reuse != cryptographic nonce reuse unless construction binding is proven;
- nonce reuse observation != cryptographic exploitability;
- token duplication != token authority confusion without consumer binding;
- crash != randomness-lifecycle failure.

All dynamic validation remains local/owned/sandboxed or explicitly authorized and uses synthetic keys/tokens, fake entropy, deterministic generator fixtures, bounded counters, in-memory persistence journals, mock consumers, and read-only receipts.

## Value class, property, and security-scope binding

For each generated value identify:

- value class;
- required security property;
- security scope identity;
- key/session/device/tenant identity;
- protocol/construction epoch if relevant;
- consumer/cryptographic construction identity;
- whether the security requirement applies to raw or transformed value.

Useful value classes include nonce, IV, salt, challenge, token, identifier, sequence number, random key material, reservation ID, and domain-specific generated IDs.

A duplicate outside the relevant security scope cannot be promoted as same-scope reuse by assumption.

## Generator, seed, entropy, and reseed generations

Track independently:

- generator implementation identity/version;
- generator instance identity/generation;
- generator state identity/generation;
- entropy source identity;
- seed material identity/generation;
- initialization generation;
- reseed epoch;
- reseed trigger and result;
- deterministic test mode versus production-like mode.

RNG API name != actual entropy/state provenance. Trace the actual initialization and reseed path in the controlled build.

A fixed seed used intentionally for deterministic tests is not evidence of production seed reuse.

## Fork, snapshot, restart, and clone lifecycle

Record:

- process/runtime identity/generation;
- parent and child identities;
- fork/snapshot/restart identity/generation;
- generator state copied at the boundary;
- child diversification/reseed step;
- restored persistent state;
- new key/session/domain generation if any;
- first raw and final values produced before and after the boundary.

Forked process != cloned output stream when child diversification/reseed is proven.

Restart state reset != security failure when the security scope also resets under an independent key or session.

## Counter, namespace, reservation, and concurrency binding

For counter or hybrid generators capture:

- counter namespace identity;
- counter width and wrap semantics;
- counter/reservation generation;
- reservation range identity;
- allocation operation identity;
- allocation/synchronization identity;
- process/thread/worker identity;
- persistence checkpoint;
- consumed value/range identity;
- overlap or duplicate relation.

Concurrent callers != collision without shared allocator/state evidence.

Reservation overlap != duplicate consumption unless overlapping ranges are actually consumed by consumers in the same security scope.

Keep generic happens-before and scheduler proof with `concurrency-race-analysis`; this profile proves whether the allocator outcome violates the required nonce/randomness lifecycle property.

## Persistence and crash/restart binding

Trace:

`state mutation -> persistence intent -> durable persistence checkpoint -> generated/consumed value -> crash/restart boundary -> restored state -> next allocation/generation`.

Record the persistence checkpoint identity/generation, which values were already consumed, what state is restored, and whether the post-restart value repeats a prior consumed value in the same scope.

Persistence lag is not enough by itself. The final duplicate/reuse relation must be correlated to prior consumption.

## Transform, encoding, and truncation binding

Record:

- raw generated value identity;
- raw value generation;
- transform/encoding/truncation identity;
- output width/domain;
- canonical decoded identity where applicable;
- any added domain-separation fields;
- final consumed value identity;
- consumer equality/comparison semantics.

Raw RNG duplicate != final-value duplicate when a transform adds unique domain data.

Truncation != dangerous collision until consumed security domain and width are bound.

An encoded/display identifier may collide while a distinct full-width value still governs security; prove which representation the final consumer uses.

## Consumer/construction and bounded consequence binding

For every promoted case record:

- consumer/cryptographic construction identity;
- key/session/device/tenant scope;
- required security property;
- duplicate/reuse/collision relation;
- whether both values are accepted/consumed;
- effective randomness-lifecycle capability;
- bounded result;
- receipt/result.

Keep construction-specific cryptographic impact with `cryptographic-protocol-misuse-analysis`. This profile establishes the lifecycle property violation and its exact input binding; it does not infer broader exploitability.

## Randomness-lifecycle evidence ladder

Use NRL0–NRL5 exactly:

- **NRL0 — Randomness surface mapped.** Value classes, requirements, scopes, generators, seed/reseed paths, counters, persistence, fork/restart behavior, transforms, and consumers are identified.
- **NRL1 — State/generation divergence observed.** A repeatable generator, seed, counter, persistence, fork/restart, reservation, transform, or scope divergence exists without proving a forbidden final-value relation.
- **NRL2 — Controlled lifecycle-property mismatch.** A deterministic synthetic fixture proves the generator lifecycle can violate a documented uniqueness, non-repetition, freshness, unpredictability, collision, reservation, or persistence invariant.
- **NRL3 — Inert forbidden-value consumption.** A mock/read-only consumer accepts two values whose reuse, collision, or prediction relation violates the bound security property in the same required scope.
- **NRL4 — Bounded reversible construction effect.** A synthetic construction or inert protocol consumer reaches a bounded duplicate/reuse/prediction marker or reversible state transition causally bound to the exact lifecycle tuple.
- **NRL5 — Regression-verified causal randomness proof.** NRL4 plus complete generator/seed/scope/lifecycle/counter/persistence/transform/consumer provenance, first-invalid-transition trace, meaningful counterfactuals, eliminated alternative explanations, receipt/result binding, and remediation replay.

RNG names, weak-looking seeds, duplicate logs, small samples, statistical tests, counter values, crashes, or synthetic markers cannot skip missing causal bindings.

## Counterfactual randomness controls

Hold unrelated dimensions constant and change one causal variable:

- child reseed/diversification absent versus present;
- stale versus current persisted counter checkpoint;
- atomic versus overlapping reservation allocation;
- full-width versus truncated final consumed value;
- same key/session scope versus independently rotated scope;
- same raw output with versus without unique domain-separation input;
- current versus restored generator-state generation.

A generic “different random seed” control is insufficient when it also changes the security scope or consumer.

## Alternative explanations

Before NRL4 or NRL5 reject:

- values belong to different independent security scopes;
- key/session rotation makes repetition permitted;
- the child process performs hidden reseed/diversification;
- deterministic test mode is intentionally active;
- logs display only a truncated value while the full consumer value remains unique;
- duplicate telemetry is one value logged twice rather than two generated/consumed values;
- persistence evidence belongs to another process generation;
- reservation overlap was never consumed;
- the observed collision is within a documented allowed probability budget;
- encoding variants remain distinct to the actual consumer;
- the construction does not require the claimed property for this value class;
- another layer adds uniqueness/domain separation before final consumption;
- a concurrency defect exists but does not create a randomness-lifecycle property violation;
- the receipt belongs to another generator or security-scope generation.

Any unresolved material alternative caps evidence at NRL2.

Keep protocol/construction consequence with `cryptographic-protocol-misuse-analysis`, scheduling/happens-before with `concurrency-race-analysis`, counter arithmetic with `bounds-and-integer-analysis`, and token authority propagation with `secrets-and-token-flow-analysis`.

## Evidence ceiling

Apply the narrowest supported level:

- generator/API/scope mapping only: NRL0 maximum;
- state/generation divergence without forbidden final-value relation: NRL1 maximum;
- deterministic lifecycle-property mismatch without final consumer: NRL2 maximum;
- inert/mock forbidden final-value consumption: NRL3 maximum;
- bounded reversible construction effect: NRL4 maximum;
- only complete lifecycle provenance, first-invalid-transition proof, meaningful counterfactuals, receipts, and remediation replay reaches NRL5.

Do not promote API names, seed observations, small samples, duplicate telemetry, counter values, crashes, or statistical anomalies into stronger claims without the missing causal bindings.

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
