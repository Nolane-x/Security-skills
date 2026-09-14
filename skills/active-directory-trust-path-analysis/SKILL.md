---
name: active-directory-trust-path-analysis
description: "Review Active Directory identity and authorization trust paths in owned or explicitly authorized environments, including forests/domains, groups, directory permissions, delegation, service identities, Kerberos/LDAP policy, GPO scope, and certificate-backed identity mappings. Use read-only inventory and synthetic lab validation to distinguish intended administration from unintended authority paths."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Active Directory Trust Path Analysis

Treat enterprise identity as a graph of principals, groups, directory objects, policy scopes, delegation edges, authentication mappings, and administrative capabilities. The goal is to establish effective authority from reviewable evidence rather than infer risk from labels alone.

## When to use

Use for Windows domain labs, enterprise identity reviews, forest/domain trust analysis, service-account boundaries, delegated administration, directory permission review, GPO scope, and certificate-backed identity mappings.

## Preconditions

1. Use only owned labs or environments with explicit authorization.
2. Prefer read-only directory exports, test identities, policy simulation, and isolated replicas.
3. Pin forest/domain topology, domain-controller versions, relevant policy revisions, and the test principal set.
4. Define the intended administrative boundary before classifying a path as unintended.

## Workflow

1. **Map trust topology.** Record forests, domains, trust direction, filtering boundaries, and administrative ownership.
2. **Inventory principals and group closure.** Resolve nested groups, service identities, computer identities, and delegated operators.
3. **Map directory-object authority.** Record owner, permissions, inheritance, object type, protected scope, and policy-relevant control rights.
4. **Trace authentication mappings.** Model Kerberos/LDAP identity, service identity, certificate-backed mappings, and where identity translation occurs.
5. **Trace delegation.** Preserve initiating principal, delegated principal, service/resource, constraints, and the final authorization decision.
6. **Map GPO/OU scope.** Resolve links, inheritance, filtering, target populations, and which administrative identities can change policy objects or scope.
7. **Model service and machine boundaries.** Separate directory authority from local host/service authority and document the transition explicitly.
8. **Build effective trust paths.** Compose only concrete edges whose conditions are satisfied in the pinned environment.
9. **Validate safely.** Use read-only evidence, policy simulation, or synthetic lab objects and identities to prove or falsify the path.
10. **Apply minimal remediation.** Narrow delegation, permissions, identity mapping, or policy scope while retaining legitimate administration.

## Operator depth

For deeper authorized methodology, use [the operator runbook](references/operator-runbook.md). The machine-readable scenario matrix is registered by the repository operator-depth manifest.

## Evidence contract

A validated trust path requires the exact initiating test principal, intermediate authority edges, relevant conditions, final synthetic capability, and paired controls. Group membership, a permissive-looking permission entry, or a trust relationship alone is not proof that the final authority path is effective.

## Stop conditions

Stop if validation cannot remain read-only or inside synthetic lab objects and test principals, if unrelated identities would be affected, or if the requested work is outside the explicitly approved environment.

## Output

```text
forest/domain topology:
initiating principal:
group/delegation closure:
directory permission edges:
authentication mappings:
GPO/OU scope:
service/machine transition:
effective trust path:
synthetic validation:
positive control:
negative control:
minimal remediation:
evidence state:
```
