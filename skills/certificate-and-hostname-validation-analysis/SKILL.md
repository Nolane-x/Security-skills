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

Use this skill when the security question depends on TLS/X.509 peer identity rather than merely whether encryption exists. Typical targets include custom verification callbacks, embedded trust stores, internal PKI, certificate pinning, redirects or alternate endpoints, TLS proxies, session resumption, revocation policy, mTLS certificate selection, and certificate-to-account mapping.

Do not use a scanner verdict, certificate dump, or one successful handshake as proof of a vulnerability. The review must bind the intended service identity to the actual verification and application decision that produced the bounded result.

## Preconditions

1. Establish explicit authorization and keep every dynamic endpoint local, owned, sandboxed, synthetic, or otherwise explicitly authorized.
2. Pin the TLS library/platform version, verifier configuration, time source, trust-store generation, pin generation when applicable, and session/cache state.
3. Define synthetic reference identifiers and certificate identities before generating test material so the certificate itself cannot define the identity it is supposed to prove.
4. Use a controlled CA/certificate hierarchy whose private keys are created only for the lab.
5. Record whether a legitimate proxy or tunnel terminates transport TLS separately from the application service identity.
6. Define stop conditions before any test could touch a third-party hostname, production key material, public CA issuance, unrelated traffic, or a non-test trust store.

## Causal certificate and peer-identity model

Use this exact causal chain as the default review graph:

`connection intent -> intended peer/service identity -> reference identifier and endpoint authority -> transport endpoint after routing/redirect/proxy selection -> TLS role/context -> presented certificate chain identity -> constructed validation path -> trust-anchor identity and trust-store generation -> signature/path validation -> certificate time state -> EKU/key-usage/policy and name-constraints state -> SAN/reference-identifier binding -> library verifier result -> application callback/override decision -> pin policy and pin generation when required -> mTLS certificate identity and principal mapping when applicable -> final accept/reject decision -> bounded synthetic connection result -> session/resumption/reuse binding -> revocation/trust-store/pin/certificate lifecycle generation`

Treat every arrow as a possible identity, authority, policy, or lifecycle transition. Evidence at one node does not prove a later node. In particular, cryptographic validity answers only part of the question: the application must still prove that the validated identity is the identity intended for this connection and that the final decision came from the expected policy generation.

### Required distinctions

Preserve these distinctions explicitly during analysis:

- `presented chain != constructed validation path`: the peer supplies certificate material, but the verifier can construct a different path using cached or local intermediates.
- `chain-valid != hostname-valid`: a cryptographically valid chain can authenticate the wrong service identity.
- `hostname/SAN match != complete certificate-policy acceptance`: name matching does not establish EKU, key-usage, name-constraint, time, revocation, or application-policy suitability.
- `trusted root presence != selected trust-anchor identity`: a root existing in a store does not prove that the observed path terminated at that root.
- `trust-anchor identity != trust-store generation`: the same root label or certificate can participate in different policy generations or scoped stores.
- `certificate time validity != revocation freshness`: being within NotBefore/NotAfter says nothing about current revocation knowledge or policy.
- `library verifier success != final application acceptance`: callbacks, wrappers, fallbacks, and application policy can alter the final decision.
- `application callback allow != correct peer-identity binding`: an allow decision can still be bound to the wrong reference identifier or endpoint authority.
- `pin match != complete PKI identity proof`: a pin can constrain key/certificate material without independently proving every required service-identity or policy condition.
- `pinning absence != vulnerability`: ordinary PKI verification can satisfy the security requirement without application pinning.
- `transport peer != application service identity`: a legitimate proxy or tunnel may terminate transport while the protocol separately authenticates the intended application service.
- `mTLS certificate possession != application principal authorization`: a valid client certificate still needs a correct certificate-to-principal mapping and authorization decision.
- `cached verification result != current policy generation`: cached acceptance can outlive trust-store, pin, certificate, or revocation changes.
- `session resumption/reuse != automatic revalidation under a changed policy generation`: resumed state must be interpreted according to the product's explicit revalidation and invalidation contract.
- `revocation status unavailable != proof of either validity or revocation`: offline or unreachable revocation data must be interpreted under the documented fail-open/fail-closed policy.
- `redirected/rerouted endpoint != original reference authority`: redirects, proxies, service discovery, and endpoint failover can change which identity contract applies.

## Peer identity and reference binding

Start from connection intent, not the certificate. Record the intended service or peer identity, the reference identifier used by the verifier, the endpoint authority that supplied that identifier, and every routing, redirect, proxy, service-discovery, SNI, or alternate-endpoint transition before the handshake.

A certificate name is evidence about what the certificate claims, not evidence that the application intended to connect to that name. For each test, answer:

1. Where did the reference identifier originate?
2. Could untrusted input replace or reinterpret it?
3. Which transport endpoint was actually reached?
4. Did SNI or equivalent context select a different synthetic certificate?
5. Is a proxy intentionally the TLS peer, or is end-service identity expected at this layer?
6. Does a redirect or failover require a new peer-identity decision?

Use synthetic identities such as `api.fixture.test` and `other.fixture.test`; never validate by impersonating a real external hostname.

## Path construction and trust-anchor authority

Capture both the presented chain and the path actually constructed by the pinned verifier. Record leaf identity, intermediates, path-building source, selected trust anchor, trust-store scope, and trust-store generation.

Do not infer the selected path from the wire chain alone. Platforms may use local intermediates, alternate paths, cached certificates, or platform-specific trust stores. A controlled matrix should vary one factor at a time: presented intermediate, local intermediate, selected root, store scope, or store generation.

Trust decisions must preserve authority boundaries. Development roots, enterprise roots, application-bundled roots, user-added roots, and system roots can represent different authority even if they are all technically trusted by one execution context. A debug-only or development-only root is not evidence of release exposure until release-boundary reachability is proven.

## Certificate policy and application decision

After path construction, record the actual policy checks that apply to the synthetic leaf and path:

- signature and path validation result;
- certificate time state under the pinned clock;
- EKU and key-usage suitability;
- certificate-policy constraints when the application depends on them;
- name-constraints state where applicable;
- SAN/reference-identifier comparison and matching rule;
- revocation policy and available freshness evidence;
- library verifier result;
- application callback, wrapper, override, retry, or fallback behavior;
- final application accept/reject decision.

A permissive callback is only security-relevant after proving that it changes the final acceptance of an otherwise invalid synthetic identity in the reviewed configuration. Conversely, a callback that logs or supplements normal validation without overriding the decision is not a bypass.

## Pinning and mutual TLS binding

Pinning is an additional policy mechanism, not a universal requirement. First state the intended pin semantics: certificate, SPKI/key, issuer, or another application-defined identity; scope it to the synthetic service identity; record the active pin generation and fallback behavior. A matching pin must not silently substitute for unrelated hostname, chain, or application requirements unless the product contract explicitly defines that model.

For mTLS, separate four facts:

1. a client certificate was presented;
2. its path and client-auth policy were validated;
3. its certificate identity was mapped to a synthetic application principal;
4. that principal was authorized for the bounded operation.

Do not promote possession of a certificate to principal authorization. Record ambiguous or many-to-one mappings, normalization rules, lifecycle changes, and revocation separately.

## Session, revocation, and lifecycle reasoning

Certificate validation is generation-sensitive. Track at least the generations relevant to the reviewed system:

- certificate/leaf generation;
- trust-store generation;
- selected trust-anchor identity;
- pin generation;
- revocation-information generation or freshness window;
- mTLS principal-mapping generation;
- TLS session/resumption/cache generation;
- endpoint/routing generation when service discovery or failover can change peers.

Test fresh and resumed/cached connections separately when the product can reuse prior decisions. A stale session is not automatically a defect; compare behavior with the documented invalidation contract. A revocation lookup failure is likewise not automatically a defect; prove whether the configured policy is fail-open, fail-closed, soft-fail, stapling-dependent, offline, or otherwise bounded.

When a policy generation changes, record which caches or sessions should be invalidated, which are intentionally grandfathered, and when a new full verification becomes mandatory.

## Certificate identity evidence ladder

Use the repository evidence state machine while expressing domain depth as `PKI0` through `PKI5`.

### PKI0 — hypothesis

A possible certificate, hostname, trust, callback, pin, mTLS mapping, revocation, or lifecycle weakness is inferred from source, configuration, scanner output, or model/tool analysis. No runtime acceptance decision has been causally demonstrated.

### PKI1 — observed

Concrete configuration, certificate properties, verifier traces, callback behavior, trust/pin state, or a final decision has been observed in a controlled environment, but identity/path/policy binding is incomplete or alternative explanations remain open.

### PKI2 — correlated

Changing one controlled synthetic certificate or policy property correlates with an acceptance/rejection change, but the complete causal chain, bounded result, or transition-specific counterfactual set is still incomplete. Do not call this a validated vulnerability.

### PKI3 — validated causal acceptance error

The relevant chain from intended reference identity through actual constructed path, trust anchor, certificate policy, library verifier, application callback, final decision, and bounded synthetic result is captured. Positive and negative controls isolate the transition, at least one counterfactual reverses the causal condition, and applicable alternative explanations are bounded.

### PKI4 — lifecycle validated

PKI3 evidence is repeated across a relevant trust-store, pin, certificate, endpoint, revocation, mTLS-mapping, or session/cache lifecycle transition. The review proves whether stale state is accepted or invalidated according to the documented policy generation.

### PKI5 — regression verified

After remediation, the original invalid synthetic binding no longer reaches the bounded result, valid neighboring identities/policies still succeed, stale sessions or caches converge correctly, and the same deterministic matrix verifies the fix without weakening adjacent checks.

## Counterfactual proof

A useful counterfactual changes one causal transition while holding neighboring state constant. Prefer deterministic pairs such as:

- same synthetic chain and policy, different reference hostname/SAN relationship;
- same reference identity, different constructed path or trust anchor;
- same identity/path, different EKU, key usage, time, or name-constraint state;
- same library verification result, application override disabled versus enabled in a mock application;
- same certificate material, trust-store or pin generation advanced;
- same policy, fresh full handshake versus resumed/cached state;
- same validated synthetic client certificate, certificate-to-principal mapping changed.

If a test changes multiple identities or policies at once, it cannot isolate which transition caused the result and its evidence ceiling stays below PKI3.

## Alternative explanations

Before promotion to PKI3 or above, explicitly evaluate applicable alternatives:

- the client reached a different local endpoint than intended;
- SNI or routing selected a different synthetic certificate;
- a configured proxy legitimately terminated transport TLS;
- platform path building selected a different local intermediate or trust anchor;
- local clock skew caused the time-validity result;
- a stale TLS session or verifier cache reused an earlier decision;
- revocation data was intentionally unavailable under the pinned offline policy;
- a permissive root or callback was debug-only and not reachable in the reviewed release configuration;
- application retry or fallback, rather than certificate acceptance, produced the observed success;
- a synthetic mTLS identity mapped to a different principal than the operator assumed.

Record the evidence that excludes each relevant explanation; do not merely label it unlikely.

## Evidence ceiling

The claim may never exceed the highest transition directly supported by captured evidence and controls. In particular:

- a certificate dump or scanner signature is at most PKI1 without decision evidence;
- a successful handshake alone does not prove the intended identity was authorized;
- a failed hostname control plus a successful valid-hostname control can establish correlation, but PKI3 additionally requires the relevant path/policy/final-decision chain and bounded consequence;
- a single full handshake cannot establish lifecycle safety for session resumption or trust/pin/revocation rotation;
- PKI5 requires a remediation oracle and preservation of legitimate neighboring behavior.

Use the repository state labels `hypothesis`, `observed`, `validated`, and `regression-verified` consistently with the PKI ladder. Never promote `scanner/model/tool says suspicious` directly to `confirmed vulnerability`.

## Controlled validation workflow

1. Define connection intent, synthetic reference identity, endpoint authority, and expected decision before generating certificates.
2. Pin library/platform, trust store, time source, callback configuration, pin generation, and session/cache generation.
3. Capture the actual endpoint/SNI/routing context.
4. Capture presented chain and constructed validation path independently.
5. Record selected trust anchor and trust-store generation.
6. Evaluate time, EKU/key usage, policy/name constraints, SAN/reference-identifier binding, and configured revocation policy.
7. Trace the library verifier result into application callbacks/overrides and the final decision.
8. Evaluate pin state and mTLS identity/principal mapping only if the product contract uses them.
9. Run positive, negative, and transition-specific counterfactual controls against local or mock endpoints.
10. Record the bounded inert connection result and bind it to the decision trace.
11. Repeat the relevant matrix across lifecycle generations when session/resumption/cache or trust/pin/revocation changes are in scope.
12. Cap the claim at the supported PKI evidence level.

## False-positive controls

At minimum distinguish:

- wrong hostname from untrusted chain;
- presented root from selected trust anchor;
- callback logging from callback override;
- legitimate proxy termination from lost end-service identity;
- absent pinning from failed normal PKI validation;
- certificate possession from mTLS principal mapping;
- current-policy verification from stale session/cache reuse;
- revocation-data absence from an actual revocation-policy violation;
- development-only trust configuration from release-reachable behavior.

If the negative control does not differ from the positive control only at the intended transition, redesign the fixture before promoting evidence.

## Remediation and regression

Prefer fixes that restore the broken binding rather than stacking unrelated checks. Examples include restoring reference-identifier validation, eliminating unsafe callback overrides, narrowing trust-store scope, correcting pin generation/fallback logic, repairing mTLS principal mapping, or invalidating stale sessions when the documented policy requires it.

Regression verification must replay the original invalid synthetic case, its positive neighbor, at least one negative neighbor, and any lifecycle case implicated by the root cause. Record whether valid adjacent identities still work and whether stale cache/session state converges to the corrected generation.

## Stop conditions

Stop or abort immediately if validation would require real third-party hostname impersonation, unrelated traffic interception, public certificate issuance for someone else's namespace, production private keys or client certificates, modifying a non-test trust store, disabling certificate validation on a production path, persistence, evasion, credential theft, destructive behavior, or any unauthorized system interaction.

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
