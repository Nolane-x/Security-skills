# Wave 10 Profile #28 — Parser State Machine Depth Implementation Plan

> **For agentic workers:** execute task-by-task and preserve exact test-first lineage.

**Goal:** Promote `parser-state-machine-analysis` into the twenty-eighth CI-enforced operator-depth profile with causal PS0–PS5 semantics and deterministic benign review cases.

**Base authority:** `main@7b283ad5a2315918e82f763e4aa23d0e8e9a5594`

**Design:** `docs/superpowers/specs/2026-09-18-wave10-parser-state-machine-depth-design.md`

## Global constraints

- Preserve 83 canonical skills and 20 packs.
- Preserve all existing 27 operator-depth profiles.
- Keep operator-depth schema version 2.
- Do not change `skill.meta.json`, graph edges, packs, routing domains, benchmark authority, agent-eval authority, superiority-court authority, or workflows.
- Commit the dedicated #28 test before SKILL/runbook/cases/registry production depth changes.
- Do not weaken #28 after intentional RED.
- Validation remains local/owned/sandboxed/explicitly authorized, deterministic, synthetic, inert/read-only, or bounded reversible.
- After behavioral GREEN, only README and the operator-depth contract may change before exact-head verification.

## Task 1 — Freeze #28 semantics with a dedicated RED test

Create `tests/test_parser_state_machine_depth.py`.

Require canonical SKILL sections:

- `## Causal parser-state model`
- `## Parser, input, phase, and state generations`
- `## Transition and invariant binding`
- `## Structural metadata and semantic-object binding`
- `## Error recovery and deferred-validation binding`
- `## Nested parser and cross-record provenance`
- `## Downstream consumer and bounded semantic effect`
- `## Parser-state evidence ladder`
- `## Counterfactual parser controls`
- `## Alternative explanations`
- `## Evidence ceiling`

Freeze distinctions from the design, including malformed input != parser vulnerability, parser crash != exploitability, phase reach != invariant violation, warning/recovery != successful validation, and state divergence != downstream dangerous consumption.

Runbook must include the common six headings plus:

- Parser/input/phase-generation trace
- Transition and invariant trace
- Structural metadata and semantic-object trace
- Error-recovery and deferred-validation trace
- Nested parser and cross-record trace
- Downstream consumer and bounded-effect trace
- Counterfactual parser controls
- Alternative explanations
- Evidence promotion and ceiling

Review matrix must contain at least:

- `recovery-state-trust-promotion`
- `duplicate-record-semantic-selection`
- `nested-length-phase-drift`
- `deferred-reference-resolution-generation`

Required fields:

`hypothesis`, `safe_oracle`, `positive_control`, `negative_control`, `stop_condition`, `remediation_oracle`, `parser_input_phase_generation`, `transition_invariant_trace`, `structural_metadata_semantic_object`, `recovery_deferred_validation_state`, `nested_cross_record_provenance`, `downstream_consumer_identity`, `effective_semantic_capability`, `bounded_result`, `receipt_result_binding`, `counterfactual_control`, `alternative_explanation`, `evidence_level`, `evidence_ceiling`.

Registry assertions: version 2, exactly 28 profiles, exactly one parser-state entry, standard runbook/matrix paths, `lab_only: true`, common six required headings.

Open a Draft PR at exact test-first SHA and require intentional RED before production implementation.

## Task 2 — Deepen canonical SKILL

Modify `skills/parser-state-machine-analysis/SKILL.md`.

Preserve frontmatter and current workflow. Add the causal tuple from the design, parser/input/phase/state generations, first-invalid-transition reasoning, error recovery and deferred validation, nested/cross-record provenance, downstream consumer binding, PS0–PS5, counterfactuals, alternatives, and evidence ceiling.

Do not absorb bounds/integer, memory-lifetime, exploitability, or grammar-fuzzing ownership.

## Task 3 — Add operator runbook

Create `skills/parser-state-machine-analysis/references/operator-runbook.md`.

Use synthetic records/files, deterministic state machines, mock/read-only consumers, generation-tagged parser states, and bounded semantic markers.

## Task 4 — Add deterministic review cases

Create `skills/parser-state-machine-analysis/references/operator-review-cases.json`.

Version 1, at least the four required IDs. Every required field >= 40 non-whitespace characters. Safe oracle must name synthetic/mock/inert/read-only/controlled. Stop condition must explicitly say stop/abort/do not proceed. Evidence fields use PS0–PS5.

## Task 5 — Register profile #28

Modify `operator-depth/profiles.json` with one sorted entry using the standard runbook/matrix paths and common six required sections. Target count 28.

## Task 6 — Repair only proven stale #27 global count assertion

Potentially modify `tests/test_sandbox_boundary_depth.py`.

If and only if behavioral CI shows its exact `len(profiles) == 27` assertion is the remaining extensibility failure, change that global assertion to `>= 27`. Preserve all profile-specific checks.

## Task 7 — Behavioral authority

Require full 9/9 GREEN: six OS/Python validation jobs, benchmark-core, agent-eval-core, superiority-court-core.

## Task 8 — Public docs

Only after behavioral GREEN, update `README.md` and `docs/operator-depth-contract.md` to 28 profiles, identify parser-state-machine as #28, summarize causal bindings, and publish PS0–PS5.

## Task 9 — Exact-head, guarded merge, closure

Require exact-head 9/9 GREEN, fresh base check, exact 10-path scope, mergeable PR, guarded merge by expected head SHA, verified merge parents, post-merge 9/9 GREEN, merge-tree reads, and final closure comment.

## Success criterion

The merge tree has exactly 28 profiles and one valid parser-state-machine profile; PS0–PS5 is published; exact-head and post-merge CI are fully GREEN; no unauthorized authority surface changed.
