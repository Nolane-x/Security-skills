---
name: reproduction-environment-capture
description: "Capture the minimum environment needed to reproduce a security observation: target revision/hash, dependencies, build flags, platform, mitigations, configuration, data fixtures, service topology, timing/state, and reset procedure. Use before evidence is handed off."
metadata:
  nolane-security-category: orchestration
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Reproduction Environment Capture

Perform dynamic or intrusive validation only in an authorized, owned lab or equivalent explicitly scoped test environment.

## When to use

Use as soon as a candidate behavior depends on build flags, OS/runtime versions, services, feature flags, device models, heap/timing state, or external dependencies.

## Preconditions

1. Capture only authorized/non-sensitive environment data.
2. Prefer hashes/version identifiers over copying proprietary binaries/configs.
3. Know how to reset the lab to a clean state.

## Workflow

1. Pin target source commit/tag and binary/artifact digest; note whether symbols/patches differ from upstream.
2. Capture compiler/interpreter/runtime versions, important build flags, sanitizers and security mitigations.
3. Capture OS/kernel/architecture, container/VM/device model and relevant resource limits.
4. Capture feature flags, permissions, network/service topology and synthetic external dependencies.
5. Identify fixture digests and state prerequisites such as cache/database contents, heap-shaping retries, login/tenant role, or protocol phase.
6. Write a reset/setup sequence and verify a fresh environment can reach the baseline positive control.
7. Separate essential reproducer requirements from incidental workstation details.

## Evidence contract

Another authorized environment should be able to recreate the observation or explain a concrete remaining mismatch from the captured variables.

## Stop conditions

Stop evidence promotion if the observation cannot be tied to a target revision/artifact, reset state is unknown, or reproduction depends on unrecorded production data.

## Output

```text
target revision/hash:
build/runtime:
platform/mitigations:
config/feature flags:
topology/dependencies:
fixture digests:
state/timing prerequisites:
reset/setup:
baseline control:
```
