# Multi-Tenant Data Isolation Operator Runbook

Use this runbook only for owned, local, sandboxed, benchmark, CTF, or explicitly authorized targets. Use synthetic tenants, principals, roles, and objects. Prefer read-only or reversible fixtures and inert markers.

## Attack surface

Map every surface where tenant context can influence security-relevant behavior: request claims/headers/path state, membership lookup, ORM/session state, query predicates, database schema/key selection, object-store prefixes, cache namespaces, search/index filters, queue/job payloads, webhooks, exports/imports, retries, callbacks, support/admin tooling, migration paths, and result/receipt construction.

For each surface record the canonical tenant identity expected there, the actual representation observed there, and the evidence source used to establish both.

## Hypothesis matrix

Write a falsifiable hypothesis for each suspected transition. Include the expected safe invariant, the smallest one-dimension synthetic control that could disprove it, the strongest safe evidence level available, and the stop condition that prevents real-customer or irreversible validation.

Examples include a claimed tenant reaching a policy/filter decision without membership/role binding, a namespace selector derived from a stale tenant representation, an async context reconstructed from worker ambient state, or a lifecycle/migration generation ignored by an index or queued job.

## Principal and tenant-identity trace

Record the request origin, authenticated principal, claimed tenant, canonical tenant identity, and evidence source for each. Preserve the distinction between authentication and tenant membership and between a caller-controlled tenant hint and the authoritative tenant selected after membership validation.

The trace should be able to answer whether the same authenticated principal can present a neighboring synthetic tenant hint without changing the canonical tenant identity or membership result.

## Membership and role-binding trace

Record the exact membership/role binding that connects the authenticated principal to the canonical tenant. Capture role, scope, decision source, decision result, membership generation where available, and evidence proving the decision precedes tenant-scoped authority.

Explicitly note whether any service, support, administrative, or worker identity is present and whether it can broaden caller-scoped access.

## Tenant-context generation trace

Record the tenant-context generation used for the request or operation. Treat membership changes, tenant migration, shard moves, org transfer, restore, archival, region changes, or other lifecycle transitions as potential generation changes when stale derived state could affect isolation.

Capture the generation before and after a controlled synthetic lifecycle change and identify which downstream representations are expected to invalidate, refresh, or remain valid.

## Representation and propagation trace

Trace every representation/propagation hop that carries tenant context across a process, RPC, job, queue, webhook, cache, storage, index, export, or callback boundary. For each hop record producer, consumer, serialized form, transformation, canonical tenant mapping, tenant-context generation, and proof source.

Equivalent encodings are acceptable only when they resolve deterministically to the same canonical tenant identity and current generation.

## Policy and filter-decision trace

Record the policy/filter decision separately from later storage or namespace selection. Capture the exact tenant value used by the policy, principal/role state, operation, resource class, result, and evidence source.

A syntactically present filter is not sufficient. The trace must prove that the policy/filter decision is bound to the canonical tenant identity rather than a stale or caller-controlled representation.

## Namespace and selector trace

Record the concrete namespace selector used for the operation: database schema/key, query predicate, cache prefix, object-store path, queue partition, search/index tenant filter, export scope, or equivalent selector.

For neighboring synthetic tenants, compare selectors while holding unrelated state constant. Note aliases, normalization, fallback/default behavior, shared namespaces, and generation-dependent routing.

## Resolved object/result identity

Capture the final resolved object/result identity after policy and namespace selection. Use synthetic tenant-bound IDs, deterministic fixture fingerprints, storage generations, index provenance, or other read-only evidence that can distinguish equal-looking objects belonging to neighboring tenants.

For list/search/export responses, identify the tenant-scoped corpus responsible for each result. For writes, bind the target identity to a reversible receipt. For reads, use inert synthetic markers instead of real data.

## Async/job context trace

Record the async context at enqueue time and execution time, including canonical tenant identity, membership/role binding where material, tenant-context generation, job payload representation, worker ambient state, retry count, duplicate/replay state, and evidence source.

Test whether a delayed synthetic job remains bound to the initiating tenant after advancing a lifecycle/migration generation. Explicitly compare serialized async context with any execution-time ambient tenant default.

## Lifecycle and migration-generation trace

Record every lifecycle/migration generation that can affect the tenant-scoped result: membership generation, tenant generation, migration/shard generation, index generation, queue generation, or storage generation when present.

Use deterministic synthetic generation changes rather than wall-clock timing. Identify whether stale cache/index/job state is invalidated, refreshed, rejected, or safely preserved after the generation advances.

## Administrative and ambient-authority trace

Record all administrative and ambient authority available to the process, worker, support tool, migration task, or service identity. Compare it explicitly with caller authority and the membership/role binding of the synthetic principal.

A normal tenant flow must not silently inherit support/admin ambient authority. Where safe, rerun the fixture with ambient authority removed or replaced by explicit caller-bound authority to localize the cause.

## Result and receipt binding

Bind every observed result or effect to the same tenant-context lineage. Capture result identity, canonical tenant identity, resolved object identity, operation, lifecycle/migration generation, and a deterministic receipt or provenance marker.

A tenant marker inside the response is not enough; the operator must prove that the result was produced from the intended tenant-scoped object or corpus.

## Controlled validation

Use one-dimension synthetic controls. Recommended controls include:

- same principal with a neighboring synthetic tenant membership;
- same tenant with a different synthetic principal or role;
- same logical object name/ID created independently in two synthetic tenants;
- same request with only the caller-controlled tenant hint changed;
- same operation with canonical tenant identity substituted for an untrusted representation;
- same namespace selector against a neighboring tenant partition;
- same queued job before and after a tenant lifecycle/migration generation change;
- same async payload with worker ambient tenant state changed;
- same caller operation with ambient admin/support authority removed;
- remediated path proving legitimate same-tenant behavior remains intact.

Keep effects read-only or reversible. Use inert markers and deterministic receipts instead of customer data or durable privilege.

## False-positive controls

Before promotion, rule out duplicate synthetic fixture data, intentionally global/shared resources, eventual consistency, delayed index refresh, stale cache better explained by cache-key identity, backend/shard/region routing, retry or duplicate delivery, explicit cross-tenant admin design, parser/canonicalization differences, migration control-plane behavior, and stale test fixtures.

Repeat the control with regenerated synthetic objects when fixture contamination is plausible.

## Counterfactual controls

A useful counterfactual changes exactly one security-relevant variable. Record baseline and counterfactual side by side, including canonical tenant identity, membership/role binding, tenant-context generation, policy/filter decision, namespace selector, resolved object/result identity, async context, lifecycle generation, ambient authority, and final receipt.

Counterfactuals should isolate the failing transition rather than change many fields at once.

## Alternative explanations

For every unexpected cross-context observation, document the alternative explanation and the evidence that supports or eliminates it. At minimum consider duplicate fixture data, eventual consistency, cache/index staleness, replica/shard routing, queue retry/replay, public/shared-resource semantics, admin/support behavior, migration state, canonicalization, framework safe-failure behavior, and test harness contamination.

Do not promote evidence merely because the primary hypothesis sounds plausible.

## Evidence capture

Capture only synthetic identifiers, redacted fingerprints, policy decisions, namespace selectors, generation markers, inert result markers, reversible receipts, and provenance needed to reproduce the finding.

Do not capture real customer content, real credentials, production support/admin traces, or third-party account data.

## Evidence promotion and ceiling

Use M0-M5 and never promote above the directly evidenced transition:

- M0 for mapped tenant surfaces only;
- M1 for directly observed tenant-context divergence;
- M2 for deterministic policy/namespace/object binding divergence;
- M3 for inert neighboring-tenant observation;
- M4 for a bounded reversible synthetic cross-tenant effect;
- M5 only for full causal lineage plus counterfactual, lifecycle/async controls where relevant, alternative-explanation elimination, remediation, and regression evidence.

The evidence ceiling is the strongest level the safe fixture directly demonstrates. If stronger proof would require real customer access, production support/admin behavior, destructive state, or unauthorized systems, stop at the lower level.

## Remediation checks

Fix the earliest tenant-context transition that violates the invariant. Then verify all of the following:

1. the original synthetic failure no longer reproduces;
2. the intended same-tenant positive control still succeeds;
3. neighboring synthetic tenants remain separated;
4. principal/role counterfactuals behave according to membership policy;
5. async/job context remains bound after retry and generation changes;
6. namespace and resolved object/result identity remain tenant-consistent;
7. ambient admin/support authority no longer substitutes for caller authority;
8. migration/lifecycle regression controls invalidate or refresh stale derived state as designed.

Record the remediation oracle and final evidence ceiling. Do not generalize beyond the authorized fixture actually tested.
