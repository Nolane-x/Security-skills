# Wave 10 Profile #20 — Boot Chain And Secure Boot Depth Design

## Status

Design authority for Wave 10 operator-depth profile #20. This deepens the existing canonical `boot-chain-and-secure-boot-analysis` skill while leaving `skill.meta.json`, graph edges, packs, routing domains, benchmark authority, agent-eval authority, superiority-court authority, and CI workflow semantics unchanged.

Base authority: `main@6b8e0f36fee255a985d39aa8178598d58e1e21ad`.

## Goal

Turn secure-boot review from a stage checklist into a causal proof of boot identity, verification authority, generation freshness, selected-vs-loaded artifact binding, transition handoff integrity, and alternate-path equivalence. Evidence must explain which root/policy authorizes which exact artifact generation at which stage, why that artifact is the one selected and loaded, what state is inherited by the next stage, and whether recovery/alternate paths preserve the same security invariant.

The profile must prevent overclaims such as treating a secure-boot-enabled flag, a signature-valid result, a measurement log, an anti-rollback field, or a verified update as proof that the currently executed boot chain is authorized and current.

## Selected approach

Three candidate directions were compared:

1. **Firmware-update trust depth.** High value, but overlaps supply-chain provenance and update-artifact reasoning more strongly.
2. **Certificate/hostname identity depth.** Strong identity binding, but narrower and partially adjacent to canonicalization/name reasoning.
3. **Boot-chain identity, authority, generation, and handoff depth.** Selected because it closes a distinct runtime trust gap: an artifact can be authentic yet not selected, selected yet not loaded, measured yet not enforced, signed yet not authorized by the active policy generation, or verified on one path while an alternate path follows different rules.

## Causal model

The canonical binding chain is:

```text
immutable or policy root-of-trust identity
-> active verification-policy/key generation
-> boot mode and path identity
-> boot target/slot/component selection
-> candidate component identity and digest
-> signature/measurement result
-> signer or verification authority decision
-> version/rollback generation decision
-> accepted component identity
-> loaded/executed component identity
-> verified-to-loaded binding
-> handoff state and next-stage security context
-> next-stage trust inheritance
-> bounded synthetic boot outcome
-> receipt/log/attestation binding
-> lifecycle, revocation, rollback, and recovery generation
```

Every evidence promotion must preserve the material transitions used by the claim.

## Core invariants and distinctions

The canonical skill and runbook must explicitly encode at least these distinctions:

- measured boot != verified boot or enforcement;
- signature validity != authorized boot signer or active verification authority;
- root key presence != proof the active boot path chains to that root;
- candidate artifact identity != selected artifact identity;
- selected artifact identity != loaded/executed artifact identity;
- digest match != approved version or rollback generation;
- rollback metadata presence != monotonic rollback enforcement;
- verified update/install != boot selection or execution;
- verification of one stage != authenticated handoff to the next stage;
- recovery/alternate slot path != equivalent verification policy by assumption;
- valid key/certificate != active authorized key generation;
- boot-success log != causal proof of the executing artifact identity;
- attestation/measurement receipt != local enforcement unless identity and freshness bindings are verified;
- mutable handoff/configuration state != authenticated policy state merely because the code image was verified;
- release/debug/manufacturing boot modes must not be conflated.

## Identity and authority model

A review must record, where applicable:

- immutable root or synthetic root identity;
- active key/policy generation and revocation state;
- boot mode and path identity;
- slot/partition/component identity;
- candidate digest/version;
- signer identity and signer authorization decision;
- anti-rollback counter/domain/generation;
- selected component identity;
- actually loaded component identity;
- next-stage consumer identity;
- handoff state identity and authentication status;
- recovery/alternate path identity;
- receipt, measurement, or synthetic trace identity.

Synthetic keys, manifests, components, counters, slots, and traces are preferred.

## Verification and selection reasoning

The review must trace:

```text
boot mode/path
-> selector inputs
-> candidate component
-> authenticated bytes/metadata
-> signer/policy lookup
-> authorization decision
-> rollback/freshness decision
-> accepted candidate
-> loader read/source
-> loaded bytes/identity
-> next-stage entry/handoff
```

A cryptographic verifier returning success establishes only the verified object under the observed policy. It does not by itself prove selection, load, execution, policy freshness, or downstream handoff.

## Lifecycle and generation model

Track generation changes for root/key rotation, revocation, policy update, rollback counters, A/B slot changes, recovery mode, manufacturing/debug mode, staged updates, failed boot fallback, power-loss recovery, bootloader update, and next-stage handoff state. A stale artifact or stale authority accepted after an authoritative generation advances is a distinct hypothesis and requires a generation-aware counterfactual.

## Evidence ladder BC0–BC5

### BC0 — surface mapped

Boot stages, roots, modes, selectors, verification points, rollback state, and alternate paths are mapped. No boundary failure is established.

### BC1 — identity or generation divergence observed

A candidate/selected/loaded artifact, signer/policy generation, path, slot, handoff, or rollback identity differs from expectation, without yet proving wrong acceptance.

### BC2 — verification/selection policy mismatch demonstrated

A deterministic fixture shows that the resolved signer, policy, version generation, selected component, or transition binding differs from the intended rule. No boot effect is required.

### BC3 — inert unauthorized acceptance

A benign synthetic marker/component/configuration is accepted at a boot transition, slot, recovery path, or handoff under an identity/authority/generation tuple that should be rejected.

### BC4 — bounded synthetic boot effect

BC3 causes a reversible owner-controlled emulator/lab effect, such as selecting a harmless synthetic marker image, reaching an inert mock next stage, or producing a read-only synthetic boot receipt through the exact path under review.

### BC5 — causal boot-chain proof

Requires BC4 plus exact root/policy identity provenance, selected-vs-loaded binding, signer authorization, rollback/freshness generation, transition/handoff trace, alternate-path control where relevant, at least one meaningful counterfactual, elimination of plausible alternative explanations, and remediation regression preserving legitimate neighboring boot behavior.

No evidence may be promoted to BC4/BC5 solely from a secure-boot flag, signature success, measurement entry, update success, log string, crash, rejected malformed image, or configuration inspection.

## Counterfactual controls

The profile should support deterministic controls such as:

- same component bytes, different authorized signer generation;
- same valid signature, signer removed from active policy;
- same component, stale vs current rollback generation;
- same selected slot metadata, loader source changed to a neighboring synthetic slot;
- same verification result, loaded-byte identity intentionally made distinguishable in a mock loader;
- normal path vs recovery/alternate path under equivalent synthetic policy;
- same verified image, authenticated vs unauthenticated handoff configuration;
- same boot receipt shape, different synthetic correlation/measurement generation;
- post-remediation intended current artifact still boots in the emulator fixture.

## Alternative explanations

The runbook must actively eliminate explanations including expected fallback after failed boot, log/telemetry delay, stale measurement data, harness observing a previous boot generation, boot-slot retry semantics, debug/manufacturing mode, expected recovery exceptions, policy propagation delay, intentional development keys, emulator-only behavior, selector-cache state, and mismatch between the file verified and the bytes actually loaded.

## Deterministic review cases

`skills/boot-chain-and-secure-boot-analysis/references/operator-review-cases.json` must include at least:

1. `root-policy-component-binding` — proves the exact synthetic root/policy generation authorizes the exact component identity selected for the current path.
2. `rollback-slot-loaded-identity-binding` — proves rollback generation and slot selection bind to the bytes actually loaded, not merely a verified candidate or manifest.
3. `recovery-handoff-generation-binding` — proves recovery/alternate paths and next-stage handoff preserve required authority/generation semantics and invalidate stale state.

Each case must use benign synthetic or emulator fixtures and contain substantive common and domain-specific fields.

## Machine-readable case contract

Required fields are:

- `id`
- `hypothesis`
- `safe_oracle`
- `positive_control`
- `negative_control`
- `stop_condition`
- `remediation_oracle`
- `root_of_trust_identity`
- `verification_policy_generation`
- `boot_mode_path`
- `selector_state`
- `candidate_component_identity`
- `candidate_digest_version`
- `signer_identity`
- `signer_authorization_decision`
- `rollback_domain_generation`
- `selected_component_identity`
- `loaded_component_identity`
- `verified_loaded_binding`
- `handoff_state_identity`
- `next_stage_consumer`
- `alternate_recovery_path`
- `bounded_boot_result`
- `receipt_attestation_binding`
- `lifecycle_generation`
- `counterfactual_control`
- `alternative_explanation`
- `evidence_level`
- `evidence_ceiling`

All textual fields must be substantive, not placeholders.

## Runbook sections

The deep runbook must contain the common operator-depth sections plus:

- Attack surface
- Hypothesis matrix
- Root-of-trust and policy-generation trace
- Boot-mode and path trace
- Component selection and identity trace
- Signature and signer-authority trace
- Rollback and freshness-generation trace
- Selected-versus-loaded binding trace
- Handoff and next-stage inheritance trace
- Recovery and alternate-path equivalence trace
- Receipt, measurement, and attestation trace
- Lifecycle/revocation generation trace
- Controlled validation
- False-positive controls
- Counterfactual controls
- Alternative explanations
- Evidence capture
- Evidence promotion and ceiling
- Remediation checks

## Safety boundary

Validation is limited to owned lab hardware with documented recovery, emulators, synthetic ROM/bootloader/component fixtures, synthetic keys and policy manifests, mock selectors/loaders, inert next stages, read-only traces, and bounded reversible effects. Do not require production signing keys, real key compromise, fuse modification, persistent security disablement, destructive flashing, boot bypass recipes, arbitrary code execution, unrecoverable device changes, third-party devices, or unauthorized systems.

## Registry and test contract

Add exactly one `boot-chain-and-secure-boot-analysis` entry to `operator-depth/profiles.json`, with `references/operator-runbook.md`, `references/operator-review-cases.json`, `lab_only: true`, and the unchanged common required sections. Registry schema remains version 2.

Add `tests/test_boot_chain_secure_boot_depth.py` with four test groups: canonical skill semantics, transition-level runbook, deterministic review-case matrix, and additive twentieth-profile registration. Commit and observe RED before production behavior is added; do not weaken the dedicated test after a valid RED.

## Exact scope

The PR must change exactly nine paths:

1. `README.md`
2. `docs/operator-depth-contract.md`
3. `docs/superpowers/plans/2026-09-17-wave10-boot-chain-secure-boot-depth.md`
4. `docs/superpowers/specs/2026-09-17-wave10-boot-chain-secure-boot-depth-design.md`
5. `operator-depth/profiles.json`
6. `skills/boot-chain-and-secure-boot-analysis/SKILL.md`
7. `skills/boot-chain-and-secure-boot-analysis/references/operator-review-cases.json`
8. `skills/boot-chain-and-secure-boot-analysis/references/operator-runbook.md`
9. `tests/test_boot_chain_secure_boot_depth.py`

Explicitly out of scope: `skill.meta.json`, graph edges, packs, routing domains, benchmark fixtures/thresholds, agent-eval authority, superiority-court authority, workflow semantics, and external-vendor superiority claims.

## TDD and integration gates

1. Isolated branch from exact base SHA.
2. Design spec commit and self-review.
3. Implementation plan commit.
4. Dedicated test-only commit.
5. Draft PR on exact test-first SHA.
6. Clean RED: dedicated assertions fail for missing depth while old gates remain green and unittest has no unexpected errors.
7. Implement skill, runbook, review cases, and one registry entry without editing the dedicated test.
8. Full behavioral GREEN across six OS/Python matrix jobs plus benchmark-core, agent-eval-core, superiority-court-core.
9. Only after behavioral GREEN, update the two public docs.
10. Prove post-GREEN delta is docs-only and total PR scope is exactly nine paths.
11. Require exact-head full GREEN on the final candidate; no commits afterward.
12. Freshly verify PR head/base/scope/mergeability and no main drift.
13. Mark Ready and merge guarded by exact expected head SHA.
14. Verify merge parents and post-merge push CI on exact merge SHA.
15. Verify registry/docs directly on merge SHA and write closure provenance.

## Non-goals

This profile does not provide secure-boot bypass instructions, claim exploitability from configuration alone, require destructive device experimentation, or claim empirical superiority over an external security system.