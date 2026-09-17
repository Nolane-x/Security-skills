# Wave 10 Profile #22 — Certificate And Hostname Trust Depth Design

## Status

Design authority for Wave 10 operator-depth profile #22, based on exact `main@0638eb26c8d66226afc3e856e58327f470a2b537` after closure of profile #21 (`deserialization-trust-analysis`).

Target canonical skill: `certificate-and-hostname-validation-analysis`.

This change deepens an existing canonical capability. It does not add a new skill, alter `skill.meta.json`, graph edges, packs, routing domains, benchmark authority, agent-eval authority, superiority-court authority, workflow semantics, or repository authorization policy.

## Problem

The canonical skill already inventories trust roots, hostname/SAN matching, EKU/key usage, validity, name constraints, verification callbacks, redirects, pinning, mTLS mapping, and controlled certificate matrices. It remains observation-oriented, however. It does not require a reviewer to bind the exact intended peer identity and endpoint state through path construction, trust-anchor selection, certificate policy, reference-identity normalization, callback/override state, lifecycle generations, final authenticated peer/session identity, and privileged consumer/result before evidence is promoted.

That gap permits false promotions such as:

- chain validity being treated as hostname or service-identity validity;
- a trusted root being treated as authorization for any peer identity;
- SNI, URL host, connection target, redirect target, and verification reference identity being assumed equivalent;
- SAN or CN text being treated as the canonical peer identity without recording normalization and matching policy;
- a valid signature or path being treated as satisfying EKU, name constraints, policy, pin, or application-purpose requirements;
- pin match being treated as a substitute for all other required PKI checks;
- callback reachability or a permissive callback return being treated as proof of an effective bypass without final-decision and consumer binding;
- mTLS certificate acceptance being treated as application-account authorization;
- resumed/cached sessions being treated as current after trust-store, pin, revocation, policy, certificate, endpoint, or account-mapping generations change;
- an observed connection/result being attributed to the wrong handshake because receipt/result correlation is missing.

Profile #22 therefore needs a causal peer-identity trust model, deterministic synthetic PKI controls, lifecycle-generation reasoning, counterfactual proof, explicit alternative explanations, and a strict evidence ceiling.

## Why this profile and why now

The merge tree now contains 21 CI-enforced operator-depth profiles. `certificate-and-hostname-validation-analysis` remains an existing beta canonical skill with evidence stage `observed` and no operator-depth registration.

It is materially distinct from existing profiles:

- `canonicalization-and-namespace-analysis` is generic representation-to-identity reasoning; profile #22 specializes endpoint/reference identity, certificate names, path policy, and authenticated peer/session binding.
- `secrets-and-token-flow-analysis` models credential issuance and verifier decisions; certificate credentials here are evaluated as one PKI input and do not replace peer-identity proof.
- `boot-chain-and-secure-boot-analysis` models firmware trust roots and loaded-component identity; profile #22 models network peer identity, path construction, hostname/reference identity, callback policy, and session lifecycle.
- `mobile-network-trust-analysis` is a higher-level mobile composition workflow; profile #22 is the reusable canonical PKI/TLS peer-verification authority.
- `authorization-boundary-analysis` begins after an action/resource identity is known; profile #22 establishes which remote peer/session identity is actually authenticated before downstream authorization.

## Scope

Expected final PR scope is exactly nine paths:

1. `README.md`
2. `docs/operator-depth-contract.md`
3. `docs/superpowers/specs/2026-09-17-wave10-certificate-hostname-depth-design.md`
4. `docs/superpowers/plans/2026-09-17-wave10-certificate-hostname-depth.md`
5. `operator-depth/profiles.json`
6. `skills/certificate-and-hostname-validation-analysis/SKILL.md`
7. `skills/certificate-and-hostname-validation-analysis/references/operator-review-cases.json`
8. `skills/certificate-and-hostname-validation-analysis/references/operator-runbook.md`
9. `tests/test_certificate_hostname_depth.py`

Explicitly out of scope:

- `skill.meta.json`;
- graph edges or packs;
- routing domains;
- benchmark fixtures or thresholds;
- agent-eval or superiority-court authority;
- workflow semantics;
- external superiority claims.

## Selected approach

Three approaches were considered.

### Certificate matrix expansion only

Rejected. Adding more malformed/expired/wrong-host fixtures increases breadth but does not freeze causal peer-identity reasoning.

### Active interception/bypass proof

Rejected. Real interception, third-party impersonation, stolen client credentials, or production traffic are unnecessary and violate the desired benign evidence-first boundary.

### Causal peer-identity, PKI-policy, and lifecycle depth

Selected. The profile models the handshake and application trust decision as a sequence of endpoint, reference identity, path, policy, callback, authenticated peer/session, consumer, result, and lifecycle transitions. Every material transition can be exercised using a local synthetic CA, loopback/mock TLS peers, fake identities, deterministic certificate fixtures, inert consumers, and read-only traces.

## Causal model

The canonical chain is:

`request/service intent -> original endpoint identity -> redirect/alternate-endpoint state -> transport target -> SNI state -> verification reference identity -> verifier/library identity and configuration -> trust-store identity -> trust-store generation -> presented leaf/chain identity -> path-building inputs -> selected certification path -> selected trust anchor -> chain-signature/validity constraints -> EKU/key-usage/policy/name-constraints state -> SAN/reference-name state -> canonical reference identity -> hostname/service-identity match -> pin policy and pin generation -> revocation/soft-fail policy state -> verification callback/override input -> callback decision -> final verifier/application accept-or-reject decision -> authenticated peer identity -> authenticated session identity -> mTLS peer-to-account mapping where applicable -> privileged consumer/use -> bounded result/receipt -> certificate/trust/pin/revocation/policy/session/account-mapping lifecycle generation`

Evidence must preserve every transition material to the claim. Missing endpoint, reference-identity, path, anchor, policy, callback, session, consumer, result, or lifecycle binding lowers the evidence ceiling.

## Core distinctions

The canonical skill and runbook must preserve at least these distinctions:

1. `chain-valid != hostname-valid`.
2. `trusted-root != authorized-peer`.
3. `certificate signature valid != certificate policy authorized`.
4. `SNI != verification reference identity`.
5. `URL/original host != redirect target != transport target`.
6. `SAN/CN text != canonical reference identity`.
7. `path-building success != intended trust-anchor selection`.
8. `EKU/key-usage validity != hostname/service authorization`.
9. `pin match != complete PKI validation`.
10. `revocation unavailable != revocation good`.
11. `callback invoked != callback controls the final decision`.
12. `callback accept != application/session authenticated-peer binding`.
13. `certificate accepted != mTLS account authorized`.
14. `connection success != proof of which certificate/path/reference identity was accepted`.
15. `session resumed != current trust/pin/revocation/policy generation`.
16. `certificate rotation != security-equivalent identity unless policy and generation binding prove it`.
17. `debug/test trust root behavior != production trust policy`.
18. `bounded synthetic wrong-peer acceptance != broad interception capability`.
19. `action/result success != receipt binding to the exact handshake tuple`.

## Core invariants

- Peer authorization is evaluated against the final canonical reference identity, not only a displayed or transport hostname.
- A successful chain path is accepted only if its selected anchor and all applicable certificate constraints are authorized for the intended peer purpose.
- Pinning, revocation, and callbacks are additive policy transitions unless the intended design explicitly defines otherwise; none silently substitutes for unrelated required checks.
- The final authenticated peer/session identity is derived from the exact accepted handshake tuple and bound to downstream consumers.
- mTLS application identity mapping is separate from certificate-chain acceptance and must be generation-aware.
- Cached/resumed sessions cannot inherit trust by assumption across authoritative trust/pin/revocation/policy/account-mapping changes.
- Results used as evidence are correlated to the exact handshake/session tuple before promotion.
- Remediation preserves neighboring valid peers, approved redirects/alternate endpoints, intended pin rotation, and legitimate session behavior.

## Identity and policy trace

A review records, where applicable:

- intended service/peer identity and purpose;
- original URL/endpoint, redirect target, alternate endpoint, transport target, port, and SNI;
- canonical verification reference identity and normalization rules;
- TLS/library/platform verifier identity and version/configuration;
- trust-store source, identity, and generation;
- presented leaf and chain fingerprints/identities;
- path-building inputs, candidate paths, selected path, and selected trust anchor;
- validity, basic constraints, path-length, KU/EKU, certificate policy, and name-constraint decisions;
- SAN/CN inputs and final hostname/service-identity match;
- pin policy, pinset identity, backup pins, and pin generation;
- revocation policy and observable status/soft-fail semantics;
- callback/override inputs, outputs, and whether they are authoritative;
- final verifier and application decision;
- authenticated peer identity and session identity;
- mTLS certificate-to-account/service mapping when applicable;
- downstream privileged consumer;
- bounded result/receipt identity;
- relevant certificate, trust, pin, revocation, verifier-policy, endpoint, session, and account-mapping generations.

## Evidence ladder PKI0–PKI5

### PKI0 — surface mapped

A trust store, certificate path, hostname/reference identity, pin, revocation policy, callback, mTLS mapping, or session lifecycle surface is identified. No trust-boundary failure is established.

### PKI1 — identity or policy divergence observed

A concrete endpoint/reference-name/path/anchor/policy/callback/generation difference is observed, but incorrect acceptance is not yet demonstrated.

### PKI2 — verification-policy mismatch demonstrated

A controlled synthetic fixture proves that path selection, trust-anchor authorization, certificate constraints, reference-identity matching, pin/revocation handling, callback semantics, or lifecycle decision diverges from intended policy. No wrong-peer connection effect is required.

### PKI3 — inert wrong-peer acceptance

A synthetic wrong-host, wrong-anchor, wrong-EKU/policy, stale-pin/trust generation, or otherwise unauthorized test peer is accepted through the final application verifier under conditions that should reject it. Only local synthetic peers and inert consumers are used.

### PKI4 — bounded authenticated-peer/session effect

The wrong-peer acceptance creates a bounded owner-controlled authenticated session state or exposes a read-only/inert synthetic consumer result through the exact intended application path. The effect is bound to the initiating endpoint/reference-identity/certificate/path/policy/session tuple.

### PKI5 — causal peer-trust proof

Requires PKI4 plus exact intended peer identity, endpoint/redirect/SNI state, canonical reference identity, verifier configuration, trust-store identity and generation, presented-chain identity, selected path and trust anchor, certificate-constraint decisions, hostname/service-identity match, pin/revocation/callback decisions, final authenticated peer/session identity, applicable mTLS account mapping, lifecycle-generation controls, privileged-consumer identity, receipt/result binding, at least one meaningful counterfactual, eliminated alternative explanations, and remediation regression preserving neighboring intended behavior.

The evidence ceiling is the highest directly supported level. Chain success, signature validity, certificate fingerprints, callback logs, a browser lock icon, pin match, or connection success cannot independently justify PKI3–PKI5.

## Counterfactual proof

Cases use transition-specific counterfactuals such as:

- same chain with neighboring valid versus wrong reference identity;
- same leaf/hostname with an unauthorized versus authorized trust anchor;
- same endpoint with redirect enabled versus removed while transport target is held constant;
- same certificate with EKU/policy/name-constraint difference only;
- same handshake with pin policy enabled versus disabled while normal PKI checks remain constant;
- same callback input with authoritative override removed while library verification is unchanged;
- same test peer across trust-store or pin-generation rollover;
- same certificate acceptance with mTLS account mapping changed independently;
- same session after authoritative trust/policy generation advances;
- post-remediation valid peer still accepted while the synthetic wrong peer is rejected.

A counterfactual must isolate one causal transition. Broad environment changes do not prove root cause.

## Alternative explanations

Before PKI3+ promotion, consider applicable alternatives including:

- harness connected to a different synthetic endpoint;
- DNS/hosts fixture or proxy configuration changed the target;
- SNI and verification host differed intentionally by documented design;
- test root was installed only in a debug/test store;
- library performed a different path because of cached intermediates;
- callback log was emitted but did not control final acceptance;
- pinning failure was masked by an unrelated fallback test mode;
- session resumption reused a previous valid session rather than exercising current verification;
- mTLS account mapping, not certificate verification, explains the downstream identity;
- revocation status was unavailable and policy intentionally soft-failed;
- another concurrent handshake produced the observed receipt/result;
- certificate timestamps or clock skew invalidated a control for an unrelated reason.

## Deterministic review cases

At least three benign synthetic cases are required.

### `peer-reference-identity-binding`

Proves original endpoint, redirect/transport target, SNI, canonical reference identity, SAN/CN match, selected path, and selected trust anchor remain causally bound before the peer is authenticated.

### `callback-pin-effective-decision-binding`

Proves library verification, certificate policy, pin state, revocation policy, callback/override semantics, and final application accept/reject decision are captured separately and causally related.

### `trust-policy-session-generation-binding`

Proves trust-store, pin, revocation, verifier-policy, certificate/account mapping, and resumed-session generations cannot preserve stale trust after authoritative policy changes while valid current peers still work.

Every case includes common operator-depth fields plus substantive fields for intended peer identity, endpoint state, SNI, reference identity, verifier, trust-store generation, leaf/chain identity, path/anchor, certificate constraints, SAN/name match, pin/revocation state, callback, final decision, authenticated peer/session, account mapping when applicable, consumer, result/receipt, lifecycle generation, counterfactual, alternative explanation, evidence level, and evidence ceiling.

## Runbook structure

The runbook contains common required sections:

- `Attack surface`
- `Hypothesis matrix`
- `Controlled validation`
- `False-positive controls`
- `Evidence capture`
- `Remediation checks`

It additionally contains domain sections for peer/endpoint intent, reference identity, verifier/trust-store, path/anchor, certificate constraints, SAN/name binding, pin/revocation policy, callback/override semantics, authenticated peer/session, mTLS mapping, lifecycle generations, consumer/result binding, counterfactuals, alternatives, and PKI0–PKI5 promotion.

## Safety boundary

All validation is limited to local/owned/sandboxed TLS clients and servers, loopback/mock endpoints, deterministic synthetic CAs and certificates, fake service identities, inert consumers, read-only traces, or bounded reversible owner-controlled session effects.

Stop before any proof requiring:

- impersonating real external services;
- intercepting unrelated third-party traffic;
- installing test roots on non-test devices/accounts;
- using real production client certificates or credentials;
- credential theft, phishing, persistence, malware, destructive actions, evasion, or unauthorized targets.

A debug/test verifier can explain architecture but cannot by itself promote a production claim.

## TDD contract

The dedicated test is committed before production profile artifacts. Clean RED requires four dedicated semantic groups to fail for missing profile semantics/artifacts, zero unexpected unittest errors, and pre-existing repository authorities to remain valid before the intended dedicated failures.

The test freezes four groups:

1. canonical skill causal chain, core distinctions/invariants, PKI0–PKI5 ladder, counterfactuals, alternatives, evidence ceiling, and safety boundary;
2. runbook transition methodology and required sections;
3. at least three substantive deterministic benign review cases with common and PKI-domain fields;
4. exactly one new registry entry, correct paths, `lab_only: true`, schema version 2, and profile count increasing from 21 to 22.

The test is not weakened after valid RED merely to accommodate an incomplete implementation.

## Integration and closure gates

1. Start from exact `main@0638eb26c8d66226afc3e856e58327f470a2b537`.
2. Commit design authority.
3. Commit implementation plan/provenance.
4. Commit dedicated test only.
5. Open Draft PR at exact test-first SHA and capture RED CI.
6. Accept RED only if the intended four groups fail and old gates remain valid.
7. Implement canonical skill, runbook, review cases, and exactly one registry entry without changing the dedicated test.
8. Require full behavioral CI GREEN across six OS/Python jobs plus benchmark, agent-eval, and superiority-court cores.
9. After behavioral GREEN only, update `README.md` and `docs/operator-depth-contract.md`; prove that delta is docs-only.
10. Require exact-final-head full CI GREEN.
11. Fresh-check head, base, scope, mergeability, and current `main`.
12. Merge using the exact expected final head SHA.
13. Require post-merge push CI GREEN on the exact merge SHA.
14. Read registry, README, and operator-depth contract from the merge tree.
15. Record closure provenance only then.

## Non-claim

This profile proves repository contract conformance and deeper causal peer-trust reasoning. It does not establish superiority over any external security agent, scanner, model, or framework.