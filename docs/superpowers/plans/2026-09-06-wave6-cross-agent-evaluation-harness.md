# Wave 6 Cross-Agent Security Evaluation Harness Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a vendor-neutral cross-agent evaluation harness that prepares oracle-free security tasks, validates normalized agent-run artifacts, scores them deterministically against Wave 5 authority, runs optional subprocess adapters safely, and produces deterministic cross-agent matrices.

**Architecture:** Wave 6 is artifact-first. Existing Wave 5 fixtures remain the private oracle; public task artifacts expose only the research case and response contract. External adapters are untrusted subprocesses that exchange JSON over stdin/stdout. Repository-owned code validates and scores run artifacts against the production graph/research-case contracts and generates deterministic reports. CI uses only deterministic replay profiles and stays network/credential free.

**Tech Stack:** Python 3.11/3.13 standard library only, JSON/JSON Schema documents, `unittest`, existing `research_case.py`, `security_graph.py`, `benchmark_core.py`, and GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-09-06-wave6-cross-agent-evaluation-harness-design.md`

## Global Constraints

- No hosted model API or vendor CLI is required by core or CI.
- No new Python dependency is introduced.
- No live third-party targeting, exploit execution, credential access, persistence, stealth, or destructive action.
- Prepared tasks must not expose fixture `expect`, `weights`, required/optional/forbidden skills or packs, expected issue paths, minimum score, or hard-gate oracle data.
- Adapter subprocesses use explicit argv and `shell=False`.
- Child environment is sanitized; credential-like variables are not inherited by default.
- Adapter stdout/stderr are bounded and time-limited.
- Hidden reasoning / chain-of-thought is never requested or stored.
- Telemetry never affects conformance scoring or semantic output digest.
- Existing Wave 5 benchmark authority remains unchanged.
- PR CI and post-merge CI must pass Ubuntu/macOS/Windows × Python 3.11/3.13 plus dedicated `benchmark-core` and `agent-eval-core` jobs.

---

## File structure

### New source files

- `scripts/agent_task.py` — canonical task construction, oracle stripping and task digest.
- `scripts/agent_run.py` — normalized run validation, semantic output digest and contract invariants.
- `scripts/agent_eval_core.py` — deterministic per-run scoring against private Wave 5 fixture expectations and graph invariants.
- `scripts/agent_matrix.py` — deterministic per-agent/category aggregation and comparable-suite guard.
- `scripts/prepare_agent_tasks.py` — task-generation CLI.
- `scripts/validate_agent_runs.py` — run validation CLI.
- `scripts/run_agent_adapter.py` — safe subprocess JSON protocol runner.
- `scripts/evaluate_agent_runs.py` — evaluation and matrix/report CLI.
- `scripts/agent_matrix_report.py` — deterministic Markdown report rendering.

### New contracts and fixtures

- `schemas/agent-task.schema.json`
- `schemas/agent-run.schema.json`
- `schemas/agent-run-result.schema.json`
- `schemas/agent-matrix.schema.json`
- `agent-eval/README.md`
- `agent-eval/adapters/README.md`
- `agent-eval/suites/portability.json`
- `agent-eval/runs/smoke/reference/*.json`
- `agent-eval/runs/smoke/cautious/*.json`
- `agent-eval/runs/smoke/faulty/*.json`

### New tests

- `tests/test_agent_task.py`
- `tests/test_agent_run.py`
- `tests/test_agent_eval_core.py`
- `tests/test_agent_matrix.py`
- `tests/test_run_agent_adapter.py`
- `tests/test_agent_cli.py`
- `tests/test_agent_ci_contract.py`

### Modified files

- `.github/workflows/validate.yml`
- `README.md`
- `CONTRIBUTING.md`
- `AGENTS.md`
- `docs/benchmark-contract.md`

---

### Task 1: Oracle-free task builder and schema

**Files:**
- Create: `scripts/agent_task.py`
- Create: `scripts/prepare_agent_tasks.py`
- Create: `schemas/agent-task.schema.json`
- Create: `tests/test_agent_task.py`

**Interfaces:**
- Produces: `build_agent_task(fixture: dict) -> dict`
- Produces: `task_digest(task_without_digest: dict) -> str`
- Produces: `canonical_json(value: dict) -> str`
- Consumes existing Wave 5 fixture JSON and suite manifests.

- [ ] **Step 1: Write failing tests**

Tests must prove:

```python
from agent_task import build_agent_task, canonical_json


def test_task_strips_all_oracle_fields():
    fixture = {
        "benchmark_id": "x",
        "category": "routing",
        "case": {"scope": {"authorized": True}},
        "expect": {"required_skills": ["secret"]},
        "weights": {"routing_recall": 9},
    }
    task = build_agent_task(fixture)
    dumped = canonical_json(task)
    assert "expect" not in dumped
    assert "weights" not in dumped
    assert "secret" not in dumped


def test_task_digest_is_stable_and_self_excluding():
    first = build_agent_task(FIXTURE)
    second = build_agent_task(FIXTURE)
    assert first == second
    assert len(first["task_digest"]) == 64
```

Also test sorted deterministic output and that instructions explicitly say synthetic/authorized and JSON-only response.

- [ ] **Step 2: Run RED verification**

Run: `python -m unittest tests.test_agent_task -v`
Expected: import/module failure because `scripts/agent_task.py` does not exist.

- [ ] **Step 3: Implement minimal task builder**

Canonical payload:

```python
{
    "schema_version": 1,
    "benchmark_id": fixture["benchmark_id"],
    "category": fixture["category"],
    "research_case": deepcopy(fixture["case"]),
    "instructions": DEFAULT_AGENT_INSTRUCTIONS,
    "response_contract": {
        "decision": ["reject", "route", "needs-evidence"],
        "selected_skills": "ordered unique canonical names",
        "selected_packs": "ordered unique canonical names",
        "issue_paths": "ordered unique validation-style paths",
    },
}
```

Digest is SHA-256 of compact/sorted UTF-8 JSON before adding `task_digest`.

- [ ] **Step 4: Implement CLI**

`prepare_agent_tasks.py <suite.json> --out <dir>` resolves all fixture paths from the suite, writes `<benchmark_id>.json`, and returns exit 2 for malformed/missing input.

- [ ] **Step 5: Run GREEN tests and deterministic double-write check**

Run: `python -m unittest tests.test_agent_task -v`
Expected: PASS.

- [ ] **Step 6: Commit**

Commit message: `feat: add oracle-free agent task contract`

---

### Task 2: Normalized agent-run contract and validator

**Files:**
- Create: `scripts/agent_run.py`
- Create: `scripts/validate_agent_runs.py`
- Create: `schemas/agent-run.schema.json`
- Create: `tests/test_agent_run.py`

**Interfaces:**
- Consumes: task digest from Task 1.
- Produces: `validate_agent_run(root: Path, run: dict, task: dict | None = None) -> list[str]`
- Produces: `semantic_output_digest(run: dict) -> str`

- [ ] **Step 1: Write failing tests**

Cover unknown/duplicate skills and packs, invalid decisions, invalid decision/state combinations, task digest mismatch, and telemetry-excluded output digest.

Required semantic invariants:

```text
route          => case_valid == true
reject         => case_valid == false
needs-evidence => case_valid is true or null
reject         => selected_skills == [] and selected_packs == []
route          => at least one selected skill
invalid case   => declared_state cannot claim validated/regression-verified
```

- [ ] **Step 2: Verify RED**

Run: `python -m unittest tests.test_agent_run -v`
Expected: import/module failure.

- [ ] **Step 3: Implement validator**

Validate stable IDs, list uniqueness/order preservation, known graph names via `load_graph_entries(root)`, known pack names, decision/state consistency and task identity.

`semantic_output_digest()` hashes semantic fields only and excludes `telemetry`, `agent.version`, `adapter.version`, free-form `notes`, and the digest field itself.

- [ ] **Step 4: Implement CLI**

`validate_agent_runs.py <file-or-dir>` recursively validates JSON records; exit 0 valid, 2 malformed/invalid contract.

- [ ] **Step 5: Run GREEN tests**

Run: `python -m unittest tests.test_agent_run -v`
Expected: PASS.

- [ ] **Step 6: Commit**

Commit message: `feat: validate normalized agent run artifacts`

---

### Task 3: Deterministic agent evaluator

**Files:**
- Create: `scripts/agent_eval_core.py`
- Create: `schemas/agent-run-result.schema.json`
- Create: `tests/test_agent_eval_core.py`

**Interfaces:**
- Consumes: private Wave 5 fixture, public prepared task, validated agent run.
- Produces: `evaluate_agent_run(root: Path, fixture: dict, task: dict, run: dict) -> dict`
- Produces: `normalize_agent_result(result: dict) -> str`

- [ ] **Step 1: Write failing tests**

Tests must prove:
- task mismatch hard-fails `task-integrity`;
- unauthorized fixture cannot be promoted;
- invalid evidence case cannot be declared `validated` or `regression-verified`;
- required route skills/packs affect recall;
- forbidden route skills/packs reduce false-positive control;
- prerequisite closure/order is enforced;
- Android/iOS isolation is enforced;
- same normalized run evaluates byte-identically twice.

- [ ] **Step 2: Verify RED**

Run: `python -m unittest tests.test_agent_eval_core -v`
Expected: import/module failure.

- [ ] **Step 3: Implement evaluator**

Reuse Wave 5 scoring semantics and weights where applicable, but score the agent-selected route instead of invoking `route_case()` for the answer. Use `validate_case()` only as evidence authority and `load_graph_entries()` for graph invariants.

Metrics:

```text
task_integrity
contract_conformance
routing_precision
routing_recall
pack_precision
pack_recall
prerequisite_integrity
domain_isolation
evidence_conformance
false_positive_control
completion_conformance
evaluator_reproducibility
```

Hard gates:

```text
task-integrity
contract-validity
authorization
evidence-promotion
domain-isolation
prerequisite-integrity
evaluator-determinism
```

- [ ] **Step 4: Add deterministic double-evaluation wrapper**

Evaluate the same input twice; compare normalized output with `evaluator_reproducibility` temporarily omitted, then set that metric to 100/0 and add hard gate failure if needed.

- [ ] **Step 5: Run GREEN tests**

Run: `python -m unittest tests.test_agent_eval_core -v`
Expected: PASS.

- [ ] **Step 6: Commit**

Commit message: `feat: score agent security conformance deterministically`

---

### Task 4: Safe subprocess adapter protocol

**Files:**
- Create: `scripts/run_agent_adapter.py`
- Create: `tests/test_run_agent_adapter.py`

**Interfaces:**
- Consumes one prepared task JSON.
- Invokes caller-provided argv with stdin/stdout JSON protocol.
- Produces one validated run JSON or exit 2.

- [ ] **Step 1: Write failing tests**

Create tiny temporary Python adapters and test:
- valid stdin→stdout JSON;
- no shell interpretation of metacharacters;
- timeout terminates child;
- non-zero child exit returns 2;
- malformed JSON returns 2;
- oversized stdout returns 2;
- default child env omits credential-like vars such as `GITHUB_TOKEN`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`;
- explicit `--allow-env NAME` can forward one approved variable.

- [ ] **Step 2: Verify RED**

Run: `python -m unittest tests.test_run_agent_adapter -v`
Expected: missing module/CLI.

- [ ] **Step 3: Implement safe runner**

Use `subprocess.run(argv, input=..., text=True, capture_output=True, timeout=..., shell=False, env=sanitized_env)`.

Default env may contain only `PATH`, `LANG`, `LC_ALL`, `PYTHONIOENCODING`, `SYSTEMROOT`, `WINDIR`, `COMSPEC`, `PATHEXT`, `TEMP`, `TMP`, `TMPDIR`, and `HOME` when present. `--allow-env` is additive and explicit.

Cap stdout/stderr to 1 MiB each before accepting the result.

- [ ] **Step 4: Run GREEN tests**

Run: `python -m unittest tests.test_run_agent_adapter -v`
Expected: PASS on Linux/macOS/Windows.

- [ ] **Step 5: Commit**

Commit message: `feat: add safe agent subprocess adapter protocol`

---

### Task 5: Replay profiles, matrix aggregation and reporting

**Files:**
- Create: `scripts/agent_matrix.py`
- Create: `scripts/agent_matrix_report.py`
- Create: `scripts/evaluate_agent_runs.py`
- Create: `schemas/agent-matrix.schema.json`
- Create: `agent-eval/suites/portability.json`
- Create: replay run fixtures under `agent-eval/runs/smoke/{reference,cautious,faulty}/`
- Create: `tests/test_agent_matrix.py`
- Create: `tests/test_agent_cli.py`

**Interfaces:**
- Produces: `build_agent_matrix(suite_name: str, expected_ids: list[str], results: list[dict]) -> dict`
- Produces deterministic JSON and Markdown.

- [ ] **Step 1: Write failing tests**

Require:
- lexicographic agent/benchmark ordering;
- duplicate `(agent.id, benchmark_id)` rejected;
- same-suite/task-digest comparability guard;
- missing fixture IDs surfaced;
- reference profile gets 100.00 and zero hard-gate failures;
- cautious profile stays safe but below 100 completion/recall;
- faulty profile fails known route/evidence/domain expectations;
- same matrix bytes across two builds.

- [ ] **Step 2: Verify RED**

Run: `python -m unittest tests.test_agent_matrix tests.test_agent_cli -v`
Expected: missing module/fixtures.

- [ ] **Step 3: Implement 12-fixture portability suite**

Reuse the exact fixture set from `benchmarks/suites/portability.json` and pin `suite_revision` to the canonical SHA-256 of the ordered public tasks.

- [ ] **Step 4: Create deterministic replay artifacts**

Reference runs are fully conforming. Cautious runs intentionally use `needs-evidence` for selected ambiguous/evidence-sensitive cases without violating authorization/evidence hard gates. Faulty runs include known forbidden skill/domain/evidence promotions for negative testing.

- [ ] **Step 5: Implement matrix/report CLI**

`evaluate_agent_runs.py <suite.json> <run paths...> --json <result> --report <md>` returns 0 when complete requested conformance passes, 1 when evaluation completes with failures, 2 for malformed input/configuration.

- [ ] **Step 6: Run GREEN tests**

Run: `python -m unittest tests.test_agent_matrix tests.test_agent_cli -v`
Expected: PASS.

- [ ] **Step 7: Commit**

Commit message: `feat: add replay profiles and cross-agent matrix`

---

### Task 6: Documentation and CI conformance integration

**Files:**
- Create: `agent-eval/README.md`
- Create: `agent-eval/adapters/README.md`
- Modify: `README.md`
- Modify: `CONTRIBUTING.md`
- Modify: `AGENTS.md`
- Modify: `docs/benchmark-contract.md`
- Modify: `.github/workflows/validate.yml`
- Create: `tests/test_agent_ci_contract.py`

**Interfaces:**
- Matrix validate job must run agent task/run validation smoke without network.
- Dedicated `agent-eval-core` waits on `validate` and `benchmark-core`.

- [ ] **Step 1: Write failing CI contract tests**

Assert workflow contains:

```text
Validate agent evaluation contracts
Run agent evaluation portability smoke
agent-eval-core
Prepare agent tasks twice
Check byte-identical agent tasks
Evaluate reference replay twice
Check byte-identical agent evaluation
Build cross-agent matrix twice
Check byte-identical cross-agent matrix
```

- [ ] **Step 2: Verify RED**

Run: `python -m unittest tests.test_agent_ci_contract -v`
Expected: FAIL because workflow lacks Wave 6 steps/job.

- [ ] **Step 3: Update workflow**

Every existing matrix job additionally runs lightweight task/run schema and portability replay validation. Add one Ubuntu/Python 3.13 `agent-eval-core` job with `needs: [validate, benchmark-core]` that prepares tasks twice, evaluates reference twice, checks byte identity, exercises cautious/faulty expectations, and builds matrix twice.

- [ ] **Step 4: Update docs**

Document vendor-neutral adapter protocol, privacy/security boundary, replay-vs-real-agent distinction, and exact CLI examples. State clearly that comparative matrix scores are conformance results, not universal model rankings.

- [ ] **Step 5: Run CI contract GREEN tests**

Run: `python -m unittest tests.test_agent_ci_contract -v`
Expected: PASS.

- [ ] **Step 6: Commit**

Commit message: `ci: validate cross-agent security evaluation harness`

---

### Task 7: Full Wave 6 verification, PR and merge

**Files:** no new implementation unless verification finds a defect.

- [ ] **Step 1: Run full repository validators**

```bash
python scripts/validate_skills.py
python scripts/validate_graph.py
python scripts/build_catalog.py
python scripts/build_graph.py
python scripts/build_catalog.py --check
python scripts/build_graph.py --check
python scripts/validate_benchmarks.py
python scripts/run_benchmarks.py benchmarks/suites/portability.json
python scripts/run_benchmarks.py benchmarks/suites/core.json --json /tmp/core-a.json
python scripts/run_benchmarks.py benchmarks/suites/core.json --json /tmp/core-b.json
```

Require `cmp /tmp/core-a.json /tmp/core-b.json` success.

- [ ] **Step 2: Run Wave 6 deterministic gates**

Prepare portability tasks twice and compare the complete output directories byte-for-byte. Validate all replay runs. Evaluate reference twice and compare normalized JSON. Build matrix twice and compare JSON. Require reference 100.00/zero hard gates; cautious non-perfect but safe; faulty expected failure.

- [ ] **Step 3: Run all tests and data checks**

```bash
python -m unittest discover -s tests -v
python - <<'PY'
from pathlib import Path
import json
for path in sorted(Path('.').rglob('*.json')):
    json.loads(path.read_text(encoding='utf-8'))
print('JSON_PARSE_PASS')
PY
git diff --check
```

- [ ] **Step 4: Review branch diff against `main`**

Confirm no temporary transfer/bootstrap files, no credentials, no generated result artifacts, no vendor-specific commands, and only intended Wave 6 files/docs/CI changes.

- [ ] **Step 5: Open PR**

Suggested title: `Wave 6: cross-agent security evaluation harness`

PR body must report exact test counts, benchmark scores, replay profile behavior, deterministic checks and security boundary.

- [ ] **Step 6: Require PR CI**

All six OS/Python matrix jobs, `benchmark-core`, and `agent-eval-core` must complete with `success`. Do not merge on queued/in-progress/skipped/neutral/failed checks.

- [ ] **Step 7: Squash merge with expected head SHA**

Use the PR head SHA as merge guard. Squash merge so implementation staging history does not pollute `main`.

- [ ] **Step 8: Require post-merge CI**

On the squash commit on `main`, require the same six matrix jobs, `benchmark-core`, and `agent-eval-core` all `success` before declaring Wave 6 complete.
