---
name: multi-tenant-data-isolation-analysis
description: "Analyze multi-tenant identity and data partitioning across request context, ORM/query filters, caches, object storage, background jobs, search indexes, exports, and administrative paths. Use to validate isolation with synthetic tenants."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Multi Tenant Data Isolation Analysis

Perform dynamic validation only in an authorized, owned, local, sandboxed, CTF, benchmark, or equivalently scoped test environment. Prefer synthetic tenants, principals, objects, inert markers, deterministic mock/read-only services, policy simulators, and bounded reversible owner-controlled state.

## When to use

Use when one service hosts multiple organizations, accounts, workspaces, projects, customers, or equivalent tenants and tenant identity influences reads, writes, queries, caches, jobs, files, object storage, indexes, exports, webhooks, support tooling, or administrative paths.

Use this skill when the question is not merely whether a principal has generic permission, but whether the same authoritative tenant identity remains correctly bound from request origin through policy, storage/namespace selection, async propagation, resolved result, and lifecycle state.

Route a cache-entry dependency problem to `cache-key-identity-analysis`, and route a generic permission decision problem to `authorization-boundary-analysis`. This skill owns the tenant-context lineage that connects those local decisions.

## Preconditions

1. Create at least two synthetic tenants and at least two synthetic principals or roles.
2. Pin the tenancy model, membership source, region/shard layout, lifecycle generation, and relevant queue/cache/index/storage state.
3. Use synthetic duplicate object names or logical IDs where safe because equal-looking identifiers can reveal missing tenant partitioning.
4. Define the strongest evidence level that can be reached without production customer data or irreversible effects.
5. Never use real customer identifiers, production support/admin paths, third-party accounts, or real credentials as proof material.

## Causal tenant-isolation model

Trace the complete security-relevant lineage:

`request origin -> authenticated principal -> claimed tenant -> canonical tenant identity -> membership/role binding -> tenant-context generation -> representation/propagation hop -> policy/filter decision -> namespace/query/cache/job/index key -> resolved object/result identity -> bounded read/write/list effect -> receipt/result binding -> lifecycle/migration generation`

The model is transition-oriented. An operator should identify which transition can change tenant identity, authority, namespace, or object/result binding, then capture direct evidence for that transition instead of inferring safety from the presence of a tenant ID or filter.

Mandatory distinctions:

- `authenticated principal != tenant membership`
- `claimed tenant != canonical tenant identity`
- `tenant hint/header != canonical tenant identity`
- `membership/role binding != ambient admin/support authority`
- `filter present != tenant-correct result`
- `namespace/key != resolved object identity`
- `same object name/id != same tenant-scoped object`
- `same logical tenant != same lifecycle/migration generation`
- `queued job tenant context != execution-time ambient tenant context`
- `cache/index/search tenant partition != storage-object tenant partition`
- `caller authority != admin/support ambient authority`
- `result payload tenant marker != causally tenant-bound result`

## Principal and tenant identity

Record the authenticated principal separately from the tenant requested or hinted by headers, path parameters, claims, job payloads, or UI state. Determine which source is authoritative for the canonical tenant identity and prove how that source is selected.

A principal can authenticate successfully while lacking membership in the claimed tenant. Treat tenant selection as a separate security-relevant decision, and preserve the distinction between an untrusted tenant hint and the canonical tenant identity chosen after membership validation.

## Membership and role binding

Trace the explicit membership/role decision that binds the authenticated principal to the canonical tenant. Record role, resource scope, decision input, decision output, and any tenant-context generation or membership generation that influences the result.

Do not treat a process-wide service identity, support role, administrative session, or worker credential as equivalent to caller membership. If ambient authority exists, prove that it cannot silently broaden the tenant-scoped authority being exercised for the caller.

## Representation and propagation

List every representation carrying tenant context across a trust or execution boundary: request claims, headers, path segments, ORM/session state, RPC metadata, queue/job payloads, webhooks, exports, callbacks, cache prefixes, index filters, object-store prefixes, or derived internal IDs.

For each representation/propagation hop, record the observed value, proof source, producer, consumer, and transformation. Equivalent representations must still map back to the same canonical tenant identity and tenant-context generation.

## Policy, filter, and namespace decisions

Trace policy/filter decision inputs separately from the namespace or selector that ultimately chooses storage, query, cache, job, index, search, or object-store state. A policy decision can be correct while a later selector resolves the wrong tenant partition, and a filter can be syntactically present while being bound to a stale or caller-controlled tenant representation.

Capture the exact policy/filter decision and the exact namespace selector or key used for the operation. Test neighboring synthetic tenants while holding unrelated request state constant.

## Resolved object and result identity

A tenant-isolation conclusion requires the final resolved object/result identity, not only the request or selector text. Record enough identity to distinguish equal-looking objects in neighboring synthetic tenants, such as tenant-bound fixture IDs, storage generation, synthetic object fingerprints, or deterministic result provenance.

For list/search/export paths, identify which tenant-scoped corpus produced each result. For writes, capture the tenant-bound target identity and a reversible receipt. For reads, capture an inert marker or synthetic object fingerprint rather than real data.

## Async and job context

Background work must bind the initiating canonical tenant context explicitly. Compare the tenant context serialized at enqueue time with the tenant context observed at execution time, including membership/role and tenant-context generation where material.

A retry, replay, worker default, ambient service tenant, stale job payload, or callback reconstruction must not redefine tenancy. Use synthetic delayed-execution controls and generation changes to distinguish propagation defects from ordinary retry semantics.

## Lifecycle and migration generation

Model lifecycle state independently from the logical tenant name. Migrations, shard moves, org transfers, membership revocation, archival, restore, region changes, export/import transitions, or control-plane reassignment can make stale representations unsafe even when the tenant label is unchanged.

Advance a deterministic lifecycle/migration generation in the fixture when stale derived state could affect the decision. Record whether queues, caches, indexes, selectors, and resolved objects are bound to the current generation or deliberately invalidated.

## Administrative and ambient authority

Administrative, support, migration, or service-control paths may intentionally span tenants. Treat them as separate authority domains and prove that a normal caller flow cannot inherit their ambient authority merely because the same process, worker, query helper, or storage client is reused.

When testing a suspected confused or ambient-authority path, use synthetic support/admin fixtures only. Compare behavior with ambient privilege removed or replaced by explicit caller-bound tenant authority.

## Workflow

1. Establish two or more synthetic tenants, principals, roles, and tenant-scoped objects with deterministic identifiers.
2. Trace request origin, authenticated principal, claimed tenant, canonical tenant identity, and membership/role binding.
3. Record tenant-context generation and every representation/propagation hop influencing the target operation.
4. Capture the policy/filter decision and the concrete namespace/query/cache/job/index selector used afterward.
5. Capture the resolved object/result identity and the bounded read/write/list effect or inert observation.
6. For async paths, compare enqueue-time and execution-time tenant context, retry/replay behavior, and lifecycle generation.
7. For administrative or service paths, separate caller authority from ambient admin/support authority.
8. Run one-dimension counterfactuals across principal, tenant, role, selector, generation, async context, and ambient authority.
9. Eliminate alternative explanations such as duplicated fixture data, eventual consistency, stale cache/index state, routing differences, or test contamination.
10. Fix the earliest tenant-context transition that violates the invariant, then rerun positive, negative, neighboring-tenant, and lifecycle regression controls.

## Tenant-isolation evidence ladder

- **M0 — Tenant surface identified:** tenant-aware identities, filters, namespaces, propagation mechanisms, or lifecycle surfaces are mapped, but no material divergence is demonstrated.
- **M1 — Tenant-context divergence:** direct evidence shows a mismatch among claimed/canonical tenant identity, principal membership, propagated representation, policy/filter input, or lifecycle generation.
- **M2 — Policy/namespace/object binding divergence:** a deterministic synthetic control shows tenant-distinct invocations can collide, alias, or converge through policy, namespace, selector, or object-resolution state when they should remain distinct.
- **M3 — Inert cross-context observation:** synthetic tenant A can observe an inert marker, object identity, list/search entry, cache/index result, or job result belonging to synthetic tenant B without a meaningful state change.
- **M4 — Bounded synthetic cross-tenant effect:** a controlled reversible owner-operated fixture demonstrates a wrong read/write/list/export/job/admin decision or effect across synthetic tenants and directly attributes it to the tenant-context defect.
- **M5 — Full causal tenant-isolation proof:** the failing transition is evidenced end to end with paired positive/negative controls, counterfactuals, async/lifecycle-generation controls where relevant, alternative-explanation elimination, remediation behavior, and regression evidence.

M5 is not permission to generalize beyond the synthetic or explicitly authorized scope actually tested.

## Counterfactual proof

Prefer one-dimension controls that change exactly one security-relevant variable while keeping everything else stable:

- same synthetic principal with a different tenant membership;
- same tenant with a different synthetic principal or role;
- same object name or logical ID in neighboring synthetic tenants;
- same request with only the tenant hint changed while canonical membership stays fixed;
- same queued job after advancing tenant lifecycle/migration generation;
- same selector against a neighboring namespace partition;
- same operation with authoritative tenant identity substituted for an untrusted representation;
- same operation with ambient admin/support authority removed;
- same remediated path proving legitimate same-tenant behavior still succeeds.

A counterfactual should localize the failing transition, not merely repeat the original request with many variables changed at once.

## Alternative explanations

Before promoting evidence, consider and document whether the observation is better explained by:

- duplicate or intentionally shared synthetic fixture data;
- eventual consistency or delayed index refresh;
- stale cache or search state better routed to cache-key identity analysis;
- backend, shard, region, or replica routing differences;
- retry, duplicate delivery, or queue replay;
- intentionally global/public/shared resources;
- explicitly authorized cross-tenant support/admin behavior;
- migration/restore control-plane semantics;
- parser/canonicalization differences;
- framework fail-safe behavior;
- stale fixtures or test harness contamination.

## Evidence contract

Record the tenant/principal pair, claimed and canonical tenant identities, membership/role binding, tenant-context generation, representation/propagation hops, policy/filter decision, namespace selector, resolved object/result identity, async context, lifecycle/migration generation, ambient authority state, bounded effect or inert observation, counterfactual controls, alternative explanations, remediation behavior, and regression result.

ID predictability, a missing-looking filter, or a tenant header alone is not proof of cross-tenant impact. Evidence must identify the causal transition and remain within synthetic/authorized scope.

## Evidence ceiling

Promote only to the strongest directly demonstrated level:

- mapping alone remains M0;
- a representation or membership mismatch without cross-context convergence remains M1;
- deterministic policy/namespace/object convergence without observable neighboring-tenant result remains M2;
- inert neighboring-tenant observation can reach M3;
- a reversible bounded synthetic effect can reach M4;
- M5 requires complete causal lineage, alternative-explanation elimination, remediation, and regression controls.

If safe proof would require real customer data, production support/admin access, irreversible state, or unauthorized systems, stop at the strongest lower evidence level supported by the available evidence.

## Stop conditions

Stop immediately if reproduction would require real customer data, production tenant identifiers, production support/admin functions, third-party accounts, live secrets, destructive or irreversible cross-tenant state, persistence, evasion, malware, or any unauthorized target.

Stop and route to an adjacent skill if the observed root cause is primarily a cache-key dependency defect, generic authorization policy defect, or canonicalization/namespace identity defect outside the tenant-context lineage.

## Output

```text
tenancy model:
authenticated principal:
claimed tenant:
canonical tenant identity:
membership/role binding:
tenant-context generation:
representation/propagation hops:
policy/filter decision:
namespace selector:
resolved object/result identity:
async context:
lifecycle/migration generation:
ambient admin/support authority:
bounded effect or observation:
counterfactual results:
alternative explanations:
evidence level:
evidence ceiling:
remediation/regression result:
```
