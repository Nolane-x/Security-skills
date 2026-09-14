# Authorization Boundary Operator Runbook

Use this runbook for code review, policy-model review, local unit/integration tests, synthetic fixtures, and explicitly authorized development environments. Prefer policy simulators, test doubles, synthetic identities, synthetic resources, and inert assertions. Do not use real third-party identities, data, or production effects as evidence.

The objective is to explain an authorization decision precisely enough that another reviewer can reproduce the reasoning from policy source to final protected effect without relying on intuition.

## Policy semantics

Begin with the expected rule, not with the implementation result.

Represent each question as:

```text
principal P
operation O
resource R
context C
policy source S
-> expected decision D
```

A **policy source** is the authority that defines the expected result: an approved access-control specification, product requirement, policy-engine configuration, ownership rule, tenant-isolation contract, workflow rule, or committed regression oracle.

Do not infer the policy solely from current behavior. Implementation behavior is evidence about enforcement; it is not automatically evidence about intent.

### Principal

Identify the security subject whose authority should govern the operation. Keep separate concepts separate:

- authenticated user;
- tenant or organization membership;
- role/group expansion;
- API or OAuth scope;
- service/workload identity;
- delegated initiator;
- background worker identity;
- support/admin impersonation mode.

A component may execute under a service identity while still being required to preserve and enforce the initiating user's narrower authority.

### Operation

Name the semantic action, not merely the transport label. A route, RPC method, resolver, queue message, and helper method may all implement the same protected operation.

Examples of semantic operations include reading private content, changing object state, changing ownership/sharing, exporting a protected set, approving a transition, or performing an administrative action.

### Resource

Distinguish caller-provided identifiers from the authoritative object used by the implementation.

Track the conceptual sequence:

```text
requested identifier
-> normalized/canonical identifier
-> resolved object
-> tenant/owner relation
-> derived representation or member set
-> final protected object/effect
```

A correct policy decision about one object does not authorize a later effect on a different object unless that transformation is explicitly part of the policy model.

### Context

Include only dimensions that can change the decision, such as tenant, workspace, ownership, role, token scope, authentication strength, delegation purpose, approval state, lifecycle state, or policy revision.

For each context value, record where it comes from. A tenant derived from authenticated membership is not equivalent to a tenant copied from caller-controlled metadata.

### Necessary condition and sufficient condition

Use these terms carefully.

A **necessary condition** must hold for the expected allow. Its absence should make the policy reject the tuple.

A **sufficient condition** is strong enough, together with the explicitly stated baseline assumptions, to justify the expected allow.

One successful example rarely proves sufficiency. A role can be necessary while ownership, tenant membership, state, and scope are also required.

## Attack surface

For this runbook, "attack surface" means the set of code and policy paths that can influence an authorization decision. Review it without expanding scope beyond owned source, policy configuration, tests, and approved fixtures.

### Identity flow

For each identity form, record:

1. where it originates;
2. how it is normalized;
3. how roles/scopes/tenant are derived;
4. how it is propagated between components;
5. which identity is expected to govern the protected operation.

Pay particular attention to transitions between user identity and service identity, delegated identity and executor identity, and request identity and asynchronous worker identity.

### Resource flow

For each resource type, record:

- canonical identifier;
- aliases;
- owner/tenant relation;
- parent-child relation;
- sharing state;
- lifecycle state;
- cached/indexed form;
- aggregate/batch membership;
- export/report representation.

The review question is always: **is the resource used by the policy decision the same security-relevant resource represented at the final sink?**

### Enforcement points

Locate the code or policy layer that decides or structurally constrains access:

- middleware or controller guard;
- service-layer policy function;
- policy engine;
- tenant-scoped repository/query;
- row-level policy;
- privileged helper boundary;
- worker/message consumer policy;
- cache decision layer.

Classify each enforcement point as authoritative, defense-in-depth, or advisory. This prevents a reviewer from assuming that an early route check is the only meaningful boundary.

## Hypothesis matrix

Write a causal hypothesis before writing a test.

| Hypothesis | Candidate cause | Synthetic evidence that would support it | Main false-positive control |
| --- | --- | --- | --- |
| subject-resource binding is incomplete | decision input omits authoritative ownership/resource relation | policy unit test shows neighboring synthetic resource receives same allow | identical policy input except authoritative resource relation |
| tenant binding is incomplete | tenant is derived from wrong source or omitted downstream | synthetic cross-tenant fixture reaches same policy branch as same-tenant fixture | same object shape with authoritative tenant changed only |
| aggregate/member policy differs | collection path constrains envelope but not members | aggregate fixture includes a member that item policy denies | all-allowed aggregate plus denied item oracle |
| delegated context is lost | executor identity replaces initiator identity | mocked delegate receives no initiator/purpose constraint | same delegate with approved initiator/purpose |
| asynchronous authority drifts | worker evaluates broader identity than intended | local worker fixture shows missing caller-bound grant/context | explicit enqueue/execution authority contract |
| cache identity is incomplete | cache key omits principal/resource/context/policy revision | unit test reuses decision after one policy-relevant dimension changes | exact same tuple should still be reusable |
| resource changes after decision | later lookup/canonicalization selects different resource | instrumented test records decision resource != final sink resource | stable canonical-resolution control |
| state transition leaves stale authority | derived permission/cache not invalidated | transition test preserves old decision beyond intended state change | before/after transition under same fixture |

A hypothesis is useful only if it predicts an observable difference and names the policy dimension responsible for that difference.

## Decision trace

The **decision trace** is the causal backbone of the review.

Capture, where applicable:

```text
authenticated identity
-> normalized principal
-> tenant/workspace derivation
-> role/scope expansion
-> requested resource
-> authoritative resource resolution
-> decision input
-> enforcement point
-> decision
-> later transformation
-> final sink
```

### Decision input

Record the exact security-relevant values presented to the enforcement point:

```text
principal
operation
resource
context
policy revision
```

Do not substitute route parameters or display-layer fields when the policy function consumes normalized values.

### Enforcement point

Name the exact function, policy rule, repository constraint, or equivalent local boundary that produces the decision. If multiple enforcement points exist, record which one is authoritative and which ones are defense-in-depth.

### Final sink

The **final sink** is the protected effect represented in the local test or review: returned protected object, mutated synthetic row, synthetic export member, state transition, queued synthetic action, or policy-protected helper call.

The key comparison is:

```text
security meaning of decision input
==
security meaning of final sink
```

Literal identifiers may change through normalization, but the trace must show that the policy decision remains bound to the same principal/resource/context relation.

### Causal candidate

When the expected and actual result differ, name the smallest candidate cause supported by the trace:

- missing decision input;
- wrong principal;
- wrong resource;
- missing context dimension;
- incorrect policy composition;
- stale cached decision;
- post-decision resource change;
- lost delegation context;
- worker identity replacing caller-bound authority;
- alternate code path not converging on the authoritative policy layer.

Avoid broad labels when the trace supports a narrower cause.

## Controlled validation

Use local automated tests and synthetic fixtures wherever possible.

1. Freeze the application/policy revision under review.
2. Create synthetic principals whose roles, tenants, scopes, and delegation relationships are explicit.
3. Create paired synthetic resources with known ownership/tenant/state.
4. Establish an intended-allow positive control through the same policy API or code path.
5. Establish a neighboring intended-deny control.
6. Change one policy-relevant dimension at a time.
7. Record the decision input and final sink identity/resource in test instrumentation or assertions.
8. Exercise aggregate, batch, cache, worker, delegation, and lifecycle representations only when they share the same policy question.
9. Keep protected effects inert: assertions, synthetic marker state, mock calls, or isolated test data.
10. Stop once the causal policy mismatch is proven by the smallest safe fixture.

Do not use a failing integration path as an authorization oracle until the corresponding positive control proves the path itself is healthy.

## Counterfactual controls

A **counterfactual** predicts what should change if the suspected authorization defect were corrected while unrelated variables remain fixed.

### Neighboring control

A **neighboring control** should differ from the case under review by the smallest policy-relevant dimension practical.

Examples:

- same principal/operation/context, different authoritative owner;
- same resource/operation, different tenant membership;
- same delegated service/resource, different initiating principal;
- same cached tuple, different policy revision;
- same batch shape, one member changed from allowed to denied.

A control that changes many dimensions can still be useful, but it provides weaker causal isolation and should be described that way.

### Necessary-condition reasoning

If a test suggests tenant membership is a necessary condition, hold route, operation, resource shape, role, and other context constant while changing only authoritative tenant membership. Then inspect whether that dimension reaches the decision input.

The goal is not simply to obtain one allow and one deny. The goal is to connect the policy dimension to the decision mechanism.

### Sufficient-condition reasoning

Treat sufficiency claims conservatively. If a rule appears to say "owner + scope X may update," state the baseline assumptions and test likely competing restrictions such as tenant membership or lifecycle state. Otherwise a successful fixture may depend on hidden administrator state rather than the rule being reviewed.

### Alternative explanation

For every promoted finding, write at least one plausible **alternative explanation** and the local control that weakens it.

Common alternatives include:

- intended sharing/inheritance;
- implicit administrator/support role;
- test resource accidentally owned by the principal;
- stale fixture setup;
- documented eventual consistency;
- generic validation/lookup failure;
- duplicate or ambiguous identifiers;
- explicit service authority independent of the caller;
- lifecycle/approval state different from the assumed state.

Stronger evidence comes from excluding specific alternatives, not from stronger adjectives.

## False-positive controls

Use paired controls appropriate to the policy dimension:

- owner vs same-tenant non-owner;
- same-tenant vs different-tenant;
- allowed role vs lower role;
- full scope vs reduced scope;
- direct item vs aggregate representation;
- single item vs batch members;
- direct execution vs local worker fixture;
- before vs after synthetic revocation/state change;
- direct caller vs delegated caller;
- cold decision vs cached decision;
- current policy revision vs intentionally changed revision;
- canonical resource vs alias representation.

Do not promote a case while the observed difference can still be explained by an approved policy rule, fixture ownership mistake, stale test state, documented propagation delay, generic validation behavior, or an uncorrelated final sink.

A response-code difference or UI visibility difference is not by itself proof of an authorization defect. The protected decision/effect relation must be demonstrated in the local policy/test model.

## Evidence ladder

Use the smallest evidence state justified by the record.

### Hypothesis

Use when source/policy review suggests a possible defect but reachability or causal effect is unproven.

Record:

- policy source;
- suspected mechanism;
- exact missing evidence.

### Observed

Use when a controlled behavior difference is reproduced but the causal mechanism or final protected effect is incomplete.

Record:

- synthetic tuple;
- environment/revision;
- observation;
- neighboring control;
- unresolved alternative explanation.

### Validated

Use only when all are present:

- authoritative policy source establishes the expected decision;
- synthetic prohibited tuple reproducibly violates that decision in the local authorized fixture;
- decision trace identifies the relevant wrong/missing/stale decision input or enforcement relation;
- positive control proves path health;
- neighboring control or equivalent counterfactual isolates the policy dimension;
- material alternative explanations have been addressed for the scope of the claim.

### Regression verified

Use only after the fixed revision is checked with the original case plus neighbors. The prohibited tuple must now be denied for the intended policy reason, the allowed tuple must remain allowed, and relevant neighboring cases must preserve the expected policy.

## Evidence capture

Capture evidence in a form that preserves policy authority, causal trace, and controls:

```text
case_id:
application_revision:
policy_revision:
policy_source:
expected_decision:
principal:
operation:
requested_resource:
authoritative_resource:
context:
decision_input:
enforcement_point:
actual_decision:
post_decision_transformations:
final_sink:
positive_control:
neighboring_control:
counterfactual_prediction:
alternative_explanation:
alternative_explanation_control:
evidence_state:
causal_mechanism:
```

Prefer a causal statement such as:

> Policy source S denies tuple P/O/R/C. The policy helper receives P/O but resource ownership is absent from the decision input, so both owner and synthetic non-owner fixtures produce the same allow. A neighboring fixture that changes only ownership reproduces the same decision, while the positive owner control proves the path is healthy.

Avoid conclusions that omit the policy source, decision input, final sink, or controls.

## Remediation checks

Remediation should repair the invariant at the narrowest authoritative layer shared by relevant code paths.

Review whether the fix:

1. evaluates the complete principal-operation-resource-context relation;
2. derives resource/tenant identity from authoritative data;
3. keeps the authorized resource bound to the final sink;
4. preserves initiator context across delegation when policy requires it;
5. gives workers only the authority model intended by the policy contract;
6. applies member-level constraints after aggregate/batch expansion when required;
7. includes all policy-relevant dimensions in decision caches or invalidation;
8. invalidates derived authority on ownership, sharing, role, revocation, or lifecycle change;
9. converges alternate implementations of the same semantic operation on the same authoritative policy rule;
10. preserves useful audit correlation among principal, resource, decision, and local protected effect.

A route-specific conditional that blocks one fixture is not sufficient if the same invariant is implemented independently elsewhere.

## Remediation proof

Prove the fix against the original causal claim rather than only against the original request shape.

### Original denied case

Replay the synthetic tuple under the fixed revision. Confirm that the decision now follows the policy source because the corrected decision input or authoritative constraint is present.

### Original allowed case

The intended-allow positive control must still succeed. A change that blocks both cases is an availability change, not proof of correct authorization.

### Neighboring regression matrix

Choose neighbors based on the causal mechanism:

- ownership binding -> owner/non-owner;
- tenant binding -> same/different tenant;
- scope composition -> adjacent scope combinations;
- delegation -> approved/denied initiator or purpose;
- cache -> exact same tuple plus one changed policy dimension;
- batch -> all-allowed/mixed/all-denied synthetic members;
- lifecycle -> before/after approved state transition.

### Decision-trace confirmation

Inspect the fixed **decision input**, **enforcement point**, and **final sink**. The repaired trace should show that the previously missing or incorrect policy dimension now remains bound through the protected effect.

### Overfitting checks

Reject a remediation proof that depends on:

- a specific test account or resource identifier;
- disabling the whole feature;
- changing only UI visibility;
- changing only error text/status;
- adding one route guard while the shared policy layer remains incomplete;
- breaking documented sharing or delegation semantics.

### Residual scope

State exactly what was verified. If a changed repository layer covers reads and exports but a separate worker path was not part of the fix, say so. Precise residual scope is stronger than an unsupported universal claim.
