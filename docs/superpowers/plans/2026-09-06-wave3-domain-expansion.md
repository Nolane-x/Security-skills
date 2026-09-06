# Wave 3 Domain Expansion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: use test-driven development for graph behavior changes and verification-before-completion before integration.

**Goal:** Expand the verified Wave 2 graph from 43 skills/12 packs to 70+ skills with deep mobile, firmware, virtualization, web-framework, cryptographic, smart-contract, and AI-agent domain coverage.

**Architecture:** Preserve canonical `SKILL.md` portability. Every new domain capability receives a `skill.meta.json` sidecar and is routed through a thin `packs/*.json` manifest. Existing evidence states and authorization boundaries remain mandatory; new pack validation rejects entrypoints outside pack membership and prerequisite ordering errors inside default flows.

**Tech stack:** Markdown, JSON, dependency-free Python 3.11+, unittest.

## Global constraints

- No vendor-specific skill body forks.
- No destructive payloads, persistence, credential theft, stealth, or indiscriminate exploitation guidance.
- Intrusive/dynamic steps require owned, local, sandboxed, benchmark/CTF, or explicitly authorized scope.
- Security claims stay evidence-gated: hypothesis -> observed -> validated -> regression-verified.
- Skills analyze primitives and trust boundaries rather than weaponizing them.

### Task 1: Strengthen pack graph validation

- Add failing tests for entrypoint-not-member and prerequisite ordering violations in `default_flow`.
- Implement minimal validation in `scripts/security_graph.py`.
- Run graph tests and the full suite.

### Task 2: Mobile security pack

Add Android component/deep-link/WebView/local-secret analysis; iOS entitlement/link analysis; mobile network trust analysis. Add metadata and `packs/mobile-security.json`.

### Task 3: Firmware and virtualization packs

Add firmware attack surface, update trust chain, secure boot, embedded debug interfaces; guest-host boundary, virtual device model, and shared-memory analysis. Add `firmware-and-boot` and `virtualization-boundaries` packs.

### Task 4: Web and cryptographic assurance packs

Add routing/middleware, SSRF boundary, upload pipeline, template/expression boundary, multi-tenant isolation; crypto misuse, nonce/randomness lifecycle, and certificate/hostname validation. Add two packs.

### Task 5: Smart-contract and deep AI-agent packs

Add smart-contract invariant, reentrancy-state, upgradeability/storage layout, oracle trust; prompt injection boundary, tool capability/confirmation, RAG-memory isolation, connector/plugin trust. Add two packs.

### Task 6: Documentation and full verification

Update README/architecture/source lineage. Validate every skill, graph, pack, generated index, JSON file, unittest, and whitespace. Keep generated catalog/graph ignored and build-on-demand.
