# Security Skills

[![CI](https://github.com/Nolane-x/Security-skills/actions/workflows/validate.yml/badge.svg)](https://github.com/Nolane-x/Security-skills/actions/workflows/validate.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

**English** · [Tiếng Việt](README-VN.md) · [简体中文](README-CN.md)

**Security Skills** is a verification-first security skill graph and deterministic evaluation framework for AI agents.

It provides portable security reasoning skills, explicit evidence contracts, prerequisite-aware routing, reproducible benchmarks, selective operator-depth methodology, and vendor-neutral agent evaluation. The goal is not to make security claims faster; it is to make them **more reproducible, reviewable, bounded, and difficult to overstate**.

> **Stable baseline: Wave 10 closed** — **83 canonical skills**, **20 packs**, **40 CI-enforced operator-depth profiles**, **36 deterministic benchmark fixtures**, **12 portability fixtures**, **6 CI environments**, **0 required third-party Python packages**, licensed under **Apache-2.0**.

## Why this repository exists

A security agent should not jump from a scanner alert, crash, suspicious trace, static-analysis warning, or model hypothesis directly to “confirmed vulnerability.”

Reliable security work requires a chain of evidence:

```text
scope + authorization
        ↓
hypothesis
        ↓
observation
        ↓
causal validation
        ↓
false-positive controls
        ↓
bounded security consequence
        ↓
remediation
        ↓
regression verification
```

Security Skills turns that discipline into portable Agent Skills plus machine-checkable contracts.

## Current architecture

```text
                         ┌─────────────────────────────┐
                         │ 83 canonical Agent Skills   │
                         └──────────────┬──────────────┘
                                        │
                         ┌──────────────▼──────────────┐
                         │ 20 curated routing packs    │
                         └──────────────┬──────────────┘
                                        │
                 ┌──────────────────────▼──────────────────────┐
                 │ deterministic case validation + routing     │
                 └──────────────────────┬──────────────────────┘
                                        │
                 ┌──────────────────────▼──────────────────────┐
                 │ 40 selective operator-depth profiles        │
                 │ runbooks + machine-readable safe cases      │
                 └──────────────────────┬──────────────────────┘
                                        │
        ┌───────────────────────────────▼───────────────────────────────┐
        │ benchmarks · cross-agent evaluation · regression authorities │
        └───────────────────────────────────────────────────────────────┘
```

Canonical skill prose lives once under `skills/`. Packs, operator-depth profiles, benchmarks, and evaluation layers reference that canonical authority rather than forking it per vendor.

## What the project provides

### 1. Canonical security reasoning graph

Each canonical capability is defined as:

```text
skills/<skill-name>/
├── SKILL.md
├── skill.meta.json
└── references/        # optional deeper local resources
```

A skill encodes a reusable decision process: when it applies, prerequisites, workflow, evidence requirements, stop conditions, and expected output.

`skill.meta.json` adds graph metadata such as domains, prerequisites, composition edges, maturity, and evidence stage.

### 2. Deterministic research routing

Research cases are validated before routing. The router closes transitive prerequisites, applies domain/context filters, preserves evidence-state constraints, and returns a deterministic skill order.

```bash
python scripts/validate_case.py examples/research-case.example.json
python scripts/route_skills.py examples/research-case.example.json --limit 12
```

Routing is advisory. Authorization and evidence requirements remain authoritative.

### 3. Evidence-state model

Security claims move through explicit states:

```text
hypothesis
    ↓
observed
    ↓
validated
    ↓
regression-verified
```

A tool result alone does not promote a finding.

A validated finding requires evidence such as a pinned target/environment, reproducible observation, causal root cause, bounded consequence, positive and negative controls, and reproducer identity. Regression verification additionally requires the fixed revision to stop reproducing the issue while controls still behave correctly.

See [docs/research-case-contract.md](docs/research-case-contract.md).

### 4. Operator depth

Wave 10 closes with **40 selective CI-enforced operator-depth profiles**.

Operator depth is intentionally selective: not every canonical skill needs a large runbook. Profiles are used where deeper causal methodology materially improves reliability.

Each registered profile combines:

- a reviewed operator runbook;
- machine-readable synthetic or controlled scenarios/review cases;
- explicit safe oracles;
- evidence ladders;
- counterfactual and false-positive controls;
- stop conditions;
- remediation and regression checks;
- dedicated deterministic tests.

Coverage spans authorization and identity, parser/protocol boundaries, memory/runtime behavior, sandbox/browser/driver boundaries, firmware and virtualization trust, cryptographic and external-data trust, AI-agent security, web framework internals, and smart-contract invariants/reentrancy/upgradeability.

See [docs/operator-depth-contract.md](docs/operator-depth-contract.md), [operator-depth/profiles.json](operator-depth/profiles.json), and the [Wave 10 closure audit](docs/wave10-closure-audit.md).

### 5. Deterministic benchmarks

Wave 5 established **36 deterministic fixtures** across six categories:

1. authorization;
2. domain isolation;
3. evidence-state conformance;
4. false-positive control;
5. remediation/regression routing;
6. representative routing correctness.

```bash
python scripts/validate_benchmarks.py
python scripts/run_benchmarks.py benchmarks/suites/portability.json
python scripts/run_benchmarks.py benchmarks/suites/core.json
```

Hard failures such as unauthorized acceptance, evidence-state violations, or domain leakage cannot be hidden by a high average score.

See [docs/benchmark-contract.md](docs/benchmark-contract.md).

### 6. Cross-agent evaluation

The evaluation layer converts reviewed benchmark fixtures into oracle-free tasks and scores normalized `agent-run` artifacts using deterministic repository code.

It does not hard-code a model vendor or proprietary CLI. External hosts integrate through a normalized artifact contract.

```bash
python scripts/prepare_agent_tasks.py benchmarks/suites/portability.json --out /tmp/agent-tasks

python scripts/prepare_replay_runs.py benchmarks/suites/portability.json \
  --profile reference \
  --out /tmp/reference-runs

python scripts/validate_agent_runs.py /tmp/reference-runs

python scripts/evaluate_agent_runs.py \
  benchmarks/suites/portability.json \
  /tmp/reference-runs
```

The committed replay profiles include a conforming reference baseline and deterministic negative controls.

See [agent-eval/README.md](agent-eval/README.md).

### 7. Controlled comparative regression

The repository also contains a deterministic “superiority-court” regression harness for controlled internal contestant views. It is an engineering test authority, **not an external model leaderboard and not evidence of universal superiority**.

Any empirical comparison with another system requires matched tasks, controlled conditions, disclosed limitations, and direct evidence.

## Security coverage

The canonical graph spans:

- scope, authorization, attack-surface mapping, and hypothesis generation;
- fuzz harnesses, corpora, coverage-guided, grammar-aware, and stateful fuzzing;
- crash triage, minimization, sanitizer evidence, and exploitability triage;
- static/dataflow analysis, symbolic execution, differential testing, and variant hunting;
- memory lifetime, bounds/integer safety, type confusion, concurrency, and JIT invariants;
- parser/protocol state machines, canonicalization, deserialization, and namespace confusion;
- authorization, confused-deputy, cache identity, secrets/tokens, and tenant isolation;
- kernel, drivers/IOCTL, sandboxing, browser process boundaries, and virtualization;
- containers, cloud IAM, supply-chain review, firmware, secure boot, and updates;
- Android/iOS security and local-storage/keystore boundaries;
- web routing, server-side request boundaries, uploads, templates, and multi-tenant internals;
- cryptographic protocols, randomness lifecycle, certificates, and hostname validation;
- smart-contract invariants, reentrancy, upgradeability, and oracle trust;
- prompt injection, RAG/memory isolation, tool confirmation, connectors/plugins, and AI-agent assessment;
- evidence ledgers, false-positive elimination, remediation, regression validation, and reporting.

## Quick start

No third-party Python package is required for the core validation path.

```bash
git clone https://github.com/Nolane-x/Security-skills.git
cd Security-skills

python scripts/validate_skills.py
python scripts/validate_operator_depth.py
python scripts/validate_graph.py
python scripts/validate_benchmarks.py
python -m unittest discover -s tests -v
```

Generate and verify indexes:

```bash
python scripts/build_catalog.py
python scripts/build_graph.py
python scripts/build_catalog.py --check
python scripts/build_graph.py --check
```

## Full validation

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
python scripts/prepare_agent_tasks.py benchmarks/suites/portability.json --out /tmp/agent-tasks
python scripts/prepare_replay_runs.py benchmarks/suites/portability.json --profile reference --out /tmp/agent-runs
python scripts/validate_agent_runs.py /tmp/agent-runs
python scripts/evaluate_agent_runs.py benchmarks/suites/portability.json /tmp/agent-runs
python -m unittest discover -s tests -v
```

CI repeats the critical gates on Ubuntu, macOS, and Windows with Python 3.11 and 3.13, then runs dedicated benchmark, cross-agent, and comparative regression jobs.

## Portability

`skills/` is the canonical source. Do not fork skill prose per vendor.

A portable host layout can point directly to the same content:

```text
<project>/
└── .agents/
    └── skills/
        └── <skill-name>/
            ├── SKILL.md
            └── ...optional local resources...
```

Any agent host that can consume Agent Skills or explicit repository context can integrate without changing the underlying security authority.

See [docs/compatibility.md](docs/compatibility.md).

## Safe adapter boundary

The local adapter path is deliberately defensive:

- `shell=False`;
- explicit argv vectors;
- enforced timeouts;
- stdout/stderr byte caps;
- child termination on overflow;
- sanitized environment by default;
- credential-like variables only through explicit allowlists;
- untrusted agent output parsed as data;
- deterministic pipe cleanup;
- hidden reasoning / chain-of-thought is neither requested nor stored.

## Repository layout

```text
Security-skills/
├── skills/              # 83 canonical Agent Skills
├── operator-depth/      # registry for 40 selective deep profiles
├── packs/               # 20 curated routing manifests
├── benchmarks/          # deterministic routing/evidence fixtures
├── agent-eval/          # vendor-neutral cross-agent contracts
├── superiority/         # controlled comparative regression authority
├── schemas/             # machine-readable schemas
├── scripts/             # validators, routers, evaluators, builders
├── tests/               # deterministic regression tests
├── examples/            # research-case examples
├── docs/                # contracts and architecture documentation
├── sources/             # research-system lineage metadata
├── AGENTS.md             # repository-level agent guidance
├── SECURITY.md           # authorization and responsible-use boundary
├── CONTRIBUTING.md       # contribution requirements
└── LICENSE               # Apache License 2.0
```

## Safety boundary

Intrusive techniques are restricted to local, owned, sandboxed, benchmark/CTF, or explicitly authorized targets.

Proofs should prefer the least harmful evidence that establishes the claim: assertions, sanitizer reports, minimized crashes, synthetic resources, marker files, policy simulation, mock services, read-only snapshots, synthetic canaries, and regression tests.

See [SECURITY.md](SECURITY.md).

## Wave 10 closure

Wave 10 is intentionally **closed at 40 operator-depth profiles**. The project does not treat repository size, skill count, profile count, or line count as a quality metric.

Future work should default to:

- correctness and maintenance;
- stronger evidence and controls;
- safer oracles;
- better benchmarks;
- portability;
- research-lineage updates;
- targeted defect fixes;
- documentation and onboarding.

Expansion beyond the 83 / 20 / 40 baseline should require a concrete non-duplicative mechanism and an explicit architecture decision.

See [docs/wave10-closure-audit.md](docs/wave10-closure-audit.md).

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) before changing canonical skills, graph metadata, packs, operator-depth contracts, benchmarks, or agent-evaluation authority.

A strong contribution adds a reusable decision process or strengthens an existing contract. A weak contribution only adds another tool wrapper, payload list, or duplicated prompt.

## Research lineage

Security Skills distills original workflows from reproducible vulnerability research, autonomous cyber-reasoning systems, fuzzing infrastructure, program analysis, reverse engineering, web/mobile/firmware/cloud security, smart-contract analysis, and modern AI-agent security research.

The repository does **not** vendor third-party offensive code or copy third-party prompts.

See [docs/sources.md](docs/sources.md) and [sources/research-systems.json](sources/research-systems.json).

## Documentation

- [Vietnamese README](README-VN.md)
- [Simplified Chinese README](README-CN.md)
- [Wave 10 closure audit](docs/wave10-closure-audit.md)
- [Compatibility](docs/compatibility.md)
- [Research-case contract](docs/research-case-contract.md)
- [Operator-depth contract](docs/operator-depth-contract.md)
- [Benchmark contract](docs/benchmark-contract.md)
- [Cross-agent evaluation](agent-eval/README.md)
- [Packs](packs/README.md)
- [Research sources](docs/sources.md)
- [Security policy](SECURITY.md)
- [Contributing](CONTRIBUTING.md)

## License

Licensed under the [Apache License 2.0](LICENSE).

---

**Security Skills follows one rule: a security claim is only as strong as the evidence, controls, and reproducibility behind it.**
