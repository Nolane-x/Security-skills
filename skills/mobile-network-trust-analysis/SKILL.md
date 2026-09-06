---
name: mobile-network-trust-analysis
description: "Analyze mobile transport trust: endpoint selection, TLS/certificate policy, network security configuration, proxy/VPN assumptions, token binding, offline queues, and debug overrides. Use to separate transport misconfiguration from server authorization issues."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Mobile Network Trust Analysis

## When to use

Use for Android/iOS clients that call APIs, use custom trust managers/delegates, pin certificates/keys, allow cleartext, ship debug CAs, or queue sensitive requests.

## Preconditions

1. Use an owned test backend or local interception endpoint with synthetic accounts.
2. Pin app build, OS network configuration, endpoint environment, and certificate chain.
3. Do not intercept unrelated user/device traffic.

## Workflow

1. Inventory endpoints, schemes, trust stores, platform network-security policies, pinning rules, debug overrides, and fallback transports.
2. Trace hostname and certificate validation decisions, including redirects and alternate endpoints.
3. Map bearer/session material to transport channels and whether replay is possible outside intended context.
4. Review cleartext/debug/proxy exceptions and whether production builds can activate them.
5. Test with controlled valid, wrong-host, untrusted, expired, and redirected certificates/endpoints as safe negative controls.
6. Separate client transport acceptance from server-side authorization; route token lifecycle findings to secrets/token analysis.

## Evidence contract

Record endpoint, trust policy, build/config state, synthetic certificate condition, observed connection result, and whether sensitive material/action was exposed. A disabled pin alone is not necessarily a vulnerability if platform validation remains correct.

## Stop conditions

Stop if reproduction requires intercepting third-party traffic, real credentials, or weakening trust on a device used by non-test users.

## Output

```text
app/build/OS:
endpoint:
trust policy:
certificate/hostname condition:
token exposure/replay context:
control matrix:
evidence status:
```
