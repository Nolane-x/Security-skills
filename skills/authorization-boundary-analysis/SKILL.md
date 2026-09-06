---
name: authorization-boundary-analysis
description: "Analyze who is allowed to perform an operation, which identity and attributes are checked, where policy is enforced, and whether alternate paths bypass or weaken authorization. Use for APIs, helpers, admin functions, object-level access control, scoped tokens, service IPC, or multi-tenant resources."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Authorization Boundary Analysis

Authorization is a relation between a principal, operation, resource, context, and policy—not a boolean property attached to a request once and forgotten.

## When to use

Use when a lower-privileged or differently scoped principal may reach an operation intended for another identity, role, tenant, object, or capability.

## Preconditions

Test only local/owned/sandboxed fixtures or systems for which explicit authorization covers the identities and operations involved. Use synthetic accounts/resources and benign marker actions.

## Workflow

1. **Define principal identities.** User, service, process token, API key, tenant, role, workload identity, delegated actor.
2. **Define operation/resource/context tuple.** Read/write/delete/admin, object id, tenant, session, origin, channel, feature state.
3. **Locate policy decisions.** Gateway, middleware, route, service method, database filter, helper IPC, backend capability.
4. **Trace identity propagation.** Headers/tokens, session object, process credentials, internal RPC metadata, database tenancy key.
5. **Check scope composition.** Global versus object-level permission, method/path constraints, token scopes, resource filters, delegated rights.
6. **Enumerate alternate paths.** Legacy endpoints, internal routes, batch APIs, background jobs, helper services, redirects, alternate verbs/content types.
7. **Check policy/data binding.** Is the authorized resource id the same one later used after lookup, mutation, caching, or canonicalization?
8. **Run positive/negative matrix.** Authorized principal succeeds; unauthorized neighbor fails; object/tenant swap fails; scope reduction fails safely.
9. **Trace privileged sink only with benign actions.** Marker file, no-op update, synthetic resource, or policy decision log.
10. **Centralize the invariant** in remediation and add regression tests for every bypass path.

## Evidence contract

A valid finding shows a specific unauthorized principal-operation-resource tuple that is accepted because a policy decision is absent, weak, or bound to the wrong identity/resource. Preserve both allowed and denied controls.

## Stop conditions

Stop if authorization semantics are undocumented and cannot be established from owner-approved policy, tests would access real third-party data, or the observed difference is intentionally delegated behavior.

## Output

```text
principal:
operation:
resource/tenant:
expected policy:
actual decision point:
identity propagation:
bypass/weak binding:
positive control:
negative control:
benign effect:
```
