---
name: sanitizer-guided-memory-analysis
description: "Interpret AddressSanitizer, UndefinedBehaviorSanitizer, MemorySanitizer, ThreadSanitizer, allocator diagnostics, and related runtime evidence for an authorized target. Use when a crash or invariant violation may involve memory lifetime, bounds, initialization, integer-driven sizing, or concurrency."
metadata:
  nolane-security-category: verification
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Sanitizer-Guided Memory Analysis

Treat sanitizer output as a structured observation about program state, not as a vulnerability verdict. Separate the first invalid operation from downstream damage and preserve the exact build that produced the signal.

## When to use

Use when runtime instrumentation reports memory or undefined-behavior evidence, or when an unexplained crash needs a stronger oracle than exit status alone.

## Preconditions

1. The target is local, owned, sandboxed, benchmark/CTF, or explicitly authorized.
2. Record compiler, sanitizer set, optimization level, allocator, architecture, and target revision.
3. Reproduce with symbols where possible and retain the original unsanitized behavior for comparison.
4. Do not infer exploitability solely from a sanitizer class or severity label.

## Workflow

1. **Capture the first report.** Preserve the complete first diagnostic, stack, register/context information, input, stderr, and target hash before retries mutate state.
2. **Classify the invalid operation.** Distinguish read/write, use-after-free, double free, stack/heap/global bounds, uninitialized use, signed/unsigned overflow, shift, alignment, race, or allocator invariant failure.
3. **Locate origin versus manifestation.** Identify where the invalid value/object state was created, where it became stale or out-of-range, and where the runtime finally detected it.
4. **Build an ownership timeline.** For lifetime failures, reconstruct allocation/creation, aliases, ownership transfer, release, reuse, and invalid access.
5. **Build a bounds equation.** For spatial failures, write the intended object size, index/offset expression, integer widths, conversions, and actual access width.
6. **Check sanitizer sensitivity.** Note redzones, quarantine, allocator replacement, timing changes, or race instrumentation that may alter layout or schedule.
7. **Minimize without changing the failure class.** Reduce the reproducer while checking that the same invalid operation and root causal path remain.
8. **Run controls.** Compare sanitizer-on/off, optimization levels, patched/unpatched versions, and at least one non-triggering near-neighbor input.
9. **Map impact primitives conservatively.** Record observable corruption properties—attacker-controlled data, direction, size, repeatability, object type—without converting the analysis into weaponization steps.
10. Route causal findings to evidence-driven-vulnerability-validation and remediation-and-regression.

## Evidence contract

A strong result preserves the exact diagnostic, target/build identity, minimized reproducer, first-invalid-operation stack, origin stack when available, ownership/bounds reasoning, reproduction rate, and control results. A sanitizer report alone establishes an observed runtime fault, not reachability in another product and not practical exploitability.

## Stop conditions

Stop or downgrade the claim when the signal disappears under a faithful rebuild, only appears after changing target semantics, stacks are dominated by harness misuse, the first report cannot be separated from cascading corruption, or authorization boundaries are unclear.

## Output

Report:

```text
target/build:
sanitisers + compiler flags:
minimized reproducer:
first invalid operation:
origin/lifetime or bounds timeline:
attacker influence observed:
reproduction rate:
controls:
confidence:
next validation step:
```
