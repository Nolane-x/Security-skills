# Wave 10 Profile #29 — Protocol State Machine Depth Implementation Plan

> **For agentic workers:** execute task-by-task and preserve exact test-first lineage.

**Goal:** Promote `protocol-state-machine-analysis` into the twenty-ninth CI-enforced operator-depth profile with causal PST0–PST5 semantics and deterministic benign review cases.

**Base authority:** `main@d2d9275b4bcc2ebb2f1a7db7730f4c576ebdf540`

**Design:** `docs/superpowers/specs/2026-09-18-wave10-protocol-state-machine-depth-design.md`

## Global constraints

- Preserve 83 canonical skills and 20 packs.
- Preserve all existing 28 operator-depth profiles.
- Keep operator-depth schema version 2.
- Do not change `skill.meta.json`, graph edges, packs, routing domains, benchmark authority, agent-eval authority, superiority-court authority, or workflows.
- Commit the dedicated #29 test before SKILL/runbook/cases/registry production-depth changes.
- Do not weaken #29 after intentional RED.
- Validation remains local/owned/sandboxed/explicitly authorized, deterministic, synthetic, inert/read-only, or bounded reversible.
- After behavioral GREEN, only README and the operator-depth contract may change before exact-head verification.

## Task 1 — Freeze #29 semantics with a dedicated RED test

Create `tests/test_protocol_state_machine_depth.py`.

Require canonical SKILL sections:

- `## Causal protocol-state model`
- `## Peer, connection, session, and role generations`
- `## Transition guard and authenticated-context binding`
- `## Replay, retry, idempotency, and duplicate-effect binding`
- `## Timeout, cancellation, reset, reconnect, and late-completion binding`
- `## Commit, terminal-state, and downstream-action binding`
- `## Protocol-state evidence ladder`
- `## Counterfactual protocol controls`
- `## Alternative explanations`
- `## Evidence ceiling`

Freeze the required distinctions from the design, including syntactically valid message != legal state transition, retry != idempotent replay, acknowledgment != commit, timeout != rollback, reset != state revocation, reconnect != same session, and stale background completion != current operation.

Runbook must include the common six headings plus:

- Peer/session/role-generation trace
- Transition-guard and authenticated-context trace
- Replay/retry/idempotency trace
- Timeout/cancellation/reset/reconnect trace
- Commit/terminal-state/downstream-action trace
- Counterfactual protocol controls
- Alternative explanations
- Evidence promotion and ceiling

Review matrix must contain at least:

- `stale-session-replay-after-reconnect`
- `retry-duplicate-commit`
- `role-change-stale-authority`
- `timeout-late-completion-cross-generation`

Required fields:

`hypothesis`, `safe_oracle`, `positive_control`, `negative_control`, `stop_condition`, `remediation_oracle`, `peer_session_role_generation`, `transition_guard_authenticated_context`, `replay_retry_idempotency_state`, `timeout_cancel_reset_reconnect_state`, `commit_terminal_downstream_action`, `downstream_consumer_identity`, `effective_protocol_capability`, `bounded_result`, `receipt_result_binding`, `counterfactual_control`, `alternative_explanation`, `evidence_level`, `evidence_ceiling`.

Registry assertions: version 2, exactly 29 profiles, exactly one protocol-state entry, standard runbook/matrix paths, `lab_only: true`, common six required headings.

Open a Draft PR at exact test-first SHA and require intentional RED before production implementation.

## Task 2 — Deepen canonical SKILL

Modify `skills/protocol-state-machine-analysis/SKILL.md`.

Preserve frontmatter and current workflow. Add the causal tuple from the design, peer/session/connection/role/stream/transaction generations, transition guard binding, replay/retry/idempotency, timeout/cancel/reset/reconnect/late-completion state, commit/terminal/action separation, PST0–PST5, counterfactuals, alternatives, and evidence ceiling.

Do not absorb authorization, concurrency-race, cryptographic-protocol, or stateful-fuzzing ownership.

## Task 3 — Add operator runbook

Create `skills/protocol-state-machine-analysis/references/operator-runbook.md`.

Use synthetic peers, loopback/mock protocol endpoints, fake transaction ledgers, inert/read-only consumers, deterministic state traces, and bounded reversible markers.

## Task 4 — Add deterministic review cases

Create `skills/protocol-state-machine-analysis/references/operator-review-cases.json`.

Version 1, at least the four required IDs. Every required field >= 40 non-whitespace characters. Safe oracle must name synthetic/mock/inert/read-only/controlled. Stop condition must explicitly say stop/abort/do not proceed. Evidence fields use PST0–PST5.

## Task 5 — Register profile #29

Modify `operator-depth/profiles.json` with one sorted entry using the standard runbook/matrix paths and common six required sections. Target count 29.

## Task 6 — Repair only proven stale #28 global count assertion

Potentially modify `tests/test_parser_state_machine_depth.py`.

If and only if behavioral CI shows its exact `len(profiles) == 28` assertion is the remaining extensibility failure, change that global assertion to `>= 28`. Preserve all profile-specific checks.

## Task 7 — Behavioral authority

Require full 9/9 GREEN: six OS/Python validation jobs, benchmark-core, agent-eval-core, superiority-court-core.

## Task 8 — Public docs

Only after behavioral GREEN, update `README.md` and `docs/operator-depth-contract.md` to 29 profiles, identify protocol-state-machine as #29, summarize causal bindings, and publish PST0–PST5.

## Task 9 — Exact-head, guarded merge, closure

Require exact-head 9/9 GREEN, fresh base check, exact 10-path scope, mergeable PR, guarded merge by expected head SHA, verified merge parents, post-merge 9/9 GREEN, merge-tree reads, and final closure comment.

## Success criterion

The merge tree has exactly 29 profiles and one valid protocol-state-machine profile; PST0–PST5 is published; exact-head and post-merge CI are fully GREEN; no unauthorized authority surface changed.
