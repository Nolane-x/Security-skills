# Contributing

## What belongs here

A good skill captures a reusable security-research decision process: when to use a technique, assumptions, evidence collection, false-positive discrimination, stop conditions, and a structured output.

A weak contribution is a thin wrapper around one scanner, shell command, or exploit recipe.

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

## Evidence language

Use statuses consistently:

- **hypothesis** — plausible from code/design reasoning but not reproduced;
- **observed** — behavior reproduced but root cause/security consequence not fully established;
- **validated** — claimed vulnerability behavior and causal root cause have evidence under stated conditions;
- **regression-verified** — the same evidence fails on the fixed build while controls still behave correctly.

## Validation

Run:

```bash
python scripts/validate_skills.py
python scripts/validate_graph.py
python scripts/build_catalog.py
python scripts/build_graph.py
python scripts/build_catalog.py --check
python scripts/build_graph.py --check
python -m unittest discover -s tests -v
```

CI repeats the stale checks and tests on Linux, macOS, and Windows. Research-case and router changes must also keep `examples/research-case.example.json` valid and routeable.

## Benchmark fixtures

Benchmark changes live under `benchmarks/` and measure the production validator/router rather than duplicating their logic. A fixture must use a synthetic, owned, sandboxed, CTF, benchmark, or explicitly authorized case and must not encode a live external target or deployable exploit payload.

Each fixture declares required, optional, and forbidden skills/packs plus any ordering, issue-path, and hard-gate expectations. Required entries should capture durable invariants; optional entries describe currently acceptable route space; forbidden entries should target meaningful false positives or cross-domain leaks. Do not snapshot every route output as “required.”

The initial Wave 5 corpus is intentionally fixed at six fixtures per category and 36 total. New fixtures after Wave 5 may increase the corpus, but removing coverage or lowering `core.minimum_score` requires an explicit reviewed contract change.

Validate and run both suites before submitting benchmark changes:

```bash
python scripts/validate_benchmarks.py
python scripts/run_benchmarks.py benchmarks/suites/portability.json
python scripts/run_benchmarks.py benchmarks/suites/core.json
```

See `docs/benchmark-contract.md` for schema semantics, hard gates, scoring, determinism requirements, and future extension boundaries.

## Cross-agent evaluation contributions

Wave 6 agent-facing tasks must be built from existing benchmark fixtures through `scripts/prepare_agent_tasks.py`; do not hand-copy fixture oracles into public task files. Prepared tasks may contain the research case and response contract, but never fixture `expect`, weights, required/optional/forbidden route oracle fields, required issue paths, minimum score, or hard-gate oracle data.

Normalized runs must follow `schemas/agent-run.schema.json`. Adapters are transport only: they must not alter evaluator authority, and they must not store credentials, raw environment variables, browser profiles, hidden reasoning, or chain-of-thought. Vendor-specific wrappers should remain outside the core contract. For local subprocess integration, use the explicit JSON stdin/stdout protocol documented in `agent-eval/adapters/README.md`.

Before submitting agent-evaluation changes, run an offline reference replay and preserve negative controls:

```bash
python scripts/prepare_agent_tasks.py benchmarks/suites/portability.json --out /tmp/agent-tasks
python scripts/prepare_replay_runs.py benchmarks/suites/portability.json --profile reference --out /tmp/reference
python scripts/prepare_replay_runs.py benchmarks/suites/portability.json --profile cautious --out /tmp/cautious
python scripts/prepare_replay_runs.py benchmarks/suites/portability.json --profile faulty --out /tmp/faulty
python scripts/validate_agent_runs.py /tmp/reference
python scripts/evaluate_agent_runs.py benchmarks/suites/portability.json /tmp/reference
```

Do not weaken hard gates, fixture oracles, or replay negative controls merely to make a real agent score higher.
