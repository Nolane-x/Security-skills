---
name: driver-ioctl-surface-analysis
description: "Analyze device-control and IOCTL-style interfaces in authorized kernel/driver labs, including request schemas, buffer methods, length validation, object handles, privilege checks, asynchronous completion, and user/kernel trust transitions. Use for Windows/Linux/embedded drivers and device services."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Driver IOCTL Surface Analysis

An IOCTL or device-control surface is an RPC interface into privileged code. Treat each command as a schema plus authorization and lifetime contract.

## When to use

Use for ioctl/device-control dispatchers, char devices, Windows IRP/IOCTL handlers, firmware control paths, vendor kernel modules, or privileged user-mode device brokers.

## Preconditions

Use only owned/sandboxed test machines, VMs, or explicitly authorized hardware. Snapshot state and avoid commands that can physically alter devices unless a safe simulator/test mode exists.

## Workflow

1. **Enumerate command numbers/selectors.** Include private/vendor ranges and versioned structures.
2. **Map request transport.** Buffered/direct/neither-style I/O, user pointer, shared buffer, mmap region, nested pointers.
3. **Model schema per command.** Minimum/maximum input/output sizes, versions, flags, unions, arrays, embedded lengths.
4. **Check principal gate.** Device ACL, capability, group, token, handle creation policy, namespace exposure.
5. **Trace length and pointer validation.** Probe/copy timing, integer conversions, output size assumptions, nested buffer ownership.
6. **Trace object handles/ids.** Lookup lifetime, type validation, cross-process ownership, stale id reuse.
7. **Inspect async/cancel paths.** Completion after close/unload, cancel races, pending request lifetime.
8. **Inspect global/device state transitions.** Setup/start/stop/reset and per-handle versus global state confusion.
9. **Build benign boundary tests** for schema and authorization; use kernel sanitizers/verifier diagnostics in the lab.
10. **Search sibling commands** sharing parsing helpers, object tables, or copy routines.

## Evidence contract

For each candidate record command id, caller privilege, exact schema, buffer transfer method, validation path, privileged sink or invalid access, and controls. An exposed IOCTL is not itself a vulnerability.

## Stop conditions

Stop if a command can damage real hardware/data and no safe test fixture exists, if caller privilege already fully authorizes the effect under documented policy, or if the request schema cannot be established reliably.

## Output

```text
driver/device:
command:
caller gate:
I/O transfer method:
request schema:
length/pointer/object checks:
async/lifetime behavior:
observed issue:
controls:
related command variants:
```
