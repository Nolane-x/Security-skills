# Wave 10 Profile #31 — Type Confusion Depth Implementation Plan

> **For agentic workers:** execute task-by-task and preserve exact test-first lineage.

**Goal:** Promote `type-confusion-analysis` into the thirty-first CI-enforced operator-depth profile with causal TCF0–TCF5 semantics and deterministic benign review cases.

**Base authority:** `main@79ef5fa450fd0d5a9cc111e8b7a9958ed38e37f5`

**Design:** `docs/superpowers/specs/2026-09-18-wave10-type-confusion-depth-design.md`

## Global constraints

- Preserve 83 canonical skills and 20 packs.
- Preserve all existing 30 operator-depth profiles.
- Keep operator-depth schema version 2.
- Do not change `skill.meta.json`, graph edges, packs, routing domains, benchmark authority, agent-eval authority, superiority-court authority, or workflows.
- Commit the dedicated #31 test before SKILL/runbook/cases/registry production-depth changes.
- Do not weaken #31 after intentional RED.
- Validation remains local/owned/sandboxed/explicitly authorized, deterministic, synthetic, inert/read-only, or bounded reversible.
- After behavioral GREEN, only README and the operator-depth contract may change before exact-head verification.

## Task 1 — Freeze #31 semantics with a dedicated RED test

Create `tests/test_type_confusion_depth.py`.

Require canonical SKILL sections:

- `## Causal type-confusion model`
- `## Object, storage, and type generations`
- `## Type-identity source and transition binding`
- `## Cast, downcast, and validator binding`
- `## Representation, layout, and active-member binding`
- `## Consumer interpretation and bounded effect`
- `## Type-confusion evidence ladder`
- `## Counterfactual type controls`
- `## Alternative explanations`
- `## Evidence ceiling`

Freeze the required distinctions from the design, including cast exists != type confusion, unchecked cast != wrong dynamic type, stale tag != stale payload, wrong logical type != memory corruption, handle value reuse != type confusion without table/type-generation mismatch, and wrong dispatch class != control-flow hijack.

Runbook must include the common six headings plus:

- Object/storage/type-generation trace
- Type-identity and transition trace
- Cast/downcast/validator trace
- Representation/layout/active-member trace
- Consumer interpretation/bounded-effect trace
- Counterfactual type controls
- Alternative explanations
- Evidence promotion and ceiling

Review matrix must contain at least:

- `stale-discriminant-after-union-transition`
- `handle-slot-type-generation-reuse`
- `unchecked-downcast-dynamic-type-mismatch`
- `shape-payload-generation-skew`

Required fields:

`hypothesis`, `safe_oracle`, `positive_control`, `negative_control`, `stop_condition`, `remediation_oracle`, `object_storage_type_generation`, `type_identity_transition_trace`, `cast_downcast_validator_state`, `representation_layout_active_member`, `consumer_interpretation`, `downstream_consumer_identity`, `effective_wrong_type_capability`, `bounded_result`, `receipt_result_binding`, `counterfactual_control`, `alternative_explanation`, `evidence_level`, `evidence_ceiling`.

Registry assertions: version 2, exactly 31 profiles, exactly one type-confusion entry, standard runbook/matrix paths, `lab_only: true`, common six required headings.

Open a Draft PR at exact test-first SHA and require intentional RED before production implementation.

## Task 2 — Deepen canonical SKILL

Modify `skills/type-confusion-analysis/SKILL.md`.

Preserve frontmatter and current workflow. Add the causal tuple, object/storage/type generations, identity-source and transition binding, cast/downcast validation, representation/layout/active-member reasoning, consumer interpretation, TCF0–TCF5, counterfactuals, alternatives, and evidence ceiling.

Do not absorb deserialization, JIT, memory-lifetime, bounds/integer, or concurrency ownership.

## Task 3 — Add operator runbook

Create `skills/type-confusion-analysis/references/operator-runbook.md`.

Use synthetic tagged unions, fake handle tables, mock/inert dispatch consumers, read-only field interpreters, shadow type metadata, and reversible owner-controlled markers.

## Task 4 — Add deterministic review cases

Create `skills/type-confusion-analysis/references/operator-review-cases.json`.

Version 1, at least the four required IDs. Every required field >= 40 non-whitespace characters. Safe oracle must name synthetic/mock/inert/read-only/controlled/fake/shadow. Stop condition must explicitly say stop/abort/do not proceed. Evidence fields use TCF0–TCF5.

## Task 5 — Register profile #31

Modify `operator-depth/profiles.json` with one alphabetically sorted entry using standard runbook/matrix paths and common six required sections. Target count 31.

## Task 6 — Repair only proven stale #30 global count assertion

Potentially modify `tests/test_bounds_integer_depth.py`.

If and only if behavioral CI shows its exact `len(profiles) == 30` assertion is the remaining extensibility failure, change that global assertion to `>= 30`. Preserve all profile-specific checks.

## Task 7 — Behavioral authority

Require full 9/9 GREEN: six OS/Python validation jobs, benchmark-core, agent-eval-core, superiority-court-core.

## Task 8 — Public docs

Only after behavioral GREEN, update `README.md` and `docs/operator-depth-contract.md` to 31 profiles, identify type-confusion as #31, summarize causal bindings, and publish TCF0–TCF5.

## Task 9 — Exact-head, guarded merge, closure

Require exact-head 9/9 GREEN, fresh base check, exact 10-path scope, mergeable PR, guarded merge by expected head SHA, verified merge parents, post-merge 9/9 GREEN, merge-tree reads, and final closure comment/readback.

## Success criterion

The merge tree has exactly 31 profiles and one valid type-confusion profile; TCF0–TCF5 is published; exact-head and post-merge CI are fully GREEN; no unauthorized authority surface changed.
