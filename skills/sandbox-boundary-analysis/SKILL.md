---
name: sandbox-boundary-analysis
description: "Analyze sandbox, broker, renderer/worker, plugin, container-like, or restricted-process boundaries in an authorized environment. Use to map privileged broker APIs, shared resources, namespace exposure, capability leaks, confused-deputy paths, and assumptions required for a sandbox escape claim."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Sandbox Boundary Analysis

A sandbox is a set of denied capabilities plus explicitly brokered exceptions. Analyze the exceptions first: every broker, inherited handle, shared mapping, namespace object, and privileged helper is part of the boundary.

## When to use

Use for browser renderers, document/media sandboxes, plugin workers, build sandboxes, mobile app sandboxes, restricted tokens, seccomp/capability profiles, or brokered file/device/network access.

## Preconditions

All tests stay on owned/local/sandboxed targets or explicit authorization. Use benign boundary proofs such as access to a synthetic broker resource; do not pursue persistence or host compromise.

## Workflow

1. **Define sandboxed principal and threat model.** Starting privileges, assumed code execution inside sandbox, assets outside.
2. **Enumerate broker interfaces.** IPC methods, file chooser/broker, network service, GPU/media service, font/printing, updater, crash service.
3. **Enumerate inherited capabilities.** Handles/fds, shared memory, environment, namespace membership, device access, tokens, sockets.
4. **Map policy enforcement layers.** OS sandbox, broker authorization, path filters, object capabilities, seccomp/syscall policy.
5. **Check identity binding.** Broker must bind request to the sandboxed caller/session and intended resource.
6. **Check resource naming/canonicalization.** Path/namespace aliases can undermine broker filters.
7. **Check shared-memory/state validation.** Lengths, object ids, ring buffers, command streams, generation counters.
8. **Check privileged service parser surfaces.** Compromise of a broker/service may be a separate boundary step; validate independently.
9. **Demonstrate only benign boundary crossing** to a synthetic asset if needed for validation.
10. **Separate primitive from complete escape.** A broker logic flaw may broaden capability without constituting arbitrary host execution.

## Evidence contract

State sandbox assumptions, denied capability, broker/inherited path, caller identity, policy check, benign external asset reached, and controls. “Process outside sandbox crashed” is not an escape unless causally tied to attacker-controlled sandbox input and a security boundary effect.

## Stop conditions

Stop if proof requires destructive host actions, the assumed in-sandbox capability is not part of the threat model, or the tested service runs with no privilege/capability advantage over the sandboxed process.

## Output

```text
sandbox principal:
assumed starting capability:
asset/boundary:
broker/inherited surfaces:
policy layers:
identity/resource binding:
benign crossed capability:
controls:
primitive vs complete escape gap:
```
