# Wave 10 Multi-Tenant Data Isolation Depth Design

## Status

Approved in-chat design for Wave 10 operator-depth profile #17. This document freezes the intended semantics before implementation.

Base authority: `main@4d2c6be108303a538f0f62cd8f45d8dca09fb90c`.

Target canonical skill: `multi-tenant-data-isolation-analysis`.

## Goal

Deepen the existing `multi-tenant-data-isolation-analysis` skill from a paired-tenant checklist into a causal tenant-isolation proof method that can distinguish identity-source mistakes, context-loss bugs, namespace/filter mistakes, async propagation drift, lifecycle generation drift, and result/object binding failures without duplicating authorization, cache-key, or RAG/memory isolation skills.

The profile must remain deterministic, evidence-first, portable, and restricted to synthetic or explicitly authorized environments.

## Why this profile is distinct

The existing skill already identifies tenant identity sources, derived representations, filters, caches, jobs, files, and indexes. That is useful surface coverage, but it does not yet require an operator to prove the complete tenant-context lineage that caused a security-relevant result.

This profile adds a tenant-specific causal model rather than another authorization or cache-key profile:

- `authorization-boundary-analysis` asks whether a principal may perform an operation on a resource;
- `cache-key-identity-analysis` asks whether a cache entry represents every security-relevant dependency;
- `rag-memory-data-isolation-analysis` focuses retrieval, memory, derived-state, and lifecycle isolation in AI/RAG systems;
- `multi-tenant-data-isolation-analysis` will ask whether the same canonical tenant identity is preserved and correctly bound through request, policy, storage, async, namespace, and result transitions.

Cross-routing remains explicit: cache-specific identity failures should still compose with cache-key analysis, and generic authorization failures should still compose with authorization-boundary analysis.

## Causal tenant-isolation model

The canonical causal chain is:

`request origin -> authenticated principal -> claimed tenant -> canonical tenant identity -> membership/role binding -> tenant-context generation -> representation/propagation hop -> policy/filter decision -> namespace/query/cache/job/index key -> resolved object/result identity -> bounded read/write/list effect -> receipt/result binding -> lifecycle/migration generation`

The operator must trace every transition that is material to the observed security-relevant result. A result is not tenant-isolation-safe merely because a request contained a tenant ID or because a query included a filter; the result must be causally bound to the canonical tenant context and current lifecycle generation.

## Mandatory distinctions

The skill and runbook must make the following distinctions explicit:

1. `authenticated principal != tenant membership`
2. `claimed tenant != canonical tenant identity`
3. `tenant hint/header != canonical tenant identity`
4. `membership/role binding != ambient admin/support authority`
5. `filter present != tenant-correct result`
6. `namespace/key != resolved object identity`
7. `same object name/id != same tenant-scoped object`
8. `same logical tenant != same lifecycle/migration generation`
9. `queued job tenant context != execution-time ambient tenant context`
10. `cache/index/search tenant partition != storage-object tenant partition`
11. `caller authority != admin/support ambient authority`
12. `result payload tenant marker != causally tenant-bound result`

## Core invariants

A profile-compliant analysis must be able to reason about these invariants:

1. A security-relevant operation must derive tenant identity from an authoritative source, not solely from attacker- or caller-controlled hints.
2. The authenticated principal must be bound to the canonical tenant through an explicit membership/role decision before tenant-scoped authority is exercised.
3. Every representation that carries tenant context across process, queue, storage, index, cache, export, or service boundaries must preserve the same canonical tenant identity or an auditable equivalent.
4. Policy filters, query predicates, namespace selectors, object-store prefixes, cache keys, job payloads, index filters, and export scopes must all be traceable to the same canonical tenant identity when they influence the result.
5. An isolation check is incomplete until the resolved object/result identity is proven tenant-consistent; a syntactically present filter is insufficient.
6. Ambient admin/support/service authority must not silently substitute for the caller's tenant-scoped authority in a way that broadens access.
7. Async work must bind the initiating tenant context explicitly; worker-local defaults or ambient context must not redefine tenancy.
8. Tenant lifecycle changes such as migration, shard movement, membership revocation, org transfer, archival, restore, or region change must advance or invalidate a generation where stale state could change the security result.
9. A cross-tenant observation must be reproduced only with synthetic data and must distinguish true context loss from duplicate fixture data, stale index/cache state, eventual consistency, and downstream routing differences.
10. Read, write, list/search, export/import, webhook, background job, cache, and administrative paths must be evaluated according to whether they can produce a security-relevant tenant-bound effect.
11. A remediation must preserve legitimate same-tenant behavior while splitting or rejecting tenant-distinct contexts that previously collapsed.
12. Evidence promotion must never exceed the directly demonstrated transition; surface suspicion must not be promoted to a confirmed cross-tenant effect without controlled proof.

## Evidence ladder M0-M5

### M0 — Tenant surface identified

Tenant-aware data paths, identities, filters, namespaces, or propagation mechanisms are identified, but no material divergence is yet demonstrated.

### M1 — Tenant-context divergence

A directly observed mismatch exists between claimed/canonical tenant identity, principal membership, propagated representation, policy/filter input, or lifecycle generation.

### M2 — Policy/namespace/object binding divergence

A deterministic synthetic control shows that tenant-distinct invocations can collide, alias, or resolve through the same policy/filter/namespace/object-selection state when they should remain distinct.

### M3 — Inert cross-context observation

Synthetic tenant A can observe an inert marker, object identity, list/search entry, cache/index result, or job result belonging to synthetic tenant B without causing a meaningful state change.

### M4 — Bounded synthetic cross-tenant effect

A controlled, reversible, owner-operated fixture demonstrates a wrong read/write/list/export/job/admin decision or effect across synthetic tenants. The effect must be bounded, non-destructive, and directly attributable to the tenant-context defect.

### M5 — Full causal tenant-isolation proof

The complete causal chain is demonstrated with direct evidence of the failing transition, paired positive/negative controls, counterfactual controls, async/lifecycle generation controls where relevant, alternative-explanation elimination, corrected remediation behavior, and regression evidence. M5 does not permit claims beyond the synthetic/authorized scope actually tested.

## Deterministic review cases

The profile will ship at least three machine-readable review cases.

### 1. `tenant-context-binding`

Purpose: prove that request principal, claimed tenant, canonical tenant identity, membership/role binding, policy/filter decision, and resolved result remain consistently bound.

Expected failure class: a caller-provided or stale tenant representation influences a policy or query path without authoritative membership binding, or the resolved object/result belongs to a neighboring synthetic tenant.

Required controls include same-principal/different-tenant, same-tenant/different-principal, corrected canonical tenant derivation, and a benign same-tenant success case.

### 2. `async-context-propagation`

Purpose: prove that background jobs, queues, schedulers, webhooks, workers, exports/imports, or deferred callbacks preserve the initiating canonical tenant context and lifecycle generation.

Expected failure class: worker-local ambient context, missing tenant payload, stale membership, stale migration generation, or retry/replay semantics cause work to execute under the wrong synthetic tenant.

Required controls include delayed execution after tenant-generation change, duplicate/retry handling, explicit tenant binding in the job artifact, and a corrected propagation control.

### 3. `namespace-to-resolved-object-binding`

Purpose: prove that DB schema/key, object-store path, cache/index/search namespace, query predicate, and final resolved object identity all correspond to the intended canonical tenant.

Expected failure class: shared namespace, omitted partition component, alias, canonicalization mismatch, stale index/cache partition, or backend routing causes a tenant-correct-looking selector to resolve a neighboring tenant's synthetic object/result.

Required controls include identical object names/IDs across synthetic tenants, neighboring namespace tests, direct resolved-object identity capture, and corrected namespace/object binding.

## Runbook structure

The operator runbook must include at least these sections:

1. `Attack surface`
2. `Hypothesis matrix`
3. `Principal and tenant-identity trace`
4. `Membership and role-binding trace`
5. `Tenant-context generation trace`
6. `Representation and propagation trace`
7. `Policy and filter-decision trace`
8. `Namespace and selector trace`
9. `Resolved object/result identity`
10. `Async/job context trace`
11. `Lifecycle and migration-generation trace`
12. `Administrative and ambient-authority trace`
13. `Result and receipt binding`
14. `Controlled validation`
15. `False-positive controls`
16. `Counterfactual controls`
17. `Alternative explanations`
18. `Evidence capture`
19. `Evidence promotion and ceiling`
20. `Remediation checks`

## Counterfactual controls

A strong analysis should select counterfactuals appropriate to the suspected transition, including:

- same principal with a different synthetic tenant membership;
- same tenant with a different synthetic principal/role;
- same object name or logical ID in two synthetic tenants;
- same request with caller-controlled tenant hint changed while canonical membership stays fixed;
- same job payload executed after a tenant lifecycle/migration generation change;
- same namespace selector with a neighboring tenant partition;
- same query/filter with authoritative tenant identity substituted for an untrusted representation;
- same operation with ambient admin/support authority disabled or replaced by explicit caller-bound authority;
- corrected tenant propagation or namespace binding that preserves legitimate same-tenant behavior.

## Alternative explanations

Before promoting evidence, the operator must consider and distinguish at least the following when applicable:

- duplicate or intentionally shared synthetic fixture data;
- eventual consistency or delayed index refresh;
- stale cache or search index behavior better explained by cache-key identity;
- backend/shard/region routing differences;
- retry, duplicate delivery, or queue replay;
- intentionally global/public/shared resources;
- admin/support paths explicitly designed to cross tenants and protected by separate authorization;
- migration/restore tooling operating on an explicit cross-tenant control plane;
- framework safe-failure semantics;
- test harness contamination or stale fixtures.

## Machine-readable scenario contract

Each deterministic review case should carry strings for at least these fields, with enough detail to make the case self-explanatory and reviewable:

- `hypothesis`
- `safe_oracle`
- `positive_control`
- `negative_control`
- `stop_condition`
- `remediation_oracle`
- `request_origin`
- `authenticated_principal`
- `claimed_tenant`
- `canonical_tenant_identity`
- `membership_role_binding`
- `tenant_context_generation`
- `representation_propagation_hop`
- `policy_filter_decision`
- `namespace_selector`
- `resolved_object_result_identity`
- `bounded_effect`
- `receipt_result_binding`
- `lifecycle_migration_generation`
- `async_context_control`
- `ambient_authority_control`
- `counterfactual_control`
- `alternative_explanation`
- `evidence_level`
- `evidence_ceiling`

The implementation test may require a minimum non-trivial string length for each field, consistent with the existing operator-depth test style.

## Skill output contract

The canonical skill should produce or request a structured output that can capture:

- tenancy model;
- authenticated principal;
- claimed and canonical tenant identities;
- membership/role binding;
- tenant-context generation;
- representation/propagation hops;
- policy/filter decision;
- storage/query/cache/job/index namespace or selector;
- resolved object/result identity;
- async context state;
- lifecycle/migration generation;
- ambient admin/support authority state;
- bounded effect or observation;
- counterfactual results;
- alternative explanations considered;
- evidence level and evidence ceiling;
- remediation and regression result.

## Safety boundary

Dynamic validation is limited to authorized, owned, local, sandboxed, CTF, benchmark, or explicitly scoped environments.

Use only synthetic tenants, synthetic principals, synthetic objects, inert markers, mock/read-only services, deterministic policy simulators, or bounded reversible owner-controlled state.

Do not access real customer data, production tenant identifiers, production support/admin paths, real credentials, third-party accounts, or unauthorized systems. Do not use destructive actions, persistence, evasion, malware, credential theft, or indiscriminate exploitation.

If proof would require real cross-customer access or irreversible state, stop at the strongest lower evidence level supported by the safe evidence.

## Implementation scope

Exactly these nine paths are expected to change for profile #17:

1. `README.md`
2. `docs/operator-depth-contract.md`
3. `docs/superpowers/specs/2026-09-16-wave10-multi-tenant-isolation-depth-design.md`
4. `docs/superpowers/plans/2026-09-16-wave10-multi-tenant-isolation-depth.md`
5. `operator-depth/profiles.json`
6. `skills/multi-tenant-data-isolation-analysis/SKILL.md`
7. `skills/multi-tenant-data-isolation-analysis/references/operator-review-cases.json`
8. `skills/multi-tenant-data-isolation-analysis/references/operator-runbook.md`
9. `tests/test_multi_tenant_data_isolation_depth.py`

## Explicit non-scope

The implementation must not change:

- `skills/multi-tenant-data-isolation-analysis/skill.meta.json`;
- skill graph edges;
- packs;
- routing domains;
- benchmark fixtures or thresholds;
- agent-eval authority;
- superiority-court authority;
- GitHub workflow semantics.

The profile may reference adjacent skills, but it must not silently redefine their authority.

## Dedicated test contract

The dedicated test should follow the same four-part structure used by recent Wave 10 profiles:

1. `test_skill_exposes_causal_tenant_isolation_model`
2. `test_runbook_requires_transition_level_tenant_reasoning`
3. `test_review_cases_encode_tenant_isolation_reasoning`
4. `test_skill_is_registered_as_seventeenth_operator_depth_profile`

The registry assertion should be additive (`>= 17`) and require exactly one matching `multi-tenant-data-isolation-analysis` registration. It must not globally assert an exact profile count in a way that blocks future additive profiles.

## Verification and merge discipline

Implementation follows the established Wave 10 provenance sequence:

1. commit this design spec;
2. self-review the spec for placeholders, contradictions, ambiguity, and scope;
3. after written-spec approval, write and commit the implementation plan;
4. add the dedicated test first;
5. obtain a clean RED CI proving the intended assertions fail for missing depth artifacts while unrelated repository gates remain healthy;
6. implement behavioral artifacts without changing the test;
7. obtain full behavioral GREEN across the six OS/Python matrix jobs plus `benchmark-core`, `agent-eval-core`, and `superiority-court-core`;
8. update only public docs after behavioral GREEN;
9. prove the post-GREEN delta is documentation-only and the total PR scope is exactly the nine paths above;
10. obtain full exact-head GREEN on the final candidate;
11. merge with an expected-head SHA guard;
12. obtain full post-merge push CI on the merge SHA;
13. record final closure provenance.

No empirical superiority claim over Claude-Red or another external system is permitted without an actual external contestant run through the repository's superiority court.
