# Secrets and Token Flow Operator Runbook

Use this runbook only for local, owned, sandboxed, benchmark/CTF, or explicitly authorized environments. Use synthetic/test credentials, synthetic principals, deterministic mock issuers/verifiers, inert markers, read-only services, or reversible owner-controlled state. Never capture or replay a real third-party credential.

## Attack surface

Map every place a credential can be issued, possessed, stored, propagated, verified, exchanged, cached, revoked, or converted into a bounded result. Include issuer identity, subject identity, credential class, verifier identity, audience/resource boundary, represented authority, local ambient authority, lifecycle generation, revocation generation, and the result/receipt path. Record both the observed value and the proof source for each transition.

## Hypothesis matrix

Turn broad concerns into falsifiable statements. Example hypotheses include: a verifier accepts the wrong token class; audience/resource binding is not enforced; a downstream exchange broadens represented authority; a stale revocation generation remains accepted; or propagation crosses an unintended trust boundary. Pair each hypothesis with a synthetic safe oracle, positive control, negative control, evidence ceiling, stop condition, and remediation oracle.

## Credential-class trace

Determine credential class from the issuing and verifying contract, not from string shape. Record whether the fixture represents a bearer access token, proof-of-possession token, identity token, refresh token, session identifier, API/service credential, workload identity, capability URL, one-time token, signing-key reference, or exchanged downstream token. Record what possession means and which verifier operations the token class is allowed to authorize.

## Issuance provenance trace

Record credential origin, issuer identity, issuer/key generation where relevant, subject identity, intended verifier, audience/resource binding, tenant/namespace binding where relevant, scopes/roles/capabilities, issue time, expiry, nonce/session/sender/channel constraints, refresh lineage, and whether further delegation is allowed. Preserve only synthetic identifiers or redacted fingerprints, never secret values.

## Possession and storage trace

Record how the synthetic credential becomes available to each component: secure cookie/session store, protected process state, environment, secret manager, protected file, database/cache representation, browser storage when applicable, or deterministic test fixture. Distinguish possession from permission and storage location from intended use. Note whether storage changes lifecycle semantics or merely retains opaque bytes.

## Propagation-boundary trace

For each propagation hop, record source component, destination component, transport representation, trust boundary, intended credential class, and proof source. Cover headers, documented redirects, IPC/RPC metadata, queues/jobs, cache/introspection state, CI/test artifacts, logs, telemetry, and diagnostics only through synthetic or redacted fixture identifiers. A propagation observation alone does not prove verifier acceptance.

## Verifier-decision trace

Trace the exact decision sequence: parser/classification, cryptographic verification when required, issuer check, subject check, audience/resource check, tenant/namespace check, lifetime and revocation generation check, sender/channel/nonce check when required, scope/capability interpretation, policy decision, and effective authority. Record verifier identity and the evidence source for every check. Separate parse success, cryptographic validity, semantic verification, and authorization.

## Audience and resource binding

Record the intended audience/resource for each synthetic credential and the resolved resource used by the verifier. Use neighboring synthetic resources and verifiers as counterfactual controls. Audience/resource equality must be evaluated according to the credential contract; a valid signature or valid audience string does not independently establish resource authorization.

## Authority representation trace

Record represented authority from the credential separately from service-local ambient authority. Identify scopes, roles, capabilities, tenant/resource limits, and the exact operation implied by the verifier decision. If the service has broader ambient privilege, record why that privilege is or is not relevant to the caller's effective authority.

## Delegation and attenuation trace

For each exchange or delegation hop record incoming represented authority, local verification/policy, local ambient authority, outgoing credential class, outgoing audience/resource, and attenuated effective authority. The outgoing authority should not silently exceed the incoming represented authority unless a distinct documented authority boundary independently grants the expansion. Compare a narrower downstream exchange and a reduced-ambient-privilege variant as controls.

## Lifecycle and revocation-generation trace

Track issuance generation, signing/verification-key generation, session generation, refresh-token lineage, logout/session invalidation, subject/service disablement generation, explicit revocation generation, and any cached verifier/introspection decision. Compare the same logical synthetic credential before and after a controlled generation advance. Expiry time and revocation generation are separate facts; stale verifier cache is an alternative explanation that must be tested independently.

## Result and receipt binding

Bind each bounded result or receipt to verifier identity, credential fixture identity, credential class, represented authority, attenuated effective authority, action/resource, and lifecycle generation. Use inert markers, read-only outputs, deterministic policy decisions, or reversible owner-controlled state. Do not infer authority from an uncorrelated downstream result.

## Controlled validation

Use one-dimension-at-a-time synthetic experiments. Hold unrelated state fixed while varying issuer identity, subject identity, audience/resource, verifier identity, token class, revocation generation, local ambient privilege, or downstream attenuation. Include a valid neighboring credential as a positive control and an expected rejection as a negative control. Never replay real tokens or capture live secret values. Stop before any third-party, production, irreversible, or unauthorized effect.

## False-positive controls

Rule out stale verifier or introspection cache, fixture contamination, clock/test-time mismatch, a different resolved audience/resource, retry or duplicate delivery, parser normalization changes, an intentionally global service identity, documented worker identity substitution, an upstream token exchange not yet observed, delayed revocation permitted by contract, and result-correlation mistakes. Record each alternative explanation and the evidence that supports or excludes it.

## Counterfactual controls

Use synthetic counterfactuals such as same issuer/class with another subject, same subject with another audience/resource, same request with another token class, same logical credential after revocation generation advance, another verifier identity, narrower downstream authority, reduced local ambient privilege, and the remediated path with the legitimate credential preserved. Each counterfactual must change only the intended authority dimension.

## Evidence capture

Capture the causal chain, synthetic fixture IDs, issuer identity, subject identity, credential class, issuance constraints, possession/storage representation, propagation hop, verifier identity, verification decision, audience/resource binding, represented authority, attenuated effective authority, lifecycle generation, revocation generation, bounded result, controls, alternative explanations, and remediation evidence. Store no real credential value.

## Evidence promotion and ceiling

Promote only from direct evidence. S0 identifies the credential surface; S1 establishes a binding or flow divergence; S2 establishes verifier-context convergence or missing semantic binding; S3 requires inert wrong-context acceptance; S4 requires a bounded reversible synthetic authority effect; S5 additionally requires issuance provenance, verifier-decision trace, token-class integrity, attenuation evidence where relevant, revocation-generation control, alternative-explanation elimination, and remediation regression. The evidence ceiling is the highest level directly supported.

## Remediation checks

Verify the causal fix at the earliest correct boundary: credential class enforcement, issuer/subject/audience/resource binding, sender/channel binding, scope reduction, explicit downstream attenuation, lifecycle-generation checks, revocation-cache invalidation, safer storage/propagation, or result-binding correction. Re-run the failing synthetic path, the positive neighboring credential, the negative control, and the relevant counterfactual. The fix passes only when wrong acceptance disappears and legitimate neighboring credential flows remain valid.
