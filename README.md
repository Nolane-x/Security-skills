# Security Skills

[![CI](https://github.com/Nolane-x/Security-skills/actions/workflows/validate.yml/badge.svg)](https://github.com/Nolane-x/Security-skills/actions/workflows/validate.yml)

**English** · [Tiếng Việt](README-VN.md) · [简体中文](README-CN.md)

A **verification-first security skill graph and deterministic cross-agent evaluation framework for AI agents**.

Security Skills gives coding agents, research agents, and autonomous security systems a portable set of reusable security reasoning skills — plus the evidence gates, routing logic, benchmarks, cross-agent conformance tooling, and selectively deep operator runbooks needed to verify that those skills are being used correctly.

> **Stable baseline: Wave 8; Wave 10 depth expansion active** — 83 canonical skills, 20 packs, 26 CI-enforced operator-depth profiles with machine-readable matrices, 36 deterministic benchmark fixtures, and a vendor-neutral cross-agent evaluation harness.

## Why this project exists

Security agents should not jump from a scanner alert, crash, static-analysis warning, or model hypothesis directly to “confirmed vulnerability.” Good security research requires explicit scope, evidence, controls, causal reasoning, reproducibility, and regression validation.

This repository turns that discipline into a portable machine-readable system.

```text
security knowledge
      │
      ▼
83 canonical Agent Skills
      │
      ├──► 26 matrix-enforced operator-depth profiles (Wave 8 + Wave 10 expansion)
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

The result is not just a collection of prompts. It is a **security intelligence system that can validate its own routing, enforce depth contracts, and evaluate how external AI agents follow the same security contract**.

## What it is — and what it is not

**Security Skills is:**

- a portable security reasoning graph for AI agents;
- a set of reusable Agent Skills with explicit applicability and evidence contracts;
- selectively deep operator runbooks and machine-readable safe review contracts for complex high-value domains;
- a deterministic prerequisite-aware router;
- a machine-readable research-case and evidence-state model;
- a benchmark suite for routing, authorization, evidence, false-positive control, and remediation;
- a vendor-neutral harness for comparing normalized agent runs;
- a defensive research framework designed for local, owned, sandboxed, CTF, benchmark, or explicitly authorized targets.

**Security Skills is not:**

- an offensive code collection;
- a replacement for authorization or human security judgment;
- a mechanism for declaring vulnerabilities from tool output alone;
- a vendor-specific prompt pack;
- a benchmark of “general intelligence.” Cross-agent scores measure conformance to this repository's reviewed security contract.

## Current snapshot

| Capability | Current baseline |
| --- | ---: |
| Canonical skills | **83** |
| Validated packs | **20** |
| Operator-depth profiles | **26** |
| Benchmark fixtures | **36** |
| Benchmark categories | **6** |
| Cross-agent portability fixtures | **12** |
| Evidence states | **4** |
| CI environments | **6** |
| Python dependencies | **0 third-party packages** |

CI validates Linux, macOS, and Windows on Python 3.11 and 3.13.

## Four-layer architecture

### 1. Security intelligence graph

Each canonical capability lives once under:

```text
skills/<skill-name>/
├── SKILL.md
└── skill.meta.json
```

`SKILL.md` follows the open Agent Skills model. `skill.meta.json` adds Nolane graph metadata such as domains, prerequisites, composition edges, maturity, and evidence stage without polluting portable skill frontmatter.

Packs under `packs/` reference canonical skills instead of duplicating them.

### 2. Selective operator depth

Wave 8 established the reviewed domain-runbook + CI-enforced machine-readable matrix contract. Each registered profile must cover attack surface, falsifiable hypotheses, controlled validation, false-positive controls, evidence capture, and remediation regression. Each case must additionally provide a benign oracle, positive and negative controls, an explicit stop condition, and a remediation oracle.

Wave 8 established eight profiles covering AI-agent security, authorization boundaries, cloud IAM paths, container isolation, driver interfaces, exploitability/evidence triage, server-side request boundaries, and web routing/middleware. Wave 10 adds `prompt-injection-boundary-analysis` as the ninth profile, `rag-memory-data-isolation-analysis` as the tenth, `connector-plugin-trust-analysis` as the eleventh, `tool-capability-and-confirmation-analysis` as the twelfth, `canonicalization-and-namespace-analysis` as the thirteenth, `confused-deputy-analysis` as the fourteenth, `cache-key-identity-analysis` as the fifteenth, `secrets-and-token-flow-analysis` as the sixteenth, `multi-tenant-data-isolation-analysis` as the seventeenth, `supply-chain-dependency-review` as the eighteenth, `browser-process-boundary-analysis` as the nineteenth, `boot-chain-and-secure-boot-analysis` as the twentieth, `deserialization-trust-analysis` as the twenty-first, `certificate-and-hostname-validation-analysis` as the twenty-second, and `cryptographic-protocol-misuse-analysis` as the twenty-third, and `guest-host-boundary-analysis` as the twenty-fourth, and `memory-lifetime-analysis` as the twenty-fifth, and `concurrency-race-analysis` as the twenty-sixth. Prompt-injection depth adds instruction-lineage, provenance, authority-conflict, decision/effect, counterfactual, and evidence-ceiling contracts. RAG/memory depth adds end-to-end principal binding, derived-state lineage, retrieval-policy traces, lifecycle/revocation generations, bounded convergence, cache/memory coherence, and R0–R5 evidence ceilings. Connector/plugin trust depth adds integration provenance, effective-permission traces, schema/argument state, response binding, composition boundaries, lifecycle generations, C0–C5 evidence ceilings, and deterministic audit-only review cases. Tool capability/confirmation depth adds request-to-action binding, argument-normalization traces, effective-authority reasoning, confirmation tuples, execution-state drift, transaction/retry/idempotency semantics, post-action receipt/final-state verification, and T0–T5 evidence ceilings. Canonicalization/namespace depth adds typed representation-to-identity traces, transformation ordering and non-commutativity, normalization idempotence, policy-key-to-resolved-identity binding, namespace-root and name-to-object state, namespace generations, counterfactual controls, deterministic audit-only review cases, and N0–N5 evidence ceilings. Confused-deputy depth adds causal authority-transfer traces, delegated-versus-ambient authority distinctions, monotonic attenuation, operation/resource and resolved-target binding, delegation generation/lifecycle reasoning, result/receipt binding, counterfactual controls, deterministic audit-only review cases, and D0–D5 evidence ceilings. Cache-key identity depth adds semantic dependency-to-key completeness, canonical key/namespace/entry identity traces, writer/reader provenance, first-writer and reverse-order controls, lifecycle/invalidation generations, deterministic audit-only review cases, counterfactual controls, and K0–K5 evidence ceilings. Secrets/token-flow depth adds credential-class semantics, issuance provenance, possession/storage/propagation boundary traces, verifier-decision reasoning, audience/resource binding, represented-authority and delegation-attenuation traces, lifecycle/revocation generations, deterministic audit-only review cases, counterfactual controls, and S0–S5 evidence ceilings. Multi-tenant isolation depth adds canonical tenant identity and membership/role binding, tenant-context generations, representation/propagation traces, policy/filter and namespace decisions, resolved object/result identity, async/job context, lifecycle/migration generations, ambient-authority controls, deterministic audit-only review cases, counterfactual controls, and M0–M5 evidence ceilings. Supply-chain dependency depth adds source/namespace resolution, immutable artifact identity, integrity/signature/provenance-verifier reasoning, build-hook and toolchain identity, CI trust and cache/reuse binding, release authority, produced-to-released-to-distributed-to-deployed artifact binding, lifecycle/revocation/update generations, deterministic audit-only review cases, counterfactual controls, and SC0–SC5 evidence ceilings. Browser-process boundary depth adds origin/site/frame-to-process identity binding, process and routed-object generations, normalized IPC routing and ownership validation, brokered capability attenuation, ambient-versus-delegated authority separation, privileged-consumer receipt/result binding, lifecycle/revocation controls, deterministic audit-only review cases, counterfactual controls, and B0–B5 evidence ceilings. Boot-chain depth adds root/policy/key-generation provenance, boot-mode and selector identity, signer authorization, rollback/freshness generation, candidate-to-selected-to-loaded component binding, authenticated handoff inheritance, recovery/alternate-path equivalence controls, receipt/attestation correlation, deterministic benign review cases, counterfactual controls, and BC0–BC5 evidence ceilings. Deserialization trust depth adds serialized-artifact/authenticity provenance, parser/canonical-field and schema/version binding, discriminator-to-canonical-runtime-type resolution, resolver/registry generations, construction/hook/secondary-interpretation traces, requested-to-effective reconstructed authority, privileged-consumer receipt/result binding, lifecycle controls, deterministic benign review cases, counterfactual controls, and DT0–DT5 evidence ceilings. Certificate/hostname depth adds intended peer identity, original/redirect/transport/SNI/reference-identity separation, verifier and trust-store generations, selected certification path and trust anchor, certificate constraints, SAN/hostname binding, pin/revocation/callback final-decision traces, authenticated peer/session and mTLS mapping, lifecycle-generation controls, deterministic benign review cases, counterfactual controls, and PKI0–PKI5 evidence ceilings. Cryptographic-protocol depth adds security-goal/protocol intent, peer/role/session and negotiated-suite identity, transcript/authenticated-negotiation binding, key-schedule role/direction/epoch and domain separation, nonce/sequence/record identity, protocol-phase authenticated context, auth-before-use ordering, replay/freshness, rekey/resumption/early-data lifecycle generations, privileged-consumer receipt/result binding, deterministic benign review cases, counterfactual controls, and CP0–CP5 evidence ceilings. Guest-host boundary depth adds guest principal/security-domain binding, interface/device/channel and queue-generation identity, guest-controlled object and descriptor provenance, address-translation/IOMMU/memory-slot generations, shared-object ownership/lifetime, backend/emulation-thread consumer identity, effective host capability, reset/hot-unplug/migration/snapshot lifecycle revocation, privileged-consumer receipt/result binding, deterministic benign review cases, counterfactual controls, and GH0–GH5 evidence ceilings. Memory-lifetime depth adds logical-object versus address/handle identity, allocation/acquisition generations, owner/alias and retain/borrow/refcount provenance, invalidation/destruction/reuse binding, async callback/work-item lifecycle, final-consumer capability and receipt/result binding, deterministic benign review cases, counterfactual controls, alternative-explanation elimination, and ML0–ML5 evidence ceilings. Concurrency-race depth adds shared-invariant and state-generation identity, actor/operation generations, scheduler/executor identity, synchronization epochs and happens-before edges, check/use and interfering-transition binding, commit points, cancellation/retry/teardown generations, single-effect semantics, final-consumer capability and receipt/result binding, deterministic schedule controls, counterfactual schedules, alternative-explanation elimination, and CR0–CR5 evidence ceilings. All profiles remain lab/owned/sandbox/authorized-only and prefer synthetic canaries, mock services, fake identities, policy simulation, inert action sinks, and read-only evidence over risky real-world proof.

See [docs/operator-depth-contract.md](docs/operator-depth-contract.md).

### 3. Deterministic benchmark authority

Wave 5 evaluates the production case validator and router against reviewed synthetic fixtures. Hard failures such as unauthorized acceptance, invalid evidence promotion, domain leakage, or broken prerequisite ordering cannot be averaged away by a high score.

### 4. Cross-agent evaluation

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
- web routing, server-side request boundaries, uploads, templates, and multi-tenant internals;
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
python scripts/validate_operator_depth.py
python scripts/validate_graph.py
python scripts/validate_benchmarks.py
python -m unittest discover -s tests -v
```

Generate the human and machine indexes on demand:

```bash
python scripts/build_catalog.py
python scripts/build_graph.py
```

Generated catalog/graph artifacts are intentionally ignored. Canonical truth remains in `SKILL.md`, `skill.meta.json`, pack manifests, and the selective operator-depth registry/runbooks/machine-readable matrices.

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

## Operator depth

Wave 8 established scenario-enforced operator depth for eight profiles. Wave 10 expands the current registry to twenty-six with `prompt-injection-boundary-analysis` as the ninth profile, `rag-memory-data-isolation-analysis` as the tenth, `connector-plugin-trust-analysis` as the eleventh, `tool-capability-and-confirmation-analysis` as the twelfth, `canonicalization-and-namespace-analysis` as the thirteenth, `confused-deputy-analysis` as the fourteenth, `cache-key-identity-analysis` as the fifteenth, `secrets-and-token-flow-analysis` as the sixteenth, `multi-tenant-data-isolation-analysis` as the seventeenth, `supply-chain-dependency-review` as the eighteenth, `browser-process-boundary-analysis` as the nineteenth, `boot-chain-and-secure-boot-analysis` as the twentieth, `deserialization-trust-analysis` as the twenty-first, `certificate-and-hostname-validation-analysis` as the twenty-second, `cryptographic-protocol-misuse-analysis` as the twenty-third, and `guest-host-boundary-analysis` as the twenty-fourth, and `memory-lifetime-analysis` as the twenty-fifth:

- `ai-agent-security-assessment`
- `authorization-boundary-analysis`
- `boot-chain-and-secure-boot-analysis`
- `browser-process-boundary-analysis`
- `cache-key-identity-analysis`
- `canonicalization-and-namespace-analysis`
- `certificate-and-hostname-validation-analysis`
- `cloud-iam-path-analysis`
- `concurrency-race-analysis`
- `confused-deputy-analysis`
- `connector-plugin-trust-analysis`
- `container-isolation-review`
- `cryptographic-protocol-misuse-analysis`
- `deserialization-trust-analysis`
- `driver-ioctl-surface-analysis`
- `exploitability-triage`
- `guest-host-boundary-analysis`
- `memory-lifetime-analysis`
- `multi-tenant-data-isolation-analysis`
- `prompt-injection-boundary-analysis`
- `rag-memory-data-isolation-analysis`
- `secrets-and-token-flow-analysis`
- `server-side-request-boundary-analysis`
- `supply-chain-dependency-review`
- `tool-capability-and-confirmation-analysis`
- `web-routing-and-middleware-analysis`

Validate them with:

```bash
python scripts/validate_operator_depth.py
```

The validator rejects unsafe paths, missing artifacts, duplicate profiles or scenario IDs, malformed or incomplete matrices, disabled lab-only policy, missing required methodology sections, insufficient authorization/evidence/control discipline, unspecified benign oracles, and missing explicit stop conditions. It intentionally does not reward file length or payload volume.

See [docs/operator-depth-contract.md](docs/operator-depth-contract.md).

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
├── skills/              # canonical Agent Skills and selective depth resources
├── operator-depth/      # CI-enforced operator-depth profile registry
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

CI repeats the critical gates across Ubuntu, macOS, and Windows on Python 3.11 and 3.13, then runs dedicated deterministic `benchmark-core`, `agent-eval-core`, and `superiority-court-core` jobs.

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

For selective deep methodology on an existing high-value skill, follow [the operator-depth contract](docs/operator-depth-contract.md) instead of creating a near-duplicate skill.

## Security boundary

Intrusive techniques are restricted to local, owned, sandboxed, benchmark/CTF, or explicitly authorized targets.

Proofs should prefer controlled and non-destructive evidence such as assertions, sanitizer reports, minimized crashes, synthetic resources, marker files, policy simulation, mock services, synthetic canaries, and regression tests rather than uncontrolled or destructive proof.

See [SECURITY.md](SECURITY.md).

## Research lineage

Security Skills distills original workflows from reproducible vulnerability research, autonomous Cyber Reasoning Systems, fuzzing infrastructure, program analysis, reverse engineering, web/mobile/firmware/cloud security, smart-contract analysis, and modern AI-agent security research.

The repository does **not** vendor third-party offensive code or copy third-party prompts.

See [docs/sources.md](docs/sources.md) and [sources/research-systems.json](sources/research-systems.json).

## Documentation

- [Vietnamese README](README-VN.md)
- [Simplified Chinese README](README-CN.md)
- [Compatibility](docs/compatibility.md)
- [Research-case contract](docs/research-case-contract.md)
- [Operator-depth contract](docs/operator-depth-contract.md)
- [Benchmark contract](docs/benchmark-contract.md)
- [Cross-agent evaluation](agent-eval/README.md)
- [Packs](packs/README.md)
- [Research sources](docs/sources.md)
- [Security policy](SECURITY.md)
- [Contributing](CONTRIBUTING.md)

---

**Security Skills** is built around a simple rule: **a security claim is only as strong as the evidence, controls, and reproducibility behind it.**