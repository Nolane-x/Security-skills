---
name: fuzz-harness-design
description: "Engineer deterministic, high-signal fuzz harnesses for authorized local targets. Use when fuzzing is slow, unstable, blocked by startup/I/O/global state, or not reaching the intended parser, API, protocol transition, or security-sensitive logic."
metadata:
  nolane-security-category: discovery
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Fuzz Harness Design

The harness defines the experiment. A poor harness can make a strong fuzzer look weak or create false findings that never occur in the real target.

## When to use

Use before a new fuzz campaign, when coverage stalls, when crashes reproduce only inside the harness, or when setup cost dominates executions.

## Preconditions

1. Exact target function/path and realistic caller invariants are identified.
2. The harness runs only against authorized local artifacts.
3. A failure oracle and reset/cleanup strategy exist.
4. Keep a reference integration path to detect harness-only behavior.

## Workflow

1. **Choose the semantic boundary.** Invoke the smallest unit that still preserves security-relevant validation and object lifecycle.
2. **Map required context.** Global initialization, allocator, locale, feature flags, callbacks, virtual filesystem, network state, or authentication context.
3. **Separate one-time from per-input work.** Move immutable initialization out of the hot loop without accidentally reusing state that real callers reset.
4. **Define input decoding.** Raw bytes, structured tuple, multiple buffers, sequence, file tree, environment, or API operation stream.
5. **Make cleanup explicit.** Free objects, reset globals, close handles, restore transactions, clear caches, and verify no state leaks between cases.
6. **Eliminate nondeterminism.** Fix seeds/time where semantically safe; virtualize external services; avoid sleeps and uncontrolled threads.
7. **Preserve production invariants.** Do not bypass validators, constructors, or state transitions unless the research question explicitly targets internals and the limitation is documented.
8. **Add reachability assertions/counters.** Know whether the intended code and deep states are actually reached.
9. **Benchmark harness quality.** Executions/sec, stable coverage, memory growth, startup percentage, timeout rate, and control-case behavior.
10. **Cross-check with the real integration path.** Re-run minimized failures through the closest production entrypoint possible.

## Evidence contract

A harness is acceptable when it deterministically reaches the intended target, maintains required invariants, resets state, exposes a meaningful oracle, and reproduces at least one known control. Preserve harness source/config and benchmark metrics with findings.

## Stop conditions

Stop and redesign if coverage is mostly harness code, state leaks between iterations, known controls no longer behave like production, timeouts dominate, or sanitizer findings originate in harness misuse.

## Output

```text
target boundary:
production invariants preserved:
one-time init:
per-input decode:
reset/cleanup:
reachability oracle:
baseline exec/s + coverage:
known control result:
integration cross-check:
```
