# Wave 10 Prompt Injection Boundary Depth Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Promote `prompt-injection-boundary-analysis` into a ninth CI-enforced operator-depth profile with causal authority/provenance reasoning and bounded evidence claims.

**Architecture:** Keep the canonical skill concise while placing deep methodology in local references. Enforce the depth through a dedicated unittest plus the existing operator-depth registry/validator; preserve routing, graph, benchmark, agent-eval, and superiority contracts.

**Tech Stack:** Markdown, JSON, Python unittest, existing repository validators and GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-09-14-wave10-prompt-injection-depth-design.md`

## Global Constraints

- Use only sandboxed, owned, benchmark, CTF, or explicitly authorized contexts.
- Use synthetic instructions, fake identities/data, mocked tools, and inert sinks.
- Do not add live-target, destructive, persistence, credential-access, or safeguard-bypass instructions.
- Do not change graph edges, routing domains, packs, benchmark thresholds, benchmark fixtures, or evaluator oracles.
- Write the dedicated depth test before production artifacts.

---

### Task 1: Freeze the RED depth contract

**Files:**
- Create: `tests/test_prompt_injection_boundary_depth.py`

**Interfaces:**
- Consumes: current `SKILL.md`, absent local runbook/scenarios, `operator-depth/profiles.json`.
- Produces: exact section, field, evidence-ladder, and profile-registration requirements.

- [ ] **Step 1: Write failing tests** requiring the canonical model sections, prompt-specific runbook sections, scenario reasoning fields, `P0` through `P5`, and registry inclusion.
- [ ] **Step 2: Open a draft PR so CI runs the RED contract.**
- [ ] **Step 3: Verify the new tests fail for missing depth artifacts/sections and not for syntax or harness errors.**

### Task 2: Implement canonical skill model

**Files:**
- Modify: `skills/prompt-injection-boundary-analysis/SKILL.md`

**Interfaces:**
- Consumes: Task 1 section/evidence requirements.
- Produces: compact authority/provenance/decision/effect model and operator-depth link.

- [ ] **Step 1: Add instruction-authority and transformation-provenance models.**
- [ ] **Step 2: Add decision/effect ladder `P0`-`P5`, counterfactual proof, alternative explanations, and evidence ceiling.**
- [ ] **Step 3: Keep workflow and evidence contract safe and bounded to synthetic proof.**

### Task 3: Add deep operator artifacts

**Files:**
- Create: `skills/prompt-injection-boundary-analysis/references/operator-runbook.md`
- Create: `skills/prompt-injection-boundary-analysis/references/operator-scenarios.json`

**Interfaces:**
- Consumes: spec reasoning contracts.
- Produces: falsifiable transition-level methodology and deterministic benign scenarios.

- [ ] **Step 1: Write the runbook with common operator-depth sections plus instruction lineage, authority conflict, transformation boundary, decision/effect, counterfactual, and evidence-ceiling sections.**
- [ ] **Step 2: Add at least three scenarios covering provenance preservation, transform-induced authority confusion, and decision/effect claim bounding.**
- [ ] **Step 3: Ensure every scenario includes the common oracle/control/stop/remediation fields and all prompt-specific reasoning fields.**

### Task 4: Register the ninth operator-depth profile

**Files:**
- Modify: `operator-depth/profiles.json`
- Modify: `docs/operator-depth-contract.md`
- Modify: `README.md`

**Interfaces:**
- Consumes: new local runbook/scenario paths.
- Produces: CI enforcement and accurate documentation of Wave 10 second-ring expansion.

- [ ] **Step 1: Register `prompt-injection-boundary-analysis` with the six common required runbook sections.**
- [ ] **Step 2: Document that Wave 8 originally established eight profiles and Wave 10 expands the registry to nine.**
- [ ] **Step 3: Do not alter any unrelated registry entry or historical Wave 8 description.**

### Task 5: Verify exact-head GREEN

**Files:**
- No new files expected.

**Interfaces:**
- Consumes: complete branch.
- Produces: exact-head CI evidence.

- [ ] **Step 1: Verify the dedicated tests pass through CI on Linux, macOS, and Windows.**
- [ ] **Step 2: Verify canonical skill, operator-depth, graph, generated-index, benchmark, portability, and agent-eval matrix steps pass.**
- [ ] **Step 3: Verify benchmark-core, agent-eval-core, and superiority-court-core determinism jobs pass.**
- [ ] **Step 4: Inspect the PR changed-file list and confirm no graph, pack, routing, benchmark fixture, threshold, or oracle files changed.**