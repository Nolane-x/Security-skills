---
name: authorization-boundary-analysis
description: "Analyze who is allowed to perform an operation, which identity and attributes are checked, where policy is enforced, and whether alternate paths bypass or weaken authorization. Use for APIs, helpers, admin functions, object-level access control, scoped tokens, service IPC, or multi-tenant resources."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Authorization Boundary Analysis

Authorization is not a property of a request. It is a decision about a specific relation: **which principal may perform which operation on which resource, under which context, according to which policy source**. A review is incomplete if it proves only that a route contains a check; it must establish that the check receives the correct decision inputs and that the same authorized tuple reaches the final sink.

## When to use

Use this skill when a lower-privileged, differently scoped, delegated, service, tenant, or lifecycle-dependent principal may reach an operation intended for another identity, role, tenant, object, capability, or state.

Typical signals include object identifiers supplied by callers, tenant or workspace switching, role-dependent actions, OAuth/API-token scopes, delegated or on-behalf-of calls, privileged helpers, background jobs, cached policy decisions, batch operations, exports, alternate routes, ownership transitions, and any path where the identity checked at one layer may differ from the identity or resource used later.

Do not treat a different HTTP status, hidden UI control, route name, or role label as proof of an authorization boundary. Those are observations about presentation or transport. The policy relation must be derived from an authoritative source and traced to the protected effect.

## Preconditions

Test only local, owned, sandboxed, benchmark/CTF, or explicitly authorized systems. The authorization must cover the identities, resources, operations, lifecycle changes, and execution paths being exercised.

Prefer synthetic principals and synthetic resources with unmistakable markers. Use inert reads, no-op mutations, policy simulator decisions, mocked privileged boundaries, or dedicated test objects. Do not use real third-party identities or data to prove a boundary failure.

Before testing, identify the **policy source** that defines the expected decision. Acceptable sources include an owner-approved product requirement, access-control specification, policy-engine configuration, explicitly approved ownership rule, regression test oracle, or other authoritative contract. If no authoritative policy can be established, record a policy ambiguity rather than manufacturing an expected allow/deny result from observed behavior.

## Decision model

Model each authorization question as a tuple:

```text
principal P
operation O
resource R
context C
policy source S
-> expected decision D_expected
```

Then trace the implementation as a causal chain:

```text
ingress identity
-> normalized principal
-> resource resolution
-> context derivation
-> decision input
-> enforcement point
-> post-decision transformations
-> final sink
```

The central question is not merely "was there an authorization check?" It is:

> Did the authoritative policy evaluate the same principal, operation, resource, and context that ultimately reached the protected effect?

Treat these elements separately:

- **Principal:** the security subject whose authority should constrain the action. Distinguish the authenticated user, delegated initiator, service identity, worker identity, support impersonator, API client, and any privileged deputy. A service credential does not erase the caller whose authority the service is supposed to represent.
- **Operation:** the semantic action after routing and normalization, not only the HTTP verb or method name. `POST /items/export`, a GraphQL mutation, a queue message, and an internal RPC may all represent the same protected operation.
- **Resource:** the authoritative object or object set actually read, changed, exported, approved, restored, or otherwise acted upon. Distinguish the caller-supplied identifier from the resolved object and from the resource at the final sink.
- **Context:** every policy-relevant state dimension, such as tenant, workspace, ownership, role, token scope, authentication strength, delegation purpose, approval state, resource lifecycle, region, feature state, or revocation status.
- **Policy source:** the authority that defines what should happen. Implementation behavior is evidence about enforcement, not automatically the policy itself.
- **Enforcement point:** the location where an allow/deny decision is made or where an invariant is structurally enforced, such as a policy engine, service method, tenant-scoped repository, row filter, privileged helper boundary, or message consumer.
- **Final sink:** the protected effect that matters: the data returned, row mutated, file exported, permission changed, task executed, approval recorded, or other security-relevant outcome.

A boundary defect exists only when the observed implementation violates the expected policy relation. A missing check is one possible mechanism; wrong identity propagation, resource substitution, stale context, incomplete scope composition, cache reuse, delegation confusion, and post-check transformation are equally important mechanisms.

## Reasoning discipline

Authorization analysis should proceed as causal reasoning, not as a collection of suspicious differences.

1. **Separate expected policy from implementation.** First write why the tuple should be allowed or denied and name the policy source. Only then compare implementation behavior. Otherwise the test risks treating an undocumented product choice as a vulnerability.
2. **Change one policy dimension at a time.** A useful negative control differs from the positive control in one relevant dimension whenever possible: principal, resource, tenant, operation, scope, lifecycle state, delegation purpose, or another explicit context field. If five dimensions change simultaneously, a denial proves little about which invariant is working.
3. **Distinguish necessary from sufficient conditions.** Showing that removing role `admin` causes denial may show that the role is necessary for one path; it does not prove that the role alone is sufficient, that object ownership is ignored, or that alternate paths share the same semantics.
4. **Trace identity and resource after the decision.** An apparently correct enforcement point is insufficient if the authorized resource is later replaced, canonicalized differently, expanded into a batch, loaded under another tenant, or executed by a worker using broader authority.
5. **Use a counterfactual.** Ask what should change if the suspected missing or incorrect decision input were corrected while all unrelated variables remain fixed. The counterfactual should predict both the denied case becoming blocked and the neighboring allowed case continuing to work.
6. **Actively search for alternative explanations.** Sharing rules, administrator inheritance, eventual-consistency windows, test-fixture ownership, soft-delete behavior, stale setup, duplicate identifiers, cache warmness, and delegated semantics can all explain an apparent boundary crossing without a policy defect.
7. **Do not equate information leakage with protected access.** A distinguishable `404`/`403`, object existence hint, count, timing difference, or search metadata may deserve separate analysis, but it is not proof that the protected object can be read or modified.
8. **Do not promote evidence by confidence alone.** A reviewer may be highly confident that source code is wrong and still have only a hypothesis if reachability and protected effect have not been established.

## Workflow

1. **Name the policy source.** Write the authoritative rule before probing behavior. If the rule is ambiguous, stop the vulnerability claim and resolve semantics with the owner.
2. **Normalize the decision tuple.** Record principal, semantic operation, authoritative resource, context, and expected decision. Explicitly distinguish caller-supplied values from authoritative values.
3. **Map principal transformations.** Follow authentication, session hydration, role/group expansion, tenant selection, token-scope interpretation, delegation, internal RPC metadata, worker identity, and privileged helper credentials.
4. **Map resource transformations.** Follow aliases, canonical identifiers, parent-child resolution, lookup filters, tenant binding, caches, indexes, batch expansion, export materialization, attachment indirection, and lifecycle transitions.
5. **Locate every enforcement point.** Identify where the policy is checked or structurally constrained and which exact decision input each point consumes.
6. **Establish a canonical positive control.** Prove that an intended allowed tuple reaches the benign final sink. A broken positive control invalidates later denials because the path itself may be nonfunctional.
7. **Establish a neighboring negative control.** Change the smallest policy-relevant dimension that should cause denial. Confirm that the same path and final sink are otherwise comparable.
8. **Trace decision-to-sink continuity.** Compare the principal/resource/context used at the enforcement point with the values present at the final sink. Any change after authorization is a candidate binding defect.
9. **Exercise alternate representations only after the baseline is known.** Compare item versus list/search/export, single versus batch, synchronous versus queued, public versus internal route, current versus legacy route, and direct versus delegated execution while preserving the same policy question.
10. **Test state transitions as policy transitions.** For synthetic resources, vary ownership, membership, role, sharing, revocation, archive/restore, approval, and token refresh state. Record when the policy is supposed to change and when each representation actually changes.
11. **Test caches and asynchronous paths with explicit semantics.** Determine whether authorization is intentionally captured at enqueue time, re-evaluated at execution time, or delegated to a narrow service role. Determine which context dimensions participate in cache identity and invalidation.
12. **Stop at the first bounded causal proof.** Once a synthetic prohibited tuple reaches the protected benign effect for a demonstrated authorization reason, preserve the evidence and do not broaden into real data or unrelated identities.
13. **Remediate the invariant, not the symptom.** Prefer the narrowest authoritative layer shared by all relevant paths. Do not special-case a route, identifier, or test account if the underlying principal-resource-context relation remains wrong elsewhere.
14. **Prove the fix with neighbors.** Replay the original denied tuple, the original allowed control, and adjacent allow/deny cases. A fix that blocks everything is not an authorization fix; it is an availability regression.

## Operator depth

For a full authorized review, load the [operator runbook](references/operator-runbook.md). It expands the model into policy semantics, decision traces, controlled identity/resource lattices, counterfactual controls, evidence thresholds, cache and asynchronous semantics, delegation analysis, aggregate/batch parity, lifecycle transitions, and remediation proof.

The machine-readable [operator scenarios](references/operator-scenarios.json) bind three representative failure mechanisms to safe oracles, causal traces, false-positive guards, evidence-upgrade criteria, and neighboring regression requirements.

## Evidence ladder

Use the smallest claim justified by the evidence.

### Hypothesis

Use when the policy source and implementation suggest a possible boundary defect, but the protected path or effect has not been demonstrated. Examples include a route that appears to omit a check, an incomplete cache key visible in code, or identity metadata that seems to be dropped before an internal call.

A hypothesis should state the suspected mechanism and the missing proof. Do not write "authorization bypass" when the current evidence is only "this path may fail to bind tenant identity after resource lookup."

### Observed

Use when a controlled behavior difference has been reproduced, but causality or protected effect is incomplete. Examples include a prohibited request reaching deeper into the stack, a policy simulator receiving an unexpected tuple, or a stale decision being observed without yet proving that the final protected sink uses it.

Record the exact observation and at least one neighboring control. Keep alternative explanations open.

### Validated

Use only when all of the following are present:

- an authoritative policy source establishes that the tuple is prohibited;
- the prohibited synthetic tuple is reproducibly accepted or reaches the protected benign effect;
- the decision trace identifies the relevant enforcement absence, wrong decision input, stale decision, or principal/resource/context binding failure;
- an allowed positive control demonstrates path health;
- a denied neighboring control or other counterfactual isolates the authorization dimension;
- plausible alternative explanations have been ruled out to the degree required for the claim.

A validated finding does not require destructive impact. A synthetic marker at the protected sink is enough when it proves the prohibited policy relation.

### Regression verified

Use only after the fixed revision is tested. The original prohibited tuple must be denied for the intended authorization reason, the original allowed tuple must still succeed, neighboring allow/deny cases must preserve policy semantics, and relevant alternate paths must no longer reproduce the causal mechanism.

If the fix works only for one route while batch/export/worker/helper paths still carry the defective relation, the finding is not regression verified.

## Evidence contract

A strong finding is a causal statement, not merely a request/response transcript:

> Under policy source S, principal P must not perform operation O on resource R in context C. At enforcement point E, decision input X omits or misbinds policy-relevant dimension Y. The prohibited synthetic tuple therefore reaches final sink F. Positive control A proves the path is healthy; neighboring control B isolates Y; alternative explanation Z is excluded by control C.

Preserve both the expected-policy evidence and the implementation evidence. If the policy source changes during testing, restart the decision comparison against the new authority rather than mixing observations from two policy revisions.

## Stop conditions

Stop or downgrade the claim when any of these conditions applies:

- the expected authorization semantics cannot be established from an owner-approved policy source;
- the next step would require real third-party identities, data, or unauthorized operations;
- the test cannot distinguish an authorization decision from generic lookup, validation, transport, or availability behavior;
- the behavior is explained by an approved delegation, sharing, inheritance, or eventual-consistency rule;
- the positive control is broken, making the negative result uninterpretable;
- the resource or identity at the final sink cannot be correlated with the one used at the enforcement point;
- the only remaining way to demonstrate impact would be destructive or unnecessary once a benign synthetic proof already exists.

## Output

```text
case_id:
policy_source:
policy_revision:
expected_decision:
principal:
principal_translation_chain:
operation_semantics:
requested_resource:
authoritative_resource:
context:
decision_input:
enforcement_point:
policy_decision:
post_decision_transformations:
final_sink:
principal_at_final_sink:
resource_at_final_sink:
positive_control:
neighboring_negative_control:
counterfactual:
alternative_explanations_checked:
benign_effect_or_marker:
evidence_state:
causal_mechanism:
remediation_invariant:
regression_neighbors:
```
