---
name: cache-key-identity-analysis
description: "Analyze whether cache keys, memoization identities, deduplication keys, or persistence indexes omit security-relevant input state or collapse distinct principals/requests. Use for cross-user data replay, stale authorization results, first-writer behavior, object serialization collisions, or tenant confusion."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Cache-Key Identity Analysis

A cache hit is an identity claim. Reuse is safe only when the cache entry identity proves that the writer context, reader context, security-relevant dependencies, namespace, and lifecycle generation are equivalent for the result being replayed—or when omitted dimensions are directly proven invariant.

## When to use

Use when request-scoped data, authenticated principal, tenant, headers/cookies, query/form values, feature flags, locale, authorization state, resource identity, policy generation, mutable object state, deployment generation, memoization arguments, deduplication keys, or persistence indexes can influence a cached computation or cached decision.

Typical signals include cross-user or cross-tenant replay, stale authorization decisions, first-writer behavior, object-serialization collapse, canonicalization collisions, surprising persistence across restart, stale results after role/resource changes, or deduplication that suppresses work for the wrong semantic request.

## Preconditions

Test only with synthetic users/tenants and owned/local/sandboxed or explicitly authorized deployments. Prefer mock or read-only caches, inert markers, deterministic policy simulators, and reversible owner-controlled state. Do not use real credentials, real customer data, destructive actions, persistence mechanisms, evasion, malware, or third-party effects.

Establish an expected oracle before varying cache identity. Record which result differences are security-relevant and which differences are intentionally global or invariant.

## Causal cache-identity model

Trace the complete chain:

`semantic invocation -> security-relevant dependency set -> canonical key inputs -> serialized key -> cache namespace -> cache entry identity -> writer principal/context -> stored result provenance -> reader principal/context -> freshness/invalidation generation -> replayed result -> bounded security decision/effect`

Do not collapse semantic invocation, key serialization, namespace selection, writer provenance, reader context, lifecycle generation, or replayed effect into one notion of “same request.” A cache hit proves only that the implementation selected an entry; it does not prove that reuse is authorized or semantically equivalent.

Keep these distinctions explicit:

- `semantic invocation != serialized key`
- `serialized key != cache entry identity`
- `cache entry identity != security identity`
- `writer context != reader context`
- `key equality != dependency equivalence`
- `freshness timestamp != invalidation generation`
- cache hit != authorization to reuse a result

Core invariants:

1. Every dependency that can change the security-relevant result is represented in cache identity or is directly proven invariant under controlled variation.
2. Canonicalization and serialization preserve distinctions that matter to the result.
3. Namespace selection binds tenant, user, service, policy, deployment, resource, or other security boundary whenever that boundary can change the result.
4. Writer provenance is retained or explicitly proven irrelevant for the exact reader context.
5. Reader context is evaluated against the entry identity contract before replay; matching key bytes alone are insufficient when context-sensitive state exists.
6. Invalidation generation advances when mutable security-relevant dependencies change.
7. First-writer order does not decide a result that should be context-specific.
8. Restart, worker migration, persistence restore, or distributed propagation do not revive entries whose identity generation is stale.
9. Remediation removes the wrong reuse while preserving legitimate neighboring cache hits.
10. Evidence promotion never exceeds the strongest directly observed causal link.

## Dependency completeness

Define the cached computation semantically before inspecting the key. Record all direct and indirect inputs that can affect the result, including reads performed by callbacks, wrappers, policy helpers, resolvers, resource loaders, environment state, or referenced mutable objects.

Candidate security-relevant dependencies include:

- authenticated principal or service identity;
- tenant or namespace;
- resource/object identity and generation;
- authorization role or policy generation;
- request method, route, query, body, selected headers, or cookie state;
- feature flag or configuration generation;
- locale or region when it changes security-sensitive output;
- mutable referenced state not visible in the explicit function arguments;
- deployment/schema/runtime generation when cached data is generation-sensitive.

Compare the semantic dependency set to key material. A dimension may be omitted only when the result is demonstrated to be invariant under controlled change to that dimension. Absence from a key is therefore not automatically a vulnerability; unproven equivalence plus security-relevant reuse is the concern.

## Key construction and canonicalization

Record actual key construction rather than inferred framework behavior:

1. primitive or object values selected as key inputs;
2. transformation and normalization order;
3. canonicalization rules;
4. serialization format;
5. hashing, truncation, case folding, sorting, encoding, or escaping rules;
6. namespace/prefix/tag selection;
7. final serialized key and cache entry identity.

Inspect wrapper/object serialization separately from live object semantics. A request or wrapper object can serialize to a generic form while code executed inside the cached computation still reads principal, tenant, headers, or other live state.

When transforms are non-commutative, record their order and prove whether neighboring semantic identities remain distinct. Intentional equivalence is safe only when the result is also equivalent.

## Namespace and entry identity

Treat the final cache entry identity as more than key bytes. Record the tuple needed to select the entry in the actual cache implementation, such as namespace, prefix, partition, tenant, shard, cache name, version, key bytes, and generation metadata.

Ask whether two callers with identical serialized keys still land in separate namespaces, and conversely whether distinct semantic identities can collapse into a shared namespace/entry. A shared global cache may be safe when the result is directly proven global and invariant; shared storage alone is not evidence of a defect.

## Writer and reader provenance

For every relevant entry, capture:

- writer principal/context;
- writer request or semantic invocation identity;
- stored result provenance;
- entry generation and creation context;
- reader principal/context;
- reader request or semantic invocation identity;
- the contract that permits or forbids replay from that writer to that reader.

Distinguish data caches, authorization/policy decision caches, derived-object caches, memoized computations, deduplication/suppression entries, and persistence indexes. The acceptable provenance relation can differ by result type, but it must be explicit and testable.

A broad writer capability does not justify replay to every reader. Conversely, a globally invariant result does not need per-user keying merely because different users consume it.

## First-writer and replay order

Use paired order controls whenever reuse may be context-specific:

- A -> B: synthetic context A writes first, then context B reads;
- B -> A: synthetic context B writes first, then context A reads.

A wrong result that follows the first writer is stronger evidence of cache reuse than a single same-result observation. Record whether the wrong value, decision, or inert marker tracks writer order, key identity, namespace, or some other state.

Hold unrelated dimensions constant. If reverse order changes the observed result, record which cache entry and provenance changed. If order does not matter, investigate whether the computation is actually invariant or whether another persistence layer is responsible.

## Lifecycle and invalidation generation

Track invalidation generation separately from TTL or freshness timestamp. Time freshness does not prove validity when authority, membership, policy, resource generation, or schema state changes independently of time.

Relevant generation transitions include:

- role or authorization changes;
- tenant membership changes;
- resource replacement or object-generation changes;
- policy/configuration updates;
- feature-gate generation changes;
- deployment/schema/runtime generation changes;
- explicit invalidation;
- restart or worker migration;
- persistence restore;
- distributed cache propagation.

Record the generation at write time, read time, invalidation time, and effect time. Determine whether stale entries are rejected, versioned, evicted, or safely proven invariant.

## Workflow

1. **Define the semantic invocation.** State what computation or decision is being cached and what result differences matter for security.
2. **Build the security-relevant dependency set.** Include direct arguments and indirect context/state reads.
3. **Extract canonical key inputs.** Record exact source values before transformation.
4. **Trace key construction.** Record normalization, serialization, hashing/truncation, namespace, and final entry identity.
5. **Compare dependency set to identity set.** Mark every omitted dimension as either proven invariant or unresolved.
6. **Capture writer provenance.** Record synthetic writer context, generation, and stored result identity.
7. **Capture reader context.** Record the synthetic reader and why replay should or should not be equivalent.
8. **Run A -> B and B -> A controls.** Determine whether first-writer state controls replay.
9. **Run one-dimension counterfactuals.** Change only principal, tenant, resource, generation, or other dependency under review.
10. **Advance lifecycle generation where relevant.** Change synthetic policy/resource/config generation and observe invalidation behavior.
11. **Rule out alternative persistence/retry explanations.** Correlate the observed entry, result, and request generation.
12. **Validate remediation.** Add corrected primitive key material, corrected namespace, or corrected invalidation generation and rerun positive, negative, reverse-order, and neighboring-hit controls.

## Cache identity evidence ladder

Use K0-K5. Report only the highest level directly supported by captured evidence.

- **K0 — cache surface:** a cache, memoization layer, deduplication key, or persistence index is identified; no security-relevant divergence is established.
- **K1 — dependency/key divergence:** a candidate result-affecting dependency is absent from, collapsed by, or unproven invariant relative to cache identity; wrong replay is not yet observed.
- **K2 — identity collision:** two semantically distinct synthetic invocations resolve to the same serialized key, namespace, or cache entry identity under controlled observation.
- **K3 — inert replay:** the colliding entry replays an inert marker, read-only result, or synthetic decision across contexts where the safe oracle expects different outputs.
- **K4 — bounded synthetic effect:** wrong replay causes a bounded, reversible, owner-controlled security-relevant decision or effect in the synthetic fixture.
- **K5 — causal lifecycle proof:** K4 plus reverse-order control, writer/reader provenance, lifecycle/invalidation-generation control, alternative-explanation elimination, corrected-key or corrected-generation remediation, and regression evidence preserving legitimate reuse.

A key collision alone never proves K3-K5. A stale-looking value without direct entry/result binding does not prove invalidation failure.

## Counterfactual proof

Change one security-relevant dimension at a time while holding the rest constant. Useful controls include:

- same request shape, different synthetic principal;
- same principal, neighboring synthetic resource;
- same semantic inputs, different tenant namespace;
- same key inputs, different policy/resource generation;
- same entry, reverse writer/reader order;
- same context with corrected primitive key material;
- same serialized key with explicit invalidation-generation advance.

Record the expected oracle, observed entry identity, observed result, and remaining alternative explanations for every counterfactual. Do not broaden the experiment beyond the owned fixture to increase apparent impact.

## Alternative explanations

Before promoting evidence, rule out or record:

- another upstream/downstream cache or persistence layer;
- intentionally global/invariant computation;
- fixture contamination between synthetic principals or tenants;
- asynchronous propagation delay rather than stale identity;
- request/result correlation error;
- canonicalization occurring at a different layer than assumed;
- intentionally sticky session/deployment behavior;
- retry or duplicate delivery rather than cache reuse;
- safe failure for unsupported/non-serializable arguments;
- a different resolved resource or policy generation than the one attributed to the observed entry.

An unexplained cache-like symptom stays below the evidence level that requires direct entry/replay binding.

## Evidence contract

A strong finding records:

- semantic invocation and safe oracle;
- security-relevant dependency set;
- canonical key inputs and transformation trace;
- serialized key, namespace, and cache entry identity;
- writer context and stored result provenance;
- reader context;
- write/read/invalidation generation;
- A -> B and B -> A results;
- one-dimension counterfactuals;
- replayed result and any bounded effect;
- alternative explanations considered;
- corrected-key or corrected-generation control;
- evidence level and explicit evidence ceiling.

Use synthetic identifiers rather than real secrets or customer data.

## Evidence ceiling

Always state what the current evidence cannot prove.

- Surface inspection without dependency divergence is capped at K0.
- Missing or collapsed key material without observed identity collision is capped at K1.
- Same entry identity without cross-context replay is capped at K2.
- Inert/read-only replay is capped at K3.
- A bounded reversible synthetic effect can support K4.
- K5 requires repeatable reverse-order and lifecycle/generation proof, alternative-explanation control, remediation, and regression evidence preserving legitimate cache behavior.

Never infer a broader tenant/user impact from one synthetic pair without evidence that the same identity defect generalizes.

## Stop conditions

Stop or downgrade the hypothesis when:

- the result is intentionally global and controlled variation proves it invariant;
- omitted dimensions do not affect the security-relevant result;
- the framework safely rejects unsupported/non-serializable key inputs;
- the apparent replay is attributable to another persistence layer;
- the observed reader is intentionally permitted to consume the writer's globally invariant result;
- the test would require real credentials, real user data, third-party systems, irreversible state, destructive behavior, persistence, evasion, malware, or scope expansion beyond authorization.

## Output

```text
cached computation:
semantic invocation:
security-relevant dependency set:
canonical key inputs:
key transformation/canonicalization:
serialized key:
cache namespace:
cache entry identity:
writer context / stored result provenance:
reader context:
write/read/invalidation generation:
A->B result:
B->A result:
counterfactual result:
replayed result / bounded effect:
alternative explanations:
corrected-key or corrected-generation control:
evidence level:
evidence ceiling:
remediation regression:
```
