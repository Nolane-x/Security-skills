# Wave 10 Profile #33 — Firmware Update Trust Chain Depth Implementation Plan

> **For agentic workers:** execute task-by-task and preserve exact test-first lineage.

**Goal:** Promote `firmware-update-trust-chain-analysis` into the thirty-third CI-enforced operator-depth profile with causal FWU0–FWU5 semantics and deterministic benign review cases.

**Base authority:** `main@6d8be8c8c006b6bb22f7504c99f49f0d3af70513`

**Design:** `docs/superpowers/specs/2026-09-18-wave10-firmware-update-trust-chain-depth-design.md`

## Global constraints

- Preserve 83 canonical skills and 20 packs.
- Preserve all existing 32 operator-depth profiles.
- Keep operator-depth schema version 2.
- Do not change `skill.meta.json`, graph edges, packs, routing domains, benchmark authority, agent-eval authority, superiority-court authority, or workflows.
- Commit the dedicated #33 test before SKILL/runbook/cases/registry production-depth changes.
- Do not weaken #33 after intentional RED.
- Validation remains local/owned/sandboxed/explicitly authorized, deterministic, synthetic, inert/read-only, or bounded reversible.
- After behavioral GREEN, only README and the operator-depth contract may change before exact-head verification.

## Task 1 — Freeze #33 semantics with a dedicated RED test

Create `tests/test_firmware_update_trust_chain_depth.py`.

Require canonical SKILL sections:

- `## Causal firmware-update trust model`
- `## Device, policy, update-attempt, and artifact generations`
- `## Manifest, signer, hardware, and version binding`
- `## Component-set and transformed-artifact binding`
- `## Staging, activation, and transaction binding`
- `## Rollback/version-state commit binding`
- `## Recovery and fallback policy binding`
- `## Final update-state consumer`
- `## Firmware-update evidence ladder`
- `## Counterfactual update controls`
- `## Alternative explanations`
- `## Evidence ceiling`

Freeze the required distinctions from the design, including authenticated bundle != authorized update, authenticated manifest != consumed component by assumption, valid delta signature != correct delta base generation, staged component != activated component, activation request != committed activation, accepted target version != monotonic rollback enforcement, update success flag != complete multi-component activation, and boot of an activated component != update-chain proof.

Runbook must include common six headings plus:

- Device/policy/update-generation trace
- Manifest/signer/hardware/version trace
- Component-set/transformed-artifact trace
- Staging/activation/transaction trace
- Rollback/version-state commit trace
- Recovery/fallback policy trace
- Final update-state consumer trace
- Counterfactual update controls
- Alternative explanations
- Evidence promotion and ceiling

Review matrix must contain at least:

- `manifest-component-resolution-substitution`
- `delta-base-generation-mismatch`
- `rollback-counter-activation-commit-order`
- `recovery-policy-generation-drift`

Required fields:

`hypothesis`, `safe_oracle`, `positive_control`, `negative_control`, `stop_condition`, `remediation_oracle`, `device_policy_update_generation`, `manifest_signer_hardware_version`, `component_set_transformed_artifact`, `staging_activation_transaction`, `rollback_version_state_commit`, `recovery_fallback_policy`, `final_update_state_consumer`, `effective_update_trust_capability`, `bounded_result`, `receipt_result_binding`, `counterfactual_control`, `alternative_explanation`, `evidence_level`, `evidence_ceiling`.

Registry assertions: version 2, exactly 33 profiles, exactly one firmware-update entry, standard runbook/matrix paths, `lab_only: true`, common six required headings.

Open a Draft PR at exact test-first SHA and require intentional RED before production implementation.

## Task 2 — Deepen canonical SKILL

Modify `skills/firmware-update-trust-chain-analysis/SKILL.md`.

Preserve frontmatter/current workflow. Add the causal tuple, device/update/policy/artifact generations, manifest/signer/hardware/version binding, component-set/transformed-artifact lineage, staging/activation transaction binding, rollback/version-state commit semantics, recovery/fallback policy, final update-state consumer, FWU0–FWU5, counterfactuals, alternatives, and evidence ceiling.

Do not absorb boot-chain, software supply-chain, parser, canonicalization, or bounds ownership.

## Task 3 — Add operator runbook

Create `skills/firmware-update-trust-chain-analysis/references/operator-runbook.md`.

Use synthetic bundles, fake roots/signers, mock manifests, in-memory slots, deterministic delta transforms, fake rollback counters, inert activation controllers, and reversible owner-controlled markers.

## Task 4 — Add deterministic review cases

Create `skills/firmware-update-trust-chain-analysis/references/operator-review-cases.json`.

Version 1, at least the four required IDs. Every required field >= 40 non-whitespace characters. Safe oracle must name synthetic/mock/inert/read-only/controlled/fake/in-memory. Stop condition must explicitly say stop/abort/do not proceed. Evidence fields use FWU0–FWU5.

## Task 5 — Register profile #33

Modify `operator-depth/profiles.json` with one sorted entry using the standard runbook/matrix paths and common six required sections. Target count 33.

## Task 6 — Repair only proven stale #32 global count assertion

Potentially modify `tests/test_jit_invariant_depth.py`.

If and only if behavioral CI shows its exact `len(profiles) == 32` assertion is the remaining extensibility failure, change that global assertion to `>= 32`. Preserve all profile-specific checks.

## Task 7 — Behavioral authority

Require full 9/9 GREEN: six OS/Python validation jobs, benchmark-core, agent-eval-core, superiority-court-core.

## Task 8 — Public docs

Only after behavioral GREEN, update `README.md` and `docs/operator-depth-contract.md` to 33 profiles, identify firmware-update trust-chain as #33, summarize causal bindings, and publish FWU0–FWU5.

## Task 9 — Exact-head, guarded merge, closure

Require exact-head 9/9 GREEN, fresh base check, exact 10-path scope, mergeable PR, guarded merge by expected head SHA, verified merge parents, post-merge 9/9 GREEN, merge-tree reads, and final closure comment/readback.

## Success criterion

The merge tree has exactly 33 profiles and one valid firmware-update trust-chain profile; FWU0–FWU5 is published; exact-head and post-merge CI are fully GREEN; no unauthorized authority surface changed.
