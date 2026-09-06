---
name: virtual-device-model-analysis
description: "Analyze virtual device models for register/message parsing, descriptor validation, DMA/address translation, reset state, migration serialization, asynchronous callbacks, and backend trust. Use to root-cause device-emulation bugs safely."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Virtual Device Model Analysis

## When to use

Use when a guest can program emulated/paravirtual device registers, queues, descriptors, command mailboxes, DMA buffers, or migration-visible device state.

## Preconditions

1. Use an isolated VMM build with sanitizers/debug logging when possible.
2. Pin exact device model/configuration and guest driver/harness.
3. Keep host resources synthetic and disposable.

## Workflow

1. Map guest-visible registers/queues/messages to host-side handlers and state objects.
2. Trace length, offset, index, descriptor-chain, and address validation before host reads/writes.
3. Model state transitions: reset, feature negotiation, queue enable/disable, hotplug, migration, async completion.
4. Trace guest addresses through DMA/IOMMU/address-space translation and backend copies.
5. Review object lifetime across asynchronous workers/timers/completions and reset/unplug.
6. Minimize any crash to a specific device command/state sequence and classify lifetime/bounds/race/type root cause.
7. Validate only benign host control-flow or memory-safety evidence in a nested lab.

## Evidence contract

Record exact virtual device, command/register sequence, guest-controlled fields, host handler, invariant violation, minimized reproducer, and sanitizer/debug evidence. Do not infer host code execution from memory corruption.

## Stop conditions

Stop if a reproducer requires passthrough to real hardware, shared host data, or a host configuration outside the authorized lab.

## Output

```text
device/config:
guest sequence:
controlled fields:
host handler/state:
violated invariant:
minimized reproducer:
oracle:
evidence status:
```
