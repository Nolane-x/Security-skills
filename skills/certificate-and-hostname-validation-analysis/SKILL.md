---
name: certificate-and-hostname-validation-analysis
description: "Analyze TLS/X.509 certificate, hostname, trust-anchor, EKU, SAN, revocation, pinning, client-auth, and verification callback behavior. Use controlled certificate matrices to prove acceptance-policy errors."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Certificate And Hostname Validation Analysis

Perform dynamic validation only in a local/owned/sandboxed lab, benchmark, CTF, or equivalent explicitly authorized environment. Use synthetic certificate hierarchies, synthetic hostnames, mock endpoints, inert canaries, read-only synthetic resources, or bounded reversible owner-controlled effects. Do not impersonate real third-party services, intercept unrelated traffic, capture credentials, or use production client certificates.

## When to use

Use for clients or servers with custom certificate callbacks, embedded trust stores, pinning, internal PKI, mTLS, certificate selection, redirects, alternate endpoints, session resumption, connection pooling, or any split between certificate-path validation and application peer-identity checks.

## Preconditions

1. Define the intended peer identity before examining certificate names.
2. Use a controlled CA/certificate hierarchy and test endpoint.
3. Pin TLS/library/platform version, verification configuration, trust-store identity, and relevant policy generation.
4. Record whether session resumption, certificate caching, connection pooling, custom callbacks, pinning, or revocation checks can affect the final application decision.
5. Stop before real external-host impersonation, test-root installation on non-test systems, production client-certificate use, or unauthorized interception.

## Causal peer-authentication model

Treat certificate acceptance as a causal chain, not as a single verifier flag:

`intended peer identity -> endpoint/redirect/SNI state -> verifier configuration -> trust-store identity -> trust-store generation -> presented chain identity -> path-building state -> selected trust-anchor identity -> certificate constraints/validity/EKU/KU/name-constraints state -> SAN/reference-identity state -> canonical reference identity -> hostname/identity match decision -> pin/revocation policy state -> callback/override state -> effective accept/reject decision -> authenticated peer/session identity -> privileged consumer boundary -> bounded synthetic result -> receipt/result binding -> trust/pin/revocation/session lifecycle generation`

Every promoted finding must explain which transition diverged, which exact identity or generation was used, and how that divergence reached the application decision. A TLS library success flag, a chain dump, or a callback log is evidence about one transition only.

The following distinctions are mandatory:

- chain validation success != hostname/reference-identity validation success;
- trusted root != authorized peer identity;
- SNI value != verification hostname/reference identity;
- signature validity != policy authorization;
- SAN text != canonical reference identity;
- pin match != complete PKI validation;
- revocation lookup success or absence != complete peer authorization;
- callback reachability != justified verification override;
- certificate acceptance != mTLS account/principal authorization;
- cached/resumed session != current trust-store/pin/revocation policy generation;
- redirect target != original authenticated peer identity;
- certificate subject/CN text != authoritative hostname match when SAN rules apply;
- verifier success != application-level authenticated-session binding;
- connection success != receipt/result binding;
- benign synthetic wrong-peer acceptance != broad interception capability.

## Reference identity and endpoint binding

Start with the identity the application actually intends to authenticate. Record endpoint URI or socket target, redirect target, SNI, proxy/tunnel target if relevant, and the verification reference identity as separate fields. Do not infer that equality is guaranteed by framework defaults.

For every redirect, alternate endpoint, service-discovery result, or connection-reuse path, ask whether the intended peer identity was recomputed, inherited, or accidentally reused. Canonicalize the reference identity according to the exact application/library rules before comparing it to certificate identities. Treat Unicode, trailing-dot, case, wildcard, IP-literal, URI-host, and service-name transformations as typed representation changes whose semantics must be explicit.

## Certificate path and trust-anchor binding

Record the presented chain identity, candidate paths, selected path, selected trust anchor, path-building rules, algorithm constraints, validity interval, EKU/KU, name constraints, policy constraints, and any platform-specific trust exceptions.

A trusted anchor proves only that a path terminates in a configured trust decision. It does not prove that the intended peer identity is authorized. Debug roots, enterprise roots, user-added roots, app-local stores, system stores, and pin stores must be distinguished by identity and generation.

If multiple valid paths exist, record which one the verifier selected and whether callback or application policy depends on attributes that differ across paths. A reproduced issue must survive a control that removes the suspected alternate anchor or path when that path is claimed to be causal.

## SAN and hostname/reference-identity reasoning

Treat SAN entries as typed identity claims rather than arbitrary strings. Record which identity type is being matched, how the verification reference identity is canonicalized, which SAN entry wins, and how wildcard/IP/service-name semantics are applied.

Do not substitute subject/CN matching for SAN behavior unless the pinned platform policy explicitly does so. A textual SAN resemblance is insufficient; evidence must bind canonical reference identity to the exact match decision and final application acceptance.

## Callback, pin, and revocation composition

Trace library verifier output into every application callback or override. Record verifier result, callback inputs, callback policy basis, callback decision, and the effective accept/reject decision after all overrides.

Pinning is a separate policy dimension. A pin match does not automatically justify bypassing name, validity, EKU/KU, or other required checks unless the documented policy explicitly defines that composition. Likewise, a pin mismatch must be interpreted relative to rotation, backup pins, intermediate/leaf scope, and generation state.

Revocation is also threat-model and platform dependent. Record whether revocation is required, soft-fail/hard-fail, stapled, cached, disabled, unavailable, or intentionally out of scope. Revocation observations cannot silently replace path or reference-identity proof.

## Authenticated session and consumer binding

After the effective certificate decision, record the authenticated peer/session identity actually attached to the resulting connection, session, pool entry, or mTLS principal mapping. Then trace the privileged consumer that relies on it.

For a bounded synthetic validation, the consumer should expose only an inert marker, read-only synthetic capability, or reversible owner-controlled effect. Bind that result to the exact authenticated peer/session identity and to a receipt/result so that connection success is not mistaken for consumer-level authorization.

For mTLS, separate certificate acceptance from application account/principal mapping. A valid client certificate does not by itself prove that the mapped account, tenant, role, or operation is authorized.

## Lifecycle and generation reasoning

Record generations for trust stores, pins, revocation data, client-certificate mappings, session tickets, cached verification results, pooled connections, and any callback policy state.

Session resumption and pooling are high-value lifecycle transitions because they may reuse an earlier authentication decision. A finding about stale trust must show that the stale session or cache actually crossed a relevant policy generation boundary and reached the consumer. Conversely, legitimate resumption under an unchanged policy is a negative control, not a vulnerability.

Rotation, revocation, trust-anchor removal, pin changes, and client-certificate/account remapping should produce predictable invalidation behavior. If the platform intentionally defers convergence, record the documented convergence boundary instead of treating temporary coexistence as proof.

## Workflow

1. Define intended peer identity, endpoint, redirect/SNI state, and verification reference identity.
2. Pin verifier configuration, trust-store identity/generation, pin/revocation policy, and lifecycle state.
3. Build a synthetic certificate matrix with known chain, SAN, validity, EKU/KU, and anchor properties.
4. Trace path building and the selected trust anchor before evaluating name matching.
5. Trace SAN/reference-identity canonicalization and the exact hostname/identity match decision.
6. Trace pin/revocation state and any callback/override into the effective accept/reject decision.
7. Bind accepted connections to authenticated peer/session identity and a bounded privileged-consumer result.
8. Exercise lifecycle controls for trust/pin/revocation/session generations when the hypothesis depends on stale state.
9. Run positive, negative, and one-variable counterfactual controls.
10. Eliminate alternative explanations before promoting evidence.
11. Re-run the same controls after remediation and require neighboring legitimate behavior to remain intact.

## Certificate evidence ladder

- **PKI0 — mapped:** peer-identity, endpoint, verifier, trust-store, path, SAN/name, callback, pin, revocation, session, and lifecycle surfaces are inventoried.
- **PKI1 — divergence observed:** a deterministic identity, policy, or generation divergence is observed, but causal acceptance is not yet proven.
- **PKI2 — policy mismatch demonstrated:** controlled positive and negative inputs demonstrate a deterministic path/name/override/pin/revocation/session-policy mismatch.
- **PKI3 — inert wrong-context acceptance:** a synthetic wrong-peer or stale-policy context is accepted in a bounded inert setup and attributed to the relevant decision path.
- **PKI4 — bounded synthetic authority effect:** wrong-context acceptance is causally bound to a bounded reversible synthetic authenticated-session effect or read-only synthetic capability.
- **PKI5 — regression-verified causal proof:** PKI4 plus exact intended/reference identity, endpoint/SNI/redirect provenance, trust-store and anchor generation, path constraints, SAN/canonical-name trace, pin/revocation state, callback decision trace, effective authenticated-session identity, lifecycle generation, privileged-consumer/result binding, meaningful counterfactuals, eliminated alternative explanations, and remediation regression.

A chain-success flag, signature-success flag, callback trace, pin match, revocation response, connection success, or TLS debug log cannot skip missing causal bindings.

## Counterfactual proof

Use one-variable-at-a-time controls whenever feasible:

- same chain, correct versus wrong verification reference identity;
- same reference identity, trusted versus untrusted anchor;
- same chain/name, callback override enabled versus disabled;
- same chain/name, matching versus non-matching pin;
- same policy, current versus stale trust/pin/revocation generation;
- same client certificate, current versus rotated account/principal mapping;
- same redirect path, preserved versus changed reference-identity binding;
- same authenticated session, consumer verifying peer identity versus relying only on connection success.

A useful counterfactual predicts the decision before the run and records whether the observed result matches that prediction. If changing an unrelated variable changes the outcome, revisit the causal model before promoting evidence.

## Alternative explanations

Explicitly test or eliminate relevant alternative explanations, including:

- debug-only permissive mode or development trust roots;
- platform/library fallback semantics that differ from the assumed policy;
- stale session tickets, pooled connections, or cached verification results;
- fixture mistakes in certificate generation, SAN encoding, validity windows, EKU/KU, or chain order;
- clock skew or deliberately frozen benchmark time;
- intentionally disabled revocation under the documented threat model;
- a policy that legitimately authorizes the observed peer identity;
- network/proxy failures unrelated to certificate acceptance;
- certificate-account mapping changes that occur after transport authentication.

Do not label a behavior as a validation bypass until alternatives consistent with the evidence have been narrowed enough to support the claimed causal transition.

## Evidence ceiling

Evidence cannot exceed the weakest demonstrated causal link. Examples:

- chain/path success without reference-identity proof is at most PKI1;
- deterministic wrong-name acceptance in a synthetic decision harness can reach PKI2;
- inert wrong-peer acceptance can reach PKI3 only with direct effective-decision attribution;
- a bounded read-only or reversible synthetic consumer effect can reach PKI4 only when bound to the wrong authenticated peer/session identity;
- PKI5 requires the full causal chain, lifecycle provenance, counterfactual controls, alternative-explanation elimination, and remediation regression.

Never infer arbitrary interception, credential compromise, or broad account takeover from a bounded synthetic marker. The evidence ceiling exists to prevent escalation beyond what the controlled lab actually proves.

## Evidence contract

Capture at minimum:

- authorized scope and pinned environment;
- intended peer identity;
- endpoint/redirect/SNI state and verification reference identity;
- verifier configuration;
- trust-store identity and trust-store generation;
- presented chain, path-building state, and selected trust anchor;
- certificate constraints and validity state;
- SAN/reference-identity state and canonical reference identity;
- hostname/identity match decision;
- pin and revocation policy state;
- callback/override state and effective accept/reject decision;
- authenticated peer/session identity;
- privileged consumer and bounded result;
- receipt/result binding;
- lifecycle generation;
- positive/negative controls;
- counterfactual control;
- alternative explanations considered;
- remediation oracle and regression result;
- final PKI evidence level and evidence ceiling.

## Stop conditions

Stop or downgrade the experiment before:

- impersonating real external hosts;
- installing synthetic roots on non-test systems;
- intercepting unrelated traffic;
- using real production client certificates or production secrets;
- capturing user credentials or tokens;
- modifying persistent host trust outside the owned lab;
- creating persistence, malware, destructive effects, or evasion mechanisms;
- escalating beyond the bounded synthetic oracle needed to distinguish hypotheses.

## Output

```text
scope/environment:
intended peer identity:
endpoint/redirect/SNI state:
verification reference identity:
verifier configuration:
trust-store identity/generation:
presented chain/path/selected anchor:
certificate constraints:
SAN/canonical reference identity:
hostname/identity match decision:
pin/revocation state:
callback/override state:
effective accept/reject decision:
authenticated peer/session identity:
privileged consumer:
bounded result + receipt/result:
lifecycle generation:
positive/negative/counterfactual controls:
alternative explanations:
remediation oracle:
PKI evidence level / ceiling:
```