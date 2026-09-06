---
name: concurrency-race-analysis
description: "Analyze interleavings, shared-state invariants, atomicity, lock coverage, cancellation, publication, teardown, and time-of-check/time-of-use behavior in authorized code. Use for race conditions, double actions, stale state, UAF races, authorization TOCTOU, or non-deterministic corruption."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Concurrency and Race Analysis

A race is security-relevant when an unsafe interleaving violates an invariant that sequential executions preserve. Describe the smallest happens-before relationship needed to prevent it.

## When to use

Use when a failure is timing-sensitive, thread/task dependent, cancellation-related, or involves separately checked and used shared state.

## Preconditions

Only stress authorized local/owned/sandboxed systems. Record thread/task model, scheduler/runtime, synchronization primitives, and whether instrumentation changes timing substantially.

## Workflow

1. **Name shared state and invariant.** Object lifetime, authorization state, uniqueness, queue membership, refcount, transaction phase, file/path identity.
2. **List actors.** Threads, processes, callbacks, signals, async tasks, interrupts, workers, external state changers.
3. **Map synchronization.** Locks, atomics/orderings, fences, channels, event loops, transactions, refcounts, epochs.
4. **Write candidate interleaving.** A1 → B1 → A2 with the exact gap that breaks the invariant.
5. **Distinguish data race from higher-level race.** Atomic memory accesses can still form an unsafe check/use sequence.
6. **Inspect cancellation/error teardown.** Concurrent abort and completion paths often duplicate release or action.
7. **Check publication.** Is a partially initialized or already-retired object visible to another actor?
8. **Amplify deterministically where possible.** Test hooks, barriers, controlled delays, repeated lab runs, or schedule tracing rather than uncontrolled production load.
9. **Run near-neighbor controls.** Add the missing ordering or disable one actor and confirm the failure disappears.
10. **State the minimal synchronization/invariant fix**, not merely “add a lock.”

## Evidence contract

Provide the shared invariant, actors, candidate interleaving, synchronization gap, reproducibility strategy, observed violation, and control. ThreadSanitizer output helps but does not replace higher-level invariant reasoning.

## Stop conditions

Stop if the interleaving is impossible under the documented memory/order model, the only reproducer relies on instrumentation-only timing, stress would affect systems outside scope, or the suspected state is not actually shared.

## Output

```text
shared invariant:
actors:
existing synchronization:
minimal bad interleaving:
observed effect:
reproduction/amplification:
control:
minimal ordering needed:
related lifetime/auth implications:
```
