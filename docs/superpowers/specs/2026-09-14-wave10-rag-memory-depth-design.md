# Wave 10 RAG and Memory Isolation Depth Design

## Goal

Promote `rag-memory-data-isolation-analysis` into the tenth CI-enforced operator-depth profile and make it reason about identity binding, derived-state lineage, lifecycle transitions, revocation/deletion, and bounded leakage evidence rather than treating a returned canary as sufficient proof by itself.

## Scope

Change only the canonical RAG/memory skill, its new local operator artifacts, the operator-depth registry/docs, README current-profile count, and a dedicated depth test. Do not change skill metadata, graph edges, packs, routing domains, benchmark fixtures or thresholds, or evaluator oracles.

## Isolation state model

Trace the complete lifecycle:

`principal -> source object -> authorization snapshot -> chunk/summary -> embedding/index/cache key -> retrieval candidate -> ACL/filter decision -> rerank/context -> model output -> memory writeback -> retention/revocation/deletion state`

Every derived representation must remain bound to the owning principal/tenant, source object, authorization context, lifecycle generation, and revocation/deletion state needed by the policy that consumes it.

## Required reasoning contracts

### Identity-binding model

Distinguish authenticated principal, tenant, session, source owner, object ACL, index namespace, cache key, memory owner, and effective retrieval principal. A namespace match is not authorization proof; a filter is not sufficient unless its input identity and consumed result are demonstrated.

### Derived-state lineage

Track source object identity into chunks, embeddings, summaries, caches, citations, memory records, and compacted state. Record which security-relevant fields survive each derivation and where stale or orphaned derived state can outlive its source authorization.

### Lifecycle and revocation model

Treat permission change, tenant move, deletion, retention expiry, reindex, cache invalidation, summary rewrite, and session reset as state transitions. Record expected convergence and characterize bounded propagation delay rather than labeling every temporary mismatch as permanent isolation failure.

### Leakage evidence ladder

Use an observable ladder:

- `R0` semantically similar content is returned without the unique canary;
- `R1` unique synthetic canary appears in a candidate/debug trace but is blocked before user-visible context;
- `R2` canary reaches retrieved context/citation under the wrong synthetic principal;
- `R3` canary appears in the wrong principal's model-visible/user-visible result with source lineage;
- `R4` stale/revoked/deleted canary remains accessible beyond the documented bounded convergence window;
- `R5` a repeatable cross-context path is causally tied to a specific identity/filter/cache/memory lifecycle defect and survives false-positive controls.

Claims may not exceed the highest demonstrated level.

### Counterfactual and contamination controls

Vary one causal dimension at a time: principal, tenant, ACL, namespace, cache generation, memory state, deletion generation, or filter state. Use fresh-index/fresh-cache controls to distinguish stale derived data from authorization failure, and unique synthetic canaries to distinguish retrieval from model prior knowledge.

## Operator runbook requirements

Retain common sections:

- Attack surface
- Hypothesis matrix
- Controlled validation
- False-positive controls
- Evidence capture
- Remediation checks

Add domain-specific sections:

- Identity and ownership binding
- Derived-state lineage
- Retrieval decision trace
- Lifecycle and revocation trace
- Cache and memory coherence
- Counterfactual isolation controls
- Evidence promotion and ceiling

All validation uses synthetic users/tenants, unique canaries, controlled indexes, mock caches, and owned test data only.

## Scenario contract

Each scenario retains the common operator-depth fields and additionally includes:

- `principal_binding`
- `source_lineage`
- `derived_state_trace`
- `retrieval_policy_trace`
- `lifecycle_state`
- `cache_memory_state`
- `counterfactual_control`
- `alternative_explanation`
- `leakage_level`
- `evidence_ceiling`

At least three deterministic scenarios cover cross-tenant retrieval isolation, revocation/deletion convergence, and stale cache/memory coherence.

## Documentation contract

Wave 8 history remains eight profiles; Wave 10 first added prompt-injection as profile nine and this phase adds RAG/memory isolation as profile ten. Registry schema version remains `2`.

## Acceptance criteria

1. Dedicated test is committed first and produces clean expected RED failures only.
2. Canonical skill exposes identity binding, derived lineage, lifecycle state, R0-R5 ladder, counterfactuals, and evidence ceiling.
3. Runbook and at least three scenarios satisfy the common operator-depth validator plus RAG-specific test fields.
4. Registry validates exactly ten profiles.
5. README/docs reflect current ten-profile state without rewriting Wave 8 history.
6. Exact-head Linux/macOS/Windows matrix, benchmark-core, agent-eval-core, and superiority-court-core all pass.
7. No graph, pack, routing, benchmark-oracle, threshold, or evaluator-oracle file changes.