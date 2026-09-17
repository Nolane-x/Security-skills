# Wave 10 Profile #21 — Certificate And Hostname Validation Depth Implementation Plan

> Execute strictly test-first. After a valid RED, the dedicated test is authority and must not be weakened to fit implementation.

**Goal:** deepen `certificate-and-hostname-validation-analysis` into a deterministic operator-depth profile proving intended peer identity, reference-name binding, selected trust path/anchor generation, SAN/name and usage decisions, pin/revocation lifecycle, application final-decision behavior, established-session peer identity, and mTLS certificate-to-principal mapping using local synthetic fixtures only.

**Base:** `main@e4979d27272ea059464b9285b5e452643b8f36f1`

**Final scope:** exactly nine paths defined by the design spec. No metadata, graph, pack, routing, benchmark, eval-authority, or workflow-semantic changes.

## Task 1 — Freeze semantics with a dedicated test

Create only `tests/test_certificate_hostname_depth.py`.

The test must contain exactly four high-level test methods:

1. canonical skill: required causal sections, full chain anchor, distinctions, PKI0–PKI5, counterfactuals, evidence ceiling, and retained canonical `Evidence contract`;
2. runbook: common methodology plus application-intent/reference, route/SNI, trust generation, chain/path, SAN/name, EKU/usage, pin, revocation, callback, session-peer, mTLS mapping, lifecycle traces;
3. review cases: version 1, at least three scenarios, required IDs, all common/domain fields, substantive strings, local/synthetic safe oracle, explicit stop condition, remediation oracle, PKI-level syntax;
4. registry: version 2, at least 21 profiles, exactly one certificate-hostname entry, expected paths, `lab_only: true`, unchanged common required sections.

Commit the test alone and open a Draft PR at the exact test-first SHA. Accept RED only if failures are the intended missing-depth failures while pre-existing validators, graph/index, benchmarks, portability, and existing operator-depth gates remain healthy with no unexpected unittest errors.

## Task 2 — Deepen the canonical skill

Update `skills/certificate-and-hostname-validation-analysis/SKILL.md` while preserving portable frontmatter identity and the mandatory canonical structure.

Required semantic sections include:

- `## Causal peer-identity model`
- `## Application intent and reference identity`
- `## Route, redirect, proxy, and SNI binding`
- `## Trust-store and path authority`
- `## SAN, hostname, and service-role validation`
- `## Pinning and revocation lifecycle`
- `## Application callback and final decision`
- `## mTLS certificate-to-principal mapping`
- `## Peer-identity evidence ladder`
- `## Counterfactual proof`
- `## Alternative explanations`
- `## Evidence ceiling`
- `## Evidence contract`

Freeze the exact normalized causal chain and distinctions from the design. Safety remains local/synthetic only.

## Task 3 — Add transition-level operator runbook

Create `skills/certificate-and-hostname-validation-analysis/references/operator-runbook.md` with the exact common and domain sections from the design spec.

The runbook must operationalize evidence transitions rather than repeat generic TLS advice. It must explicitly separate chain/path validity, hostname/reference identity, usage/role, pin/revocation policy, library verifier result, application callback result, established-session identity, and mTLS application-principal mapping.

## Task 4 — Add deterministic benign review cases

Create `skills/certificate-and-hostname-validation-analysis/references/operator-review-cases.json` version 1 with at least:

- `reference-name-chain-policy-binding`
- `pin-revocation-generation-binding`
- `mtls-certificate-principal-binding`

All common and domain-specific fields frozen by the test must be substantive. Use synthetic CAs/certificates, loopback endpoints, mock revocation status, test-only pins, local redirects/proxies, mock callbacks, and inert principal sinks. Stop before any third-party impersonation/interception, production key use, public DNS modification, or non-test root installation.

## Task 5 — Register exactly one profile

Update `operator-depth/profiles.json` after valid RED. Add exactly one object for `certificate-and-hostname-validation-analysis` pointing to `references/operator-runbook.md` and `references/operator-review-cases.json`, with `lab_only: true` and the unchanged six common required sections. Keep schema version 2 and every pre-existing registration unchanged.

## Task 6 — Behavioral verification

Push Tasks 2–5 without changing the dedicated test. Require full success on the exact behavioral SHA:

- six Ubuntu/macOS/Windows × Python 3.11/3.13 matrix jobs;
- `benchmark-core` including byte-identical result;
- `agent-eval-core` including cautious/faulty controls and deterministic matrix;
- `superiority-court-core` including deterministic court output.

If a failure appears, use root-cause debugging and modify production artifacts only unless the test itself is demonstrably wrong.

## Task 7 — Docs-only public finalization

Only after behavioral FULL GREEN, update exactly:

- `README.md`
- `docs/operator-depth-contract.md`

Publish 21 CI-enforced profiles, identify `certificate-and-hostname-validation-analysis` as the twenty-first, summarize its causal identity/authority/lifecycle model and PKI0–PKI5 ceiling, and retain the external-superiority caveat.

Prove the delta from behavioral GREEN to final candidate is exactly these two docs.

## Task 8 — Exact-head integration gate

On the final candidate:

1. confirm total PR scope is exactly nine expected paths;
2. require full exact-head CI GREEN;
3. create no commit afterward;
4. freshly verify final head, base, main SHA, changed paths, and mergeable state;
5. require no base drift;
6. mark Ready and merge only the exact reviewed head SHA.

## Task 9 — Post-merge closure

On the merge commit:

1. verify `main` points to the merge SHA;
2. verify parent 1 = pre-merge main and parent 2 = exact final PR head;
3. require post-merge push CI FULL GREEN;
4. read `operator-depth/profiles.json`, `README.md`, and `docs/operator-depth-contract.md` directly from the merge SHA;
5. verify registry version 2, 21 profiles, exactly one new entry, correct paths, `lab_only: true`, README/docs count 21 and PKI0–PKI5 publication;
6. write closure provenance with test-first SHA, RED run, behavioral authority, exact-head run, merge topology, post-merge run, exact scope, safety boundary, and no unsupported external-superiority claim.

Only then declare Wave 10 profile #21 complete.