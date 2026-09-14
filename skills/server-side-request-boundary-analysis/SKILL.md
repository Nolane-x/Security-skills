---
name: server-side-request-boundary-analysis
description: "Analyze server-side outbound request features for destination parsing, DNS/address resolution, redirect policy, scheme support, proxy use, credential forwarding, and network trust zones. Use to assess SSRF-like boundaries without scanning internal networks."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Server Side Request Boundary Analysis

A server-side outbound request is a security decision that evolves through multiple representations. The original text supplied to an application is not necessarily the destination later resolved, routed, connected, or authorized to receive attached server authority.

Analyze the complete request state from **request provenance** to **final peer**. A destination policy is trustworthy only when it constrains the security-relevant destination at every transformation that can change that destination or the authority attached to the request.

Perform dynamic validation only in local, owned, sandboxed, benchmark, or explicitly authorized test environments. Use synthetic destination classes, controlled resolvers/proxies, mock receivers, fake credentials, and inert protected markers. Do not probe real internal networks, metadata services, administrative endpoints, or third-party infrastructure.

## When to use

Use when software performs server-side retrieval, callback, preview, rendering, webhook validation, remote import, repository/package/feed access, media/document processing, or another operation in which untrusted or semi-trusted input influences an outbound destination.

Use this skill when the security question involves one or more of these boundaries:

- textual input versus parsed destination;
- validation parser versus execution client;
- hostname identity versus resolved address identity;
- initial destination versus redirected destination;
- direct route versus configured proxy/egress route;
- synchronous request versus delayed/background execution;
- destination identity versus credentials, cookies, headers, mTLS identity, or other attached authority;
- policy decision versus the connection target or final peer that actually receives the request.

Do not infer a boundary failure merely because a string resembles an internal address, a DNS lookup occurred, or the server produced a different HTTP status. The evidence must connect the defined destination policy to the controlled final network effect.

## Preconditions

1. Define an owner-approved destination policy before testing: accepted schemes, destination classes, ports, redirect behavior, resolution policy, proxy expectations, credential/header forwarding rules, and revalidation points.
2. Use only controlled mock destinations and fake authority markers.
3. Pin or record resolver, proxy, HTTP client, container/network namespace, redirect, worker, and connection-pool behavior relevant to the test.
4. Keep all dynamic confirmation inside an isolated test topology. If a case cannot be proven without contacting a real protected or third-party endpoint, stop at the strongest lower evidence state.

## Destination decision model

Represent the outbound decision as a stateful relation rather than a one-time URL allow/deny check.

```text
request provenance P
validation input I
canonical destination D0
resolution result R0
redirect state H0
policy checkpoint C0
route/egress E0
connection target T0
final peer F0
authority attachment A0
-> bounded effect O
```

Each state transition may preserve the same security meaning or may create a new destination decision that must be evaluated again.

### Request provenance

**Request provenance** answers where the destination influence came from and which feature is responsible for interpreting it. Distinguish direct URL input from an indirect object ID, stored callback, imported configuration, repository metadata, queue payload, previously validated record, or application-generated redirect target.

Provenance matters because a background worker or downstream component may incorrectly treat stored data as trusted simply because an earlier component accepted it.

### Validation input

The validation input is the exact representation seen by the policy layer before execution. Record whether the policy receives raw text, parsed URL components, a normalized host/port tuple, a resource identifier that later resolves to a URL, or another derived representation.

Do not assume the validator and the network client interpret the same text identically.

### Canonical destination

The **canonical destination** is the security-relevant destination identity after the application-defined normalization required before policy evaluation. It normally includes at least scheme, canonical host identity, effective port, and any provider/application-specific attributes that change routing or trust.

Canonicalization is not valuable by itself. It is valuable only if the execution path is bound to the same canonical destination or to a later destination that is re-evaluated.

### Resolution result

The **resolution result** is the address or controlled address set produced for the canonical host at the point relevant to connection establishment. A host-level policy and an address-level policy answer different questions; record both where the security boundary depends on address class.

A DNS answer observed at one time is not automatically proof of the address used by the actual connection. Resolver cache, dual-stack selection, proxy resolution, connection pooling, or later lookup can change the effective result.

### Redirect state

The **redirect state** is the ordered, bounded set of destination transitions produced by an application/client-controlled redirect flow. Each hop may change scheme, host, effective port, address class, origin, or authority-forwarding eligibility.

Treat a redirect hop as a new destination state unless the owner-approved policy explicitly and safely defines an equivalent class that remains valid without recomputation.

### Policy checkpoint

A **policy checkpoint** is the point where the current destination state is classified and allowed, denied, or left unresolved. Record both the input to the checkpoint and what future transformation it authorizes.

A checkpoint before name resolution does not prove a post-resolution address decision. A checkpoint before redirect does not authorize an unrelated later hop. A request-time checkpoint does not automatically authorize a worker that reinterprets the destination under a different environment.

### Egress route

The **egress route** describes how the request leaves the application component: direct socket, explicit proxy, sidecar/gateway, service mesh, sandbox broker, or another controlled routing layer. The policy model must state whether destination resolution and enforcement occur before the route, inside the route, or both.

A proxy can narrow reachability, preserve it, or change the identity of the component that performs resolution. Do not infer final destination from application-side socket information when the proxy is the real connector.

### Connection target and final peer

The **connection target** is the endpoint selected for a connection attempt after the relevant parsing, resolution, routing, and policy stages.

The **final peer** is the controlled receiver that actually accepts the bounded test connection, or the equivalent transport identity exposed by a local test double. Keep this distinct from hostname, DNS answer, proxy endpoint, and HTTP Host/SNI metadata.

A validated destination-boundary claim must explain how the policy-relevant destination maps to the final peer. "The application performed a lookup" or "the client constructed a request" is weaker evidence than final-peer correlation.

### Authority attachment

**Authority attachment** is the set of security-relevant capabilities added to the outbound request or transport: fake authorization markers in tests, cookies, service headers, client identity, proxy identity, or source-network privilege represented by the test topology.

Analyze attachment separately from reachability. A controlled destination may be reachable but correctly receive no protected authority. Conversely, a header-forwarding defect may matter even when destination reachability is expected.

## Request-path reasoning discipline

1. **Define policy before behavior.** State which destination classes, schemes, ports, redirect transitions, and authority transfers should be allowed. If the owner cannot define the rule, record a design ambiguity instead of manufacturing a vulnerability expectation.
2. **Treat the request as a state machine.** Record how destination identity changes at parsing, canonicalization, resolution, redirect, routing, worker execution, and connection reuse.
3. **Bind every policy checkpoint to what it authorizes.** A validation result is meaningful only for the destination state it actually evaluated.
4. **Separate host policy from address policy.** A permitted hostname does not by itself prove every resolved address is permitted, and a blocked address class does not prove every hostname that once resolved there remains blocked after later resolution.
5. **Separate resolution evidence from connection evidence.** DNS logs, resolver output, client plans, and final-peer logs are different evidence layers.
6. **Re-evaluate after destination-changing transitions.** Redirect, re-resolution, proxy routing, delayed execution, alias resolution, and other transformations require an explicit reason if the old decision is reused.
7. **Keep authority attachment origin-aware.** Forwarding a fake credential marker to one approved origin does not imply it may follow redirects or be sent to a neighboring destination class.
8. **Model connection reuse explicitly.** A pool key or reused transport must preserve the same destination/origin assumptions on which policy and authority attachment relied.
9. **Use counterfactual reasoning.** Change one security-relevant dimension and predict which policy checkpoint or final-peer outcome should change while the intended neighboring flow remains stable.
10. **Search for alternative explanations.** Test proxy configuration, stale resolver cache, container host mapping, mock redirect behavior, connection reuse, worker configuration drift, and documented destination exceptions can explain apparent mismatches.
11. **Do not equate reachability with protected consequence.** Reaching a controlled socket proves one boundary. Receiving a benign protected marker or fake authority marker proves a stronger, different boundary.
12. **Stop at first sufficient synthetic proof.** Never extend a validated mock result into real internal, metadata, administrative, or third-party targets.

## Workflow

1. Freeze the application revision and relevant parser/client/resolver/proxy/worker configuration.
2. Write the destination policy and identify every policy checkpoint.
3. Trace request provenance from feature input or stored state to the execution component.
4. Record the validation input and canonical destination.
5. Record resolution behavior and which component performs it.
6. Determine the destination/address class at the point immediately relevant to connection creation.
7. Trace redirect state hop by hop and record a fresh policy decision whenever security-relevant destination identity changes.
8. Trace the egress route and identify whether a proxy/gateway performs its own resolution or destination enforcement.
9. Correlate the connection target with the controlled final peer.
10. Trace fake authority attachment and stripping rules independently from destination reachability.
11. For background work, repeat the state model at execution time rather than relying on a stale "validated" flag.
12. Establish an intended allowed positive control and a neighboring denied control through the same code path.
13. Change one state dimension at a time for counterfactuals.
14. If stronger impact evidence is necessary, use a benign protected mock marker only; do not substitute a real protected service.
15. Remediate at the narrowest shared policy/connection-binding layer and replay the original state trace plus neighboring controls.

## Operator depth

For a full authorized review, load the [operator runbook](references/operator-runbook.md). It expands this model into destination-policy semantics, request state transitions, parser/client agreement, resolution-to-connection binding, redirect checkpoints, egress/proxy semantics, authority attachment, asynchronous execution, false-positive controls, evidence thresholds, and remediation proof using controlled fixtures only.

The [operator scenarios](references/operator-scenarios.json) retain the existing three scenario classes while adding explicit request-state traces, policy checkpoints, false-positive guards, evidence-upgrade criteria, and neighboring regression requirements.

## Evidence ladder

### Hypothesis

Use when source/configuration review suggests a destination-policy mismatch may exist, but no controlled final-peer or equivalent transport evidence establishes the relevant transition.

Record the suspected state transition and the missing proof. Example: validation occurs before resolution, but it is not yet known whether the connector rechecks the selected address.

### Observed

Use when a controlled state transition or final-peer event is reproduced, but the policy violation, causal mechanism, or protected consequence remains incomplete.

Examples include a controlled DNS resolution, redirect transition, proxy route, or final-peer connection that is relevant to the hypothesis but has not yet been tied to the full owner-approved destination rule.

### Validated

Use only when:

- the destination policy is explicit;
- the controlled request state trace identifies the relevant policy checkpoint or missing checkpoint;
- the final connection target/final peer violates that policy or receives authority it should not receive;
- an intended positive control proves the feature/path is healthy;
- a neighboring control or counterfactual isolates the relevant destination/authority dimension;
- material alternative explanations such as proxy, resolver cache, host mapping, mock behavior, or documented exceptions have been addressed;
- any protected consequence is demonstrated with an inert synthetic marker only.

### Regression verified

Use only after remediation when the original synthetic state trace is blocked at the intended policy checkpoint or connection-binding invariant, intended allowed traffic still reaches its controlled final peer, and neighboring representations/transitions cannot reproduce the same causal defect in the reviewed scope.

## Evidence contract

A strong finding is a state-transition statement:

> Under destination policy S, request provenance P produces validation input I and canonical destination D. Policy checkpoint C authorizes state X, but transformation Y changes the resolution/redirect/route state to Z without an equivalent decision. Connection target T therefore reaches controlled final peer F. Neighboring control N changes only decision-relevant dimension Q and does not cross the boundary. Alternative explanation A is excluded by control B.

Preserve both policy-side and transport-side evidence. Do not promote based only on textual URL appearance, scanner classification, or an uncorrelated DNS event.

## Stop conditions

Stop or downgrade when:

- the owner-approved destination policy is undefined or contradictory;
- the next step would leave the isolated topology;
- a real internal, metadata, administrative, or third-party endpoint would be required;
- real credentials or secrets would be required instead of fake markers;
- the final peer cannot be correlated to the tested request;
- the observed route is explained by the test proxy, host mapping, resolver cache, connection pool, or documented exception;
- the only evidence is a URL string, status difference, or DNS event without transport binding;
- the benign synthetic proof already establishes the boundary and further impact would add risk rather than evidence.

## Output

```text
case_id:
application_revision:
feature_or_entrypoint:
request_provenance:
destination_policy:
validation_input:
canonical_destination:
resolution_result:
redirect_state:
policy_checkpoints:
egress_route:
connection_target:
final_peer:
authority_attachment:
positive_control:
neighboring_control:
counterfactual:
alternative_explanations_checked:
bounded_mock_effect:
evidence_state:
causal_transition:
remediation_invariant:
regression_neighbors:
```
