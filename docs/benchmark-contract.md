# Benchmark Contract

Wave 5 evaluates Security-skills as a deterministic conformance system. The benchmark layer calls the production research-case validator and advisory router directly; it does not maintain a second routing implementation.

## Source of truth

- `benchmarks/cases/<category>/*.json` are source fixtures.
- `benchmarks/suites/core.json` is the complete Wave 5 regression suite.
- `benchmarks/suites/portability.json` is a representative subset run across every supported CI OS/Python pair.
- `schemas/benchmark-case.schema.json` and `schemas/benchmark-result.schema.json` document interoperable JSON shapes.
- Result JSON/Markdown files are generated outputs and are not committed by default.

## Fixture semantics

A fixture embeds a research case and an `expect` object. `required_*` values are durable invariants that must appear. `optional_*` values define acceptable current output space and keep precision scoring from penalizing legitimate prerequisite/context nodes. `forbidden_*` values represent concrete false positives or cross-domain leaks that must remain absent.

`ordered_before` expresses explicit route ordering constraints. `required_issue_paths` is used when a deliberately invalid research case must be rejected for known validation reasons. `route_limit` pins the advisory-router budget for reproducibility.

## Hard gates

Enabled fixture hard gates are non-negotiable:

- `authorization` — unauthorized scope must be rejected before routing.
- `evidence-promotion` — a case missing evidence required by its declared state must not be accepted as that state.
- `domain-isolation` — mutually exclusive domain routing must not leak domain-exclusive capabilities.
- `prerequisite-integrity` — every routed prerequisite must exist and precede its dependent node.
- `determinism` — repeated evaluation of the same fixture and repository state must normalize identically.

An aggregate score cannot compensate for a hard-gate failure.

## Metrics and suite pass condition

Applicable metrics are scored from 0 to 100: routing precision/recall, pack precision/recall, prerequisite integrity, domain isolation, evidence conformance, false-positive control, and reproducibility. Metrics that do not apply to a fixture are omitted rather than scored as zero.

A suite passes only when all fixtures pass their explicit constraints, enabled hard-gate failures are zero, and the weighted aggregate score meets the suite's committed `minimum_score`. The Wave 5 core threshold is 95.0.

## Determinism

Normalized machine output excludes timestamps, hostnames, random identifiers, absolute paths, and temporary locations. Fixture results are ordered by `benchmark_id`, mappings use stable key ordering, and scores are rounded to two decimals. Two runs against the same repository state must produce byte-identical normalized JSON.

## Security boundary

Fixtures are synthetic or controlled abstractions. They may model security-relevant claims and evidence, but benchmark execution performs no network targeting, exploit execution, credential access, persistence, stealth, or destructive action. A fixture that requires a live third-party target or deployable exploit payload does not belong in this corpus.

## Extension boundary

Future agent runners may emit normalized observation objects, and future qualitative judges may add optional metrics. Neither may override deterministic hard gates. The Wave 5 conformance result remains authoritative for authorization, evidence-state integrity, prerequisite ordering, domain isolation, and reproducibility.
