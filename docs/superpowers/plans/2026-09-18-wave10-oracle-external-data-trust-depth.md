# Wave 10 Profile #35 — Oracle And External Data Trust Depth Implementation Plan

> **For agentic workers:** execute task-by-task and preserve exact test-first lineage.

**Goal:** Promote `oracle-and-external-data-trust-analysis` into the thirty-fifth CI-enforced operator-depth profile with causal OED0–OED5 semantics and deterministic benign review cases.

**Base authority:** `main@50fadf2729baf2f8bc65e9c70f847358fda27b64`

**Design:** `docs/superpowers/specs/2026-09-18-wave10-oracle-external-data-trust-depth-design.md`

## Global constraints

- Preserve 83 canonical skills and 20 packs.
- Preserve all existing 34 operator-depth profiles.
- Keep operator-depth schema version 2.
- Do not change `skill.meta.json`, graph edges, packs, routing domains, benchmark authority, agent-eval authority, superiority-court authority, or workflows.
- Commit the dedicated #35 test before SKILL/runbook/cases/registry production-depth changes.
- Do not weaken #35 after intentional RED.
- Validation remains local/owned/sandboxed/explicitly authorized, deterministic, synthetic, inert/read-only, or bounded reversible.
- After behavioral GREEN, only README and the operator-depth contract may change before exact-head verification.

## Task 1 — Freeze #35 semantics with a dedicated RED test

Create `tests/test_oracle_external_data_trust_depth.py`.

Require canonical SKILL sections:

- `## Causal external-data trust model`
- `## Datum class, trust property, and source generations`
- `## Round, timestamp, heartbeat, and freshness binding`
- `## Unit, decimal, scale, and normalization binding`
- `## Aggregation, source diversity, and quorum binding`
- `## Fallback, emergency, and liveness-state binding`
- `## Authenticity, replay, and origin-domain binding`
- `## Consumer snapshot and invariant-reference binding`
- `## External-data evidence ladder`
- `## Counterfactual external-data controls`
- `## Alternative explanations`
- `## Evidence ceiling`

Freeze the distinctions from the design, including authenticated source != fresh source, heartbeat configured != heartbeat enforced, quorum met != independent source diversity, fallback available != fallback equivalent in trust guarantees, signed datum != intended origin-domain binding, stale oracle input != invariant violation until a consumer decision is bound, and code-level trust assumption != price manipulability.

Runbook must include common six headings plus:

- Datum/source/configuration-generation trace
- Round/freshness/heartbeat trace
- Unit/decimal/normalization trace
- Aggregation/source-diversity/quorum trace
- Fallback/liveness-state trace
- Authenticity/replay/origin-domain trace
- Consumer-snapshot/invariant-reference trace
- Counterfactual external-data controls
- Alternative explanations
- Evidence promotion and ceiling

Review matrix must contain at least:

- `stale-round-after-heartbeat-generation-change`
- `decimal-configuration-generation-drift`
- `fallback-source-diversity-downgrade`
- `cross-domain-report-binding-mismatch`

Required fields:

`hypothesis`, `safe_oracle`, `positive_control`, `negative_control`, `stop_condition`, `remediation_oracle`, `datum_source_configuration_generation`, `round_freshness_heartbeat_trace`, `unit_decimal_normalization_state`, `aggregation_source_diversity_quorum`, `fallback_liveness_state`, `authenticity_replay_origin_domain`, `consumer_snapshot_invariant_reference`, `downstream_consumer_identity`, `effective_external_data_trust_capability`, `bounded_result`, `receipt_result_binding`, `counterfactual_control`, `alternative_explanation`, `evidence_level`, `evidence_ceiling`.

Registry assertions: version 2, exactly 35 profiles, exactly one external-data trust entry, standard runbook/matrix paths, `lab_only: true`, common six required headings.

Open a Draft PR at exact test-first SHA and require intentional RED before production implementation.

## Task 2 — Deepen canonical SKILL

Modify `skills/oracle-and-external-data-trust-analysis/SKILL.md`.

Preserve frontmatter/current workflow. Add the causal tuple, datum/source/configuration generations, round/freshness policy, unit/decimal/normalization, aggregation/source diversity/quorum, fallback/liveness transitions, authenticity/replay/origin-domain binding, consumer snapshot/invariant-reference binding, OED0–OED5, counterfactuals, alternatives, and evidence ceiling.

Do not absorb smart-contract invariant, bounds/integer, randomness-lifecycle, or cryptographic-protocol ownership.

## Task 3 — Add operator runbook

Create `skills/oracle-and-external-data-trust-analysis/references/operator-runbook.md`.

Use synthetic feeds, fake reports/signatures, mock aggregators, local fork/test contracts, read-only consumers, fake accounting ledgers, and bounded reversible threshold markers.

## Task 4 — Add deterministic review cases

Create `skills/oracle-and-external-data-trust-analysis/references/operator-review-cases.json`.

Version 1, at least the four required IDs. Every required field >= 40 non-whitespace characters. Safe oracle must name synthetic/mock/inert/read-only/controlled/fake/local. Stop condition must explicitly say stop/abort/do not proceed. Evidence fields use OED0–OED5.

## Task 5 — Register profile #35

Modify `operator-depth/profiles.json` with one sorted entry using standard runbook/matrix paths and common six required sections. Target count 35.

## Task 6 — Repair only proven stale #34 global count assertion

Potentially modify `tests/test_nonce_randomness_lifecycle_depth.py`.

If and only if behavioral CI shows its exact `len(profiles) == 34` assertion is the remaining extensibility failure, change that global assertion to `>= 34`. Preserve all profile-specific checks.

## Task 7 — Behavioral authority

Require full 9/9 GREEN: six OS/Python validation jobs, benchmark-core, agent-eval-core, superiority-court-core.

## Task 8 — Public docs

Only after behavioral GREEN, update `README.md` and `docs/operator-depth-contract.md` to 35 profiles, identify oracle/external-data trust as #35, summarize causal bindings, and publish OED0–OED5.

## Task 9 — Exact-head, guarded merge, closure

Require exact-head 9/9 GREEN, fresh base check, exact 10-path scope, mergeable PR, guarded merge by expected head SHA, verified merge parents, post-merge 9/9 GREEN, merge-tree reads, and final closure comment/readback.

## Success criterion

The merge tree has exactly 35 profiles and one valid oracle/external-data trust profile; OED0–OED5 is published; exact-head and post-merge CI are fully GREEN; no unauthorized authority surface changed.
