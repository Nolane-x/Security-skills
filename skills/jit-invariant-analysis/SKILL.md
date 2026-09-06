---
name: jit-invariant-analysis
description: "Analyze interpreter/JIT/compiler optimization invariants in an authorized local runtime using tier transitions, speculative assumptions, representation/type feedback, deoptimization, bounds reasoning, and differential execution. Use when optimized execution may diverge from interpreter/baseline semantics or trust stale type/range facts."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# JIT Invariant Analysis

JIT analysis is semantic-invariant analysis. Focus on where optimization assumes a fact, what invalidates that fact, and whether deoptimization or guards restore correctness.

## When to use

Use for JavaScript/Wasm runtimes, JVM/.NET-style JITs, dynamic-language optimizing compilers, shader/compiler pipelines, or tiered execution engines.

## Preconditions

Use only local/owned/sandboxed runtimes or explicitly authorized builds. Keep proofs at semantic divergence, assertion, sanitizer, or benign marker level; do not develop weaponized exploit chains.

## Workflow

1. **Establish baseline semantics.** Interpreter/reference result for the minimized program/input.
2. **Map tiers and trigger conditions.** Warmup count, profile feedback, optimization threshold, OSR, inlining, specialization.
3. **List speculative facts.** Type/shape, range, aliasing, length, prototype/class stability, side-effect freedom, escape status.
4. **Locate guards and invalidation.** Check, dependency registration, watchpoint, deopt trigger, class transition, bounds guard.
5. **Model representation transitions.** Tagged/unboxed values, integer/double, compressed pointers, object layouts, Wasm/native boundaries.
6. **Compare optimized versus baseline execution** using differential-testing and deterministic tier controls.
7. **Minimize while preserving optimization.** Ensure reduction does not silently fall back to baseline tier.
8. **Trace first semantic divergence.** Wrong value, omitted check, stale type, impossible-path assumption, incorrect deopt state.
9. **Use runtime assertions/sanitizers** to strengthen causal evidence.
10. **Search optimization siblings** that consume the same range/type analysis fact.

## Evidence contract

Show baseline result, optimized result, tier/optimization confirmation, speculative invariant, invalidation/guard gap, minimized trigger, and control disabling the optimization or restoring the guard. A crash only in a custom debug build is evidence of a candidate, not automatically production impact.

## Stop conditions

Stop when the program relies on language-level undefined/implementation-defined behavior, tier activation cannot be confirmed, differential result is allowed by specification, or analysis would move into weaponized exploitation.

## Output

```text
runtime/build:
baseline semantics:
optimized tier confirmed:
speculative invariant:
guard/invalidation:
first divergence:
minimized trigger:
optimization-disabled control:
production relevance:
variant optimization passes:
```
