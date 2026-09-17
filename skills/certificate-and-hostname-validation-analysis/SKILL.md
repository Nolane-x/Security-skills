---
name: certificate-and-hostname-validation-analysis
description: "Analyze TLS/X.509 certificate, hostname, trust-anchor, EKU, SAN, revocation, pinning, client-auth, and verification callback behavior. Use controlled certificate matrices to prove acceptance-policy errors."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Certificate And Hostname Validation Analysis

Perform dynamic validation only in an authorized, owned lab or equivalent explicitly scoped test environment. Prefer synthetic hostnames, synthetic certificate authorities, local TLS services, mock verifier callbacks, local trust stores, inert sinks, and read-only traces. Do not impersonate real third-party services, intercept unrelated traffic, install test roots on non-test devices, or use production private keys or client certificates.

## When to use

Use this skill when the security question depends on TLS/X.509 peer identity rather than merely whether encryption exists: custom verification callbacks, embedded trust stores, internal PKI, certificate pinning, redirects or alternate endpoints, TLS proxies, session resumption, revocation policy, mTLS certificate selection, and certificate-to-account mapping.

Do not treat a scanner verdict, certificate dump, or one successful handshake as proof of a vulnerability. Bind the intended peer identity to the actual validation path, application decision, and bounded result.

## Preconditions

1. Establish explicit authorization and keep dynamic endpoints local, owned, sandboxed, synthetic, or otherwise explicitly authorized.
2. Pin TLS library/platform version, verifier configuration, time source, trust-store generation, pin generation when applicable, and session/cache state.
3. Define synthetic reference identifiers before generating certificates so certificate metadata cannot define the identity it is supposed to prove.
4. Use a controlled CA/certificate hierarchy whose private keys exist only for the lab.
5. Record whether a legitimate proxy or tunnel terminates transport TLS separately from application-service identity.
6. Define stop conditions before a test could touch a third-party hostname, production key material, public CA issuance, unrelated traffic, or a non-test trust store.

## Causal certificate and peer-identity model

Use this exact default review graph:

`connection intent -> intended peer/service identity -> reference identifier and endpoint authority -> transport endpoint after routing/redirect/proxy selection -> tls role/context -> presented certificate chain identity -> constructed validation path -> trust-anchor identity and trust-store generation -> signature/path validation -> certificate time state -> eku/key-usage/policy and name-constraints state -> san/reference-identifier binding -> library verifier result -> application callback/override decision -> pin policy and pin generation when required -> mtls certificate identity and principal mapping when applicable -> final accept/reject decision -> bounded synthetic connection result -> session/resumption/reuse binding -> revocation/trust-store/pin/certificate lifecycle generation`

Every arrow can change identity, authority, policy, or lifecycle state. Evidence at one node does not prove a later node. Cryptographic validity is only one transition; the reviewed application must still prove that the validated identity is the identity intended for this connection and that the final decision came from the expected policy generation.

## Peer identity and reference binding

Start from connection intent, not the certificate. Record the intended peer/service identity, reference identifier, endpoint authority, and every routing, redirect, proxy, service-discovery, SNI, or alternate-endpoint transition before the handshake.

Preserve these distinctions:

- `chain-valid != hostname-valid`: a cryptographically valid chain can authenticate the wrong service identity.
- `hostname/SAN match != complete certificate-policy acceptance`: name matching does not establish EKU, key-usage, name-constraint, time, revocation, or application-policy suitability.
- `transport peer != application service identity`: a legitimate proxy or tunnel may terminate transport while the protocol authenticates an end service separately.
- `redirected/rerouted endpoint != original reference authority`: redirects, failover, service discovery, and proxy selection can change which identity contract applies.

The reference identifier must come from the intended connection authority, not from attacker-controlled certificate metadata. Use synthetic identities such as `api.fixture.test` and `other.fixture.test`; never prove this by impersonating a real external hostname.

## Path construction and trust-anchor authority

Capture both the presented chain and the validation path actually constructed by the pinned verifier. Record leaf identity, intermediates, path-building source, selected trust anchor, trust-store scope, and trust-store generation.

Preserve these distinctions:

- `presented chain != constructed validation path`: the verifier can use cached or local intermediates rather than only the wire chain.
- `trusted root presence != selected trust-anchor identity`: a root existing in a store does not prove that the observed path terminated there.
- `trust-anchor identity != trust-store generation`: the same anchor can participate in different scoped stores or policy generations.

Development roots, enterprise roots, bundled roots, user-added roots, and system roots can represent different authority. A debug-only root is not evidence of release exposure until release-boundary reachability is proven.

## Certificate policy and application decision

After path construction, record signature/path result, certificate time state, EKU/key usage, certificate policy/name constraints where applicable, SAN/reference-identifier matching, revocation policy, library verifier result, application callbacks/overrides, and final accept/reject decision.

Preserve these distinctions:

- `certificate time validity != revocation freshness`: NotBefore/NotAfter does not establish current revocation knowledge.
- `library verifier success != final application acceptance`: wrappers, callbacks, retries, or fallback can alter the final decision.
- `application callback allow != correct peer-identity binding`: an allow result can still be bound to the wrong reference identity or endpoint authority.
- `revocation status unavailable != proof of either validity or revocation`: interpret unavailable status only under the documented fail-open, fail-closed, soft-fail, stapling, or offline policy.

A permissive callback becomes security-relevant only when a controlled fixture proves that changing the override changes acceptance of an otherwise invalid synthetic identity.

## Pinning and mutual TLS binding

Pinning is an additional policy mechanism, not a universal requirement. State what a pin identifies, scope it to the intended synthetic service, and record the active pin generation and fallback rules.

Preserve these distinctions:

- `pin match != complete PKI identity proof`: pin material can constrain a key or certificate without independently proving every service-identity and policy condition.
- `pinning absence != vulnerability`: ordinary PKI may fully satisfy the declared requirement.
- `mTLS certificate possession != application principal authorization`: a valid client certificate still requires correct certificate-to-principal mapping and any downstream authorization decision.

For mTLS, separately capture certificate presentation, client-auth path/policy validation, validated certificate identity, application principal mapping, and the bounded operation associated with that synthetic principal.

## Session, revocation, and lifecycle reasoning

Track the generations relevant to the reviewed system: certificate/leaf, trust store, selected trust anchor, pin set, revocation information, mTLS principal mapping, TLS session/cache, and endpoint/routing state.

Preserve these distinctions:

- `cached verification result != current policy generation`: cached acceptance can outlive trust, pin, certificate, or revocation changes.
- `session resumption/reuse != automatic revalidation under a changed policy generation`: interpret resumed state according to the explicit invalidation/revalidation contract.

Test fresh and resumed/cached connections separately when the product can reuse prior decisions. A stale session is not automatically a defect; prove whether its behavior violates the documented lifecycle contract.

## Certificate identity evidence ladder

Use the repository evidence states while expressing domain depth as `PKI0` through `PKI5`.

### PKI0 — hypothesis

A possible certificate, hostname, trust, callback, pin, mTLS mapping, revocation, or lifecycle weakness is inferred from source, configuration, scanner output, or model/tool analysis. No runtime acceptance decision has been causally demonstrated.

### PKI1 — observed

Concrete configuration, certificate properties, verifier traces, callback behavior, trust/pin state, or a final decision has been observed, but identity/path/policy binding remains incomplete or alternatives remain open.

### PKI2 — correlated

Changing one controlled synthetic property correlates with an accept/reject change, but the complete causal chain, bounded result, or transition-specific counterfactual set is still incomplete. Do not call this a validated vulnerability.

### PKI3 — validated causal acceptance error

The relevant chain from intended reference identity through constructed path, selected trust anchor, certificate policy, verifier, application callback, final decision, and bounded synthetic result is captured. Positive and negative controls isolate the transition, at least one counterfactual reverses the causal condition, and applicable alternatives are bounded.

### PKI4 — lifecycle validated

PKI3 evidence is repeated across a relevant trust-store, pin, certificate, endpoint, revocation, mTLS-mapping, or session/cache lifecycle transition, proving whether stale state follows or violates the documented generation contract.

### PKI5 — regression verified

After remediation, the original invalid synthetic binding no longer reaches the bounded result, valid neighboring identities/policies still succeed, stale sessions/caches converge correctly, and the deterministic matrix verifies the fix without weakening adjacent checks.

## Counterfactual proof

Change one disputed transition while holding neighboring state constant. Useful pairs include:

- same synthetic chain and policy, different reference hostname/SAN relationship;
- same reference identity, different constructed path or trust anchor;
- same identity/path, different EKU, key usage, time, or name-constraint state;
- same library result, application override disabled versus enabled in a mock application;
- same certificate material, trust-store or pin generation advanced;
- same policy, fresh full handshake versus resumed/cached state;
- same validated synthetic client certificate, certificate-to-principal mapping changed.

If a test changes several identities or authorities at once, it cannot isolate root cause and its evidence ceiling remains below PKI3.

## Alternative explanations

Before PKI3+ promotion, explicitly evaluate applicable alternatives:

- the client reached a different local endpoint;
- SNI or routing selected another synthetic certificate;
- a configured proxy legitimately terminated transport TLS;
- platform path building selected a different local intermediate or trust anchor;
- clock skew caused time-validity behavior;
- a stale session or verifier cache reused an older decision;
- revocation data was intentionally unavailable under the pinned offline policy;
- permissive trust or callbacks were debug-only and absent from the reviewed release path;
- application retry/fallback rather than certificate acceptance produced the observed success;
- an mTLS fixture selected a different client certificate or principal mapping.

Record evidence that excludes each relevant alternative; do not merely label it unlikely.

## Workflow

1. Define connection intent, synthetic reference identity, endpoint authority, and expected decision before generating certificate fixtures.
2. Pin platform/library, time source, trust-store generation, callback configuration, pin generation, and session/cache generation.
3. Capture actual endpoint, routing, proxy, and SNI context.
4. Capture presented chain and constructed validation path independently.
5. Record selected trust-anchor identity and trust-store generation.
6. Evaluate time, EKU/key usage, policy/name constraints, SAN/reference-identifier binding, and configured revocation policy.
7. Trace library verifier result into application callback/override and final decision.
8. Evaluate pin state and mTLS identity/principal mapping only when the product contract uses them.
9. Run positive, negative, and transition-specific counterfactual controls against local or mock endpoints.
10. Bind the final decision to an inert local result or controlled canary.
11. Repeat the relevant matrix across lifecycle generations when reuse or rotation is in scope.
12. Cap the claim at the directly supported PKI evidence level.

## Evidence contract

For every decisive case, record fixture identity; library/platform and verifier configuration; intended reference identity; endpoint/SNI/proxy context; presented chain; constructed path; selected trust anchor and trust-store generation; certificate time/EKU/key-usage/policy/name-constraint/SAN state; revocation policy; library verifier result; application override; pin generation; mTLS certificate identity/principal mapping when applicable; final decision; bounded synthetic result; session/cache generation; positive and negative controls; counterfactual; alternative explanations; evidence level; and evidence ceiling.

Low-level signals never auto-promote to impact. A signature, certificate dump, scanner finding, successful handshake, callback log, or pin match is not causal proof by itself. `validated` requires bounded evidence plus controls; `regression-verified` requires a fix oracle and preservation of neighboring legitimate behavior.

## False-positive controls

At minimum distinguish wrong hostname from untrusted chain, presented root from selected trust anchor, SAN match from EKU/policy suitability, callback logging from override, normal PKI from optional pinning, client-certificate possession from principal mapping, fresh verification from stale session/cache reuse, revocation-data absence from policy violation, proxy termination from wrong-service identity, and debug-only state from release-reachable state.

If a negative control changes several transitions at once, redesign it or retain a lower evidence ceiling.

## Remediation and regression

Fix the broken binding rather than stacking unrelated checks. Examples include restoring reference-identifier verification, eliminating unsafe callback overrides, narrowing trust-store authority, correcting pin scope/rotation, repairing mTLS principal mapping, or invalidating stale sessions when the documented policy requires it.

Regression must replay the original invalid synthetic case, its valid positive neighbor, at least one negative neighbor, any lifecycle case implicated by root cause, and the transition-specific counterfactual. Valid adjacent identities must remain usable.

## Evidence ceiling

The claim may never exceed the highest transition directly supported by captured evidence and controls:

- a scanner signature or certificate dump is at most PKI1 without decision evidence;
- a successful handshake does not prove intended identity authorization;
- a controlled accept/reject correlation remains PKI2 until the relevant path/policy/final-decision chain and counterfactual are bound;
- one fresh handshake cannot establish lifecycle safety for session resumption or trust/pin/revocation rotation;
- PKI5 requires remediation proof plus legitimate-neighbor preservation.

Never promote `scanner/model/tool says suspicious` directly to `confirmed vulnerability`.

## Stop conditions

Stop or abort immediately if validation would require real third-party hostname impersonation, unrelated traffic interception, public certificate issuance for another namespace, production private keys or client certificates, modifying a non-test trust store, disabling validation on a production path, persistence, evasion, credential theft, destructive behavior, or any unauthorized system interaction.

## Output

```text
library/platform and generation:
connection intent:
intended peer/service identity:
reference identifier and endpoint authority:
routing/SNI/proxy context:
presented chain identity:
constructed validation path:
trust-anchor identity and trust-store generation:
certificate policy/name-binding state:
revocation policy/state:
library verifier result:
application callback/override:
pin policy/generation:
mTLS certificate identity/principal mapping:
final accept/reject decision:
bounded synthetic result:
session/resumption/cache generation:
counterfactual controls:
alternative explanations:
evidence level (PKI0-PKI5):
evidence ceiling:
remediation oracle:
```
