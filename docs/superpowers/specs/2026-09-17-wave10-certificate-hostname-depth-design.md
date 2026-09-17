# Wave 10 Profile #21 — Certificate And Hostname Validation Depth Design

## Status

Design authority for Wave 10 operator-depth profile #21. This deepens the existing canonical `certificate-and-hostname-validation-analysis` skill without changing `skill.meta.json`, graph edges, packs, routing domains, benchmark authority, agent-eval authority, superiority-court authority, or CI workflow semantics.

Base authority: `main@e4979d27272ea059464b9285b5e452643b8f36f1`.

## Goal

Turn certificate/hostname review from a certificate-matrix checklist into a causal proof of **which application-intended peer identity was verified, under which active trust/policy generation, through which chain/path and name/usage constraints, with which pin/revocation/application-override semantics, and which final peer/principal the established session was actually bound to**.

The profile must prevent overclaims such as treating `certificate verify OK`, chain validity, root presence, SAN presence, SNI, pin match, revocation configuration, client-certificate acceptance, or connection success as equivalent to a correctly authenticated application peer.

## Selected approach

Candidate gaps considered after profile #20:

1. `firmware-update-trust-chain-analysis` — high value but materially overlaps supply-chain #18 and boot-chain #20 around signer/artifact/generation/activation semantics.
2. `nonce-and-randomness-lifecycle-analysis` — strong lifecycle value, but its deepest semantics are generator state, scope, and uniqueness/unpredictability rather than authority binding.
3. `certificate-and-hostname-validation-analysis` — selected because it closes a distinct composite identity/authority gap spanning reference identity, X.509 path authority, name constraints, usage, policy generation, application callbacks, pin/revocation lifecycle, mTLS mapping, and final established-peer binding.

## Causal model

The canonical reasoning chain is:

```text
application-intended peer/service identity
-> reference identity and normalized verification name
-> connection route/redirect/proxy target and TLS SNI context
-> active trust-store and verification-policy generation
-> candidate leaf/intermediate/root certificate identities
-> chain/path-building result and selected trust anchor
-> signature, validity-time, basic-constraints, path-length, and name-constraints decisions
-> SAN/reference-name match decision
-> EKU/key-usage/service-role decision
-> revocation policy/state generation and result
-> pin policy/set generation and result
-> library verification result
-> application callback/override/fallback decision
-> final accepted server-certificate identity
-> established session peer/service identity
-> request/consumer binding and bounded synthetic result
-> receipt/log/correlation binding
-> lifecycle rotation/revocation/pin/trust-store generation
```

For mTLS/server-side review, add:

```text
presented client-certificate identity
-> client trust/path/usage decision
-> certificate-to-principal mapping
-> mapped principal/tenant/account identity
-> authorization consumer
```

Every evidence promotion must preserve the identity and authority transitions material to the claim.

## Core invariants and distinctions

The canonical skill and runbook must encode at least these distinctions:

- chain/path validity != hostname/reference-identity validity;
- root present in a trust store != selected path anchored to the intended active root generation;
- certificate signature validity != certificate authorization for the intended peer/service role;
- SAN presence != match to the application-intended reference identity;
- SNI value != hostname-verification reference identity by assumption;
- DNS resolution/connection target != authenticated service identity by assumption;
- redirect/proxy target identity != original service identity unless policy explicitly binds them;
- EKU/key-usage validity != hostname or principal authorization;
- pin match != complete PKI/name validation unless the explicit application policy says so;
- pin configured != active pin generation actually consulted;
- revocation configuration != revocation enforcement/result;
- OCSP/CRL presence != freshness or authoritative revocation decision;
- library verification success != final application accept decision;
- application callback invocation != safe callback behavior;
- connection success != proof of intended peer identity;
- accepted client certificate != correctly mapped application principal;
- certificate subject/CN != authoritative hostname when SAN/name policy says otherwise;
- wildcard syntax acceptance != correct label/IDNA/reference-name semantics;
- trust-store update/rotation != immediate invalidation of stale sessions, caches, callbacks, or pins.

## Identity and authority model

A review must record where applicable:

- application-intended service identity;
- original reference name and normalized verification name;
- route/redirect/proxy target identity;
- TLS SNI identity;
- trust-store identifier and generation;
- verification-policy generation;
- leaf/intermediate/root certificate identities/fingerprints;
- selected path and trust-anchor identity;
- SAN set and matched SAN/reference rule;
- EKU/key-usage/name-constraints decisions;
- validation-time identity/source;
- revocation source/status/freshness/policy generation;
- pin-set identity and generation;
- library verifier result;
- application callback/override decision;
- final accepted server-certificate identity;
- established session peer identity;
- mTLS client-certificate identity and mapped principal when applicable;
- bounded result/receipt correlation;
- rotation/revocation/trust/pin lifecycle generation.

Use only synthetic CAs/certificates, local TLS endpoints, mock verifiers/callbacks, and inert identities.

## Reference identity and route reasoning

The security claim starts from the application's intended service identity, not merely the socket destination. Trace how a URL/service name becomes the hostname/reference identity given to verification, how redirects/proxies/SNI affect that tuple, and whether canonicalization/IDNA/wildcard handling is performed by the correct authority.

This profile may consume canonicalization results, but it is not a duplicate of `canonicalization-and-namespace-analysis`: the focus is the **cryptographic peer-identity decision and its binding to the final accepted TLS/mTLS session**.

## Path-building and trust-anchor reasoning

Record the actual path selected by the verifier, not just certificates presented by the peer. Synthetic matrices should distinguish:

- alternate intermediate paths;
- multiple roots/trust stores;
- stale vs current trust generations;
- cross-signing or alternative anchors where the library supports them;
- basic constraints/path-length/name constraints;
- validation time.

A root existing on disk proves neither that the active verifier loaded it nor that the selected chain terminated there.

## Name, usage, and service-role reasoning

Trace the exact reference identity, SAN candidate, wildcard/IDNA rule, EKU/key usage, and application service role used in the decision. Keep chain validation, name validation, and role/usage validation separate in evidence even if one library API returns a combined status.

## Pinning and revocation lifecycle

Treat pins and revocation as generation-aware policy systems:

- current/stale pin-set generation;
- backup/rotation pins;
- fallback behavior;
- trust-store changes relative to pins;
- CRL/OCSP/synthetic revocation source and freshness;
- hard-fail/soft-fail policy;
- cached status/session behavior;
- certificate/key rotation.

A missing or unavailable revocation signal is not automatically the same as an explicit good or revoked decision. Document policy and observable decision semantics.

## Application callback and final-decision binding

Trace library verification result into custom callbacks, exception handlers, compatibility fallbacks, debug/development overrides, retry logic, and the final connection decision. Record whether an application callback replaces, augments, or ignores parts of standard verification.

A library rejection followed by an application override must be represented as two distinct transitions. A library success is not final proof if later code changes endpoint/session binding.

## mTLS certificate-to-principal mapping

For server-side mTLS, distinguish cryptographic certificate acceptance from application identity mapping. Trace SAN/subject/extension or synthetic mapping fields into the exact account/tenant/principal consumed by authorization. A trusted client certificate does not automatically establish the intended application principal.

## Evidence ladder PKI0–PKI5

### PKI0 — surface mapped

Reference identities, routes/SNI, trust sources, path builder, name/usage checks, revocation/pin policy, callbacks, and principal mappings are mapped. No peer-identity failure is established.

### PKI1 — identity/policy divergence observed

A normalized reference name, selected path/anchor, trust/pin/revocation generation, callback result, session peer, or mTLS principal differs from expectation without yet proving wrongful acceptance.

### PKI2 — deterministic verification-policy mismatch

A controlled synthetic matrix demonstrates that chain/path, name, usage, pin, revocation, callback, or principal-mapping behavior differs from the intended policy. No accepted session effect is required.

### PKI3 — inert wrong-peer/principal acceptance

A synthetic server/client certificate tuple that should be rejected is accepted to an inert TLS/mTLS decision boundary under the wrong identity/authority/policy tuple.

### PKI4 — bounded synthetic session effect

PKI3 establishes a local reversible TLS/mTLS session or inert request/authorization marker through the exact wrong-peer/principal path. No third-party interception or production identity is involved.

### PKI5 — causal peer-identity proof

PKI4 plus exact application-intent/reference-name provenance, route/SNI context, selected path/trust-anchor and policy generation, SAN/name and EKU/usage decisions, relevant pin/revocation generation, library-to-application final decision, session-peer/principal binding, result correlation, meaningful counterfactuals, eliminated alternatives, and remediation regression preserving legitimate neighboring behavior.

No evidence may be promoted to PKI4/PKI5 solely from a verifier string, certificate dump, root-store listing, SAN presence, pin match, revocation setting, callback registration, handshake success, or connection failure.

## Counterfactual controls

Useful deterministic controls include:

- same certificate chain, intended reference name changed to matching vs non-matching synthetic hostname;
- same leaf certificate, current vs stale trust-store generation;
- same cryptographically valid chain, selected anchor/policy generation changed;
- same reference name, SAN exact-match vs neighboring/wildcard/IDNA synthetic identity;
- same chain/name, serverAuth EKU present vs absent/wrong synthetic role;
- same certificate, current vs stale pin-set generation;
- same chain/name, synthetic revocation status fresh-good vs revoked vs unavailable under explicit soft/hard-fail policy;
- same library result with safe callback behavior vs an intentionally permissive synthetic callback fixture;
- same verified server certificate under direct route vs redirect/proxy/SNI identity mismatch;
- same accepted synthetic client certificate mapped to intended vs neighboring mock principal;
- post-remediation intended peer/principal still succeeds.

## Alternative explanations

Eliminate where relevant:

- test hitting a different local endpoint;
- stale connection/session resumption;
- stale DNS/route/redirect/proxy fixture;
- trust-store or pin cache from a previous generation;
- validation time mismatch;
- expected development/debug root or callback;
- platform-specific hostname-verifier behavior;
- callback not actually installed on the exercised code path;
- certificate chain different from fixture expectation;
- expected soft-fail revocation policy;
- mTLS mapping based on a different certificate field;
- telemetry/receipt from a prior session.

## Deterministic review cases

`skills/certificate-and-hostname-validation-analysis/references/operator-review-cases.json` must contain at least:

1. `reference-name-chain-policy-binding` — proves application intent/reference name, selected trust path/anchor generation, SAN/name and EKU decisions, final callback decision, and session-peer binding.
2. `pin-revocation-generation-binding` — proves active pin-set/revocation policy generation, freshness/decision semantics, and stale-generation invalidation without confusing signal availability with status.
3. `mtls-certificate-principal-binding` — proves accepted synthetic client-certificate identity maps to the intended mock principal/tenant and that neighboring trusted certificates do not inherit that identity.

All cases are local/synthetic and non-destructive.

## Machine-readable case contract

Required common fields:

- `id`
- `hypothesis`
- `safe_oracle`
- `positive_control`
- `negative_control`
- `stop_condition`
- `remediation_oracle`

Required domain-specific fields:

- `intended_service_identity`
- `reference_identity`
- `normalized_verification_name`
- `route_redirect_proxy_identity`
- `sni_identity`
- `trust_store_generation`
- `verification_policy_generation`
- `leaf_certificate_identity`
- `chain_path_identity`
- `selected_trust_anchor_identity`
- `san_name_decision`
- `eku_key_usage_decision`
- `validation_time_identity`
- `revocation_policy_generation`
- `revocation_status_freshness`
- `pin_set_generation`
- `library_verification_result`
- `application_callback_decision`
- `final_accepted_certificate_identity`
- `established_session_peer_identity`
- `client_certificate_identity`
- `mapped_principal_identity`
- `bounded_session_result`
- `receipt_correlation_binding`
- `lifecycle_generation`
- `counterfactual_control`
- `alternative_explanation`
- `evidence_level`
- `evidence_ceiling`

All textual fields must be substantive, not placeholders.

## Runbook sections

Required common and domain-specific sections:

- Attack surface
- Hypothesis matrix
- Application intent and reference-identity trace
- Route, redirect, proxy, and SNI trace
- Trust-store and verification-policy generation trace
- Chain/path-building and trust-anchor trace
- SAN, hostname, wildcard, and IDNA decision trace
- EKU, key-usage, and service-role trace
- Pinning generation trace
- Revocation policy, status, and freshness trace
- Library verifier and application-callback trace
- Established-session peer binding trace
- mTLS certificate-to-principal mapping trace
- Lifecycle/rotation/revocation generation trace
- Controlled validation
- False-positive controls
- Counterfactual controls
- Alternative explanations
- Evidence capture
- Evidence promotion and ceiling
- Remediation checks

## Safety boundary

Validation is limited to local/owned TLS endpoints, synthetic CA hierarchies, synthetic server/client certificates, test-only trust stores and pins, mock revocation responders/status fixtures, local redirect/proxy fixtures, mock callbacks, and inert principal/authorization sinks.

Do not impersonate real third-party services, intercept unrelated traffic, install test roots on non-test devices, obtain/use production private keys or client certificates, alter public DNS, poison trust stores, weaken production TLS policy, perform credential capture, or test unauthorized systems.

## Registry and TDD contract

Add exactly one profile registration for `certificate-and-hostname-validation-analysis` to `operator-depth/profiles.json` with:

- `references/operator-runbook.md`
- `references/operator-review-cases.json`
- `lab_only: true`
- the unchanged six common required runbook sections.

Registry schema remains version 2.

Add `tests/test_certificate_hostname_depth.py` with exactly four high-level semantic test groups:

1. canonical skill causal model/distinctions/PKI0–PKI5/counterfactual/evidence ceiling;
2. operator runbook sections and transition-level semantics;
3. deterministic review-case schema, three required IDs, substantive fields, benign controls, stop/remediation oracles;
4. exactly one additive twenty-first registry registration.

Commit and observe a clean RED before production behavior is added. Do not weaken the dedicated test after a valid RED.

## Exact scope

The final PR must change exactly nine paths:

1. `README.md`
2. `docs/operator-depth-contract.md`
3. `docs/superpowers/plans/2026-09-17-wave10-certificate-hostname-depth.md`
4. `docs/superpowers/specs/2026-09-17-wave10-certificate-hostname-depth-design.md`
5. `operator-depth/profiles.json`
6. `skills/certificate-and-hostname-validation-analysis/SKILL.md`
7. `skills/certificate-and-hostname-validation-analysis/references/operator-review-cases.json`
8. `skills/certificate-and-hostname-validation-analysis/references/operator-runbook.md`
9. `tests/test_certificate_hostname_depth.py`

Out of scope: `skill.meta.json`, graph edges, packs, routing domains, benchmark fixtures/thresholds, agent-eval authority, superiority-court authority, workflow semantics, and external-vendor superiority claims.

## Integration gates

Use the proven Wave 10 lineage:

1. exact isolated branch from current main;
2. design commit;
3. implementation plan commit;
4. dedicated test-only commit;
5. Draft PR on exact test-first SHA;
6. clean RED with old gates healthy;
7. behavioral implementation without changing test;
8. full six-platform matrix + benchmark-core + agent-eval-core + superiority-court-core GREEN;
9. only then update README and operator-depth contract;
10. prove post-GREEN delta exactly two docs and total PR scope exactly nine paths;
11. exact-head full GREEN with no later commit;
12. fresh head/base/scope/mergeability/no-drift check;
13. merge only the exact reviewed final head;
14. verify two-parent merge topology and post-merge push CI full GREEN;
15. read registry/README/operator-depth contract directly from merge SHA;
16. write closure provenance comment;
17. only then declare profile #21 complete.

## Non-goals

This profile does not provide certificate impersonation instructions, third-party interception workflows, public-trust abuse, private-key theft, or a general claim that pinning/revocation is mandatory in every application. It establishes whether the implementation conforms to its documented peer-identity policy under controlled evidence.