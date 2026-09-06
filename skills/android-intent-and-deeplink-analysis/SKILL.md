---
name: android-intent-and-deeplink-analysis
description: "Analyze Android intents, app links, deep links, task/URI routing, and cross-component parameter trust. Use to find routing confusion, unsafe forwarding, validation gaps, and privilege changes without treating every deep link as exploitable."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Android Intent And Deeplink Analysis

## When to use

Use when an Android app accepts custom schemes, verified app links, implicit intents, nested intents, redirect parameters, file/content URIs, or forwards intents between components.

## Preconditions

1. Use an authorized app and controlled emulator/device.
2. Document verified-domain state, installed competing handlers, launch mode/task configuration, and login state.
3. Use inert target activities and synthetic URIs for tests.

## Workflow

1. Enumerate intent filters, schemes, hosts, paths, categories, extras, nested intents, and URI-bearing fields.
2. Map who can originate each route and which component ultimately consumes the data.
3. Trace normalization/allowlist decisions across every forwarding hop rather than validating only the first URI.
4. Check whether nested intents or redirect targets can select privileged/internal components.
5. Model task/back-stack and authentication assumptions where state changes across launches.
6. Run benign positive and negative controls for allowed versus disallowed destinations/parameters.
7. Route namespace issues to canonicalization analysis and authorization changes to authorization-boundary analysis.

## Evidence contract

A finding requires a concrete attacker-controlled routing field, a validation/forwarding mismatch, and a benign observable consequence under pinned state. A custom scheme by itself is only attack surface.

## Stop conditions

Stop if test routing could launch third-party apps, cause real transactions, or depends on unverifiable production-domain ownership.

## Output

```text
route/filter:
origin principal:
controlled fields:
normalization/allowlist logic:
forwarding hops:
state assumptions:
control results:
evidence status:
```
