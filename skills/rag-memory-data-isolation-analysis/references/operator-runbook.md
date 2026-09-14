# RAG and Memory Data Isolation Operator Runbook

This runbook deepens `rag-memory-data-isolation-analysis` for owned, local, sandboxed, benchmark/CTF, simulated, or explicitly authorized systems. Use synthetic principals, synthetic tenants, unique test canaries, dedicated indexes, mock caches, and controlled memory stores. The objective is to prove or disprove identity/lifecycle isolation at observable boundaries without searching real-user data.

## Attack surface

Model the system as an identity-bound lifecycle graph, not only as a vector search call.

Inventory:

- authenticated users, tenants, service identities, sessions, conversation IDs, and the **effective retrieval principal**;
- source objects, source owners, ACLs, policy versions, tenant bindings, and retention state;
- ingestion jobs, chunkers, parsers, summarizers, embedding workers, indexers, rerankers, context builders, and citation renderers;
- vector/index namespaces, metadata filters, ACL filters, hybrid-search stores, cache layers, query-result caches, and cache generations;
- memory writes, memory retrieval, conversation summaries, profile stores, compacted state, and memory compaction pipelines;
- deletion queues, revocation propagation, reindex jobs, cache invalidation, lifecycle generation changes, and retention expiry.

For each boundary identify the owner of the data, the principal under which policy is evaluated, the security metadata carried by derived state, and the component that consumes the authorization decision.

## Hypothesis matrix

Express each hypothesis as principal/ownership → derived-state → policy decision → lifecycle consequence.

| Hypothesis class | State transition | Protected invariant | Safe proof signal |
| --- | --- | --- | --- |
| cross-tenant candidate selection | tenant B query against tenant A synthetic object | non-owner candidates must not survive retrieval policy | unique synthetic canary appears only in a controlled candidate/context trace |
| filter identity mismatch | request principal → effective retrieval principal | filter evaluates the initiating synthetic identity/tenant | controlled trace shows the wrong principal bound to ACL/filter evaluation |
| cache key identity omission | authorized query → cached result → neighboring principal | cache entries remain principal/tenant/policy-generation scoped | synthetic canary reappears only through a controlled stale cache path |
| memory ownership loss | synthetic memory write → compaction/readback | memory retains owner, purpose, tenant, and provenance | neighboring synthetic session receives a canary only after ownership metadata is lost |
| revocation lag | ACL/revocation generation change | revoked object becomes unreachable within the bounded convergence window | controlled canary remains reachable after the documented window expires |
| deletion orphan | source deletion → derived chunks/embeddings/summary/cache | deletion invalidates policy-reachable derived representations | controlled deleted canary remains reachable from a dedicated test index after convergence |

If the owner-approved policy does not define expected visibility or a bounded convergence window, keep the result as `needs-policy`/observed timing behavior rather than declaring an isolation defect.

## Identity and ownership binding

Record every identity separately:

```text
requesting_principal:
authenticated_tenant:
session_or_conversation:
source_owner:
source_object_id:
source_acl_generation:
ingestion_identity:
index_namespace:
cache_scope_and_generation:
memory_owner_and_purpose:
effective_retrieval_principal:
```

The effective retrieval principal must be causally derived from the authenticated/requesting context and consumed by the policy layer that gates candidates. A namespace or tenant string by itself is not sufficient evidence of authorization.

For a returned object, prove both directions:

1. the object is bound to the expected source owner and source ACL; and
2. the retrieval decision was evaluated for the expected requesting principal/tenant.

Identity confusion at an intermediate layer is an observation until the wrong binding changes a protected retrieval/memory outcome.

## Derived-state lineage

Maintain **source lineage** from the canonical source object through every derived representation:

```text
source_object_id:
source_owner:
authorization_snapshot:
derivation_type:
derivation_revision:
derived_id:
derived_tenant_or_owner:
policy_generation_binding:
lifecycle_generation:
created_at:
invalidated_at:
downstream_consumers:
```

Apply this to chunks, embeddings, summaries, reranker features, caches, citations, memory records, and compacted conversation state.

A source deletion or ACL change does not automatically remove all derived bytes immediately. The security question is whether stale derived state remains policy-reachable when it should not. Preserve enough reverse lineage to determine which source object and authorization snapshot produced a returned canary.

If source lineage is missing, lower the evidence ceiling because model prior knowledge, another synthetic fixture, or an unrelated duplicate may explain the output.

## Retrieval decision trace

Trace one request hop-by-hop:

```text
requesting_principal:
effective_retrieval_principal:
query_revision:
namespace_selection:
cache_lookup_key_and_generation:
candidate_ids:
candidate_source_lineage:
acl_filter_input:
acl_filter_output:
metadata_filter_input/output:
reranker_input/output:
context_builder_input/output:
source_or_citation_ids:
model_visible_context:
user_visible_result:
```

Distinguish candidate presence from policy-approved context. A unique synthetic canary in a debug candidate that is removed before model-visible context is R1, not a disclosure claim.

When a cache is hit, prove which principal/tenant, authorization snapshot, and lifecycle generation are part of the cache identity. A cache hit can bypass later retrieval filters if the cache contract is incorrectly scoped.

## Lifecycle and revocation trace

Treat authorization and lifecycle changes as generations:

```text
authorization_generation: A_n -> A_n+1
revocation_generation: Rv_n -> Rv_n+1
lifecycle_generation: L_n -> L_n+1
index_generation: I_n -> I_n+1
cache_generation: C_n -> C_n+1
memory_generation: M_n -> M_n+1
```

Record the transition timestamp, expected invalidation steps, and the documented **bounded convergence window**. Query before, during, and after the window using the same synthetic principal pair and canary.

For deletion, distinguish:

- source object unavailable;
- new retrieval candidates suppressed;
- old index representations removed or tombstoned;
- caches invalidated;
- summaries/memory compacted or rewritten;
- citations/source IDs no longer resolve;
- user-visible context denied.

A stale internal representation may be operationally expected during convergence; a policy-reachable stale representation beyond the documented window is stronger evidence.

## Cache and memory coherence

Track cache and memory as independent derived-state stores with their own ownership and generations.

For caches record:

- complete cache key identity, including principal/tenant/policy generation where required;
- value source lineage;
- TTL and invalidation events;
- cache generation and namespace;
- whether a cache hit bypasses ACL/filter evaluation.

For memory record:

- writer principal and tenant;
- memory owner/purpose;
- source provenance;
- memory generation and expiry;
- read-time authorization;
- **memory compaction** or summary generation;
- deletion/reset semantics.

A **stale cache** or compacted memory record can reproduce a canary even when the primary index is correct. Use fresh-cache and fresh-memory controls before attributing a result to the retrieval filter itself.

## Controlled validation

1. **Freeze environment.** Capture model/runtime, retriever/reranker, index version, policy revision, cache/memory generations, and synthetic principals.
2. **Create controlled sources.** Give each synthetic owner/tenant a unique synthetic canary and source object ID.
3. **Establish owner positive control.** The owner retrieves its own canary with source lineage.
4. **Establish non-owner negative control.** A neighboring synthetic principal queries a semantically adjacent topic and must not receive the canary.
5. **Capture retrieval decision trace.** Record candidate, filter, context, citation, and output stages.
6. **Change one state dimension.** Modify ACL, revoke access, delete the source, reset session, invalidate cache, or compact memory.
7. **Track generations and convergence.** Observe behavior before, during, and after the bounded convergence window.
8. **Use fresh-state controls.** Repeat with a fresh cache/index generation or cleared synthetic memory as appropriate.
9. **Use a canary-free semantic control.** Verify similar general content does not masquerade as retrieval leakage.
10. **Assign R-level and evidence ceiling.** Promote only to the directly observed, causally controlled boundary.

Never broaden a test from dedicated fixtures into production-wide searches because a canary was observed.

## False-positive controls

Use controls that separate isolation failure from model behavior and stale infrastructure:

- owner/non-owner principal pair with identical query semantics;
- same tenant versus neighboring tenant pair;
- unique-canary versus canary-free semantically similar source;
- citation/source-lineage present versus absent;
- fresh cache versus stale cache;
- fresh index generation versus pre-transition index generation;
- fresh memory/session versus existing compacted memory;
- before/during/after bounded convergence window;
- ACL restored versus ACL revoked;
- feature disabled versus correctly scoped, so remediation is not mistaken for total service shutdown.

Downgrade or reject the case when an **alternative explanation** better fits: model prior knowledge, duplicate synthetic fixtures, stale test cleanup, expected asynchronous convergence, cache contamination, citation rendering drift, query-semantic differences, or an undocumented policy assumption.

## Counterfactual isolation controls

Target the hypothesized causal field while preserving the rest of the harness.

Useful counterfactuals:

- keep query and source fixed but switch only the effective retrieval principal;
- keep principal fixed but move the source between synthetic tenants;
- keep source/ACL fixed but rotate only cache generation;
- keep cache empty and switch only index generation;
- keep retrieval fixed but clear only the synthetic memory record;
- keep source deleted and compare before versus after the convergence window;
- keep semantics fixed but replace the unique synthetic canary.

A causal identity/filter/cache/memory/lifecycle hypothesis should track the changed variable. If it does not, record the competing explanation and reduce the evidence ceiling.

## Evidence capture

Preserve a compact observable ledger:

```text
case_id:
environment_revision:
requesting_principal:
tenant_and_session:
effective_retrieval_principal:
source_owner_and_object:
unique_synthetic_canary:
authorization_snapshot:
authorization_generation:
revocation_generation:
lifecycle_generation:
derived_state_trace:
index_generation:
cache_generation:
memory_generation:
retrieval_policy_trace:
model_visible_context:
user_visible_result:
source_lineage:
transition_timestamp:
bounded_convergence_window:
fresh_state_control:
canary_free_control:
alternative_explanation:
highest_r_level:
evidence_state:
evidence_ceiling:
```

Machine-captured IDs, policy/filter decisions, cache/memory generations, and source/citation lineage are stronger than screenshots or reconstructed prose.

## Evidence promotion and ceiling

Use both repository evidence state and the R0-R5 ladder:

- **R0:** semantic similarity only; not leakage evidence.
- **R1:** controlled candidate/debug exposure that is blocked before context.
- **R2:** wrong-principal canary reaches retrieved context/citation.
- **R3:** wrong-principal canary reaches model/user-visible output with source lineage.
- **R4:** revoked/deleted/expired canary remains accessible after the bounded convergence window.
- **R5:** repeatable R2-R4 behavior is causally tied to a specific isolation/lifecycle defect and survives controls.

Repository promotion remains:

- **hypothesis** for plausible but unobserved paths;
- **observed** for reproduced relevant behavior with incomplete causality/consequence;
- **validated** for a prohibited isolation boundary causally demonstrated under synthetic controls;
- **regression-verified** when the fixed revision blocks the original path and neighboring allowed controls remain functional.

The **evidence ceiling** is the lower of the directly observed R-level and the repository evidence state justified by identity/source/lifecycle evidence and controls.

## Remediation checks

Prefer repairing the isolation invariant rather than disabling retrieval or memory.

1. **Bind identity end-to-end:** propagate authenticated principal/tenant to the effective retrieval principal and policy consumer.
2. **Bind derived state:** retain source owner, ACL/policy generation, tenant, purpose, and lifecycle generation on chunks, embeddings, summaries, caches, citations, and memory.
3. **Authorize at consumption:** evaluate current authorization before candidate/context use, not only at ingestion time.
4. **Version cache identity:** include principal/tenant and policy/lifecycle generation in cache identity where required; invalidate on relevant transitions.
5. **Govern memory:** enforce owner/purpose/tenant binding, read-time authorization, expiry, reset, and memory-compaction lineage.
6. **Make deletion/revocation convergent:** tombstone or invalidate all policy-reachable derived representations and document the bounded convergence window.
7. **Preserve reverse lineage:** make every retrieved/cached/memory representation traceable to its source object for invalidation and evidence.
8. **Regression test:** replay the original synthetic path, fresh-state counterfactuals, owner positive control, and neighboring non-owner negative control.

A remediation is not successful if it merely removes all retrieval/memory functionality. The intended owner path must continue to work while the prohibited cross-context or stale-lifecycle path is denied.
