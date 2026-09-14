---
name: cloud-iam-path-analysis
description: "Analyze cloud identity and authorization paths across principals, roles, policies, trust relationships, workload identity, service delegation, resource policies, and effective permissions in owned or explicitly authorized environments. Use for privilege-path review, least privilege, tenant isolation, or confused-deputy risks."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Cloud IAM Path Analysis

Cloud IAM analysis is not a search for isolated `Allow` statements. It is reasoning about whether a principal can obtain a specific capability through a sequence of identity, policy, delegation, workload, resource, and session transitions **under the provider's actual authorization semantics**.

A path is only as strong as its weakest edge. If one edge depends on an unsatisfied trust condition, an overriding explicit deny, a maximum-permission ceiling, an incompatible session context, a stale policy snapshot, or a merely hypothetical policy mutation, the whole path remains unvalidated.

## When to use

Use for cloud accounts/projects/subscriptions, Kubernetes-to-cloud workload identity, CI/CD identities, service principals, cross-scope trust, resource policies, managed-service delegation, federation, session policies, role chaining, or reviews of who can change IAM itself.

Use this skill when the security question involves **effective authority**, not only policy syntax. Examples include:

- whether a principal can actually assume or receive another identity;
- whether identity and resource policies compose to permit a capability;
- whether organization controls, permission boundaries, session policies, or equivalent controls cap an apparent grant;
- whether workload identity maps the intended external subject to the intended cloud principal;
- whether a managed service remains bound to the initiating account/resource/context;
- whether policy-management rights create a future authority state that is materially different from current direct permissions;
- whether session lifetime, revocation, tags/claims, audience, source identity, region, or other conditions change the decision.

## Preconditions

Use only owned accounts/projects/subscriptions/tenants, dedicated sandboxes, benchmark fixtures, or explicitly authorized development environments. Prefer read-only inventory, provider policy simulation/explain tools, normalized policy models, synthetic principals/resources, and inert assertions.

Do not use production secrets, unrelated tenants, real third-party identities/data, destructive administrative actions, or guardrail removal to prove a path.

Freeze the policy and identity snapshot before drawing a conclusion. Cloud IAM is temporal: group membership, role bindings, trust, policy versions, session issue time, session expiry, revocation state, workload claims, organization controls, and resource policy may change independently.

## Effective authorization model

Represent each candidate edge as a decision problem rather than as an arrow inferred from policy text.

```text
source principal P
requested transition/capability A
subject or target T
resource/scope R
session context C
policy sources S
edge preconditions Q
-> effective decision D
```

The exact composition rule is provider-specific. Do not impose one universal algebra on AWS, Azure, GCP, Kubernetes federation, or other systems. Instead, normalize the concepts below and then apply the provider's authoritative precedence rules.

### Policy source

A **policy source** is any authority that contributes to the decision: identity policy or role assignment, resource policy, trust policy, organization/folder/account control, permission boundary or equivalent maximum-permission rule, session policy, key policy, federation mapping, service-delegation policy, conditional-access rule, or another provider-defined layer.

Record which source grants, limits, conditions, or denies the edge. A path report that cites only granting statements is incomplete when restrictive layers exist.

### Explicit deny

Treat an **explicit deny** as a first-class fact according to the provider's documented precedence. Do not infer that a positive grant wins because it is more specific, attached later, or appears closer to the target resource unless the provider semantics actually say so.

A deny that is outside the evaluated policy universe is not relevant; a deny that is applicable and authoritative must not be silently discarded. The analysis must state why a restrictive rule applies or does not apply.

### Maximum permission

A **maximum permission** control is a ceiling on what an identity/session can effectively obtain, such as a permission boundary, organization guardrail, maximum role scope, or analogous provider construct. It is not another positive grant.

Distinguish:

- a policy that grants a capability;
- a policy that permits a capability to be granted up to a ceiling;
- a policy that denies the capability;
- a condition that makes an otherwise applicable rule inactive.

Confusing these categories is a major source of false-positive privilege paths.

### Trust condition

An assumption, federation, workload-identity, or delegated-service edge usually has a **trust condition** in addition to an action permission. Normalize the complete trust tuple: intended issuer/source, subject/principal, audience or recipient, source scope/resource, external/context identifier, claim/tag requirements, and any provider-specific condition that materially changes acceptance.

A source principal having an assume/delegate-like action does not prove the target will trust that source.

### Session context

The **session context** is the authority-bearing state produced or used at an edge: session policy, tags/claims, source identity, delegated subject, authentication context, issue time, expiry, chain depth, revocation semantics, and provider-specific attributes.

Do not assume that permissions attached to a long-lived principal automatically survive unchanged inside a derived session. Conversely, do not assume a later policy edit immediately changes an already issued session unless the provider semantics say it does.

### Edge precondition

An **edge precondition** is a fact that must be true for the transition to exist. Examples include applicable source permission, target trust, required condition values, resource match, current session validity, workload-claim match, organization scope, service-specific prerequisites, or permission to change the policy state that the next edge depends on.

Write preconditions explicitly. Hidden preconditions make an IAM graph look more powerful than the real authorization system.

### Effective decision

The **effective decision** is the result after all relevant policy sources, restrictive controls, conditions, trust requirements, resource/scope matching, session context, and provider precedence rules are considered.

Prefer authoritative provider simulators/explain APIs or a validated local model. Where a simulator is incomplete, state exactly which policy layers or runtime conditions it does not model and keep the edge at a lower evidence state.

## Path reasoning discipline

1. **Prove edges before paths.** Never infer a multi-edge capability because each policy document looks permissive in isolation. Every edge must have a stated effective decision and satisfied edge precondition.
2. **Do not assume transitivity.** If A can use B and B can use C, it does not automatically follow that A can use C. The B→C decision may depend on B's original identity, session tags, source identity, issue mechanism, chain depth, resource context, or time.
3. **Separate present authority from authority-changing capability.** Permission to edit a policy, workload binding, trust relationship, or deployment definition is an edge that can create a new graph state. It is not identical to already possessing the future target capability. Model the state transition explicitly.
4. **Evaluate restrictive layers before promoting a path.** Explicit deny, organization controls, permission boundaries, session policy, resource conditions, and service-specific limits can invalidate an apparent allow chain.
5. **Bind trust to the complete subject context.** Federation and delegation are not proven by issuer alone or role name alone. Record the complete trust condition and the claims/context actually evaluated.
6. **Keep session state temporal.** A path requiring one session before revocation and another policy state after revocation may be impossible even though both facts appear in a static inventory. Edge states must be mutually compatible in time.
7. **Distinguish principal identity from code/config influence.** Ability to modify code or configuration executed by a stronger workload may be security-relevant, but the causal path must explain how that influence becomes an authority-bearing effect rather than labeling every deployment permission as direct privilege.
8. **Treat resource policy as part of the same decision.** Do not analyze identity policy and resource policy as unrelated findings when the provider composes them for one effective authorization result.
9. **Use a counterfactual for causal claims.** Change one decision-relevant dimension—trust claim, boundary, deny, resource, session tag, source scope, or policy revision—and predict which edge should disappear while intended neighboring paths remain.
10. **Search for alternative explanations.** Stale inventory, inherited membership, provider implicit behavior, simulator blind spots, eventual consistency, session reuse, policy-version mismatch, resource aliasing, and intentionally broad managed-service authority can all explain an apparent path.
11. **Stop at the first speculative edge.** The remainder of a chain after an unproven edge is a hypothetical continuation, not a validated path.
12. **Use the smallest evidence state that fits.** A visually convincing graph is not stronger evidence than the policy composition supporting its edges.

## Workflow

1. **Freeze scope and time.** Record provider, account/project/subscription/tenant, policy revisions/snapshots, identity-provider configuration, organization controls, and relevant session times.
2. **Normalize principals.** Resolve users, groups, roles, service/workload identities, federated subjects, managed services, deployment identities, and delegated initiators into explicit nodes.
3. **Normalize policy sources by semantic role.** Separate positive grants, resource grants, trust rules, explicit denies, maximum-permission controls, session restrictions, conditions, and service-specific delegation rules.
4. **Define the target capability.** State the semantic action and authoritative resource/scope being reasoned about. Avoid vague targets such as "admin" when the actual question is a narrower capability.
5. **Build candidate edges with preconditions.** For every edge record source, target/capability, policy sources, resource scope, trust condition, session context, and unresolved assumptions.
6. **Compute the effective decision for each edge.** Apply the provider's documented policy composition, including restrictive layers and conditions. Mark unknown semantics as unresolved rather than guessing.
7. **Check temporal compatibility.** Verify that all edge facts can hold in the same relevant policy/session state.
8. **Model authority-changing edges as state transitions.** If an edge depends on changing policy/trust/workload configuration, represent the before/after state and evaluate the next edge only in the resulting synthetic model.
9. **Trace workload and delegation binding.** Preserve initiating subject, executor identity, workload claims, purpose/source context, and any derived session attributes that policy depends on.
10. **Use policy simulation/explain evidence first.** Note simulator coverage and blind spots explicitly.
11. **Use only bounded synthetic confirmation where needed.** Prefer sandbox fixtures, synthetic resources, test identities, and inert markers; avoid production effects.
12. **Construct neighboring controls.** Remove or change one required precondition and confirm the expected edge disappears while the intended edge remains.
13. **Promote the path only when every required edge is effective.** One unresolved edge keeps the path unresolved.
14. **Remediate by breaking the causal path at the narrowest reliable control.** Preserve intended neighboring paths and recompute the entire path after the fix.

## Operator depth

For a full review, load the [operator runbook](references/operator-runbook.md). It expands this model into provider-aware effective-permission semantics, edge proof records, path causality, policy-layer composition, trust/session reasoning, counterfactual controls, false-positive analysis, evidence thresholds, and path-breaking remediation proof.

The [operator scenarios](references/operator-scenarios.json) preserve the existing three scenario classes while adding explicit edge preconditions, path causality, false-positive guards, evidence-upgrade criteria, and neighboring regression requirements.

## Evidence ladder

### Hypothesis

Use when normalized policy sources suggest a candidate edge/path but one or more effective decisions, conditions, session states, or provider semantics remain unresolved.

State the exact unresolved edge precondition. Do not summarize the whole chain as reachable when the missing proof is in the middle.

### Observed

Use when an authoritative simulator/explain tool or controlled local/sandbox fixture establishes at least one meaningful edge, but the whole target path or causal mechanism is incomplete.

Record which edge is observed, which path edges remain modeled only, and any simulator coverage limitation.

### Validated

Use only when:

- every required edge has an effective decision supported by authoritative policy semantics;
- every edge precondition is satisfied in a mutually compatible policy/session state;
- applicable explicit deny and maximum-permission controls have been evaluated;
- trust condition and session context are bound where relevant;
- the target capability is demonstrated through a bounded synthetic oracle when static/simulator evidence alone is insufficient;
- neighboring controls isolate material conditions and plausible alternative explanations are addressed.

A path does not become validated because the final capability is high impact. Evidence completeness, not impact, controls promotion.

### Regression verified

Use only after the remediation is evaluated against the complete original path. The chosen path-breaking control must invalidate the intended dangerous edge/path, intended neighboring paths must remain effective, and no equivalent alternate edge in the reviewed scope may reconstruct the same target capability without being analyzed.

## Evidence contract

A strong IAM path finding states:

> Under policy snapshot S and session context C, source principal P can reach target capability T through ordered edges E1..En. For each Ei, the contributing policy sources, edge preconditions, effective decision, restrictive layers, and trust/session conditions are recorded. Counterfactual control K removes decision-relevant condition Q and breaks edge Ej while the intended neighboring path remains effective. Alternative explanation Z is excluded by control R.

Preserve enough normalized policy identifiers/statements, condition values, decision outputs, timestamps, and assumptions for another reviewer to reconstruct the result.

## Stop conditions

Stop or downgrade when:

- ownership/authorization is unclear;
- the policy snapshot is stale or materially incomplete;
- provider precedence semantics for a required edge cannot be established;
- an intermediate edge remains speculative;
- the required edge states cannot coexist in one session/policy timeline;
- a simulator does not cover a material policy layer and no safe authorized oracle is available;
- validation would require real sensitive data, real third-party identities, production IAM mutation, guardrail removal, or destructive capability use;
- the apparent path is explained by an intended managed-service, federation, delegation, or session rule.

## Output

```text
case_id:
provider_and_scope:
inventory_timestamp:
policy_snapshot_or_revision:
source_principal:
target_capability:
ordered_path_edges:
per_edge_policy_sources:
per_edge_preconditions:
per_edge_effective_decision:
explicit_denies:
maximum_permission_controls:
trust_conditions:
session_context:
temporal_compatibility:
resource_policy_composition:
workload_or_delegation_binding:
policy_simulator_coverage:
positive_control:
neighboring_negative_control:
counterfactual:
alternative_explanations_checked:
bounded_synthetic_oracle:
evidence_state:
causal_path_summary:
path_breaking_remediation:
neighboring_regression_paths:
```
