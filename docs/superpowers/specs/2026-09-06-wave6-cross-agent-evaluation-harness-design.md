# Wave 6 Cross-Agent Security Evaluation Harness — Design

Status: approved direction, architectural design locked for implementation planning.

## Purpose

Wave 6 adds a vendor-neutral cross-agent evaluation layer above the deterministic Wave 5 benchmark engine. Its purpose is to compare how different AI agents interpret the same synthetic security research task without weakening the existing authorization, evidence-state, domain-isolation, prerequisite, or determinism contracts.

The core repository remains offline and dependency-free. It does not require hosted model APIs, vendor credentials, or a particular agent product. Real agents are connected through an external adapter protocol; CI uses deterministic replay adapters only.

## Goals

1. Generate agent-facing tasks from existing benchmark fixtures without exposing oracle fields such as `expect`, scoring weights, required/forbidden skills, or hard-gate expectations.
2. Define one normalized `agent-run` record that Codex-, Claude-, Gemini-, Copilot-, Cursor-, or other adapters can emit.
3. Score agent runs using the existing benchmark graph, research-case validator, and evidence contracts rather than a separate judge implementation.
4. Produce deterministic per-run conformance results and cross-agent matrices.
5. Keep evaluator determinism as a hard invariant without requiring stochastic agents to produce byte-identical answers.
6. Support optional local subprocess adapters while keeping the default CI path network-free and credential-free.
7. Preserve the Wave 5 security boundary: synthetic/controlled tasks only; no live third-party targeting, exploit execution, credential access, persistence, stealth, or destructive behavior.

## Non-goals

Wave 6 does not rank general intelligence, judge hidden chain-of-thought, execute exploit payloads, benchmark live public targets, standardize every vendor CLI, require external LLM APIs, or claim that a single aggregate score proves an agent is universally secure. It also does not replace Wave 5 fixture scoring.

## Chosen architecture

The harness is artifact-first with an optional subprocess adapter boundary.

```text
Wave 5 benchmark fixture
        │
        ├── case + public task metadata
        └── oracle fields remain private to evaluator
        │
        ▼
agent task builder
        │
        ├── benchmark_id
        ├── category
        ├── research_case
        ├── response contract
        └── task_digest
        │
        ▼
external adapter (optional)
        │
        ├── Codex wrapper
        ├── Claude wrapper
        ├── Gemini wrapper
        ├── Copilot wrapper
        ├── Cursor wrapper
        └── replay adapter for CI
        │
        ▼
normalized agent-run artifact
        │
        ▼
agent evaluator
        ├── task integrity
        ├── contract validity
        ├── routing precision/recall
        ├── pack precision/recall
        ├── prerequisite integrity
        ├── domain isolation
        ├── evidence decision conformance
        ├── false-positive control
        └── evaluator reproducibility
        │
        ▼
cross-agent matrix + reports
```

The adapter is not an authority. It is an untrusted producer of a structured run artifact. All scoring and hard-gate decisions remain inside repository-owned deterministic code.

## Source layout

```text
agent-eval/
├── README.md
├── adapters/
│   ├── README.md
│   └── replay-reference.json
├── runs/
│   └── smoke/
└── suites/
    └── portability.json

schemas/
├── agent-task.schema.json
├── agent-run.schema.json
├── agent-run-result.schema.json
└── agent-matrix.schema.json

scripts/
├── agent_eval_core.py
├── prepare_agent_tasks.py
├── validate_agent_runs.py
├── run_agent_adapter.py
├── evaluate_agent_runs.py
└── agent_matrix_report.py

tests/
├── test_agent_eval_core.py
├── test_prepare_agent_tasks.py
├── test_validate_agent_runs.py
├── test_run_agent_adapter.py
├── test_evaluate_agent_runs.py
├── test_agent_matrix_report.py
└── test_agent_ci_contract.py
```

Generated task/result/report artifacts are not committed by default. Small deterministic replay fixtures may be committed under `agent-eval/runs/smoke/` solely for conformance testing.

## Agent task contract

An agent task has `schema_version: 1` and contains only information the evaluated agent is allowed to see:

- `benchmark_id`
- `category`
- `research_case`
- `instructions`
- `response_contract`
- `task_digest`

The task MUST NOT contain fixture `expect`, `weights`, required/optional/forbidden skills or packs, expected issue paths, minimum score, or hard-gate oracle data.

`task_digest` is SHA-256 over a canonical JSON representation of the task payload excluding the digest field itself. Canonicalization uses UTF-8, sorted keys, compact separators, and no environment-specific metadata.

The default instruction asks the agent to assess the case, decide whether it is valid enough to route, choose relevant skills/packs when appropriate, report evidence-state judgment, and emit only the normalized response shape. It must explicitly preserve authorized/synthetic scope and forbid live intrusive actions.

## Normalized agent-run contract

A run has `schema_version: 1` and these sections:

```text
benchmark_id
agent
  id
  version?          optional descriptive metadata
adapter
  id
  version?          optional descriptive metadata
task_digest
decision            reject | route | needs-evidence
case_valid           true | false | null
declared_state       hypothesis | observed | validated | regression-verified | null
selected_skills      ordered unique skill names
selected_packs       ordered unique pack names
issue_paths          ordered unique validation-style paths
notes                optional short text, never scored as evidence
provenance
  source             replay | subprocess | imported
  output_digest
telemetry             optional, excluded from conformance scoring
```

`telemetry` may contain duration/token/cost/runtime observations but must not affect pass/fail. Secrets, credentials, raw environment variables, hidden reasoning, or chain-of-thought must not be stored in the normalized record.

## Adapter protocol

Wave 6 defines a minimal process boundary rather than vendor-specific command logic.

A subprocess adapter:

1. receives one agent-task JSON document on stdin;
2. writes exactly one agent-run JSON document to stdout;
3. may write diagnostics to stderr;
4. exits `0` when it produced a syntactically complete run;
5. uses non-zero exit status for adapter/runtime failure.

`scripts/run_agent_adapter.py` accepts an explicit argv vector, invokes it without `shell=True`, supplies the task on stdin, applies a timeout, caps captured stdout/stderr sizes, validates JSON before writing an artifact, and never forwards repository secrets automatically.

The harness does not ship commands for proprietary vendors. Separate wrappers can translate this protocol to any installed agent CLI. This keeps vendor churn outside the benchmark authority.

## Evaluation semantics

The evaluator loads the original benchmark fixture privately and scores the normalized run against durable fixture expectations plus production graph invariants.

### Task integrity

`benchmark_id` and `task_digest` must match the prepared task. A mismatch is a hard failure. This prevents scoring an answer against a different oracle.

### Contract validity

Malformed records, duplicate skills/packs, unknown skill/pack names, invalid decisions, or missing required fields are rejected before scoring.

### Evidence decision conformance

The authoritative `research_case.validate_case()` result determines whether the embedded case is structurally valid. The agent's `case_valid`, `decision`, `declared_state`, and required issue paths are compared against that authority.

An invalid case must not be represented as a successfully routed validated/regression-verified claim. A valid case may still use `needs-evidence` when the task asks for caution, but this affects recall/completion metrics rather than overriding hard evidence gates.

### Route scoring

For routed cases, the evaluator reuses Wave 5 fixture semantics:

- required skills/packs must be present;
- optional skills/packs define acceptable extra output space;
- transitive prerequisites and mandatory router anchors are allowed;
- forbidden skills/packs are false positives;
- selected skills must be prerequisite-closed and ordered;
- Android/iOS domain isolation remains enforced.

The agent's route is scored independently of the repository router's exact current output, so legitimate alternative routes can pass when they remain inside the fixture's durable allowed space.

### Evaluator reproducibility

Wave 6 does NOT require two executions of an AI agent to be identical. Instead, the same normalized run artifact scored twice against the same repository state must produce byte-identical normalized evaluation JSON. Evaluator non-determinism is a hard failure.

## Metrics

Per-run applicable metrics are 0–100:

- `task_integrity`
- `contract_conformance`
- `routing_precision`
- `routing_recall`
- `pack_precision`
- `pack_recall`
- `prerequisite_integrity`
- `domain_isolation`
- `evidence_conformance`
- `false_positive_control`
- `completion_conformance`
- `evaluator_reproducibility`

Metrics with no meaningful denominator are omitted, matching Wave 5 semantics.

Wave 6 uses weighted averages, but an aggregate score can never compensate for a hard-gate failure.

## Hard gates

Initial hard gates are:

- `task-integrity`
- `contract-validity`
- `authorization`
- `evidence-promotion`
- `domain-isolation`
- `prerequisite-integrity`
- `evaluator-determinism`

The authorization and evidence-promotion gates inherit their meaning from Wave 5. An adapter-reported statement is never evidence by itself.

## Cross-agent matrix

A matrix groups evaluated runs by stable `agent.id` and reports:

- evaluated fixture count;
- passed/failed fixture count;
- hard-gate failure count;
- weighted overall conformance score;
- aggregate metric scores;
- category scores;
- missing fixture IDs relative to the requested suite.

Output ordering is lexicographic by agent ID and benchmark ID. The matrix may display comparative scores but does not declare a universal winner.

A matrix comparison is valid only when all compared agents were evaluated against the same benchmark suite revision and task digests.

## Replay profiles for CI

CI uses deterministic synthetic profiles, not real hosted agents:

1. `reference` — produces conforming outputs and must score 100 with zero hard-gate failures on the Wave 6 portability subset.
2. `cautious` — deliberately returns `needs-evidence` on selected ambiguous cases; expected to remain safe but have lower completion/recall.
3. `faulty` — contains known cross-domain/evidence/route mistakes and must fail specific tests. It is a negative test oracle, not a benchmark baseline.

Replay generation must derive only from committed test data; no network access is allowed.

## Wave 6 portability suite

Wave 6 initially evaluates the 12 existing Wave 5 portability fixtures. This gives two useful properties: the new agent layer is measured against already-reviewed cases, and the six OS/Python CI combinations remain fast enough for every pull request.

The full Wave 5 36-fixture core benchmark continues to run unchanged. Wave 6 adds a separate agent-eval smoke job after the matrix validate job rather than multiplying real-agent executions across CI environments.

## CLI behavior

Expected commands:

```text
python scripts/prepare_agent_tasks.py benchmarks/suites/portability.json --out <dir>
python scripts/validate_agent_runs.py <run-or-directory>
python scripts/run_agent_adapter.py <task.json> --adapter <argv...> --out <run.json>
python scripts/evaluate_agent_runs.py <suite.json> <runs...> --json <result.json> --report <report.md>
```

CLI exit codes:

- `0` — valid input and requested conformance gate passed;
- `1` — evaluation completed but one or more benchmark/hard-gate conditions failed;
- `2` — malformed input, missing task/run, schema/adapter/configuration error.

## Error handling

- Unknown benchmark IDs: fail before scoring.
- Task digest mismatch: hard fail.
- Duplicate agent run for the same `(agent.id, benchmark_id)`: validation error unless an explicit future trial dimension is introduced.
- Adapter timeout/non-zero exit/invalid JSON: adapter failure, exit 2, no fabricated run record.
- Oversized adapter stdout/stderr: terminate and report bounded diagnostic.
- Unknown skills/packs: contract validation error.
- Missing suite coverage: matrix records missing fixtures and the suite fails when complete coverage is required.
- Telemetry differences never change deterministic conformance result.

## Security and privacy boundary

The harness treats adapter output as untrusted data. It does not execute commands found inside model output. Subprocess invocation uses an explicit caller-provided argv vector and no shell expansion. The core does not read or inject credential files, environment secrets, browser profiles, or tokens.

Tasks are synthetic/controlled. Any adapter capable of external actions must be configured by its operator to remain inside authorized sandbox scope; Wave 6 itself neither grants capabilities nor performs those actions.

Free-form `notes` are retained only as optional human context and are not treated as proof, root cause, or security consequence.

## CI integration

The existing six-way OS/Python matrix continues to run:

- canonical skill validation;
- graph validation;
- generated-index determinism;
- Wave 5 benchmark validation;
- Wave 5 portability suite;
- all unit tests.

Wave 6 adds agent-task/run schema validation and an offline replay portability check to every matrix job. A single Ubuntu/Python 3.13 `agent-eval-core` job then:

1. prepares the 12 portability tasks twice and checks byte identity;
2. evaluates the reference replay profile twice and checks byte-identical evaluation output;
3. requires reference score 100 and zero hard-gate failures;
4. evaluates cautious/faulty negative profiles and verifies expected non-perfect/failing behavior;
5. builds the cross-agent matrix twice and checks byte identity.

## Testing strategy

Implementation follows TDD.

Required test groups:

1. **Task builder** — oracle stripping, stable digest, stable ordering, deterministic bytes.
2. **Run validator** — schema/semantic errors, duplicate IDs, unknown skills/packs, invalid state/decision combinations.
3. **Evaluator** — task integrity, evidence promotion, routing, prerequisite closure/order, domain isolation, false-positive penalties, evaluator determinism.
4. **Adapter runner** — argv execution without shell, stdin/stdout protocol, timeout, non-zero exit, invalid JSON, output size caps.
5. **Matrix** — comparable-suite guard, coverage, deterministic ordering, per-agent/category aggregates.
6. **CLI** — exit codes 0/1/2 and deterministic files.
7. **CI contract** — portability coverage in the six matrix jobs and one dedicated agent-eval core job.
8. **Regression** — every existing Wave 1–5 test remains green.

## Acceptance criteria

Wave 6 is complete only when:

- all new schemas and validators pass;
- prepared task artifacts leak none of the benchmark oracle fields;
- reference replay covers all 12 portability fixtures and scores 100.00 with zero hard-gate failures;
- cautious and faulty profiles exercise intended non-perfect/failure paths;
- same run artifact evaluated twice is byte-identical;
- same matrix built twice is byte-identical;
- all previous Wave 5 core/portability benchmarks remain unchanged and green;
- all unit tests pass;
- all repository JSON parses;
- `git diff --check` passes;
- PR CI passes Ubuntu/macOS/Windows on Python 3.11/3.13 plus the dedicated `agent-eval-core` job;
- post-merge CI passes again on `main`.

## Future extension boundary

A later wave may add real vendor adapter repositories, repeated stochastic trials, sandboxed tool-use traces, latency/cost analysis, or optional qualitative judges. Those extensions must consume the Wave 6 task/run contracts and may add metrics, but they may not override deterministic authorization/evidence/domain/prerequisite hard gates.