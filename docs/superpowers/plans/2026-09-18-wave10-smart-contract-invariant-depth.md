# Wave 10 Profile #38 — Smart Contract Invariant Depth Implementation Plan

> **For agentic workers:** execute task-by-task and preserve exact test-first lineage.

**Goal:** Promote `smart-contract-invariant-analysis` into the thirty-eighth CI-enforced operator-depth profile with causal SCI0–SCI5 semantics and deterministic benign local-chain review cases.

**Base authority:** `main@aa5d7dfff1d3bdc59b6d90633ede6bc0f747e568`

**Design:** `docs/superpowers/specs/2026-09-18-wave10-smart-contract-invariant-depth-design.md`

## Global constraints

- Preserve 83 canonical skills and 20 packs.
- Preserve all existing 37 operator-depth profiles.
- Keep operator-depth schema version 2.
- Do not change `skill.meta.json`, graph edges, packs, routing domains, benchmark authority, agent-eval authority, superiority-court authority, or workflows.
- Commit the dedicated #38 test before SKILL/runbook/cases/registry production-depth changes.
- Do not weaken #38 after intentional RED.
- Validation remains local/owned/test-chain/explicitly authorized, deterministic, synthetic, inert/read-only, or bounded reversible.
- Use test accounts/assets only; no mainnet transactions, real funds, public protocol manipulation, or live oracle manipulation.
- After behavioral GREEN, only README and operator-depth contract may change before exact-head verification.

## Task 1 — Freeze #38 semantics with a dedicated RED test

Create `tests/test_smart_contract_invariant_depth.py`.

Required SKILL sections:

- `## Causal smart-contract-invariant model`
- `## Protocol, deployment, contract, and state generations`
- `## Invariant identity and domain binding`
- `## Entrypoint, actor, and transition binding`
- `## Asset, accounting, and conservation binding`
- `## External dependency and assumption binding`
- `## Reachability, witness, and bounded consequence binding`
- `## Smart-contract invariant evidence ladder`
- `## Counterfactual invariant controls`
- `## Alternative explanations`
- `## Evidence ceiling`

Freeze distinctions from the design, including suspicious pattern != invariant violation, invariant violation != economic loss, reachable entrypoint != reachable violating state, temporary imbalance != terminal invariant break, event != committed state, callback reachability != invariant violation, and fuzz counterexample != root cause.

Runbook must include common six headings plus:

- Protocol/deployment/state-generation trace
- Invariant/domain/observation-point trace
- Entrypoint/actor/transition trace
- Asset/accounting/conservation trace
- External-dependency/assumption trace
- Reachability/witness/bounded-consequence trace
- Counterfactual invariant controls
- Alternative explanations
- Evidence promotion and ceiling

Review matrix IDs:

- `conservation-ledger-supply-divergence`
- `claim-uniqueness-epoch-generation-reuse`
- `phase-transition-skips-required-accounting-state`
- `solvency-accounting-domain-omits-pending-liability`

Required fields:

`hypothesis`, `safe_oracle`, `positive_control`, `negative_control`, `stop_condition`, `remediation_oracle`, `protocol_deployment_state_generation`, `invariant_domain_observation_point`, `entrypoint_actor_transition_trace`, `asset_accounting_conservation_state`, `external_dependency_assumption_state`, `reachability_violation_witness`, `downstream_protocol_consumer_identity`, `effective_invariant_break_capability`, `bounded_result`, `receipt_result_binding`, `counterfactual_control`, `alternative_explanation`, `evidence_level`, `evidence_ceiling`.

Registry target: version 2, exactly 38 profiles, exactly one smart-contract-invariant entry, standard paths, `lab_only: true`, common six sections.

Open a Draft PR at exact test-first SHA and require intentional RED before production implementation.

## Task 2 — Deepen canonical SKILL

Add the causal tuple, protocol/deployment/state generations, invariant identity/domain/observation point, actor/entrypoint/transition chain, accounting/conservation equations, external assumptions, bounded reachability witness, SCI0–SCI5, counterfactuals, alternatives, and evidence ceiling.

Keep reentrancy causality in profile #39 and upgrade causality in profile #40.

## Task 3 — Add operator runbook

Use local test chains, synthetic accounts/tokens, bounded balances, fake dependencies, deterministic snapshots, property assertions, shadow ledgers, and reversible local state.

## Task 4 — Add deterministic review cases

Create version-1 JSON with the four frozen IDs. All required fields >=40 non-whitespace characters. Safe oracle must name synthetic/mock/inert/read-only/controlled/fake/local/test-chain/shadow. Stop condition explicitly says stop/abort/do not proceed. Evidence fields use SCI0–SCI5.

## Task 5 — Register profile #38

Add one sorted entry to `operator-depth/profiles.json`, target 38.

## Task 6 — Repair only proven stale #37 global count assertion

Potentially modify `tests/test_template_expression_boundary_depth.py` only if CI proves its exact `len(profiles) == 37` assertion is the sole remaining extensibility failure. Change only that global assertion to `>= 37`.

## Task 7 — Behavioral authority

Require full 9/9 GREEN.

## Task 8 — Public docs

Only after behavioral GREEN, publish 38 profiles in README and operator-depth contract, including SCI0–SCI5.

## Task 9 — Exact-head, guarded merge, closure

Require exact-head 9/9 GREEN, fresh base check, exact 10-path scope, mergeable PR, guarded merge by expected head SHA, verified merge parents, post-merge 9/9 GREEN, merge-tree reads, closure comment/readback.

## Success criterion

Merge tree contains exactly 38 profiles and one valid smart-contract-invariant profile; SCI0–SCI5 is published; exact-head and post-merge CI are fully GREEN; no unauthorized authority surface changed.
