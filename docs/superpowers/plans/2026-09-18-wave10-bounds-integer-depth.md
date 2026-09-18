# Wave 10 Profile #30 — Bounds and Integer Depth Implementation Plan

> **For agentic workers:** execute task-by-task and preserve exact test-first lineage.

**Goal:** Promote `bounds-and-integer-analysis` into the thirtieth CI-enforced operator-depth profile with causal BND0–BND5 semantics and deterministic benign review cases.

**Base authority:** `main@a9608f01062666181a9e882fbcb96d696691887e`

**Design:** `docs/superpowers/specs/2026-09-18-wave10-bounds-integer-depth-design.md`

## Global constraints

- Preserve 83 canonical skills and 20 packs.
- Preserve all existing 29 operator-depth profiles.
- Keep operator-depth schema version 2.
- Do not change `skill.meta.json`, graph edges, packs, routing domains, benchmark authority, agent-eval authority, superiority-court authority, or workflows.
- Commit the dedicated #30 test before SKILL/runbook/cases/registry production-depth changes.
- Do not weaken #30 after intentional RED.
- Keep all dynamic validation local/owned/sandboxed/explicitly authorized and prefer synthetic values, fake objects, shadow ranges, inert/read-only consumers, bounded assertions, or sanitizer-only local fixtures.
- After behavioral GREEN, only README and `docs/operator-depth-contract.md` may change before exact-head verification.

## Task 1 — Freeze #30 semantics with a dedicated RED test

Create `tests/test_bounds_integer_depth.py`.

Require canonical SKILL sections:

- `## Causal bounds-and-integer model`
- `## Value identity, units, and representation generations`
- `## Arithmetic expression and conversion binding`
- `## Check-domain and use-domain binding`
- `## Allocation, object, region, and usable-size binding`
- `## Index, offset, stride, and access-width binding`
- `## Aggregate, alignment, and nested-size arithmetic`
- `## Bounds-and-integer evidence ladder`
- `## Counterfactual arithmetic controls`
- `## Alternative explanations`
- `## Evidence ceiling`

Freeze the non-equivalences from the design, including overflow != OOB, truncation != underallocation, allocation success != sufficient size, one-past-end pointer formation != OOB dereference, sanitizer report != exploitability, and arithmetic divergence != downstream dangerous consumption.

Runbook must include common six headings plus:

- Value/unit/representation trace
- Arithmetic and conversion trace
- Check-domain versus use-domain trace
- Allocation/object/usable-size trace
- Index/offset/stride/access-width trace
- Aggregate/alignment/nested-size trace
- Counterfactual arithmetic controls
- Alternative explanations
- Evidence promotion and ceiling

Review matrix must contain:

- `multiply-truncate-underallocation`
- `signed-negative-to-unsigned-range`
- `alignment-rounding-wrap`
- `inclusive-end-access-width-mismatch`

Required fields:

`hypothesis`, `safe_oracle`, `positive_control`, `negative_control`, `stop_condition`, `remediation_oracle`, `value_unit_representation_trace`, `arithmetic_conversion_trace`, `check_use_domain_binding`, `allocation_object_usable_size`, `index_offset_stride_access_width`, `aggregate_alignment_nested_size`, `downstream_consumer_identity`, `effective_invalid_range_capability`, `bounded_result`, `receipt_result_binding`, `counterfactual_control`, `alternative_explanation`, `evidence_level`, `evidence_ceiling`.

Registry assertions: version 2, exactly 30 profiles, exactly one bounds/integer entry, standard runbook/matrix paths, `lab_only: true`, common six required headings.

Open a Draft PR at exact test-first SHA and require intentional RED before production implementation.

## Task 2 — Deepen canonical SKILL

Modify `skills/bounds-and-integer-analysis/SKILL.md`.

Preserve frontmatter/current workflow and add:
- causal tuple;
- value identity, units, representation generations;
- conversion/arithmetic chain;
- check/use domain binding;
- allocation/object/usable-size distinction;
- access-width and exact range reasoning;
- aggregate/alignment/nested-size arithmetic;
- BND0–BND5;
- counterfactuals;
- alternative explanations;
- evidence ceiling;
- explicit ownership boundaries.

Do not absorb parser-state, memory-lifetime, sanitizer interpretation, type-confusion, or JIT ownership.

## Task 3 — Add operator runbook

Create `skills/bounds-and-integer-analysis/references/operator-runbook.md`.

Use synthetic numeric fixtures, fake allocators/objects, shadow ranges, deterministic checked arithmetic, inert/read-only range consumers, and bounded local sanitizer/assertion oracles.

## Task 4 — Add deterministic review cases

Create `skills/bounds-and-integer-analysis/references/operator-review-cases.json`.

Version 1, at least the four required IDs. Every required field >= 40 non-whitespace characters. Safe oracle must name synthetic/mock/inert/read-only/controlled. Stop condition must explicitly say stop/abort/do not proceed. Evidence fields use BND0–BND5.

## Task 5 — Register profile #30

Modify `operator-depth/profiles.json` with one alphabetically sorted entry using standard paths and common six required sections. Target count: 30.

## Task 6 — Repair only proven stale #29 global count assertion

Potentially modify `tests/test_protocol_state_machine_depth.py`.

If and only if behavioral CI proves the prior exact `len(profiles) == 29` assertion is the remaining extensibility failure, change only that global assertion to `>= 29`. Preserve all #29-specific semantics.

## Task 7 — Behavioral authority

Require full 9/9 GREEN:
- validate macOS 3.11
- validate macOS 3.13
- validate Ubuntu 3.11
- validate Ubuntu 3.13
- validate Windows 3.11
- validate Windows 3.13
- benchmark-core
- agent-eval-core
- superiority-court-core

## Task 8 — Public docs

Only after behavioral GREEN, update:
- `README.md` to 30 profiles and profile #30 summary;
- `docs/operator-depth-contract.md` with #30 + BND0–BND5.

## Task 9 — Exact-head, guarded merge, closure

Require:
1. exact-head 9/9 GREEN;
2. fresh `main` check;
3. final head ahead and 0 behind;
4. exactly ten intended paths;
5. PR mergeable;
6. guarded merge by exact expected head SHA;
7. exact merge-parent verification;
8. post-merge 9/9 GREEN;
9. merge-tree registry/docs reads;
10. closure provenance comment/readback.

## Success criterion

The merge tree has exactly 30 profiles and one valid `bounds-and-integer-analysis` profile; BND0–BND5 is published; exact-head and post-merge CI are fully GREEN; no unauthorized authority surface changed.
