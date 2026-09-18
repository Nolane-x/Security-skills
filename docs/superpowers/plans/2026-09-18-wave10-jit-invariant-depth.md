# Wave 10 Profile #32 — JIT Invariant Depth Implementation Plan

> **For agentic workers:** execute task-by-task and preserve exact test-first lineage.

**Goal:** Promote `jit-invariant-analysis` into the thirty-second CI-enforced operator-depth profile with causal JIT0–JIT5 semantics and deterministic benign review cases.

**Base authority:** `main@67c9fd9df58ed4ff5ecca365a9fe83a5fe17d87a`

**Design:** `docs/superpowers/specs/2026-09-18-wave10-jit-invariant-depth-design.md`

## Global constraints

- Preserve 83 canonical skills and 20 packs.
- Preserve all existing 31 operator-depth profiles.
- Keep operator-depth schema version 2.
- Do not change `skill.meta.json`, graph edges, packs, routing domains, benchmark authority, agent-eval authority, superiority-court authority, or workflows.
- Commit the dedicated #32 test before SKILL/runbook/cases/registry production-depth changes.
- Do not weaken #32 after intentional RED.
- Validation remains local/owned/sandboxed/explicitly authorized, deterministic, synthetic, inert/read-only, or bounded reversible.
- After behavioral GREEN, only README and the operator-depth contract may change before exact-head verification.

## Task 1 — Freeze #32 semantics with a dedicated RED test

Create `tests/test_jit_invariant_depth.py`.

Require canonical SKILL sections:

- `## Causal JIT-invariant model`
- `## Runtime, program, tier, and compilation generations`
- `## Feedback, speculation, and dependency binding`
- `## Guard, invalidation, and optimization-transform binding`
- `## OSR, inlining, and specialization binding`
- `## Deoptimization and frame-state reconstruction binding`
- `## Baseline/reference and semantic-consumer binding`
- `## JIT-invariant evidence ladder`
- `## Counterfactual JIT controls`
- `## Alternative explanations`
- `## Evidence ceiling`

Freeze the required distinctions from the design, including baseline/optimized mismatch != JIT bug when language semantics permit the difference, tier activation != specific pass causality, deoptimization occurred != incorrect deoptimization, stale type feedback != type confusion, stale range fact != out-of-bounds effect, and minimized trigger != same optimizer path unless tier/pass activation is preserved.

Runbook must include common six headings plus:

- Runtime/program/tier-generation trace
- Feedback/speculation/dependency trace
- Guard/invalidation/optimization-transform trace
- OSR/inlining/specialization trace
- Deopt/frame-state reconstruction trace
- Baseline/reference/semantic-consumer trace
- Counterfactual JIT controls
- Alternative explanations
- Evidence promotion and ceiling

Review matrix must contain at least:

- `stale-type-feedback-after-shape-transition`
- `range-fact-invalidated-by-side-effect`
- `deopt-frame-state-reconstruction-mismatch`
- `osr-tier-generation-assumption-leak`

Required fields:

`hypothesis`, `safe_oracle`, `positive_control`, `negative_control`, `stop_condition`, `remediation_oracle`, `runtime_program_tier_generation`, `feedback_speculation_dependency`, `guard_invalidation_transform_trace`, `osr_inlining_specialization_state`, `deopt_frame_state_reconstruction`, `baseline_reference_semantics`, `downstream_semantic_consumer`, `effective_optimized_divergence_capability`, `bounded_result`, `receipt_result_binding`, `counterfactual_control`, `alternative_explanation`, `evidence_level`, `evidence_ceiling`.

Registry assertions: version 2, exactly 32 profiles, exactly one JIT entry, standard runbook/matrix paths, `lab_only: true`, common six required headings.

Open a Draft PR at exact test-first SHA and require intentional RED before production implementation.

## Task 2 — Deepen canonical SKILL

Modify `skills/jit-invariant-analysis/SKILL.md`.

Preserve frontmatter/current workflow. Add the causal tuple, runtime/program/tier/code generations, feedback/speculation/dependency provenance, guard/invalidation/transform binding, OSR/inlining/specialization state, deopt frame-state reconstruction, baseline/reference consumer binding, JIT0–JIT5, counterfactuals, alternatives, and evidence ceiling.

Do not absorb type-confusion, bounds/integer, concurrency, differential-testing, or sanitizer ownership.

## Task 3 — Add operator runbook

Create `skills/jit-invariant-analysis/references/operator-runbook.md`.

Use toy/synthetic programs, deterministic tier controls, mock IR/pass traces, shadow values, inert/read-only semantic consumers, bounded assertions, and reversible owner-controlled markers.

## Task 4 — Add deterministic review cases

Create `skills/jit-invariant-analysis/references/operator-review-cases.json`.

Version 1, at least the four required IDs. Every required field >= 40 non-whitespace characters. Safe oracle must name synthetic/mock/inert/read-only/controlled/shadow/toy. Stop condition must explicitly say stop/abort/do not proceed. Evidence fields use JIT0–JIT5.

## Task 5 — Register profile #32

Modify `operator-depth/profiles.json` with one sorted entry using the standard runbook/matrix paths and common six required sections. Target count 32.

## Task 6 — Repair only proven stale #31 global count assertion

Potentially modify `tests/test_type_confusion_depth.py`.

If and only if behavioral CI shows its exact `len(profiles) == 31` assertion is the remaining extensibility failure, change that global assertion to `>= 31`. Preserve all profile-specific checks.

## Task 7 — Behavioral authority

Require full 9/9 GREEN: six OS/Python validation jobs, benchmark-core, agent-eval-core, superiority-court-core.

## Task 8 — Public docs

Only after behavioral GREEN, update `README.md` and `docs/operator-depth-contract.md` to 32 profiles, identify JIT invariant as #32, summarize causal bindings, and publish JIT0–JIT5.

## Task 9 — Exact-head, guarded merge, closure

Require exact-head 9/9 GREEN, fresh base check, exact 10-path scope, mergeable PR, guarded merge by expected head SHA, verified merge parents, post-merge 9/9 GREEN, merge-tree reads, and final closure comment/readback.

## Success criterion

The merge tree has exactly 32 profiles and one valid JIT-invariant profile; JIT0–JIT5 is published; exact-head and post-merge CI are fully GREEN; no unauthorized authority surface changed.
