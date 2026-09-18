# Wave 10 Profile #34 — Nonce and Randomness Lifecycle Depth Implementation Plan

> **For agentic workers:** execute task-by-task and preserve exact test-first lineage.

**Goal:** Promote `nonce-and-randomness-lifecycle-analysis` into the thirty-fourth CI-enforced operator-depth profile with causal NRL0–NRL5 semantics and deterministic benign review cases.

**Base authority:** `main@b8434170ce5f3be7d38e25fff9c2ca50fb1f87fb`

**Design:** `docs/superpowers/specs/2026-09-18-wave10-nonce-randomness-lifecycle-depth-design.md`

## Global constraints

- Preserve 83 canonical skills and 20 packs.
- Preserve all existing 33 operator-depth profiles.
- Keep operator-depth schema version 2.
- Do not change `skill.meta.json`, graph edges, packs, routing domains, benchmark authority, agent-eval authority, superiority-court authority, or workflows.
- Commit the dedicated #34 test before SKILL/runbook/cases/registry production-depth changes.
- Do not weaken #34 after intentional RED.
- Validation remains local/owned/sandboxed/explicitly authorized, deterministic, synthetic, inert/read-only, or bounded reversible.
- After behavioral GREEN, only README and the operator-depth contract may change before exact-head verification.

## Task 1 — Freeze #34 semantics with a dedicated RED test

Create `tests/test_nonce_randomness_lifecycle_depth.py`.

Require canonical SKILL sections:

- `## Causal randomness-lifecycle model`
- `## Value class, property, and security-scope binding`
- `## Generator, seed, entropy, and reseed generations`
- `## Fork, snapshot, restart, and clone lifecycle`
- `## Counter, namespace, reservation, and concurrency binding`
- `## Persistence and crash/restart binding`
- `## Transform, encoding, and truncation binding`
- `## Consumer/construction and bounded consequence binding`
- `## Randomness-lifecycle evidence ladder`
- `## Counterfactual randomness controls`
- `## Alternative explanations`
- `## Evidence ceiling`

Freeze the required distinctions from the design, including duplicate value != vulnerability without same-scope non-repetition requirement, predictability != repetition, RNG API name != actual state provenance, forked process != cloned output stream when diversification exists, counter reset != duplicate consumed value when scope changes, reservation overlap != duplicate consumption, truncation != dangerous collision until final consumer domain is bound, and nonce reuse observation != cryptographic exploitability.

Runbook must include common six headings plus:

- Value/property/security-scope trace
- Generator/seed/entropy/reseed trace
- Fork/snapshot/restart lifecycle trace
- Counter/namespace/reservation trace
- Persistence/crash-restart trace
- Transform/encoding/truncation trace
- Consumer/construction trace
- Counterfactual randomness controls
- Alternative explanations
- Evidence promotion and ceiling

Review matrix must contain at least:

- `fork-cloned-generator-state-reuse`
- `restart-counter-persistence-reset`
- `concurrent-counter-reservation-overlap`
- `truncation-encoding-domain-collapse`

Required fields:

`hypothesis`, `safe_oracle`, `positive_control`, `negative_control`, `stop_condition`, `remediation_oracle`, `value_property_security_scope`, `generator_seed_entropy_reseed`, `fork_snapshot_restart_lifecycle`, `counter_namespace_reservation`, `persistence_crash_restart`, `transform_encoding_truncation`, `consumer_construction_identity`, `effective_randomness_lifecycle_capability`, `bounded_result`, `receipt_result_binding`, `counterfactual_control`, `alternative_explanation`, `evidence_level`, `evidence_ceiling`.

Registry assertions: version 2, exactly 34 profiles, exactly one nonce/randomness entry, standard runbook/matrix paths, `lab_only: true`, common six required headings.

Open a Draft PR at exact test-first SHA and require intentional RED before production implementation.

## Task 2 — Deepen canonical SKILL

Modify `skills/nonce-and-randomness-lifecycle-analysis/SKILL.md`.

Preserve frontmatter/current workflow. Add the causal tuple, value/property/scope binding, generator/seed/reseed generations, fork/restart lifecycle, counter/reservation concurrency, persistence, transform/truncation, final consumer/construction binding, NRL0–NRL5, counterfactuals, alternatives, and evidence ceiling.

Do not absorb cryptographic-protocol consequence, generic concurrency root cause, numeric bounds, or token-authority ownership.

## Task 3 — Add operator runbook

Create `skills/nonce-and-randomness-lifecycle-analysis/references/operator-runbook.md`.

Use synthetic keys, fake entropy sources, deterministic PRNG fixtures, in-memory persistence journals, bounded counter namespaces, mock consumers, and read-only receipts.

## Task 4 — Add deterministic review cases

Create `skills/nonce-and-randomness-lifecycle-analysis/references/operator-review-cases.json`.

Version 1, at least the four required IDs. Every required field >= 40 non-whitespace characters. Safe oracle must name synthetic/mock/inert/read-only/controlled/fake/in-memory. Stop condition must explicitly say stop/abort/do not proceed. Evidence fields use NRL0–NRL5.

## Task 5 — Register profile #34

Modify `operator-depth/profiles.json` with one sorted entry using the standard runbook/matrix paths and common six required sections. Target count 34.

## Task 6 — Repair only proven stale #33 global count assertion

Potentially modify `tests/test_firmware_update_trust_chain_depth.py`.

If and only if behavioral CI shows its exact `len(profiles) == 33` assertion is the remaining extensibility failure, change that global assertion to `>= 33`. Preserve all profile-specific checks.

## Task 7 — Behavioral authority

Require full 9/9 GREEN: six OS/Python validation jobs, benchmark-core, agent-eval-core, superiority-court-core.

## Task 8 — Public docs

Only after behavioral GREEN, update `README.md` and `docs/operator-depth-contract.md` to 34 profiles, identify nonce/randomness lifecycle as #34, summarize causal bindings, and publish NRL0–NRL5.

## Task 9 — Exact-head, guarded merge, closure

Require exact-head 9/9 GREEN, fresh base check, exact 10-path scope, mergeable PR, guarded merge by expected head SHA, verified merge parents, post-merge 9/9 GREEN, merge-tree reads, and final closure comment/readback.

## Success criterion

The merge tree has exactly 34 profiles and one valid nonce/randomness-lifecycle profile; NRL0–NRL5 is published; exact-head and post-merge CI are fully GREEN; no unauthorized authority surface changed.
