---
name: ios-url-scheme-and-universal-link-analysis
description: "Analyze iOS URL schemes, universal links, scene/application routing, redirect handling, handoff, and cross-app identity assumptions. Use to test routing and authorization safely with synthetic destinations."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Ios Url Scheme And Universal Link Analysis

## When to use

Use when iOS apps consume custom URL schemes, universal links, callback URLs, authentication redirects, Handoff activities, or app-to-app routing parameters.

## Preconditions

1. Use controlled domains/schemes and an authorized build.
2. Pin associated-domains entitlement, AASA content/state, OS version, and installed test handlers.
3. Use synthetic callback tokens and inert destinations.

## Workflow

1. Enumerate registered schemes, universal-link domains/path rules, scene/app delegate handlers, and callback parameters.
2. Map source principal and destination handler for every route, including fallbacks between web and app.
3. Trace normalization, host/path allowlists, percent-decoding, and redirect/return URL validation.
4. Check whether security decisions bind to the verified universal-link origin or merely a caller-provided URL/string.
5. Test custom-scheme collision/handler ambiguity only with controlled companion apps.
6. Use positive and negative controls for allowed versus disallowed hosts/paths/callbacks.

## Evidence contract

Record registration/association state, controlled routing input, normalization path, destination, security-sensitive action, and controls. Do not treat custom-scheme registration as account takeover without an actual state/token consequence.

## Stop conditions

Stop if testing would intercept third-party callbacks, real OAuth codes, or production universal links outside authorization.

## Output

```text
scheme/domain:
association state:
source principal:
controlled parameters:
normalization/validation:
destination action:
control results:
evidence status:
```
