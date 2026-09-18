# Wave 10 Profile #34 — Nonce and Randomness Lifecycle Causal Depth Design

**Date:** 2026-09-18  
**Base authority:** `main@b8434170ce5f3be7d38e25fff9c2ca50fb1f87fb`  
**Canonical skill:** `nonce-and-randomness-lifecycle-analysis`

## Purpose

Promote `nonce-and-randomness-lifecycle-analysis` into the thirty-fourth CI-enforced operator-depth profile without changing routing, graph, packs, benchmark authority, agent-eval authority, superiority-court authority, or workflow semantics.

The current skill already distinguishes uniqueness, unpredictability, non-repetition, freshness, collision resistance, seeding, counters, persistence, restart/fork behavior, scope, width/truncation, and concurrency. The missing contract is causal state identity: exactly which generator instance, seed/reseed epoch, process/fork/restart generation, namespace/key/session/device scope, counter/reservation state, persistence checkpoint, encoding/truncation transform, and final consumer produced a duplicate, collision, repetition, or predictable sequence under a security requirement that actually forbids it.

## Causal lifecycle model

Every promoted finding must bind one reconstructable tuple:

`value class + required security property + security scope identity + key/session/device/tenant identity + generator implementation identity/version + generator instance identity/generation + generator state identity/generation + entropy source identity + seed material identity/generation + reseed epoch + process/runtime identity/generation + fork/snapshot/restart identity/generation + counter namespace identity + counter/reservation generation + allocation/synchronization identity + persistence checkpoint identity/generation + raw generated value identity + raw value generation + transform/encoding/truncation identity + final consumed value identity + consumer/cryptographic construction identity + duplicate/reuse/collision relation + effective randomness-lifecycle capability + bounded result + receipt/result`

The proof must identify the first lifecycle transition that violates the required property and bind the resulting value to the exact consumer or cryptographic construction whose requirement is affected.

## Required distinctions

Freeze these non-equivalences:

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
- same salt != unsafe nonce reuse; salt requirements are construction-specific;
- same IV != nonce misuse unless the primitive/mode requires uniqueness or unpredictability under the bound key;
- sequence-number reuse != cryptographic nonce reuse unless construction binding is proven;
- nonce reuse observation != cryptographic exploitability;
- token duplication != token authority confusion without consumer binding;
- crash != randomness-lifecycle failure.

## Value class, property, and security-scope binding

For each generated value identify:

- value class: nonce, IV, salt, challenge, token, identifier, sequence number, random key material, reservation ID, or other class;
- exact required property: uniqueness, same-key non-repetition, unpredictability, freshness, collision resistance, domain separation, or an explicit combination;
- security scope: per key, session, connection, process, device, tenant, protocol epoch, storage object, transaction, or global namespace;
- consumer/cryptographic construction identity;
- whether the construction requirement applies to raw or transformed/encoded value.

A duplicate outside the relevant scope cannot be promoted as same-scope reuse without evidence.

## Generator, seed, entropy, and reseed generations

Track independently:

- generator implementation identity/version;
- generator instance identity/generation;
- generator state identity/generation;
- entropy source identity;
- seed material identity/generation;
- initialization generation;
- reseed epoch and trigger;
- health-test or failure state where relevant;
- deterministic-test mode versus production-like mode.

Do not infer entropy quality from API names. Capture the actual seed/reseed path used by the controlled build.

## Fork, snapshot, restart, and clone lifecycle

Record:

- parent process/runtime identity/generation;
- child identity/generation;
- fork/clone/snapshot identity;
- state copied at the boundary;
- child diversification/reseed event;
- restart identity/generation;
- persisted generator/counter state restored;
- new key/session/domain generation, if any;
- first generated values before and after the lifecycle boundary.

A copied state is only a security failure if the relevant scope remains shared and the post-boundary generation can produce forbidden reuse/prediction.

## Counter, namespace, reservation, and concurrency binding

For counters or hybrid generators capture:

- counter namespace identity;
- counter width and wrap rule;
- current counter generation;
- reservation range identity;
- allocation operation identity;
- atomicity/synchronization identity;
- persistence checkpoint;
- process/thread/worker identity;
- consumed range/value identity;
- duplicate or overlap relation.

Keep generic scheduler/happens-before root cause with `concurrency-race-analysis`; this profile owns whether the resulting allocation lifecycle violates a nonce/randomness security property.

## Persistence and crash/restart binding

Trace:

`state mutation -> persistence/write intent -> durable checkpoint -> generated/consumed value -> crash/restart boundary -> restored state -> next allocation/generation`.

Record which values were consumed before the persistence checkpoint and which state is restored after restart. A persistence lag is not proof of duplicate consumption until the post-restart value is correlated to a prior consumed value in the same security scope.

## Transform, encoding, and truncation binding

Record:

- raw generated value;
- raw generation identity;
- transform/encoding/truncation identity;
- encoded width/domain;
- canonical decoded value if applicable;
- additional domain fields;
- final consumed value;
- consumer comparison/equality semantics.

Truncation or encoding can create a collision domain different from the underlying RNG state. Prove which representation the final security consumer actually uses.

## Consumer/construction and bounded consequence binding

For each promoted case record:

- consumer/cryptographic construction identity;
- key/session/device/tenant scope;
- exact required property;
- duplicate/reuse/collision relation;
- whether duplicate values are both accepted/consumed;
- effective randomness-lifecycle capability demonstrated;
- bounded result;
- receipt/result.

Keep cryptographic protocol consequence and construction-specific misuse interpretation with `cryptographic-protocol-misuse-analysis`; this profile proves the lifecycle property violation and binds it to the construction input.

## Evidence ladder

Use NRL0–NRL5 exactly:

- **NRL0 — Randomness surface mapped:** value classes, requirements, scopes, generators, seed/reseed paths, counters, persistence, fork/restart behavior, transforms, and consumers are identified.
- **NRL1 — State/generation divergence observed:** a repeatable generator, seed, counter, persistence, fork/restart, reservation, transform, or scope divergence exists without proving a forbidden final-value relation.
- **NRL2 — Controlled lifecycle-property mismatch:** a deterministic synthetic fixture proves the generator lifecycle can violate a documented uniqueness, non-repetition, freshness, unpredictability, collision, reservation, or persistence invariant.
- **NRL3 — Inert forbidden-value consumption:** a mock/read-only consumer accepts two values whose reuse/collision/prediction relation violates the bound security property in the same required scope.
- **NRL4 — Bounded reversible construction effect:** a synthetic construction or inert protocol consumer reaches a bounded duplicate/reuse/prediction marker or reversible state transition causally bound to the exact lifecycle tuple.
- **NRL5 — Regression-verified causal randomness proof:** NRL4 plus complete generator/seed/scope/lifecycle/counter/persistence/transform/consumer provenance, first-invalid-transition trace, meaningful counterfactuals, eliminated alternatives, receipt/result binding, and remediation replay.

RNG names, weak-looking seeds, duplicate logs, small samples, statistical tests, counter values, crashes, or synthetic markers cannot skip missing causal bindings.

## Deterministic benign review cases

At minimum freeze four cases:

1. `fork-cloned-generator-state-reuse` — a synthetic child inherits generator state and emits a same-scope repeated final value because diversification/reseed is absent.
2. `restart-counter-persistence-reset` — a fake persistent counter restores an earlier checkpoint after restart and reissues a same-scope consumed value.
3. `concurrent-counter-reservation-overlap` — two synthetic workers receive overlapping ranges from the same nonce namespace and a mock consumer observes duplicate consumption.
4. `truncation-encoding-domain-collapse` — distinct raw synthetic values transform into the same final consumed identifier/nonce under the security-relevant equality domain.

Use synthetic keys, fake entropy, deterministic PRNG fixtures, in-memory persistence journals, bounded counter namespaces, mock consumers, and read-only receipts only.

## Counterfactual requirements

Change exactly one causal variable while holding the rest constant, such as:

- child reseed/diversification absent versus present;
- stale versus current persisted counter checkpoint;
- atomic versus overlapping reservation allocation;
- full-width versus truncated consumed value;
- same key/session scope versus independently rotated key/session;
- same raw output with versus without unique domain-separation input;
- current versus restored generator-state generation.

## Alternative explanations

Before NRL4/NRL5 eliminate:

- values belong to different independent security scopes;
- key/session rotation makes repetition permitted for the construction;
- child process performs hidden reseed/diversification;
- deterministic test mode is enabled intentionally;
- logged/displayed value is truncated while full consumer value is unique;
- duplicate telemetry belongs to one value logged twice rather than generated twice;
- persistence receipt is stale or from another process generation;
- reservation overlap was never consumed;
- collision is expected within the documented probability budget and does not violate the required property;
- encoding variants decode to distinct consumer identities;
- the construction does not require uniqueness/unpredictability for this value class;
- another layer adds a uniqueness field before cryptographic consumption;
- a concurrency defect explains allocator overlap but no randomness-lifecycle property is violated;
- the receipt belongs to another generator/scope generation.

Any unresolved material alternative caps evidence at NRL2.

## Ownership boundaries

- `nonce-and-randomness-lifecycle-analysis` owns generator state, seed/reseed, fork/restart/snapshot, persistence, counters/reservations, transforms, and same-scope value lifecycle.
- `cryptographic-protocol-misuse-analysis` owns construction/protocol consequences such as confidentiality/authentication impact from nonce misuse.
- `concurrency-race-analysis` owns unsafe interleavings and happens-before proof when allocator races are the root cause.
- `bounds-and-integer-analysis` owns counter-width/wrap arithmetic when numeric range reasoning is the root cause.
- `secrets-and-token-flow-analysis` owns token authority/propagation after a generated token exists.
- This profile may compose with those skills but must not replace their evidence ownership.

## Expected repository scope

1. `README.md`
2. `docs/operator-depth-contract.md`
3. `docs/superpowers/plans/2026-09-18-wave10-nonce-randomness-lifecycle-depth.md`
4. `docs/superpowers/specs/2026-09-18-wave10-nonce-randomness-lifecycle-depth-design.md`
5. `operator-depth/profiles.json`
6. `skills/nonce-and-randomness-lifecycle-analysis/SKILL.md`
7. `skills/nonce-and-randomness-lifecycle-analysis/references/operator-review-cases.json`
8. `skills/nonce-and-randomness-lifecycle-analysis/references/operator-runbook.md`
9. `tests/test_nonce_randomness_lifecycle_depth.py`
10. `tests/test_firmware_update_trust_chain_depth.py` only if behavioral CI proves its exact global-count assertion is the sole extensibility defect.

Do not change `skill.meta.json`, graph edges, packs, routing domains, benchmark authority, agent-eval authority, superiority-court authority, or workflow semantics.

## Success criterion

Profile #34 is complete only when the merge tree contains exactly 34 profiles, exactly one valid `nonce-and-randomness-lifecycle-analysis` entry, NRL0–NRL5 is published, exact-head and post-merge CI are fully GREEN, merge parents are verified, and the final scope remains bounded to the intended paths.
