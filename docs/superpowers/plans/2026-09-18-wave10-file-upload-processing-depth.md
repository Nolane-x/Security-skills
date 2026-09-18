# Wave 10 Profile #36 — File Upload Processing Depth Implementation Plan

> **For agentic workers:** execute task-by-task and preserve exact test-first lineage.

**Goal:** Promote `file-upload-processing-analysis` into the thirty-sixth CI-enforced operator-depth profile with causal UPL0–UPL5 semantics and deterministic benign review cases.

**Base authority:** `main@78d3a60712479fbdfd8a87070a80f9829b5c1d09`

**Design:** `docs/superpowers/specs/2026-09-18-wave10-file-upload-processing-depth-design.md`

## Global constraints

- Preserve 83 canonical skills and 20 packs.
- Preserve all existing 35 operator-depth profiles.
- Keep operator-depth schema version 2.
- Do not change `skill.meta.json`, graph edges, packs, routing domains, benchmark authority, agent-eval authority, superiority-court authority, or workflows.
- Commit the dedicated #36 test before SKILL/runbook/cases/registry production-depth changes.
- Do not weaken #36 after intentional RED.
- Validation remains local/owned/sandboxed/explicitly authorized, deterministic, synthetic, inert/read-only, or bounded reversible.
- After behavioral GREEN, only README and operator-depth contract may change before exact-head verification.

## Task 1 — Freeze #36 semantics with a dedicated RED test

Create `tests/test_file_upload_processing_depth.py`.

Require SKILL sections:

- `## Causal upload-pipeline model`
- `## Upload transaction, principal, and artifact generations`
- `## Representation and classification binding`
- `## Validation, scanning, and quarantine binding`
- `## Parser, delegate, transformation, and derived-artifact provenance`
- `## Storage promotion, object-version, and serving binding`
- `## Cleanup, derivative, and lifecycle binding`
- `## Consumer and bounded-effect binding`
- `## Upload-pipeline evidence ladder`
- `## Counterfactual upload controls`
- `## Alternative explanations`
- `## Evidence ceiling`

Freeze distinctions including upload accepted != validated, validated != promoted, promoted != served, clean original != clean transformed derivative, validator verdict != current artifact generation, and cleanup requested != object inaccessible.

Runbook must include common six headings plus:

- Upload/principal/artifact-generation trace
- Representation/classification trace
- Validation/scanning/quarantine trace
- Parser/delegate/derived-artifact trace
- Storage/object-version/serving trace
- Cleanup/derivative lifecycle trace
- Consumer/bounded-effect trace
- Counterfactual upload controls
- Alternative explanations
- Evidence promotion and ceiling

Review matrix IDs:

- `scanner-verdict-reused-after-artifact-generation-change`
- `derived-preview-inherits-source-verdict-without-revalidation`
- `declared-mime-sniffed-type-serving-policy-mismatch`
- `cleanup-removes-source-but-leaves-served-derivative-generation`

Required fields:

`hypothesis`, `safe_oracle`, `positive_control`, `negative_control`, `stop_condition`, `remediation_oracle`, `upload_principal_artifact_generation`, `representation_classification_trace`, `validation_scanning_quarantine_state`, `parser_delegate_derived_artifact`, `storage_object_version_serving_state`, `cleanup_derivative_lifecycle`, `consumer_bounded_effect`, `downstream_consumer_identity`, `effective_upload_pipeline_capability`, `bounded_result`, `receipt_result_binding`, `counterfactual_control`, `alternative_explanation`, `evidence_level`, `evidence_ceiling`.

Registry target: version 2, exactly 36 profiles, exactly one file-upload entry, standard paths, `lab_only: true`, common six sections.

Open a Draft PR at exact test-first SHA and require intentional RED before production implementation.

## Task 2 — Deepen canonical SKILL

Modify `skills/file-upload-processing-analysis/SKILL.md` with causal tuple, transaction/artifact generations, representations/classification, validation/scanning/quarantine, transform/delegate/derived-artifact lineage, storage/version/serving binding, cleanup lifecycle, consumer binding, UPL0–UPL5, counterfactuals, alternatives, evidence ceiling.

## Task 3 — Add operator runbook

Create `skills/file-upload-processing-analysis/references/operator-runbook.md` using inert text/image/document fixtures, fake archives without active content, mock scanners, local converters, fake object stores, read-only consumers, and reversible markers.

## Task 4 — Add deterministic review cases

Create `skills/file-upload-processing-analysis/references/operator-review-cases.json`, version 1 with at least the four required IDs. All required fields >= 40 non-whitespace characters. Safe oracle names synthetic/mock/inert/read-only/controlled/fake/local. Stop condition explicitly says stop/abort/do not proceed. Evidence fields use UPL0–UPL5.

## Task 5 — Register profile #36

Add one sorted entry to `operator-depth/profiles.json`, target 36.

## Task 6 — Repair only proven stale #35 global count assertion

Potentially modify `tests/test_oracle_external_data_trust_depth.py` only if CI proves its exact `len(profiles) == 35` assertion is the sole remaining extensibility failure. Change only that global assertion to `>= 35`.

## Task 7 — Behavioral authority

Require full 9/9 GREEN.

## Task 8 — Public docs

Only after behavioral GREEN, publish 36 profiles in README and operator-depth contract, including UPL0–UPL5.

## Task 9 — Exact-head, guarded merge, closure

Require exact-head 9/9 GREEN, fresh base check, exact 10-path scope, mergeable PR, guarded merge by expected head SHA, verified merge parents, post-merge 9/9 GREEN, merge-tree reads, closure comment/readback.

## Success criterion

Merge tree contains exactly 36 profiles and one valid file-upload profile; UPL0–UPL5 published; exact-head and post-merge CI fully GREEN; no unauthorized authority surface changed.
