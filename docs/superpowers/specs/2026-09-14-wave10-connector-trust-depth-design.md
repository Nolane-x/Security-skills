# Wave 10 Connector Trust Depth Design

## Goal
Promote `connector-plugin-trust-analysis` into the Wave 10 second-depth ring as a CI-enforced operator-depth profile. The profile remains defensive, authorized-only, and based on synthetic identities, mock services, inert actions, and read-only observations.

## Scope
The canonical skill must reason about connector identity, install/update provenance, granted permissions, delegated credential scope, dynamic tool/schema contracts, invocation identity, deterministic policy/confirmation, callback/result provenance, cross-connector data flow, and revocation/update state.

No routing, graph metadata, packs, benchmark fixtures, thresholds, evaluator authority, or skill metadata will change.

## Causal model
Every candidate finding should be traced through:

`integration identity -> provenance -> permission grant -> delegated scope -> tool/schema contract -> invocation principal -> argument authority -> policy/confirmation -> bounded remote effect -> callback/result provenance -> cross-connector propagation -> revocation/update state`

A finding is not validated from broad capability, model prose, or schema text alone. The exact transition where intended policy and observed effective policy diverge must be demonstrated in a controlled fixture.

## Effective authority
Record initiating-principal authority, host/orchestrator policy, explicit connector grant, delegated credential scope/audience, remote capability, dynamic schema-derived capability, confirmation-bound authority, callback/result influence, and any compound authority created by composition.

`effective authority` means the capability that remains after deterministic policy, grant, scope, schema, confirmation, and service-side constraints are applied.

## Provenance continuity
Track provenance across discovery, installation, publisher identity, update channel, runtime metadata, dynamic schema discovery, callback origin, and tool results. Treat schema, publisher, permission, callback, or update drift as evidence only when the drift is tied to a policy-relevant state transition.

## Schema and argument contract
Separate declared schema, host-normalized schema, model proposal, policy-filtered/confirmed arguments, remote interpretation, and observed bounded effect. This prevents a suspicious description from being overstated as a policy failure.

## Credential and callback binding
Bind delegated scope/audience, subject or tenant, connector identity, session/request identity, callback/result identity, and revocation generation. Use only fake credentials, sandbox identities, and inert callback sinks.

## Cross-connector composition
Treat output from connector A as typed data with provenance before it can influence connector B. Record whether it is data, instruction-like content, proposed arguments, or policy-relevant state. Validate only bounded synthetic policy divergence.

## Lifecycle and revocation
Track grant generation, update generation, and revocation generation. Define an expected convergence window so delayed propagation can be distinguished from an actual post-revocation policy failure.

## Evidence ladder
- `C0`: suspicious metadata, schema text, or theoretical capability.
- `C1`: reproducible proposal/schema/permission divergence without accepted bounded action.
- `C2`: deterministic policy or confirmation decision diverges in a synthetic harness.
- `C3`: inert sandbox capability is accepted outside the intended grant.
- `C4`: bounded synthetic boundary effect is observed and causally tied to the transition.
- `C5`: composition, update, or revocation consequence is reproduced with controls and regression proof.

Never report above the highest directly demonstrated level.

## Counterfactual proof
Keep the harness and intended task fixed while changing one causal variable at a time: provenance, permission generation, delegated scope, schema version, confirmation binding, callback identity, cross-connector provenance, or revocation generation. If the effect persists, downgrade or reject that explanation.

## Required artifacts
Create:
- `skills/connector-plugin-trust-analysis/references/operator-runbook.md`
- `skills/connector-plugin-trust-analysis/references/operator-scenarios.json`
- `tests/test_connector_plugin_trust_depth.py`

The runbook must include the common operator-depth sections plus lifecycle/provenance, effective authority, schema/argument, credential/callback, cross-connector, revocation, counterfactual, and evidence-ceiling reasoning.

The scenario matrix must contain at least three benign deterministic fixtures covering: schema/permission drift; delegated-scope plus callback binding; and cross-connector composition plus revocation. Each scenario must include causal traces, controls, alternative explanations, stop conditions, and evidence ceilings.

## TDD
The dedicated test is committed before production artifacts. RED must be assertion failures caused by absent depth sections/artifacts/profile registration, never Python/JSON errors. The test freezes semantics rather than line count and uses additive profile registration (`>= 11`) instead of a global exact-count invariant.

## Registry and docs
Register the skill as profile 11 in `operator-depth/profiles.json` without changing registry schema/version. Update `docs/operator-depth-contract.md` and `README.md` only after behavioral GREEN. Preserve history: Wave 8 = 8 profiles, prompt injection = 9, RAG/memory = 10.

## Verification
Exact head must pass the six OS/Python matrix jobs plus `benchmark-core`, `agent-eval-core`, and `superiority-court-core`. Changed-file review must confirm no graph, pack, routing, benchmark-authority, evaluator-oracle, or skill-metadata drift.
