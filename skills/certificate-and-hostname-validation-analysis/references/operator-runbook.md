# Certificate And Hostname Validation Operator Runbook

Use only on local/owned/sandboxed/benchmark or otherwise explicitly authorized TLS systems. Prefer a synthetic CA, loopback/mock peers, fake service identities, inert consumers, read-only traces, and bounded reversible session effects. Never require third-party impersonation, unrelated traffic interception, production client credentials, or unsafe proof.

## Attack surface

Inventory every place that can influence peer trust: original URL/service name, redirect and alternate endpoints, transport target, SNI, verification reference identity, TLS/library verifier and callbacks, trust-store sources, intermediate caches, path builder, trust anchors, SAN/CN matching, certificate policies, key usage/EKU, name constraints, pinsets, revocation behavior, session resumption, client-certificate mapping, and downstream consumers of authenticated peer/session identity.

Do not collapse these into a single “TLS valid” state. Each is a separate transition that may diverge.

## Hypothesis matrix

Write one falsifiable hypothesis per transition. Examples include: a wrong-host certificate reaches final acceptance because the application reference identity differs from the URL; an alternate path selects an unauthorized anchor; a callback overrides a library rejection; pin fallback masks an otherwise required check; a resumed session survives a trust-store generation change; or mTLS certificate acceptance maps to a stale application identity.

For each hypothesis record intended behavior, controlled positive case, controlled negative case, observable transition, safe oracle, evidence ceiling, and remediation oracle.

## Peer and endpoint intent trace

Record intended peer/service identity and purpose, original endpoint, redirect target, alternate endpoint, transport target, scheme/port, and any proxy or local fixture state. A change in endpoint identity changes the hypothesis unless policy explicitly authorizes equivalence.

## Reference-identity and SNI trace

Record SNI separately from the verification host/reference identity. Derive and capture the canonical reference identity used by the verifier, including relevant normalization or IDNA/IP-address rules in the test environment. Do not infer identity from a displayed URL or connection target alone.

## Verifier and trust-store trace

Pin the TLS/library/platform verifier identity and configuration. Record trust-store source, exact test-root/intermediate set, trust-store generation, debug-only versus production-equivalent configuration, and any intermediate/path cache that can affect resolution.

## Certification-path and trust-anchor trace

Capture presented leaf/intermediates, path-building inputs, candidate or observable path state, selected certification path, and selected trust anchor. A signature-valid chain is not enough; show which anchor and policy actually authorized the synthetic peer.

## Certificate-constraint trace

Record validity interval, signature/path state, basic constraints, path length when applicable, key usage, EKU, certificate policies, name constraints, and any platform-specific constraint decision. Keep cryptographic validity separate from intended peer-purpose authorization.

## SAN and hostname binding trace

Record SAN/CN inputs used by the verifier, canonical reference identity, wildcard/IP/name handling, and final hostname/service-identity match result. A wrong-host negative control should differ only at the intended identity transition where possible.

## Pinning and revocation trace

Record pinset identity, backup pins, rotation state, pin generation, revocation policy, observable status, cache/generation state, and soft-fail semantics. Pin success does not replace required PKI checks; revocation unavailable is not equivalent to revocation good.

## Callback and final-decision trace

Capture library verification result before the callback, callback/override input, callback output, whether the callback is authoritative, and the final application decision. Callback reachability alone is not evidence of bypass. Keep debug-only callbacks explicit and separate from production-equivalent policy.

## Authenticated-peer/session and mTLS mapping trace

After final acceptance, record authenticated peer identity and authenticated session identity exposed to the application. For mTLS, separately record certificate identity, mapping rule/generation, mapped application account/service, and downstream authorization context. Certificate acceptance is not application-account authorization.

## Lifecycle and generation trace

Track certificate rotation, trust-store generation, pin generation, revocation cache/policy generation, verifier-policy generation, endpoint policy, mTLS mapping generation, session-ticket/cache generation, and resumed-session state. A resumed session after an authoritative change is its own hypothesis; do not assume the new policy was re-evaluated.

## Privileged-consumer and result trace

Identify the downstream consumer that relies on the authenticated peer/session identity. Use only an inert or read-only synthetic consumer, or a bounded reversible owner-controlled session marker. Bind the bounded result and receipt/result correlation to the exact handshake tuple so concurrent handshakes cannot be mistaken for the causal source.

## Controlled validation

1. Build a deterministic synthetic CA and local test peers with explicit certificate identities.
2. Pin verifier, trust store, endpoint, callback, pin, revocation, and lifecycle state before each trial.
3. Run the positive control first to prove the fixture can establish the intended valid peer.
4. Change one transition for the negative or hypothesis case: wrong-host, wrong anchor, wrong EKU/policy, pin generation, callback decision, or lifecycle generation.
5. Capture selected path/anchor, canonical reference identity, final application decision, authenticated peer/session identity, and receipt/result correlation.
6. If testing session resumption, prove whether a full verification path was re-run or a previous authenticated session was reused.
7. Stop at inert/read-only/bounded evidence; do not escalate to real interception or credential use.

## False-positive controls

Use controls that eliminate nearby explanations: valid neighboring hostname, authorized anchor, intended EKU/policy, current pinset, callback disabled while library behavior stays fixed, fresh versus resumed session, current versus stale trust-store generation, and independent mTLS mapping state. Keep clock/time, DNS/hosts fixture, proxy state, and intermediate cache deterministic.

A failure caused by malformed syntax, unrelated certificate expiry, clock skew, broken fixture DNS, or disabled test service does not validate a peer-trust hypothesis.

## Counterfactual controls

Choose at least one transition-specific counterfactual: same chain with valid versus wrong canonical reference identity; same leaf with authorized versus unauthorized selected trust anchor; same certificate with one EKU/policy/name-constraint difference; same verifier with pin generation changed; same callback input with override removed; same peer before and after trust-store generation update; same authenticated certificate with mTLS mapping changed independently; or same resumed session after authoritative policy generation advances.

A useful counterfactual isolates one causal transition while holding other identities and policies constant.

## Alternative explanations

Before PKI3+ promotion, explicitly evaluate applicable alternative explanation paths: wrong synthetic endpoint selected; DNS/hosts/proxy changed the target; SNI/reference identity difference is intentional; test root exists only in a debug-only store; cached intermediates changed the selected trust anchor; callback was non-authoritative; pin fallback/test mode explains acceptance; session resumption reused earlier valid state; mTLS account mapping explains downstream identity; revocation soft-fail is documented policy; clock skew invalidated a control; or another handshake produced the receipt.

Do not promote until the claimed root cause remains after plausible alternatives are controlled.

## Evidence capture

Capture at minimum: environment and verifier version/configuration; intended peer identity; endpoint/redirect/transport/SNI; canonical reference identity; trust-store identity and trust-store generation; presented leaf/chain fingerprints; path-building state, selected path and selected trust anchor; certificate constraints; SAN/hostname result; pin policy and pin generation; revocation and soft-fail state; callback state; final application decision; authenticated peer identity; authenticated session identity; mTLS mapping when relevant; privileged consumer; bounded result; receipt/result binding; lifecycle generations; positive/negative controls; counterfactual; alternative explanations; evidence level; evidence ceiling; remediation result.

## Evidence promotion and ceiling

Use PKI0–PKI5:

- **PKI0:** surface mapped only.
- **PKI1:** identity/policy/generation divergence observed.
- **PKI2:** controlled verification-policy mismatch demonstrated.
- **PKI3:** inert synthetic wrong-peer acceptance reaches the final application verifier.
- **PKI4:** the wrong-peer acceptance creates a bounded reversible authenticated-session effect or read-only/inert consumer result bound to the exact handshake tuple.
- **PKI5:** PKI4 plus exact peer/endpoint/SNI/reference identity, verifier/trust-store generation, chain/path/anchor, certificate constraints, SAN/hostname binding, pin/revocation/callback decisions, final application decision, authenticated peer/session, applicable mTLS mapping, lifecycle controls, privileged consumer, receipt/result binding, meaningful counterfactual, eliminated alternatives, and remediation regression.

The evidence ceiling is the highest directly supported level. A fingerprint, chain success, pin match, callback log, connection success, or lock icon cannot jump missing transitions.

## Remediation checks

Fix the earliest incorrect transition, then re-run both the negative hypothesis case and neighboring valid behavior. Confirm the synthetic wrong peer is rejected while intended valid peers still work. If redirects or alternate endpoints are legitimate, preserve only documented equivalence. If rotating roots or pins, test old/current/next generations explicitly. If changing callbacks, verify library failures remain failures unless narrowly authorized. If changing session invalidation or mTLS mapping, verify stale sessions/mappings lose authority while current legitimate sessions still work.

Record the fixed revision/config generation and promote to regression-verified only after the former hypothesis no longer reproduces and positive controls remain healthy.
