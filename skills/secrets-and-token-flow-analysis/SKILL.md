---
name: secrets-and-token-flow-analysis
description: "Analyze where credentials, API keys, session tokens, cloud/workload identities, signing keys, capability URLs, and bearer secrets originate, propagate, persist, cross trust boundaries, and become authorized actions. Use for exposure, over-scoping, token confusion, logging/cache leaks, or delegation review."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Secrets and Token Flow Analysis

Model every credential as both sensitive data and a representation of authority. The review goal is not merely to find where credential-shaped bytes appear; it is to prove whether issuance, propagation, verification, delegation, and lifecycle state preserve the intended authority contract.

## When to use

Use for application sessions, API tokens, OAuth/OIDC/JWT flows, cloud credentials, CI secrets, service-account tokens, signed URLs, reset links, capability references, token exchange, workload identity, or inter-service authentication.

## Preconditions

1. Work only in an owned, local, sandboxed, benchmark/CTF, or explicitly authorized environment.
2. Use synthetic/test credentials, synthetic principals, deterministic mock issuers/verifiers, inert capability markers, or read-only services.
3. Pin issuer/verifier configuration, token class, policy generation, clock/test-time source, and relevant cache/introspection state.
4. Never collect, expose, or replay real third-party credentials as proof.

## Causal credential-authority model

Reason through this chain for each credential-sensitive decision:

`credential origin -> issuer identity -> subject identity -> credential class -> issuance constraints -> possession channel -> storage representation -> propagation hop -> verifier identity -> verification decision -> audience/resource binding -> represented authority -> downstream exchange/delegation -> attenuated effective authority -> bounded action/result -> lifecycle/revocation generation`

A credential is safe to accept only when the exact credential class and lifecycle generation are valid for the exact verifier, resource, and authority decision. Keep these distinctions explicit:

- secret bytes != authority semantics;
- issuer identity != subject identity;
- possession != permission;
- syntactic validity != verification success;
- valid signature/MAC != valid authorization context;
- identity token != access token;
- access token != refresh token;
- bearer credential != proof-of-possession credential;
- delegated authority != deputy/downstream ambient authority;
- audience validity != resource authorization;
- expiry time != revocation generation;
- storage location != intended propagation boundary;
- credential acceptance != proof that the resulting action is bound to the same authority context.

Core invariants:

1. Every accepted credential has traceable provenance to an issuer or origin authorized for that credential class.
2. The verifier checks the credential class expected by the interface rather than treating all credential-shaped inputs as interchangeable.
3. Issuer, subject, audience/resource, tenant/namespace when relevant, scopes/roles/capabilities, lifetime, generation, and sender/channel binding are checked according to the credential contract.
4. Cryptographic validity is not treated as sufficient authorization by itself.
5. Represented authority is no broader than the credential and independently justified policy permit for the exact verifier/resource context.
6. Exchange or delegation attenuates authority unless a distinct documented authority boundary independently authorizes expansion.
7. Propagation does not silently change credential semantics or cross an unintended trust boundary.
8. Rotation, refresh replacement, logout/session invalidation, key-generation changes, subject disablement, and explicit revocation advance the relevant lifecycle/revocation generation.
9. Result/receipt/post-state evidence binds the accepted credential context, effective authority, action/resource, and lifecycle generation.
10. Evidence level never exceeds the strongest directly observed causal link.

## Credential-class model

Determine credential class from issuer and verifier contracts, not from string shape. Relevant classes include bearer access tokens, proof-of-possession tokens, identity tokens, refresh tokens, session identifiers, API/service credentials, workload identities, capability or signed resource URLs, one-time reset/verification tokens, signing-key references, and downstream tokens produced by an explicit exchange.

For every class, record what possession means, what verification steps are required, what authority it can represent, whether exchange is allowed, and which lifecycle event invalidates it.

## Issuance provenance and binding

Capture credential origin, issuer identity, issuer/key generation when applicable, subject identity, intended verifier, credential class, audience/resource binding, tenant/namespace binding, scopes/roles/capabilities, issue time, lifetime, nonce/session/sender/channel constraints, refresh/rotation lineage, and whether further delegation is permitted.

A well-formed credential that cannot be traced to the expected issuer or intended semantic class does not satisfy the authority contract.

## Possession, storage, and propagation

Trace how the credential becomes available to each component without exposing the credential value. Record possession channel, storage representation, and every propagation hop across secure cookies/session stores, browser storage when applicable, process memory/environment, secret managers, protected files, database/cache state, HTTP headers, documented redirects, IPC/RPC metadata, queues/jobs, CI/test artifacts, logs, telemetry, or diagnostics.

Use redacted fingerprints, synthetic opaque IDs, issuer-generated canaries, or deterministic fixture identifiers instead of real secret values. Unexpected storage is evidence of a flow divergence, not automatically evidence that a credential was accepted or authorized.

## Verifier-decision trace

Trace the actual decision boundary:

`received credential -> parser/classification -> cryptographic verification where required -> issuer check -> subject check -> audience/resource check -> tenant/namespace check -> lifetime/generation check -> sender/channel/nonce check where required -> scope/capability interpretation -> policy decision -> effective authority`

For each transition, record the observed value and proof source. Distinguish parser acceptance from cryptographic verification, cryptographic verification from semantic verification, and semantic verification from authorization.

## Token-class integrity

Test only with synthetic credentials whether an interface enforces the intended credential class. Safe controls include identity token versus access token, refresh token versus resource token, one-time capability versus reusable access token, bearer versus proof-of-possession semantics, neighboring synthetic audiences/resources, and upstream versus explicitly exchanged downstream credentials.

A wrong-class credential reaching a parser is not enough for promotion; the review must show the verifier decision that incorrectly converges or accepts it.

## Authority representation and attenuation

For every delegation or exchange hop, capture:

`incoming represented authority -> local verification/policy -> local ambient authority -> outgoing/exchanged authority -> next verifier/resource`

The credential's represented authority and the service's ambient authority are separate. Local ambient privileges must not silently broaden downstream authority on behalf of the caller. Any authority expansion must be attributable to an independent documented authority boundary for the exact operation/resource.

## Lifecycle, rotation, and revocation generation

Model timestamp validity separately from lifecycle and revocation generation. Track issuance generation, signing/verification-key generation, refresh rotation lineage, session generation, explicit revocation generation, subject/service disablement generation, logout/session invalidation, and any cached introspection/verifier decision state.

Use synthetic fixtures to compare the same logical credential before and after a generation transition. A still-unexpired timestamp does not override a newer revocation generation unless the documented contract explicitly permits a bounded propagation delay, which must be captured as such.

## Workflow

1. Classify the credential and write the complete credential-authority chain before testing.
2. Map issuance provenance and all semantic bindings required by that class.
3. Trace possession, storage, and propagation using redacted or synthetic identifiers only.
4. Trace verifier decisions and separate parsing, cryptographic verification, semantic verification, and authorization.
5. Compare represented authority with local ambient authority and downstream exchanged authority.
6. Exercise one-dimension synthetic counterfactuals for subject, audience/resource, verifier identity, token class, generation, and attenuation.
7. Advance lifecycle/revocation generation in the deterministic fixture and verify stale acceptance behavior independently of TTL/expiry.
8. Bind any bounded action/result or receipt back to the exact credential context and generation.
9. Eliminate alternative explanations such as stale verifier cache, clock mismatch, different resolved resource, retry/duplicate delivery, or fixture contamination.
10. Verify remediation blocks the wrong flow while preserving legitimate neighboring credential use.

## Credential-authority evidence ladder

- **S0 — credential surface:** a credential, token, session, key, capability reference, or issuance/verification path is identified; no security-relevant divergence is established.
- **S1 — binding/flow divergence:** issuance, storage, propagation, verifier expectation, token class, audience/resource, scope, or lifecycle metadata diverges from the documented contract, but incorrect acceptance is not observed.
- **S2 — verifier-context mismatch:** controlled synthetic evidence shows contexts that should remain distinct converging at a verifier decision, or a required semantic binding is absent, without an accepted bounded effect.
- **S3 — inert wrong-context acceptance:** a synthetic credential is accepted by a mock, read-only, or inert verifier in a token-class, audience/resource, subject, verifier, or lifecycle context where the oracle expects rejection.
- **S4 — bounded synthetic authority effect:** the wrong-context acceptance produces a bounded, reversible, owner-controlled security-relevant action/result in the synthetic fixture.
- **S5 — causal lifecycle/authority proof:** S4 plus issuance provenance, verifier-decision trace, credential-class integrity, exchange/attenuation trace where applicable, revocation-generation control, alternative-explanation elimination, remediation, and regression evidence preserving legitimate neighboring credential flows.

## Counterfactual proof

Use one-dimension-at-a-time synthetic controls such as same issuer/class with another subject, same subject with another audience, neighboring synthetic resource, same fixture identity after revocation-generation advance, same request with another credential class, narrower downstream exchange, another verifier identity, reduced local ambient privilege, and the remediated flow with the legitimate neighboring credential still accepted.

Keep unrelated state fixed so the changed authority dimension remains causal.

## Alternative explanations

Before promotion, rule out or record fixture use of another issuer/key, stale introspection/verifier cache, clock skew or deterministic test-time mismatch, different resolved audience/resource, retry or duplicate delivery, intentionally global service identity, contractually required background-worker identity substitution, unobserved upstream exchange, parser normalization changes, action/result correlation error, documented delayed revocation, and synthetic fixture contamination.

## Evidence contract

Record credential class, credential origin, issuer/subject/verifier identities, issuance constraints, possession/storage/propagation path, verification decision, audience/resource binding, represented and attenuated authority, lifecycle/revocation generation, counterfactuals, alternative explanations, bounded result if any, and remediation regression.

A secret string in code or logs, a successful parse, a valid signature, or a permissive-looking configuration is not by itself a validated authority failure.

## Evidence ceiling

Report no higher than the strongest directly captured level S0-S5. Do not infer S3 from suspicious bindings alone, S4 from inert acceptance, or S5 without lifecycle/revocation controls, authority attenuation evidence where relevant, alternative-explanation elimination, and remediation regression.

## Stop conditions

Stop if validation would expose real secret values, replay a production or third-party credential, access real customer data, require an unauthorized verifier/resource, create irreversible state, bypass a consent boundary, or exceed the synthetic/mock/read-only/reversible fixture. Record the ceiling reached and the missing evidence instead of escalating risk.

## Output

```text
credential class:
credential origin / issuer / subject:
issuance constraints:
possession and storage representation:
propagation hops:
verifier identity and decision:
audience/resource binding:
represented authority:
downstream exchange / attenuation:
lifecycle / revocation generation:
bounded result or receipt:
counterfactual controls:
alternative explanations:
evidence level / ceiling:
remediation regression:
```
