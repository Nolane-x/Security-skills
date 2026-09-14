# Wave 10 Tool Capability And Confirmation Depth Design

## Goal
Promote `tool-capability-and-confirmation-analysis` into the Wave 10 second-depth ring as the twelfth CI-enforced operator-depth profile. The profile remains defensive, authorized-only, and based on mock tools, synthetic identities, reversible fixtures, inert actions, and read-only observations.

The new depth is not a larger checklist of risky actions. It is a causal model for proving whether a tool action remained bound to the user's intended request, effective authority, confirmation snapshot, execution state, and post-action receipt.

## Scope
Deepen the existing canonical skill, add a reviewed operator runbook, add a deterministic machine-readable audit matrix, add a dedicated depth contract test, register the profile, and synchronize operator-depth documentation and README status.

Do not change `skill.meta.json`, skill graph edges, packs, routing domains, benchmark fixtures or thresholds, agent-eval authority, or superiority-court authority.

## Boundary with connector/plugin trust
`connector-plugin-trust-analysis` owns integration identity, publisher/install/update provenance, connector permissions, delegated connector scope, dynamic schema provenance, connector response identity, and connector lifecycle/revocation.

`tool-capability-and-confirmation-analysis` owns the action-level contract after a tool capability is available to the agent: request intent, proposed capability, normalized arguments, effective authority, policy decision, confirmation content, execution binding, observable effect, receipt/state, retry/idempotency, and rollback semantics.

This separation prevents duplicate canonical capabilities while allowing the two skills to compose.

## Action-binding causal model
Every candidate finding should be traced through:

`request intent -> capability proposal -> normalized arguments -> effective authority -> policy decision -> confirmation snapshot -> execution binding -> observable bounded effect -> receipt/state -> retry/rollback state`

A claim is not validated from tool availability, schema text, model prose, or confirmation UI alone. The exact state transition where the intended contract and observed effective contract diverge must be demonstrated in a controlled fixture.

## Intent and capability model
Record the initiating principal, requested task, allowed side-effect class, proposed tool/capability, and whether the proposal is read-only, draft/propose, create, modify, execute, external-send, delete, or privilege-changing.

Distinguish:
- requested intent from model/tool proposal;
- declared capability from effective capability after policy and credential limits;
- read capability from write/effect capability;
- one-step authority from authority created by a chained plan.

A broad tool being installed is not itself a finding. Evidence requires a mismatch between intended authority and the effective action path.

## Argument normalization and binding
Track arguments through these states:
- user-visible request arguments;
- model-proposed arguments;
- host-normalized arguments;
- policy-filtered arguments;
- confirmation-bound arguments;
- execution-time arguments;
- receipt-observed target/effect.

The profile should detect contract drift without teaching consent bypass. Safe review cases use synthetic targets and inert effects to determine whether the same tuple remains bound across stages.

## Effective authority model
Effective authority is the bounded action capability that remains after principal identity, credential scope, host policy, allowlists, capability class, argument constraints, confirmation state, transaction policy, and service-side restrictions are applied.

Record both the nominal tool capability and the effective authority at the decision point. Do not infer effect authority from schema exposure alone.

## Confirmation tuple
Confirmation must be modeled as a snapshot over the materially relevant tuple, not merely as a boolean `confirmed` state.

At minimum, record:
- principal/session;
- tool/capability;
- target/resource;
- effect class;
- salient arguments such as recipient, path, resource identifier, quantity, or irreversible flag when applicable;
- policy/credential generation;
- confirmation generation or nonce when available;
- expiry or mutation boundary.

If a material field changes after confirmation, the old confirmation must not be treated as proof of consent for the new tuple.

## Execution binding and state drift
Compare the confirmation snapshot against the execution-time tuple. Test only controlled fixtures for stale state, policy generation changes, target substitutions, normalized-argument changes, or chained-plan transitions.

Use a time-of-check/time-of-use lens defensively: identify whether policy, target, capability, or arguments changed between decision/confirmation and the inert execution boundary. Do not provide instructions for bypassing real confirmation systems.

## Transaction, retry, and idempotency model
Record transaction identity, action generation, retry attempt, idempotency key or equivalent, observable receipt, rollback/compensation state, and final state.

A timeout or duplicate proposal is not evidence of duplicate effect. Promote only when the fixture can distinguish proposal, accepted execution, receipt, and final state.

## Post-action verification
Require observable receipts or read-back state for effect claims. Model:

`proposal != accepted execution != receipt != durable final state`

A success string from the model or tool wrapper is insufficient when the backing state can be checked safely.

## Tool evidence ladder
Use levels `T0` through `T5`:

- `T0`: tool/capability/schema is present or broadly described; no protected decision divergence.
- `T1`: proposal, normalization, or confirmation tuple differs from the request, but policy rejects it or no bounded effect is accepted.
- `T2`: deterministic policy/confirmation decision diverges from the intended action contract in a synthetic harness.
- `T3`: an inert mock action is accepted outside the intended effective authority or confirmation tuple.
- `T4`: a bounded synthetic effect or state change is observed and bound to the wrong action tuple.
- `T5`: the causal defect is repeatable across controls and includes durable post-action, retry/idempotency, or rollback-state proof plus regression evidence.

Never report above the highest directly demonstrated level.

## Counterfactual proof
Keep the harness and intended task fixed while changing one causal variable at a time: principal, capability class, argument tuple, policy generation, confirmation generation, target, retry identity, or final-state read-back. If the effect persists after the suspected variable is restored, downgrade or reject that explanation.

## Alternative explanations
Explicitly consider benign causes such as stale UI text with correct execution binding, harmless normalization, asynchronous receipt delay, duplicate proposal without duplicate effect, mock-service artifact, expected idempotent replay, intentionally broad but policy-constrained schema, or bounded convergence after rollback.

## Evidence ceiling
The report must state the maximum defensible evidence level and why it cannot be promoted further. A mismatch in text or proposal cannot be reported as an executed effect. An accepted mock call cannot be reported as durable state without a receipt/read-back oracle.

## Required artifacts
Create:
- `skills/tool-capability-and-confirmation-analysis/references/operator-runbook.md`
- `skills/tool-capability-and-confirmation-analysis/references/operator-review-cases.json`
- `tests/test_tool_capability_confirmation_depth.py`

The runbook must include the common operator-depth sections plus intent/capability binding, argument normalization, effective authority, confirmation tuple, execution binding, transaction/retry/idempotency, post-action verification, counterfactual controls, and evidence promotion/ceiling.

The review-case matrix must contain at least three deterministic benign cases covering:
1. request-to-confirmation argument binding;
2. read/propose versus write/effect authority and chained-plan boundaries;
3. transaction retry/idempotency plus receipt/final-state verification.

Each case must include causal traces, controls, alternative explanations, stop conditions, remediation oracles, evidence level, and evidence ceiling.

## TDD contract
Commit the dedicated depth test before production artifacts. The RED state must be assertion failures caused by absent depth sections, runbook, review cases, and twelfth-profile registration. Missing files must be checked before reads so RED contains failures rather than file-not-found errors.

Use additive registry checks (`>= 12`) rather than an exact global count. The central operator-depth validator remains authoritative for registry schema, uniqueness, path validity, safety language, and common matrix fields.

## Registry and docs
Register the skill as profile 12 in `operator-depth/profiles.json` without changing registry schema/version. Keep `scenario_matrix` as the stable registry field and bind it to `references/operator-review-cases.json`.

Update `docs/operator-depth-contract.md` and `README.md` only after behavioral GREEN. Preserve history: Wave 8 = eight profiles; prompt injection = 9; RAG/memory = 10; connector/plugin trust = 11; tool capability/confirmation = 12.

## Verification
Before integration, the exact PR head must pass:
- Ubuntu, macOS, and Windows on Python 3.11 and 3.13;
- canonical skill validation;
- operator-depth validation with 12 profiles;
- graph/index checks;
- benchmark validation and portability;
- full tests;
- `benchmark-core` double-run byte-identical check;
- `agent-eval-core` deterministic tasks/evaluations/matrix including cautious/faulty controls;
- `superiority-court-core` deterministic contestant views/tasks/scores/court.

Changed-file review must confirm no drift in skill metadata, graph edges, packs, routing, benchmark authority, evaluator authority, or superiority-court authority.