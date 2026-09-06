# Wave 6 Cross-Agent Security Evaluation Harness — Design

Status: approved direction; implementation pending plan/TDD.

## Purpose

Wave 6 adds a vendor-neutral cross-agent evaluation layer above the deterministic Wave 5 benchmark engine. It compares how different AI agents interpret the same synthetic security research task without weakening authorization, evidence-state, domain-isolation, prerequisite, or determinism contracts.

The core repository remains offline and dependency-free. It requires no hosted model API, vendor credential, or specific agent product. Real agents connect through an external adapter protocol; CI uses deterministic replay adapters only.

## Goals

1. Generate agent-facing tasks from existing benchmark fixtures without exposing oracle fields such as `expect`, scoring weights, required/forbidden outputs, issue-path expectations, or hard gates.
2. Define one normalized `agent-run` record that any agent adapter can emit.
3. Score agent runs with the existing graph, `research_case.validate_case()`, and Wave 5 fixture semantics rather than a second judge implementation.
4. Produce deterministic per-run evaluations and cross-agent matrices.
5. Require evaluator determinism without requiring stochastic agents to return identical outputs.
6. Support optional local subprocess adapters while keeping default CI network-free and credential-free.
7. Preserve the Wave 5 security boundary: synthetic/controlled tasks only; no live third-party targeting, exploit execution, credential access, persistence, stealth, or destructive behavior.

## Non-goals

Wave 6 does not rank general intelligence, judge hidden chain-of-thought, benchmark live public targets, standardize every vendor CLI, require external LLM APIs, execute exploit payloads, or replace Wave 5 fixture scoring.

## Approaches considered

### Vendor-specific runners

Hard-code Codex/Claude/Gemini/Copilot/Cursor commands into the repository. This is convenient initially but couples the benchmark authority to rapidly changing vendor interfaces and credentials.

### Artifact-only import

Accept normalized result files but never launch adapters. This is maximally stable but stops short of being a usable harness.

### Chosen: artifact-first core plus optional subprocess adapter protocol

Tasks and runs are portable artifacts. A small subprocess boundary lets external wrappers invoke any agent while repository-owned deterministic code remains the sole scoring authority. CI can therefore exercise the complete harness with replay adapters and no network access.

## Architecture

```text
Wave 5 benchmark fixture
        │
        ├── public case/task metadata
        └── private oracle fields stay evaluator-only
        │
        ▼
agent task builder
        │
        ├── benchmark_id/category
        ├── research_case
        ├── response contract
        └── task_digest
        │
        ▼
external adapter (optional)
        │
        ├── vendor wrapper
        └── replay adapter for CI
        │
        ▼
normalized agent-run artifact
        │
        ▼
agent evaluator
        ├── task/contract integrity
        ├── evidence decision conformance
        ├── route/pack scoring
        ├── prerequisite/domain checks
        ├── false-positive control
        └── evaluator reproducibility
        │
        ▼
cross-agent matrix + reports
```

Adapters are untrusted artifact producers. They never become authorities for evidence or hard gates.

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

Generated task/result/report artifacts are not committed by default. Small deterministic replay fixtures may be committed solely for conformance testing.

## Agent task contract

An agent task has `schema_version: 1` and exactly the public information the evaluated agent may see:

- `benchmark_id`
- `category`
- `research_case`
- `instructions`
- `response_contract`
- `task_digest`

The task MUST NOT contain fixture `expect`, `weights`, required/optional/forbidden skills or packs, expected issue paths, suite minimum score, or hard-gate oracle data.

`task_digest` is SHA-256 over canonical JSON of the task excluding `task_digest`: UTF-8, sorted keys, compact separators, no timestamps, hostnames, random IDs, or paths.

The default instructions ask the agent to assess the case, decide whether it is valid enough to route, select relevant skills/packs when appropriate, report its evidence-state judgment, and emit only the normalized response shape. Instructions preserve authorized/synthetic scope and forbid live intrusive actions.

## Normalized agent-run contract

A run has `schema_version: 1`:

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
case_valid           boolean
declared_state       hypothesis | observed | validated | regression-verified | null
selected_skills      ordered unique skill names
selected_packs       ordered unique pack names
issue_paths          ordered unique validation-style paths
notes?               optional short text, never scored as evidence
provenance
  source             replay | subprocess | imported
  output_digest
telemetry?            optional and excluded from conformance scoring
```

### Decision invariants

- `route` requires `case_valid=true`; `declared_state` must equal the input case state; selected skills may be non-empty.
- `reject` requires `case_valid=false`; `declared_state=null`; selected skills and packs must be empty; at least one issue path must be supplied.
- `needs-evidence` requires `case_valid=true`; `declared_state` must equal the input case state; it may return analysis-oriented skills but must not claim a state above the input state. It is a cautious completion decision, not a replacement for case validation.
- No decision may promote `declared_state` above the input research-case state.

The state order is `hypothesis < observed < validated < regression-verified`.

`telemetry` may contain duration/token/cost/runtime observations but never changes score/pass/fail. Secrets, raw environment variables, hidden reasoning, and chain-of-thought are forbidden in the normalized record.

`provenance.output_digest` is SHA-256 over canonical semantic run fields excluding `provenance.output_digest`, `telemetry`, and free-form `notes`. Thus changing latency/cost or human notes cannot change semantic run identity.

## Adapter protocol

A subprocess adapter:

1. receives one agent-task JSON document on stdin;
2. writes exactly one agent-run JSON document to stdout;
3. may write bounded diagnostics to stderr;
4. exits `0` only when it produced a syntactically complete run;
5. uses non-zero status for adapter/runtime failure.

`scripts/run_agent_adapter.py` accepts an explicit argv vector, invokes it with `shell=False`, supplies the task on stdin, applies a timeout, caps stdout/stderr, validates JSON before writing an artifact, and never executes commands contained in model output.

Environment handling is deny-by-default. The child receives only a minimal runtime environment (`PATH` plus basic locale/platform variables required to launch the process). Additional environment variable names must be explicitly allowlisted by the caller. The harness never discovers or forwards repository secrets, credential files, browser profiles, tokens, or cloud credentials automatically.

The repository does not ship proprietary vendor command templates. External wrappers translate this protocol to installed agent CLIs, keeping vendor churn outside the benchmark authority.

## Evaluation semantics

The evaluator privately loads the original benchmark fixture and scores the run against durable fixture expectations plus production graph invariants.

### Task integrity

`benchmark_id` and `task_digest` must match the prepared task. Mismatch is a hard failure and prevents normal route scoring.

### Contract validity

Malformed records, duplicate skill/pack entries, unknown skill/pack names, impossible decision invariants, invalid state promotion, or missing required fields are rejected before ordinary scoring.

### Evidence decision conformance

`research_case.validate_case()` is authoritative for structural/evidence validity. The agent's `case_valid`, `decision`, `declared_state`, and issue paths are compared against that result.

An invalid case must be rejected and must never be represented as a routed validated/regression-verified claim. An adapter statement is never evidence by itself.

### Route scoring

For `route` and `needs-evidence` decisions on valid cases, scoring reuses Wave 5 fixture semantics:

- required skills/packs contribute recall and must be present when the fixture requires completion;
- optional skills/packs define acceptable extra output space;
- transitive prerequisites and mandatory router anchors are allowed;
- forbidden skills/packs are false positives;
- selected skills must be prerequisite-closed and ordered;
- Android/iOS isolation remains enforced.

A `needs-evidence` decision may intentionally lose completion/recall points while remaining free of safety/evidence hard-gate failures.

### Evaluator reproducibility

Wave 6 does NOT require repeated model invocations to be identical. The same normalized run artifact scored twice against the same repository state must produce byte-identical normalized evaluation JSON. Evaluator non-determinism is a hard failure.

## Metrics

Applicable per-run metrics are 0–100:

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

Metrics with no meaningful denominator are omitted. Weighted averages cannot compensate for hard-gate failures.

## Hard gates

- `task-integrity`
- `contract-validity`
- `authorization`
- `evidence-promotion`
- `domain-isolation`
- `prerequisite-integrity`
- `evaluator-determinism`

Authorization and evidence-promotion inherit Wave 5 meaning.

## Cross-agent matrix

The matrix groups evaluated runs by stable `agent.id` and reports:

- evaluated fixture count;
- passed/failed fixture count;
- hard-gate failure count;
- weighted overall conformance score;
- aggregate metric scores;
- category scores;
- missing fixture IDs relative to the requested suite.

Ordering is lexicographic by agent ID then benchmark ID. Comparative scores are allowed, but the report does not declare a universal winner.

A matrix comparison is valid only when all compared agents use the same suite identity and identical task digests for each benchmark ID. Duplicate `(agent.id, benchmark_id)` records are errors; repeated stochastic trials are intentionally deferred to a later schema version.

## Replay profiles for CI

CI uses deterministic synthetic profiles only:

1. `reference` — generated from private fixture oracle data by test tooling; covers the 12 portability fixtures and must score 100 with zero hard-gate failures.
2. `cautious` — returns `needs-evidence` for selected valid cases; expected to remain hard-gate safe but score below reference on completion/recall.
3. `faulty` — contains known domain/evidence/route mistakes and must fail targeted negative tests.

Replay generation may use fixture oracle fields because it is evaluator-owned test data, but generated public agent tasks must never contain those fields. No replay path uses network access.

## Wave 6 portability scope

Wave 6 initially reuses the 12 existing Wave 5 portability fixtures. The full 36-fixture Wave 5 core benchmark continues unchanged. This keeps the first cross-agent layer reviewable and fast while exercising all six existing benchmark categories.

## CLI behavior

```text
python scripts/prepare_agent_tasks.py benchmarks/suites/portability.json --out <dir>
python scripts/validate_agent_runs.py <run-or-directory>
python scripts/run_agent_adapter.py <task.json> --adapter <argv...> --out <run.json>
python scripts/evaluate_agent_runs.py <suite.json> <runs...> --json <result.json> --report <report.md>
```

Exit codes:

- `0` — valid input and requested conformance gate passed;
- `1` — evaluation completed but one or more benchmark/hard-gate conditions failed;
- `2` — malformed input, missing artifact, schema/adapter/configuration error.

## Error handling

- Unknown benchmark ID: fail before scoring.
- Task digest mismatch: task-integrity hard failure.
- Duplicate `(agent.id, benchmark_id)`: validation error.
- Adapter timeout, non-zero exit, invalid/multiple JSON documents, or oversized output: exit 2 and create no fabricated run.
- Unknown skills/packs or impossible decision/state combination: contract error.
- Missing required suite coverage: matrix records missing IDs and fails when complete coverage is required.
- Telemetry/notes differences never change deterministic conformance output.

## Security and privacy boundary

Adapter output is untrusted data. The harness never executes commands found in model output. Subprocess invocation is explicit argv with no shell expansion. Environment inheritance is minimal and extra credential variables are opt-in by name.

Tasks are synthetic/controlled. Any external adapter capable of actions must be independently configured by its operator to remain in authorized sandbox scope; Wave 6 neither grants capabilities nor performs those actions.

Free-form notes are optional human context only and never count as proof, root cause, or security consequence.

## CI integration

The existing six-way OS/Python matrix continues to validate skills/graph/indexes, Wave 5 benchmarks, portability, and unit tests. Wave 6 adds task/run contract validation and an offline replay smoke evaluation to each matrix job.

A single Ubuntu/Python 3.13 `agent-eval-core` job then:

1. prepares the 12 portability tasks twice and requires byte identity;
2. evaluates the reference profile twice and requires byte-identical evaluation output;
3. requires reference score 100 and zero hard-gate failures;
4. evaluates cautious/faulty profiles and verifies expected non-perfect/failing behavior;
5. builds the cross-agent matrix twice and requires byte identity.

## Testing strategy

Implementation follows TDD:

1. **Task builder** — oracle stripping, stable digest/order/bytes.
2. **Run validator** — schema and semantic errors, unknown references, decision/state invariants.
3. **Evaluator** — task integrity, evidence promotion, route scoring, prerequisite order, domain isolation, false positives, deterministic scoring.
4. **Adapter runner** — no shell, stdin/stdout protocol, sanitized env, explicit env allowlist, timeout, non-zero exit, invalid/multiple JSON, output caps.
5. **Matrix** — comparable-suite guard, coverage, deterministic ordering, per-agent/category aggregates.
6. **CLI** — exit codes 0/1/2 and deterministic files.
7. **CI contract** — six matrix jobs plus one `agent-eval-core` job.
8. **Regression** — all Wave 1–5 tests and Wave 5 core/portability outputs remain green.

## Acceptance criteria

Wave 6 is complete only when:

- all new schemas/validators pass;
- generated tasks leak none of the fixture oracle fields;
- reference replay covers all 12 portability fixtures and scores 100.00 with zero hard-gate failures;
- cautious/faulty profiles exercise intended non-perfect/failure paths;
- same run artifact evaluated twice is byte-identical;
- same cross-agent matrix built twice is byte-identical;
- Wave 5 core and portability remain unchanged and green;
- all unit tests pass;
- all repository JSON parses;
- `git diff --check` passes;
- PR CI passes Ubuntu/macOS/Windows × Python 3.11/3.13 plus `agent-eval-core`;
- post-merge CI passes again on `main`.

## Future extension boundary

Later waves may add maintained vendor adapter repositories, repeated stochastic trials, sandboxed tool-use traces, latency/cost analysis, or optional qualitative judges. Those extensions must consume the Wave 6 task/run contracts and may add metrics, but cannot override deterministic authorization/evidence/domain/prerequisite hard gates.