# Security Skills

A portable, verification-first security research skill graph for AI agents.

The canonical capability format is the open **Agent Skills** structure: each reusable capability lives under `skills/<name>/SKILL.md`, with optional local references/scripts/assets. Nolane adds a machine-readable sidecar (`skill.meta.json`) and pack manifests without polluting portable Agent Skills frontmatter.

The project teaches agents **how to reason, route, collect evidence, reject false positives, and close regressions**. It is deliberately not a payload collection.

## Current Wave 6

- **83 canonical skills**
- **20 validated skill packs**
- **36 deterministic benchmark fixtures** across six conformance categories
- **12-fixture portability smoke suite** for cross-platform CI
- **vendor-neutral cross-agent evaluation harness** with oracle-free tasks and normalized agent-run artifacts
- deterministic `reference`, `cautious`, and `faulty` offline replay profiles
- deterministic build-on-demand catalog and graph indexes
- source-controlled graph metadata and pack manifests
- prerequisite cycle detection and unknown-node rejection
- dependency-free Python validation
- Linux/macOS/Windows CI on Python 3.11 and 3.13

The current graph spans:

- research routing, scope, authorization, attack-surface mapping, hypothesis generation;
- fuzz harness design, corpus engineering, coverage-guided, grammar-aware and stateful fuzzing;
- crash minimization, sanitizer-guided analysis, exploitability triage, evidence validation;
- static/dataflow, symbolic execution, binary reconnaissance, differential testing, variant hunting;
- memory lifetime, bounds/integer, type confusion, concurrency/race analysis;
- parser and protocol state machines, canonicalization/namespaces, deserialization trust;
- authorization, confused deputy, cache identity, secret/token flow;
- kernel, driver/IOCTL, sandbox, browser process and JIT invariant analysis;
- container isolation, cloud IAM, supply-chain dependency review;
- remediation, patch-diff analysis, regression matrices, secure code review and AI-agent security;
- mobile Android/iOS trust boundaries, firmware/update/boot/debug surfaces, virtualization guest-host/device/shared-memory boundaries;
- web-framework routing/SSRF/upload/template/multi-tenant internals, cryptographic protocol/randomness/PKI assurance, smart-contract invariants/reentrancy/upgrades/oracles, and deep AI-agent prompt/tool/RAG/plugin trust;
- research-case state management, controlled experiments, evidence ledgers, false-positive elimination, static/dynamic correlation, route selection, fix-validation experiments and security-research reporting.

Generate the human and machine indexes on demand with `python scripts/build_catalog.py` and `python scripts/build_graph.py`. The generated files are intentionally ignored so `SKILL.md`, `skill.meta.json`, and pack manifests remain the only source of truth.

## Why the graph matters

A security agent should not jump from “tool output” to “confirmed vulnerability.” The graph routes through explicit research states:

```text
hypothesis
    ↓
observed
    ↓
validated
    ↓
regression-verified
```

A typical memory-safety route may become:

```text
attack surface
  → fuzz harness
  → corpus/campaign
  → crash minimization
  → sanitizer evidence
  → lifetime/bounds/type/race root cause
  → evidence validation
  → conservative exploitability triage
  → variant hunt
  → remediation
  → regression matrix
```

Every hop has its own evidence contract and stop conditions.

## Research-case engine

Wave 4 adds a dependency-free machine-readable case contract so an agent can preserve evidence state across long investigations instead of re-deriving status from prose. The case validator enforces authorization and evidence gates; the router is advisory-only and closes skill prerequisites transitively before returning a deterministic route.

```bash
python scripts/validate_case.py examples/research-case.example.json
python scripts/route_skills.py examples/research-case.example.json --limit 12
```

A case cannot skip directly from `hypothesis` to `validated`. `validated` requires a pinned reproducer, causal root cause, bounded security consequence, and positive/negative controls. `regression-verified` additionally requires a fixed revision where the same evidence no longer reproduces while controls remain healthy. See [docs/research-case-contract.md](docs/research-case-contract.md).

## Benchmark and evaluation layer

Wave 5 adds a deterministic conformance benchmark above the production case validator and advisory router. Fixtures are synthetic or controlled JSON cases; they never execute exploits or target live external systems.

```bash
python scripts/validate_benchmarks.py
python scripts/run_benchmarks.py benchmarks/suites/portability.json
python scripts/run_benchmarks.py benchmarks/suites/core.json --json /tmp/security-skills-benchmark.json --report /tmp/security-skills-benchmark.md
```

The `core` suite contains 36 fixtures: six each for authorization, domain isolation, evidence-state conformance, false-positive control, remediation/regression routing, and representative domain routing. A passing suite requires zero enabled hard-gate failures and an aggregate score at or above its committed threshold. See [docs/benchmark-contract.md](docs/benchmark-contract.md).

## Cross-agent evaluation

Wave 6 converts the reviewed Wave 5 portability cases into **oracle-free agent tasks**. An external wrapper can feed those tasks to any agent host and return the same normalized `agent-run` JSON contract. The repository does not hard-code vendor APIs or proprietary CLI commands; the adapter is an untrusted transport boundary and deterministic repository code remains the scoring authority.

```bash
python scripts/prepare_agent_tasks.py benchmarks/suites/portability.json --out /tmp/agent-tasks
python scripts/prepare_replay_runs.py benchmarks/suites/portability.json --profile reference --out /tmp/reference-runs
python scripts/validate_agent_runs.py /tmp/reference-runs
python scripts/evaluate_agent_runs.py benchmarks/suites/portability.json /tmp/reference-runs --json /tmp/agent-matrix.json --report /tmp/agent-matrix.md
```

Real adapters may use `scripts/run_agent_adapter.py` with an explicit argv vector. It uses `shell=False`, time/output limits, and a sanitized child environment; credentials are never forwarded unless explicitly allowlisted. CI uses offline replay profiles only. Comparative matrix scores measure conformance to the selected benchmark contract, not universal model intelligence. See [agent-eval/README.md](agent-eval/README.md).

## Portability model

`skills/` is the single canonical source. Do not fork the prose per vendor.

A broadly interoperable project layout is:

```text
<project>/
└── .agents/
    └── skills/
        └── <skill-name>/
            ├── SKILL.md
            └── ...optional local resources...
```

`skill.meta.json` is Nolane graph metadata. Hosts that only understand Agent Skills can ignore it. Agents without native skill discovery can use the repository-level `AGENTS.md` plus the same canonical skill files as explicit context. See [docs/compatibility.md](docs/compatibility.md).

## Packs

Packs are routing manifests under `packs/`; they reference canonical skills rather than copying them. Current deep packs include:

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
- plus compact foundation/program-analysis/remediation/AI-agent packs.

See [packs/README.md](packs/README.md).

## Validate

No third-party Python package is required:

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

After changing canonical skills or graph metadata:

```bash
python scripts/build_catalog.py
python scripts/build_graph.py
```

## Adding skills

Read [CONTRIBUTING.md](CONTRIBUTING.md). A new skill must encode a reusable decision process rather than a thin tool command. It needs explicit applicability, preconditions, workflow, evidence contract, stop conditions, output, and graph metadata.

## Research lineage

The project distills original workflows from reproducible vulnerability research, autonomous Cyber Reasoning Systems, fuzzing infrastructure, program analysis, reverse engineering, and domain security ecosystems. It does not vendor third-party exploit code or copy third-party prompts. See [docs/sources.md](docs/sources.md) and [sources/research-systems.json](sources/research-systems.json).

## Security boundary

Intrusive techniques are restricted to local, owned, sandboxed, benchmark/CTF, or explicitly authorized targets. Proofs prefer assertions, sanitizer evidence, controlled crashes, synthetic resources, marker files, policy simulation, and regression tests over destructive or persistent effects. See [SECURITY.md](SECURITY.md).
