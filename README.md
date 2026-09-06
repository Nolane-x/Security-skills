# Security Skills

A portable, verification-first security research skill graph for AI agents.

The canonical capability format is the open **Agent Skills** structure: each reusable capability lives under `skills/<name>/SKILL.md`, with optional local references/scripts/assets. Nolane adds a machine-readable sidecar (`skill.meta.json`) and pack manifests without polluting portable Agent Skills frontmatter.

The project teaches agents **how to reason, route, collect evidence, reject false positives, and close regressions**. It is deliberately not a payload collection.

## Current Wave 2

- **43 canonical skills**
- **12 validated skill packs**
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
- remediation, patch-diff analysis, regression matrices, secure code review and AI-agent security.

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
