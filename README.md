# Security Skills

[![CI](https://github.com/Nolane-x/Security-skills/actions/workflows/validate.yml/badge.svg)](https://github.com/Nolane-x/Security-skills/actions/workflows/validate.yml)

**English** · [Tiếng Việt](README-VN.md) · [简体中文](README-CN.md)

A **verification-first security skill graph and deterministic cross-agent evaluation framework for AI agents**.

Security Skills gives coding agents, research agents, and autonomous security systems a portable set of reusable security reasoning skills — plus the evidence gates, routing logic, benchmarks, and cross-agent conformance tooling needed to verify that those skills are being used correctly.

> **Stable baseline: Wave 6** — 83 canonical skills, 20 packs, 36 deterministic benchmark fixtures, and a vendor-neutral cross-agent evaluation harness.

## Why this project exists

Security agents should not jump from a scanner alert, crash, static-analysis warning, or model hypothesis directly to “confirmed vulnerability.” Good security research requires explicit scope, evidence, controls, causal reasoning, reproducibility, and regression validation.

This repository turns that discipline into a portable machine-readable system.

```text
security knowledge
      │
      ▼
83 canonical Agent Skills
      │
      ▼
deterministic research router
      │
      ▼
evidence-state machine
      │
      ▼
Wave 5 benchmark authority
      │
      ▼
Wave 6 cross-agent evaluator
```

The result is not just a collection of prompts. It is a **security intelligence system that can validate its own routing and evaluate how external AI agents follow the same security contract**.

## What it is — and what it is not

**Security Skills is:**

- a portable security reasoning graph for AI agents;
- a set of reusable Agent Skills with explicit applicability and evidence contracts;
- a deterministic prerequisite-aware router;
- a machine-readable research-case and evidence-state model;
- a benchmark suite for routing, authorization, evidence, false-positive control, and remediation;
- a vendor-neutral harness for comparing normalized agent runs;
- a defensive research framework designed for local, owned, sandboxed, CTF, benchmark, or explicitly authorized targets.

**Security Skills is not:**

- a payload or exploit collection;
- a replacement for authorization or human security judgment;
- a mechanism for declaring vulnerabilities from tool output alone;
- a vendor-specific prompt pack;
- a benchmark of “general intelligence.” Cross-agent scores measure conformance to this repository's reviewed security contract.

## Current snapshot

| Capability | Current baseline |
| --- | ---: |
| Canonical skills | **83** |
| Validated packs | **20** |
| Benchmark fixtures | **36** |
| Benchmark categories | **6** |
| Cross-agent portability fixtures | **12** |
| Evidence states | **4** |
| CI environments | **6** |
| Python dependencies | **0 third-party packages** |

CI validates Linux, macOS, and Windows on Python 3.11 and 3.13.

## Three-layer architecture

### 1. Security intelligence graph

Each canonical capability lives once under:

```text
skills/<skill-name>/
├── SKILL.md
└── skill.meta.json
```

`SKILL.md` follows the open Agent Skills model. `skill.meta.json` adds Nolane graph metadata such as domains, prerequisites, composition edges, maturity, and evidence stage without polluting portable skill frontmatter.

Packs under `packs/` reference canonical skills instead of duplicating them.

### 2. Deterministic benchmark authority

Wave 5 evaluates the production case validator and router against reviewed synthetic fixtures. Hard failures such as unauthorized acceptance, invalid evidence promotion, domain leakage, or broken prerequisite ordering cannot be averaged away by a high score.

### 3. Cross-agent evaluation

Wave 6 converts reviewed benchmark fixtures into **oracle-free agent tasks**, accepts normalized `agent-run` artifacts from external wrappers, and scores them using deterministic repository code.

The core does not hard-code model vendors or proprietary CLIs. Any agent host can integrate through the same normalized artifact contract.

## Evidence model

Every investigation moves through explicit states:

```text
hypothesis
    ↓
observed
    ↓
validated
    ↓
regression-verified
```

A finding is not promoted just because a tool, fuzzer, model, or analyzer says so.

A validated case requires, at minimum, evidence such as:

- a pinned environment or target revision;
- a reproducible observation;
- a causal root cause;
- a bounded security consequence;
- positive and negative controls;
- reproducer steps and fixture identity.

`regression-verified` additionally requires evidence that the fixed revision no longer reproduces the issue while controls still behave correctly.

See [docs/research-case-contract.md](docs/research-case-contract.md).

## Capability coverage

The graph currently includes deep workflows across:

- scope, authorization, research routing, attack-surface mapping, and hypothesis generation;
- fuzz harness design, corpus engineering, coverage-guided fuzzing, grammar-aware fuzzing, and stateful fuzzing;
- crash triage, minimization, sanitizer-guided analysis, root-cause analysis, and exploitability triage;
- static/dataflow analysis, symbolic execution, differential testing, binary reconnaissance, and variant hunting;
- memory lifetime, bounds/integer safety, type confusion, and concurrency/race analysis;
- parser/protocol state machines, canonicalization, deserialization boundaries, and namespace confusion;
- authorization, confused-deputy, cache identity, secret/token flow, and tenant isolation;
- kernel, driver/IOCTL, sandbox, browser-process, and JIT invariant analysis;
- containers, cloud IAM, supply-chain review, and dependency trust;
- Android/iOS security, mobile trust boundaries, and local storage/keystore analysis;
- firmware, update trust chains, secure boot, and embedded debug surfaces;
- virtualization guest-host boundaries, virtual devices, and shared memory;
- web routing, SSRF boundaries, uploads, templates, and multi-tenant internals;
- cryptographic protocol misuse, randomness lifecycle, certificates, and hostname validation;
- smart-contract invariants, reentrancy, upgradeability, and oracle trust;
- prompt-injection boundaries, tool confirmation, RAG/memory isolation, connector/plugin trust;
- controlled experiments, evidence ledgers, false-positive elimination, static/dynamic correlation, remediation, regression validation, and reporting.

## Quick start

Clone the repository and run the full deterministic validation stack:

```bash
git clone https://github.com/Nolane-x/Security-skills.git
cd Security-skills

python scripts/validate_skills.py
python scripts/validate_graph.py
python scripts/validate_benchmarks.py
python -m unittest discover -s tests -v
```

Generate the human and machine indexes on demand:

```bash
python scripts/build_catalog.py
python scripts/build_graph.py
```

Generated catalog/graph artifacts are intentionally ignored. Canonical truth remains in `SKILL.md`, `skill.meta.json`, and pack manifests.

## Research-case engine

Validate and route a machine-readable research case:

```bash
python scripts/validate_case.py examples/research-case.example.json
python scripts/route_skills.py examples/research-case.example.json --limit 12
```

The router is advisory-only. It validates authorization and case state first, closes transitive prerequisites, applies domain/context filtering, and returns a deterministic skill order.

A representative memory-safety route may look like:

```text
scope + authorization
  → attack surface
  → fuzzing
  → crash minimization
  → sanitizer evidence
  → lifetime / bounds / type / race analysis
  → evidence validation
  → conservative exploitability triage
  → variant hunt
  → remediation
  → regression verification
```

## Benchmark engine

Wave 5 provides 36 deterministic fixtures across six categories:

1. authorization;
2. domain isolation;
3. evidence-state conformance;
4. false-positive control;
5. remediation/regression routing;
6. representative routing correctness.

Run the portability or full core suite:

```bash
python scripts/run_benchmarks.py benchmarks/suites/portability.json
python scripts/run_benchmarks.py benchmarks/suites/core.json
```

Produce machine and human reports:

```bash
python scripts/run_benchmarks.py benchmarks/suites/core.json \
  --json /tmp/security-skills-benchmark.json \
  --report /tmp/security-skills-benchmark.md
```

See [docs/benchmark-contract.md](docs/benchmark-contract.md).

## Cross-agent evaluation

Wave 6 lets external AI agents be evaluated against the same reviewed security authority without exposing fixture oracles in the task artifact.

Prepare oracle-free tasks:

```bash
python scripts/prepare_agent_tasks.py benchmarks/suites/portability.json --out /tmp/agent-tasks
```

Generate the deterministic reference replay profile:

```bash
python scripts/prepare_replay_runs.py benchmarks/suites/portability.json \
  --profile reference \
  --out /tmp/reference-runs
```

Validate and score normalized runs:

```bash
python scripts/validate_agent_runs.py /tmp/reference-runs
python scripts/evaluate_agent_runs.py benchmarks/suites/portability.json /tmp/reference-runs \
  --json /tmp/agent-evaluation.json \
  --report /tmp/agent-evaluation.md
```

The committed replay profiles are:

- `reference` — conforming deterministic baseline;
- `cautious` — safe but intentionally incomplete `needs-evidence` behavior;
- `faulty` — deterministic negative controls that must fail.

See [agent-eval/README.md](agent-eval/README.md).

## Safe adapter boundary

External agent wrappers may use `scripts/run_agent_adapter.py` with an explicit argv vector.

The adapter boundary is intentionally defensive:

- `shell=False`;
- explicit argv, no shell interpolation;
- timeout enforcement;
- streaming stdout/stderr byte caps;
- child termination on overflow;
- sanitized environment by default;
- credential-like variables only through explicit allowlists;
- untrusted agent output parsed only as data;
- subprocess pipes closed deterministically;
- hidden reasoning / chain-of-thought is neither requested nor stored.

## Portability

`skills/` is the single canonical source. Do not fork skill prose per vendor.

A broadly interoperable project layout is:

```text
<project>/
└── .agents/
    └── skills/
        └── <skill-name>/
            ├── SKILL.md
            └── ...optional local resources...
```

The repository is designed to be usable by modern coding/agent hosts that understand Agent Skills or can consume explicit repository context. Vendor-specific discovery paths can point to the same canonical skill content.

See [docs/compatibility.md](docs/compatibility.md).

## Packs

Packs are curated routing manifests under `packs/`. Major packs include:

- `fuzzing-research`
- `memory-safety`
- `parsers-and-protocols`
- `trust-and-authorization`
- `kernel-sandbox-browser`
- `cloud-and-supply-chain`
- `verification-engineering`
- `mobile-security`
- `firmware-and-boot`
- `virtualization-boundaries`
- `web-framework-internals`
- `cryptographic-assurance`
- `smart-contracts`
- `ai-agent-deep-security`
- `autonomous-research-orchestration`

See [packs/README.md](packs/README.md) for the full set.

## Repository layout

```text
Security-skills/
├── skills/              # canonical Agent Skills
├── packs/               # curated skill routing manifests
├── benchmarks/          # Wave 5 deterministic fixtures and suites
├── agent-eval/          # Wave 6 cross-agent contracts and suites
├── schemas/             # machine-readable schemas
├── scripts/             # validators, routers, evaluators, builders
├── tests/               # deterministic regression tests
├── examples/            # research-case examples
├── docs/                # contracts, compatibility, design documentation
├── sources/             # research-system lineage metadata
├── AGENTS.md             # repository-level agent guidance
├── SECURITY.md           # safety and authorization boundary
└── CONTRIBUTING.md       # contribution requirements
```

## Full validation

No third-party Python package is required.

```bash
python scripts/validate_skills.py
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

CI repeats the critical gates across Ubuntu, macOS, and Windows on Python 3.11 and 3.13, then runs dedicated deterministic `benchmark-core` and `agent-eval-core` jobs.

## Adding a skill

Read [CONTRIBUTING.md](CONTRIBUTING.md) before adding capabilities.

A canonical skill should encode a reusable **decision process**, not a thin wrapper around a tool command. It needs explicit:

- applicability;
- preconditions;
- workflow;
- evidence contract;
- stop conditions;
- output contract;
- graph metadata.

## Security boundary

Intrusive techniques are restricted to local, owned, sandboxed, benchmark/CTF, or explicitly authorized targets.

Proofs should prefer controlled and non-destructive evidence such as assertions, sanitizer reports, minimized crashes, synthetic resources, marker files, policy simulation, and regression tests over persistence, stealth, destructive impact, credential theft, or indiscriminate exploitation.

See [SECURITY.md](SECURITY.md).

## Research lineage

Security Skills distills original workflows from reproducible vulnerability research, autonomous Cyber Reasoning Systems, fuzzing infrastructure, program analysis, reverse engineering, web/mobile/firmware/cloud security, smart-contract analysis, and modern AI-agent security research.

The repository does **not** vendor third-party exploit code or copy third-party prompts.

See [docs/sources.md](docs/sources.md) and [sources/research-systems.json](sources/research-systems.json).

## Documentation

- [Vietnamese README](README-VN.md)
- [Simplified Chinese README](README-CN.md)
- [Compatibility](docs/compatibility.md)
- [Research-case contract](docs/research-case-contract.md)
- [Benchmark contract](docs/benchmark-contract.md)
- [Cross-agent evaluation](agent-eval/README.md)
- [Packs](packs/README.md)
- [Research sources](docs/sources.md)
- [Security policy](SECURITY.md)
- [Contributing](CONTRIBUTING.md)

---

**Security Skills** is built around a simple rule: **a security claim is only as strong as the evidence, controls, and reproducibility behind it.**
