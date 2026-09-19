# Contributing

## What belongs here

A good contribution captures or strengthens a reusable security-research decision process: when to use a technique, assumptions, evidence collection, false-positive discrimination, stop conditions, remediation, and structured output.

A weak contribution is a thin wrapper around one scanner, shell command, payload list, or duplicated prompt.

The Wave 10 release baseline is intentionally closed at **83 canonical skills, 20 packs, and 40 operator-depth profiles**. Expansion beyond that baseline is not the default. New canonical skills, packs, or depth profiles should require a concrete uncovered mechanism, non-duplicative design, and an explicit architecture change.

See `docs/wave10-closure-audit.md`.

## Canonical skill structure

Each `skills/<name>/SKILL.md` must use valid Agent Skills frontmatter and contain:

- `## When to use`
- `## Preconditions`
- `## Workflow`
- `## Evidence contract`
- `## Stop conditions`
- `## Output`

Use lowercase kebab-case names. Keep the main file focused; put very deep notes in local `references/`.

Required Nolane metadata in frontmatter:

```yaml
metadata:
  nolane-security-category: discovery
  nolane-security-version: "1"
  nolane-security-authorization: required
```

Authorization is `required`, `conditional`, or `not-applicable`.

## Graph sidecar

Every skill has `skill.meta.json`:

```json
{
  "schema_version": 1,
  "maturity": "beta",
  "domains": ["fuzzing", "parsers"],
  "prerequisites": ["security-scope-and-authorization"],
  "composes_with": ["evidence-driven-vulnerability-validation"],
  "evidence_stage": "observed"
}
```

Rules:

- all referenced skill names must exist;
- a skill cannot reference itself;
- prerequisite edges must remain acyclic;
- `composes_with` is advisory and may be reciprocal;
- use prerequisites only for true ordering/knowledge dependencies, not “related to” relationships.

## Packs

A `packs/<name>.json` manifest must declare one or more routing `domains` and list every skill used by its `default_flow`. Pack entrypoints and members must reference canonical skill names. When a prerequisite and its dependent both appear in `default_flow`, the prerequisite must come first. Packs never duplicate skill prose.

The Wave 10 closure baseline contains exactly **20 packs**. Changing that count is an architecture change, not routine maintenance.

## Operator depth

Operator depth is selective and CI-enforced.

A registered profile must preserve the contract in `docs/operator-depth-contract.md` and provide:

- an existing canonical skill identity;
- a reviewed operator runbook;
- a machine-readable scenario/review-case matrix;
- `lab_only: true`;
- explicit safe oracles;
- evidence and counterfactual controls;
- stop conditions;
- remediation/regression checks;
- deterministic tests.

The Wave 10 baseline contains exactly **40 profiles**. Routine contributions should improve existing profiles rather than add new ones.

## Evidence language

Use statuses consistently:

- **hypothesis** — plausible from code/design reasoning but not reproduced;
- **observed** — behavior reproduced but root cause/security consequence not fully established;
- **validated** — claimed vulnerability behavior and causal root cause have evidence under stated conditions;
- **regression-verified** — the same evidence fails on the fixed build while controls still behave correctly.

Do not promote findings solely because a scanner, fuzzer, model, static analyzer, or tool says so.

## Validation

Run the complete architectural validation path:

```bash
python scripts/validate_skills.py
python scripts/validate_operator_depth.py
python scripts/validate_graph.py
python scripts/build_catalog.py
python scripts/build_graph.py
python scripts/build_catalog.py --check
python scripts/build_graph.py --check
python scripts/validate_case.py examples/research-case.example.json
python scripts/route_skills.py examples/research-case.example.json --limit 12
python scripts/validate_benchmarks.py
python scripts/run_benchmarks.py benchmarks/suites/portability.json
python scripts/run_benchmarks.py benchmarks/suites/core.json
python -m unittest discover -s tests -v
```

The test suite includes a Wave 10 closure regression that freezes the published 83 / 20 / 40 architecture and Apache-2.0 license baseline.

CI repeats critical gates on Linux, macOS, and Windows with Python 3.11 and 3.13 and runs dedicated benchmark, cross-agent, and controlled comparative-regression jobs.

## Benchmark fixtures

Benchmark changes live under `benchmarks/` and measure the production validator/router rather than duplicating their logic. A fixture must use a synthetic, owned, sandboxed, CTF, benchmark, or explicitly authorized case and must not encode a live external target or deployable exploit payload.

Each fixture declares required, optional, and forbidden skills/packs plus any ordering, issue-path, and hard-gate expectations. Required entries should capture durable invariants; optional entries describe currently acceptable route space; forbidden entries should target meaningful false positives or cross-domain leaks. Do not snapshot every route output as “required.”

The Wave 5 corpus is fixed at six fixtures per category and 36 total. Removing coverage or lowering `core.minimum_score` requires an explicit reviewed contract change.

Validate and run both suites before submitting benchmark changes:

```bash
python scripts/validate_benchmarks.py
python scripts/run_benchmarks.py benchmarks/suites/portability.json
python scripts/run_benchmarks.py benchmarks/suites/core.json
```

See `docs/benchmark-contract.md` for schema semantics, hard gates, scoring, determinism requirements, and extension boundaries.

## Cross-agent evaluation contributions

Agent-facing tasks must be built from existing benchmark fixtures through `scripts/prepare_agent_tasks.py`; do not hand-copy fixture oracles into public task files. Prepared tasks may contain the research case and response contract, but never fixture `expect`, weights, required/optional/forbidden route oracle fields, required issue paths, minimum score, or hard-gate oracle data.

Normalized runs must follow `schemas/agent-run.schema.json`. Adapters are transport only: they must not alter evaluator authority, and they must not store credentials, raw environment variables, browser profiles, hidden reasoning, or chain-of-thought.

Before submitting agent-evaluation changes, run an offline reference replay and preserve negative controls.

Do not weaken hard gates, fixture oracles, closure invariants, or replay negative controls merely to make a real agent score higher.

## Safety

Intrusive work remains restricted to local, owned, sandboxed, benchmark/CTF, or explicitly authorized targets.

Prefer bounded, reversible, non-destructive evidence. See `SECURITY.md`.

## License

Contributions to this repository are distributed under the repository's [Apache License 2.0](LICENSE) unless a file explicitly states otherwise.
