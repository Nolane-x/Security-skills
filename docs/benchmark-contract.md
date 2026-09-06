# Benchmark Contract

Wave 5 evaluates Security-skills as a deterministic conformance system. The benchmark layer calls the production research-case validator and advisory router directly; it does not maintain a second routing implementation. Wave 6 adds a vendor-neutral agent artifact layer without changing that authority.

## Source of truth

- `benchmarks/cases/<category>/*.json` are source fixtures.
- `benchmarks/suites/core.json` is the complete Wave 5 regression suite.
- `benchmarks/suites/portability.json` is a representative subset run across every supported CI OS/Python pair.
- `schemas/benchmark-case.schema.json` and `schemas/benchmark-result.schema.json` document interoperable Wave 5 JSON shapes.
- `schemas/agent-*.schema.json` document Wave 6 public task, normalized run, evaluation-result, and matrix shapes.
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

Applicable Wave 5 metrics are scored from 0 to 100: routing precision/recall, pack precision/recall, prerequisite integrity, domain isolation, evidence conformance, false-positive control, and reproducibility. Metrics that do not apply to a fixture are omitted rather than scored as zero.

A suite passes only when all fixtures pass their explicit constraints, enabled hard-gate failures are zero, and the weighted aggregate score meets the suite's committed `minimum_score`. The Wave 5 core threshold is 95.0.

## Determinism

Normalized machine output excludes timestamps, hostnames, random identifiers, absolute paths, and temporary locations. Fixture results are ordered by `benchmark_id`, mappings use stable key ordering, and scores are rounded to two decimals. Two runs against the same repository state must produce byte-identical normalized JSON.

## Wave 6 cross-agent layer

Wave 6 prepares a public task from a private benchmark fixture. The task contains the research case, instructions, response contract, and a canonical SHA-256 `task_digest`; it does **not** contain fixture `expect`, weights, route or issue-path oracles, thresholds, or hard-gate expectations. The digest binds an agent-run artifact to the exact public task without exposing the private oracle.

A normalized `agent-run` contains the agent/adapter identity, task digest, decision, case-validity judgment, declared evidence state, selected canonical skills/packs, validation-style issue paths, and provenance. Telemetry and free-form notes are non-authoritative and excluded from semantic scoring. Hidden reasoning and chain-of-thought are neither requested nor stored.

The evaluator privately reloads the Wave 5 fixture and production graph/case contracts. It scores task integrity, contract conformance, routing and pack precision/recall, prerequisite integrity, domain isolation, evidence conformance, false-positive control, completion conformance, and evaluator reproducibility. The same normalized run evaluated twice must produce byte-identical result JSON. The AI agent itself is not required to be deterministic.

Wave 6 hard gates include task integrity, contract validity, authorization, evidence promotion, domain isolation, prerequisite integrity, and evaluator determinism. An adapter or aggregate score may not override them.

## Adapter boundary

Adapters are untrusted transport. Core ships no proprietary vendor commands. The optional subprocess protocol receives one task JSON on stdin and must emit one run JSON on stdout. `run_agent_adapter.py` invokes an explicit argv with `shell=False`, timeout/output caps, and a sanitized environment. Credentials are forwarded only through an explicit allowlist. Model output is never interpreted as executable commands by the evaluator.

CI uses deterministic offline `reference`, `cautious`, and `faulty` replay profiles. Reference must remain fully conforming; cautious intentionally sacrifices completion on selected evidence-sensitive cases without crossing hard gates; faulty is a negative-control profile and must fail known checks.

## Security boundary

Fixtures and agent tasks are synthetic or controlled abstractions. They may model security-relevant claims and evidence, but benchmark execution performs no network targeting, exploit execution, credential access, persistence, stealth, or destructive action. A fixture or agent task that requires a live third-party target or deployable exploit payload does not belong in this corpus.

## Extension boundary

Real Codex-, Claude-, Gemini-, Copilot-, Cursor-, or other wrappers may consume the Wave 6 adapter protocol, and future qualitative judges may add optional metrics. Neither may override deterministic hard gates. Comparative cross-agent matrices measure conformance to a fixed suite and task revision; they are not universal model rankings.
