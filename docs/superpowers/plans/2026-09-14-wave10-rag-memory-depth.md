# Wave 10 RAG and Memory Isolation Depth Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Promote `rag-memory-data-isolation-analysis` into a tenth CI-enforced operator-depth profile with lifecycle-aware identity/isolation evidence.

**Architecture:** Keep the portable `SKILL.md` as the compact reasoning entry point and place deep lifecycle methodology/scenarios under local `references/`. Freeze semantics with a dedicated unittest and the existing operator-depth registry/validator; preserve graph, routing, benchmark, and evaluator authority unchanged.

**Tech Stack:** Markdown, JSON, Python unittest, existing zero-dependency validators and GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-09-14-wave10-rag-memory-depth-design.md`

## Global Constraints

- Synthetic users, tenants, documents, canaries, indexes, caches, and memory only.
- No broad production searches or real-user data.
- No graph/routing/pack/benchmark/evaluator-oracle changes.
- Dedicated test first; confirm a clean RED before production artifacts.
- Preserve Wave 8 history while updating current registry count to ten.

---

### Task 1: Freeze RED contract

**Files:** Create `tests/test_rag_memory_isolation_depth.py`.

- [ ] Require identity/lifecycle/evidence sections and R0-R5 in the canonical skill.
- [ ] Require domain-specific runbook sections and phrases.
- [ ] Require at least three scenarios with common and RAG-specific fields.
- [ ] Require exact ten-profile registration.
- [ ] Open draft PR and verify failures are expected assertions, not harness errors.

### Task 2: Deepen canonical skill

**Files:** Modify `skills/rag-memory-data-isolation-analysis/SKILL.md`.

- [ ] Add lifecycle state chain, identity-binding model, derived-state lineage, lifecycle/revocation model, R0-R5 evidence ladder, counterfactual/contamination controls, evidence ceiling, and operator-depth link.
- [ ] Keep proof synthetic and explicitly distinguish retrieval evidence from model prior knowledge.

### Task 3: Add operator artifacts

**Files:** Create `references/operator-runbook.md` and `references/operator-scenarios.json` in the skill directory.

- [ ] Implement common operator-depth sections plus identity/ownership, derived-state, retrieval decision, lifecycle/revocation, cache/memory coherence, counterfactual, and evidence-ceiling reasoning.
- [ ] Add deterministic cross-tenant, deletion/revocation, and stale-cache/memory scenarios.

### Task 4: Register profile and synchronize docs

**Files:** Modify `operator-depth/profiles.json`, `docs/operator-depth-contract.md`, and `README.md`.

- [ ] Register the tenth profile using existing common required sections.
- [ ] Preserve Wave 8 eight-profile history and Wave 10 prompt-injection ninth-profile lineage.
- [ ] Update only current profile counts/list and necessary Wave 10 prose.

### Task 5: Exact-head verification and merge

- [ ] Confirm six OS/Python matrix jobs pass.
- [ ] Confirm benchmark-core deterministic double run passes.
- [ ] Confirm agent-eval-core deterministic and negative-profile gates pass.
- [ ] Confirm superiority-court-core deterministic gates pass.
- [ ] Inspect changed-file list and README patch for scope drift.
- [ ] Update PR provenance, mark ready, and merge only with expected exact head SHA.