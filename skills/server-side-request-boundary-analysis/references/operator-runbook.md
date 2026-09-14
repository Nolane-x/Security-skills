# Server-Side Request Boundary Operator Runbook

Use this runbook for source review, policy-model review, local unit/integration tests, synthetic resolvers/proxies, mock receivers, isolated lab networks, and explicitly authorized development environments. Dynamic checks must terminate at controlled services. Do not probe real internal networks, link-local metadata services, administrative endpoints, or unrelated third-party infrastructure.

The objective is to prove how an outbound request changes state from application input to controlled final peer, and whether each security-relevant transformation remains bound to the owner-approved destination policy.

A complete review correlates four evidence layers:

1. **policy evidence** — what destination/authority relation should be allowed;
2. **application-state evidence** — what parser, canonicalizer, redirect handler, worker, and policy layer believe the destination is;
3. **transport evidence** — which resolver/route/connection target and controlled final peer are actually used;
4. **control evidence** — neighboring cases that isolate the relevant state transition and rule out harness artifacts.

## Destination policy semantics

Write the destination policy before evaluating behavior. A useful policy identifies the semantic classes that matter to the application rather than relying on an informal phrase such as "public URLs only."

Record, where relevant:

```text
accepted request provenance
accepted schemes
canonical host/origin rule
permitted port rule
resolved-address classes
redirect transition rule
proxy/egress rule
authority-attachment rule
worker revalidation rule
connection-reuse assumptions
```

### Validation input

The **validation input** is the exact representation presented to a destination-policy decision. It may be raw text, parsed components, a canonical tuple, a stored callback record, or an indirect identifier that later resolves to a destination.

Record the representation because a rule over raw text and a rule over a canonical destination are not equivalent. If the policy layer receives only a stored "validated=true" flag while execution reconstructs a destination independently, the flag does not preserve the security state by itself.

### Canonical destination

Define the **canonical destination** in terms that can be compared across components. Typically it includes:

- scheme/protocol family;
- canonical host or origin identity;
- effective port;
- path-independent attributes that alter routing/trust if the application policy depends on them;
- any application-level destination class.

Do not prescribe one universal normalization algorithm. The correct canonicalization depends on the URL/network libraries and the application's policy contract. The requirement is semantic agreement between the policy representation and the execution representation.

### Resolved address and destination class

A **resolved address** is one resolution result considered by the component that ultimately selects a network endpoint. Record who resolved the name: application resolver, HTTP client, proxy, sidecar, gateway, or another component.

Classify only controlled addresses in tests. The policy question is whether the address actually eligible for connection belongs to the allowed class, not whether an earlier lookup returned an allowed value.

### Redirect rule

Specify whether redirects are followed, which destination changes require revalidation, and how authority attachment changes across hops. Avoid assuming that a redirect remains inside the original trust relation merely because the first URL was approved.

### Authority attachment

**Authority attachment** includes security-relevant request/transport context the server may add: synthetic credential markers in tests, cookies, internal headers, proxy identity, client certificate identity, or source-network privilege represented by the test topology.

Define authority-forwarding policy separately from reachability. A destination may be allowed to receive a request but not a particular credential/header class.

### Policy checkpoint

A **policy checkpoint** is a decision over a specific request state. Name the exact state fields it sees and the transformation it authorizes next.

Examples of semantic checkpoints include:

- after canonical parsing but before resolution;
- after address selection but before connect;
- after each redirect target is canonicalized/resolved;
- at proxy/gateway egress;
- at worker execution time;
- before attaching origin-scoped authority.

A checkpoint should not be credited with protecting a later state it never evaluated.

## Attack surface

Model the complete outbound request path inside owned source and test infrastructure.

### Entrypoints

Inventory application features that produce server-side requests, such as preview/import/render/callback/webhook/integration functionality, remote schemas/templates, repository/package/feed retrieval, or asynchronous fetch jobs.

For each entrypoint record:

- request provenance;
- user-influenced fields;
- whether the destination is direct or derived;
- whether the destination is stored and fetched later;
- whether multiple components reinterpret it;
- whether any server authority is attached.

### Parsing and canonicalization components

Identify each component that can reinterpret destination identity:

- validation parser;
- application canonicalizer;
- network/HTTP client;
- redirect handler;
- resolver;
- proxy/sidecar/gateway;
- connection pool;
- worker or downstream renderer/protocol handler.

The review question is not "do these libraries differ?" It is "can a policy-approved state become a materially different execution state without an equivalent policy decision?"

### Egress and trust zones

Use synthetic destination classes in tests, for example:

```text
approved-external-style-mock
protected-style-mock
same-origin-neighbor-mock
redirector-mock
proxy-routed-mock
authority-receiver-mock
```

These are semantic fixtures, not substitutes for real protected infrastructure. A unique controlled marker is enough to prove which class received a request.

## Hypothesis matrix

| Hypothesis class | Causal question | Evidence required | Main disambiguation |
| --- | --- | --- | --- |
| parser-policy divergence | does validation authorize a destination meaning different from the client interpretation? | validation state + canonical execution state + controlled final-peer correlation | same semantic destination through both parsers |
| resolution binding gap | is policy bound to the address selected for connection? | canonical host, resolution result, selected connection target, checkpoint decision | fixed resolver state versus changed controlled result |
| redirect checkpoint gap | does every security-relevant hop receive an equivalent policy decision? | ordered redirect state and per-hop checkpoints | approved in-class hop chain versus one changed class |
| proxy/egress divergence | does downstream routing reinterpret or widen the destination? | application state + proxy route + proxy-side/final-peer evidence | direct and proxy fixtures under same policy |
| authority-forwarding gap | is attached authority constrained by final origin/destination class? | authority-attachment decision + controlled receiver log | same flow with and without fake authority marker |
| worker validation drift | does delayed execution reconstruct/revalidate destination state? | request-time state + execution-time state + worker checkpoint | same stored fixture under pinned worker environment |
| connection-reuse mismatch | does reused transport preserve origin/destination assumptions? | pool identity + logical request state + controlled peer identity | isolated connection versus reused connection fixture |
| consequence overclaim | is reachability being mistaken for protected access? | transport evidence separated from benign protected marker | receiver reachable but marker unavailable control |

Every hypothesis should predict which request-state field or policy checkpoint must differ in a neighboring control.

## Request state machine

Treat each outbound operation as a sequence of security states rather than a single URL.

A useful conceptual trace is:

```text
S0 request provenance
S1 validation input
S2 parsed/canonical destination
S3 resolution result or proxy destination request
S4 selected route/egress
S5 redirect target state (zero or more)
S6 connection target
S7 final peer
S8 authority attachment actually received
S9 bounded mock effect
```

Not every implementation exposes all states. Record only states that exist, but do not silently merge states whose distinction matters to the policy.

### State identity

For each state, record:

- component that produced it;
- canonical destination identity known at that point;
- resolution/route identity if available;
- applicable policy checkpoint;
- authority that may be attached next;
- evidence source and timestamp/revision.

### Transition invariant

For transition `Si -> Sj`, ask:

> Does the security meaning remain inside the state authorized by the latest applicable policy checkpoint?

If yes, document why the transition preserves equivalence. If no, identify the new checkpoint that must evaluate the changed state.

### Redirect state

Represent redirects as repeated state transitions, not one final URL. For each controlled hop capture:

- previous canonical destination;
- redirect target representation;
- canonicalized target;
- resolution/route state relevant to the next request;
- destination-policy decision;
- authority-forwarding decision.

### Async state

When a worker executes later, create a new state snapshot. Record what was persisted from request time and what is recomputed at execution time. A persisted "validated" bit is evidence only if the worker's effective destination is cryptographically/structurally bound to the exact state that was validated, or if execution revalidates the final state.

## Resolution and connection binding

Resolution evidence is valuable only when it can be related to the connection that follows.

### Resolution result

Record the controlled **resolved address** or address set and the resolver component responsible. Distinguish:

- application-side resolution;
- client-internal resolution;
- proxy-side resolution;
- cached resolution;
- connection-reuse path where no fresh resolution occurs.

Do not claim the connection used an address merely because a DNS log contains it.

### Connection target

The **connection target** is the endpoint selected by the component that opens or delegates the transport. In a direct local test this may be a controlled IP/port tuple; under a test proxy, the application connection target may be the proxy while the proxy has a separate upstream target.

Record both layers when they differ.

### Final peer

The **final peer** is the controlled receiver correlated to the tested request. Correlation may use an inert unique request marker, receiver log, local transport instrumentation, or an equivalent deterministic test signal.

Do not use sensitive content as the correlation mechanism.

### Binding requirement

A strong proof connects:

```text
canonical destination
-> policy checkpoint
-> resolution/route result
-> connection target
-> final peer
```

If one of these mappings is inferred rather than observed, mark the assumption and reduce the evidence state accordingly.

### Proxy and gateway semantics

When a proxy/gateway performs upstream resolution or connection, the application-side policy must either constrain the exact proxy request sufficiently or rely on an independently enforced downstream destination policy. Review both parts rather than assuming the application socket target is the protected destination.

### Connection pooling

Document the pool key or semantic connection identity only to the extent needed to prove origin/destination isolation in a local test. The key question is whether a new logical request can inherit a transport whose peer/authority assumptions belong to a different policy state.

## Controlled validation

Use only isolated fixtures and inert effects.

1. Freeze application, parser/client, resolver, proxy, redirect, worker, and pool configuration.
2. Write the destination and authority-forwarding policy.
3. Create controlled destination classes with unique non-sensitive markers.
4. Establish an intended allowed positive control through the actual feature path.
5. Establish a neighboring denied destination class through the same path.
6. Capture the request state machine for both cases.
7. Change one state dimension at a time: canonical destination class, controlled resolution result, redirect class, route/proxy state, worker snapshot, or fake authority attachment.
8. Correlate the selected connection target to the controlled final peer.
9. Treat fake credential/header markers as independent evidence from reachability.
10. Stop once the smallest synthetic causal proof is obtained.

Do not substitute real internal or metadata destinations for semantic mock classes.

## Counterfactual controls

A **counterfactual** asks which outcome should change if one security-relevant request-state fact changes while the rest of the path stays comparable.

### Neighboring control

A strong **neighboring control** differs in one policy-relevant dimension, for example:

- same feature/path, different canonical destination class;
- same canonical host, different controlled resolution result;
- same redirect chain, one hop changes destination class;
- same final peer class, fake authority attachment enabled versus stripped;
- same stored request record, worker environment/policy checkpoint differs;
- same logical origin, isolated versus reused controlled connection.

### Canonicalization counterfactual

If the causal hypothesis is parser/canonicalization divergence, a representation that canonicalizes to the same approved destination should preserve the decision, while a representation that canonicalizes to a different policy class should not inherit the old decision.

### Resolution counterfactual

Hold canonical host and feature path fixed while changing only the controlled resolution class. If address class is policy-relevant, the connection checkpoint should change as predicted.

### Redirect counterfactual

Hold the initial approved destination fixed and vary only one controlled redirect hop. An in-policy hop should remain functional; a hop that moves into a denied class should stop before a connection to that next controlled peer.

### Authority counterfactual

Hold reachability constant and vary only the fake authority marker. This separates "destination may be contacted" from "destination may receive server authority."

### Alternative explanation

For every promoted finding, name at least one plausible **alternative explanation** and the control that weakens it. Common alternatives include:

- test proxy or gateway intentionally rewrote the route;
- resolver cache retained earlier controlled state;
- container/hosts mapping changed destination identity;
- mock redirect fixture was misconfigured;
- receiver marker came from an unrelated request;
- connection reuse explains peer identity;
- worker ran a different revision/configuration;
- owner-approved exception permits the observed class.

Stronger language does not replace these controls.

## False-positive controls

Use controls aligned to the state machine:

- approved versus denied semantic destination through the same entrypoint;
- validation input versus canonical destination recorded by the same test;
- fixed versus changed controlled resolution result;
- direct approved destination versus approved initial destination with changed redirect class;
- direct route versus test proxy route;
- fresh connection versus controlled reused-connection fixture;
- fake authority absent versus present;
- request-time versus worker-execution policy snapshot;
- receiver marker correlated versus uncorrelated request;
- reachability-only mock versus benign protected-marker mock.

Downgrade a case when the mismatch is explained by the test harness, documented policy exception, stale/cached state, or an unbound evidence layer.

A URL string, response status, or DNS event alone is insufficient for a validated boundary-crossing claim.

## Evidence ladder

### Hypothesis

Use when source/configuration review suggests a possible mismatch between a policy checkpoint and a later request state, but controlled transport/final-peer evidence is missing.

Record:

- expected destination rule;
- suspected state transition;
- checkpoint believed to be stale/missing/misaligned;
- missing evidence needed for promotion.

### Observed

Use when a controlled state transition or final-peer event is reproducible but the owner-approved policy violation or causal mechanism is incomplete.

Record the exact state(s) observed and the remaining assumption.

### Validated

Use only when:

- the destination/authority policy is explicit;
- the request state machine shows the relevant transformation;
- policy checkpoint coverage is known;
- connection target/final peer is correlated to the tested request;
- the final peer or received fake authority violates the policy being tested;
- positive and neighboring controls isolate the relevant dimension;
- material alternative explanations have been addressed;
- any protected consequence is an inert synthetic marker.

### Regression verified

Use only after the fixed revision blocks the original causal transition for the intended reason, preserves the positive flow, and passes neighboring controls covering equivalent canonical/resolution/redirect/route/authority states in the reviewed scope.

## Evidence capture

Preserve state-machine evidence rather than only request/response text:

```text
case_id:
application_revision:
feature_or_entrypoint:
request_provenance:
destination_policy:
validation_input:
canonical_destination:
resolution_result:
resolver_component:
redirect_states:
policy_checkpoints:
egress_route:
proxy_upstream_target_if_any:
connection_target:
final_peer:
correlation_marker:
authority_attachment:
bounded_mock_effect:
positive_control:
neighboring_control:
counterfactual_prediction:
alternative_explanation:
alternative_explanation_control:
evidence_state:
causal_transition:
```

A strong causal statement names the state transition, not merely the symptom.

## Remediation checks

Prefer an invariant shared by validation and execution rather than a blacklist of textual forms.

Review whether remediation:

1. defines one canonical destination representation for policy purposes;
2. evaluates the actual controlled resolution/connection class when address class matters;
3. rechecks destination policy after each security-relevant redirect transition;
4. constrains effective port/scheme according to policy;
5. preserves equivalent enforcement through proxy/gateway routing;
6. scopes authority attachment to the correct normalized destination/origin;
7. binds worker execution to an execution-time destination decision or an immutable validated state;
8. preserves destination/origin isolation across connection reuse;
9. uses network/egress controls as independent defense in depth where appropriate;
10. emits enough non-secret state/decision telemetry to reconstruct a future policy mismatch.

## Remediation proof

A remediation is proven by replaying the causal request-state transition, not by blocking one textual input.

### 1. Replay the original state trace

Use the same synthetic provenance, semantic destination class, and controlled topology. Confirm where the fixed **policy checkpoint** now denies or reclassifies the transition.

### 2. Preserve the intended positive flow

The approved destination must still reach the intended controlled **final peer** through its expected **connection target** and egress route.

### 3. Replay neighboring controls

Choose controls based on the original cause:

- parser/canonicalization issue -> equivalent approved representation plus changed canonical class;
- resolution issue -> same host with approved versus denied controlled resolution class;
- redirect issue -> approved in-class chain plus one changed hop;
- proxy issue -> direct and proxy semantic equivalents;
- authority-forwarding issue -> same reachability with fake marker stripped/attached as policy requires;
- worker issue -> request-time and execution-time state variants;
- pool issue -> fresh and reused controlled connection variants.

### 4. Confirm resolution and connection binding

The fixed trace should connect **canonical destination -> resolved address/route -> connection target -> final peer** without relying on the stale representation that caused the original defect.

### 5. Confirm authority attachment independently

If the issue involved credentials/headers, prove the destination is still reachable when intended while the protected fake marker is absent from peers that should not receive it.

### 6. Reject overfit fixes

Do not accept proof that only:

- blocks one literal string;
- changes an error/status without changing request-state enforcement;
- disables the feature;
- special-cases one test host;
- fixes the synchronous path while a worker reconstructs the old unsafe state;
- adds application validation while proxy/egress semantics still bypass the intended invariant.

### 7. State residual scope

Record which entrypoints, execution modes, redirect behavior, proxy route, and worker path were covered. A precise residual scope is stronger than claiming universal outbound-request safety without evidence.
