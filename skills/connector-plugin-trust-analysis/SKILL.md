---
name: connector-plugin-trust-analysis
description: "Review AI-agent connectors, plugins, and MCP-like integrations for provenance, permission state, schema consistency, delegated access, response identity, update integrity, and cross-connector policy conformance."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Connector Plugin Trust Analysis

Use only owned, sandboxed, synthetic, or explicitly authorized environments.

## When to use

Use when an agent depends on connectors, plugins, remote tools, or app integrations whose identity, permission state, schema, or update state may vary over time.

## Preconditions

1. Record integration identity, publisher/source, version, permission state, delegated scope, schema version, host policy, and response-binding mechanism.
2. Use synthetic test data and non-production accounts.
3. Define expected allowed behavior, neighboring denied behavior, confirmation state, and revocation convergence before observation.

## Integration lifecycle and provenance model

Use this state chain:

```text
integration identity -> provenance -> permission grant -> delegated scope -> tool/schema contract -> invocation principal -> policy gate -> observable bounded effect -> result provenance -> revocation state
```

Compare intended and observed state at each transition. Preserve provenance across install source, publisher identity, update source, runtime metadata, dynamic schema source, invocation identity, and returned result identity.

## Effective permission model

Record initiating principal, host policy, permission grant, `grant generation`, delegated scope, service audience, dynamic schema state, confirmation-bound permission, and any `composition boundary` with another connector.

`effective permission` is the permission remaining after all recorded policy restrictions are applied.

## Schema and argument contract

Track declared schema, host-normalized schema, `dynamic schema`, proposed arguments, policy-filtered arguments, remote interpretation, and observable result. Record `schema drift` only as a state difference until policy relevance is demonstrated.

## Delegated access and response binding

Bind delegated access to integration identity, service audience, subject/session, and lifecycle generation. `response identity` records which integration produced a result, for which invocation, and under which permission/update state.

## Cross-connector composition

Classify information passed from connector A to connector B and preserve its provenance. A `composition boundary` is policy-relevant when the handoff changes B's effective permission or decision state.

## Lifecycle and revocation model

Track `grant generation`, `update generation`, and `revocation generation` independently. Define a `bounded convergence window` so expected propagation delay can be separated from unexpected state.

## Connector evidence ladder

- `C0` — metadata or theoretical concern only.
- `C1` — reproducible state mismatch without policy decision change.
- `C2` — deterministic policy or confirmation divergence in a synthetic harness.
- `C3` — inert sandbox behavior differs from the intended permission state.
- `C4` — a bounded synthetic result is causally tied to the identified transition.
- `C5` — composition, update, or revocation behavior is reproduced with controls and remediation regression proof.

## Counterfactual proof

Hold the task and harness fixed while changing one candidate variable such as provenance, permission generation, delegated scope, schema version, confirmation state, response identity, cross-connector provenance, or revocation generation. If the observation persists, downgrade that explanation.

## Alternative explanations

Consider stale metadata, explicitly approved permission changes, service-side restrictions, schema-display drift, expected propagation delay, duplicate results, cached results, and model output that never changed deterministic policy state.

## Workflow

1. Freeze lifecycle and policy state.
2. Build provenance and effective-permission traces.
3. Establish positive and negative synthetic controls.
4. Compare declared, normalized, and runtime schema states.
5. Bind delegated access and response identity to the invocation.
6. Trace composition boundaries.
7. Run one-variable counterfactual controls.
8. Assign the highest supported C0-C5 level.
9. Re-run controls after remediation.

## Evidence contract

Record integration identity/version, publisher provenance, permission state and generations, delegated scope, schema state, invocation principal, policy decision, bounded result, response identity, composition trace, revocation state, controls, and evidence ceiling.

## Evidence ceiling

State the maximum supported evidence level and why higher levels are not proven. Missing provenance, uncertain response identity, absent counterfactual control, or no bounded observable result lowers the evidence ceiling.

## Stop conditions

Stop before production-account use, real sensitive data, uncontrolled external effects, or activity outside the explicitly authorized synthetic fixture.

## Output

```text
integration/version/publisher:
provenance trace:
grant/update/revocation generations:
effective permission trace:
schema and argument states:
delegated access and response identity:
composition boundaries:
controls and counterfactual:
evidence level / evidence ceiling:
remediation regression:
```

## Operator depth

Use `references/operator-runbook.md` and `references/operator-scenarios.json` for deeper reviewed methodology and deterministic benign scenarios.
