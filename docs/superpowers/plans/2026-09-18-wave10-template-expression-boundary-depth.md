# Wave 10 Profile #37 — Template Expression Boundary Depth Implementation Plan

> **For agentic workers:** execute task-by-task and preserve exact test-first lineage.

**Goal:** Promote `template-expression-boundary-analysis` into the thirty-seventh CI-enforced operator-depth profile with causal TEB0–TEB5 semantics and deterministic benign review cases.

**Base authority:** `main@4121862c46b8102ba42fc2ac153682bf8c9be828`

**Design:** `docs/superpowers/specs/2026-09-18-wave10-template-expression-boundary-depth-design.md`

## Global constraints

- Preserve 83 canonical skills and 20 packs.
- Preserve all existing 36 operator-depth profiles.
- Keep operator-depth schema version 2.
- Do not change `skill.meta.json`, graph edges, packs, routing domains, benchmark authority, agent-eval authority, superiority-court authority, or workflows.
- Commit the dedicated #37 test before SKILL/runbook/cases/registry production-depth changes.
- Do not weaken #37 after intentional RED.
- Validation remains local/owned/sandboxed/explicitly authorized, deterministic, synthetic, inert/read-only, or bounded reversible.
- After behavioral GREEN, only README and operator-depth contract may change before exact-head verification.

## Task 1 — Freeze #37 semantics with a dedicated RED test

Create `tests/test_template_expression_boundary_depth.py`.

Required SKILL sections:

- `## Causal template-expression model`
- `## Principal, transaction, source, and data generations`
- `## Data-to-source construction binding`
- `## Compile, cache, and source-trust binding`
- `## Evaluation context, helper, and object-graph binding`
- `## Include, import, inheritance, and nested evaluation lineage`
- `## Escaping, output context, and downstream interpretation binding`
- `## Template-expression evidence ladder`
- `## Counterfactual template-expression controls`
- `## Alternative explanations`
- `## Evidence ceiling`

Freeze distinctions from the design, including source control != data control, evaluation != injection, intended templating != unauthorized source promotion, helper reachability != sandbox escape, cache hit != current policy generation, trusted parent != trusted child by inheritance, and rendered marker != code execution.

Runbook must include common six headings plus:

- Principal/source/data-generation trace
- Data-to-source construction trace
- Compile/cache/source-trust trace
- Evaluation-context/helper/object-graph trace
- Include/import/inheritance trace
- Escaping/output-context/downstream trace
- Counterfactual template-expression controls
- Alternative explanations
- Evidence promotion and ceiling

Review matrix IDs:

- `data-concatenation-reparsed-as-expression-source`
- `compiled-template-cache-reused-after-policy-generation-change`
- `trusted-parent-includes-lower-trust-child-as-source`
- `helper-registry-generation-exposes-new-synthetic-capability`

Required fields:

`hypothesis`, `safe_oracle`, `positive_control`, `negative_control`, `stop_condition`, `remediation_oracle`, `principal_source_data_generation`, `data_to_source_construction`, `compile_cache_source_trust`, `evaluation_context_helper_object_graph`, `include_import_inheritance_lineage`, `escaping_output_downstream_state`, `downstream_consumer_identity`, `effective_template_expression_capability`, `bounded_result`, `receipt_result_binding`, `counterfactual_control`, `alternative_explanation`, `evidence_level`, `evidence_ceiling`.

Registry target: version 2, exactly 37 profiles, exactly one template-expression entry, standard paths, `lab_only: true`, common six sections.

Open a Draft PR at exact test-first SHA and require intentional RED before production implementation.

## Task 2 — Deepen canonical SKILL

Add causal tuple, source/data generations, source-construction trace, compile/cache/source trust, evaluation context/helper/object graph, nested-source lineage, escaping/output/downstream binding, TEB0–TEB5, counterfactuals, alternatives, and evidence ceiling.

## Task 3 — Add operator runbook

Use arithmetic/string markers, mock include loaders, fake helper registries, synthetic object graphs, shadow policies, read-only render sinks, and bounded reversible markers only.

## Task 4 — Add deterministic review cases

Create version-1 JSON with the four frozen IDs. All required fields >=40 non-whitespace characters; safe oracle includes synthetic/mock/inert/read-only/controlled/fake/local/shadow; stop condition explicitly says stop/abort/do not proceed; evidence fields use TEB0–TEB5.

## Task 5 — Register profile #37

Add one sorted entry to `operator-depth/profiles.json`, target 37.

## Task 6 — Repair only proven stale #36 global count assertion

Potentially modify `tests/test_file_upload_processing_depth.py` only if CI proves its exact `len(profiles) == 36` assertion is the sole remaining extensibility failure. Change only that global assertion to `>= 36`.

## Task 7 — Behavioral authority

Require full 9/9 GREEN.

## Task 8 — Public docs

Only after behavioral GREEN, publish 37 profiles in README and operator-depth contract, including TEB0–TEB5.

## Task 9 — Exact-head, guarded merge, closure

Require exact-head 9/9 GREEN, fresh base check, exact 10-path scope, mergeable PR, guarded merge by expected head SHA, verified merge parents, post-merge 9/9 GREEN, merge-tree reads, closure comment/readback.

## Success criterion

Merge tree contains exactly 37 profiles and one valid template-expression profile; TEB0–TEB5 published; exact-head and post-merge CI fully GREEN; no unauthorized authority surface changed.
