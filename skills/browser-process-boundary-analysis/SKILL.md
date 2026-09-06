---
name: browser-process-boundary-analysis
description: "Analyze modern multi-process browser security boundaries in an authorized local build: renderer, browser, GPU, network, utility, extension, site isolation, IPC serialization, object routing, and brokered capabilities. Use for browser security review without assuming a renderer bug automatically becomes a sandbox escape."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Browser Process Boundary Analysis

Treat browser security as multiple chained boundaries. A renderer memory bug, IPC validation bug, privileged-service bug, and browser-process authorization flaw are distinct findings unless evidence connects them.

## When to use

Use for browser engines, Electron-like shells, embedded webviews, site-isolated renderers, privileged utility services, extension/native messaging, or browser IPC reviews.

## Preconditions

Use local instrumented builds/profiles or explicitly authorized test environments. Never test real users/sites; use synthetic origins and benign marker resources.

## Workflow

1. **Map process graph.** Browser, renderer, GPU, network, audio/video, storage, extension, crash/updater, platform brokers.
2. **Record privilege/sandbox profile per process.** OS token, namespaces, filesystem/device/network capability.
3. **Map IPC channels and generated schemas.** Message ids, object routing, handles, shared buffers, sequencing, associated interfaces.
4. **Identify renderer-controlled fields** consumed by more privileged processes.
5. **Check message/state validation.** Object ownership, frame/origin/site binding, lifecycle generation, size/type checks, sequence legality.
6. **Check shared memory/command buffers.** Bounds, versioning, producer/consumer trust, stale mappings.
7. **Check origin/security-context propagation.** Which process makes the final policy decision and on what identity?
8. **Check privileged service parsers** separately with sanitizer/static techniques.
9. **Validate process-boundary effects** with a synthetic capability/marker and negative origin/process controls.
10. **Document chain assumptions explicitly.** Never collapse “renderer reachable” into “browser compromise.”

## Evidence contract

Preserve process roles, sandbox profiles, IPC schema/path, attacker-controlled field/state, privileged consumer, violated invariant, benign effect, and controls. Every chain hop requires independent evidence.

## Stop conditions

Stop when process topology/profile differs from the claimed release, a finding requires enabling debug-only privileged interfaces, or proof would require unsafe host-level actions.

## Output

```text
browser/build:
process graph:
origin/process attacker position:
IPC/shared boundary:
privileged consumer:
validation/identity invariant:
benign cross-boundary effect:
controls:
chain hops proven/unproven:
```
