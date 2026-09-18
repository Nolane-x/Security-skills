# Wave 10 Profile #26 — Concurrency Race Depth Implementation Plan

> **For agentic workers:** execute this plan task-by-task and preserve the test-first lineage.

**Goal:** Promote `concurrency-race-analysis` into the twenty-sixth CI-enforced operator-depth profile with causal CR0–CR5 semantics and deterministic benign review cases.

**Architecture:** Keep the canonical skill portable; add one deep operator runbook and one machine-readable review-case matrix; register both under schema v2; freeze semantics in a dedicated test before production changes; publish public docs only after behavioral GREEN.

**Base authority:** `main@4182da63931dbcaf9d2562df5f4e471bec64f4be`

**Design:** `docs/superpowers/specs/2026-09-18-wave10-concurrency-race-depth-design.md`

## Global constraints

- Preserve 83 canonical skills and 20 packs.
- Preserve all existing 25 operator-depth profiles.
- Keep `operator-depth/profiles.json` schema version 2.
- Do not modify `skill.meta.json`, graph edges, packs, routing domains, benchmark authority, agent-eval authority, superiority-court authority, or workflow semantics.
- The #26 test must be committed before SKILL deepening, runbook, matrix, or registry promotion.
- The #26 test must not be weakened after intentional RED.
- All dynamic methodology stays local/owned/sandboxed/explicitly authorized, deterministic, bounded, and benign.
- After behavioral GREEN, only `README.md` and `docs/operator-depth-contract.md` may change before exact-head verification.

---

## Task 1 — Freeze profile #26 semantics with a dedicated RED test

**Create:** `tests/test_concurrency_race_depth.py`

The test must require these canonical SKILL sections:

- `## Causal concurrency model`
- `## Shared invariant and state generations`
- `## Actor, scheduler, and operation generations`
- `## Synchronization and happens-before binding`
- `## Check/use, publication, and commit binding`
- `## Cancellation, retry, and teardown binding`
- `## Final consumer and bounded effect binding`
- `## Concurrency evidence ladder`
- `## Counterfactual schedules`
- `## Alternative explanations`
- `## Evidence ceiling`

It must freeze these distinctions:

- data race != higher-level race;
- atomic access != atomic invariant;
- lock present != protected operation;
- overlap != harmful interleaving;
- timing correlation != causal schedule;
- TOCTOU window != demonstrated stale decision use;
- cancellation requested != work revoked;
- queue order != execution order;
- retry overlap != duplicate effect;
- sanitizer race report != complete causal concurrency proof;
- crash != exploitability.

The runbook test must require the six common sections plus:

- Shared invariant and state-generation trace
- Actor and operation-generation trace
- Synchronization and happens-before trace
- Check/use and commit-point trace
- Queue, executor, and publication trace
- Cancellation, retry, and teardown trace
- Final consumer and single-effect trace
- Deterministic schedule control
- Counterfactual schedules
- Alternative explanations
- Evidence promotion and ceiling

The review matrix must include at least:

- `check-use-generation-race`
- `duplicate-completion-single-effect`
- `cancellation-commit-epoch-race`
- `publication-initialization-order-race`

Each scenario must include substantive strings for:

`hypothesis`, `safe_oracle`, `positive_control`, `negative_control`, `stop_condition`, `remediation_oracle`, `shared_invariant_state_generation`, `actor_operation_generations`, `scheduler_executor_identity`, `synchronization_happens_before`, `check_use_commit_trace`, `queue_publication_state`, `cancellation_retry_teardown_state`, `final_consumer_identity`, `effective_concurrent_capability`, `bounded_result`, `receipt_result_binding`, `counterfactual_schedule`, `alternative_explanation`, `evidence_level`, and `evidence_ceiling`.

The registry test must require version 2, exactly 26 profiles, exactly one `concurrency-race-analysis` entry, standard runbook/matrix paths, `lab_only: true`, and the common six required sections.

Open a Draft PR at the exact test-first SHA and require intentional RED before production implementation.

---

## Task 2 — Deepen the canonical skill

**Modify:** `skills/concurrency-race-analysis/SKILL.md`

Preserve frontmatter and existing portable sections.

Add the causal tuple:

`shared invariant + shared object/state identity + state generation + actor identities + operation generations + scheduler/executor + synchronization epoch + check observation + interfering transition + use/commit transition + happens-before relation + cancellation/teardown generation + final consumer + effective concurrent capability + bounded result + receipt`

Add CR0–CR5, counterfactual schedules, alternative explanations, and an explicit evidence ceiling.

Do not absorb neighboring skill ownership for lifetime, authorization, protocol legality, sanitizer interpretation, or exploitability.

---

## Task 3 — Add the operator runbook

**Create:** `skills/concurrency-race-analysis/references/operator-runbook.md`

Include the six common contract headings exactly:

- Attack surface
- Hypothesis matrix
- Controlled validation
- False-positive controls
- Evidence capture
- Remediation checks

Also include every domain-specific heading frozen by Task 1.

Use deterministic barriers, scheduler hooks, synthetic tasks, mock queues/executors, fake ledgers, inert sinks, read-only fixtures, and bounded reversible markers.

---

## Task 4 — Add deterministic benign review cases

**Create:** `skills/concurrency-race-analysis/references/operator-review-cases.json`

Use version 1 and at least the four required scenario IDs.

Every field must be at least 40 non-whitespace characters.

Each safe oracle must explicitly name a benign mechanism such as `synthetic`, `mock`, `inert`, `read-only`, or `controlled`.

Each stop condition must explicitly say `stop`, `abort`, or `do not proceed`.

Evidence fields must use CR0–CR5.

No uncontrolled production stress or impact escalation is allowed.

---

## Task 5 — Register profile #26

**Modify:** `operator-depth/profiles.json`

Add exactly one sorted entry:

- skill: `concurrency-race-analysis`
- runbook: `references/operator-runbook.md`
- scenario_matrix: `references/operator-review-cases.json`
- lab_only: `true`
- standard six required runbook sections

Target registry count: 26.

---

## Task 6 — Repair only stale previous global-count assertions if behavioral CI proves the need

**Potentially modify:** `tests/test_memory_lifetime_depth.py`

Do not preemptively change #25.

If #25 alone fails because it asserts exactly 25 total profiles, change only that global count assertion from exact 25 to at-least 25. Preserve every #25 profile-specific assertion.

Require full behavioral 9/9 GREEN after this correction.

---

## Task 7 — Publish public docs only after behavioral GREEN

**Modify only after behavioral GREEN:**

- `README.md`
- `docs/operator-depth-contract.md`

Update the profile count from 25 to 26, add `concurrency-race-analysis` as the twenty-sixth profile, and publish the CR0–CR5 causal ladder.

The delta from behavioral authority to final reviewed head must be exactly these two paths.

---

## Task 8 — Exact-head integration and closure

1. Require exact-head 9/9 GREEN.
2. Confirm current main still equals the expected base.
3. Confirm exact reviewed head and final changed-path scope.
4. Require mergeable state.
5. Guarded merge with the exact expected head SHA.
6. Verify merge parents.
7. Require post-merge 9/9 GREEN on the exact merge SHA.
8. Read the merge-tree registry, README, and operator-depth contract.
9. Record closure provenance: design, plan, test-first SHA, RED run, implementation SHAs, any minimal compatibility repair, behavioral authority, docs-only delta, exact-head run, guarded merge, merge parents, post-merge run, final scope, safety boundary, and no external-superiority claim.

## Success criterion

Profile #26 is complete only when the merge tree contains exactly 26 profiles, exactly one valid `concurrency-race-analysis` entry, CR0–CR5 is published, exact-head and post-merge CI are fully green, and no unauthorized scope expansion occurred.
