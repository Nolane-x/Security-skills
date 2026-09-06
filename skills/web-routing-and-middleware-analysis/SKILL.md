---
name: web-routing-and-middleware-analysis
description: "Analyze server-side routing and middleware composition: path normalization, mount scopes, auth filters, rewrites, method matching, proxy headers, error routes, and handler reachability. Use to find policy gaps caused by route interpretation differences."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Web Routing And Middleware Analysis

## When to use

Use for web frameworks, API gateways, reverse proxies, middleware stacks, route groups, rewrite engines, or applications with multiple normalization/auth layers.

## Preconditions

1. Use source plus a local/staging authorized deployment.
2. Pin framework/server/proxy versions and route configuration.
3. Use synthetic users/tenants and inert endpoints for negative controls.

## Workflow

1. Construct the effective request path from edge/proxy through normalization, rewrites, routing, middleware, controller, and downstream service.
2. Record path/method/host/header/query representations at every hop.
3. Map where authentication, authorization, CSRF/origin, tenant, and content-type policies attach relative to rewrites/mounts.
4. Test equivalent representations: encoded separators, duplicate slashes, case, suffixes, method overrides, forwarded headers, and internal rewrites only in the local deployment.
5. Compare protected and unprotected control routes to distinguish framework behavior from app configuration.
6. Route canonicalization mismatches and auth filter gaps to corresponding skills.

## Evidence contract

Record raw request, representation at each routing layer, middleware sequence, selected handler, principal, and positive/negative control. A route alias is not a bypass unless policy attachment changes.

## Stop conditions

Stop if testing targets public production endpoints, causes stateful business actions, or depends on spoofing infrastructure headers not present in the authorized topology.

## Output

```text
stack/versions:
raw request:
routing transformations:
middleware sequence:
selected handler:
principal/policy:
control matrix:
evidence status:
```
