---
name: web-routing-and-middleware-analysis
description: "Analyze server-side routing and middleware composition: path normalization, mount scopes, auth filters, rewrites, method matching, proxy headers, error routes, and handler reachability. Use to find policy gaps caused by route interpretation differences."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Web Routing And Middleware Analysis

Treat routing as a sequence of request interpretations and policy decisions, not as a lookup from a URL string to a handler. A security conclusion requires evidence that two requests belonging to the same intended semantic-equivalence class cross the routing stack with materially different policy treatment.

## When to use

Use for web frameworks, API gateways, reverse proxies, middleware stacks, route groups, rewrite engines, or applications with multiple normalization/auth layers.

## Preconditions

1. Use source plus a local, staging, sandboxed, or explicitly authorized deployment.
2. Pin framework, server, proxy, middleware, route-table, and relevant configuration revisions.
3. Use synthetic users and tenants, inert handlers, controlled response markers, and test-only state.
4. Write the reviewed policy invariant before changing request representation. State which requests are intended to be equivalent and which neighboring requests are intentionally distinct.
5. Identify which infrastructure-derived fields are trusted in the authorized topology. Do not manufacture proxy trust that the deployment does not actually grant.

## Request-policy invariant model

Model each request as a state trace rather than one path string:

```text
raw request
  -> edge/proxy interpretation
  -> normalized request
  -> rewrite/mount state
  -> route candidate + route match
  -> middleware partial order
  -> identity binding + tenant binding
  -> policy attachment point + policy decision
  -> selected handler
  -> downstream dispatch / bounded effect
```

For every transition, record an **interpretation snapshot**: the path, method, host, authority-relevant headers, query/body classification when relevant, route scope, identity/tenant state, and which component produced the next state.

The key unit of comparison is a **semantic-equivalence class**. Two syntactically different requests belong to the same class only when the application contract says they represent the same reviewed resource/action. Similar-looking strings are not enough. Conversely, intentionally distinct method, host, tenant, route, or policy classes must remain distinct and serve as negative controls.

A finding requires a broken invariant, not merely a surprising route. Express the invariant explicitly:

```text
if request A and request B are intended to be semantically equivalent,
then required security policy P must attach before security-relevant dispatch D
under the same relevant identity, tenant, and trusted-topology assumptions.
```

## Interpretation and policy discipline

### Interpretation provenance

Keep **mutation provenance** for every normalization, rewrite, mount, alias, fallback, or internal dispatch. Record the component that changed the representation, the before/after state, and whether the change occurs before or after security policy attaches. Do not collapse several transformations into a final normalized path because that hides where semantics diverged.

### Policy attachment point

For every relevant control, identify the exact **policy attachment point**: authentication, authorization, tenant restriction, CSRF/origin policy, content-type policy, or another reviewed guard. Record whether it binds to the pre-rewrite route, post-rewrite route, route group, controller, downstream service, or another state.

A middleware name in a trace is not proof that its decision governed the selected handler. Confirm its position in the **middleware partial order**, the state it consumed, whether it short-circuited or delegated, and whether later rewrites or dispatch changed the object/action governed by that decision.

### Identity and tenant timing

Record **identity binding** and tenant binding as state transitions. A principal being present eventually is insufficient if routing or policy-relevant selection happened earlier. Conversely, late identity attachment is not automatically wrong: the reviewed invariant must require identity at the earlier decision point.

### Method, host, and proxy semantics

Treat method semantics, host interpretation, forwarded metadata, scheme/port, and proxy-derived identity as topology-dependent state. Only infrastructure-authenticated metadata may participate in trusted policy reasoning. A client-visible header name is not evidence of trust.

### Handler reachability

Separate route match from **handler reachability**. A selected route can be unreachable because earlier middleware terminates the request; a policy can also be enforced downstream after route selection. Record the complete causal path to the inert handler or controlled marker before claiming a policy difference.

### Fallback and error routing

Model each **fallback route** and **error route** as an explicit transition with its own policy context. Distinguish framework-generated error handling, application fallback, proxy fallback, and downstream retry/dispatch. A fallback that intentionally belongs to another policy class is not a bypass.

## Workflow

1. Define one reviewed request-policy invariant and its semantic-equivalence class before testing variants.
2. Build the expected request-state trace from source and configuration: edge/proxy interpretation, normalization, rewrite/mount, route match, middleware order, identity/tenant state, policy decision, handler, and downstream dispatch.
3. Capture one canonical positive control and at least one intentionally distinct negative control using synthetic identities and inert handlers.
4. Record an interpretation snapshot at every observable hop for the canonical request.
5. Change one representation dimension at a time inside the authorized deployment while preserving the declared semantic intent. Examples can include documented aliases, normalization differences, method handling, mount/rewrite paths, or trusted proxy context.
6. When behavior differs, identify the first state divergence and preserve its mutation provenance rather than reasoning backward only from the final handler.
7. Bind that divergence to a policy attachment point. Determine whether the relevant policy consumed a different state, was absent, moved in the middleware partial order, or remained equivalent despite the route difference.
8. Run a **counterfactual** that removes the suspected causal difference while keeping neighboring state fixed. The policy difference should disappear if the suspected transition is causal.
9. Repeat with neighboring allowed and denied controls to reject explanations based on stale state, intentionally different policy classes, handler instrumentation, cache artifacts, or unrelated middleware behavior.
10. Route confirmed normalization or authorization subproblems to the corresponding canonical skills; do not duplicate their domain logic here.

## Evidence ladder

Use the repository evidence states conservatively:

- **Hypothesis** — source/configuration suggests an interpretation or policy-ordering risk, but no runtime trace proves it.
- **Observed** — an authorized inert test shows a route, middleware, identity, or policy-state difference, but causality or semantic equivalence is not yet established.
- **Validated** — semantic equivalence is justified, the first divergent transition is identified, the relevant policy attachment changes or consumes different security state, a counterfactual links that difference to the result, and neighboring controls exclude plausible alternatives.
- **Regression verified** — after remediation, the original equivalent representations receive the intended common policy treatment and neighboring intentionally distinct classes retain their expected behavior.

Do not promote an observation merely because a different handler, status code, middleware trace, or normalized path appears.

## Evidence contract

A validated finding records:

- pinned stack/configuration revisions and authorized topology;
- the declared semantic-equivalence class and reviewed invariant;
- raw request plus hopwise interpretation snapshots;
- rewrite/mount/mutation provenance;
- middleware partial order and policy attachment point;
- identity binding and tenant binding timing;
- selected handler and proof of handler reachability or controlled downstream dispatch;
- positive, negative, counterfactual, and neighboring controls;
- the first causal state divergence and the alternative explanations rejected;
- evidence state and remediation regression result.

A route alias, handler difference, or middleware-order difference is not a security finding unless it changes the reviewed policy invariant.

## Stop conditions

Stop if testing targets public production endpoints, causes stateful business actions, uses real user or tenant data unnecessarily, requires spoofing infrastructure trust not present in the authorized topology, or cannot be reduced to inert/synthetic validation. Stop escalation if semantic equivalence cannot be justified or the suspected policy difference cannot be causally separated from alternative explanations.

## Output

```text
stack/config revisions:
authorized topology:
reviewed invariant:
semantic-equivalence class:
raw request:
interpretation snapshots:
mutation provenance:
route match / fallback / error state:
middleware partial order:
identity + tenant binding:
policy attachment point / decision:
selected inert handler:
handler reachability:
first causal divergence:
counterfactual result:
positive / negative / neighboring controls:
alternative explanations rejected:
evidence state:
remediation regression:
```
