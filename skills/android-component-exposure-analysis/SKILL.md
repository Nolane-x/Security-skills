---
name: android-component-exposure-analysis
description: "Analyze Android exported components, permissions, Binder-facing entrypoints, providers, services, receivers, and activity boundaries in an authorized app assessment. Use to distinguish intended inter-app APIs from privilege or data exposure."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Android Component Exposure Analysis

## When to use

Use when reviewing Android manifests, component registration, IPC surfaces, custom permissions, providers, bound services, broadcast receivers, or externally launchable activities.

## Preconditions

1. Use an owned test APK/source tree or an explicitly authorized application.
2. Pin app build, Android API level, signing/config variants, and test profile state.
3. Use synthetic accounts and test data; do not probe unrelated installed apps.

## Workflow

1. Inventory manifest and runtime component exposure, including explicit/implicit export rules and permission guards.
2. For each exposed component, map caller identity, required permission level, URI/intent/Binder inputs, and side effects.
3. Trace permission checks from entrypoint to sensitive operations; distinguish manifest gates from in-code authorization.
4. Review content-provider URI permissions, path grants, projection/selection handling, and caller-dependent filtering.
5. Review service/Binder methods for caller UID/package assumptions and confused-deputy behavior.
6. Test only benign cross-app calls with synthetic data and negative controls from an unauthorized test caller.
7. Route identity mismatches to authorization/confused-deputy analysis and confirmed behavior to evidence validation.

## Evidence contract

Record component, exported state, permission model, caller principal, accepted input, sensitive sink, positive/negative-control outcomes, and affected build/API level. Exported=true alone is not a vulnerability.

## Stop conditions

Stop when caller identity or permission assumptions cannot be reproduced safely, testing would touch real user data, or the component is not reachable by the stated principal.

## Output

```text
app/build/API level:
component + entrypoint:
caller principal:
manifest/runtime guards:
sensitive sink:
positive control:
negative control:
evidence status:
```
