# Nonce and Randomness Lifecycle Operator Runbook

Use this runbook only for local, owned, sandboxed, benchmark/CTF, simulated, or explicitly authorized environments. Use synthetic keys/tokens, fake entropy, deterministic PRNG fixtures, in-memory journals, bounded counters, mock consumers, and read-only receipts. Never collect production session tokens or perform live prediction attacks.

## Attack surface

Map:

- value class and required property;
- security scope and key/session/device/tenant identity;
- generator implementation and generator state generation;
- entropy source, seed generation, and reseed epoch;
- process/runtime, fork, snapshot, restart, and clone lifecycle;
- counter namespace and reservation allocation;
- persistence checkpoint and crash/restart behavior;
- transform/encoding/truncation;
- final consumed value;
- consumer/cryptographic construction;
- duplicate/reuse/collision relation and bounded result.

## Hypothesis matrix

| Hypothesis | Safe oracle | Control |
| --- | --- | --- |
| fork clones generator output stream | synthetic deterministic PRNG plus mock consumer records same-scope duplicate | child reseed/diversification produces distinct stream |
| restart restores stale counter checkpoint | fake in-memory journal reissues a prior consumed counter | durable current checkpoint resumes after last consumed value |
| concurrent reservation ranges overlap | bounded fake namespace assigns overlapping ranges to synthetic workers | atomic non-overlapping allocator |
| truncation collapses distinct raw values | read-only consumer records same final truncated value | full-width final consumer preserves distinct identity |

## Value/property/security-scope trace

Record:

- value class;
- required property;
- security scope;
- key/session/device/tenant identity;
- construction epoch if any;
- whether the property applies to raw or final consumed value.

The required property must be explicit: uniqueness, same-key non-repetition, unpredictability, freshness, collision resistance, domain separation, or another documented rule.

## Generator/seed/entropy/reseed trace

Capture:

- generator implementation/version;
- generator instance and generator state generation;
- entropy source identity;
- seed generation and seed material identity;
- initialization generation;
- reseed epoch and trigger;
- deterministic test mode state.

Do not infer security from an RNG API name. Trace the actual initialization/reseed path used by the controlled build.

## Fork/snapshot/restart lifecycle trace

Capture:

- parent process/runtime generation;
- child/clone identity;
- fork or snapshot boundary;
- copied generator state;
- child diversification/reseed event;
- restart identity;
- restored state;
- new key/session scope if any;
- first outputs before and after the lifecycle transition.

A copied state is not itself proof of forbidden final-value reuse.

## Counter/namespace/reservation trace

Record:

- counter namespace;
- counter width/wrap rule;
- counter/reservation generation;
- reservation range identity;
- allocator operation;
- synchronization/atomicity;
- worker/process identity;
- consumed values/ranges;
- overlap or duplicate relation.

Reservation overlap matters only when overlapping values are actually consumed in the same required security scope.

## Persistence/crash-restart trace

Trace:

1. generator/counter state mutation;
2. persistence intent;
3. durable persistence checkpoint;
4. generated and consumed value;
5. controlled crash/restart;
6. restored state generation;
7. next generated/allocated value;
8. duplicate/reuse relation to previously consumed values.

Use an in-memory fake persistence journal or equivalent reversible fixture.

## Transform/encoding/truncation trace

Record:

- raw generated value;
- raw generation identity;
- transform/encoding/truncation operation;
- output width/domain;
- canonical decoding where relevant;
- added scope/domain fields;
- final consumed value;
- consumer equality semantics.

Prove the representation that the security consumer actually compares or feeds into a construction.

## Consumer/construction trace

Identify:

- consumer/construction identity;
- key/session/device/tenant scope;
- required property;
- both relevant final consumed values;
- duplicate/reuse/collision relation;
- effective randomness-lifecycle capability;
- bounded result;
- receipt/result.

Do not infer cryptographic exploitability from reuse alone; compose with cryptographic-protocol analysis for construction impact.

## Controlled validation

Use deterministic benign fixtures:

- synthetic keys and tokens;
- fake entropy sources;
- deterministic PRNG states;
- bounded counter namespaces;
- in-memory persistence journals;
- controlled fork/snapshot simulations;
- mock/read-only consumers;
- reversible construction markers.

Recommended sequence:

1. establish a current positive control;
2. record scope, generator state, seed/reseed, counter/persistence, transform, and consumer identities;
3. change exactly one lifecycle binding;
4. reproduce the forbidden final-value relation;
5. prove both values are consumed in the same required scope;
6. apply the minimal lifecycle fix;
7. replay failing and positive controls;
8. compare deterministic receipts.

## False-positive controls

Eliminate:

- different independent key/session scopes;
- hidden child reseed/diversification;
- intentional deterministic test mode;
- display-only truncation while full consumer values are unique;
- one value logged twice;
- stale persistence telemetry;
- overlap that is never consumed;
- construction that does not require the claimed property;
- expected collision probability within policy;
- domain separation added after the observed raw duplicate;
- receipt from another generator or scope generation.

## Counterfactual randomness controls

Useful controls include:

- fork with versus without child reseed;
- stale versus current persistence checkpoint;
- overlapping versus atomic reservations;
- full-width versus truncated consumed value;
- same security scope versus a rotated independent scope;
- same raw value with versus without unique domain-separation input;
- restored versus current generator state generation.

Change one causal variable while keeping generator implementation, consumer, and unrelated scope data constant.

## Alternative explanations

Before NRL4/NRL5 explicitly reject:

- independent scopes;
- permitted repetition after key/session rotation;
- hidden reseed;
- intended test mode;
- display-only truncation;
- duplicate logging;
- stale persistence receipt;
- unconsumed reservation overlap;
- allowed collision probability;
- consumer-distinct encodings;
- construction lacking the claimed requirement;
- downstream domain separation;
- allocator race without forbidden consumption;
- unrelated generator/scope receipt.

Any unresolved material alternative caps evidence at NRL2.

## Evidence capture

Capture one reconstructable tuple:

`value class + required security property + security scope identity + key/session/device/tenant identity + generator implementation identity/version + generator instance identity/generation + generator state identity/generation + entropy source identity + seed material identity/generation + reseed epoch + process/runtime identity/generation + fork/snapshot/restart identity/generation + counter namespace identity + counter/reservation generation + allocation/synchronization identity + persistence checkpoint identity/generation + raw generated value identity + raw value generation + transform/encoding/truncation identity + final consumed value identity + consumer/cryptographic construction identity + duplicate/reuse/collision relation + effective randomness-lifecycle capability + bounded result + receipt/result`

Useful artifacts include generator-state IDs, seed/reseed receipts, fork/restart traces, fake counter journals, reservation allocations, transform receipts, final consumer receipts, and remediation replay.

## Evidence promotion and ceiling

### NRL0 — Randomness surface mapped

Value classes, required properties, scopes, generators, seed/reseed paths, counters, persistence, lifecycle transitions, transforms, and consumers are known.

### NRL1 — State/generation divergence observed

A repeatable generator, seed, counter, persistence, fork/restart, reservation, transform, or scope divergence exists without proving forbidden final-value relation.

### NRL2 — Controlled lifecycle-property mismatch

A deterministic synthetic fixture proves a uniqueness, non-repetition, freshness, unpredictability, collision, reservation, or persistence invariant can be violated.

### NRL3 — Inert forbidden-value consumption

A mock/read-only consumer accepts values whose reuse, collision, or prediction relation violates the bound property in the same security scope.

### NRL4 — Bounded reversible construction effect

A synthetic construction or inert protocol consumer reaches a bounded duplicate/reuse/prediction marker or reversible state transition bound to the exact lifecycle tuple.

### NRL5 — Regression-verified causal randomness proof

NRL4 plus complete generator/seed/scope/lifecycle/counter/persistence/transform/consumer provenance, first-invalid-transition trace, meaningful counterfactuals, eliminated alternatives, receipt/result binding, and remediation replay.

Evidence ceiling rules:

- mapping only: NRL0 maximum;
- state/generation divergence only: NRL1 maximum;
- lifecycle-property mismatch without final consumer: NRL2 maximum;
- inert forbidden consumption: NRL3 maximum;
- bounded reversible construction effect: NRL4 maximum;
- complete causal proof plus regression: NRL5.

## Remediation checks

Replay the exact synthetic fixture and verify:

1. required property and security scope remain explicit;
2. generator state generation advances as intended;
3. seed generation and reseed epoch are current;
4. fork/snapshot/restart diversification is correct;
5. counter namespace and reservations cannot repeat consumed values;
6. persistence checkpoint advances beyond consumed state;
7. transforms/truncation preserve the intended security domain;
8. final consumed values satisfy the construction requirement;
9. deterministic receipts bind the repaired lifecycle.

Prefer the smallest state-diversification, reseed, persistence, allocator, namespace, or transform fix that restores the documented property.
