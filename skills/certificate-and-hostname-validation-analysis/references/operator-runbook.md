# Certificate And Hostname Validation Operator Runbook

This runbook is for authorized, owned, local, sandbox, synthetic, benchmark, or otherwise explicitly scoped systems. Use synthetic hostnames, synthetic CA hierarchies, mock verifier callbacks, local trust stores, inert sinks, and bounded reversible configuration. Stop before any third-party impersonation, unrelated traffic interception, production key use, or non-test trust-store modification.

The objective is not to prove that a certificate looks unusual. The objective is to reconstruct the identity-and-policy decision that caused a peer to be accepted or rejected, isolate the transition with deterministic controls, and cap the claim at the evidence actually captured.

## Attack surface

Inventory every component that can influence peer authentication or reuse its result:

- connection-intent and endpoint-authority construction;
- DNS/service discovery, redirect, proxy, tunnel, failover, and SNI selection;
- TLS library/platform verifier and path builder;
- presented leaf/intermediates and locally supplied intermediates;
- application, user, enterprise, bundled, and system trust stores;
- time source, EKU/key usage, certificate policy, name constraints, and SAN/reference-identifier matching;
- revocation mechanisms and documented fail-open/fail-closed/soft-fail behavior;
- application callbacks, wrappers, overrides, retries, and fallbacks;
- certificate/SPKI pin policy, fallback, and pin generation;
- mTLS client-certificate selection, validation, certificate identity, and principal mapping;
- TLS sessions, verifier caches, connection pools, and session resumption;
- lifecycle events that rotate certificates, roots, pins, mappings, endpoints, or revocation state.

For every surface, record whether it is reachable in the reviewed release configuration. A debug-only root or callback is not release exposure without release-boundary proof.

## Hypothesis matrix

Write hypotheses as transition failures rather than labels. Each row should state the intended invariant, the controlled variable, expected valid result, expected invalid result, evidence level before testing, and the alternative explanation most likely to mimic the result.

Examples:

| Hypothesis | Controlled transition | Positive control | Negative control | Primary alternative |
| --- | --- | --- | --- | --- |
| wrong peer name is accepted | reference identifier -> SAN binding | synthetic valid name accepted | same chain with wrong synthetic name rejected | client reached different local endpoint/SNI |
| local alternate path changes authority | presented chain -> constructed path -> trust anchor | intended synthetic root selected | alternate untrusted root rejected | platform path builder used cached intermediate |
| callback bypasses verifier | library result -> application override -> final decision | verifier-valid case accepted | verifier-invalid case rejected when override off | retry/fallback produced apparent success |
| stale session ignores policy rotation | policy generation -> session reuse | fresh session follows new policy | pre-rotation session cannot retain forbidden authority | product intentionally grandfathers sessions |
| mTLS identity maps to wrong principal | certificate identity -> principal mapping | mapped synthetic cert reaches intended principal | same cert cannot reach neighboring principal | test fixture selected different client cert |

Do not combine several changed variables in one decisive row. Split the matrix until a counterfactual can isolate one transition.

## Connection intent and reference identity trace

Record the connection intent before examining the certificate. Capture the intended peer/service identity, reference identifier, endpoint authority, and the configuration or protocol field from which that reference identifier originated.

Trace every redirect, service-discovery result, endpoint failover, proxy hop, and authority rewrite. Ask whether untrusted input can replace the reference identity or merely influence transport routing. The reference identifier must not be inferred from the presented certificate itself.

For deterministic fixtures, use synthetic names such as `api.fixture.test` and `other.fixture.test`. Record the exact expected identity contract for each local endpoint.

## Endpoint routing and TLS context trace

Record the actual transport peer, proxy/tunnel role, SNI value, ALPN or equivalent TLS context when relevant, and which local synthetic certificate the server selected. Confirm that the test client reached the intended local endpoint before interpreting a verification result.

When a legitimate proxy terminates TLS, separate `transport peer` from `application service identity`. Determine whether the protocol expects authentication of the proxy at this layer, the end service at another layer, or both. Do not call proxy termination an identity loss merely because the transport certificate names the proxy.

An endpoint or SNI mismatch is a first-class alternative explanation and must be ruled out before PKI3 promotion.

## Presented chain and constructed path trace

Capture the wire-presented leaf and intermediates separately from the verifier's constructed path. Record certificate fingerprints or other synthetic fixture identities, issuer/subject relationships, local intermediate sources, and platform path-building behavior.

A presented chain is input, not the final validation path. Platforms can use cached or local intermediates and may build an alternate path. Use a controlled fixture to change only one intermediate or trust path while holding the reference identifier and application callback constant.

If the platform does not expose the constructed path directly, document the strongest available read-only trace and lower the evidence ceiling rather than pretending the selected path is known.

## Trust anchor and trust-store generation trace

Record the selected trust-anchor identity, the trust-store scope from which it came, and the trust-store generation active for the decision. Distinguish system, application-bundled, enterprise, user-added, test, and development trust where the platform exposes those scopes.

`trusted root presence` is not proof that the verifier selected that root. Use a synthetic hierarchy or read-only verifier trace that can distinguish path choice. Record trust-store changes as generation transitions and state whether cached verifier/session decisions are expected to survive them.

Never install a test root on a third-party or non-test device. Keep trust mutations local and reversible.

## Certificate policy and name-binding trace

Record, independently:

- signature/path-validation result;
- certificate time state under the pinned clock;
- EKU and key-usage suitability;
- policy/name-constraints state if applicable;
- SAN/reference-identifier comparison and matching rule;
- revocation policy/state;
- any platform-specific policy result consumed by the application.

A name match does not imply the rest of policy passed, and a valid chain does not imply the name matches. For a hostname counterfactual, hold chain, endpoint, time, EKU, callback, and policy constant while changing only the synthetic reference identifier or SAN relation.

## Verifier callback and final-decision trace

Capture the library verifier result before the application callback, the callback inputs, the callback's explicit return or override state, wrapper behavior, retries/fallbacks, and the final application accept/reject decision.

Distinguish an `application override` from logging, telemetry, or supplemental checks. An unsafe callback hypothesis becomes causal only if the owned fixture demonstrates that changing the override alone changes final acceptance of an otherwise invalid synthetic peer.

Bind the final decision to a bounded result such as an inert local response, canary receipt, or controlled connection-state observation. Do not infer application impact from a callback line alone.

## Pin policy and pin-generation trace

First state whether the product requires pinning at all. Absence of pinning is not a vulnerability when normal PKI satisfies the declared requirement.

If pins exist, record what they identify (certificate, SPKI/key, issuer, or application-defined material), their synthetic service scope, fallback behavior, and current `pin generation`. Trace whether a pin match supplements normal PKI or intentionally replaces a specific part of it under the product contract.

Test rotation with versioned synthetic pins. Keep hostname, trust path, and callback behavior constant when isolating pin-policy logic.

## mTLS identity and principal-mapping trace

For mutual TLS, record the client certificate presented, its constructed validation path, client-auth EKU/policy, validated certificate identity, and the application `principal mapping` that consumes that identity.

Separate certificate possession from application authorization. A synthetic client certificate may validate cryptographically yet map to no principal, the wrong principal, or a principal without the bounded permission. If authorization is outside this skill's scope, record the mapping result without claiming a downstream authorization bypass.

Use only lab-created client certificates. Stop before any production client certificate or private key would be required.

## Session cache and resumption trace

Record whether the result came from a fresh full verification, connection-pool reuse, verifier cache, or `session resumption`. Capture the session/cache generation and the policy generation against which it was established.

When trust, pins, certificate material, revocation state, endpoint authority, or mTLS mapping changes, state the documented invalidation rule. Compare a fresh connection with a pre-change resumed/cached connection. A difference is not automatically a defect: determine whether grandfathering is intentional and whether its lifetime is bounded.

Treat stale-state behavior as PKI4 material only after the underlying PKI3 identity/policy transition is already proven.

## Revocation and lifecycle-generation trace

Record the configured `revocation policy`, mechanism (for example stapled status or configured lookup), freshness window, availability state, and fail-open/fail-closed/soft-fail semantics. `unknown` or `unavailable` must not be silently rewritten as `good` or `revoked` in the evidence record.

Build a lifecycle timeline that includes relevant certificate, trust-store, pin, revocation, endpoint, principal-mapping, and session/cache generations. For each transition, identify which decisions must be recomputed and which cached state is allowed to persist.

Use synthetic revocation fixtures or policy simulation. Do not publish revocation or CA state that affects third parties.

## Controlled validation

Use the smallest benign fixture that isolates the hypothesis:

1. create a synthetic CA hierarchy and synthetic hostnames;
2. run a local TLS endpoint or mock verifier with a pinned library/platform version;
3. record connection intent, endpoint/SNI context, presented chain, constructed path, selected trust-anchor identity, and trust-store generation;
4. record certificate policy/name checks, library verifier result, application callback, pin/mTLS state if applicable, and final decision;
5. bind that decision to an inert local or controlled canary result;
6. run the positive control;
7. run the negative control changing only the intended transition;
8. run at least one counterfactual that reverses the causal condition;
9. when lifecycle is in scope, repeat with fresh and resumed/cached state across one versioned policy-generation change.

All dynamic actions must remain local, owned, sandboxed, synthetic, or explicitly authorized. Abort if the fixture would require a real external hostname, unrelated traffic, production key material, or a non-test trust store.

## False-positive controls

At minimum test the applicable distinctions:

- chain-valid versus hostname-valid;
- presented root versus selected trust-anchor identity;
- trust-anchor identity versus trust-store generation;
- SAN match versus EKU/key-usage/policy suitability;
- verifier success versus final application acceptance;
- callback logging versus actual application override;
- normal PKI success versus optional pinning;
- pin match versus complete peer identity;
- client-certificate possession versus mTLS principal mapping;
- fresh validation versus stale session resumption or verifier cache;
- revocation-data unavailability versus a documented revocation-policy violation;
- intended proxy termination versus accidental wrong-service identity;
- debug-only trust/callback behavior versus release-reachable behavior.

A control is weak if it changes several of these simultaneously. Redesign it until the transition is isolated or retain a lower evidence ceiling.

## Counterfactual controls

Choose a counterfactual at the exact disputed edge:

- same chain, callback, and endpoint; change only reference hostname/SAN relation;
- same hostname and leaf; change only the constructed path or selected synthetic trust anchor;
- same path and identity; change only EKU/key usage, clock state, or name-constraint policy;
- same verifier result; toggle only the mock application override;
- same certificate and endpoint; advance only trust-store or pin generation;
- same policy; compare fresh verification with a pre-change resumed/cached session;
- same validated synthetic client certificate; change only its certificate-to-principal mapping.

Record expected and observed decisions before interpreting the result. Counterfactual failure means the hypothesized cause is not isolated.

## Alternative explanations

For every PKI3+ candidate, record applicable alternatives and the evidence used to exclude them:

- wrong local endpoint or routing result;
- SNI selected a different synthetic certificate;
- legitimate proxy/tunnel termination explains transport identity;
- platform path construction chose a local intermediate or alternate trust anchor;
- clock skew explains validity behavior;
- stale session/cache explains apparent policy behavior;
- pinned offline revocation policy explains missing status;
- permissive trust/callback state is debug-only or otherwise absent from release configuration;
- application retry/fallback produced the bounded success;
- mTLS fixture selected a different client certificate or principal mapping.

If an alternative remains plausible and could fully explain the result, keep the evidence below PKI3.

## Evidence capture

For every run, capture a deterministic record containing:

- fixture ID and synthetic identities;
- library/platform version and verifier configuration;
- reference identifier and endpoint authority;
- routing/SNI/proxy context and actual local transport peer;
- presented chain and constructed path evidence;
- selected trust-anchor identity and trust-store generation;
- time, EKU/key usage, policy/name-constraint, SAN/reference-identifier, and revocation state;
- library verifier result and application override/callback result;
- pin policy/generation and mTLS principal mapping when applicable;
- final accept/reject decision and bounded inert result;
- session/resumption/cache generation;
- positive, negative, and counterfactual controls;
- alternative explanation dispositions;
- PKI evidence level and evidence ceiling.

Prefer normalized text/JSON fixture data over screenshots. Do not capture production secrets or private keys.

## Evidence promotion and ceiling

- **PKI0:** hypothesis only.
- **PKI1:** concrete configuration/trace/decision observed, causal binding incomplete.
- **PKI2:** controlled correlation exists, but the complete identity/policy chain or counterfactual set is incomplete.
- **PKI3:** intended reference identity, actual path/trust anchor, relevant policy checks, verifier/callback, final decision, bounded result, controls, and alternatives are causally bound.
- **PKI4:** PKI3 is extended across a relevant lifecycle generation with fresh-versus-stale behavior proven.
- **PKI5:** remediation oracle passes, the original invalid case no longer reaches the result, neighboring legitimate behavior is preserved, and stale state converges correctly.

The `evidence ceiling` is the highest level directly supported by the trace. Scanner/model/tool output, a certificate dump, a valid signature, a single handshake, or a callback message cannot independently establish PKI3+.

## Remediation checks

Tie remediation to the broken transition. Examples include restoring reference-identifier verification, removing an unsafe callback override, narrowing trust-store authority, correcting pin scope/rotation, repairing mTLS identity-to-principal mapping, or invalidating stale sessions when the documented policy requires it.

Regression must replay:

1. the original invalid synthetic case, which must now reject or lose the bounded effect;
2. the valid positive control, which must continue to work;
3. at least one neighboring negative control, which must remain rejected;
4. any lifecycle/resumption case implicated by the root cause;
5. the exact transition-specific counterfactual.

Do not accept a fix that merely hides the trace, changes the test identity, disables the feature, or globally trusts more certificate material. Preserve the legitimate behavior surrounding the corrected binding.
