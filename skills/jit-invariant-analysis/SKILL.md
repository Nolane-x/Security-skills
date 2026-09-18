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

## Causal JIT-invariant model

Treat every promoted JIT finding as one causal tuple:

`runtime/build identity + language/specification semantics + program/input identity/generation + compilation unit/function identity + execution tier identity/generation + optimized code identity/generation + optimization pipeline/pass identity + feedback/profile identity/generation + speculative invariant identity + assumption/dependency generation + guard/check identity + invalidation/watchpoint identity/generation + OSR/inlining/specialization state + representation state + side-effect/alias state + deopt trigger identity + deopt metadata/frame-state generation + baseline/reference result + optimized result + first semantic divergence + downstream semantic consumer + effective optimized-divergence capability + bounded result + receipt/result`.

The proof must identify the first invalid assumption, unsound transform, missing or ineffective guard, stale dependency, incorrect OSR transfer, or incorrect deopt reconstruction and bind it to the first language-level semantic divergence.

Preserve these distinctions explicitly:

- optimized execution != optimization bug;
- baseline/optimized mismatch != JIT bug when language semantics permit the difference;
- tier activation != specific pass causality;
- optimization log != semantic divergence;
- stale feedback != harmful stale assumption;
- stale type feedback != type confusion without wrong runtime interpretation;
- stale range fact != out-of-bounds effect;
- missing guard != required guard proven absent;
- guard elimination != unsound elimination;
- deoptimization occurred != incorrect deoptimization;
- deopt metadata mismatch != wrong reconstructed state without consumer evidence;
- OSR entry != equivalent full-function entry state by assumption;
- inlining != preserved call semantics without dependency proof;
- representation transition != semantic divergence;
- same source function != same optimized code generation;
- same code address != same compilation generation;
- different machine code != different language semantics;
- debug assertion != production semantic mismatch;
- sanitizer finding != optimizer root cause;
- crash != JIT invariant violation;
- minimized trigger != same optimizer path unless tier/pass activation is preserved;
- differential mismatch != security relevance;
- wrong optimized result != arbitrary memory corruption or code execution;
- language-level undefined/implementation-defined behavior != optimizer unsoundness.

All dynamic validation remains local/owned/sandboxed or explicitly authorized. Use toy or synthetic programs, deterministic tier controls, mock IR/pass traces, shadow values, inert/read-only consumers, bounded assertions, and reversible owner-controlled markers.

## Runtime, program, tier, and compilation generations

Track independently:

- runtime/build identity and relevant flags;
- language/specification semantics;
- program/input identity/generation;
- compilation unit/function identity;
- baseline/interpreter execution generation;
- profiling/warmup generation;
- execution tier identity/generation;
- optimized code identity/generation;
- optimization pipeline/pass identity;
- OSR generation;
- inlining/specialization generation;
- invalidation/recompile generation;
- deoptimization generation.

A function optimized twice is two optimized code generations even when its source name, source bytes, or code address appears unchanged.

## Feedback, speculation, and dependency binding

For every speculative fact record:

- feedback/profile identity/generation;
- speculative invariant identity;
- assumption/dependency generation;
- optimization pass consuming the fact;
- guard/check identity;
- dependency/watchpoint registration;
- invalidation/watchpoint identity/generation;
- optimized code generation relying on the fact;
- first semantic operation that becomes invalid if the assumption is stale.

Feedback is observation, not authority. Prove which code generation consumed it and which invalidation event should have retired or constrained that code.

## Guard, invalidation, and optimization-transform binding

For each suspected optimization path capture:

1. source IR/value state;
2. optimization pipeline/pass identity;
3. speculative invariant;
4. guard/check identity;
5. dependency/watchpoint identity;
6. transformation performed;
7. invalidation event and generation;
8. retirement/patch/recompile response;
9. next semantic operation;
10. first semantic divergence.

A removed check is not evidence when an equivalent dominating condition or specification-valid invariant proves it redundant.

## OSR, inlining, and specialization binding

Bind separately:

- pre-OSR baseline state;
- OSR entry identity and generation;
- locals/stack/environment transferred;
- feedback/profile generation;
- inlined callee identity/generation;
- specialization assumptions;
- dependency generation;
- exit/deopt target.

The same source location does not imply equivalent state across baseline entry, OSR entry, inlined frames, optimized code, or deoptimized reconstruction.

## Deoptimization and frame-state reconstruction binding

For every deopt path capture:

- deopt trigger identity;
- optimized code generation;
- deopt metadata/frame-state generation;
- materialization recipe;
- expected logical frame/environment state;
- reconstructed value identities;
- representation conversions;
- exception/control state;
- resumed execution tier;
- first semantic consumer after resume.

Deoptimization occurred != incorrect deoptimization. A frame-state mismatch matters only when the reconstructed state differs from the language-level state required by baseline/reference semantics and a consumer observes that difference.

## Baseline/reference and semantic-consumer binding

Use a deterministic baseline/reference oracle and record:

- reference execution mode/build;
- exact program/input generation;
- baseline/reference result;
- optimized execution generation;
- optimized result;
- first semantic divergence;
- downstream semantic consumer;
- effective optimized-divergence capability;
- bounded result;
- receipt/result.

Eliminate allowed nondeterminism, undefined behavior, implementation-defined behavior, time, randomness, external state, and uncontrolled concurrency before promoting a differential mismatch.

## JIT-invariant evidence ladder

Use JIT0–JIT5 exactly:

- **JIT0 — Optimization surface mapped.** Runtime/build, tiers, compilation units, feedback, optimization passes, speculative invariants, guards, invalidation, OSR/inlining, deopt, and semantic consumers are identified.
- **JIT1 — Tier/assumption divergence observed.** A repeatable optimized-only state, feedback, dependency, guard, invalidation, OSR, or deopt divergence exists without a deterministic semantic mismatch.
- **JIT2 — Controlled optimization-invariant mismatch.** A deterministic local fixture proves a documented speculative, guard, dependency, invalidation, OSR-state, or deopt-state invariant can be violated while preserving the intended optimization path.
- **JIT3 — Inert semantic divergence.** Optimized execution produces a deterministic wrong value, wrong branch, stale logical state, or incorrect deopt reconstruction observed by a read-only/mock semantic consumer while baseline/reference execution remains correct.
- **JIT4 — Bounded reversible optimized effect.** A synthetic canary, inert state mutation, read-only shadow result, bounded assertion, or reversible owner-controlled marker is causally bound to the exact program/tier/code/pass/assumption/guard/deopt/consumer tuple.
- **JIT5 — Regression-verified causal JIT proof.** JIT4 plus complete build/program/compilation provenance, first-invalid-assumption or first-unsound-transform trace, tier/pass confirmation, dependency/invalidation proof, deopt/OSR state where relevant, meaningful counterfactuals, eliminated alternative explanations, receipt/result binding, and remediation replay.

Crashes, assertions, sanitizer reports, optimization logs, different machine code, stale-looking feedback, or synthetic markers cannot skip missing causal bindings.

## Counterfactual JIT controls

Hold language-level program/input semantics constant and change one optimizer variable:

- current versus stale feedback generation;
- dependency registered versus omitted;
- required guard retained versus removed;
- invalidation retires old code versus old code remains executable;
- current versus stale OSR state generation;
- correct versus mismatched deopt frame-state metadata;
- suspect optimization pass enabled versus disabled while preserving all other relevant tiers.

Disabling all optimization is useful as a coarse control but does not by itself establish pass-level causality.

## Alternative explanations

Before JIT4 or JIT5 reject:

- language semantics permit both results;
- undefined or implementation-defined behavior exists;
- baseline and optimized runs used different input or external state;
- tier/pass activation changed during minimization;
- the suspected pass did not execute on the final trigger;
- concurrency or scheduling explains the result;
- independent runtime type confusion explains the consumer mismatch;
- independent bounds/integer arithmetic explains the result;
- sanitizer instrumentation changes the optimization path;
- debug-only flags or assertions create the divergence;
- deoptimization resumed a specification-equivalent state;
- the receipt belongs to another compilation/execution generation.

Any unresolved material alternative caps evidence at JIT2.

Keep live runtime type-identity confusion with `type-confusion-analysis`, arithmetic/range/object-size proof with `bounds-and-integer-analysis`, unsafe interleavings with `concurrency-race-analysis`, generic discovery with `differential-testing`, and instrumentation evidence with `sanitizer-guided-memory-analysis`.

## Evidence ceiling

Apply the narrowest supported level:

- optimization surface or logs only: JIT0 maximum;
- tier/feedback/dependency divergence without semantic mismatch: JIT1 maximum;
- deterministic optimization-invariant mismatch without final semantic consumer: JIT2 maximum;
- inert/read-only optimized semantic divergence: JIT3 maximum;
- bounded causally bound optimized effect: JIT4 maximum;
- only complete compilation/tier/pass/dependency/deopt provenance, counterfactuals, receipts, and remediation replay reaches JIT5.

Do not promote crashes, assertions, sanitizer reports, stale feedback, deopt events, or different machine code into stronger JIT claims without the missing causal bindings.

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
