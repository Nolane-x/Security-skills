# Certificate And Hostname Validation — Operator Runbook

Use this runbook only for local, owned, sandboxed, benchmark, CTF, or explicitly authorized environments. Prefer a synthetic CA, synthetic hostnames, mock endpoints, inert canaries, read-only synthetic resources, and bounded reversible owner-controlled effects. Stop before real third-party host impersonation, unrelated traffic interception, production client-certificate use, credential capture, persistence, malware, destructive actions, evasion, or unauthorized targets.

## Attack surface

Inventory every component that can influence peer authentication:

- intended peer identity and application account/principal identity;
- endpoint, redirect, alternate endpoint, proxy/tunnel target, and SNI state;
- verification reference identity and its canonicalization rules;
- TLS/library/platform version and verifier configuration;
- system, user, enterprise, app-local, embedded, debug, and benchmark trust stores;
- trust-store generation and anchor rotation/removal state;
- presented certificate chain and alternate path candidates;
- selected trust anchor and path-building policy;
- certificate validity, EKU/KU, name constraints, algorithm constraints, and policy constraints;
- SAN identity types, wildcard/IP/service-name behavior, and subject/CN fallback rules;
- pin sets, backup pins, pin scope, and pin generation;
- revocation mode, cache, stapling, soft/hard fail semantics, and revocation generation;
- callback/override entry points and callback policy state;
- session resumption, session tickets, connection pooling, cached verification results, and lifecycle invalidation;
- mTLS certificate-to-account or certificate-to-principal mapping;
- privileged consumer that trusts the authenticated session;
- bounded synthetic result and receipt/result channel used for validation.

## Hypothesis matrix

For each hypothesis, record the claimed causal transition, the exact variable expected to change, the safe oracle, the positive and negative control, and the maximum evidence level that the planned experiment can support.

| Hypothesis class | Example causal claim | Required discriminator |
| --- | --- | --- |
| Reference-identity binding | Valid chain is accepted for the wrong intended peer because verification reference identity diverges | Same chain with only the verification reference identity changed |
| Path/anchor policy | An alternate trusted anchor changes acceptance despite intended policy | Same leaf/identity with suspected anchor present vs removed in the synthetic store |
| Callback override | Application callback converts a verifier rejection into effective acceptance | Same verifier result with callback override enabled vs disabled |
| Pin composition | Pin match bypasses another required identity/path property | Same chain/name with matching vs non-matching synthetic pin while other properties remain fixed |
| Revocation composition | Revocation state changes effective acceptance contrary to documented policy | Same chain/name with controlled current vs stale synthetic revocation state |
| Lifecycle/session reuse | A resumed or pooled session survives a relevant trust-policy generation change | Same authenticated peer with fresh connection vs pre-change resumed session |
| mTLS principal binding | Accepted client certificate maps to an unintended synthetic principal | Same certificate acceptance with current vs rotated synthetic account mapping |

Do not collapse chain validation, hostname/reference-identity matching, callback policy, pinning, revocation, authenticated-session identity, and application principal mapping into one binary result.

## Reference identity, endpoint, redirect, and SNI trace

Record these as separate values:

- intended peer identity;
- initial endpoint;
- redirect or alternate endpoint, if any;
- SNI value;
- proxy/tunnel target, if relevant;
- verification reference identity;
- canonical reference identity after library/application normalization.

A common false inference is that SNI equals the verification reference identity. Prove that relation from the pinned stack instead of assuming it. For redirects, trace whether the application recomputes the verification reference identity, inherits it, or reuses stale state.

When canonicalization matters, record the transformation of URI host, DNS name, IP literal, wildcard, trailing dot, case, Unicode/IDNA representation, or service name before the name-match decision.

## Trust store, path building, and trust-anchor trace

Pin the trust-store identity and trust-store generation. Record whether roots come from system, enterprise, user, app-local, embedded, debug, or benchmark stores.

For each synthetic chain, record:

1. presented leaf/intermediates;
2. candidate path identities;
3. selected path;
4. selected trust anchor;
5. anchor source/store;
6. path-policy inputs;
7. verifier path result.

If alternate paths exist, vary only the suspected anchor/store membership as a counterfactual. A selected trust anchor being configured does not by itself establish authorized peer identity.

## Certificate constraints and validity trace

Record controlled values for:

- not-before/not-after and benchmark clock;
- EKU and KU;
- basic constraints/path length;
- algorithm/key-size policy;
- name constraints;
- certificate policies when relevant;
- client/server authentication role;
- chain order and malformed-chain controls.

Clock skew, fixture generation mistakes, or platform-specific compatibility behavior are alternative explanations that must be eliminated before promoting a policy-bypass claim.

## SAN/canonical reference-identity and name-match trace

Record the SAN identity type and exact SAN values, then separately record the verification reference identity, canonical reference identity, and final hostname/identity match decision.

Test at minimum a controlled valid identity and a controlled wrong-peer identity. When applicable, add wildcard, IP-literal, trailing-dot, or redirect-derived identity controls. Do not use real public service names.

Subject/CN behavior should be treated as a pinned policy fact, not a general assumption. If the platform ignores CN when SAN exists, that fact belongs in the trace.

## Callback/override, pin, and revocation trace

For custom callbacks, record:

- library verifier result;
- callback input state;
- callback code/policy identity;
- callback policy generation;
- callback decision;
- effective accept/reject decision after all overrides.

Callback reachability is not evidence of a bypass. The key question is whether a rejected synthetic wrong-peer context becomes effectively accepted and reaches the authenticated peer/session identity.

For pins, record pin scope, identity, backup pins, match result, and generation. A matching pin is not a substitute for unrelated path/name requirements unless the documented policy explicitly defines it that way.

For revocation, record whether checks are required, disabled, soft-fail, hard-fail, stapled, cached, unavailable, or intentionally outside the threat model. Record revocation generation if stale-state behavior is under test.

## Authenticated peer/session and privileged-consumer trace

After effective acceptance, record the authenticated peer/session identity attached to the resulting connection, resumed session, pooled connection, or mTLS mapping.

Then identify the privileged consumer that relies on that identity. The consumer oracle must remain bounded: an inert marker, a read-only synthetic capability, or a reversible owner-controlled effect.

Bind the consumer outcome to a receipt/result that includes enough synthetic identity to prove which session caused the result. Connection success alone is not sufficient.

For mTLS, separately record transport certificate acceptance and application principal/account mapping. Do not infer principal authorization merely from a valid client certificate.

## Lifecycle/trust/pin/revocation/session generation trace

Record generations for:

- trust store;
- selected anchor set;
- pin policy;
- revocation data/policy;
- callback policy;
- client-certificate/account mapping;
- session ticket or resumed-session state;
- connection pool entry;
- cached verification decision.

When testing session resumption or pooling, compare a fresh connection under the current generation with a pre-change session created under the prior generation. The hypothesis is only supported if stale authentication state actually crosses the relevant generation boundary and reaches the privileged consumer.

## Controlled validation

Use a bounded matrix that changes one causal variable at a time. A strong minimum sequence is:

1. establish a fully valid synthetic baseline;
2. hold the chain fixed and change only verification reference identity;
3. restore identity and change only trust anchor/store membership;
4. restore path and toggle callback override state;
5. hold path/name fixed and change only pin state;
6. when revocation is in scope, change only revocation state/generation;
7. when lifecycle is in scope, compare fresh vs resumed/pooled state across a documented policy-generation change;
8. bind accepted sessions to the same bounded synthetic consumer oracle.

Predict expected outcomes before executing each control. If an unrelated variable changes the result, stop promotion and revisit the causal model.

## False-positive controls

Include controls for:

- debug-only or development permissive modes;
- synthetic debug roots accidentally remaining enabled;
- intentionally disabled revocation;
- legitimate policies that authorize the observed identity;
- clock skew or benchmark-time mistakes;
- malformed fixture generation;
- unrelated network/proxy/TLS negotiation failures;
- cached state that did not actually cross a policy generation;
- library behavior that is documented and security-equivalent to the intended policy;
- mTLS principal mapping changes occurring after transport authentication.

Do not classify pinning absence as a defect when normal PKI verification meets the intended policy.

## Counterfactual controls

Use meaningful counterfactuals such as:

- same chain, correct vs wrong verification reference identity;
- same identity, trusted vs untrusted synthetic anchor;
- same verifier rejection, callback override enabled vs disabled;
- same path/name, matching vs non-matching pin;
- same path/name, current vs stale synthetic revocation state;
- same endpoint, redirect preserves vs changes reference-identity binding;
- same certificate, current vs rotated synthetic mTLS account mapping;
- same trust/pin/revocation policy, fresh connection vs session resumption created under the previous generation;
- same accepted session, consumer verifies authenticated peer/session identity vs relying only on connection success.

A counterfactual should isolate the claimed cause. Avoid changing multiple certificate properties at once when a narrower discriminator is available.

## Alternative explanations

Before evidence promotion, address alternatives that could explain the observation:

- debug-only trust or permissive callbacks;
- app-local vs system trust-store confusion;
- alternate path selection rather than name-check failure;
- platform-specific SAN/CN/wildcard behavior;
- stale connection pooling or session resumption unrelated to the claimed generation change;
- test-certificate validity or EKU/KU generation mistakes;
- benchmark clock skew;
- intentionally disabled revocation under the declared threat model;
- legitimate pin rotation or backup-pin behavior;
- a policy that intentionally authorizes the peer identity;
- unrelated network errors or application retries.

Document why each relevant alternative is inconsistent with the final evidence or leave the evidence ceiling below PKI5.

## Evidence capture

Capture a deterministic record containing:

- authorized scope and environment revision;
- intended peer identity;
- endpoint/redirect/SNI state;
- verification reference identity;
- verifier configuration;
- trust-store identity and trust-store generation;
- presented chain identity;
- path-building state and selected trust anchor;
- certificate constraints/validity state;
- SAN/reference-identity state;
- canonical reference identity;
- hostname/identity match decision;
- pin policy state;
- revocation policy state;
- callback/override state;
- effective accept/reject decision;
- authenticated peer/session identity;
- privileged consumer;
- bounded result and receipt/result binding;
- lifecycle generation;
- positive and negative controls;
- counterfactual control;
- alternative explanation analysis;
- remediation oracle;
- evidence level and evidence ceiling.

Prefer machine-readable synthetic identities and stable fixture names so independent agents can reproduce the reasoning without external secrets.

## Evidence promotion and ceiling

Use the PKI evidence ladder strictly:

- **PKI0:** surface mapped only.
- **PKI1:** deterministic identity/policy/generation divergence observed.
- **PKI2:** controlled policy mismatch demonstrated with positive and negative controls.
- **PKI3:** inert wrong-peer or stale-policy acceptance directly attributed to the relevant decision path.
- **PKI4:** PKI3 plus a bounded reversible synthetic authority effect or read-only synthetic capability bound to the wrong authenticated peer/session identity.
- **PKI5:** PKI4 plus exact identity/path/anchor/name/pin/revocation/callback/session/lifecycle provenance, meaningful counterfactuals, alternative-explanation elimination, receipt/result binding, and remediation regression.

Evidence ceiling rules:

- chain success without reference-identity proof cannot exceed PKI1;
- deterministic wrong-name acceptance in a decision harness can reach PKI2 but not PKI3 without effective acceptance;
- callback reachability alone cannot exceed PKI1;
- an inert wrong-peer acceptance can reach PKI3 only with effective accept/reject attribution;
- a bounded consumer effect can reach PKI4 only when tied to the wrong authenticated peer/session identity;
- PKI5 requires regression verification and preserved legitimate neighboring behavior.

Never promote a synthetic marker into a claim of arbitrary interception, credential compromise, or broad account takeover.

## Remediation checks

After a fix:

1. repeat the original positive control;
2. repeat the original negative control;
3. repeat the causal counterfactual that distinguished the issue;
4. verify the wrong-peer/stale-policy condition is rejected or invalidated as intended;
5. verify the valid synthetic peer still succeeds;
6. verify trust/pin/revocation/session generation transitions converge according to policy;
7. verify callback or pin changes do not silently disable independent path/name checks;
8. verify mTLS principal mapping still authorizes the intended synthetic account;
9. verify the privileged consumer receipt/result is bound to the expected authenticated peer/session identity.

Promote to regression-verified only when the fixed revision blocks the demonstrated causal path while neighboring legitimate behavior remains intact.