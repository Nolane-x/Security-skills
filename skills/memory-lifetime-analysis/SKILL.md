---
name: memory-lifetime-analysis
description: "Analyze ownership, aliasing, allocation, destruction, reuse, callbacks, and asynchronous lifetime boundaries in authorized code or crash evidence. Use for suspected use-after-free, double free, stale handles, iterator invalidation, refcount mistakes, or teardown races."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Memory Lifetime Analysis

Model object lifetime as a timeline of authority over one logical resource. The important question is not merely “where was it freed?” but which alias remained trusted after the lifetime invariant ended.

## When to use

Use when a pointer, handle, reference, callback context, iterator, future/promise state, or refcounted object may outlive its owner or be released more than once.

## Preconditions

All dynamic testing must stay on local, owned, sandboxed, or explicitly authorized targets. Pin the build and identify the object/resource type whose lifetime is in question.

## Workflow

1. **Name the object identity.** Separate logical object identity from reused address/handle values.
2. **List constructors and acquisition paths.** Allocation, open, map, retain, borrow, cache lookup, registration, callback capture.
3. **List release paths.** Free, close, unmap, decrement, cancellation, error cleanup, shutdown, container removal.
4. **Map aliases.** Owners, borrowed references, weak references, indexes, callbacks, global caches, thread-local state, queued work.
5. **Write the expected lifetime invariant.** Which event invalidates which aliases, and who is responsible for clearing or fencing them?
6. **Trace exceptional paths.** Partial construction, retry, early return, timeout, cancellation, double error handling, shutdown ordering.
7. **Check address reuse separately from stale identity.** Reuse can make a stale pointer appear valid while referring to a different logical object.
8. **Inspect refcount transitions.** Underflow, missing retain, duplicated release, cycle break, resurrection, non-atomic updates.
9. **Test concurrency edges.** Destruction racing with callback, iteration, I/O completion, or worker handoff.
10. **Validate with timeline evidence.** Sanitizer origin/free/access stacks, deterministic logging, assertions, or a minimal local reproducer.
11. **Search siblings.** Other object classes using the same ownership helper or cleanup pattern may share the invariant defect.

## Evidence contract

Preserve an object-lifetime timeline with creation, aliases, invalidation, release, stale use, and the exact condition that permits the stale alias. Address reuse alone is not proof; demonstrate that a logically dead reference is consumed or released incorrectly.

## Stop conditions

Stop when the suspected alias is actually retained by contract, sanitizer instrumentation changes the relevant lifetime semantics, the reproducer depends on harness-only ownership mistakes, or target scope is unauthorized.

## Output

```text
object/resource:
owner(s):
aliases:
creation/acquisition:
invalidation event:
release paths:
stale/double-use path:
concurrency/error-path role:
evidence:
variant candidates:
```
