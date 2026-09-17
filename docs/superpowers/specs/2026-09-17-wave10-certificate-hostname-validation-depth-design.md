# Wave 10 Certificate And Hostname Validation Depth Design

## Status

Design for Wave 10 operator-depth profile #20, based on `main@6b8e0f36fee255a985d39aa8178598d58e1e21ad`.

Target canonical skill: `certificate-and-hostname-validation-analysis`.

This change deepens an existing canonical capability. It does not add a new skill, change routing, modify graph edges, alter benchmark authority, or expand the repository's authorization boundary.

## Problem

The canonical skill currently identifies important TLS/X.509 checks — chain validation, hostname/SAN matching, trust anchors, EKU, revocation, pinning, mTLS mapping, and callbacks — but it remains observation-oriented. It does not yet force an operator to prove which service identity was intended, which validation path was actually constructed, which trust anchor and trust-store generation authorized that path, how application callbacks modified the library decision, whether cached or resumed state belongs to the current policy generation, or which bounded result is causally attributable to the validation decision.

That gap permits several false promotions:

- a syntactically valid certificate can be mistaken for an authorized peer;
- a chain that terminates in a locally trusted root can be mistaken for a hostname-authorized service;
- a SAN match can be mistaken for complete certificate-policy acceptance;
- a library verification success can be mistaken for the application's final acceptance decision;
- a pin match can be mistaken for complete PKI identity proof, or absence of pinning can be mislabeled as a vulnerability;
- a cached verification result or resumed session can be treated as current after trust, revocation, pin, routing, or certificate generations changed;
- possession of an mTLS certificate can be confused with application-principal authorization.

Profile #20 therefore needs a causal identity-and-policy model, deterministic synthetic review cases, explicit counterfactual controls, and an evidence ceiling.

## Why this profile and why now

`certificate-and-hostname-validation-analysis` is an existing high-value canonical skill with no operator-depth profile. Its current `SKILL.md` is substantially shallower than the recent Wave 10 profiles and its core security semantics depend on identity, binding, authority, and lifecycle reasoning that are not fully covered by any of the nineteen registered profiles.

The profile is distinct from neighboring capabilities:

- `canonicalization-and-namespace-analysis` reasons about representation-to-identity normalization generally; this profile reasons about TLS reference identifiers, certificate identities, path construction, trust anchors, and endpoint authority.
- `secrets-and-token-flow-analysis` reasons about credential issuance and propagation; this profile reasons about peer certificate acceptance and certificate-to-principal mapping.
- `supply-chain-dependency-review` reasons about artifact provenance and release/deployment authority; this profile reasons about connection-time PKI trust and service identity.
- `server-side-request-boundary-analysis` reasons about server-side destination boundaries; this profile reasons about TLS peer authentication after endpoint/routing selection.
- `browser-process-boundary-analysis` reasons about browser process/object/capability boundaries; this profile remains transport/PKI specific.

## Scope

Expected final PR scope is exactly nine paths:

1. `README.md`
2. `docs/operator-depth-contract.md`
3. `docs/superpowers/specs/2026-09-17-wave10-certificate-hostname-validation-depth-design.md`
4. `docs/superpowers/plans/2026-09-17-wave10-certificate-hostname-validation-depth.md`
5. `operator-depth/profiles.json`
6. `skills/certificate-and-hostname-validation-analysis/SKILL.md`
7. `skills/certificate-and-hostname-validation-analysis/references/operator-review-cases.json`
8. `skills/certificate-and-hostname-validation-analysis/references/operator-runbook.md`
9. `tests/test_certificate_hostname_validation_depth.py`

Out of scope unless a failing existing authority proves otherwise:

- `skill.meta.json`;
- graph edges;
- packs;
- routing domains;
- benchmark fixtures or thresholds;
- agent-eval authority;
- superiority-court authority;
- CI workflow semantics;
- external superiority claims.

## Causal model

The canonical causal chain is:

`connection intent -> intended peer/service identity -> reference identifier and endpoint authority -> transport endpoint after routing/redirect/proxy selection -> TLS role/context -> presented certificate chain identity -> constructed validation path -> trust-anchor identity and trust-store generation -> signature/path validation -> certificate time state -> EKU/key-usage/policy and name-constraints state -> SAN/reference-identifier binding -> library verifier result -> application callback/override decision -> pin policy and pin generation when required -> mTLS certificate identity and principal mapping when applicable -> final accept/reject decision -> bounded synthetic connection result -> session/resumption/reuse binding -> revocation/trust-store/pin/certificate lifecycle generation`

The operator must not skip from an intermediate observation to final impact. Every transition that carries identity or policy authority must be recorded explicitly.

## Required distinctions and invariants

The skill and runbook must preserve at least these distinctions:

1. `presented chain != constructed validation path`.
2. `chain-valid != hostname-valid`.
3. `hostname/SAN match != complete certificate-policy acceptance`.
4. `trusted root presence != selected trust-anchor identity`.
5. `trust-anchor identity != trust-store generation`.
6. `certificate time validity != revocation freshness`.
7. `library verifier success != final application acceptance`.
8. `application callback allow != correct peer-identity binding`.
9. `pin match != complete PKI identity proof`.
10. `pinning absence != vulnerability` when ordinary PKI satisfies the stated requirement.
11. `transport peer != application service identity` when a legitimate proxy or tunnel terminates transport separately.
12. `mTLS certificate possession != application principal authorization`.
13. `cached verification result != current policy generation`.
14. `session resumption/reuse != automatic revalidation under a changed policy generation`.
15. `revocation status unavailable != proof of either validity or revocation`; the documented policy controls the decision.
16. `redirected/rerouted endpoint != original reference authority`; the verifier must bind the identity required by the actual protocol contract.

Core invariants:

- the reference identifier comes from the intended connection authority, not attacker-controlled certificate metadata;
- path construction and trust-anchor selection are evaluated in the pinned platform/library and trust-store generation;
- hostname/reference-identifier matching occurs against the identity contract applicable to the selected endpoint;
- application overrides cannot silently convert an untrusted identity into an accepted peer without an explicit documented policy;
- pins, if required, are scoped to the intended identity and current pin generation rather than serving as a global bypass;
- mTLS identity mapping binds the validated client certificate identity to the intended synthetic application principal before authorization consequences are inferred;
- resumed or cached state is never promoted above the evidence available for its current lifecycle generation.

## Evidence ladder

Use `PKI0` through `PKI5`.

### PKI0 — hypothesis

A possible peer-identity, chain, callback, pinning, mTLS-mapping, revocation, or lifecycle weakness is inferred from source/configuration or a model/tool report. No runtime acceptance decision has been causally demonstrated.

### PKI1 — observed

The operator has captured concrete verifier configuration, a controlled certificate property, callback path, trust-store/pin state, or final decision observation. Identity binding remains incomplete or alternative explanations remain open.

### PKI2 — correlated

A controlled synthetic certificate or policy variation correlates with an acceptance/rejection change, but the complete identity/path/policy chain or counterfactual controls are still incomplete. This is not sufficient for a validated vulnerability claim.

### PKI3 — validated causal acceptance error

The operator has demonstrated the full relevant causal chain with the intended reference identity, actual path/trust anchor, policy checks, verifier/callback behavior, final decision, bounded synthetic result, positive control, negative control, and at least one transition-specific counterfactual. Competing explanations have been bounded.

### PKI4 — lifecycle validated

PKI3 evidence is extended across a relevant lifecycle transition — such as trust-store change, pin rotation, certificate replacement, revocation state, endpoint/routing change, or session/cache generation — and the operator proves that stale state is or is not honored according to the documented policy.

### PKI5 — regression verified

A remediation is applied, the original causal oracle no longer succeeds, legitimate neighboring identities and policy cases still work, stale cache/session state converges correctly, and the same deterministic matrix verifies the fix without broadening authority or weakening other checks.

The evidence ceiling is always the highest level directly supported by the captured transitions and controls. Scanner output, certificate dumps, successful handshakes, callback logs, or a single rejected/accepted connection do not independently justify PKI3+.

## Counterfactual proof

The runbook must require safe, deterministic counterfactuals selected from the transition under test, for example:

- hold the chain constant and change only the reference hostname/SAN relationship;
- hold the hostname constant and change only the trust anchor/path;
- hold identity and chain constant and change only EKU/key usage or policy constraints;
- hold the library result constant and toggle only the application override in an owned fixture;
- hold certificate material constant and advance only the trust-store or pin generation;
- hold policy constant and compare a fresh handshake with resumed/cached state;
- hold the validated client certificate constant and change only the synthetic certificate-to-principal mapping.

A counterfactual must target one causal transition. A broad configuration change that simultaneously alters several identities or authorities is not sufficient to isolate root cause.

## Alternative explanations

Before promotion to PKI3 or above, the operator must explicitly consider applicable alternatives:

- the synthetic client connected to a different endpoint than intended;
- SNI or routing selected a different synthetic certificate;
- a configured TLS proxy legitimately terminates transport identity;
- platform/library path-building behavior selected a different intermediate or trust anchor;
- local clock skew explains time-validity behavior;
- stale session/cache state explains an apparent policy bypass;
- revocation data is intentionally unavailable under the pinned offline policy;
- a development-only root or callback is not reachable in the reviewed release configuration;
- the observed result came from application retry/fallback rather than the certificate decision under test.

## Deterministic review cases

The profile will add at least three benign synthetic cases.

### `peer-identity-chain-hostname-binding`

A local test TLS service uses a synthetic CA hierarchy and synthetic hostnames. The case proves the binding from intended reference identifier through constructed path and selected trust anchor to SAN/name-policy acceptance and final bounded result. Positive and negative controls change one identity/path property at a time.

### `callback-pin-policy-binding`

An owned mock verifier/application callback fixture records both the library decision and application override. Synthetic pin sets are versioned. The case proves whether an override or pin state changes the final decision without conflating pinning with ordinary PKI identity proof.

### `lifecycle-resumption-mtls-binding`

A local fixture models a certificate/trust/pin lifecycle generation plus resumed/cached state, and includes a synthetic mTLS identity-to-principal mapping where applicable. The case proves that stale verification/session state and certificate possession do not silently cross the current policy or principal-mapping boundary.

Every case contains the common operator-depth fields plus substantive domain-specific identity/path/policy/lifecycle fields. All effects remain inert or local.

## Runbook structure

In addition to the common required sections, the runbook will contain transition-specific sections for:

- connection intent and reference identity;
- endpoint/routing/TLS-context trace;
- presented-chain and constructed-path trace;
- trust-anchor and trust-store-generation trace;
- certificate-policy and name-binding trace;
- verifier/callback/final-decision trace;
- pin-policy and pin-generation trace;
- mTLS identity/principal-mapping trace;
- session/cache/resumption trace;
- revocation and lifecycle-generation trace;
- counterfactual controls;
- alternative explanations;
- evidence promotion and ceiling.

## Safety boundary

Validation is restricted to local or owned TLS endpoints, synthetic hostnames, synthetic certificate authorities and certificates, mock verifiers, local trust stores, inert connection sinks, read-only traces, and bounded reversible configuration in explicitly authorized environments.

Stop before any action that would require:

- impersonating a real third-party hostname or service;
- intercepting unrelated traffic;
- installing a test CA on a non-test or third-party device;
- using a production private key, client certificate, token, or credential;
- modifying public DNS, public certificate issuance, or external trust stores;
- disabling certificate validation on a production path as proof;
- persistence, evasion, credential theft, destructive behavior, or unauthorized access.

The profile demonstrates validation logic with synthetic identities. It does not teach third-party interception or certificate abuse.

## TDD contract

The dedicated test is written before production artifacts. Pre-implementation RED is valid only if:

- the four dedicated semantic groups fail for the intended missing profile artifacts/semantics;
- there are zero unexpected unittest errors;
- pre-existing canonical-skill validation, existing nineteen-profile operator-depth validation, graph/index checks, benchmark core, agent-eval core, and superiority-court core remain green before the dedicated failure.

The dedicated test freezes:

1. canonical skill causal model, distinctions, PKI0–PKI5 ladder, counterfactuals, alternatives, and evidence ceiling;
2. runbook transition-level methodology and common sections;
3. at least three substantive deterministic synthetic review cases;
4. exactly one new registry entry, `lab_only: true`, correct paths, and exact profile count 20.

The dedicated test must not be weakened after observing RED merely to accommodate an incomplete implementation.

## Integration and closure gates

1. Behavioral implementation excludes the two public documentation files.
2. Full behavioral CI must be green before public docs are changed.
3. After behavioral GREEN, update only `README.md` and `docs/operator-depth-contract.md`.
4. Prove post-GREEN delta is exactly those two docs.
5. Prove the whole PR contains exactly the expected nine paths.
6. Run full CI on the exact final candidate SHA.
7. Create no commit after exact-head GREEN.
8. Re-check current `main`, PR base/head, changed paths, mergeability, and absence of base drift immediately before merge.
9. Mark the PR ready and merge only with `expected_head_sha=<exact-final-head>`.
10. Verify merge parent 1 is the pre-merge `main` and parent 2 is the exact final PR head.
11. Require post-merge push CI to be full GREEN on the exact merge SHA.
12. Read the registry, README, and operator-depth contract on the merge SHA and record closure provenance in the PR.

## Success criteria

Profile #20 is complete only when all closure gates above are satisfied. The acceptable claim is that this repository now has deterministic internal verification for deeper certificate/hostname causal reasoning. No claim of empirical superiority over an external security system is permitted without an actual external contestant evaluated under the repository's protocol.
