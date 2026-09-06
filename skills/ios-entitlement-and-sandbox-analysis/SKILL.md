---
name: ios-entitlement-and-sandbox-analysis
description: "Analyze iOS application entitlements, sandbox containers, app groups, keychain access groups, extensions, XPC boundaries, and capability inheritance in an authorized build. Use to identify cross-process/container trust mistakes."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Ios Entitlement And Sandbox Analysis

## When to use

Use when reviewing iOS/macOS-mobile-style entitlements, app groups, extensions, keychain groups, URL/file sharing, XPC services, or privileged capabilities.

## Preconditions

1. Use an owned/authorized signed build and test device/simulator profile.
2. Pin provisioning profile, entitlements, OS version, and extension set.
3. Use synthetic data in shared containers/keychain groups.

## Workflow

1. Extract effective entitlements from the signed product and compare them with source/build configuration.
2. Map each entitlement to concrete container, service, extension, or keychain access it enables.
3. Enumerate app-group/shared-container producers and consumers and their trust assumptions.
4. Map extension/XPC messages and whether caller identity, audit token, or entitlement checks protect sensitive operations.
5. Review file-protection class and lock-state assumptions for data in shared containers.
6. Use benign companion test components only where explicitly authorized to test positive/negative access.
7. Route deputy/authorization issues to the corresponding trust skills.

## Evidence contract

Record effective entitlement, principal/process, resource namespace, expected policy, observed access, and negative-control result. Entitlement presence alone is not a bug.

## Stop conditions

Stop if testing requires unauthorized signing identities, jailbreak-only bypasses outside scope, or access to another developer/team’s resources.

## Output

```text
build/OS/profile:
effective entitlements:
principal/process:
shared resource:
identity/policy check:
control results:
evidence status:
```
