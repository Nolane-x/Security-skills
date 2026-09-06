---
name: certificate-and-hostname-validation-analysis
description: "Analyze TLS/X.509 certificate, hostname, trust-anchor, EKU, SAN, revocation, pinning, client-auth, and verification callback behavior. Use controlled certificate matrices to prove acceptance-policy errors."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Certificate And Hostname Validation Analysis

Perform any dynamic validation only in an authorized, owned lab or equivalent explicitly scoped test environment.

## When to use

Use for clients/servers with custom certificate callbacks, embedded trust stores, pinning, internal PKI, mTLS, certificate selection, or endpoint identity checks.

## Preconditions

1. Use a controlled CA/certificate hierarchy and test endpoint.
2. Pin TLS/library/platform version and verification configuration.
3. Do not impersonate third-party services or intercept unrelated traffic.

## Workflow

1. Define intended peer identity and trust policy: roots, hostname/SAN, EKU/key usage, validity, name constraints, client-cert mapping, pin scope.
2. Trace library verification result into application callbacks/overrides and final accept/reject decision.
3. Check hostname/identity matching after redirects/alternate endpoints and any split between chain validation and name validation.
4. Review trust-anchor loading, debug/development roots, pin rotation/fallback, and mTLS certificate-to-account mapping.
5. Run a controlled matrix: valid, wrong hostname, untrusted root, expired/not-yet-valid, wrong EKU, malformed chain, and configured pin variants.
6. Treat revocation policy separately according to documented threat model and platform behavior.

## Evidence contract

Record controlled certificate chain properties, intended identity, library callback/result, application override, and final connection decision. Pinning absence is not a bug when normal PKI validation meets the requirement.

## Stop conditions

Stop before impersonating real external hosts, installing test roots on non-test devices, or using production client certificates.

## Output

```text
library/platform:
intended peer identity:
trust policy:
certificate matrix:
callback/override path:
accept/reject results:
evidence status:
```
