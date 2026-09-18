# Wave 10 Profile #39 — Smart Contract Reentrancy-State Depth Implementation Plan

> **For agentic workers:** execute task-by-task and preserve exact test-first lineage.

**Goal:** Promote `smart-contract-reentrancy-state-analysis` into the thirty-ninth CI-enforced operator-depth profile with causal SCR0–SCR5 semantics and deterministic benign local-chain review cases.

**Base authority:** `main@21bd3afcb6672dbaec58db79574a0a9822f8e8e1`

**Design:** `docs/superpowers/specs/2026-09-19-wave10-smart-contract-reentrancy-depth-design.md`

## Global constraints

- Preserve 83 canonical skills and 20 packs.
- Preserve all existing 38 operator-depth profiles.
- Keep operator-depth schema version 2.
- Do not change `skill.meta.json`, graph edges, packs, routing domains, benchmark authority, agent-eval authority, superiority-court authority, or workflows.
- Commit the dedicated #39 test before SKILL/runbook/cases/registry production-depth changes.
- Do not weaken #39 after intentional RED.
- Validation remains local/owned/test-chain/explicitly authorized, deterministic, synthetic, inert/read-only, bounded depth, and reversible.
- Use synthetic callback contracts/tokens and test assets only; no live protocol attack contracts, real asset movement, public-chain interaction, or gas/resource griefing.
- After behavioral GREEN, only README and operator-depth contract may change before exact-head verification.

## Task 1 — Freeze #39 semantics with a dedicated RED test

Create `tests/test_smart_contract_reentrancy_depth.py`.

Required SKILL sections:

- `## Causal smart-contract-reentrancy model`
- `## Outer transaction, call-frame, and callback generations`
- `## External-call, callback, and reentrant-entry binding`
- `## Transient-state and update-ordering binding`
- `## Lock, guard, and invariant-scope binding`
- `## Cross-function, cross-contract, hook, and read-only lineage`
- `## Outer continuation, commit, and duplicate-effect binding`
- `## Smart-contract reentrancy evidence ladder`
- `## Counterfactual reentrancy controls`
- `## Alternative explanations`
- `## Evidence ceiling`

Freeze distinctions from the design, including external call != reentrancy, callback reachability != harmful reentrancy, lock present != protected invariant, per-function lock != cross-function invariant lock, read-only callback != defect until consumed, and local bounded accounting divergence != real financial loss.

Runbook must include common six headings plus:

- Outer-transaction/call-frame/callback-generation trace
- External-call/callback/reentrant-entry trace
- Transient-state/update-ordering trace
- Lock/guard/invariant-scope trace
- Cross-function/cross-contract/hook/read-only trace
- Outer-continuation/commit/duplicate-effect trace
- Counterfactual reentrancy controls
- Alternative explanations
- Evidence promotion and ceiling

Review matrix IDs:

- `cross-function-callback-consumes-transient-accounting-state`
- `per-function-guard-misses-cross-function-invariant`
- `hook-enabled-token-callback-before-balance-commit`
- `read-only-callback-observer-consumes-transient-share-state`

Required fields:

`hypothesis`, `safe_oracle`, `positive_control`, `negative_control`, `stop_condition`, `remediation_oracle`, `outer_transaction_callback_generation`, `external_call_reentrant_entry_trace`, `transient_state_update_ordering`, `lock_guard_invariant_scope`, `cross_function_contract_hook_lineage`, `outer_continuation_commit_state`, `downstream_protocol_consumer_identity`, `effective_reentrancy_state_capability`, `bounded_result`, `receipt_result_binding`, `counterfactual_control`, `alternative_explanation`, `evidence_level`, `evidence_ceiling`.

Registry target: version 2, exactly 39 profiles, exactly one reentrancy entry, standard paths, `lab_only: true`, common six sections.

Open a Draft PR at exact test-first SHA and require intentional RED before production implementation.

## Task 2 — Deepen canonical SKILL

Add causal tuple, outer/callback frame generations, external-call/reentrant-entry trace, transient-state ordering, lock/guard scope, cross-function/cross-contract/hook/read-only lineage, outer continuation/commit, SCR0–SCR5, counterfactuals, alternatives, and evidence ceiling.

## Task 3 — Add operator runbook

Use local test chains, depth-1 synthetic callbacks, fake hook tokens, bounded test balances, deterministic state snapshots, read-only observers, shadow ledgers, and reversible local markers.

## Task 4 — Add deterministic review cases

Create version-1 JSON with the four frozen IDs. All required fields >=40 non-whitespace characters. Safe oracle must name synthetic/mock/inert/read-only/controlled/fake/local/test-chain/shadow. Stop condition explicitly says stop/abort/do not proceed. Evidence fields use SCR0–SCR5.

## Task 5 — Register profile #39

Add one sorted entry to `operator-depth/profiles.json`, target 39.

## Task 6 — Repair only proven stale #38 global count assertion

Potentially modify `tests/test_smart_contract_invariant_depth.py` only if CI proves its exact `len(profiles) == 38` assertion is the sole remaining extensibility failure. Change only that global assertion to `>= 38`.

## Task 7 — Behavioral authority

Require full 9/9 GREEN.

## Task 8 — Public docs

Only after behavioral GREEN, publish 39 profiles in README and operator-depth contract, including SCR0–SCR5.

## Task 9 — Exact-head, guarded merge, closure

Require exact-head 9/9 GREEN, fresh base check, exact 10-path scope, mergeable PR, guarded merge by expected head SHA, verified merge parents, post-merge 9/9 GREEN, merge-tree reads, closure comment/readback.

## Success criterion

Merge tree contains exactly 39 profiles and one valid reentrancy profile; SCR0–SCR5 is published; exact-head and post-merge CI are fully GREEN; no unauthorized authority surface changed.
