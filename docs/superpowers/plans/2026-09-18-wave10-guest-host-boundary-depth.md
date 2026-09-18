# Wave 10 Profile #24 — Guest/Host Boundary Depth Implementation Plan

**Date:** 2026-09-18  
**Design authority:** `cc5902d81542c9d2ece745294479698fb229032a`  
**Base:** `main@6030025f045b170faccc61d99a836c6c86b0d6b8`

## Goal

Promote `guest-host-boundary-analysis` from a shallow canonical skill into the twenty-fourth CI-enforced operator-depth profile while preserving the 83-skill graph, 20 packs, benchmark/cross-agent/superiority authorities, and safety model.

The implementation must prove transition-level guest→host causality rather than equating guest-controlled input, a host crash, or a sanitizer report with an escape.

## Required workflow skills

- Follow test-driven development: dedicated #24 test first, observe RED, then implement.
- If any unexpected validator/test failure appears, use systematic debugging and correct the root cause without weakening the dedicated #24 test.
- Before behavioral/final/merge completion claims, use fresh verification evidence.

## Task 1 — Freeze profile #24 semantics with a dedicated RED test

**Create:**
- `tests/test_guest_host_boundary_depth.py`

The test has four assertion groups:

1. canonical SKILL causal guest-host model;
2. operator runbook transition methodology;
3. deterministic benign review-case semantics;
4. exactly-one registry promotion from 23 to 24.

### SKILL assertions

Require these sections:

- `## Causal guest-to-host boundary model`
- `## Guest, interface, and device-generation identity`
- `## Address translation and shared-object binding`
- `## Host consumer, ownership, and effective authority`
- `## Reset, unplug, migration, and snapshot lifecycle`
- `## Guest-host evidence ladder`
- `## Counterfactual proof`
- `## Alternative explanations`
- `## Evidence ceiling`

Require the full causal chain and the distinctions frozen by the design, including GH0–GH5.

### Runbook assertions

Require common operator-depth sections plus:

- Guest principal and boundary intent trace
- Interface, device, queue, and channel identity trace
- Guest-controlled object and descriptor trace
- Address translation and IOMMU/memory-slot trace
- Shared-memory ownership and lifetime trace
- Backend/emulation-thread consumer trace
- Effective host capability trace
- Reset, hot-unplug, and async revocation trace
- Migration and snapshot lifecycle trace
- Privileged-consumer and result trace
- Counterfactual controls
- Alternative explanations
- Evidence promotion and ceiling

### Review-case assertions

Require at least four scenarios with IDs:

- `stale-descriptor-reset-generation`
- `shared-memory-revocation-lifetime`
- `address-translation-generation-binding`
- `migration-snapshot-stale-capability`

Each scenario must contain substantive machine fields for:

- hypothesis;
- safe_oracle;
- positive_control;
- negative_control;
- stop_condition;
- remediation_oracle;
- guest_principal_boundary_intent;
- interface_device_channel_identity;
- device_queue_channel_generation;
- guest_controlled_object_identity;
- address_translation_generation;
- shared_object_ownership_lifetime;
- host_consumer_identity;
- effective_host_capability;
- validation_ownership_decision;
- lifecycle_transition_generation;
- final_host_decision;
- bounded_host_result;
- receipt_result_binding;
- counterfactual_control;
- alternative_explanation;
- evidence_level;
- evidence_ceiling.

Use GH0–GH5 regex checks and benign-oracle terms.

### Registry assertion

Require schema version 2, exactly 24 profiles, exactly one `guest-host-boundary-analysis`, correct runbook/scenario paths, `lab_only: true`, and the six common required runbook sections.

### Test-first verification

Commit only the design, plan, and dedicated test before production artifacts.

Open a Draft PR on the exact test-first SHA and require RED where:

- existing canonical-skill validator passes;
- existing 23-profile registry passes;
- graph/index checks pass;
- benchmark validation/portability pass;
- agent-eval smoke passes;
- the new dedicated #24 assertions fail for missing deep semantics/runbook/cases/registry promotion;
- no unittest import/read error masks the intended RED.

Do not modify the #24 dedicated test after a valid RED.

## Task 2 — Implement the canonical SKILL depth

**Modify:**
- `skills/guest-host-boundary-analysis/SKILL.md`

Preserve:

- exact canonical frontmatter name;
- authorization metadata;
- required canonical sections `When to use`, `Preconditions`, `Workflow`, `Evidence contract`, `Stop conditions`, `Output`;
- body <= 500 lines.

Add the causal chain, identity model, GH invariants, GH0–GH5 ladder, counterfactual reasoning, alternative-explanation discipline, evidence ceiling, and explicit safe boundary.

Do not absorb detailed device-local/shared-ring root-cause methodology that belongs to adjacent canonical skills.

## Task 3 — Add the guest-host operator runbook

**Create:**
- `skills/guest-host-boundary-analysis/references/operator-runbook.md`

The runbook should provide a falsifiable transition methodology:

1. Attack surface
2. Hypothesis matrix
3. Guest principal and boundary intent trace
4. Interface/device/queue/channel identity trace
5. Guest-controlled object/descriptor trace
6. Address translation and IOMMU/memory-slot trace
7. Shared-memory ownership/lifetime trace
8. Backend/emulation-thread consumer trace
9. Effective host capability trace
10. Reset/hot-unplug/async revocation trace
11. Migration/snapshot lifecycle trace
12. Privileged-consumer/result trace
13. Controlled validation
14. False-positive controls
15. Counterfactual controls
16. Alternative explanations
17. Evidence capture
18. Evidence promotion and ceiling
19. Remediation checks

All dynamic examples remain synthetic/nested/inert/read-only/bounded.

## Task 4 — Add deterministic benign review cases

**Create:**
- `skills/guest-host-boundary-analysis/references/operator-review-cases.json`

Use schema `version: 1`, at least four scenarios, unique IDs, >=40-character substantive fields, GH evidence level/ceiling, explicit positive/negative controls, stop conditions, remediation oracle, counterfactuals, and alternative explanations.

No real host file/device/credential access is required.

## Task 5 — Register exactly one profile

**Modify:**
- `operator-depth/profiles.json`

Add exactly one sorted entry:

`guest-host-boundary-analysis`

with:

- `runbook: references/operator-runbook.md`
- `scenario_matrix: references/operator-review-cases.json`
- `lab_only: true`
- exact common required-runbook-section list.

Preserve schema version 2 and existing entries.

## Task 6 — Repair only the stale global-count assertion if required

**Potentially modify:**
- `tests/test_cryptographic_protocol_misuse_depth.py`

Current profile #23 test freezes the global registry with `len(profiles) == 23`. A valid profile #24 would therefore fail an older test for the wrong reason.

Change only the global count assertion to `len(profiles) >= 23`.

Do not modify:

- any #23 semantic assertion;
- crypto skill/runbook/review-case assertions;
- paths;
- evidence ladder checks;
- dedicated #24 test.

If the current main no longer has the stale exact-count assertion, skip this path and reduce final scope accordingly.

## Task 7 — Behavioral verification

Commit implementation artifacts atomically when possible so one SHA represents behavioral authority.

Run/observe the repository CI on the exact behavioral head.

Require full 9/9 success:

- Ubuntu Python 3.11
- Ubuntu Python 3.13
- macOS Python 3.11
- macOS Python 3.13
- Windows Python 3.11
- Windows Python 3.13
- benchmark-core
- agent-eval-core
- superiority-court-core

If CI fails:

- identify exact failing gate;
- keep dedicated #24 test unchanged;
- make the smallest root-cause correction;
- rerun full behavioral verification;
- document every failed attempt in PR provenance.

## Task 8 — Publish public docs only after behavioral GREEN

**Modify only:**
- `README.md`
- `docs/operator-depth-contract.md`

README must update current profile count 23→24, identify guest-host as the twenty-fourth profile, and summarize GH causal depth.

Operator-depth contract must add the profile bullet and GH0–GH5 evidence ladder.

After publication, prove behavioral-authority→final-head delta is exactly these two paths.

## Task 9 — Exact-head and integration gates

Require full 9/9 CI on the exact final head.

After exact-head GREEN:

- create no further commit;
- fetch current `main`;
- confirm PR base equals current `main`;
- confirm PR head equals exact-GREEN SHA;
- confirm `mergeable=true`;
- confirm changed filenames match intended scope;
- update PR provenance/body only if needed because metadata changes do not alter head SHA;
- mark Ready.

## Task 10 — Guarded merge and post-merge verification

Merge using `expected_head_sha=<exact-final-head>`.

Verify:

- merge commit SHA;
- parent 1 = pre-merge main;
- parent 2 = exact final head;
- main = merge SHA;
- GitHub merge verification.

Require post-merge push CI 9/9 success on the exact merge SHA.

Read directly from merge tree:

- `operator-depth/profiles.json` version 2, exactly 24 profiles, exactly one guest-host entry;
- README 24-profile publication;
- operator-depth contract guest-host profile and GH0–GH5 ladder.

Add a closure-provenance PR comment and read it back.

Only then declare profile #24 complete.

## Expected final scope

Normally exactly ten paths:

1. `README.md`
2. `docs/operator-depth-contract.md`
3. `docs/superpowers/plans/2026-09-18-wave10-guest-host-boundary-depth.md`
4. `docs/superpowers/specs/2026-09-18-wave10-guest-host-boundary-depth-design.md`
5. `operator-depth/profiles.json`
6. `skills/guest-host-boundary-analysis/SKILL.md`
7. `skills/guest-host-boundary-analysis/references/operator-review-cases.json`
8. `skills/guest-host-boundary-analysis/references/operator-runbook.md`
9. `tests/test_guest_host_boundary_depth.py`
10. `tests/test_cryptographic_protocol_misuse_depth.py` — one-line extensibility maintenance only.

No other path is allowed unless a verification failure demonstrates a real compatibility defect and the reason is documented before merge.
