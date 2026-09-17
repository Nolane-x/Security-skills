---
name: certificate-and-hostname-validation-analysis
description: "Analyze TLS/X.509 certificate, hostname, trust-anchor, EKU, SAN, revocation, pinning, client-auth, and verification callback behavior. Use controlled certificate matrices to prove acceptance-policy errors."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Certificate And Hostname Validation Analysis

Perform dynamic validation only in a local/owned/sandboxed lab, benchmark, or other explicitly authorized environment. Use synthetic CA hierarchies, fake service identities, loopback/mock peers, inert consumers, read-only traces, and bounded reversible owner-controlled session effects. Do not impersonate real external services, intercept unrelated traffic, install test roots on non-test devices, or use production client credentials.

## When to use

Use for TLS clients or servers with custom certificate callbacks, embedded trust stores, pinning, internal PKI, mTLS, certificate selection, redirects or alternate endpoints, session resumption, or application-specific endpoint identity checks.

## Preconditions

1. Define the intended peer/service identity and purpose before testing.
2. Use a controlled CA/certificate hierarchy and test endpoint.
3. Pin TLS/library/platform version, verifier configuration, trust-store source, and relevant policy generations.
4. Keep all effects synthetic, inert, read-only, or bounded and reversible.

## Causal peer-trust model

Treat peer verification as an identity-and-policy transition chain rather than a certificate checklist:

`request/service intent -> original endpoint identity -> redirect/alternate-endpoint state -> transport target -> SNI state -> verification reference identity -> verifier/library identity and configuration -> trust-store identity -> trust-store generation -> presented leaf/chain identity -> path-building inputs -> selected certification path -> selected trust anchor -> chain-signature/validity constraints -> EKU/key-usage/policy/name-constraints state -> SAN/reference-name state -> canonical reference identity -> hostname/service-identity match -> pin policy and pin generation -> revocation/soft-fail policy state -> verification callback/override input -> callback decision -> final verifier/application accept-or-reject decision -> authenticated peer identity -> authenticated session identity -> mTLS peer-to-account mapping where applicable -> privileged consumer/use -> bounded result/receipt -> certificate/trust/pin/revocation/policy/session/account-mapping lifecycle generation`

A claim can rise only as high as the weakest material transition that is actually captured. A certificate fingerprint, a library success code, a callback log, or a successful connection cannot replace missing identity, policy, session, consumer, or lifecycle proof.

## Endpoint and reference-identity binding

Record the service intent, original URL/endpoint, redirect target, alternate endpoint, transport target, port, SNI value, and the exact verification reference identity used by the verifier. Normalize and record the final canonical reference identity before matching certificate names.

Preserve these distinctions:

- `SNI != verification reference identity`.
- `URL/original host != redirect target != transport target`.
- `SAN/CN text != canonical reference identity`.
- A redirect or alternate endpoint changes the hypothesis unless policy explicitly binds the new target to the same intended service identity.

## Certification path and trust-anchor binding

Capture the presented leaf and intermediates, path-building inputs, candidate or observable path state, selected certification path, selected trust anchor, trust-store identity, and trust-store generation.

Preserve these distinctions:

- `chain-valid != hostname-valid`.
- `trusted-root != authorized-peer`.
- `path-building success != intended trust-anchor selection`.
- Cached intermediates or alternate path construction can change which root/policy actually authorized the peer and must be treated as a separate causal variable.

## Certificate constraints and peer authorization

Record validity interval, signature/path status, basic constraints, path length where applicable, key usage, EKU, certificate policies, name constraints, SAN/reference-name state, and hostname/service-identity decision.

Preserve these distinctions:

- `certificate signature valid != certificate policy authorized`.
- `EKU/key-usage validity != hostname/service authorization`.
- A path may be cryptographically valid while failing the intended service purpose, identity, policy, or name constraints.

## Pinning, revocation, and callback semantics

Model pinning, revocation, and application callbacks as separate policy transitions. Record pinset identity, backup/rotation state, pin generation, revocation policy, observable status, soft-fail semantics, callback input, callback output, and whether the callback is actually authoritative for the final application decision.

Preserve these distinctions:

- `pin match != complete PKI validation`.
- `revocation unavailable != revocation good`.
- `callback invoked != callback controls the final decision`.
- `callback accept != application/session authenticated-peer binding`.
- A debug-only callback or test root may explain architecture but does not establish production acceptance.

## Authenticated peer, session, and mTLS mapping

After the final verifier/application decision, record the authenticated peer identity and authenticated session identity that downstream code actually consumes. For mTLS, keep certificate acceptance separate from application account/service mapping and authorization.

Preserve these distinctions:

- `certificate accepted != mTLS account authorized`.
- `connection success != proof of which certificate/path/reference identity was accepted`.
- A connection or request result must be bound back to the exact handshake/session tuple before evidence promotion.

## Lifecycle and generation reasoning

Track relevant generations for certificate rotation, trust-store updates, root removal/addition, pinset rotation, revocation cache/policy, verifier configuration, endpoint policy, mTLS certificate-to-account mapping, session tickets/caches, and resumed sessions.

Preserve this distinction:

- `session resumed != current trust/pin/revocation/policy generation`.

A resumed or cached session cannot inherit trust by assumption after an authoritative generation changes. Re-run the intended control path or capture explicit platform semantics proving which generation governs the resumed session.

## Workflow

1. Define intended service/peer identity and trust policy.
2. Capture endpoint, redirect, transport, SNI, and canonical reference-identity state.
3. Record verifier/library configuration and trust-store identity/generation.
4. Capture presented chain, selected path, selected trust anchor, and certificate-constraint decisions.
5. Record SAN/reference-name and final hostname/service-identity match.
6. Record pin, revocation, callback/override, and final application decision independently.
7. Bind accepted state to authenticated peer/session identity and any mTLS account mapping.
8. Use controlled positive and negative peers to isolate one transition at a time.
9. Bind bounded result/receipt evidence to the exact handshake tuple.
10. Re-run remediation with neighboring intended behavior preserved.

## Certificate and hostname evidence ladder

### PKI0 — surface mapped

A trust store, certificate path, reference identity, pin, revocation policy, callback, mTLS mapping, or session-lifecycle surface is identified. No incorrect trust decision is established.

### PKI1 — identity or policy divergence observed

A concrete endpoint/reference-name/path/anchor/policy/callback/generation divergence is observed, but incorrect acceptance is not yet demonstrated.

### PKI2 — verification-policy mismatch demonstrated

A controlled synthetic fixture proves that path selection, trust-anchor authorization, certificate constraints, reference-identity matching, pin/revocation handling, callback semantics, or lifecycle decision diverges from intended policy. No wrong-peer effect is required.

### PKI3 — inert wrong-peer acceptance

A synthetic wrong-host, wrong-anchor, wrong-EKU/policy, stale-pin/trust generation, or otherwise unauthorized local test peer is accepted by the final application verifier under conditions that should reject it. The consumer remains inert or read-only.

### PKI4 — bounded authenticated-peer/session effect

The PKI3 mismatch creates a bounded reversible owner-controlled authenticated session state or exposes a read-only/inert synthetic consumer result through the intended application path. This is `bounded synthetic wrong-peer acceptance != broad interception capability`. The result must be correlated to the initiating endpoint/reference-identity/certificate/path/policy/session tuple.

### PKI5 — causal peer-trust proof

Requires PKI4 plus exact intended peer identity, endpoint/redirect/SNI state, canonical reference identity, verifier configuration, trust-store identity and generation, presented-chain identity, selected path and selected trust anchor, certificate-constraint decisions, hostname/service-identity match, pin/revocation/callback decisions, final authenticated peer identity, authenticated session identity, applicable mTLS account mapping, lifecycle-generation controls, privileged consumer identity, receipt/result binding, a meaningful counterfactual, eliminated alternative explanations, and remediation regression preserving neighboring intended behavior.

## Counterfactual proof

Change one causal transition at a time while holding the rest constant. Useful counterfactuals include the same chain with a neighboring valid versus wrong reference identity; the same leaf under an authorized versus unauthorized trust anchor; the same endpoint with redirect state changed while the transport target remains pinned; the same certificate with EKU/policy/name-constraint state changed; the same handshake with pin policy enabled versus disabled while normal PKI validation is unchanged; the same callback input with the override removed; the same peer across trust-store or pin-generation rollover; or the same resumed session after authoritative policy generation changes.

A broad environment change that alters several identities or policies at once cannot establish root cause.

## Alternative explanations

Before PKI3 or higher, consider and eliminate applicable alternative explanations: the harness connected to a different synthetic endpoint; DNS/hosts or proxy state changed the target; SNI and verification reference identity intentionally differ by documented design; a test root exists only in a debug-only store; cached intermediates selected a different path; a callback log was emitted but did not control the final application decision; pin failure was masked by test fallback; session resumption reused a previous valid session; mTLS account mapping rather than certificate verification explains downstream identity; revocation was unavailable and intentionally soft-failed; clock skew broke a control; or another concurrent handshake produced the observed receipt.

## Evidence ceiling

The evidence ceiling is the highest PKI0–PKI5 level directly supported by captured transitions and controls. Chain success, signature validity, a certificate fingerprint, lock icon, pin match, callback reachability, or connection success cannot skip missing causal bindings. `action/result success != receipt binding` to the exact handshake tuple, so uncorrelated results remain below causal proof.

## Evidence contract

Record environment and verifier version, intended peer identity, endpoint/SNI/reference identity, trust-store generation, presented chain, selected path/anchor, certificate constraints, SAN/name decision, pin/revocation/callback state, final application decision, authenticated peer/session identity, lifecycle generations, positive and negative controls, counterfactual, bounded result/receipt, evidence level, and evidence ceiling.

## Stop conditions

Stop before impersonating real external hosts, intercepting unrelated traffic, installing test roots on non-test devices, using production client certificates or real credentials, or escalating from a bounded synthetic result to persistence, malware, destructive action, evasion, credential theft, or unauthorized testing.

## Remediation guidance

Prefer fixes that restore the intended binding at the earliest incorrect transition: canonical reference identity, trust-store/anchor policy, certificate constraints, pin/revocation handling, callback semantics, mTLS mapping, or lifecycle invalidation. Verify that the synthetic wrong peer is rejected while neighboring valid peers, approved redirects/alternate endpoints, intended pin rotation, and legitimate session behavior still work.

## Output

```text
intended peer/service identity:
endpoint / redirect / transport / SNI:
canonical reference identity:
verifier + trust-store identity/generation:
presented chain + selected path/anchor:
certificate constraints + SAN/name decision:
pin/revocation/callback decisions:
final application decision:
authenticated peer/session identity:
mtls account mapping if applicable:
lifecycle generations:
positive/negative/counterfactual controls:
bounded result + receipt binding:
evidence level / evidence ceiling:
remediation regression:
```
