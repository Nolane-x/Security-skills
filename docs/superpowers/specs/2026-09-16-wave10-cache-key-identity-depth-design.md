# Wave 10 Cache-Key Identity Depth Design

## Status

Approved design for Wave 10 operator-depth profile #15. Base: `main@787fb28377f51edd3799ee5bd1e12881b94abd27`.

## Goal

Deepen the existing canonical `cache-key-identity-analysis` skill from a workflow checklist into a causal cache-identity method that can distinguish benign reuse from security-relevant identity collapse, stale replay, cross-context reuse, and lifecycle/invalidation drift using deterministic, synthetic, evidence-bounded review artifacts.

## Non-goals

- Do not create a new canonical skill.
- Do not change `skill.meta.json`, graph edges, packs, routing domains, benchmark fixtures/thresholds, agent-eval authority, or superiority-court authority.
- Do not add payload corpora, offensive exploitation guidance, real-account testing, credential material, persistence, destructive actions, evasion, malware, or third-party effects.
- Do not claim empirical superiority over Claude-Red or any external system without an actual contestant run through the repository superiority court.

## Scope

Exactly these nine paths are intended:

1. `README.md`
2. `docs/operator-depth-contract.md`
3. `docs/superpowers/specs/2026-09-16-wave10-cache-key-identity-depth-design.md`
4. `docs/superpowers/plans/2026-09-16-wave10-cache-key-identity-depth.md`
5. `operator-depth/profiles.json`
6. `skills/cache-key-identity-analysis/SKILL.md`
7. `skills/cache-key-identity-analysis/references/operator-review-cases.json`
8. `skills/cache-key-identity-analysis/references/operator-runbook.md`
9. `tests/test_cache_key_identity_depth.py`

The registry schema remains version `2`. Public docs are synchronized only after behavioral GREEN.

## Causal cache-identity model

The canonical reasoning chain is:

`semantic invocation -> security-relevant dependency set -> canonical key inputs -> serialized key -> cache namespace -> cache entry identity -> writer principal/context -> stored result provenance -> reader principal/context -> freshness/invalidation generation -> replayed result -> bounded security decision/effect`

The method treats a cache hit as an identity claim, not merely a performance event. Reuse is safe only when the entry identity is strong enough to prove equivalence for the security-relevant result being reused.

## Core distinctions

The skill must make these distinctions explicit:

- semantic invocation != serialized key;
- serialized key != cache entry identity;
- cache entry identity != security identity;
- writer context != reader context;
- key equality != dependency equivalence;
- freshness timestamp != invalidation generation;
- cache hit != authorization to reuse a result.

## Core invariants

1. Every security-relevant result dependency is represented in cache identity or is explicitly proven invariant for the result under review.
2. Canonicalization and serialization preserve distinctions that matter to the result; distinct security identities must not collapse into one key/namespace entry.
3. Cache namespace binds the relevant tenant, user, service, deployment, policy, or resource boundary whenever that boundary can change the result.
4. Writer provenance is retained or otherwise made irrelevant by proof that any authorized writer would produce an equivalent result for the exact reader context.
5. Reader context is checked against the entry's identity contract before replay; a matching key alone is insufficient when context-sensitive state exists.
6. Invalidation generation advances when any mutable dependency that affects the result changes, including policy, role, resource generation, feature gate, schema, authorization state, or deployment contract when applicable.
7. First-writer and replay order do not change a result that is supposed to be context-specific. A->B and B->A controls must converge to each context's correct result.
8. Process restart, worker migration, persistence restoration, or distributed cache propagation do not revive entries whose identity generation is no longer valid.
9. A corrected-key or corrected-generation remediation removes the wrong reuse while preserving legitimate neighboring cache hits.
10. Evidence level never exceeds the strongest directly observed causal link.

## Dependency completeness

The operator must first model the cached computation semantically, including both direct and indirect dependencies. Candidate dimensions include authenticated principal, tenant, resource identity, authorization state, request method, route, query/body material, locale, feature flags, policy generation, object generation, mutable referenced state, and deployment/runtime generation.

A dimension may be omitted from the key only when the review proves the cached result is invariant under controlled changes to that dimension. Absence from the key is therefore not automatically a defect; the defect is unproven equivalence combined with security-relevant reuse.

## Key construction and canonicalization

The method records:

- source values selected as key material;
- transformation order;
- canonicalization rules;
- serialization format;
- hashing/truncation rules when present;
- namespace/prefix selection;
- entry identity after serialization;
- object/wrapper behavior when stringified or normalized.

The review must distinguish intentional equivalence from accidental collapse and must consider non-commutative transformations where order changes identity.

## Writer/reader provenance

For entries created in one context and consumed in another, capture:

- writer principal/context;
- reader principal/context;
- entry generation;
- result provenance;
- whether the cached value is data, a policy decision, an authorization decision, a derived object, or a side-effect suppression/dedup result;
- the contract that allows or forbids cross-context replay.

A cache may be globally shared and still safe when the result is proven globally invariant; shared storage alone is not evidence of a vulnerability.

## Lifecycle and invalidation generation

Timestamp-based freshness is insufficient when mutable authority or resource state changes independently of time. The method therefore tracks an invalidation/lifecycle generation distinct from TTL.

Relevant transitions include role changes, tenant membership changes, resource replacement, policy updates, secret/token rotation when only derived non-secret state is cached, deployment/schema generation changes, explicit invalidation, restart, persistence restore, and distributed propagation.

## Counterfactual proof

Use one-dimension-at-a-time controls:

- same semantic invocation, different principal;
- same principal, neighboring synthetic resource;
- same request, different tenant namespace;
- same key inputs, different policy/resource generation;
- same cache entry, reverse writer/reader order;
- same context with corrected key material;
- same key with explicit invalidation-generation change.

Counterfactuals must use synthetic identities and inert or reversible owner-controlled state.

## Alternative explanations

Before promoting evidence, rule out or record:

- a second persistence layer producing the replay;
- upstream/downstream memoization not represented by the observed key;
- intentionally global/invariant computation;
- fixture contamination between synthetic principals;
- stale observation from asynchronous propagation;
- request/result correlation error;
- canonicalization occurring at a different layer than assumed;
- intentionally sticky session or deployment behavior;
- duplicate delivery or retry behavior rather than cache reuse;
- unsupported/non-serializable argument behavior with safe failure.

## Evidence ladder K0-K5

- **K0 — cache surface:** a cache, memoization layer, dedup key, or persistence index is identified; no security-relevant divergence is established.
- **K1 — dependency/key divergence:** a result-affecting candidate dependency is shown to be absent from or collapsed by key construction, but wrong replay is not yet observed.
- **K2 — identity collision:** two semantically distinct synthetic invocations resolve to the same serialized key/namespace/entry identity under controlled observation.
- **K3 — inert replay:** the colliding entry is shown to replay an inert marker, read-only result, or synthetic decision across contexts where the oracle expects different outputs.
- **K4 — bounded synthetic effect:** the replay causes a bounded, reversible, owner-controlled security-relevant decision/effect in the synthetic fixture.
- **K5 — causal lifecycle proof:** K4 plus reverse-order control, writer/reader provenance, lifecycle/invalidation generation control, alternative-explanation elimination, corrected-key or corrected-generation remediation, and regression evidence preserving legitimate cache reuse.

The evidence ceiling is the highest level directly supported by captured artifacts. A reviewer must never infer K4/K5 from key collision alone.

## Deterministic review cases

### 1. `dependency-to-key-completeness`

Tests whether a security-relevant dependency is absent from key material or unproven invariant. Controls vary exactly one synthetic dependency while holding unrelated state constant. The remediation oracle adds the missing primitive identity material or proves invariance.

### 2. `canonical-key-and-namespace-identity`

Tests whether distinct semantic identities collapse after canonicalization, serialization, hashing/truncation, or namespace selection. Controls verify intentional equivalence remains equivalent while neighboring synthetic identities stay distinct. The remediation oracle preserves canonical stability without cross-identity collapse.

### 3. `writer-reader-lifecycle-binding`

Tests first-writer/replay order, writer/reader provenance, lifecycle generation, persistence/restart behavior, and invalidation. Controls run A->B and B->A, then advance a synthetic policy/resource generation. The remediation oracle demonstrates stale entries no longer replay while valid same-generation hits remain reusable.

Each scenario must provide strings for at least:

- `hypothesis`
- `safe_oracle`
- `positive_control`
- `negative_control`
- `stop_condition`
- `remediation_oracle`
- `semantic_invocation`
- `security_dependency_set`
- `canonical_key_inputs`
- `serialized_key`
- `cache_namespace`
- `cache_entry_identity`
- `writer_context`
- `stored_result_provenance`
- `reader_context`
- `invalidation_generation`
- `replayed_result`
- `bounded_effect`
- `reverse_order_control`
- `counterfactual_control`
- `alternative_explanation`
- `evidence_level`
- `evidence_ceiling`

## Operator runbook

The runbook must contain the common required sections plus cache-specific sections:

- Attack surface
- Hypothesis matrix
- Semantic dependency trace
- Key-construction trace
- Canonicalization and serialization trace
- Namespace and entry-identity trace
- Writer and reader provenance trace
- First-writer and replay-order trace
- Lifecycle and invalidation-generation trace
- Result and effect binding
- Controlled validation
- False-positive controls
- Counterfactual controls
- Evidence capture
- Evidence promotion and ceiling
- Remediation checks

## Dedicated test contract

`tests/test_cache_key_identity_depth.py` will freeze four things:

1. `SKILL.md` exposes the causal cache-identity model, K0-K5 ladder, counterfactual proof, alternative explanations, and evidence ceiling.
2. The operator runbook contains all cache-specific transition-level reasoning sections.
3. The machine-readable review cases contain at least three deterministic scenarios and every required identity/lifecycle field with substantive content.
4. `operator-depth/profiles.json` contains exactly one additive registration for `cache-key-identity-analysis` using the existing runbook/scenario paths and `lab_only: true`, while the total profile assertion remains additive (`>= 15`).

## TDD and verification sequence

1. Commit this design spec on the isolated branch.
2. Commit the implementation plan.
3. Add only the dedicated test and run CI to obtain a clean RED caused by the missing depth artifacts/profile registration.
4. Implement the skill, runbook, review cases, and additive registry entry.
5. Obtain behavioral GREEN on the full repository workflow.
6. Only after behavioral GREEN, synchronize README and `docs/operator-depth-contract.md` to 15 profiles.
7. Run exact-head full CI on the final candidate.
8. Review changed-file scope and provenance.
9. Mark Ready and merge only with an expected-head SHA guard.
10. Require post-merge push CI on the merge commit: all six matrix jobs plus `benchmark-core`, `agent-eval-core`, and `superiority-court-core` must succeed.

## Safety boundary

All dynamic examples and review cases use synthetic principals/tenants, mock or read-only caches, inert markers, deterministic policy simulators, or reversible owner-controlled state. No real credentials, third-party data, destructive actions, persistence mechanisms, evasion, malware, or unauthorized targets are permitted.
