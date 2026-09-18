# Type Confusion Operator Runbook

Use this runbook only for local, owned, sandboxed, benchmark/CTF, simulated, or explicitly authorized targets. Prefer synthetic tagged unions, fake handle tables, mock/inert dispatch sinks, read-only field consumers, shadow type metadata, deterministic assertions, and bounded reversible owner-controlled markers.

## Attack surface

Map:

- logical object identity;
- allocation/storage identity and generation;
- logical/nominal type;
- actual dynamic type;
- type-identity mechanism and generation;
- active union/variant member and member generation;
- representation/layout identity and generation;
- producer/transition identity;
- cast/downcast sites;
- validators/checks and dominance;
- consumer identities;
- wrong-field or dispatch-sensitive operations.

## Hypothesis matrix

| Hypothesis | Safe oracle | Control |
| --- | --- | --- |
| stale union discriminant survives member transition | read-only synthetic field interpreter reports wrong active-member interpretation | synchronized discriminant/member generation converges |
| handle slot reused for new runtime type | fake handle-table consumer emits inert resolved-type receipt | slot generation/type revalidation rejects stale handle |
| unchecked downcast consumes wrong dynamic type | mock read-only consumer records target/actual type mismatch | dominating dynamic-type validator rejects |
| shape/map generation disagrees with payload generation | shadow object reports wrong-field interpretation without unsafe memory access | synchronized shape/payload generations converge |

## Object/storage/type-generation trace

Record:

- logical object identity;
- storage identity;
- object/storage generation;
- logical type identity;
- actual dynamic type;
- type-identity mechanism;
- type-identity generation;
- active member generation;
- representation/layout identity and generation;
- validator generation;
- consumer generation.

Do not collapse address reuse, handle reuse, or equal bit patterns into type continuity.

## Type-identity and transition trace

For each relevant transition capture:

1. source logical/dynamic type;
2. source representation;
3. type-identity mechanism and generation;
4. producer/transition identity;
5. member/type transition;
6. expected new active representation;
7. fields cleared/destroyed/reinitialized;
8. identity metadata updated;
9. validator/check performed;
10. first consumer trusting the result.

Identify the first point where type identity and actual representation diverge.

## Cast/downcast/validator trace

Capture:

- source static type;
- target/interpreted type;
- actual dynamic type;
- cast/downcast operation;
- validator/check identity;
- validator generation;
- dominance over all uses;
- result of safe control cast;
- post-cast transformations;
- final consumer.

A cast existing is not enough; require wrong dynamic type plus downstream interpretation.

## Representation/layout/active-member trace

Record:

- candidate layouts and representation generations;
- shared prefix if any;
- semantic field/member identities;
- active member and member generation;
- runtime type metadata;
- actual storage member/field;
- expected interpreted field/operation;
- whether compatibility is explicit by contract.

Keep range arithmetic in the bounds profile and lifetime ownership in memory-lifetime analysis.

## Consumer interpretation/bounded-effect trace

For the final consumer record:

- consumer identity;
- consumed object/storage generation;
- observed type-identity generation;
- interpreted type;
- actual dynamic type;
- expected field/dispatch/operation;
- actual storage member;
- wrong-field or inert wrong-dispatch result;
- effective wrong-type capability;
- bounded result;
- receipt/result.

## Controlled validation

Use deterministic benign fixtures:

- synthetic variants/tagged unions;
- fake handle tables with explicit slot generations;
- mock class hierarchies;
- inert dispatch tables;
- read-only wrong-field interpreters;
- shadow type maps;
- deterministic assertions.

Recommended sequence:

1. establish valid same-type positive control;
2. establish safe-rejection negative control;
3. change one type identity/member/validator generation variable;
4. capture first identity/representation divergence;
5. bind to final consumer;
6. apply minimal validator/transition/generation fix;
7. replay exact fixture;
8. capture before/after receipts.

## False-positive controls

Eliminate:

- dominating dynamic-type validation;
- safe failing language/runtime casts;
- explicitly permitted representation punning;
- shared-prefix-only access;
- deserialization-only reconstruction mismatch;
- memory-lifetime root cause;
- concurrency-race root cause;
- JIT speculation/deoptimization root cause;
- bounds arithmetic root cause;
- debug-only metadata disagreement;
- sanitizer instrumentation artifacts;
- receipts from another object/storage generation.

## Counterfactual type controls

Change exactly one causal variable:

- stale versus current discriminant generation;
- stale versus current handle-slot generation;
- unchecked versus validated downcast;
- synchronized versus skewed shape/payload generation;
- stale versus reinitialized active member;
- stale versus current validator generation.

Arbitrary byte corruption is not sufficient.

## Alternative explanations

Before TCF4/TCF5 explicitly reject:

- every use is dominated by a valid type guard;
- the runtime safely rejects the cast;
- layout compatibility is contractual;
- only compatible fields are accessed;
- deserialization reconstruction is the true root cause;
- lifetime reuse fully explains the observation;
- race interleaving owns the mismatch;
- JIT specialization owns the assumption;
- bounds arithmetic alone explains the fault;
- debug metadata is stale but runtime identity is correct;
- instrumentation caused the observation;
- receipt belongs to another object generation.

Any unresolved material alternative caps evidence at TCF2.

## Evidence capture

Capture one reconstructable tuple:

`logical object identity + object/storage generation + logical type identity + actual dynamic type identity + type-identity mechanism/generation + representation/layout identity/generation + producer/transition identity + cast/downcast/variant transition + validator/check identity/generation + consumer identity + interpreted type + field/dispatch/operation identity + actual storage member/field identity + type/layout expectation + observed interpretation + effective wrong-type capability + bounded result + receipt/result`

## Evidence promotion and ceiling

### TCF0 — Type surface mapped

Identity mechanisms, object/storage generations, layouts, transitions, validators, casts, active members, and consumers are known.

### TCF1 — Identity/representation divergence observed

A repeatable tag/type/layout/member/generation divergence exists without final wrong-type consumer acceptance.

### TCF2 — Controlled type-invariant mismatch

A deterministic fixture violates a documented dynamic-type, active-member, handle-table-type, validator, or representation invariant.

### TCF3 — Inert wrong-type interpretation

A mock/read-only consumer performs wrong-field interpretation or inert wrong-class dispatch under the wrong type identity/generation.

### TCF4 — Bounded reversible wrong-type effect

A synthetic canary, fake object/handle table, inert dispatch target, read-only shadow object, or reversible owner-controlled marker is causally tied to the exact type tuple.

### TCF5 — Regression-verified causal type-confusion proof

TCF4 plus complete object/storage/type-generation provenance, first-divergence trace, transition/validator binding, meaningful counterfactuals, eliminated alternatives, receipt/result binding, and remediation replay.

Evidence ceiling rules:

- mapped type surface only: TCF0;
- identity/representation divergence only: TCF1;
- controlled type invariant mismatch without consumer: TCF2;
- inert wrong-type interpretation: TCF3;
- bounded causal wrong-type effect: TCF4;
- complete causal proof plus regression: TCF5.

## Remediation checks

Replay the exact fixture and verify:

1. type identity and representation generations stay synchronized;
2. active-member transitions clear or reinitialize stale payload state;
3. handle-table lookup validates slot generation and runtime type;
4. downcasts are dominated by current dynamic-type checks;
5. shape/map and payload generations remain coherent;
6. intended valid polymorphism still works;
7. receipts bind to the corrected object generation;
8. sibling consumers trusting the same identity source remain safe.

Prefer the smallest invariant-level fix.

## Safety boundary

Use only local/owned/sandboxed/explicitly authorized targets. Stop if proof requires weaponized control flow, uncontrolled memory corruption, destructive payloads, credential use, persistence, malware, evasion, or unauthorized systems.
