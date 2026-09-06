# Wave 5 Security Skill Evaluation & Benchmark Engine Design

## Status

Approved concept, implementation pending written-spec review.

## Purpose

Wave 5 adds a deterministic evaluation layer on top of the existing Security-skills graph, research-case contract, and advisory router. Its purpose is to measure whether the system routes, validates, and reasons consistently rather than merely counting skills or relying on subjective impressions.

The benchmark engine is deliberately offline, dependency-free, vendor-neutral, and safe-by-construction. It evaluates structured synthetic or controlled research cases and expected behavior. It does not execute exploit payloads, target external systems, or treat model prose as evidence.

## Design goals

1. Measure routing quality with repeatable fixtures.
2. Detect regressions in authorization-first behavior, prerequisite closure, evidence-stage ordering, domain isolation, and pack recommendations.
3. Detect false-positive promotion, especially attempts to treat hypotheses or observations as validated findings without the required evidence.
4. Produce stable machine-readable results and concise human-readable reports.
5. Run identically on Linux, macOS, and Windows with Python 3.11 and 3.13.
6. Keep benchmark fixtures versioned and reviewable as source truth.
7. Preserve compatibility with current Agent Skills portability: benchmark machinery must not alter canonical `SKILL.md` format.
8. Provide future extension points for external agent runs and model-based judging without making either a Wave 5 dependency.

## Non-goals

Wave 5 does not:

- benchmark offensive exploitation against public or third-party targets;
- execute intrusive fuzzing, exploitation, persistence, credential access, or destructive actions;
- score hidden chain-of-thought or require agents to expose private reasoning;
- depend on hosted LLM APIs, external databases, Docker, or third-party Python packages;
- establish that a skill is universally effective from a single aggregate score;
- replace the existing research-case validator, graph validator, or router.

## Architecture

The benchmark subsystem is a conformance layer above existing runtime contracts.

```text
benchmark fixture
      │
      ├── research case
      ├── expected route constraints
      ├── expected pack constraints
      ├── expected validation outcome
      ├── hard gates
      └── metric weights
      │
      ▼
research_case.validate_case()
      │
      ├── rejected case ───────────────┐
      │                                │
      ▼                                │
route_case()                           │
      │                                │
      ▼                                │
benchmark evaluator ◄─────────────────┘
      │
      ├── hard-gate verdicts
      ├── per-metric scores
      ├── fixture score
      └── deterministic diagnostics
      │
      ▼
benchmark suite aggregate
      │
      ├── benchmark-result.json
      └── human-readable report
```

The benchmark engine calls existing validation and routing functions directly. It must not duplicate their logic. This makes benchmark failures informative: a fixture catches changed behavior in the actual production contracts rather than in a parallel implementation.

## Source layout

```text
benchmarks/
├── README.md
├── cases/
│   ├── authorization/
│   ├── domain-isolation/
│   ├── evidence/
│   ├── false-positive/
│   ├── remediation/
│   └── routing/
└── suites/
    ├── core.json
    └── portability.json

schemas/
├── benchmark-case.schema.json
└── benchmark-result.schema.json

scripts/
├── benchmark_core.py
├── benchmark_report.py
├── run_benchmarks.py
└── validate_benchmarks.py

tests/
├── test_benchmark_core.py
├── test_benchmark_report.py
├── test_run_benchmarks.py
└── test_validate_benchmarks.py
```

Generated benchmark result files are not source truth and are not committed by default.

## Benchmark fixture contract

Each benchmark case is one JSON object with `schema_version: 1` and these top-level sections:

- `benchmark_id`: stable globally unique fixture identifier.
- `category`: one of `authorization`, `domain-isolation`, `evidence`, `false-positive`, `remediation`, `routing`.
- `description`: concise statement of the behavior under test.
- `case`: a research-case-shaped object passed to `validate_case` and, when valid, `route_case`.
- `expect`: expected validator/router behavior.
- `weights`: optional per-fixture metric weights; omitted keys use suite defaults.
- `tags`: stable descriptive labels for filtering and reporting.

`expect` supports:

- `case_valid`: boolean.
- `required_skills`: skills that must be present in the route.
- `forbidden_skills`: skills that must not be present.
- `required_packs`: packs that must be recommended.
- `forbidden_packs`: packs that must not be recommended.
- `ordered_before`: list of `[a, b]` pairs requiring skill `a` to appear before skill `b` when both are present.
- `route_limit`: explicit router limit for the fixture.
- `required_issue_paths`: validator issue paths expected for invalid cases.
- `hard_gates`: named hard constraints active for the fixture.

All skill and pack references in fixtures must resolve against the current graph at benchmark-validation time. Duplicate IDs are forbidden across the full corpus.

## Hard gates

Aggregate score must never hide a severe conformance failure. A suite fails if any fixture violates an enabled hard gate.

Wave 5 hard gates are:

### Authorization gate

A research case with unauthorized scope must never be routed. The expected outcome is case rejection with an authorization issue.

### Evidence-promotion gate

A case that lacks evidence required by its declared state must never be accepted as that state. Examples include `validated` without root cause, bounded consequence, positive and negative controls, or a pinned reproducer.

### Domain-isolation gate

Explicit mutually exclusive domains must not cross-route. Initial required invariant: Android fixtures must not recommend iOS-exclusive skills and vice versa.

### Prerequisite-integrity gate

Every returned route must be prerequisite-closed and ordered so each prerequisite precedes its dependent skill.

### Determinism gate

Repeated evaluation of the same fixture and repository state must return byte-identical normalized result data, excluding explicitly non-deterministic metadata such as invocation timestamps. Wave 5 result schema therefore contains no required timestamp field.

## Metrics

Each valid-routed fixture can produce these 0–100 metrics:

- `routing_precision`: fraction of routed skills that are expected/allowed under fixture constraints. Forbidden skills impose direct penalties; neutral prerequisite skills are not penalized.
- `routing_recall`: fraction of `required_skills` present.
- `pack_precision`: analogous score for pack recommendations.
- `pack_recall`: fraction of `required_packs` present.
- `prerequisite_integrity`: 100 only when closure and ordering are correct; otherwise 0 and hard failure when enabled.
- `domain_isolation`: 100 when no forbidden domain-specific route leaks occur.
- `evidence_conformance`: 100 when validator acceptance/rejection and required issue paths match expectations.
- `false_positive_control`: 100 when forbidden promotions/routes are absent; decreases deterministically for explicitly forbidden outputs.
- `reproducibility`: 100 when two in-process executions normalize identically.

Invalid-case fixtures focus on `evidence_conformance`, authorization behavior, false-positive control, and reproducibility. Metrics that do not apply are omitted rather than treated as zero.

## Aggregate score

Scores are weighted arithmetic means over applicable metrics only.

Default suite weights:

```json
{
  "routing_precision": 1.0,
  "routing_recall": 1.0,
  "pack_precision": 0.5,
  "pack_recall": 0.5,
  "prerequisite_integrity": 1.5,
  "domain_isolation": 1.5,
  "evidence_conformance": 2.0,
  "false_positive_control": 2.0,
  "reproducibility": 1.0
}
```

The aggregate result contains both `overall_score` and `hard_gate_failures`. A suite is passing only if:

- `hard_gate_failures == 0`; and
- `overall_score >= suite.minimum_score`.

Initial `core` suite minimum score is 95.0. The score threshold may be raised later, but lowering it requires an explicit reviewed fixture/suite change rather than a runtime flag.

## Normalization and deterministic output

Machine result JSON uses stable key ordering and sorted fixture IDs. Float scores are rounded to two decimals using deterministic arithmetic. Diagnostics are stable strings derived from fixture IDs and violated constraints.

The canonical result object contains:

- `schema_version`;
- `suite`;
- `fixture_count`;
- `passed_fixture_count`;
- `failed_fixture_count`;
- `overall_score`;
- `minimum_score`;
- `hard_gate_failures`;
- `metrics` aggregate mapping;
- `fixtures` ordered result entries;
- `passed` boolean.

It intentionally omits timestamps, hostnames, absolute paths, random IDs, and environment-specific temp locations.

## Corpus design

Wave 5 starts with 36 fixtures: six fixtures in each of six categories.

Each category must include a balance of positive, negative, and boundary cases rather than six near-duplicates.

### Authorization

Examples include local/owned/sandbox scopes that should validate, and explicitly unauthorized cases that must fail before routing.

### Domain isolation

Examples include Android/iOS exclusivity, virtualization vs unrelated web-only internals, firmware vs smart-contract-specific routing, and generic-domain cases where cross-domain primitives remain permitted only through non-exclusive shared skills.

### Evidence

Fixtures cover all four research states and invalid attempts to skip evidence requirements.

### False positive

Fixtures encode incomplete observations, misleading scanner-like claims, missing controls, and ambiguous symptoms that must not be promoted into confirmed vulnerability state.

### Remediation

Fixtures assert that validation prerequisites occur before remediation/regression skills and that regression-verified cases satisfy fixed-revision evidence.

### Routing

Fixtures cover representative memory-safety, parser/protocol, web, mobile, AI-agent, and firmware routes with required anchors and forbidden unrelated skills.

All fixtures are synthetic or controlled abstractions. They contain no deployable exploit payloads and no live external targets.

## Suite manifests

`benchmarks/suites/core.json` enumerates all required Wave 5 fixtures, default metric weights, hard gates, and `minimum_score: 95.0`.

`benchmarks/suites/portability.json` is a smaller smoke suite selected to detect path ordering, JSON, and deterministic-runtime differences across Windows/macOS/Linux. It uses the same evaluator and schemas.

Suite manifests list fixture paths explicitly. Files present in `benchmarks/cases/` but absent from every suite are rejected by `validate_benchmarks.py`, preventing orphan fixtures.

## Validation

`validate_benchmarks.py` performs static corpus validation before any suite run:

1. parse every benchmark fixture and suite manifest;
2. validate schema-version and required fields;
3. reject duplicate benchmark IDs;
4. validate embedded research cases through `validate_case` when `expect.case_valid` is true;
5. allow deliberately invalid embedded cases only when `expect.case_valid` is false;
6. verify skill and pack references against the current graph;
7. validate `ordered_before` shape and references;
8. reject unknown hard-gate or metric names;
9. reject orphan or multiply-listed fixture paths where suite policy requires uniqueness;
10. validate minimum score range `0 <= score <= 100`.

The validator is dependency-free and does not require a JSON Schema package; schema files document interoperability while Python performs canonical runtime validation, matching the project’s current pattern.

## Runner behavior

`run_benchmarks.py` accepts:

```text
python scripts/run_benchmarks.py benchmarks/suites/core.json
python scripts/run_benchmarks.py benchmarks/suites/core.json --json /tmp/result.json
python scripts/run_benchmarks.py benchmarks/suites/core.json --report /tmp/report.md
```

Execution order is deterministic by benchmark ID, regardless of manifest ordering.

Exit code is:

- `0` when the suite passes;
- `1` for benchmark failures or hard-gate violations;
- `2` for malformed benchmark/suite input.

No network access is required.

## Human report

`benchmark_report.py` renders a concise Markdown report containing:

- suite/pass status;
- overall score and minimum threshold;
- aggregate metrics table;
- hard-gate failures;
- failed fixtures with stable diagnostics;
- category summary.

The report does not hide failed fixtures behind the aggregate score.

## CI integration

The existing six-job OS/Python matrix remains the primary portability gate.

Each matrix job will add:

```text
Validate benchmarks
Run portability benchmark
```

The full `core` suite runs on Ubuntu/Python 3.13 in a separate `benchmark-core` job after canonical graph/unit tests pass. This avoids running all 36 fixtures six times while still proving the evaluator itself is portable through the smoke suite.

PR merge requirements for Wave 5:

- all existing canonical skill/graph/index/unit-test jobs pass;
- portability suite passes on all six matrix combinations;
- core suite passes with zero hard-gate failures and score >= 95.0;
- benchmark corpus validator passes;
- benchmark result is deterministic across two executions in the core job.

## Testing strategy

TDD is required for benchmark implementation.

Unit tests cover:

- fixture validation;
- duplicate IDs;
- unknown skills/packs;
- invalid `ordered_before` constraints;
- scoring precision/recall;
- prerequisite hard-gate failures;
- evidence hard-gate failures;
- invalid-case scoring;
- deterministic normalization;
- report rendering;
- runner exit codes.

Integration tests run small temporary suites against the real repository graph/router so benchmark code cannot silently diverge from production behavior.

Corpus tests assert exact initial fixture counts by category: six each and 36 total.

## Compatibility and extension points

Wave 5’s evaluator consumes structured behavior, not a specific AI vendor API. Future external-agent runners may emit a normalized `agent_observation` object that can be evaluated alongside router results without changing existing fixture contracts.

A future LLM judge may add optional qualitative metrics, but deterministic Wave 5 metrics remain mandatory and authoritative for hard gates. A model-based score can never override authorization, evidence-promotion, prerequisite, domain-isolation, or determinism failures.

## Security boundary

Benchmark fixtures use synthetic inputs, structured metadata, and controlled evidence. The benchmark engine performs no network access, exploit execution, credential operations, persistence, stealth, or destructive actions.

A fixture that attempts to specify an external live target or executable attack payload is outside Wave 5 scope and must be rejected during review. Benchmark correctness is measured through routing and evidence contracts, not successful exploitation.

## Acceptance criteria

Wave 5 is complete only when all of the following are true:

1. 36 reviewed benchmark fixtures exist, exactly six per category.
2. `core.json` and `portability.json` validate.
3. Benchmark schemas are committed.
4. The dependency-free evaluator, runner, validator, and report renderer are implemented.
5. Unit/integration tests cover hard gates, scoring, deterministic output, and runner behavior.
6. `python scripts/run_benchmarks.py benchmarks/suites/core.json` exits 0 with zero hard-gate failures and score >= 95.0.
7. Running the core suite twice produces byte-identical normalized JSON.
8. Portability suite passes on Linux/macOS/Windows under Python 3.11 and 3.13.
9. Existing 83 skills / 20 packs continue to validate without graph regression.
10. README, CONTRIBUTING/AGENTS guidance, and benchmark documentation describe how agents and maintainers use the benchmark layer.
11. PR CI is fully green before merge.
12. Post-merge `main` CI is checked independently.
