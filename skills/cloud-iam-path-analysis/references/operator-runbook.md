# Cloud IAM Path Operator Runbook

Use this runbook only in dedicated sandbox cloud accounts/projects/subscriptions, owned environments, benchmark fixtures, or environments covered by explicit authorization. Prefer read-only inventory, policy simulation, synthetic resources, fake data, and no-op actions. Do not use production secrets or exercise destructive privileges to prove a path.

The objective is to distinguish a theoretical permission chain from a reachable effective-authorization path whose every edge is supported by current policy, conditions, identity state, and controlled evidence.

## Attack surface

Build a normalized graph with principal, policy, delegation, resource, workload, token, and organization-control nodes.

### Principal inventory

Include:

- human users and groups;
- roles and service accounts/service principals/managed identities;
- workload identities from compute, containers, Kubernetes, CI/CD, and serverless runtimes;
- federated subjects from OIDC/SAML/external identity providers;
- managed cloud services acting on behalf of customers;
- automation and deployment identities;
- break-glass/admin identities in the sandbox if explicitly in scope.

For each principal record account/project/subscription/tenant, authentication mechanism, role/group attachments, federation issuer/audience/subject constraints, session duration, tags/attributes, and where credentials/tokens can be obtained.

### Policy sources

Normalize all policy layers that can affect an action:

- identity-based policies/role assignments;
- resource-based policies and ACLs;
- role trust/assume policies;
- organization/folder/account guardrails such as explicit deny/SCP-like controls;
- permission boundaries or equivalent maximum-permission constraints;
- session policies;
- conditional access/attribute conditions;
- key-management policies;
- service-specific delegation policies;
- network/source/resource conditions that participate in authorization.

Record explicit denies and constraints as first-class graph edges; an apparent allow path is not effective if a higher-precedence deny or unsatisfied condition blocks it.

### Privilege-changing edges

Pay special attention to permissions that can change authority rather than directly access data:

- assume/delegate/pass-role operations;
- modify trust relationships;
- attach/create/update policies or role bindings;
- create workloads that run as a stronger identity;
- modify CI/CD or deployment definitions tied to a stronger identity;
- alter federation mappings or workload identity bindings;
- write to code/artifacts/config consumed by a privileged workload;
- read tokens/credentials representing another principal;
- alter resource policies, key policies, or service delegation settings.

### Resource and data surfaces

Map synthetic storage, secrets, keys, queues, databases, functions, compute, registries, and administrative APIs used as proof targets. Keep proof resources isolated from production and populate them only with unique non-sensitive markers.

## Hypothesis matrix

| Hypothesis class | Required reasoning | Controlled proof |
| --- | --- | --- |
| direct excess permission | principal → action → resource | policy simulator plus inert action on synthetic resource |
| role-assumption path | source → trust condition → target role | sandbox session is issued only when every trust condition is satisfied |
| pass/delegate-role escalation | caller can bind stronger identity to workload/service | synthetic workload receives target sandbox identity under controlled configuration |
| policy-management escalation | principal can change its own/effective authority | sandbox policy change grants only a benign marker permission and is reverted |
| federation over-breadth | issuer/audience/subject mapping accepts unintended synthetic subject | test identity from an adjacent fixture obtains sandbox-only session unexpectedly |
| confused deputy | managed service fails to bind source/resource/customer context | controlled service action crosses between two synthetic source contexts |
| resource-policy bypass | resource policy grants capability absent from identity policy | synthetic resource is reachable only through the resource-policy edge |
| deny/boundary oversight | modeled allow path ignores explicit deny or maximum boundary | simulator/authorization result proves the path is blocked, preventing a false positive |
| condition mismatch | tags, region, source identity, audience, network, or resource attributes differ | paired synthetic condition values produce expected allow/deny results |
| workload/code-to-identity coupling | actor can modify code/config executed under stronger identity | inert marker emitted by controlled workload demonstrates the boundary without reading secrets |
| token/session lifetime gap | revoked/changed authority persists through session semantics | test session behavior is measured against documented sandbox revocation expectations |
| cross-scope trust | account/project/subscription/tenant boundary trusts unintended principal | adjacent synthetic scope obtains a bounded marker capability |

Every hypothesis must list each edge and the exact precondition needed for that edge to exist. Do not collapse a multi-edge chain into “principal can become admin” unless all intermediate edges are effective and reachable.

## Controlled validation

1. **Freeze inventory.** Capture cloud scope identifiers, policy revisions or snapshots, organization controls, identity-provider configuration, relevant service settings, and the current time because conditions/session expiry can matter.
2. **Normalize identities.** Resolve group membership, role attachments, federation claims, workload bindings, and delegation relationships into explicit principals.
3. **Compute candidate paths statically.** Include allows, denies, boundaries, trust conditions, resource policy, and service-specific prerequisites. Mark unresolved edges as hypotheses.
4. **Use provider policy simulators/read-only explain tools first.** Preserve simulator inputs and outputs; note where a simulator cannot model resource policy, organization policy, service delegation, or runtime context.
5. **Create synthetic proof resources.** Use dedicated sandbox objects with unique markers and permissions that have no value outside the test.
6. **Validate one edge at a time.** For assumption/delegation, prove session issuance; for resource access, prove only the synthetic marker action; for policy modification, grant a minimal temporary marker permission and restore the original state.
7. **Validate conditions explicitly.** Pair condition-satisfying and condition-failing synthetic requests so the result is not attributed to a broader grant incorrectly.
8. **Trace effective identity.** Record the principal/session actually used at every edge, including session policy, tags/claims, source identity, and expiry.
9. **Validate workload coupling safely.** If code/config write is part of the path, use a sandbox workload whose only privileged behavior is writing a benign marker to a dedicated test sink.
10. **Check cross-scope boundaries with paired fixtures.** Use two sandbox accounts/projects/subscriptions/tenants where possible; never substitute unrelated real tenants.
11. **Restore state.** Remove temporary role bindings, policy statements, workloads, federation mappings, and synthetic resources created for validation.
12. **Stop when an edge is speculative.** Record the blocked/unproven edge rather than assuming the remainder of the chain.

Do not prove privilege paths by reading production secrets, modifying production IAM, disabling guardrails, or invoking destructive administrative actions.

## False-positive controls

Cloud IAM analysis is especially vulnerable to false positives from incomplete policy composition. Use controls that test the whole effective decision:

- allowed action versus adjacent denied action on the same synthetic resource;
- identity policy alone versus identity + resource policy evaluation;
- candidate allow with explicit deny present versus equivalent fixture without the deny;
- session inside versus outside required tag/audience/source/resource conditions;
- intended federated subject versus adjacent synthetic subject;
- source account/project A versus synthetic neighboring source B;
- role assumption with correct external/context binding versus missing/wrong binding;
- direct principal versus delegated managed service path;
- policy simulator result versus bounded runtime validation where safe;
- newly issued session versus an older session when testing revocation/lifetime semantics;
- principal that can edit a policy versus principal that can only read it;
- workload configuration write with strong execution identity versus equivalent workload using a low-authority test identity.

Reject or downgrade paths caused by stale inventory, inherited roles omitted from the model, organization-level deny not captured, provider-specific implicit permissions, simulator limitations, eventual consistency inside a documented window, or synthetic resource policy that does not match the target architecture.

An IAM graph edge is not validated merely because a policy statement contains an allow. Effective authorization requires all relevant policy layers and runtime conditions.

## Evidence capture

For each candidate or validated path preserve:

```text
case_id:
cloud_provider_and_scope:
inventory_timestamp:
source_principal:
source_authentication_method:
target_capability:
path_edges_in_order:
identity_policy_sources:
resource_policy_sources:
trust_policy_sources:
organization_denies_or_guardrails:
permission_boundary_or_max_scope:
session_policy:
conditions_and_claims:
federation_issuer_audience_subject:
per_edge_effective_decision:
policy_simulation_evidence:
synthetic_runtime_validation:
effective_identity_per_edge:
session_expiry_or_lifetime:
positive_control:
negative_control:
restoration_record:
evidence_state:
```

Classify evidence conservatively:

- **hypothesis:** policy composition suggests a candidate path;
- **observed:** at least one relevant edge is reproduced in the sandbox;
- **validated:** every required edge is effective and a bounded synthetic target capability is demonstrated with controls;
- **regression-verified:** remediation breaks the dangerous path while intended neighboring access remains functional.

Keep policy identifiers and normalized statements where possible so another reviewer can reconstruct the effective decision without relying on a screenshot or agent assertion.

## Remediation checks

Break the path at the smallest reliable control point while preserving required workflows.

Evaluate:

1. **Least-privilege actions/resources:** remove wildcards and unrelated management actions; scope synthetic regression tests to the exact intended resource classes.
2. **Trust restriction:** bind role/service assumption to intended principals, issuer, audience, subject, source scope, external/context identifiers, and resource conditions.
3. **Privilege-management separation:** restrict who can attach/update policies, role bindings, trust policies, federation mappings, and organization controls.
4. **Pass/delegate-role constraints:** constrain which identities may be attached to workloads/services and which callers may create or modify those workloads.
5. **Guardrails:** add permission boundaries, explicit denies, organization policies, or equivalent maximum-scope controls where independent containment is required.
6. **Workload isolation:** prevent low-authority actors from modifying code/config/artifacts executed by stronger identities unless that delegation is intentional and reviewed.
7. **Resource-policy alignment:** ensure identity and resource policies agree on tenant/account/project boundaries and do not create unintended alternate grants.
8. **Federation hardening:** use exact issuer/audience/subject/claim mappings and short-lived sessions appropriate to the workload.
9. **Session lifecycle:** define rotation/revocation expectations and avoid long-lived credentials when short-lived workload/session identity is available.
10. **Audit correlation:** log role assumption/delegation, policy changes, resource-policy changes, workload identity changes, and the initiating principal.

Regression verification must recompute the entire original path after the fix, not only inspect the edited policy. Replay the original synthetic path, an intended allowed neighboring path, and at least one denied adjacent identity/condition. A remediation is incomplete if another equivalent privilege-changing edge still reaches the same target capability.
