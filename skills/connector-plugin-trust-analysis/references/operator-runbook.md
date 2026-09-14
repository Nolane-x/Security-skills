# Connector Plugin Trust Operator Runbook

Use only owned, sandboxed, synthetic, simulated, read-only, or explicitly authorized environments.

## Attack surface

Record integration identity, publisher provenance, version, update source, permission grant, delegated access, schema source, host policy, response identity, lifecycle generations, and each composition boundary between integrations.

## Hypothesis matrix

Turn each concern into one falsifiable expected-versus-observed state claim. Keep provenance, permission, schema, response binding, composition, and lifecycle hypotheses separate. Record the candidate transition, controls, and evidence ceiling for each claim.

## Integration lifecycle and provenance

Trace install source, publisher provenance, update source, runtime metadata, schema source, invocation identity, result identity, and lifecycle generation. Preserve where state is cached, normalized, transformed, or refreshed.

## Effective permission trace

Record initiating principal, host policy, permission grant, delegated scope, service audience, schema-derived state, confirmation state, service-side restriction, and composition boundary. Compare intended permission with observed effective permission at every transition.

## Schema and argument trace

Record declared schema, host-normalized schema, runtime schema, proposed arguments, policy-filtered arguments, remote interpretation, and bounded observed result. Treat schema drift as a state difference until a policy-relevant transition is demonstrated.

## Delegated access and response binding

Bind delegated access to integration identity, service audience, session, invocation identity, and lifecycle generation. Bind response identity to the expected integration and invocation before downstream policy reasoning.

## Cross-connector composition

Preserve provenance across each composition boundary and classify the transferred value before downstream use. Compare the downstream decision with a neighboring control that differs only in the upstream-derived state.

## Lifecycle and revocation trace

Track grant generation, update generation, and revocation generation independently. Define a bounded convergence window before evaluating lifecycle changes so expected propagation delay is not confused with unexpected state.

## Controlled validation

Use synthetic identities, mock services, inert outcomes, and read-only observations. Freeze intended task, versions, policy state, schema state, lifecycle generations, and expected bounded result. Change one variable at a time.

## False-positive controls

Require positive and negative neighboring controls. Record stale metadata, explicitly approved changes, service-side restrictions, display-only schema differences, propagation delay, caching, and model output without policy change as possible alternative explanation categories.

## Counterfactual controls

Hold the harness and intended task constant while changing one candidate variable such as provenance, permission generation, delegated scope, schema version, confirmation state, response identity, upstream provenance, or revocation generation. If the observation persists, downgrade that explanation.

## Evidence capture

Capture integration/version identity, publisher provenance, permission grant, delegated access, schema states, invocation identity, policy decision, response identity, composition trace, lifecycle generations, positive/negative controls, counterfactual outcome, alternative explanation status, and evidence ceiling.

## Evidence promotion and ceiling

Use the canonical C0-C5 ladder. Promote only when the corresponding transition is directly observed with controls. Missing provenance, incomplete response binding, absent counterfactual control, or uncertain lifecycle generation lowers the evidence ceiling.

## Remediation checks

Re-run the same synthetic fixture after remediation. Confirm the unexpected state transition no longer occurs while neighboring intended behavior remains available. Record the fixed revision or configuration and the original fixture identity.
