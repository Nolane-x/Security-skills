---
name: hypervisor-shared-memory-analysis
description: "Analyze guest-host shared-memory and ring protocols for ownership, lifetime, index arithmetic, ordering, fencing, grant/map revocation, and cross-domain validation. Use for virtqueues, grants, shared pages, doorbells, and memory-backed IPC."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Hypervisor Shared Memory Analysis

Perform any dynamic validation only in an authorized, owned lab or equivalent explicitly scoped test environment.

## When to use

Use when host and guest communicate through shared pages, rings, descriptors, grant tables, memory slots, event channels, or mapped buffers.

## Preconditions

1. Use a disposable isolated guest/host pair.
2. Pin shared-memory protocol version, negotiated features, page/grant layout, and concurrency model.
3. Use synthetic buffer contents and addresses.

## Workflow

1. Define ownership of each shared field/buffer at every protocol state.
2. Trace producer/consumer indices with wraparound, width conversion, bounds, and monotonicity assumptions.
3. Map memory-order/fence requirements and which side may observe partially updated descriptors.
4. Model revocation/unmap/reset while asynchronous host or guest work still references shared memory.
5. Review validation of lengths, segment counts, page offsets, indirect descriptors, and nested tables.
6. Stress safe concurrency/state transitions with benign buffers and use race/memory sanitizers where available.
7. Route concrete invariant failures to bounds/lifetime/concurrency analysis.

## Evidence contract

Evidence must identify the shared field/buffer, ownership state, ordering/lifetime invariant, exact transition causing violation, and host/guest observable result. A malformed ring entry alone is not a host compromise.

## Stop conditions

Stop if shared memory maps real host devices/files, testing can corrupt non-lab guests, or concurrency cannot be contained/recovered.

## Output

```text
protocol/shared object:
ownership states:
indices/lengths:
ordering/fences:
revocation/reset path:
violated invariant:
oracle:
evidence status:
```
