# Wave 10 profile #22 — certificate and hostname validation depth design

## Context

`certificate-and-hostname-validation-analysis` is already canonical, but its current skill remains comparatively shallow. It inventories intended peer identity, trust policy, certificate-chain validation, hostname matching, callbacks, pinning, and controlled certificate matrices. It does not yet freeze the causal bindings required to distinguish a valid chain from an authorized peer identity, current trust-policy state from stale session/cache state, or verifier output from the application's final effective authentication decision.

This profile deepens that existing capability rather than creating a duplicate skill.

## Goal

Promote `certificate-and-hostname-validation-analysis` into the twenty-second CI-enforced operator-depth profile with deterministic, benign, evidence-first reasoning over peer identity, path building, certificate constraints, hostname/reference-identity matching, pin/revocation policy, callback overrides, authenticated-session identity, and trust-policy lifecycle generations.

## Causal model

The profile freezes the following end-to-end causal chain:

`intended peer identity -> endpoint/redirect/SNI state -> verifier configuration -> trust-store identity -> trust-store generation -> presented chain identity -> path-building state -> selected trust-anchor identity -> certificate constraints/validity/EKU/KU/name-constraints state -> SAN/reference-identity state -> canonical reference identity -> hostname/identity match decision -> pin/revocation policy state -> callback/override state -> effective accept/reject decision -> authenticated peer/session identity -> privileged consumer boundary -> bounded synthetic result -> receipt/result binding -> trust/pin/revocation/session lifecycle generation`

The chain is evidence-oriented rather than payload-oriented. Each transition must be attributable to a concrete identity, policy decision, or lifecycle generation.

## Required distinctions

The canonical skill and operator runbook must explicitly preserve these non-equivalences:

- chain validation success != hostname/reference-identity validation success;
- trusted root != authorized peer identity;
- SNI value != verification hostname/reference identity;
- signature validity != policy authorization;
- SAN text != canonical reference identity;
- pin match != complete PKI validation;
- revocation lookup success/absence != complete peer authorization;
- callback reachability != justified verification override;
- certificate acceptance != mTLS account/principal authorization;
- cached/resumed session != current trust-store/pin/revocation policy generation;
- redirect target != original authenticated peer identity;
- certificate subject/CN text != authoritative hostname match when SAN rules apply;
- verifier success != application-level authenticated-session binding;
- connection success != receipt/result binding;
- benign synthetic wrong-peer acceptance != broad interception capability.

## Invariants

1. **Reference-identity binding** — The application must define the identity it intends to authenticate before interpreting certificate names. Endpoint text, redirect targets, SNI, and verification reference identity must be recorded separately.
2. **Path-policy binding** — The accepted path must be attributable to the exact trust store, selected anchor, algorithm/constraint policy, and trust-store generation used for the decision.
3. **Name-binding integrity** — SAN/reference-identity canonicalization and matching must be traceable; textual coincidence alone is insufficient.
4. **Override accountability** — A custom callback or verifier override must expose its input verifier state, explicit policy basis, decision, and effective consequence.
5. **Pin/revocation composition** — Pinning and revocation are additional policy dimensions; neither may silently replace unrelated identity/path requirements unless the documented policy explicitly says so.
6. **Session-generation freshness** — Session resumption, connection pooling, cached verification state, or retained client-certificate/account mappings must not silently outlive relevant trust/pin/revocation generations.
7. **Consumer binding** — Acceptance must be bound to the authenticated peer/session identity actually consumed by the privileged operation, plus a result/receipt proving the bounded synthetic effect.
8. **Counterfactual causality** — Changing exactly one causal variable at a time must predictably change or preserve the decision according to policy.

## Deterministic benign review cases

The profile must provide at least three substantive cases:

1. `chain-vs-reference-identity-binding` — distinguish a valid path from wrong reference identity, redirect/SNI confusion, and SAN canonicalization behavior.
2. `callback-pin-effective-decision-binding` — prove whether callback overrides, pin policy, and verifier outputs compose into the intended effective accept/reject decision without treating callback reachability as proof.
3. `trust-policy-session-generation-binding` — test trust-store/pin/revocation generation changes against session resumption/cache/pool reuse and authenticated-session identity.

All cases use synthetic CA hierarchies, synthetic hostnames, local mock endpoints, inert canaries, read-only synthetic capabilities, or bounded reversible owner-controlled effects. No real interception, public-host impersonation, credential capture, external network abuse, or production certificate use is required.

## Evidence ladder

- **PKI0 — mapped:** peer-identity, endpoint, verifier, trust-store, path, name, callback, pin, revocation, session, and lifecycle surfaces are enumerated.
- **PKI1 — divergence observed:** a deterministic identity/policy/generation divergence is observed, but causal acceptance is not yet proven.
- **PKI2 — policy mismatch demonstrated:** controlled inputs show a deterministic path/name/override/pin/revocation/session-policy mismatch with positive and negative controls.
- **PKI3 — inert wrong-context acceptance:** a synthetic wrong-peer or stale-policy context is accepted in a bounded inert setup, with direct attribution to the relevant decision path.
- **PKI4 — bounded synthetic authority effect:** the wrong-context acceptance is causally bound to a bounded reversible synthetic authenticated-session effect or read-only synthetic capability.
- **PKI5 — regression-verified causal proof:** PKI4 plus exact intended/reference identity, endpoint/SNI/redirect provenance, trust-store and anchor generation, path constraints, SAN/canonical-name trace, pin/revocation state, callback decision trace, effective authenticated-session identity, lifecycle generation, privileged-consumer/result binding, meaningful counterfactuals, eliminated alternatives, and remediation regression.

No chain-success flag, signature-success flag, callback trace, pin match, revocation response, connection success, or TLS debug log may skip missing causal bindings.

## Counterfactual controls

The runbook must require bounded one-variable-at-a-time controls, including examples such as:

- same chain, correct vs wrong reference identity;
- same reference identity, trusted vs untrusted anchor;
- same chain/name, callback override enabled vs disabled;
- same chain/name, matching vs non-matching pin;
- same policy, current vs stale trust/pin/revocation generation;
- same certificate/account mapping, current vs rotated client-certificate generation;
- same endpoint, redirect/reference-identity binding preserved vs changed;
- same authenticated session, bounded consumer checks correct peer identity vs only connection success.

## Alternative explanations

Evidence review must explicitly eliminate relevant alternatives before promotion, including test-only permissive modes, debug roots, platform/library fallback semantics, stale caches/session tickets, unrelated network errors, certificate-generation mistakes, clock skew, fixture misconfiguration, intentionally disabled revocation, and policies that legitimately accept the observed identity.

## Registry and repository scope

Expected final scope is exactly nine paths:

1. `README.md`
2. `docs/operator-depth-contract.md`
3. this design document
4. `docs/superpowers/plans/2026-09-17-wave10-certificate-hostname-validation-depth.md`
5. `operator-depth/profiles.json`
6. `skills/certificate-and-hostname-validation-analysis/SKILL.md`
7. `skills/certificate-and-hostname-validation-analysis/references/operator-review-cases.json`
8. `skills/certificate-and-hostname-validation-analysis/references/operator-runbook.md`
9. `tests/test_certificate_hostname_validation_depth.py`

Do not modify `skill.meta.json`, graph edges, packs, routing domains, benchmark fixtures/thresholds, agent-eval authority, superiority-court authority, or workflow semantics.

## TDD and integration gates

1. Add this design document.
2. Add the implementation plan.
3. Add the dedicated test before production artifacts.
4. Open a Draft PR on the exact test-first SHA.
5. Observe RED: dedicated certificate/hostname assertions fail while pre-existing repository gates remain healthy.
6. Implement skill/runbook/review-cases/one registry entry without weakening the dedicated test.
7. Require full behavioral GREEN across six OS/Python matrix jobs plus benchmark-core, agent-eval-core, and superiority-court-core.
8. Only after behavioral GREEN, update README and operator-depth contract.
9. Require exact-head GREEN on the final SHA.
10. Fresh-check base/head/scope/mergeability, then guarded merge with the exact reviewed head SHA.
11. Require post-merge GREEN on the exact merge commit.
12. Re-read registry, README, and operator-depth contract from the merge tree and record closure provenance.

## Safety boundary

Dynamic validation is restricted to local, owned, sandboxed, benchmark, CTF, or explicitly authorized systems using synthetic certificate hierarchies, synthetic hostnames, local mock endpoints, inert canaries, policy simulation, read-only synthetic resources, or bounded reversible owner-controlled effects.

Stop before real third-party host impersonation, traffic interception outside scope, installation of test roots on non-test systems, production client-certificate use, credential capture, persistence, malware, destructive actions, evasion, or unauthorized targets.

## Claim boundary

This profile can establish repository-contract depth and deterministic conformance. It does not establish empirical superiority over external security systems without running those external systems through the same evaluation authority.