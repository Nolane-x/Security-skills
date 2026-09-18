# Wave 10 Profile #33 — Firmware Update Trust Chain Causal Depth Design

**Date:** 2026-09-18  
**Base authority:** `main@6d8be8c8c006b6bb22f7504c99f49f0d3af70513`  
**Canonical skill:** `firmware-update-trust-chain-analysis`

## Purpose

Promote `firmware-update-trust-chain-analysis` into the thirty-third CI-enforced operator-depth profile without changing routing, graph, packs, benchmark authority, agent-eval authority, superiority-court authority, or workflow semantics.

The current skill already covers acquisition, manifests, signatures, version/hardware binding, staging, activation, rollback, recovery, archive/path handling, delta/update parsing, and partial update behavior. The missing contract is end-to-end causal identity across update generations: exactly which bundle, authenticated envelope, canonical manifest, signer/policy generation, target hardware, version/rollback domain, component set, transformed/extracted output, staging generation, activation transaction, rollback-counter commit, recovery policy, and final update result are bound together.

## Causal update model

Every promoted finding must bind one reconstructable tuple:

`device/revision identity + update path/mode identity + update attempt generation + acquired bundle identity + authenticated object/envelope identity + signer/root identity + signer/policy generation + canonical manifest identity + manifest field generation + hardware target identity + current version/rollback generation + target version + rollback domain + component-set identity + component identity/generation + authenticated component digest/metadata + transform/extraction/delta identity + delta-base identity/generation + transformed component identity + staging target/slot identity + staging generation + activation transaction identity/generation + rollback/version-state commit identity/generation + recovery/fallback path identity + recovery policy generation + final activated component-set identity + update-state consumer + effective update-trust capability + bounded result + receipt/result`

The proof must identify the first broken trust binding and show how it survives into staging, activation, version/rollback state, or recovery. Signature success alone is never enough.

## Required distinctions

Freeze these non-equivalences:

- downloaded bundle != authenticated bundle;
- authenticated bundle != authorized update;
- signature validity != authorized signer for current policy generation;
- authenticated manifest != consumed component by assumption;
- manifest field != canonical security identity until normalization/binding is proven;
- component name/version != component artifact identity;
- authenticated compressed/archive bytes != authenticated extracted object by assumption;
- authenticated delta != authenticated final reconstructed component;
- valid delta signature != correct delta base generation;
- component digest match != hardware-target authorization;
- accepted target version != monotonic rollback enforcement;
- rollback metadata presence != rollback-state commit;
- version check before staging != version check at activation by assumption;
- staged component != activated component;
- activation request != committed activation;
- update success flag != complete multi-component activation;
- partial component success != atomic update transaction;
- slot write != slot selection or boot execution;
- recovery path != normal-path policy equivalence by assumption;
- recovery signer != production signer authorization by assumption;
- rollback/fallback != stale-version acceptance without policy evidence;
- failed update != known recoverable state by assumption;
- power-loss recovery != transaction rollback by assumption;
- post-verification parsing != safe parsing;
- archive extraction success != path/component binding;
- hardware identifier string match != canonical hardware identity;
- same version number != same artifact generation;
- update receipt != installed/activated identity unless correlated;
- boot of an activated component != update-chain proof; boot execution belongs to boot-chain analysis.

## Device, policy, update-attempt, and artifact generations

Track independently:

- device identity and hardware revision;
- update path/mode identity;
- update attempt/session generation;
- current installed version generation;
- rollback-domain generation;
- root/signer policy generation;
- acquired bundle identity;
- authenticated envelope/object identity;
- canonical manifest identity;
- component-set identity;
- per-component identity/generation;
- staging generation;
- activation transaction generation;
- committed version/rollback generation;
- recovery/fallback generation.

A retry, recovery-mode transition, staged-slot switch, partial update, interrupted write, re-download, key rotation, or policy change can advance one generation without advancing another.

## Manifest, signer, hardware, and version binding

For every accepted update record:

1. authenticated object/envelope identity;
2. signer/root identity and active policy generation;
3. canonical manifest identity;
4. exact authenticated manifest fields;
5. component identifiers and digests;
6. target hardware identity and canonicalization;
7. current and target version values;
8. rollback domain/counter generation;
9. acceptance decision;
10. consumer that uses each decision.

A signature over one representation does not automatically authenticate a differently parsed, normalized, merged, defaulted, or externally resolved field.

## Component-set and transformed-artifact binding

Track separately:

- authenticated component metadata;
- fetched/embedded component bytes;
- archive member identity;
- decompressed/extracted bytes;
- delta identity;
- required delta base identity/generation;
- reconstructed output identity;
- final staged component identity.

For delta and transformed updates, require a binding from authenticated update metadata through the exact base generation and transformation to the final staged artifact. A signed patch applied to the wrong base is a distinct trust-chain hypothesis.

## Staging, activation, and transaction binding

Separate:

`update accepted -> component transformed -> component staged -> component-set completeness verified -> activation authorized -> activation committed -> version/rollback state committed -> update transaction terminal state`.

Record per-component staging receipt and the activation transaction generation. For multi-component updates, define atomicity requirements explicitly. A success flag from one component or phase cannot prove the whole update transaction committed.

## Rollback/version-state commit binding

Record:

- rollback domain;
- current authoritative version/counter generation;
- comparison semantics;
- target version;
- stage-time decision;
- activation-time decision;
- counter/version-state write;
- counter/version-state commit;
- power-loss/interruption semantics;
- retry/recovery behavior.

Accepted target version != committed rollback state. Counter advancement before durable activation can create a different failure mode than stale artifact acceptance after counter advancement.

## Recovery and fallback policy binding

For normal, recovery, local, removable, rescue, manufacturing, fallback, and A/B-slot paths in scope, record:

- update path identity;
- active root/signer policy generation;
- hardware/version/rollback policy;
- component-set binding;
- staging/activation semantics;
- rollback-state commit semantics;
- transition back to normal mode.

An intentional recovery exception is not automatically a vulnerability. Evidence must show the observed acceptance violates the documented policy for that path.

## Final update-state consumer

The final consumer for this profile is the update/staging/activation/recovery controller, not the boot execution chain.

Bind:

- final activated component-set identity;
- activation transaction generation;
- authoritative version/rollback generation after commit;
- final slot/staging state;
- recovery state if applicable;
- bounded update result;
- receipt/result.

Whether the boot chain later selects, verifies, loads, and executes that component belongs to `boot-chain-and-secure-boot-analysis`.

## Evidence ladder

Use FWU0–FWU5 exactly:

- **FWU0 — Update surface mapped:** update paths, bundle formats, roots/signers, manifests, hardware/version policy, rollback domains, transformations, staging, activation, and recovery are identified.
- **FWU1 — Identity/generation divergence observed:** a repeatable bundle/manifest/component/hardware/version/staging/activation/recovery identity or generation divergence exists without wrongful final update-state acceptance.
- **FWU2 — Controlled update-policy mismatch:** a deterministic synthetic fixture proves a signer, manifest-binding, hardware, version, rollback, component-set, transform/base, staging, activation, or recovery invariant can be violated.
- **FWU3 — Inert wrong-context update acceptance:** a mock/read-only update consumer accepts the wrong component, base generation, version generation, hardware target, policy generation, or partial component set into staging/activation state.
- **FWU4 — Bounded reversible update effect:** an owner-controlled synthetic bundle causes a bounded staged-slot marker, fake component-set activation, reversible version-state transition, or read-only recovery result bound to the exact update tuple.
- **FWU5 — Regression-verified causal update-chain proof:** FWU4 plus complete device/path/bundle/signer/manifest/component/version/rollback/staging/activation/recovery provenance, first-broken-binding trace, meaningful counterfactuals, eliminated alternatives, receipt/result binding, and remediation replay.

Downloads, valid signatures, parser success, update success flags, version strings, slot writes, recovery entry, crashes, or synthetic markers cannot skip missing causal bindings.

## Deterministic benign review cases

At minimum freeze four cases:

1. `manifest-component-resolution-substitution` — authenticated synthetic manifest metadata is valid, but staging resolves a different component identity than the authenticated component binding.
2. `delta-base-generation-mismatch` — a signed synthetic delta is applied to the wrong base generation and the reconstructed output is accepted by a mock staging consumer.
3. `rollback-counter-activation-commit-order` — synthetic activation and rollback/version-state commit occur in an unsafe order across a controlled interruption.
4. `recovery-policy-generation-drift` — recovery mode consumes a stale signer/version/hardware policy generation that differs from the documented current recovery policy.

Use only synthetic bundles, fake signers/roots, mock manifests, in-memory slots, fake counters, deterministic delta transforms, inert activation controllers, and reversible state markers.

## Counterfactual requirements

Change exactly one causal update variable while keeping the rest constant, such as:

- authenticated component identity versus substituted resolver result;
- correct versus wrong delta-base generation;
- activation commit before versus after rollback-counter commit;
- current versus stale recovery policy generation;
- canonical hardware identity versus ambiguous alias;
- complete versus partial multi-component staging set;
- authenticated transformed-output digest versus envelope-only authentication.

## Alternative explanations

Before FWU4/FWU5 eliminate:

- the update specification intentionally permits the observed path;
- recovery/manufacturing policy explicitly allows the signer/version;
- manifest normalization makes the compared representations canonically equivalent;
- the substituted component is documented as an alias of the same immutable artifact;
- delta bases are intentionally content-equivalent and identity-independent;
- at-least-once retry semantics explain duplicate staging without duplicate activation;
- the success flag refers only to staging, not activation;
- slot state observed belongs to an earlier update attempt;
- rollback counter is advisory rather than authoritative;
- power-loss behavior is documented and safely recoverable;
- the mock harness reused state across attempts;
- the receipt belongs to another device/path/transaction generation;
- a parser, canonicalization, or boot-chain defect fully explains the observation independently of update-trust binding.

Any unresolved material alternative caps evidence at FWU2.

## Ownership boundaries

- `firmware-update-trust-chain-analysis` owns device update intake through manifest/signer/hardware/version/component/transform/staging/activation/rollback/recovery binding.
- `boot-chain-and-secure-boot-analysis` owns candidate/selected/loaded/executed boot component identity, boot root/policy, verified-to-loaded binding, and boot handoff.
- `supply-chain-dependency-review` owns software dependency/build/release/distribution provenance before the device update intake boundary.
- `canonicalization-and-namespace-analysis` owns generic canonical identity transformation defects when the update issue reduces to representation normalization.
- `parser-state-machine-analysis` owns parser-local transition/recovery mechanics.
- `bounds-and-integer-analysis` owns numeric size/range/offset arithmetic.
- This profile may compose with those skills but must not duplicate their evidence ownership.

## Expected repository scope

1. `README.md`
2. `docs/operator-depth-contract.md`
3. `docs/superpowers/plans/2026-09-18-wave10-firmware-update-trust-chain-depth.md`
4. `docs/superpowers/specs/2026-09-18-wave10-firmware-update-trust-chain-depth-design.md`
5. `operator-depth/profiles.json`
6. `skills/firmware-update-trust-chain-analysis/SKILL.md`
7. `skills/firmware-update-trust-chain-analysis/references/operator-review-cases.json`
8. `skills/firmware-update-trust-chain-analysis/references/operator-runbook.md`
9. `tests/test_firmware_update_trust_chain_depth.py`
10. `tests/test_jit_invariant_depth.py` only if behavioral CI proves its exact global-count assertion is the sole extensibility defect.

Do not change `skill.meta.json`, graph edges, packs, routing domains, benchmark authority, agent-eval authority, superiority-court authority, or workflow semantics.

## Success criterion

Profile #33 is complete only when the merge tree contains exactly 33 profiles, exactly one valid `firmware-update-trust-chain-analysis` entry, FWU0–FWU5 is published, exact-head and post-merge CI are fully GREEN, merge parents are verified, and the final scope remains bounded to the intended paths.
