# Security Skills Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Bootstrap `Nolane-x/Security-skills` as a portable, verification-first Agent Skills library with deterministic validation and an initial foundation skill graph.

**Architecture:** Canonical skills live once under `skills/` and conform to the open Agent Skills format. A dependency-free Python toolchain validates skills and generates a catalog; compatibility documentation maps the canonical format into native skill directories or instruction fallbacks used by current agents.

**Tech Stack:** Markdown, JSON, Python 3.9+ standard library, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-09-06-security-skills-foundation-design.md`

## Global Constraints

- Canonical skill content is stored once under `skills/<name>/`.
- Every skill must be usable without assuming a specific LLM vendor.
- Intrusive security workflows require owned, local, sandboxed, or explicitly authorized targets.
- Finding status must distinguish hypothesis, reproduction, evidence, and confirmation.
- Foundation code has no runtime third-party Python dependencies.
- CI must execute on Linux, macOS, and Windows.
- No placeholders such as TBD/TODO are allowed in committed foundation files.

---

### Task 1: Repository contract and portability documentation

**Files:**
- Create: `README.md`
- Create: `AGENTS.md`
- Create: `SECURITY.md`
- Create: `CONTRIBUTING.md`
- Create: `docs/architecture.md`
- Create: `docs/compatibility.md`
- Create: `docs/sources.md`

**Interfaces:**
- Consumes: approved design.
- Produces: repository-wide conventions consumed by contributors and AI agents.

- [ ] Write the repository contract, architecture, compatibility matrix, security policy, and source registry.
- [ ] Check all documentation links and ensure canonical skills are never duplicated as product-specific forks.
- [ ] Commit documentation with the design and plan.

### Task 2: Dependency-free skill parser and validator

**Files:**
- Create: `scripts/skilllib.py`
- Create: `scripts/validate_skills.py`
- Test: `tests/test_skilllib.py`
- Test: `tests/test_validate_skills.py`

**Interfaces:**
- Produces: `parse_skill(path) -> Skill`, `validate_skill(skill, root) -> list[Issue]`, and repository validation CLI.

- [ ] Write failing parser/validator tests for valid skills and malformed names, descriptions, directories, missing contract sections, and risky metadata.
- [ ] Run tests and confirm failures.
- [ ] Implement parser and validator using only the Python standard library.
- [ ] Run tests and confirm they pass.

### Task 3: Initial foundation skill graph

**Files:**
- Create: `skills/*/SKILL.md`
- Create: focused `references/*.md` for router, fuzzing, validation, and AI-agent security.

**Interfaces:**
- Consumes: canonical skill contract enforced by Task 2.
- Produces: composable skills discoverable by Agent Skills clients.

- [ ] Add the router and authorization boundary skills first.
- [ ] Add discovery skills: attack surface, hypotheses, fuzzing, static/dataflow, symbolic execution, binary reconnaissance.
- [ ] Add verification/remediation skills: crash triage, evidence validation, patch-diff variants, remediation/regression, secure review.
- [ ] Add AI/agent security assessment as the first domain pack.
- [ ] Run validator and fix every error.

### Task 4: Deterministic catalog

**Files:**
- Create: `scripts/build_catalog.py`
- Create: `catalog.json`
- Create: `CATALOG.md`
- Test: `tests/test_build_catalog.py`

**Interfaces:**
- Consumes: parsed canonical skills.
- Produces: machine-readable and human-readable deterministic catalog.

- [ ] Write failing tests for stable ordering and check mode.
- [ ] Implement catalog generation.
- [ ] Generate catalog and run tests.

### Task 5: Cross-platform CI and final verification

**Files:**
- Create: `.github/workflows/validate.yml`
- Create: `.github/copilot-instructions.md`

**Interfaces:**
- Consumes: validator, catalog generator, tests.
- Produces: automated repository gate for future skill additions.

- [ ] Add Linux/macOS/Windows Python matrix CI.
- [ ] Run full local test suite, validator, catalog check, and placeholder scan.
- [ ] Review the generated tree for accidental vendor lock-in or offensive payload content.
- [ ] Publish only after all checks pass.
