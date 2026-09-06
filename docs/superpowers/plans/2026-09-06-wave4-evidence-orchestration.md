# Wave 4 Evidence Orchestration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the static 73-skill graph into an evidence-aware research substrate that can represent a security case, enforce claim-state transitions, preserve controls/uncertainty, and deterministically recommend relevant skills without executing intrusive actions.

**Architecture:** Keep canonical skills portable. Add dependency-free Python modules for a machine-readable research-case contract and graph-based route recommendation. Add orchestration skills that teach agents how to maintain the same state/claim discipline when no CLI integration is available.

**Tech Stack:** Python 3.11+, JSON, unittest, Markdown, existing Security Skills graph.

**Spec:** `docs/architecture.md` and `docs/graph-contract.md`

## Global Constraints

- Routing is advisory and cannot grant authorization.
- A case cannot advance evidence state without the required evidence fields/controls.
- Machine routing does not execute security tools, payloads, network actions, or external writes.
- Output must be deterministic for the same canonical graph and case input.
- No third-party Python dependencies.

---

### Task 1: Research-case state model

**Files:** create `scripts/research_case.py`; create `tests/test_research_case.py`; create `docs/research-case-contract.md`.

- [ ] Write failing tests for case parsing, legal/illegal state transitions, scope gate, validated-evidence requirements, and regression-verified requirements.
- [ ] Run tests and confirm RED failures.
- [ ] Implement minimal state model and validator.
- [ ] Run targeted/full tests.

### Task 2: Deterministic skill routing

**Files:** create `scripts/route_skills.py`; create `tests/test_route_skills.py`.

- [ ] Write failing tests for authorization-first routing, domain matching, prerequisite closure/order, evidence-stage-aware recommendations, and deterministic output.
- [ ] Run tests and confirm RED failures.
- [ ] Implement graph-based advisory routing.
- [ ] Run targeted/full tests.

### Task 3: Orchestration skill pack

**Files:** add 10 orchestration/verification skills plus `packs/autonomous-research-orchestration.json` and sidecars.

- [ ] Add case-management, controlled-experiment, evidence-ledger, false-positive, static-dynamic correlation, environment capture, route selection, root-cause/impact separation, fix validation, and reporting skills.
- [ ] Validate portable skill and graph contracts.

### Task 4: Documentation and full gate

**Files:** update `README.md`, `docs/architecture.md`, `CONTRIBUTING.md` as needed.

- [ ] Document case JSON and routing behavior.
- [ ] Run all skill/graph/catalog tests and canonical JSON parse.
- [ ] Run `git diff --check`.
