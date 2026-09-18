# JIT Invariant Operator Runbook

Use this runbook only for local, owned, sandboxed, benchmark/CTF, simulated, or explicitly authorized runtimes. Keep the proof at deterministic semantic divergence, read-only observation, bounded assertion, synthetic marker, or reversible owner-controlled effect. Do not turn a JIT invariant review into weaponized exploitation.

## Attack surface

Map:

- runtime/build identity and flags;
- language/specification semantics;
- program/input identity and generation;
- compilation unit/function identity;
- baseline/interpreter generation;
- warmup/profile generation;
- execution tier and optimized code generations;
- optimization pipeline/pass identity;
- speculative invariants and dependencies;
- guards/checks and invalidation/watchpoints;
- OSR/inlining/specialization state;
- representation and side-effect/alias state;
- deopt triggers and frame-state metadata;
- baseline/reference results, optimized results, and downstream semantic consumers.

## Hypothesis matrix

| Hypothesis | Safe oracle | Control |
| --- | --- | --- |
| stale type/shape feedback survives transition | synthetic toy runtime emits a read-only shadow value under old feedback generation | current dependency generation invalidates and recompiles before consumer |
| range fact crosses invalidating side effect | mock optimizer fixture records an inert wrong branch/value | retained guard or dependency refresh restores baseline result |
| deopt reconstructs stale frame state | shadow frame-state consumer reports synthetic local/environment mismatch | current deopt metadata reconstructs baseline-equivalent values |
| OSR enters with stale profile generation | controlled toy program emits a bounded semantic marker only in stale OSR generation | current OSR transfer state matches baseline/reference semantics |

## Runtime/program/tier-generation trace

Record:

- runtime/build identity;
- language/specification mode;
- program/input identity/generation;
- function/compilation-unit identity;
- baseline execution generation;
- profile/warmup generation;
- tier identity/generation;
- optimized code identity/generation;
- OSR/inlining/specialization generations;
- invalidation/recompile/deopt generations.

Do not collapse repeated compilation of the same source function into one code generation.

## Feedback/speculation/dependency trace

For every speculative fact capture:

- feedback/profile identity/generation;
- speculative invariant identity;
- assumption/dependency generation;
- pass consuming the fact;
- dependency/watchpoint registration;
- guard/check identity;
- invalidation event/generation;
- optimized code generation using the fact;
- first semantic operation relying on it.

Feedback is evidence about past execution, not an authorization for future generations.

## Guard/invalidation/optimization-transform trace

Capture:

1. pre-pass IR/value state;
2. optimization pass identity;
3. assumed invariant;
4. guard/check identity;
5. dependency/watchpoint identity;
6. transformation;
7. invalidation event;
8. retirement/patch/recompile behavior;
9. next semantic operation;
10. first semantic divergence.

A removed check is not a defect if an equivalent dominating proof makes it redundant.

## OSR/inlining/specialization trace

Record:

- baseline state before OSR;
- OSR entry identity/generation;
- locals/stack/environment transferred;
- current profile generation;
- inlined callee identity/generation;
- specialization assumptions;
- dependency generations;
- exit/deopt reconstruction target.

Keep baseline entry, OSR entry, inlined frames, and deoptimized frames distinct.

## Deopt/frame-state reconstruction trace

Capture:

- deopt trigger;
- optimized code generation;
- deopt metadata/frame-state generation;
- materialization recipe;
- expected logical frame/environment;
- reconstructed value identities;
- representation conversions;
- exception/control state;
- resumed tier;
- first semantic consumer after resume.

A deopt event alone is not evidence; show incorrect reconstructed language-level state.

## Baseline/reference/semantic-consumer trace

For each controlled case record:

- deterministic baseline/reference mode;
- exact program/input generation;
- expected language-level result;
- optimized code generation;
- optimized result;
- first semantic divergence;
- downstream semantic consumer;
- effective optimized-divergence capability;
- bounded result;
- receipt/result.

Eliminate time, randomness, external state, permitted nondeterminism, undefined behavior, implementation-defined behavior, and uncontrolled concurrency.

## Controlled validation

Use:

- toy/synthetic programs;
- deterministic tier thresholds or explicit test-only optimization controls;
- mock IR/pass traces;
- synthetic feedback tables;
- shadow frame-state/value oracles;
- inert/read-only semantic consumers;
- bounded assertions or reversible owner-controlled markers.

Recommended sequence:

1. establish baseline/reference result;
2. confirm the intended optimized tier and pass;
3. capture feedback/speculation/dependency generation;
4. trigger exactly one invalidation/transition variable;
5. locate the first semantic divergence;
6. bind it to the final semantic consumer;
7. apply the minimal guard/dependency/deopt/OSR fix;
8. replay the same program/input and tier path;
9. capture deterministic before/after receipts.

## False-positive controls

Eliminate:

- specification-permitted result differences;
- undefined or implementation-defined behavior;
- input or external-state drift;
- optimizer pass not active on final trigger;
- tier fallback during minimization;
- different optimized code generation;
- concurrency/scheduling root cause;
- independent type-confusion root cause;
- independent bounds/integer root cause;
- sanitizer instrumentation changing the tier path;
- debug-only behavior;
- receipt from another execution generation.

## Counterfactual JIT controls

Hold program/input semantics fixed and change one optimizer variable:

- stale versus current feedback generation;
- dependency omitted versus registered;
- guard removed versus retained;
- stale code remains executable versus retired on invalidation;
- stale versus current OSR transfer state;
- mismatched versus current deopt frame-state metadata;
- suspect pass enabled versus disabled while keeping the remaining tier path stable.

A generic “disable optimization” comparison is a coarse control, not sufficient pass-level proof.

## Alternative explanations

Before JIT4/JIT5 explicitly reject:

- allowed language semantics;
- undefined/implementation-defined behavior;
- baseline/optimized input drift;
- changed optimization path during minimization;
- concurrency-only behavior;
- independent runtime type confusion;
- independent numeric/bounds defect;
- instrumentation-induced tier change;
- debug-only flags/assertions;
- specification-equivalent deopt state;
- unrelated compilation/execution receipt.

Any unresolved material alternative caps evidence at JIT2.

## Evidence capture

Capture one reconstructable tuple:

`runtime/build identity + language/specification semantics + program/input identity/generation + compilation unit/function identity + execution tier identity/generation + optimized code identity/generation + optimization pipeline/pass identity + feedback/profile identity/generation + speculative invariant identity + assumption/dependency generation + guard/check identity + invalidation/watchpoint identity/generation + OSR/inlining/specialization state + representation state + side-effect/alias state + deopt trigger identity + deopt metadata/frame-state generation + baseline/reference result + optimized result + first semantic divergence + downstream semantic consumer + effective optimized-divergence capability + bounded result + receipt/result`

Useful artifacts include tier/pass confirmation, mock IR deltas, feedback-generation records, dependency/watchpoint receipts, deopt frame-state snapshots, baseline/optimized result pairs, and remediation replay.

## Evidence promotion and ceiling

### JIT0 — Optimization surface mapped

Runtime/build, tiers, compilation units, feedback, optimization passes, speculative invariants, guards, invalidation, OSR/inlining, deopt, and semantic consumers are known.

### JIT1 — Tier/assumption divergence observed

A repeatable optimized-only state, feedback, dependency, guard, invalidation, OSR, or deopt divergence exists without deterministic semantic mismatch.

### JIT2 — Controlled optimization-invariant mismatch

A deterministic local fixture proves a speculative, guard, dependency, invalidation, OSR-state, or deopt-state invariant can be violated while the intended optimization path remains active.

### JIT3 — Inert semantic divergence

A read-only/mock consumer observes a deterministic wrong value, branch, stale state, or incorrect deopt reconstruction only under optimized execution while baseline/reference execution remains correct.

### JIT4 — Bounded reversible optimized effect

A synthetic canary, inert state mutation, read-only shadow result, bounded assertion, or reversible owner-controlled marker is bound to the exact optimizer causal tuple.

### JIT5 — Regression-verified causal JIT proof

JIT4 plus complete build/program/compilation provenance, first-invalid-assumption or unsound-transform trace, tier/pass confirmation, dependency/invalidation proof, deopt/OSR state where relevant, meaningful counterfactuals, eliminated alternatives, receipt/result binding, and remediation replay.

Evidence ceiling rules:

- optimization map/log only: JIT0 maximum;
- optimized-only state divergence without semantic mismatch: JIT1 maximum;
- deterministic invariant mismatch without final consumer: JIT2 maximum;
- inert/read-only semantic divergence: JIT3 maximum;
- bounded causal optimized effect: JIT4 maximum;
- complete causal proof plus regression: JIT5.

## Remediation checks

Replay the exact fixture and verify:

1. the intended optimized tier/pass still activates;
2. feedback/dependency generations are current;
3. required guards dominate their consumers;
4. invalidation retires or patches stale optimized code;
5. OSR transfers current baseline-equivalent state;
6. deopt reconstructs language-level state correctly;
7. baseline and optimized outputs reconverge;
8. positive controls still optimize and execute correctly;
9. deterministic receipts prove the change.

Prefer the smallest guard, dependency, invalidation, OSR-state, deopt-metadata, or transform fix that restores semantic equivalence.
