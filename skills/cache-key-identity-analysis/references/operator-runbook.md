# Cache-Key Identity Operator Runbook

This runbook is for owned/local/sandboxed or explicitly authorized review only. Use synthetic principals/tenants, mock or read-only caches, inert markers, deterministic policy simulators, and reversible owner-controlled state. Do not use real credentials, customer data, destructive actions, persistence mechanisms, evasion, malware, or third-party effects.

## Attack surface

Inventory every place where a result can be reused by identity rather than recomputed: memoization wrappers, local process caches, distributed caches, authorization caches, response caches, object caches, deduplication/suppression tables, persistence indexes, and framework-level decorators. Record cache name, namespace, entry selector, writer context, reader context, result type, lifecycle boundary, and the semantic computation being cached.

Do not assume that a cache shared across users or tenants is unsafe. First determine whether the cached result is intended to be globally invariant. The audit question is whether the selected entry identity is strong enough for the result being replayed.

## Hypothesis matrix

Write one hypothesis per identity transition. Each row records semantic invocation, security-relevant dependency set, key inputs, serialized key, namespace, entry identity, writer context, reader context, invalidation generation, safe oracle, positive control, negative control, alternative explanation, and evidence ceiling.

Prefer hypotheses that can be falsified by changing exactly one synthetic dimension while holding unrelated state constant. Examples include principal, tenant, neighboring resource, policy generation, or canonical representation.

## Semantic dependency trace

Define the cached computation independently from the implementation key. Record every direct argument and indirect state read that can change the security-relevant result: principal, tenant, authorization role, policy generation, resource identity/generation, request method/route, selected headers/cookies, query/body values, feature flags, locale, referenced mutable objects, configuration generation, and deployment/schema generation when relevant.

For every omitted dimension record either the proof that the result is invariant or the unresolved hypothesis. A missing dimension is not itself a finding; it becomes security-relevant only when omitted identity can change the result and reuse occurs.

## Key-construction trace

Record the exact primitive/object values selected as canonical key inputs before transformation. Then trace the implementation operations in order: extraction, normalization, sorting, case folding, encoding, escaping, canonicalization, serialization, hashing/truncation, versioning, prefix/tag selection, and final key bytes.

For wrapper objects or requests, record what is serialized versus what the cached callback can still read from live context. Capture the proof source for each transformation: source code, framework configuration, deterministic instrumentation, or observed mock key output.

## Canonicalization and serialization trace

Test whether intentional semantic equivalents converge and whether security-distinct identities remain separate. Record transformation order when operations are non-commutative. Compare representative synthetic values before and after canonicalization and serialization, including neighboring values that differ in exactly one security-relevant dimension.

A collision is meaningful only when the safe oracle expects different security-relevant results. Canonical equivalence with equal results is a benign control, not a defect.

## Namespace and entry-identity trace

Record the full entry selector, not only visible key text. Include cache name, partition/shard, namespace, tenant/user prefix, version, policy generation, resource generation, key bytes, and any implicit framework scoping that affects entry selection.

The cache entry identity should answer: which exact stored object would be reused, under which namespace and generation, and why does the reader map to that same object? If a framework isolates identical key bytes by tenant or request scope, capture that as a false-positive control.

## Writer and reader provenance trace

Record the synthetic writer principal/context, semantic invocation, write generation, stored result provenance, result type, and entry identity. Then record the reader principal/context, semantic invocation, read generation, and the contract that permits or forbids reuse.

Treat data results, authorization/policy decisions, memoized derived objects, and deduplication/suppression entries separately. Writer context != reader context does not automatically imply a finding; the result may be globally invariant. The proof must bind context differences to an expected result difference.

## First-writer and replay-order trace

Run paired controls:

`A -> B`: context A populates the entry, then context B requests the computation.

`B -> A`: context B populates first, then context A requests the computation.

Record key, namespace, entry identity, stored result provenance, reader result, and request generation for both orders. A result that follows the first writer is strong causal evidence of cache reuse; a stable correct result in both orders is a positive control.

Also record whether an existing entry was explicitly cleared between order controls. Do not mistake fixture contamination for first-writer behavior.

## Lifecycle and invalidation-generation trace

Track invalidation generation separately from TTL. Record write generation, read generation, explicit invalidation generation, policy/resource generation, restart/worker generation, and any distributed propagation state relevant to reuse.

Use deterministic synthetic transitions such as a role-generation update, policy-generation increment, resource replacement generation, or mock deployment/schema generation. Verify which event should make the old entry unusable and whether the cache identity or invalidation mechanism enforces that transition.

A fresh timestamp does not prove a value belongs to the current authority/resource generation. Conversely, a long-lived entry can be safe when all security-relevant dependencies remain invariant.

## Result and effect binding

Bind the observed replay to the exact cache entry and semantic requests. Record writer request generation, entry identity, stored result identifier, reader request generation, replayed result identifier, and any bounded synthetic decision/effect.

Prefer inert markers or read-only synthetic decisions. If a reversible owner-controlled effect is used, prove that it follows the replayed result rather than an independent policy path. Never increase impact merely to raise evidence level.

## Controlled validation

Use paired synthetic principals/tenants and neighboring synthetic resources. A typical validation sequence is:

1. run a same-context positive control proving legitimate cache reuse;
2. run a different-context negative control expected to produce a distinct result;
3. capture key/namespace/entry identity for both;
4. execute A -> B and B -> A order controls;
5. change one dependency at a time while holding all other state constant;
6. advance a deterministic policy/resource/invalidation generation;
7. test corrected primitive key material, corrected namespace, or corrected invalidation generation;
8. verify the fix preserves legitimate same-context cache hits.

All validation remains synthetic, read-only, inert, or reversible owner-controlled.

## False-positive controls

Rule out intentionally global/invariant computation, hidden namespace isolation, a second upstream/downstream cache, fixture contamination, asynchronous propagation delay, request/result correlation error, canonicalization at a different layer, documented sticky-session behavior, retry/duplicate delivery, safe rejection of unsupported non-serializable arguments, and use of a different policy/resource generation than the one attributed to the observed entry.

Record every surviving alternative explanation. Do not promote an unexplained cache-like symptom to a direct replay finding.

## Counterfactual controls

Change exactly one security-relevant dimension while holding the rest constant:

- synthetic principal;
- tenant namespace;
- neighboring synthetic resource;
- policy or resource generation;
- canonical representation of the same intended value;
- writer/reader order;
- corrected primitive key input;
- explicit invalidation generation.

For each counterfactual record the expected oracle, observed key/entry identity, replayed result, and the alternative explanation it rules in or out.

## Evidence capture

Capture the semantic dependency trace, canonical key inputs, transformation order, serialized key, namespace, cache entry identity, writer context, stored result provenance, reader context, write/read/invalidation generations, A -> B and B -> A results, counterfactual controls, alternative explanations, remediation oracle, and evidence ceiling.

Use synthetic identifiers and redacted fixture labels. Do not record real secrets, real customer data, or third-party telemetry.

## Evidence promotion and ceiling

Promote only to the highest directly demonstrated level:

- K0: cache surface only;
- K1: dependency/key divergence without observed identity collision;
- K2: deterministic identity collision across security-distinct synthetic invocations;
- K3: inert/read-only replay across contexts where the safe oracle expects different outputs;
- K4: bounded reversible owner-controlled security-relevant decision/effect caused by wrong replay;
- K5: K4 plus reverse-order proof, writer/reader provenance, lifecycle/invalidation-generation control, alternative-explanation elimination, remediation, and regression preserving legitimate cache reuse.

Always state why the current evidence ceiling applies. Key equality alone is capped below K3; a stale-looking value without direct entry/result binding is not lifecycle proof.

## Remediation checks

Re-run positive, negative, reverse-order, generation, and counterfactual controls after remediation. Verify that corrected primitive key material, namespace scoping, or invalidation generation removes cross-context or stale reuse while intended same-context hits remain reusable.

Confirm that the remediation does not merely disable caching globally unless that is the explicitly intended design. Preserve legitimate performance behavior where it can remain safe, and record the exact identity dimension or lifecycle transition that now separates entries.
