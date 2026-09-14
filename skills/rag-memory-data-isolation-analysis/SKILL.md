---
name: rag-memory-data-isolation-analysis
description: "Analyze AI RAG and memory isolation across users, tenants, sessions, documents, vector indexes, caches, summaries, embeddings, citations, deletion, and retention. Use synthetic canary facts to detect cross-context leakage."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Rag Memory Data Isolation Analysis

Analyze RAG and memory as a lifecycle of identity-bound derived state rather than as one retrieval query. A unique canary is useful only when its source lineage, requesting principal, authorization state, derived representations, and lifecycle generation are known well enough to distinguish isolation failure from stale state, model prior knowledge, or an expected convergence delay.

## When to use

Use when an AI system stores or retrieves conversation memory, documents, vector embeddings, shared knowledge bases, summaries, caches, citations, or long-lived user context across users, tenants, sessions, permission changes, deletion, or retention transitions.

## Preconditions

1. Create synthetic users/tenants and a unique synthetic canary per source object.
2. Document source ownership, object ACLs, index namespaces, retrieval filters, session/user identifiers, retention/deletion policy, embedding/cache layers, and documented propagation/convergence behavior.
3. Freeze model/runtime, retrieval/index revision, cache generation, memory state, and synthetic identities for each comparison.
4. Never use real user documents, conversations, credentials, or sensitive data as leakage canaries.

## Isolation state model

Trace the complete observable lifecycle:

`principal -> source object -> authorization snapshot -> chunk/summary -> embedding/index/cache key -> retrieval candidate -> ACL/filter decision -> rerank/context -> model output -> memory writeback -> retention/revocation/deletion state`

For each hop, bind the derived representation to the security context required by the next policy consumer. Record the authenticated principal, tenant, session, source owner, object identifier, authorization snapshot, namespace, cache generation, memory owner, lifecycle generation, and **effective retrieval principal**.

Isolation is not proven by namespace separation alone. Likewise, the presence of a filter in configuration is not proof that the correct identity reached that filter or that its result controlled the candidate set actually consumed downstream.

## Identity-binding model

Keep these identities distinct:

- authenticated/requesting principal;
- tenant or organization identity;
- current session/conversation identity;
- source owner and source-object ACL identity;
- ingestion/service identity;
- index namespace and partition identity;
- cache-key and cache-generation identity;
- memory-record owner/purpose identity;
- **effective retrieval principal** used by retrieval policy;
- model/runtime identity, which is not itself the authorization principal.

For every retrieval or memory read, prove how the requesting principal becomes the effective retrieval principal and how that identity is consumed by namespace, ACL, filter, reranker, cache, memory, and citation logic. A mismatch at any hop is an isolation hypothesis, not automatically a validated leak.

## Derived-state lineage

Treat chunks, embeddings, summaries, reranker features, caches, citations, memory records, conversation summaries, and compacted context as **derived representations** of a source object.

For each derived representation record:

- source object and source owner;
- derivation revision and timestamp/generation;
- tenant/principal binding retained;
- authorization snapshot or policy-generation binding;
- lifecycle generation and retention state;
- cache/index namespace and key material;
- reverse link needed for invalidation, revocation, or deletion;
- downstream consumers.

Derived state that outlives its source authorization is not necessarily a leak until it is reachable by a principal who should no longer receive it. Preserve source lineage so a returned canary can be attributed to retrieval/memory rather than model prior knowledge.

## Lifecycle and revocation model

Model permission change, tenant reassignment, source deletion, retention expiry, reindexing, cache invalidation, summary rewrite, memory reset, and session reset as explicit state transitions.

Record:

```text
authorization generation: A_n -> A_n+1
lifecycle generation: L_n -> L_n+1
index generation: I_n -> I_n+1
cache generation: C_n -> C_n+1
memory generation: M_n -> M_n+1
```

Define the documented or owner-approved **bounded convergence window** for asynchronous propagation. During that window, characterize which derived copies can legally remain and which user-visible surfaces must already be denied. After the window, stale accessibility can support a stronger finding.

Do not conflate a stale citation label, stale debug candidate, and a user-visible retrieval result. Record where revocation is enforced and whether stale downstream state is still consumable.

## Leakage evidence ladder

Bound every claim to the highest directly observed level:

- **R0 — semantic similarity only:** related content appears, but the unique synthetic canary and source lineage are absent;
- **R1 — blocked candidate exposure:** the unique canary appears only in a controlled candidate/debug trace and is removed before model-visible or user-visible context;
- **R2 — wrong-context retrieval:** the unique canary reaches retrieved context or citation under the wrong synthetic principal/tenant;
- **R3 — user/model-visible disclosure:** the unique canary appears in the wrong principal's model-visible or user-visible result with source lineage tying it to the test object;
- **R4 — lifecycle persistence:** a revoked/deleted/expired canary remains reachable beyond the documented bounded convergence window;
- **R5 — causal isolation defect:** a repeatable R2-R4 path is causally tied to a specific identity, filter, cache, memory, namespace, or lifecycle defect and survives false-positive/counterfactual controls.

`R0 != R1 != R2 != R3 != R4 != R5`. A semantically similar answer is not leakage proof. A debug candidate blocked before context is different from a user-visible disclosure. R4 additionally requires lifecycle timing evidence.

## Counterfactual and contamination controls

Change one causal dimension while holding the rest of the harness fixed:

- requesting principal or tenant only;
- source-object ACL generation only;
- namespace or filter binding only;
- cache generation only;
- memory state/generation only;
- deletion/revocation generation only;
- fresh index/cache versus stale derived state;
- same semantic topic with a different unique synthetic canary.

Use a fresh-index/fresh-cache/fresh-memory control to detect stale derived state. Use a canary-free semantically similar control to distinguish general model knowledge from retrieval. Use source IDs/citations or controlled retrieval traces to tie a canary to the intended synthetic object.

## Evidence ceiling

Set an explicit evidence ceiling using both the R-level and repository evidence state. Promotion is limited by the weaker of the two.

- R0 cannot support a leakage claim.
- R1 can demonstrate a candidate-selection or filtering observation but not disclosure.
- R2/R3 require identity/source lineage and controls before `validated` promotion.
- R4 requires proof that the bounded convergence window has expired and that the stale representation remained policy-reachable.
- R5 requires a causal defect plus counterfactual evidence and neighboring allowed controls.

Do not overstate severity from a unique canary alone. State which representation leaked, under which principal, at which lifecycle generation, and through which policy consumer.

## Workflow

1. Map ingestion, derivation, retrieval, context, memory writeback, and lifecycle transitions using the isolation state model.
2. Establish synthetic owners/tenants and seed a different unique canary into each controlled source object.
3. Record authorization, lifecycle, index, cache, and memory generations before testing.
4. Prove the owning principal positive control and a neighboring non-owner negative control.
5. Trace the effective retrieval principal through namespace, candidate selection, ACL/filter decision, reranking, context construction, and citation/source attribution.
6. Test one lifecycle transition at a time: ACL change, tenant move, revocation, deletion, retention expiry, session reset, cache invalidation, or memory compaction.
7. Respect the bounded convergence window and record intermediate states rather than immediately labeling asynchronous propagation as a permanent defect.
8. Classify the highest observed R-level and set the evidence ceiling.
9. Run fresh-cache/index/memory and canary-free semantic controls to eliminate stale-state and model-prior explanations.
10. Route confirmed cache-key defects to cache identity analysis and authorization-policy defects to multi-tenant/authorization analysis without inflating this skill's claim.

## Operator depth

For a full authorized assessment, load the [operator runbook](references/operator-runbook.md) and its CI-enforced scenario matrix. They require principal binding, source/derived-state lineage, retrieval policy traces, lifecycle/revocation timing, cache/memory coherence, counterfactual isolation controls, and evidence ceilings using synthetic data only.

## Evidence contract

Record at minimum:

- requesting principal, tenant, session, and effective retrieval principal;
- source owner, source-object ID, source ACL/policy generation, and unique synthetic canary;
- derived representation IDs/generations for chunk, embedding, summary, cache, memory, and citation where applicable;
- namespace, candidate-selection, ACL/filter, reranker, and context-construction trace;
- authorization/lifecycle/index/cache/memory generations;
- revocation/deletion event time and bounded convergence window;
- returned source/citation and highest observed R-level;
- fresh-state and canary-free semantic controls;
- alternative explanations tested;
- evidence state and evidence ceiling.

Similar semantic content without the unique canary and source lineage is not leakage proof.

## Stop conditions

Stop if testing could expose real users' documents or conversations, requires broad production index searches, crosses an unauthorized tenant/account boundary, or would alter real retention/deletion state. Use synthetic fixtures and dedicated test indexes instead.

## Output

```text
RAG/memory architecture:
requesting/effective retrieval principal:
source owner/object:
unique synthetic canary:
authorization + lifecycle generation:
derived-state lineage:
index/cache/memory generations:
retrieval policy trace:
revocation/deletion transition:
bounded convergence window:
highest R-level:
fresh-state control:
canary-free semantic control:
alternative explanations:
evidence status:
evidence ceiling:
remediation invariant:
```
