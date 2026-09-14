# Wave 10 Connector Trust Depth Design

## Goal
Promote `connector-plugin-trust-analysis` into the Wave 10 second-depth ring as a CI-enforced operator-depth profile using defensive, synthetic, read-only evidence.

## Scope
The profile reasons about integration identity, provenance, permission state, interface/schema consistency, invocation identity, result provenance, cross-connector composition, and lifecycle state.

No routing, graph metadata, packs, benchmark fixtures, thresholds, evaluator authority, or skill metadata change.

## Causal model
Trace each finding through:

`integration identity -> provenance -> permission grant -> delegated scope -> tool/schema contract -> invocation principal -> policy gate -> observable bounded effect -> result provenance -> revocation state`

A finding is not validated from metadata or descriptive text alone. The relevant transition must be shown with bounded synthetic evidence and neighboring controls.

## Effective permission
Record the initiating principal, host policy, explicit permission grant, delegated scope, schema-derived state, confirmation state, service-side restriction, and any composition boundary.

`effective permission` is the permission remaining after the recorded restrictions are applied.

## Provenance continuity
Track provenance across discovery, publisher/source identity, update source, runtime metadata, schema source, invocation identity, and returned result identity. Treat drift as evidence only when it is tied to a policy-relevant transition.

## Interface state
Keep declared schema, normalized schema, review inputs, policy-filtered arguments, and bounded observed result separate so descriptive differences are not overstated.

## Response binding
Bind delegated scope and returned results to integration identity, invocation identity, session, lifecycle generation, and service audience using synthetic records only.

## Cross-connector composition
Preserve provenance when a value from one integration is used by another. Record the composition boundary and compare downstream policy state with a neighboring control.

## Lifecycle
Track grant, update, and revocation generations independently. Define a bounded convergence window so expected propagation delay is distinguished from unexpected state.

## Evidence ladder
- `C0`: metadata or theoretical concern only.
- `C1`: reproducible state mismatch without policy-state change.
- `C2`: deterministic policy or confirmation divergence in a synthetic harness.
- `C3`: inert sandbox behavior differs from intended permission state.
- `C4`: a bounded synthetic result is causally tied to the identified transition.
- `C5`: lifecycle or composition behavior is reproduced with controls and remediation regression proof.

Never report above the highest directly demonstrated level.

## Counterfactual proof
Hold the task and harness fixed while changing one causal variable at a time. If the observation persists, downgrade that explanation.

## Required artifacts
Create:
- `skills/connector-plugin-trust-analysis/references/operator-runbook.md`
- `skills/connector-plugin-trust-analysis/references/operator-review-cases.json`
- `tests/test_connector_plugin_trust_depth.py`

The runbook contains the common operator-depth sections plus lifecycle/provenance, effective-permission, interface-state, response-binding, composition, counterfactual, and evidence-ceiling reasoning.

The machine-readable review-case matrix contains at least three deterministic audit-only records. Each case includes the common operator-depth fields plus provenance, permission profile, schema/argument trace, response binding, composition trace, lifecycle state, counterfactual control, alternative explanation, evidence level, and evidence ceiling. The existing registry field remains named `scenario_matrix`; only the bound filename is profile-specific.

## TDD
The dedicated test is committed before production artifacts. RED must be assertion failures caused by absent depth sections/artifacts/profile registration, never Python/JSON errors. The test freezes semantics rather than line count and uses additive profile registration (`>= 11`).

## Registry and docs
Register the skill as profile 11 without changing registry schema/version. Preserve history: Wave 8 = 8 profiles, prompt injection = 9, RAG/memory = 10, connector/plugin trust = 11.

## Verification
Exact head must pass the six OS/Python matrix jobs plus `benchmark-core`, `agent-eval-core`, and `superiority-court-core`. Changed-file review must confirm no graph, pack, routing, benchmark-authority, evaluator-oracle, or skill-metadata drift.
