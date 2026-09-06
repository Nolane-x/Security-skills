---
name: cloud-iam-path-analysis
description: "Analyze cloud identity and authorization paths across principals, roles, policies, trust relationships, workload identity, service delegation, resource policies, and effective permissions in owned or explicitly authorized environments. Use for privilege-path review, least privilege, tenant isolation, or confused-deputy risks."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Cloud IAM Path Analysis

Cloud IAM analysis is graph reasoning over who can assume, pass, invoke, attach, modify, or act through another principal. Distinguish effective permissions from hypothetical chains that fail an intermediate condition.

## When to use

Use for cloud accounts/projects/subscriptions, Kubernetes-to-cloud workload identity, CI/CD roles, service principals, cross-account trust, resource policies, or delegated managed services.

## Preconditions

Use only owned accounts or explicit authorization. Prefer policy simulation/read-only inventory and synthetic resources; do not exercise destructive privileges or access real third-party data.

## Workflow

1. **Inventory principals.** Human, workload, service account, role, federated subject, managed service.
2. **Inventory policy sources.** Identity policy, resource policy, trust/assume policy, org/SCP/deny controls, permission boundaries, session policy.
3. **Normalize actions/resources/conditions.** Wildcards, tags, regions, source identities, audience, external id, network/source constraints.
4. **Build privilege edges.** Assume/delegate/pass role, create/update policy, attach role, invoke service, create workload with identity, modify trust.
5. **Compute effective path step-by-step.** Every edge must satisfy allow and absence of overriding deny plus conditions.
6. **Check confused-deputy controls.** Service delegation must bind source account/resource/audience/context.
7. **Check privilege-management rights.** Ability to edit policy/trust often dominates direct action lists.
8. **Check workload/secret coupling.** Who can deploy code into a principal or read tokens that represent it?
9. **Validate with policy simulation or synthetic no-op resource** when possible.
10. **Produce minimal privilege remediation** that breaks dangerous paths without unrelated access loss.

## Evidence contract

A privilege path is validated only when every edge has concrete effective permission and relevant conditions are satisfied. Preserve source policy statements/ids, denies/boundaries, path, synthetic validation, and assumptions.

## Stop conditions

Stop if account ownership/authorization is unclear, validation would access real sensitive resources, policy snapshots are stale/incomplete, or an intermediate edge is only speculative.

## Output

```text
source principal:
target capability:
policy sources:
validated privilege path:
conditions/denies:
delegation/confused-deputy controls:
workload/token coupling:
synthetic validation:
minimal path-breaking remediation:
```
