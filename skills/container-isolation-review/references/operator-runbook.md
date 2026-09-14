# Container Isolation Operator Runbook

Use this runbook only for owned clusters, isolated labs, benchmark fixtures, or explicitly authorized deployments. Prefer read-only inspection, synthetic workloads, mock services, and disposable namespaces. The goal is to verify that effective workload boundaries match the reviewed deployment policy.

## Attack surface

Model the boundary as the composition of workload identity, namespace placement, runtime class, filesystem exposure, process/network isolation, security profiles, device access, admission policy, controller templates, node integration, and cluster authorization.

For every reviewed workload record both the declared configuration and the effective runtime state. Also record which component can mutate or override each field: user manifest, controller, admission layer, runtime default, or node policy.

## Hypothesis matrix

Turn broad concerns into falsifiable policy hypotheses. Representative classes include namespace isolation, storage exposure, workload identity scope, admission consistency, controller-template consistency, network policy, device assignment, and node-local integration.

Each hypothesis must state the expected boundary first and use only a synthetic or read-only signal. A configuration that is intentionally broad is reported as exposure unless a separate reviewed invariant is violated.

## Controlled validation

1. Pin cluster, node, runtime, admission, and policy revisions.
2. Create a disposable namespace and synthetic test identity.
3. Capture the expected boundary for the exact workload class before testing.
4. Use a minimal synthetic workload with no unrelated application logic.
5. Record effective identity, namespace, storage, security-profile, device, and network state.
6. Exercise one boundary at a time with synthetic markers, mock services, policy simulation, or read-only resources.
7. Compare requested configuration with admitted configuration and effective runtime state.
8. Repeat with one neighboring allowed configuration and one neighboring denied configuration.
9. When a controller is involved, compare controller-generated state with the equivalent direct test workload.
10. Promote evidence only when the pinned environment reproduces the unexpected boundary and the controls rule out fixture/configuration error.

## False-positive controls

Use paired controls such as intended versus neighboring identity, allowed versus denied mock service, declared versus effective configuration, direct versus controller-generated workload, and policy-enabled versus documented exception path.

Reject or downgrade a case when the behavior is fully explained by reviewed configuration, stale test state, an explicitly documented exception, or a synthetic fixture that accidentally grants broader access.

## Evidence capture

Preserve a compact evidence ledger:

```text
cluster_revision:
node_runtime_revision:
workload_identity:
namespace_runtime_class:
requested_configuration:
effective_configuration:
storage_and_device_state:
security_profile_state:
admission_decision:
network_policy:
hypothesis:
synthetic_or_mock_signal:
positive_control:
negative_control:
configuration_vs_defect:
evidence_state:
```

Evidence must identify the exact intended boundary and the effective state that contradicted it. A scanner label or configuration keyword alone is not sufficient.

## Remediation checks

Prefer the smallest change that restores the intended boundary: narrow identity scope, remove unnecessary exceptions, align controller templates with admission policy, reduce broad storage/device exposure, constrain network reach, and make runtime defaults explicit.

Regression verification must replay the original synthetic case plus neighboring allowed and denied controls. A remediation is not successful if it simply prevents every test workload from functioning.
