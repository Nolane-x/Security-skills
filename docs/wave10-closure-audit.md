# Wave 10 Closure Audit

**Status:** closed baseline  
**Closure base:** `main@896ad4d1e3bd65c0f249319740669f1c32e63b45`  
**Final operator-depth target:** 40 profiles  
**Canonical architecture preserved:** 83 skills, 20 packs  
**License:** Apache-2.0

## Purpose

Wave 10 was a depth program, not a skill-count expansion program. Its purpose was to take selected high-value canonical security skills and add deeper, CI-enforced operator methodology without duplicating the canonical skill graph or changing benchmark, routing, or cross-agent authority merely to inflate repository size.

The closure baseline therefore freezes the intended architecture at:

- **83 canonical skills** under `skills/`;
- **20 routing packs** under `packs/`;
- **40 CI-enforced operator-depth profiles** registered in `operator-depth/profiles.json`;
- **36 deterministic benchmark fixtures** across the existing benchmark authority;
- **12 portability fixtures** used by the cross-agent evaluation path;
- **zero required third-party Python packages** for the core validation path;
- **Apache License 2.0** at the repository root.

Wave 10 ends here by design. Future work should prioritize correctness, evidence quality, interoperability, benchmark quality, maintenance, and targeted depth improvements. It should not automatically increase the profile count or canonical skill count.

## Closure invariants

The closure test in `tests/test_wave10_closure.py` makes the release baseline machine-checkable.

It verifies that:

1. exactly 83 canonical `SKILL.md` entry points exist;
2. exactly 20 JSON pack manifests exist;
3. the operator-depth registry remains schema version 2;
4. exactly 40 unique operator-depth profiles are registered;
5. every registered profile points to an existing canonical skill;
6. every profile remains `lab_only: true`;
7. every registered runbook and scenario/review-case matrix exists;
8. all three public READMEs publish the same 83 / 20 / 40 Wave 10 baseline;
9. all three public READMEs expose the Apache-2.0 license;
10. the root `LICENSE` is the complete Apache License 2.0 text.

These checks are intentionally architectural. They do not attempt to replace the deeper per-profile contract tests, benchmark gates, graph validation, or cross-agent evaluation suite.

## Mechanism-coverage audit

The forty selected operator-depth profiles span the repository's highest-risk causal boundaries rather than one narrow vulnerability class.

### Authorization, identity, and isolation

Depth coverage includes authorization boundaries, confused-deputy behavior, cache identity, secret/token flow, tenant isolation, cloud IAM, container isolation, sandbox boundaries, and connector/plugin trust.

The recurring mechanism is identity or authority drift across a boundary: who requested an operation, which principal is effective, what scope is active, which state generation is authoritative, and whether downstream consumers bind to the same identity and policy snapshot.

### Parsing, protocol, and representation boundaries

Depth coverage includes canonicalization/namespace behavior, deserialization trust, parser state machines, protocol state machines, file upload processing, template-expression boundaries, server-side request boundaries, and web routing/middleware.

The recurring mechanism is representation or state-machine divergence: one component interprets bytes, names, states, routes, or templates differently from another component that makes the security decision.

### Memory, runtime, and low-level execution

Depth coverage includes memory lifetime, bounds/integer reasoning, type confusion, concurrency/race behavior, JIT invariants, driver/IOCTL surfaces, browser process boundaries, and exploitability triage.

The recurring mechanism is temporal or structural mismatch between the state assumed by a security decision and the state actually consumed by runtime execution.

### Platform, boot, firmware, and virtualization

Depth coverage includes secure boot, firmware update trust chains, guest-host boundaries, containers, sandboxing, browser processes, and low-level driver interfaces.

The recurring mechanism is trust transfer across privilege layers, update generations, boot measurements, shared resources, or isolation boundaries.

### Cryptography and external trust

Depth coverage includes certificate/hostname validation, cryptographic protocol misuse, nonce/randomness lifecycle, and oracle/external-data trust.

The recurring mechanism is binding: identity to key material, message to protocol state, nonce to uniqueness domain, or external data to an authenticated and freshness-constrained source.

### AI-agent security

Depth coverage includes AI-agent security assessment, prompt-injection boundaries, RAG/memory data isolation, tool capability and confirmation, and connector/plugin trust.

The recurring mechanism is authority separation between untrusted content, model interpretation, memory/retrieval context, tool execution, user confirmation, and external connectors.

### Smart contracts

The final three profiles cover smart-contract invariants, reentrancy state, and upgradeability. They bind transaction/call generations, protocol invariants, callback/reentry paths, governance/upgrade authority, implementation routing, storage interpretation, initialization/migration state, and rollback lifecycle.

Profile #40, `smart-contract-upgradeability-analysis`, is the final planned Wave 10 profile.

## Evidence discipline

Operator depth remains evidence-first.

A tool result, scanner finding, model hypothesis, static warning, or suspicious trace does not by itself justify a validated security claim. The repository continues to distinguish:

```text
hypothesis
    ↓
observed
    ↓
validated
    ↓
regression-verified
```

Deep profiles add deterministic methodology for:

- provenance and generation binding;
- positive and negative controls;
- alternative-explanation elimination;
- bounded safe oracles;
- explicit stop conditions;
- downstream-consumer evidence;
- counterfactual checks;
- remediation replay and regression verification.

## Safety boundary

Closure does not relax the repository's safety model.

Operator-depth validation remains restricted to local, owned, sandboxed, benchmark/CTF, or explicitly authorized environments. Profiles prefer synthetic identities, mock services, inert markers, read-only snapshots, bounded state transitions, and reversible fixtures over risky real-world proof.

No closure claim should be interpreted as authorization to test arbitrary third-party systems.

## What closure does not claim

This baseline does **not** claim that:

- every one of the 83 canonical skills needs an operator-depth profile;
- line count or repository size is a quality metric;
- forty profiles imply complete security coverage;
- an internal deterministic benchmark proves superiority over an external system;
- a passing test suite proves absence of vulnerabilities.

The closure claim is narrower and reproducible: the repository has reached its planned Wave 10 operator-depth architecture and now has a machine-checkable release baseline.

## Maintenance policy after Wave 10

Changes after closure should normally fall into one of these classes:

1. fix an incorrect, ambiguous, or unsafe contract;
2. improve evidence quality or false-positive discrimination;
3. improve portability or host integration without forking canonical skill prose;
4. strengthen deterministic tests, benchmarks, or regression fixtures;
5. update research lineage and factual references;
6. improve documentation, onboarding, or localization;
7. repair security or reliability defects.

Increasing the canonical skill count, pack count, or operator-depth profile count is no longer the default direction. Such expansion should require a concrete uncovered mechanism, a non-duplicative design, and an explicit reviewed architecture change.

## Verification

Run the complete validation stack:

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

CI repeats the critical gates across Linux, macOS, and Windows on Python 3.11 and 3.13 and then exercises the benchmark, cross-agent, and superiority-court regression jobs.

## Final baseline

Wave 10 closes at **83 canonical skills / 20 packs / 40 operator-depth profiles**.

The intended next phase is not automatic expansion. It is to keep this baseline factual, reproducible, safe, portable, and difficult to regress.
