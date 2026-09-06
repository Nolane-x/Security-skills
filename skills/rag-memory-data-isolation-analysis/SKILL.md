---
name: rag-memory-data-isolation-analysis
description: "Analyze AI RAG and memory isolation across users, tenants, sessions, documents, vector indexes, caches, summaries, embeddings, citations, deletion, and retention. Use synthetic canary facts to detect cross-context leakage."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Rag Memory Data Isolation Analysis

Perform any dynamic validation only in an authorized, owned lab or equivalent explicitly scoped test environment.

## When to use

Use when an AI system stores or retrieves conversation memory, documents, vector embeddings, shared knowledge bases, summaries, caches, or long-lived user context.

## Preconditions

1. Create synthetic users/tenants and canary documents/facts.
2. Document index namespaces, ACL filters, session/user identifiers, retention/deletion policy, and embedding/cache layers.
3. Never seed real secrets as leakage canaries.

## Workflow

1. Map ingestion from principal/document → chunk/metadata → embedding/index namespace → retrieval filters → reranker → prompt → memory writeback/cache.
2. Identify the canonical authorization context and every derived index/cache key.
3. Seed unique synthetic canaries in separate users/tenants and query semantically adjacent topics from other contexts.
4. Test deletion/revocation, permission changes, session reset, and cache invalidation with the synthetic canaries.
5. Distinguish model memorization/general knowledge from retrieval leakage using citations/source IDs and controlled uniqueness.
6. Check summaries/memory compaction for lost ACL/tenant metadata.
7. Route key-collision findings to cache identity and policy gaps to multi-tenant authorization analysis.

## Evidence contract

Record synthetic canary, owner/tenant, storage/index identifiers, retrieval request principal, filter trace, returned source/citation, and controls. Similar semantic content without the unique canary is not leakage proof.

## Stop conditions

Stop if testing could expose real users’ documents/conversations or requires broad production index searches.

## Output

```text
RAG/memory architecture:
principal/tenant:
synthetic canary:
index/cache keys:
retrieval filters:
deletion/revocation result:
cross-context controls:
evidence status:
```
