---
name: firmware-update-trust-chain-analysis
description: "Analyze firmware update authenticity, rollback policy, component selection, manifest binding, version transitions, recovery images, and post-verification parsing. Use to test update trust without producing malicious firmware."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Firmware Update Trust Chain Analysis

## When to use

Use when a device accepts OTA/local/recovery updates, capsules, manifests, signed bundles, delta patches, component images, or staged boot updates.

## Preconditions

1. Use vendor-authorized test images or synthetic fixtures.
2. Pin current/target versions, hardware identifiers, signer/root configuration, and recovery path.
3. Never deploy altered unsigned payloads to production/shared devices.

## Workflow

1. Map update acquisition, transport, manifest parsing, signature verification, component/version/hardware binding, staging, activation, rollback, and recovery.
2. Identify exactly which bytes/metadata are authenticated and which fields are consumed before or after verification.
3. Check anti-rollback/version comparisons, downgrade exceptions, recovery-mode policy, and multi-component version coupling.
4. Review archive/path/canonicalization and decompression steps after signature verification for authenticated-but-unsafe parsing.
5. Use harmless mutations of synthetic/test bundles to verify rejection of wrong signer, changed manifest, wrong hardware, stale version, and component substitution.
6. Verify failed updates leave a recoverable, known state and do not silently accept partial components.

## Evidence contract

Record authenticated object, signer/root, version/hardware bindings, mutated field, rejection/acceptance point, and resulting boot/update state. Signature verification existing somewhere is not enough; prove binding to the consumed artifact.

## Causal firmware-update trust model

Treat every promoted firmware-update finding as one causal tuple:

`device/revision identity + update path/mode identity + update attempt generation + acquired bundle identity + authenticated object/envelope identity + signer/root identity + signer/policy generation + canonical manifest identity + manifest field generation + hardware target identity + current version/rollback generation + target version + rollback domain + component-set identity + component identity/generation + authenticated component digest/metadata + transform/extraction/delta identity + delta-base identity/generation + transformed component identity + staging target/slot identity + staging generation + activation transaction identity/generation + rollback/version-state commit identity/generation + recovery/fallback path identity + recovery policy generation + final activated component-set identity + update-state consumer + effective update-trust capability + bounded result + receipt/result`.

The proof must identify the first broken update-trust binding and then show how that mismatch survives into staging, activation, rollback/version state, recovery state, or the final update-state consumer. Signature success alone cannot substitute for the rest of the chain.

Preserve these distinctions explicitly:

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
- boot of an activated component != update-chain proof.

All dynamic validation remains local/owned/sandboxed or explicitly authorized. Use synthetic bundles, fake roots/signers, mock manifests, in-memory slots, deterministic delta transforms, fake counters, inert activation controllers, and reversible owner-controlled markers.

## Device, policy, update-attempt, and artifact generations

Track independently:

- device identity and hardware revision;
- update path/mode identity;
- update attempt generation;
- current installed version generation;
- current version/rollback generation;
- rollback domain and authoritative counter generation;
- signer/root identity and signer/policy generation;
- acquired bundle identity;
- authenticated object/envelope identity;
- canonical manifest identity and manifest field generation;
- component-set identity;
- component identity/generation;
- staging generation;
- activation transaction identity/generation;
- rollback/version-state commit identity/generation;
- recovery/fallback generation and recovery policy generation.

A retry, recovery-mode transition, staged-slot switch, interrupted write, re-download, partial update, key rotation, or policy change can advance one generation without advancing another.

## Manifest, signer, hardware, and version binding

For every accepted update record:

1. acquired bundle identity;
2. authenticated object/envelope identity;
3. signer/root identity;
4. signer/policy generation;
5. canonical manifest identity;
6. exact authenticated manifest fields and manifest field generation;
7. hardware target identity;
8. current version/rollback generation;
9. target version and rollback domain;
10. component-set identity and component metadata;
11. acceptance decision;
12. update-state consumer that uses the decision.

A signature over one representation does not automatically authenticate a differently parsed, normalized, merged, defaulted, aliased, or externally resolved security field.

Hardware identifier string match != canonical hardware identity. Bind aliases, model families, board revisions, SKU identifiers, component compatibility, and any wildcard semantics to a canonical hardware-target decision.

## Component-set and transformed-artifact binding

Track separately:

- component-set identity;
- component identity/generation;
- authenticated component digest/metadata;
- archive/container member identity;
- transform/extraction/delta identity;
- delta-base identity/generation;
- transformed component identity;
- final bytes delivered to staging.

For delta updates, bind the signed/authenticated delta metadata to the exact base generation and reconstructed output. Valid delta signature != correct delta base generation.

For archives or compressed updates, authenticated compressed/archive bytes != authenticated extracted object by assumption. Prove how member identity, path, transform parameters, and final staged bytes stay bound to the authenticated component metadata.

## Staging, activation, and transaction binding

Separate the update transaction:

`update accepted -> component transformed -> component staged -> component-set completeness verified -> activation authorized -> activation request -> committed activation -> rollback/version state commit -> terminal update transaction`.

Record staging target/slot identity, staging generation, per-component staging receipts, activation transaction identity/generation, component-set completeness rule, and final activated component-set identity.

Staged component != activated component. Activation request != committed activation. Update success flag != complete multi-component activation. Partial component success != atomic update transaction.

The final update-state consumer must observe the same component-set generation that passed manifest, signer, hardware, version, transform, and staging checks.

## Rollback/version-state commit binding

Record:

- rollback domain;
- authoritative current version/rollback generation;
- comparison semantics;
- target version;
- decision at intake/staging;
- decision at activation;
- rollback/version-state write;
- rollback/version-state commit identity/generation;
- activation commit ordering;
- interruption/power-loss point;
- retry and recovery semantics.

Accepted target version != monotonic rollback enforcement. Rollback metadata presence != rollback-state commit.

Counter/version advancement before durable activation is a different causal path from stale component activation after the counter has advanced. Prove commit ordering rather than inferring it from final version strings.

## Recovery and fallback policy binding

For each normal, recovery, fallback, rescue, local/removable, manufacturing, or alternate update path in scope record:

- recovery/fallback path identity;
- recovery policy generation;
- signer/root and policy generation;
- hardware target policy;
- version/rollback policy;
- component-set requirements;
- staging/activation semantics;
- rollback/version-state commit semantics;
- transition back to the normal update policy.

Recovery path != normal-path policy equivalence by assumption. Recovery signer != production signer authorization by assumption.

An intentional recovery exception is not automatically a vulnerability. The proof must show the observed acceptance violates the documented policy for that specific path and generation.

## Final update-state consumer

The final consumer for this profile is the update/staging/activation/recovery controller.

Capture:

- final activated component-set identity;
- activation transaction identity/generation;
- authoritative rollback/version-state generation after commit;
- final staging/slot state;
- recovery/fallback state if applicable;
- update-state consumer;
- effective update-trust capability;
- bounded result;
- receipt/result.

Slot write != slot selection or boot execution. Boot of an activated component != update-chain proof.

Keep candidate/selected/loaded/executed boot-component identity and boot handoff with `boot-chain-and-secure-boot-analysis`. This profile stops at the device update-state boundary.

## Firmware-update evidence ladder

Use FWU0–FWU5 exactly:

- **FWU0 — Update surface mapped.** Update paths, bundle formats, roots/signers, manifests, hardware/version policy, rollback domains, component transforms, staging, activation, and recovery are identified.
- **FWU1 — Identity/generation divergence observed.** A repeatable bundle, manifest, component, hardware, version, staging, activation, rollback, or recovery identity/generation divergence exists without wrongful final update-state acceptance.
- **FWU2 — Controlled update-policy mismatch.** A deterministic synthetic fixture proves a signer, manifest-binding, hardware, version, rollback, component-set, transform/base, staging, activation, or recovery invariant can be violated.
- **FWU3 — Inert wrong-context update acceptance.** A mock/read-only update consumer accepts the wrong component, delta-base generation, version generation, hardware target, policy generation, transformed artifact, or partial component set into staging/activation state.
- **FWU4 — Bounded reversible update effect.** An owner-controlled synthetic bundle causes a bounded staged-slot marker, fake component-set activation, reversible version-state transition, or read-only recovery result bound to the exact update tuple.
- **FWU5 — Regression-verified causal update-chain proof.** FWU4 plus complete device/path/bundle/signer/manifest/component/version/rollback/staging/activation/recovery provenance, first-broken-binding trace, meaningful counterfactuals, eliminated alternative explanations, receipt/result binding, and remediation replay.

Downloads, valid signatures, parser success, update success flags, version strings, slot writes, recovery entry, crashes, or synthetic markers cannot skip missing causal bindings.

## Counterfactual update controls

Hold unrelated update state constant and change one causal variable:

- authenticated component identity versus substituted resolver result;
- correct versus wrong delta-base generation;
- activation commit before versus after rollback/version-state commit;
- current versus stale recovery policy generation;
- canonical hardware identity versus ambiguous alias;
- complete versus partial multi-component staging set;
- authenticated transformed-output binding versus envelope-only authentication.

A generic “invalid update” comparison is insufficient when it changes multiple trust dimensions at once.

## Alternative explanations

Before FWU4 or FWU5 reject:

- the update specification intentionally permits the observed path;
- recovery/manufacturing policy explicitly allows the signer or version;
- manifest normalization makes compared representations canonically equivalent;
- the substituted component is a documented alias of the same immutable artifact;
- delta bases are intentionally content-equivalent and identity-independent;
- retry semantics explain duplicate staging without duplicate activation;
- the success flag refers only to staging rather than activation;
- observed slot state belongs to an earlier update attempt;
- rollback state is advisory rather than authoritative;
- documented power-loss behavior safely recovers;
- the mock harness reused state across attempts;
- the receipt belongs to another device/path/activation generation;
- a parser, canonicalization, or boot-chain defect independently explains the result.

Any unresolved material alternative caps evidence at FWU2.

Keep boot selection/load/execution with `boot-chain-and-secure-boot-analysis`, build/release/distribution provenance with `supply-chain-dependency-review`, generic representation normalization with `canonicalization-and-namespace-analysis`, parser mechanics with `parser-state-machine-analysis`, and numeric size/range arithmetic with `bounds-and-integer-analysis`.

## Evidence ceiling

Apply the narrowest supported level:

- mapped update topology, signatures, manifests, or version strings only: FWU0 maximum;
- identity/generation divergence without final update-state acceptance: FWU1 maximum;
- deterministic policy/binding mismatch without final consumer acceptance: FWU2 maximum;
- inert/mock wrong-context staging or activation acceptance: FWU3 maximum;
- bounded reversible update-state effect: FWU4 maximum;
- only complete trust-chain provenance, first-broken-binding proof, counterfactuals, receipts, and remediation replay reaches FWU5.

Do not promote signature validity, parser success, staged writes, recovery entry, version comparisons, crashes, or update-success telemetry into stronger claims without the missing causal bindings.

## Stop conditions

Stop if a test risks unrecoverable flash state, requires real signing-key compromise, or would bypass production update policy outside explicit authorization.

## Output

```text
update format/path:
authenticated bytes/metadata:
signer/root:
version/hardware policy:
mutation matrix:
accept/reject point:
recovery result:
evidence status:
```
