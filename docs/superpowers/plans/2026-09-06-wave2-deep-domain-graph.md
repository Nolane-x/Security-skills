# Wave 2 Deep Domain Graph Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Expand Security-skills from a 14-skill foundation into a 40+ skill structured security-research graph with domain packs, machine-readable relationships, deterministic validation, and evidence-first workflows.

**Architecture:** Keep every portable capability canonical under `skills/<name>/SKILL.md`. Add `skill.meta.json` sidecars for graph-only metadata that must not pollute Agent Skills frontmatter, plus pack manifests under `packs/`. Dependency-free Python validates graph integrity and deterministically generates `GRAPH.md`/`graph.json`; CI verifies both canonical skill syntax and graph structure.

**Tech Stack:** Markdown, JSON, dependency-free Python 3.11+, unittest, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-09-06-security-skills-foundation-design.md`

## Global Constraints

- Canonical skill content stays vendor-neutral and portable.
- No destructive payloads, persistence, credential theft, stealth, or operational intrusion instructions.
- Intrusive research requires local/owned/sandboxed/CTF/explicitly authorized scope.
- Findings progress through hypothesis -> observed -> validated -> regression-verified.
- Graph generation and validation must be deterministic and dependency-free.
- Unknown prerequisite references and prerequisite cycles are hard errors.

---

### Task 1: Graph contract and TDD validator

**Files:** create `scripts/graphlib.py`, `scripts/validate_graph.py`, `scripts/build_graph.py`; create `tests/test_graphlib.py`, `tests/test_build_graph.py`; create `docs/graph-contract.md`.

**Interfaces:** `load_skill_meta(path) -> dict`, `validate_graph(root) -> list[GraphIssue]`, `build_graph_data(root) -> dict`.

- [ ] Write failing tests for missing sidecars, unknown prerequisite, cycle detection, valid graph, deterministic build.
- [ ] Run tests and confirm graph tests fail before implementation.
- [ ] Implement dependency-free graph parsing/validation/building.
- [ ] Run graph tests and full suite.
- [ ] Commit locally.

### Task 2: Add machine-readable metadata to all existing skills

**Files:** create `skills/*/skill.meta.json` for all foundation skills; create initial `packs/*.json` manifests.

**Interfaces:** every sidecar uses schema version 1 and fields `maturity`, `domains`, `prerequisites`, `composes_with`, `evidence_stage`.

- [ ] Add sidecars with acyclic prerequisites.
- [ ] Add initial pack manifests and validate pack references.
- [ ] Run graph validator.
- [ ] Commit locally.

### Task 3: Add deep technique skills

**Files:** create technique skill directories for sanitizer-guided analysis, exploitability triage, differential testing, grammar/stateful fuzzing, harness design, corpus engineering, variant hunting, and regression matrices.

- [ ] Write canonical SKILL.md files with all required sections.
- [ ] Add sidecar graph metadata.
- [ ] Validate skill and graph contracts.
- [ ] Commit locally.

### Task 4: Add deep vulnerability-pattern skills

**Files:** create domain skills for lifetime, bounds/integer, type confusion, concurrency, parser state, canonicalization, authorization, confused deputy, cache identity, deserialization trust, and protocol state machines.

- [ ] Encode reusable hypothesis models and evidence contracts.
- [ ] Keep exploitability analysis benign and non-weaponizing.
- [ ] Add metadata and pack membership.
- [ ] Validate.
- [ ] Commit locally.

### Task 5: Add kernel/sandbox/browser/cloud packs

**Files:** create kernel attack-surface, driver IOCTL, sandbox boundary, browser process boundary, JIT invariant, container isolation, cloud IAM path, supply-chain dependency, and secrets/token flow skills.

- [ ] Encode domain-specific trust boundaries and stop conditions.
- [ ] Add metadata and pack manifests.
- [ ] Validate.
- [ ] Commit locally.

### Task 6: Sources, docs, generated graph, and CI

**Files:** modify `README.md`, `docs/architecture.md`, `sources/research-systems.json`, `.github/workflows/validate.yml`; generate `GRAPH.md`, `graph.json`, `CATALOG.md`, `catalog.json`.

- [ ] Add authoritative methodology sources and lineage notes.
- [ ] Add graph validation/check commands to CI.
- [ ] Generate graph/catalog outputs.
- [ ] Run full verification: skill validator, graph validator, both stale checks, unittest, `git diff --check`.
- [ ] Commit locally and prepare stacked GitHub PR.

## Implementation note: generated indexes

Wave 2 intentionally treats `CATALOG.md`, `catalog.json`, `GRAPH.md`, and `graph.json` as build artifacts rather than source-controlled truth. CI generates them from canonical skills/sidecars/packs and immediately runs the deterministic `--check` gates. This removes a second mutable source of truth while preserving reproducible human and machine indexes.
