---
name: secrets-and-token-flow-analysis
description: "Analyze where credentials, API keys, session tokens, cloud/workload identities, signing keys, capability URLs, and bearer secrets originate, propagate, persist, cross trust boundaries, and become authorized actions. Use for exposure, over-scoping, token confusion, logging/cache leaks, or delegation review."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Secrets and Token Flow Analysis

Model a secret/token as both sensitive data and authority. The same flow can create confidentiality risk, privilege risk, or cross-tenant identity confusion.

## When to use

Use for application sessions, API tokens, OAuth/OIDC/JWT flows, cloud credentials, CI secrets, service-account tokens, signed URLs, reset links, or inter-service authentication.

## Preconditions

Use synthetic/test credentials in owned/local/sandboxed or explicitly authorized environments. Never collect or replay real third-party secrets as proof.

## Workflow

1. **Classify credential semantics.** Bearer, proof-of-possession, signing key, refresh token, session id, capability URL, workload identity.
2. **Map issuance.** Issuer, subject, audience, scopes/roles, resource binding, lifetime, rotation, nonce/session binding.
3. **Map storage.** Browser storage/cookie, process memory, env, file, secret manager, database, cache, logs, telemetry.
4. **Map propagation.** Headers, query strings, IPC/RPC metadata, redirects, jobs/queues, build logs, crash reports.
5. **Map verification.** Signature/MAC, issuer, audience, expiry, nonce, tenant/resource, sender/channel binding.
6. **Check scope attenuation.** Delegated tokens should not silently become broader downstream credentials.
7. **Check token-type confusion.** One token class accepted where another is required, or identity token used as access token.
8. **Check persistence and revocation.** Cache lifetime versus token lifetime, refresh rotation, logout/revocation behavior.
9. **Use synthetic canary credentials** to trace unexpected flow and verify they cannot authorize real resources.
10. **Fix at earliest authority boundary.** Reduce scope/lifetime, bind audience/resource, remove unsafe transport/storage, redact logs.

## Evidence contract

Show credential class, authority represented, issuance constraints, unexpected flow/storage/acceptance, synthetic proof, and negative control. A token string appearing in code is not automatically a live secret; verify provenance without exposing sensitive value.

## Stop conditions

Stop if analysis would reveal real secrets in output, require replay against third-party systems, or token semantics cannot be safely determined from documentation/test fixtures.

## Output

```text
credential class:
authority/scopes:
issuance/binding:
storage locations:
propagation path:
verification checks:
unexpected exposure/acceptance:
synthetic canary evidence:
revocation/lifetime:
remediation:
```
