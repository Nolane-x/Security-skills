---
name: confused-deputy-analysis
description: "Analyze privileged components that act on behalf of less-privileged callers and may authorize the wrong caller property, delegated capability, or request context. Use for helpers, brokers, services, signed host processes, plugins, IPC/RPC gateways, cloud roles, or privileged automation."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Confused Deputy Analysis

A confused deputy problem exists when a more privileged component applies its authority to a request whose initiating authority, delegation, operation, or target does not justify that effect. Treat the deputy path as an authority-transfer system rather than a trusted-caller checklist.

## When to use

Use when a helper, broker, service, signed host, plugin host, IPC/RPC gateway, cloud role, background worker, or privileged automation acts on behalf of another principal. Route generic subject-action-resource policy questions to `authorization-boundary-analysis`, integration provenance to `connector-plugin-trust-analysis`, confirmation/transaction semantics to `tool-capability-and-confirmation-analysis`, representation-to-object identity questions to `canonicalization-and-namespace-analysis`, and cloud-specific IAM semantics to `cloud-iam-path-analysis`.

## Preconditions

Use only owned/local/sandboxed or explicitly authorized principals and benign effects. Prefer synthetic principals, mock/read-only deputies, inert markers, or reversible owner-controlled state. Do not use real credentials, persistence, destructive operations, evasion, malware, or third-party effects as proof.

## Causal authority-transfer model

Trace the complete chain:

`request origin -> authenticated principal -> initiating authority -> delegation artifact -> requested operation -> requested resource -> deputy identity -> deputy ambient authority -> policy decision -> attenuated effective authority -> resolved target identity -> bounded effect -> receipt/result binding`

Do not infer later authority from an earlier identity check. Authentication, delegation, policy acceptance, target resolution, bounded effect, and result correlation are separate transitions with separate proof obligations.

The default inequality is:

`authenticated principal != delegated authority != deputy ambient authority != attenuated effective authority`

Treat equality as a claim that requires evidence for the exact operation and resource.

## Authority conservation and attenuation

Apply these invariants:

1. Every privileged bounded effect has a traceable initiating principal and request generation.
2. Effective authority is no broader than explicitly delegated authority plus independently justified service policy for the exact operation/resource.
3. Deputy ambient authority is not silently inherited by the initiating caller.
4. Delegation binds operation, resource or target identity, relevant tenant/namespace, material constraints, and lifecycle generation.
5. Multi-hop delegation attenuates monotonically unless a distinct authority boundary explicitly authorizes an expansion.
6. Material operation or target changes trigger a fresh policy decision.
7. Policy identity and resolved target identity are equivalent, or authorization is bound to an immutable object/handle.
8. Receipt, callback, and post-action observation are correlated to the same initiating request and authority tuple.
9. Revocation, expiry, or delegation-generation changes invalidate later use according to the documented lifecycle contract.
10. Remediation preserves legitimate neighboring callers and delegated operations while removing the incorrect authority transfer.

Authority attenuation is the proof obligation that converts the deputy's maximum capability into the subset available for the current request.

## Delegation as structured authority

Model a delegation artifact as a structured authority object, not a boolean trust flag. Record the authority source or issuer, initiating principal, deputy identity, operation class, resource/target scope, tenant or namespace scope when relevant, material constraints, generation/version, issue/expiry/revocation state, whether further delegation is allowed, and the attenuation rule for the next hop.

A process image, signer, connection, bearer token, session, or service identity may authenticate a channel without authorizing the requested privileged operation.

## Multi-hop authority trace

For each brokered hop, record:

`incoming principal -> incoming delegated authority -> local policy -> local ambient authority -> outgoing delegated authority -> next-hop target`

Compare hops for authority amplification, context loss, principal substitution, operation/resource drift, and result misbinding. A background worker may legitimately execute under a different runtime identity; the question is whether the original initiating authority remains correctly bound and attenuated through that transition.

## Deputy ambient authority

List what the deputy can do independent of the request, then derive the request-specific subset separately. Deputy ambient authority is a capability ceiling, not evidence that a caller is authorized to exercise the same set.

Record the mechanism that derives attenuated effective authority from initiating authority, delegation constraints, local policy, operation/resource binding, and target identity.

## Operation and resource binding

Authorization should bind at least:

`initiating principal + delegation generation + requested operation + resolved target identity + relevant tenant/namespace + material request constraints`

If policy executes before target resolution, prove that the policy key is equivalent to the sink's resolved identity or carry an immutable target binding forward. Compose with `canonicalization-and-namespace-analysis` when representation equivalence is material.

## Result and receipt binding

A successful action alone is not enough to attribute the effect to the intended request. Record initiating principal, request/delegation generation, deputy identity, operation, resolved target identity, accepted bounded effect, receipt/result identity, and post-action state observation when relevant.

Result binding means the evidence is correlated to the same request and authority tuple that policy accepted, not merely to the same time window or deputy process.

## Delegation generation and lifecycle

Track delegation generation, issue time, expiry, revocation state, refresh/rotation state, and any cache generation that influences policy. Determine whether a previously valid delegation remains usable after a documented lifecycle transition and whether result/receipt correlation survives retries or asynchronous execution.

A lifecycle claim must identify which generation policy evaluated and which generation the deputy used when producing the bounded result.

## Workflow

1. Identify the deputy, initiating principal, privilege differential, and intended delegated operation.
2. Build the causal authority-transfer trace end to end.
3. Record the structured delegation artifact and its lifecycle generation.
4. Separate deputy ambient authority from the request's attenuated effective authority.
5. Bind operation and resource to the policy decision and resolved target identity.
6. Expand every intermediary into a multi-hop authority trace when applicable.
7. Correlate bounded effect, receipt/result, and post-action observation to the same request generation.
8. Exercise a positive control, a negative control, and at least one single-variable counterfactual in a synthetic environment.
9. Evaluate alternative explanations before promoting evidence.
10. Validate remediation by proving correct attenuation while preserving legitimate neighboring behavior.

## Deputy evidence ladder

- **D0 — surface only:** a privileged deputy, delegation mechanism, or broad role exists, but no security-relevant authority divergence is demonstrated.
- **D1 — authority-context divergence:** synthetic requests produce different principal/delegation/operation/resource context, while policy still rejects the unauthorized path or no accepted bounded effect occurs.
- **D2 — policy or attenuation divergence:** deterministic synthetic policy evaluation authorizes a tuple outside the intended delegation/attenuation contract without relying on a real privileged effect.
- **D3 — inert deputy acceptance:** an owned mock/read-only deputy accepts an operation or resolved target outside the intended effective authority and exposes a deterministic inert marker/result.
- **D4 — bounded synthetic effect:** a reversible or inert owner-controlled state change/read-back proves that the wrong authority tuple caused the deputy to act on the wrong permitted synthetic target or operation.
- **D5 — causal lifecycle proof:** the defect reproduces across counterfactual controls and includes multi-hop, delegation-generation/revocation, or result-binding evidence plus remediation regression proving correct attenuation without breaking legitimate neighboring behavior.

Never report above the highest directly demonstrated level.

## Counterfactual proof

Change exactly one security-relevant authority dimension while holding the rest constant. Useful defensive controls include the same principal with narrower delegation, the same delegation with a different operation, the same operation with a neighboring synthetic resource, the same request with a different delegation generation, or the same deputy path with ambient privilege reduced to the delegated subset.

A counterfactual should identify which authority transition caused the divergence rather than merely showing that a privileged component was present.

## Alternative explanations

Before promoting evidence, consider independent downstream authorization, stale cached policy or delegation generation, a different resolved target identity, fixture contamination between synthetic principals, result/receipt correlation error, retry or duplicate-delivery behavior, background-worker identity substitution by design, and intentionally global service behavior independent of caller authority.

Record the alternative explanation and the control that rejects or preserves it.

## Evidence contract

Record the full authority-transfer chain, the exact intended delegation, deputy ambient authority, policy decision, attenuated effective authority, resolved target identity, bounded synthetic observation, controls, alternative explanations, current evidence level, and evidence ceiling. A writable endpoint, privileged process, broad role, or successful authentication alone is not proof of an authority-transfer defect.

## Evidence ceiling

State both `evidence_level` and `evidence_ceiling`.

- Without an accepted bounded effect, ceiling is D2.
- With inert mock acceptance only, ceiling is D3.
- With a bounded synthetic effect but no lifecycle/counterfactual causal proof, ceiling is D4.
- D5 requires repeatable causal controls and remediation regression evidence.

## Stop conditions

Stop when each operation is re-authorized against attenuated effective authority, target identity is bound consistently, lifecycle generations are respected, and result binding is unambiguous. Also stop when further proof would require real credentials, destructive effects, persistence, third-party systems, or any action outside the authorized synthetic environment.

## Output

```text
request origin:
authenticated principal:
initiating authority:
delegation artifact/generation:
requested operation/resource:
deputy identity:
deputy ambient authority:
policy decision:
attenuated effective authority:
resolved target identity:
bounded effect:
result binding:
counterfactual control:
alternative explanation:
evidence level / ceiling:
remediation regression:
```
