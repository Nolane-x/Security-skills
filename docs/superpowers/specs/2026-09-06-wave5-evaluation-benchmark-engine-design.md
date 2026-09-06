# Wave 5 Security Skill Evaluation & Benchmark Engine Design

## Status

Approved concept, implementation pending written-spec review.

## Purpose

Wave 5 adds a deterministic evaluation layer on top of the existing Security-skills graph, research-case contract, and advisory router. Its purpose is to measure whether the system routes, validates, and reasons consistently rather than merely counting skills or relying on subjective impressions.

The benchmark engine is offline, dependency-free, vendor-neutral, and safe-by-construction. It evaluates structured synthetic or controlled research cases and expected behavior. It does not execute exploit payloads, target external systems, or treat model prose as evidence.

## Design goals

1. Measure routing quality with repeatable fixtures.
2. Detect regressions in authorization-first behavior, prerequisite closure, evidence-stage ordering, domain isolation, and pack recommendations.
3. Detect false-positive promotion, especially attempts to treat hypotheses or observations as validated findings without required evidence.
4. Produce stable machine-readable results and concise human-readable reports.
5. Run identically on Linux, macOS, and Windows with Python 3.11 and 3.13.
6. Keep fixtures versioned and reviewable as source truth.
7. Preserve Agent Skills portability: benchmark machinery must not alter canonical `SKILL.md` format.
8. Leave extension points for external agent runs and model-based judging without making either a Wave 5 dependency.

## Non-goals

Wave 5 does not benchmark offensive exploitation against public or third-party targets; execute intrusive fuzzing, exploitation, persistence, credential access, or destructive actions; score hidden chain-of-thought; require hosted LLM APIs, Docker, databases, or third-party Python packages; or replace the existing case, graph, and routing contracts.

## Architecture

```text
benchmark fixture
      │
      ├── research case
      ├── expected validation outcome
      ├── route/pack constraints
      ├── ordering constraints
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
      ├── benchmark-result.json
      └── Markdown report
```

The evaluator calls the existing validator and router directly; it must not duplicate their behavior. Benchmark failures therefore identify regressions in production contracts rather than in a parallel implementation.

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

Generated benchmark results are not source truth and are not committed by default.

## Benchmark fixture contract

Each fixture is one JSON object with `schema_version: 1` and:

- `benchmark_id`: stable globally unique identifier.
- `category`: one of `authorization`, `domain-isolation`, `evidence`, `false-positive`, `remediation`, `routing`.
- `description`: behavior under test.
- `case`: research-case-shaped object.
- `expect`: expected validation/router behavior.
- `weights`: optional per-fixture metric overrides.
- `tags`: stable filter/report labels.

`expect` supports:

- `case_valid`: boolean.
- `required_skills`: every listed skill must be present.
- `optional_skills`: listed non-prerequisite skills are permitted but not required.
- `forbidden_skills`: every listed skill must be absent.
- `required_packs`: every listed pack must be recommended.
- `optional_packs`: permitted but not required packs.
- `forbidden_packs`: every listed pack must be absent.
- `ordered_before`: `[a, b]` pairs requiring `a` before `b` when both are present.
- `route_limit`: explicit router limit.
- `required_issue_paths`: validator issue paths expected for invalid cases.
- `hard_gates`: named hard constraints active for the fixture.

For scoring a valid route, the allowed skill set is:

```text
required_skills
+ optional_skills
+ transitive prerequisites of required/optional skills
+ mandatory router anchors implied by the case goal/state
```

Any routed skill outside that allowed set counts as an unexpected route output for precision. `forbidden_skills` remain an explicit stronger assertion and can trigger hard-gate or false-positive penalties. Pack precision uses `required_packs + optional_packs` as the allowed set.

All skill and pack references must resolve against the current graph. Duplicate benchmark IDs are forbidden across the corpus.

## Hard gates

Aggregate score must never hide a severe conformance failure. A suite fails when any enabled hard gate fails.

### Authorization

Unauthorized scope must never be routed. Expected behavior is case rejection with an authorization issue.

### Evidence promotion

A case lacking evidence required by its declared state must not be accepted as that state. `validated` requires root cause, bounded consequence, positive and negative controls, and a pinned reproducer; `regression-verified` additionally requires fixed-revision non-reproduction with healthy controls.

### Domain isolation

Mutually exclusive domains must not cross-route. Initial invariant: Android fixtures must not recommend iOS-exclusive skills and vice versa.

### Prerequisite integrity

Every returned route must be prerequisite-closed and each prerequisite must precede its dependent skill.

### Determinism

Repeated evaluation of the same fixture and repository state must return byte-identical normalized result data. Required result data therefore contains no timestamp, hostname, random ID, absolute temp path, or other environment-specific field.

## Metrics

Applicable metrics are 0–100:

- `routing_precision`: allowed routed skills / all routed skills, with transitive prerequisites and mandatory anchors treated as allowed.
- `routing_recall`: required skills present / required skills.
- `pack_precision`: allowed recommended packs / all recommended packs.
- `pack_recall`: required packs present / required packs.
- `prerequisite_integrity`: 100 only when closure and ordering are correct.
- `domain_isolation`: 100 when no forbidden domain-specific output appears.
- `evidence_conformance`: 100 when validator acceptance/rejection and required issue paths match expectations.
- `false_positive_control`: 100 when forbidden promotions/routes are absent; deterministic penalties apply to each explicit forbidden output.
- `reproducibility`: 100 when two normalized in-process evaluations are identical.

A metric with no meaningful denominator for a fixture is omitted instead of assigned zero.

## Aggregate score

Scores use a weighted arithmetic mean over applicable metrics only.

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

A suite passes only when `hard_gate_failures == 0` and `overall_score >= minimum_score`. Initial `core` threshold is `95.0`. Lowering the threshold requires a reviewed source change to the suite manifest; no runtime flag may lower it.

## Deterministic result schema

Machine JSON uses stable key ordering, fixtures sorted by `benchmark_id`, and scores rounded to two decimals. Stable diagnostics identify the fixture and violated constraint.

The canonical result contains:

- `schema_version`;
- `suite`;
- `fixture_count`;
- `passed_fixture_count`;
- `failed_fixture_count`;
- `overall_score`;
- `minimum_score`;
- `hard_gate_failures`;
- aggregate `metrics`;
- ordered `fixtures` results;
- `passed`.

## Corpus design

Wave 5 starts with exactly 36 fixtures: six in each category. Every category contains positive, negative, and boundary cases rather than near-duplicates.

### Authorization

Local/owned/sandbox cases that should validate plus unauthorized synthetic targets that must fail before routing.

### Domain isolation

Android/iOS exclusivity, virtualization versus web-only internals, firmware versus smart-contract-specific routing, and generic shared-primitives cases.

### Evidence

All four research states plus invalid attempts to skip evidence requirements.

### False positive

Incomplete observations, scanner-like claims, missing controls, and ambiguous symptoms that must not be promoted.

### Remediation

Validation prerequisites before remediation/regression skills and regression-verified fixed-revision evidence.

### Routing

Representative memory-safety, parser/protocol, web, mobile, AI-agent, and firmware routes with required anchors and unrelated forbidden outputs.

All cases are synthetic or controlled abstractions and contain no deployable exploit payloads or live external targets.

## Suite manifests and membership

`benchmarks/suites/core.json` is the authoritative Wave 5 corpus and explicitly lists all 36 fixtures, default metric weights, hard gates, and `minimum_score: 95.0`.

`benchmarks/suites/portability.json` is an explicit subset of `core` selected for path, JSON, ordering, and deterministic-runtime portability checks. A fixture may therefore appear in both `core` and `portability` by design.

Corpus membership rules are:

1. every file under `benchmarks/cases/` must appear exactly once in `core.json`;
2. `core.json` must not list the same path twice;
3. every portability path must also exist in `core.json`;
4. `portability.json` must not list the same path twice;
5. no suite may reference a nonexistent fixture.

These rules prevent orphans without incorrectly treating the portability subset as duplication.

## Corpus validation

`validate_benchmarks.py` performs static validation before any suite run:

1. parse every fixture and suite;
2. validate schema version and required fields;
3. reject duplicate benchmark IDs;
4. validate embedded cases through `validate_case` when `expect.case_valid` is true;
5. permit deliberately invalid cases only when `expect.case_valid` is false and the validator actually reports errors;
6. verify skill/pack references against the graph;
7. validate `ordered_before` pair shape and references;
8. reject unknown hard-gate and metric names;
9. enforce corpus/suite membership rules above;
10. enforce `0 <= minimum_score <= 100`;
11. enforce exactly six core fixtures per category and 36 total for Wave 5.

The JSON Schema files document interoperability while dependency-free Python performs canonical runtime validation, matching current project practice.

## Runner

```text
python scripts/run_benchmarks.py benchmarks/suites/core.json
python scripts/run_benchmarks.py benchmarks/suites/core.json --json /tmp/result.json
python scripts/run_benchmarks.py benchmarks/suites/core.json --report /tmp/report.md
```

Execution order is deterministic by benchmark ID regardless of manifest order.

Exit codes:

- `0`: suite passes;
- `1`: evaluated suite fails score or hard gate;
- `2`: malformed benchmark/suite input.

No network access is required.

## Human report

`benchmark_report.py` renders Markdown with suite status, overall/minimum score, aggregate metrics, hard-gate failures, failed fixtures with stable diagnostics, and category summaries. Failed fixtures are always visible even if aggregate score is high.

## CI integration

The existing six-job OS/Python matrix remains the portability gate. Each matrix job adds:

```text
Validate benchmarks
Run portability benchmark
```

A separate `benchmark-core` job runs the full 36-fixture `core` suite on Ubuntu/Python 3.13 after canonical validation/unit tests. This avoids executing all fixtures six times while the smaller portability subset proves cross-platform evaluator behavior.

Wave 5 merge requirements:

- existing skill/graph/index/unit-test jobs pass;
- portability suite passes on all six OS/Python combinations;
- core suite passes with zero hard-gate failures and score >= 95.0;
- corpus validator passes;
- two core executions produce byte-identical normalized JSON.

## Testing strategy

TDD is mandatory. Unit/integration tests cover fixture validation, duplicate IDs, unknown skills/packs, invalid ordering constraints, precision/recall scoring, prerequisite and evidence hard gates, invalid-case scoring, deterministic normalization, report rendering, runner exit codes, integration with the real graph/router, and exact corpus counts of six per category / 36 total.

## Compatibility and extension points

Wave 5 consumes structured behavior rather than vendor-specific APIs. A future external-agent runner may emit a normalized `agent_observation` evaluated alongside router output without changing existing fixture contracts.

A future model-based judge may contribute optional qualitative metrics, but deterministic Wave 5 metrics remain authoritative for hard gates. No model score may override authorization, evidence-promotion, prerequisite, domain-isolation, or determinism failures.

## Security boundary

Fixtures use synthetic inputs, structured metadata, and controlled evidence. The engine performs no network access, exploit execution, credential operations, persistence, stealth, or destructive actions. A fixture containing a live external target or executable attack payload is outside Wave 5 scope and must be rejected in review.

## Acceptance criteria

Wave 5 is complete only when:

1. 36 reviewed fixtures exist, exactly six per category.
2. `core.json` and `portability.json` validate under the membership rules.
3. Both benchmark schemas are committed.
4. Dependency-free evaluator, runner, validator, and report renderer are implemented.
5. Tests cover hard gates, scoring, deterministic output, runner behavior, and real graph integration.
6. Core exits 0 with zero hard-gate failures and score >= 95.0.
7. Two core executions produce byte-identical normalized JSON.
8. Portability passes on Linux/macOS/Windows under Python 3.11 and 3.13.
9. Existing 83 skills / 20 packs continue to validate without graph regression.
10. README, CONTRIBUTING/AGENTS guidance, and benchmark documentation explain the layer.
11. PR CI is fully green before merge.
12. Post-merge `main` CI is checked independently.
