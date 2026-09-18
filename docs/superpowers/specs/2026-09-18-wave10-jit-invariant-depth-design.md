# Wave 10 Profile #32 — JIT Invariant Causal Depth Design

**Date:** 2026-09-18  
**Base authority:** `main@67c9fd9df58ed4ff5ecca365a9fe83a5fe17d87a`  
**Canonical skill:** `jit-invariant-analysis`

## Purpose

Promote `jit-invariant-analysis` into the thirty-second CI-enforced operator-depth profile without changing routing, graph, packs, benchmark authority, agent-eval authority, superiority-court authority, or workflow semantics.

The current skill already asks for baseline semantics, tier confirmation, speculative facts, guards/invalidation, representation transitions, differential execution, first divergence, and optimization controls. The missing contract is causal identity across compilation generations: exactly which runtime/build, source program/input generation, compilation unit, tier/code generation, feedback generation, optimization pass, speculative assumption, guard/dependency, invalidation/watchpoint, OSR/inlining state, and deoptimization frame state produced the first semantic divergence and which downstream semantic consumer observed it.

## Causal model

Every promoted finding must bind one reconstructable tuple:

`runtime/build identity + language/specification semantics + program/input identity/generation + compilation unit/function identity + execution tier identity/generation + optimized code identity/generation + optimization pipeline/pass identity + feedback/profile identity/generation + speculative invariant identity + assumption/dependency generation + guard/check identity + invalidation/watchpoint identity/generation + OSR/inlining/specialization state + representation state + side-effect/alias state + deopt trigger identity + deopt metadata/frame-state generation + baseline/reference result + optimized result + first semantic divergence + downstream semantic consumer + effective optimized-divergence capability + bounded result + receipt/result`

The proof must identify the first invalid speculative assumption, missing/ineffective guard, stale dependency, incorrect optimization transform, or incorrect deoptimization reconstruction. A later wrong value or crash does not replace the missing optimizer-state provenance.

## Required distinctions

Freeze these non-equivalences:

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

## Runtime, program, tier, and compilation generations

Track independently:

- runtime/build identity and relevant flags;
- language/specification mode;
- program/input identity and generation;
- function/compilation-unit identity;
- baseline/interpreter execution generation;
- profiling/warmup generation;
- tier identity and tier generation;
- optimized code identity and generation;
- optimization pipeline/pass identity;
- OSR entry and OSR generation;
- inlining/specialization generation;
- invalidation/recompile generation;
- deoptimization generation.

A function optimized twice is two code generations even when source, name, or code address appears stable.

## Feedback, speculation, and dependency binding

For every speculative fact record:

- feedback/profile source;
- feedback/profile generation;
- speculative invariant;
- consumer optimization pass;
- dependency/watchpoint registration;
- guard/check identity;
- invalidation condition;
- invalidation generation;
- code generation relying on the fact;
- first operation whose semantics would differ if the fact is stale.

Feedback is discovery input, not authority. The proof must show which optimized code consumed it and why the dependency should have become invalid.

## Guard, invalidation, and optimization-transform binding

For the suspected optimization path record:

1. source IR/value state before the pass;
2. optimization pass identity;
3. speculative assumption;
4. guard/check identity;
5. dependency/watchpoint identity;
6. transformation performed;
7. invalidation event, if any;
8. whether optimized code is retired, patched, or remains executable;
9. next semantic operation;
10. first baseline/optimized divergence.

A removed check is not a defect when an equivalent dominating condition or proven invariant exists.

## OSR, inlining, and specialization binding

Bind separately:

- pre-OSR interpreter/baseline state;
- OSR entry identity;
- locals/stack/environment transferred;
- feedback generation used by optimized code;
- inlined callee identity/generation;
- specialization assumptions;
- dependency generations;
- exit/deopt reconstruction targets.

The same source position does not imply the same semantic state across baseline entry, OSR entry, inlined contexts, or deoptimized reconstruction.

## Deoptimization and frame-state reconstruction binding

For each deopt path capture:

- deopt trigger identity;
- optimized code generation;
- deopt metadata generation;
- materialization recipe;
- expected logical frame/environment state;
- reconstructed frame/value identities;
- representation conversions;
- active exception/control state;
- resumed tier identity;
- first semantic consumer after resume.

Deopt occurred != incorrect deopt. A mismatch matters only when reconstructed state differs from the language-level state that baseline/reference execution requires.

## Baseline/reference and semantic-consumer binding

Use a deterministic baseline or specification oracle. Record:

- reference execution mode/build;
- exact program/input generation;
- expected language-level result;
- optimized execution generation;
- optimized result;
- first differing semantic operation;
- final downstream semantic consumer;
- bounded observable result and receipt.

If baseline and optimized executions differ because of permitted nondeterminism, undefined behavior, implementation-defined behavior, time, randomness, external state, or uncontrolled concurrency, evidence is capped until those alternatives are eliminated.

## Evidence ladder

Use JIT0–JIT5 exactly:

- **JIT0 — Optimization surface mapped:** runtime/build, tiers, compilation units, feedback, optimization passes, speculative invariants, guards, invalidation, OSR/inlining, deopt, and semantic consumers are identified.
- **JIT1 — Tier/assumption divergence observed:** a repeatable optimized-only state, feedback, dependency, guard, invalidation, OSR, or deopt divergence exists, but a deterministic semantic mismatch is not yet bound.
- **JIT2 — Controlled optimization-invariant mismatch:** a deterministic local fixture proves a documented speculative, guard, dependency, invalidation, OSR-state, or deopt-state invariant can be violated while preserving the intended optimization path.
- **JIT3 — Inert semantic divergence:** optimized execution produces a deterministic wrong value, wrong branch, stale logical state, or incorrect deopt reconstruction observed by a read-only/mock semantic consumer, while baseline/reference execution remains correct.
- **JIT4 — Bounded reversible optimized effect:** a synthetic canary, inert state mutation, read-only shadow result, bounded assertion, or reversible owner-controlled marker is causally bound to the exact program/tier/code/pass/assumption/guard/deopt/consumer tuple.
- **JIT5 — Regression-verified causal JIT proof:** JIT4 plus complete build/program/compilation provenance, first-invalid-assumption or first-unsound-transform trace, tier/pass confirmation, dependency/invalidation proof, deopt/OSR state where relevant, meaningful counterfactuals, eliminated alternatives, receipt/result binding, and remediation replay.

Crashes, assertions, sanitizer reports, optimization logs, different machine code, stale-looking feedback, or synthetic markers cannot skip missing causal bindings.

## Deterministic benign review cases

At minimum freeze four cases:

1. `stale-type-feedback-after-shape-transition` — optimized code keeps a synthetic type/shape assumption after the dependency generation should have invalidated it.
2. `range-fact-invalidated-by-side-effect` — an optimization reuses a synthetic range fact across a modeled side effect that invalidates the fact; the oracle remains at wrong-value/read-only range-consumer level.
3. `deopt-frame-state-reconstruction-mismatch` — deoptimization reconstructs a synthetic local/environment value from the wrong representation or generation and a read-only consumer observes the mismatch.
4. `osr-tier-generation-assumption-leak` — OSR enters optimized code using a profile/assumption generation that does not match the current baseline state, producing an inert deterministic semantic divergence.

Use only toy/synthetic programs, mock IR/pass traces, deterministic compiler/JIT fixtures, read-only semantic consumers, shadow values, bounded assertions, or reversible owner-controlled markers.

## Counterfactual requirements

Change exactly one causal optimizer variable while holding program/input semantics constant, such as:

- current versus stale feedback generation;
- dependency registered versus omitted;
- guard retained versus unsafely removed;
- invalidation retires old code versus old code remains executable;
- correct versus stale OSR state generation;
- correct versus mismatched deopt frame-state metadata;
- optimization enabled versus the single suspect pass disabled while preserving all other tiers.

A generic “disable all optimization” control is useful but insufficient for JIT5 if it does not isolate the causal pass or dependency.

## Alternative explanations

Before JIT4/JIT5 eliminate:

- language semantics permit both results;
- undefined or implementation-defined behavior exists;
- baseline and optimized executions used different inputs or external state;
- tier/pass activation changed during minimization;
- the suspected pass did not run on the final trigger;
- concurrency/scheduling explains the result;
- a runtime type-confusion bug fully explains the consumer mismatch independently of JIT speculation;
- a bounds/integer bug exists independently of the optimizer assumption;
- sanitizer instrumentation changes the tier/optimization path;
- debug-only assertions or flags create the divergence;
- deoptimization resumed a different but specification-equivalent state;
- the receipt belongs to another compilation or execution generation.

Any unresolved material alternative caps evidence at JIT2.

## Ownership boundaries

- `jit-invariant-analysis` owns optimizer semantic equivalence, tier/code generations, speculative assumptions, dependency/guard/invalidation binding, OSR/inlining state, and deoptimization reconstruction.
- `type-confusion-analysis` owns live runtime type-identity/representation mismatch at the final consumer.
- `bounds-and-integer-analysis` owns arithmetic width/signedness/range/object-size/access equations.
- `concurrency-race-analysis` owns unsafe interleavings and missing happens-before edges.
- `differential-testing` remains a discovery technique; this profile supplies causal optimizer proof.
- `sanitizer-guided-memory-analysis` supplies instrumentation evidence; sanitizer output does not replace optimizer causality.

## Expected repository scope

1. `README.md`
2. `docs/operator-depth-contract.md`
3. `docs/superpowers/plans/2026-09-18-wave10-jit-invariant-depth.md`
4. `docs/superpowers/specs/2026-09-18-wave10-jit-invariant-depth-design.md`
5. `operator-depth/profiles.json`
6. `skills/jit-invariant-analysis/SKILL.md`
7. `skills/jit-invariant-analysis/references/operator-review-cases.json`
8. `skills/jit-invariant-analysis/references/operator-runbook.md`
9. `tests/test_jit_invariant_depth.py`
10. `tests/test_type_confusion_depth.py` only if behavioral CI proves its exact global-count assertion is the sole extensibility defect.

Do not change `skill.meta.json`, graph edges, packs, routing domains, benchmark authority, agent-eval authority, superiority-court authority, or workflow semantics.

## Success criterion

Profile #32 is complete only when the merge tree contains exactly 32 profiles, exactly one valid `jit-invariant-analysis` entry, JIT0–JIT5 is published, exact-head and post-merge CI are fully GREEN, merge parents are verified, and the final scope remains bounded to the intended paths.
