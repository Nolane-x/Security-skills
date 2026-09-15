# Confused Deputy Operator Runbook

This runbook is for owned/local/sandboxed or explicitly authorized review only. Use synthetic principals, mock/read-only deputies, inert markers, or reversible owner-controlled state. Do not use real credentials, persistence, destructive operations, evasion, malware, or third-party effects.

## Attack surface

Identify every component that can act with more authority than the initiating principal: helpers, brokers, services, signed hosts, plugin hosts, IPC/RPC gateways, background workers, and privileged automation. For each, record the initiating principal, initiating authority, deputy identity, deputy ambient authority, operation classes, target namespaces, and result channels. Treat a privileged runtime identity as a capability ceiling rather than proof of delegated authority.

## Hypothesis matrix

Write one hypothesis per authority transition. Each row states the expected initiating authority, delegation artifact, requested operation/resource, deputy ambient authority, attenuated effective authority, resolved target identity, expected policy decision, safe oracle, negative control, alternative explanation, and evidence ceiling. Prefer hypotheses that can be falsified with one changed synthetic authority dimension.

## Authority-transfer trace

Record the full chain:

`request origin -> authenticated principal -> initiating authority -> delegation artifact -> requested operation -> requested resource -> deputy identity -> deputy ambient authority -> policy decision -> attenuated effective authority -> resolved target identity -> bounded effect -> receipt/result binding`

Do not collapse authentication, delegation, policy, target resolution, accepted effect, or result binding into one trusted state.

## Delegation trace

Treat the delegation artifact as structured authority. Record issuer/authority source, initiating principal, deputy identity, operation scope, resource/target scope, tenant/namespace where relevant, material constraints, delegation generation, issue/expiry/revocation state, downstream-delegation permission, and the attenuation rule for the next hop. Note whether the artifact proves identity, authority, or both.

## Ambient-authority and attenuation trace

List deputy ambient authority independently from the request. Then document how local policy derives attenuated effective authority. The audit question is whether the request receives only the subset justified by initiating authority, delegation constraints, operation/resource binding, and independent service policy. Explicitly look for authority amplification or silent inheritance of the deputy's broader role.

## Operation/resource binding

Bind the policy decision to the tuple of initiating principal, delegation generation, requested operation, relevant material constraints, and the resource identity actually used by policy. When operation or resource changes materially, require a fresh authorization decision rather than reusing connection-level trust.

## Multi-hop authority trace

For each intermediary record:

`incoming principal -> incoming delegated authority -> local policy -> local ambient authority -> outgoing delegated authority -> next-hop target`

Compare adjacent hops for principal substitution, context loss, authority amplification, operation/resource drift, generation drift, and loss of tenant/namespace binding. A runtime identity change is not automatically a defect if the original authority remains correctly attenuated and attributable.

## Target identity binding

Record the policy key and resolved target identity. If authorization happens before resolution, require either demonstrated policy/resolver equivalence or an immutable object/handle binding. Route detailed representation-equivalence questions to `canonicalization-and-namespace-analysis` while preserving the deputy authority tuple here.

## Result and receipt binding

Record result binding using the initiating principal, request/delegation generation, deputy identity, operation, resolved target identity, bounded effect, receipt/result identity, and post-action state observation where relevant. Reject conclusions based only on timing or the fact that the deputy process emitted a result.

## Delegation generation and lifecycle trace

Record delegation generation, issue time, expiry, revocation state, rotation/refresh state, and any policy-cache generation. Determine which generation was evaluated at policy time and which generation remained active when the mock/read-only deputy produced its result. Include retry/asynchronous-delivery state when it can change attribution.

## Controlled validation

Use paired synthetic principals and synthetic resources. Prefer read-only responses, inert markers, deterministic policy harnesses, or reversible owner-controlled state. Exercise one intended path and one neighboring path while recording the same authority-transfer fields. Never broaden the test beyond the authorized fixture just to increase impact.

## False-positive controls

Rule out independent downstream authorization, intentionally global service behavior, stale policy cache, stale delegation generation, fixture contamination, different resolved target identity, retry/duplicate delivery, result-correlation mistakes, and documented background-worker identity substitution. A broad deputy role or successful channel authentication alone is not a finding.

## Counterfactual controls

Change exactly one security-relevant dimension while holding the rest constant: narrower delegation, neighboring operation, neighboring synthetic resource, different delegation generation, or reduced deputy ambient authority. A valid counterfactual identifies the authority transition responsible for the divergence and records any surviving alternative explanation.

## Evidence capture

Capture the authority-transfer trace, delegation artifact summary, delegation generation, policy inputs and decision, deputy ambient authority, attenuated effective authority, resolved target identity, bounded effect, result binding, positive/negative controls, counterfactual, alternative explanation, and remediation oracle. Avoid recording live secret material; use synthetic identifiers and redacted fixture labels.

## Evidence promotion and ceiling

Promote only to the highest directly demonstrated level. D0 is surface only; D1 is authority-context divergence without accepted effect; D2 is deterministic policy/attenuation divergence; D3 is inert mock/read-only deputy acceptance outside intended authority; D4 is a bounded reversible synthetic effect tied to the wrong authority tuple; D5 additionally requires repeatable counterfactual/lifecycle or multi-hop proof plus remediation regression. Always record the evidence ceiling and why it applies.

## Remediation checks

Re-run the same positive, negative, and counterfactual controls after the fix. Verify that effective authority is correctly attenuated, operation/resource and resolved target identity remain bound, invalid delegation generations no longer authorize later use, result binding remains attributable, and legitimate neighboring callers/operations continue to work. A remediation is incomplete if it blocks the test case by breaking unrelated authorized behavior.