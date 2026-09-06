# Wave 5 Security Skill Evaluation & Benchmark Engine Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a deterministic, dependency-free benchmark/conformance layer that measures routing quality, evidence-state correctness, authorization behavior, false-positive control, domain isolation, reproducibility, and portability for the existing Security Skills graph.

**Architecture:** Benchmark fixtures wrap existing research-case inputs plus expected validator/router constraints. `benchmark_core.py` evaluates fixtures by calling the production `validate_case()` and `route_case()` functions directly, applies hard gates and weighted metrics, and returns normalized deterministic result objects. Static corpus validation, CLI running, Markdown reporting, schemas, 36 reviewed fixtures, and CI integration compose around that core without duplicating graph/router logic.

**Tech Stack:** Python 3.11/3.13 standard library only, JSON, Markdown, unittest, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-09-06-wave5-evaluation-benchmark-engine-design.md`

## Global Constraints

- No third-party Python dependencies.
- No network access is required by benchmark execution.
- Benchmark fixtures are synthetic or controlled and contain no deployable exploit payloads or live external targets.
- Existing `SKILL.md`, graph, pack, research-case, and router contracts remain source truth.
- `core` starts with exactly 36 fixtures: six per category across authorization, domain-isolation, evidence, false-positive, remediation, and routing.
- `core.minimum_score` is 95.0 and cannot be lowered by a runtime flag.
- A suite passes only when `hard_gate_failures == 0` and `overall_score >= minimum_score`.
- Machine results omit timestamps, hostnames, random IDs, absolute paths, and temp paths.
- Portability suite must pass on Linux/macOS/Windows under Python 3.11 and 3.13.

---

### Task 1: Benchmark core contracts and scoring

**Files:**
- Create: `scripts/benchmark_core.py`
- Test: `tests/test_benchmark_core.py`

**Interfaces:**
- Consumes: `research_case.validate_case(case)`, `route_skills.route_case(root, case, limit=...)`, `security_graph.load_graph_entries(root)`, `security_graph.load_packs(root)`.
- Produces: `evaluate_fixture(root: Path, fixture: dict) -> dict`, `evaluate_suite(root: Path, suite: dict, fixtures: list[dict]) -> dict`, `normalize_result(result: dict) -> str`.

- [ ] **Step 1: Write failing tests for valid routing recall/precision, forbidden outputs, prerequisite ordering, invalid-case evidence conformance, authorization hard gate, and deterministic normalization.**

Representative test:

```python
def test_invalid_unauthorized_fixture_passes_when_rejected(self):
    fixture = make_fixture(case_valid=False, hard_gates=['authorization'])
    fixture['case']['scope']['authorized'] = False
    result = evaluate_fixture(ROOT, fixture)
    self.assertTrue(result['passed'])
    self.assertEqual(result['metrics']['evidence_conformance'], 100.0)
    self.assertEqual(result['hard_gate_failures'], [])
```

- [ ] **Step 2: Run `python -m unittest tests.test_benchmark_core -v` and verify RED because `benchmark_core` does not exist.**
- [ ] **Step 3: Implement only the metric/hard-gate behavior required by the failing tests.**
- [ ] **Step 4: Re-run targeted tests until GREEN, then run all existing tests.**
- [ ] **Step 5: Commit `feat: add deterministic benchmark scoring core`.**

### Task 2: Static benchmark corpus validation and schemas

**Files:**
- Create: `scripts/validate_benchmarks.py`
- Create: `schemas/benchmark-case.schema.json`
- Create: `schemas/benchmark-result.schema.json`
- Test: `tests/test_validate_benchmarks.py`

**Interfaces:**
- Consumes: benchmark fixture/suite JSON, production graph/pack names, `validate_case`.
- Produces: `validate_fixture(root: Path, fixture: dict, source: str) -> list[BenchmarkIssue]`, `validate_corpus(root: Path) -> list[BenchmarkIssue]`, CLI exit code 0/1.

- [ ] **Step 1: Write failing tests for duplicate IDs, unknown skill/pack refs, malformed `ordered_before`, unknown hard gates/metrics, invalid minimum score, orphan fixture detection, and deliberate invalid research cases.**
- [ ] **Step 2: Run targeted validator tests and confirm RED.**
- [ ] **Step 3: Implement dependency-free validator and JSON schema documents matching runtime names exactly.**
- [ ] **Step 4: Run targeted + full unittest suite until GREEN.**
- [ ] **Step 5: Commit `feat: validate benchmark corpus contracts`.**

### Task 3: Runner, deterministic JSON output, and Markdown report

**Files:**
- Create: `scripts/run_benchmarks.py`
- Create: `scripts/benchmark_report.py`
- Test: `tests/test_run_benchmarks.py`
- Test: `tests/test_benchmark_report.py`

**Interfaces:**
- Consumes: validated suite manifest, fixtures, `evaluate_suite()`.
- Produces: CLI exit 0 pass / 1 benchmark fail / 2 malformed input; optional JSON and Markdown files; `render_report(result: dict) -> str`.

- [ ] **Step 1: Write failing tests for exit codes, byte-identical JSON across two runs, stable fixture ordering, and reports that always expose hard-gate/failed-fixture details.**
- [ ] **Step 2: Verify RED.**
- [ ] **Step 3: Implement runner/report with stable JSON (`sort_keys=True`, fixed separators/indent policy) and no environment metadata.**
- [ ] **Step 4: Verify targeted + full tests GREEN.**
- [ ] **Step 5: Commit `feat: add benchmark runner and deterministic reports`.**

### Task 4: Initial 36-fixture benchmark corpus and suites

**Files:**
- Create: `benchmarks/README.md`
- Create: `benchmarks/cases/authorization/*.json` (6)
- Create: `benchmarks/cases/domain-isolation/*.json` (6)
- Create: `benchmarks/cases/evidence/*.json` (6)
- Create: `benchmarks/cases/false-positive/*.json` (6)
- Create: `benchmarks/cases/remediation/*.json` (6)
- Create: `benchmarks/cases/routing/*.json` (6)
- Create: `benchmarks/suites/core.json`
- Create: `benchmarks/suites/portability.json`
- Test: `tests/test_benchmark_corpus.py`

**Interfaces:**
- Consumes: Wave 4 graph/router/case contracts.
- Produces: exactly 36 valid source fixtures; core suite covering all 36; portability subset covering representative OS/path/determinism cases.

- [ ] **Step 1: Write failing corpus-count/category/suite-membership tests before creating fixture files.**
- [ ] **Step 2: Verify RED because corpus is absent.**
- [ ] **Step 3: Add six meaningfully different fixtures per category with explicit expected required/optional/forbidden skills and packs where applicable.**
- [ ] **Step 4: Run `validate_benchmarks.py`, corpus tests, core suite, portability suite, and full tests; tune fixture expectations only when production behavior proves the original expectation wrong and the revised expectation still matches the spec.**
- [ ] **Step 5: Commit `test: add wave5 benchmark corpus`.**

### Task 5: Documentation and agent integration

**Files:**
- Modify: `README.md`
- Modify: `AGENTS.md`
- Modify: `CONTRIBUTING.md`
- Create: `docs/benchmark-contract.md`

**Interfaces:**
- Produces: discoverable commands, fixture-authoring rules, hard-gate semantics, and source-of-truth guidance for maintainers/agents.

- [ ] **Step 1: Add a failing documentation-presence test only for machine-critical command/path references if needed; do not test prose style.**
- [ ] **Step 2: Document benchmark validation/run commands, 36-fixture policy, no-live-target rule, hard gates, and extension boundary for future agent observations/LLM judges.**
- [ ] **Step 3: Run full validation/tests and `git diff --check`.**
- [ ] **Step 4: Commit `docs: document benchmark evaluation layer`.**

### Task 6: CI regression gates

**Files:**
- Modify: `.github/workflows/validate.yml`
- Test: `tests/test_benchmark_ci_contract.py`

**Interfaces:**
- Produces: portability suite in all six matrix jobs; separate Ubuntu/Python 3.13 `benchmark-core` job running corpus validation, core suite, and two-run byte-identity check.

- [ ] **Step 1: Write a failing CI-contract test that parses workflow text and asserts benchmark validator + portability command + benchmark-core job/core command are present.**
- [ ] **Step 2: Verify RED.**
- [ ] **Step 3: Update workflow minimally to satisfy the contract without duplicating full core work six times.**
- [ ] **Step 4: Run complete local gate: skill/graph validation, generated index build/check, benchmark validation, portability suite, core suite twice with byte comparison, all unittests, canonical JSON parse, and `git diff --check`.**
- [ ] **Step 5: Commit `ci: gate security skill benchmark regressions`.**

### Task 7: Publish, PR verification, and merge

**Files:**
- No new implementation files unless CI exposes a real regression.

**Interfaces:**
- Produces: Wave 5 PR from `wave5/evaluation-benchmark-engine` to `main`, server-side CI evidence, squash merge only after green, independent post-merge main verification.

- [ ] **Step 1: Compare branch with `main` and confirm no generated benchmark results or unrelated artifacts are tracked.**
- [ ] **Step 2: Push/publish the verified tree and create PR with exact counts/scores from the final local gate.**
- [ ] **Step 3: Wait for/inspect all six portability matrix jobs plus `benchmark-core`; fix failures on branch rather than bypassing gates.**
- [ ] **Step 4: Re-check PR head SHA and mergeable state; squash merge with expected head SHA.**
- [ ] **Step 5: Check post-merge `main` CI independently and report only observed success states.**
