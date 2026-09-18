# Firmware Update Trust Chain Operator Runbook

Use this runbook only for local, owned, sandboxed, vendor-authorized, simulated, or explicitly authorized update paths. Prefer synthetic bundles, fake roots/signers, mock manifests, in-memory slots, fake rollback counters, deterministic delta transforms, inert activation controllers, read-only receipts, and reversible state. Do not require malicious firmware, real signing-key compromise, irreversible flashing, or unauthorized devices.

## Attack surface

Map:

- device identity and hardware revision;
- normal/recovery/fallback/local update paths;
- update attempt generation;
- bundle acquisition and authenticated envelope;
- root/signer and policy generation;
- canonical manifest and security-relevant fields;
- hardware-target and version/rollback policy;
- component-set identity and per-component metadata;
- transform/extraction/delta pipeline and delta base;
- staging targets/slots and staging generation;
- activation transaction;
- rollback/version-state commit;
- recovery/fallback policy and final update-state consumer.

## Hypothesis matrix

| Hypothesis | Safe oracle | Control |
| --- | --- | --- |
| authenticated manifest resolves a different component | synthetic bundle plus in-memory staging consumer records component identity mismatch | immutable authenticated component binding resolves the intended component |
| signed delta uses wrong base generation | fake deterministic delta transform emits read-only reconstructed digest | current base generation reconstructs the expected component |
| rollback counter and activation commit in unsafe order | mock activation controller plus fake counter records bounded transaction state | corrected commit order survives controlled interruption |
| recovery consumes stale policy generation | synthetic recovery signer/version fixture produces inert acceptance receipt | current recovery policy generation rejects stale context |

## Device/policy/update-generation trace

Record:

- device identity;
- hardware revision;
- update path/mode identity;
- update attempt generation;
- current installed version generation;
- current policy generation;
- signer/root generation;
- rollback domain and rollback generation;
- staging generation;
- activation transaction generation;
- recovery generation.

Treat retries, re-downloads, recovery transitions, interrupted updates, partial staging, slot changes, key rotation, and policy changes as independent generation transitions.

## Manifest/signer/hardware/version trace

Capture:

- acquired bundle identity;
- authenticated object/envelope identity;
- signer/root identity;
- signer/policy generation;
- canonical manifest identity;
- authenticated manifest fields;
- hardware target identity;
- current and target version;
- rollback domain;
- comparison decision;
- component-set identity.

Prove which canonical values the update policy actually consumes. A signature-valid envelope does not automatically authorize every parsed or externally resolved field.

## Component-set/transformed-artifact trace

Record:

- component-set identity;
- component identity/generation;
- authenticated component digest/metadata;
- archive/container member identity;
- transform/extraction/delta identity;
- delta base identity and delta base generation;
- transformed/reconstructed component identity;
- exact bytes/digest delivered to staging.

For signed deltas, bind the exact base generation to the final reconstructed artifact. For compressed/archive bundles, bind authenticated metadata through extraction to the staged object.

## Staging/activation/transaction trace

Separate:

1. update acceptance;
2. transform completion;
3. component staging;
4. component-set completeness;
5. activation authorization;
6. activation request;
7. committed activation;
8. rollback/version-state commit;
9. terminal transaction state.

Record staging target/slot identity, staging generation, activation transaction identity, per-component receipts, and final activated component-set identity.

## Rollback/version-state commit trace

Capture:

- rollback domain;
- authoritative current counter/version generation;
- target version;
- comparison semantics;
- stage-time decision;
- activation-time decision;
- version/counter write;
- rollback state commit;
- activation commit;
- interruption or power-loss point;
- post-recovery authoritative state.

Accepted target version is not proof that monotonic rollback state committed correctly.

## Recovery/fallback policy trace

For every relevant recovery/fallback path record:

- path identity;
- recovery policy generation;
- root/signer authority;
- hardware policy;
- version/rollback policy;
- component-set rules;
- staging/activation rules;
- rollback-state commit behavior;
- transition back to normal mode.

Do not assume recovery policy equals normal policy. Documented exceptions are controls, not vulnerabilities.

## Final update-state consumer trace

Identify the exact final update-state consumer and record:

- final activated component-set identity;
- activation transaction generation;
- final staging/slot state;
- authoritative rollback/version generation;
- recovery state if any;
- effective update-trust capability;
- bounded result;
- receipt/result.

This profile stops at the update-state boundary. Boot selection, verified-to-loaded identity, execution, and next-stage handoff belong to boot-chain analysis.

## Controlled validation

Use deterministic benign fixtures:

- synthetic update bundles;
- fake lab roots/signers;
- mock canonical manifests;
- in-memory slots;
- deterministic transform/delta functions;
- fake rollback/version counters;
- inert activation controllers;
- read-only state receipts;
- reversible transaction markers.

Recommended sequence:

1. establish a valid current-generation positive control;
2. capture all identities/generations before mutation;
3. change exactly one trust binding;
4. observe the first broken update decision;
5. trace whether it reaches staging or activation;
6. bind final update state to the exact attempt/transaction;
7. apply the minimal fix;
8. replay failing and positive controls;
9. compare deterministic receipts.

## False-positive controls

Eliminate:

- documented recovery/manufacturing exceptions;
- stale receipts from a previous update attempt;
- aliasing that resolves to the same immutable component;
- canonical-equivalent manifest forms;
- intentionally content-equivalent delta bases;
- retry-only duplicate staging;
- staging-only success flags;
- advisory rollback metadata;
- expected safe power-loss recovery;
- harness state reuse;
- a different slot or activation transaction than the one reported;
- independent parser/canonicalization/boot-chain root causes.

## Counterfactual update controls

Useful controls include:

- authenticated component identity versus substituted resolver result;
- correct versus wrong delta base generation;
- current versus stale signer/policy generation;
- canonical hardware identity versus ambiguous alias;
- complete versus partial component set;
- activation-before-counter versus counter-before-activation commit ordering;
- current versus stale recovery policy generation;
- authenticated final transformed output versus envelope-only authentication.

Change one variable while holding device, bundle, target version, and unrelated policy constant.

## Alternative explanations

Before FWU4/FWU5 explicitly reject:

- specification-permitted behavior;
- recovery/manufacturing exception;
- canonical-equivalent manifest;
- immutable alias equivalence;
- intentional base equivalence;
- retry-only staging;
- staging-only status;
- advisory counter semantics;
- safe documented interruption recovery;
- harness state leakage;
- unrelated attempt/transaction receipt;
- independent parser, canonicalization, or boot-chain defect.

Any unresolved material alternative caps evidence at FWU2.

## Evidence capture

Capture one reconstructable tuple:

`device/revision identity + update path/mode identity + update attempt generation + acquired bundle identity + authenticated object/envelope identity + signer/root identity + signer/policy generation + canonical manifest identity + manifest field generation + hardware target identity + current version/rollback generation + target version + rollback domain + component-set identity + component identity/generation + authenticated component digest/metadata + transform/extraction/delta identity + delta-base identity/generation + transformed component identity + staging target/slot identity + staging generation + activation transaction identity/generation + rollback/version-state commit identity/generation + recovery/fallback path identity + recovery policy generation + final activated component-set identity + update-state consumer + effective update-trust capability + bounded result + receipt/result`

Useful artifacts include canonical manifest snapshots, fake signer decisions, component digests, transform receipts, staging receipts, fake counter journals, activation transaction records, recovery-policy decisions, and post-remediation replay.

## Evidence promotion and ceiling

### FWU0 — Update surface mapped

Update paths, bundle formats, roots/signers, manifests, hardware/version policy, rollback domains, transformations, staging, activation, and recovery are known.

### FWU1 — Identity/generation divergence observed

A repeatable bundle, manifest, component, hardware, version, staging, activation, rollback, or recovery divergence exists without wrongful final update-state acceptance.

### FWU2 — Controlled update-policy mismatch

A deterministic synthetic fixture violates a signer, manifest, hardware, version, rollback, component-set, transform/base, staging, activation, or recovery invariant.

### FWU3 — Inert wrong-context update acceptance

A mock/read-only final update-state consumer accepts the wrong component, base generation, policy generation, hardware target, version generation, transformed artifact, or partial set into staging/activation state.

### FWU4 — Bounded reversible update effect

A synthetic bundle creates a bounded staged marker, fake component-set activation, reversible version-state transition, or read-only recovery result bound to the exact update tuple.

### FWU5 — Regression-verified causal update-chain proof

FWU4 plus complete device/path/bundle/signer/manifest/component/version/rollback/staging/activation/recovery provenance, first-broken-binding trace, meaningful counterfactuals, eliminated alternatives, receipt/result binding, and remediation replay.

Evidence ceiling rules:

- update topology/signatures/manifests/version strings only: FWU0 maximum;
- identity/generation divergence without final acceptance: FWU1 maximum;
- deterministic policy mismatch without final consumer acceptance: FWU2 maximum;
- inert wrong-context staging/activation acceptance: FWU3 maximum;
- bounded reversible update effect: FWU4 maximum;
- complete causal trust-chain proof plus regression: FWU5.

## Remediation checks

Replay the exact fixture and verify:

1. only the authorized current signer/policy generation is accepted;
2. canonical manifest fields bind to consumed component identities;
3. hardware/version/rollback decisions use current authoritative state;
4. delta transforms require the intended base generation;
5. final transformed bytes stay bound to authenticated metadata;
6. component-set completeness is enforced before activation;
7. staging generation binds to the activation transaction;
8. rollback/version-state commit ordering survives controlled interruption;
9. recovery/fallback paths enforce their documented current policy;
10. deterministic receipts bind the final update-state consumer to the repaired transaction.

Prefer the smallest manifest-binding, resolver, transform/base, transaction, rollback-commit, or recovery-policy fix that restores the intended trust chain.
