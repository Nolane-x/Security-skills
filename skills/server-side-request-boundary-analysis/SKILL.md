---
name: server-side-request-boundary-analysis
description: "Analyze server-side outbound request features for destination parsing, DNS/address resolution, redirect policy, scheme support, proxy use, credential forwarding, and network trust zones. Use to assess SSRF-like boundaries without scanning internal networks."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Server Side Request Boundary Analysis

Perform any dynamic validation only in an authorized, owned lab or equivalent explicitly scoped test environment.

## When to use

Use when an application fetches user-influenced URLs, webhooks, images, imports, callbacks, redirects, repository/package sources, or metadata from remote endpoints.

## Preconditions

1. Use a controlled callback server and synthetic internal-style endpoints.
2. Do not probe real internal/cloud metadata services or third-party networks.
3. Pin resolver/proxy/container network configuration.

## Workflow

1. Trace user-controlled URL/host/scheme fields to URL parser, allow/deny logic, DNS resolution, connection creation, redirects, and credential/header attachment.
2. Record normalization differences between validation parser and network client.
3. Model hostname-to-address changes, redirect targets, IPv4/IPv6 forms, proxy routing, and scheme transitions using controlled addresses only.
4. Check whether destination policy is re-evaluated after DNS and every redirect.
5. Use local loopback/mock services to prove reachability classes without scanning.
6. Separate network reachability from sensitive-data access; require a benign protected mock endpoint to show security consequence.

## Evidence contract

Record controlled input, parsed destination, resolution, redirect chain, final socket target, forwarded credentials/headers, and mock protected-resource outcome. “Server made a request” alone is only observed reachability.

## Stop conditions

Stop before contacting real internal/admin/metadata endpoints, enumerating network ranges, or forwarding real production credentials.

## Output

```text
feature/entrypoint:
controlled URL fields:
validation parser:
resolution/redirect policy:
final controlled endpoint:
credential forwarding:
mock protected outcome:
evidence status:
```
