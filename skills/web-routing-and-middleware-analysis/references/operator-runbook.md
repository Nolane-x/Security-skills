# Web Routing And Middleware Operator Runbook

Use this runbook only with source code, configuration, and a local/staging/sandboxed or explicitly authorized test harness. Use synthetic principals, inert handlers, recorded fixtures, and test-only state. The goal is to prove or falsify request-policy invariants without production probing or business side effects.

## Request-policy invariant semantics

Start by declaring a **semantic-equivalence class**: request forms that the reviewed application contract says represent the same protected resource/action under the same relevant principal, tenant, and trusted-topology assumptions. Similar-looking strings are not enough.

For each class, write an invariant:

```text
equivalent request states must receive equivalent required policy treatment
before the same security-relevant dispatch boundary.
```

Keep an intentionally distinct neighboring class as a negative control. A strong review proves both that equivalent states remain policy-equivalent and that intentionally distinct states remain distinct.

## Hopwise interpretation model

Represent the request as a sequence of interpretation snapshots:

```text
raw input
  -> edge/proxy interpretation
  -> normalization
  -> rewrite provenance / mount provenance
  -> route candidate and match
  -> middleware partial order
  -> identity binding / tenant binding
  -> policy attachment and decision
  -> handler reachability
  -> bounded downstream dispatch
```

Each **interpretation snapshot** records the representation consumed by that component: path, method, host, trusted forwarding context, route scope, principal/tenant state, and the component that produced the next state.

Preserve before/after values and provenance for every transformation. Do not infer earlier state from the final route or handler.

## Policy attachment and identity timing

For every reviewed control, record the exact **policy attachment point** and the state it consumes. Authentication, authorization, tenant restriction, CSRF/origin, content-type, or another policy may attach at different points in the request lifecycle.

Record **identity binding** and **tenant binding** as explicit state transitions. A principal being visible at the final handler does not prove it governed an earlier route decision; conversely, late binding is not automatically incorrect unless the reviewed invariant requires earlier identity context.

Record the **middleware partial order**, not only middleware names. For each relevant component, document which request state it consumes and whether later routing or dispatch changes the object/action to which its decision applies.

## Method, host, and proxy trust semantics

Treat **method semantics**, **host semantics**, and **proxy trust** as explicit reviewed state. Determine from source/configuration which component is authoritative and which forwarded metadata is trusted by design. Do not assume a field is trusted merely because it is present.

Validation should rely on static configuration review and synthetic fixtures that model the declared topology, not on sending spoofed infrastructure metadata to live systems.

## Fallback, error, and downstream routing

Model each **fallback route** and **error route** as a separate state transition with its own policy context. Distinguish framework error handling, application fallback, proxy fallback, and downstream dispatch in the reasoning model.

A different fallback or error handler is not a finding by itself. The reviewed invariant must also change for requests that are intended to be equivalent.

## Attack surface

Map every component that can reinterpret or reclassify a request: proxy configuration, framework normalization, rewrite/mount rules, router, middleware stack, identity/tenant binding, controller, fallback/error handling, and downstream dispatch.

For each component record its revision, input state, output state, transformation provenance, policy position, and whether the transition can change handler reachability. The attack surface is the set of interpretation and policy transitions, not merely the route table.

## Hypothesis matrix

Create falsifiable hypotheses for:

- semantic-equivalent representations receiving different policy treatment;
- rewrite provenance or mount provenance changing the governed object after a policy decision;
- middleware partial order differing inside one reviewed policy class;
- identity binding or tenant binding occurring after a decision that requires that context;
- method semantics or host semantics being interpreted inconsistently;
- proxy trust assumptions differing between reviewed components;
- fallback route or error route changing policy attachment;
- apparent route selection that is not actually handler-reachable;
- downstream dispatch changing the governed object/action.

Each row should state the expected invariant, suspected transition, expected first divergence, policy attachment point, positive control, negative control, synthetic counterfactual, alternative explanations, and remediation oracle.

## Controlled validation

1. Pin framework, proxy, application, middleware, and route configuration revisions.
2. Define the semantic-equivalence class and neighboring intentionally distinct class before evaluating behavior.
3. Build synthetic request fixtures and inert handlers inside the authorized test harness.
4. Record interpretation snapshots for a canonical positive-control fixture.
5. Record a neighboring negative-control fixture under the same instrumentation.
6. Vary one representation dimension at a time in the synthetic harness while preserving the declared semantic intent.
7. Identify the first state divergence and record rewrite provenance or mount provenance when applicable.
8. Bind the divergence to the middleware partial order and policy attachment point using source/configuration traces.
9. Check identity binding, tenant binding, method semantics, host semantics, and proxy trust at the relevant decision point.
10. Establish handler reachability using an inert test marker or deterministic unit/integration assertion.
11. Add explicit snapshots for fallback route, error route, or downstream dispatch transitions.
12. Evaluate a synthetic counterfactual fixture that removes only the suspected causal difference.
13. Re-run positive, negative, and neighboring controls to reject stale fixtures, instrumentation differences, or intentionally different policy classes.
14. Preserve the smallest fixture set that demonstrates the reviewed invariant and its controls.

## False-positive controls

Use canonical versus equivalent fixtures, protected versus intentionally public inert handlers, expected versus neighboring methods, and trusted versus untrusted modeled topology metadata.

Reject or downgrade a candidate when any **alternative explanation** remains plausible, including:

- the requests are not actually one semantic-equivalence class;
- the route classes intentionally have different policy;
- a documented alias changes semantics rather than representation only;
- middleware traces differ but the same policy decision still governs the handler;
- the selected handler is not handler-reachable in the modeled control flow;
- principal or tenant context differs legitimately;
- proxy trust assumptions in the fixture do not match reviewed configuration;
- a fallback route or error route is intentionally a distinct policy class;
- stale fixture/configuration state explains the difference.

## Counterfactual controls

Use source-level, policy-model, or synthetic fixture counterfactuals only. A useful counterfactual changes the modeled suspected cause while keeping neighboring state constant, then asks whether the policy difference disappears in the deterministic harness.

Always retain a **neighboring control** that should remain allowed or intentionally distinct. This prevents a proposed remediation from appearing successful merely because the test harness no longer reaches any handler.

## Evidence ladder

- **Hypothesis** — source/configuration suggests a plausible interpretation or policy-ordering issue, but no deterministic trace establishes it.
- **Observed** — a synthetic authorized trace shows a representation, route, middleware, identity, or policy-state difference.
- **Validated** — semantic equivalence is justified; the first causal divergence is identified; the relevant policy attachment consumes different or missing security state; handler reachability is proven in the inert harness; a counterfactual removes the effect; positive/negative/neighboring controls reject plausible alternatives.
- **Regression verified** — after remediation, equivalent fixtures receive the intended common policy treatment and intentionally distinct neighboring classes retain expected behavior.

Do not infer validated state from a status code, normalized path, route name, handler name, middleware list, or one surprising trace alone.

## Evidence capture

```text
stack_revision:
topology_revision:
semantic_equivalence_class:
reviewed_invariant:
raw_test_fixture:
interpretation_snapshots:
rewrite_provenance:
mount_provenance:
route_match:
middleware_partial_order:
identity_binding:
tenant_binding:
method_semantics:
host_semantics:
proxy_trust:
policy_attachment_point:
policy_decision:
fallback_or_error_route:
selected_inert_handler:
handler_reachability:
downstream_dispatch:
first_causal_divergence:
counterfactual_result:
positive_control:
negative_control:
neighboring_control:
alternative_explanations_rejected:
evidence_state:
```

The evidence chain must show which component changes state, which policy consumes that state, and how the transition affects the reviewed invariant.

## Remediation proof

Prefer remediation that restores a stable invariant rather than special-casing one fixture. Depending on root cause, that can mean a single canonical interpretation before policy, explicit route-group policy, stable middleware ordering, earlier identity/tenant binding, tighter modeled trust assumptions, or policy re-evaluation after a security-relevant internal transformation.

Remediation proof requires all of the following in the deterministic harness:

1. the original equivalent fixtures now receive the intended common policy treatment;
2. the first causal divergence no longer creates a policy difference;
3. the synthetic counterfactual agrees with the proposed mechanism;
4. positive and negative controls retain expected outcomes;
5. at least one neighboring control remains valid;
6. relevant fallback route, error route, method/host semantics, and downstream dispatch fixtures are rechecked.

## Remediation checks

Replay the original synthetic fixtures and controls against the fixed revision. Compare hopwise interpretation snapshots before and after the change rather than comparing only final responses.

A remediation is incomplete if it fixes one representation while another equivalent fixture still breaks the invariant, moves the policy inconsistency into fallback/error handling, changes identity or tenant timing elsewhere, or passes only because legitimate handler reachability was removed.
