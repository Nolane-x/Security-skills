# Wave 10 Profile #40 — Smart Contract Upgradeability Depth Implementation Plan

> **For agentic workers:** execute task-by-task and preserve exact test-first lineage.

**Goal:** Promote `smart-contract-upgradeability-analysis` into the fortieth and final planned CI-enforced operator-depth profile with causal SCU0–SCU5 semantics and deterministic benign local-upgrade review cases.

**Base authority:** `main@004cd6299e8c76904f2634625af2213492488482`

**Design:** `docs/superpowers/specs/2026-09-19-wave10-smart-contract-upgradeability-depth-design.md`

## Global constraints

- Preserve 83 canonical skills and 20 packs.
- Preserve all existing 39 operator-depth profiles.
- Keep operator-depth schema version 2.
- Do not change `skill.meta.json`, graph edges, packs, routing domains, benchmark authority, agent-eval authority, superiority-court authority, or workflows.
- Commit the dedicated #40 test before SKILL/runbook/cases/registry production-depth changes.
- Do not weaken #40 after intentional RED.
- Validation remains local/owned/test-chain/explicitly authorized, deterministic, synthetic, inert/read-only, or bounded reversible.
- Use synthetic admin/user accounts, local proxies/implementations, fake governance/timelocks, bounded state, read-only snapshots, and reversible upgrades only.
- After behavioral GREEN, only README and operator-depth contract may change before exact-head verification.
- After #40 closure, Wave 10 enters closure/audit mode; no automatic profile expansion.

## Task 1 — Freeze #40 semantics with a dedicated RED test

Create `tests/test_smart_contract_upgradeability_depth.py`.

Required SKILL sections:

- `## Causal smart-contract-upgradeability model`
- `## Proxy, implementation, governance, and lifecycle generations`
- `## Upgrade authorization and commit binding`
- `## Storage-layout and state-interpretation binding`
- `## Initializer, reinitializer, and migration binding`
- `## Selector, fallback, beacon, and facet routing binding`
- `## Upgrade invariant and bounded consequence binding`
- `## Smart-contract upgradeability evidence ladder`
- `## Counterfactual upgradeability controls`
- `## Alternative explanations`
- `## Evidence ceiling`

Freeze distinctions from the design, including upgradeability != vulnerability, implementation deployed != proxy upgraded, storage-layout diff != storage corruption, initializer exists != initialization flaw, selector collision != reachable unintended function, rollback possible != rollback unsafe, and upgrade event != committed implementation change.

Runbook must include common six headings plus:

- Proxy/implementation/governance-generation trace
- Upgrade-authorization/commit trace
- Storage-layout/state-interpretation trace
- Initializer/reinitializer/migration trace
- Selector/fallback/beacon/facet trace
- Upgrade-invariant/bounded-consequence trace
- Counterfactual upgradeability controls
- Alternative explanations
- Evidence promotion and ceiling

Review matrix IDs:

- `storage-layout-slot-reinterpreted-after-upgrade`
- `reinitializer-version-replayed-after-upgrade`
- `selector-routing-generation-targets-unintended-facet`
- `rollback-restores-code-but-not-migrated-state-generation`

Required fields:

`hypothesis`, `safe_oracle`, `positive_control`, `negative_control`, `stop_condition`, `remediation_oracle`, `proxy_implementation_governance_generation`, `upgrade_authorization_commit_trace`, `storage_layout_state_interpretation`, `initializer_reinitializer_migration_state`, `selector_fallback_beacon_facet_state`, `upgrade_invariant_bounded_consequence`, `downstream_proxy_consumer_identity`, `effective_upgradeability_capability`, `bounded_result`, `receipt_result_binding`, `counterfactual_control`, `alternative_explanation`, `evidence_level`, `evidence_ceiling`.

Registry target: version 2, exactly 40 profiles, exactly one smart-contract-upgradeability entry, standard paths, `lab_only: true`, common six sections.

Open a Draft PR at exact test-first SHA and require intentional RED before production implementation.

## Task 2 — Deepen canonical SKILL

Add the causal tuple, proxy/implementation/governance lifecycle generations, upgrade commit, storage-layout interpretation, initializer/reinitializer/migration state, selector/fallback/beacon/facet routing, upgrade invariant consequence, SCU0–SCU5, counterfactuals, alternatives, and evidence ceiling.

Keep general invariant ownership in profile #38 and reentrancy ordering in profile #39.

## Task 3 — Add operator runbook

Use local deployments, synthetic admin/user accounts, local implementation pairs, fake governance/timelocks, inert selectors, bounded storage markers, deterministic snapshots, and reversible upgrade/downgrade transitions.

## Task 4 — Add deterministic review cases

Create version-1 JSON with the four frozen IDs. All required fields >=40 non-whitespace characters. Safe oracle must name synthetic/mock/inert/read-only/controlled/fake/local/test-chain/shadow. Stop condition explicitly says stop/abort/do not proceed. Evidence fields use SCU0–SCU5.

## Task 5 — Register profile #40

Add one sorted entry to `operator-depth/profiles.json`, target 40.

## Task 6 — Repair only proven stale #39 global count assertion

Potentially modify `tests/test_smart_contract_reentrancy_depth.py` only if CI proves its exact `len(profiles) == 39` assertion is the sole remaining extensibility failure. Change only that global assertion to `>= 39`.

## Task 7 — Behavioral authority

Require full 9/9 GREEN.

## Task 8 — Public docs

Only after behavioral GREEN, publish 40 profiles in README and operator-depth contract, including SCU0–SCU5.

## Task 9 — Exact-head, guarded merge, closure

Require exact-head 9/9 GREEN, fresh base check, exact 10-path scope, mergeable PR, guarded merge by expected head SHA, verified merge parents, post-merge 9/9 GREEN, merge-tree reads, closure comment/readback.

## Task 10 — Enter closure-only phase

After #40 is CLOSED:
- freeze operator-depth target at 40 unless audit proves a distinct uncovered causal domain;
- perform operator-depth overlap/duplication audit;
- map all 83 canonical skills to causal profiles or explicitly justified workflow/support roles;
- validate graph/packs/routing and evidence-ladder consistency;
- validate deterministic matrices, cross-agent evaluation, and superiority court;
- complete repository license;
- rewrite README professionally and synchronize README-VN/README-CN.

## Success criterion

Merge tree contains exactly 40 profiles and one valid smart-contract-upgradeability profile; SCU0–SCU5 is published; exact-head and post-merge CI are fully GREEN; no unauthorized authority surface changed; Wave 10 then moves to closure-only work.
