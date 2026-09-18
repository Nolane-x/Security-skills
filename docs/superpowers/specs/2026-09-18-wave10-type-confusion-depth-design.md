# Wave 10 Profile #31 — Type Confusion Causal Depth Design

**Date:** 2026-09-18  
**Base authority:** `main@79ef5fa450fd0d5a9cc111e8b7a9958ed38e37f5`  
**Canonical skill:** `type-confusion-analysis`

## Purpose

Promote `type-confusion-analysis` into the thirty-first CI-enforced operator-depth profile while preserving canonical routing, graph, pack, benchmark, agent-eval, superiority-court, and workflow authority.

The current skill already identifies type identities, representation layouts, identity producers, consumers, union transitions, unchecked downcasts, stale tags, and benign wrong-field/dispatch evidence. The missing contract is causal: which logical object and storage generation exists, which type-identity source and generation claims what dynamic type, which representation/layout actually occupies storage, what transition or cast created disagreement, what validator dominated or failed to dominate the consumer, and what exact field/dispatch/operation was interpreted under the wrong type.

## Ownership boundary

This profile owns runtime **type identity ↔ storage representation ↔ consumer interpretation** causality.

It does not absorb:
- `deserialization-trust-analysis`: serialized artifact authenticity/schema/discriminator-to-runtime-type reconstruction and hook authority;
- `jit-invariant-analysis`: speculative optimization assumptions, guards, deoptimization, and machine-code specialization;
- `memory-lifetime-analysis`: allocation lifetime, retirement, reuse, stale aliases, and UAF generations;
- `bounds-and-integer-analysis`: numeric range, offset, size, and access-width arithmetic;
- `concurrency-race-analysis`: unsafe interleavings and missing happens-before edges.

Those profiles may supply adjacent evidence, but #31 owns the moment where a live storage representation is interpreted as the wrong logical/runtime type.

## Causal model

Every promoted finding must bind one reconstructable tuple:

`logical object identity + object/storage generation + logical type identity + actual dynamic type identity + type-identity mechanism + type-identity generation + representation/layout identity + representation generation + producer/transition identity + cast/downcast/variant transition + validator/check identity + validator generation + consumer identity + interpreted type + field/dispatch/operation identity + actual storage member/field identity + type/layout expectation + observed interpretation + effective wrong-type capability + bounded result + receipt/result`

The proof must identify the **first type-identity/representation divergence** and bind it to the exact consumer whose interpretation becomes invalid.

## Required distinctions

Freeze these non-equivalences:

- cast exists != type confusion;
- unchecked cast != wrong dynamic type;
- failed cast != unsafe interpretation;
- stale tag != stale payload;
- tag mismatch != wrong-field access;
- wrong logical type != memory corruption;
- different representation != invalid interpretation when layouts are compatible by contract;
- shared prefix != whole-object type equivalence;
- union member switch != stale-member use;
- discriminator change != active-member transition;
- vtable/class pointer change != valid object transition;
- handle value reuse != type confusion without table/type-generation mismatch;
- object reuse != type confusion without current-lifetime identity mismatch;
- shape/map change != wrong payload interpretation;
- polymorphic dispatch != wrong dispatch;
- debug metadata mismatch != runtime type confusion;
- sanitizer type report != exploitability;
- assertion failure != wrong-type capability;
- wrong-field interpretation != arbitrary code execution;
- wrong dispatch class != control-flow hijack;
- corrupted type metadata != logic-created confusion;
- same bit pattern != same semantic type;
- nominal type != current dynamic type;
- parser tag != current runtime type unless reconstruction binding is proven.

## Object, storage, and type generations

Track independently:

- logical object identity;
- allocation/storage identity;
- object generation;
- storage generation;
- logical/nominal type;
- actual dynamic type;
- type-identity mechanism (tag, discriminant, class/vtable pointer, shape/map, handle-table entry, schema/type id, opcode);
- type-identity generation;
- active union/variant member and member generation;
- representation/layout identity;
- representation generation;
- validator/check generation;
- consumer generation.

Equal addresses, handles, tags, shapes, or bit patterns do not prove the same logical type generation.

## Type-identity source and transition binding

For each relevant producer or transition record:

1. source logical/dynamic type;
2. source storage representation;
3. identity mechanism and identity generation;
4. transition identity;
5. new logical/dynamic type;
6. active member or representation expected after transition;
7. fields destroyed/cleared/reinitialized;
8. new identity metadata written;
9. validation/checks performed;
10. consumer that first trusts the new type.

For tagged unions and variants, bind both the discriminant generation and active payload/member generation.

For handle tables, bind handle value, slot identity, slot generation, stored runtime type, and resolved object generation.

## Cast, downcast, and validator binding

For every cast/downcast or dynamic interpretation record:

- source static type;
- expected target type;
- actual dynamic type;
- validator/check identity;
- whether validation dominates every use;
- validator generation;
- cast result;
- post-cast transformations;
- final consumer.

A cast alone is not evidence. A failed safe cast is a control, not a vulnerability. Promotion requires wrong-type interpretation reaching a consumer.

## Representation/layout and active-member binding

Record separately:

- candidate type A layout;
- candidate type B layout;
- shared prefix if any;
- field/member offsets and semantic meanings;
- alignment/size only as context, leaving arithmetic ownership to bounds analysis;
- active union/variant member;
- member generation;
- object/header metadata;
- runtime type identity;
- exact field/operation interpreted by the consumer.

Representation compatibility must be established by contract, not assumed from overlapping bytes.

## Consumer interpretation and bounded effect

For the final consumer record:

- consumer identity;
- object/storage generation consumed;
- identity mechanism value/generation observed;
- interpreted runtime type;
- expected field/dispatch/operation;
- actual storage member/representation;
- wrong-field read/write or wrong-class dispatch demonstrated;
- effective wrong-type capability;
- bounded result;
- receipt/result.

Prefer read-only field interpretation, inert dispatch sinks, fake handle tables, synthetic tagged unions, assertion/shadow-type oracles, and reversible owner-controlled markers.

## Evidence ladder

- **TCF0 — Type surface mapped:** identity mechanisms, object/storage generations, layouts, producers/transitions, validators, casts, active members, and consumers are identified.
- **TCF1 — Identity/representation divergence observed:** a repeatable tag/type/layout/member/generation divergence exists, but no final wrong-type consumer acceptance is shown.
- **TCF2 — Controlled type-invariant mismatch:** a deterministic fixture proves a documented dynamic-type, active-member, handle-table-type, validator, or representation invariant can be violated.
- **TCF3 — Inert wrong-type interpretation:** a mock/read-only consumer performs a wrong-field interpretation or wrong-class/inert dispatch under the wrong type identity/generation.
- **TCF4 — Bounded reversible wrong-type effect:** a synthetic canary, fake object/handle table, inert dispatch target, read-only shadow object, or reversible owner-controlled marker is causally bound to the exact object/type/representation/consumer tuple.
- **TCF5 — Regression-verified causal type-confusion proof:** TCF4 plus complete object/storage/type-generation provenance, first-divergence trace, transition/validator binding, meaningful counterfactuals, eliminated alternatives, receipt/result binding, and remediation replay.

A cast, tag mismatch, sanitizer finding, assertion, crash, wrong-field observation, or synthetic marker cannot skip missing causal bindings.

## Deterministic benign review cases

At minimum freeze four cases:

1. `stale-discriminant-after-union-transition` — synthetic variant transitions to a new active member but stale discriminant or payload generation causes wrong-member interpretation.
2. `handle-slot-type-generation-reuse` — fake handle-table slot is reused for a new runtime type while stale type/slot generation is accepted by a consumer.
3. `unchecked-downcast-dynamic-type-mismatch` — deterministic synthetic object of type B is consumed through an unchecked type-A downcast despite a failing/absent dominating dynamic-type guard.
4. `shape-payload-generation-skew` — synthetic dynamic-object shape/map generation indicates one layout while payload generation remains from another representation, producing inert wrong-field interpretation.

All cases must use synthetic objects, fake handle tables, mock/inert dispatch, read-only field consumers, deterministic assertions, or bounded reversible local markers.

## Counterfactual requirements

Each case changes exactly one causal variable while holding the rest constant, such as:

- current versus stale discriminant generation;
- current versus stale handle-slot type generation;
- validated versus unchecked downcast;
- shape/map generation synchronized versus skewed with payload;
- active member cleared/reinitialized versus stale payload retained.

Generic corruption or arbitrary byte mutation is not a sufficient counterfactual.

## Alternative explanations

Before TCF4/TCF5 eliminate:

- a dominating runtime type check covers every consumer;
- language/runtime cast semantics fail safely;
- shared-prefix or representation-punning behavior is explicitly permitted;
- consumer accesses only representation-compatible fields;
- deserialization reconstruction explains the wrong runtime type before live-object use;
- memory-lifetime reuse fully explains the observation;
- concurrency/race interleaving owns the identity/payload skew;
- JIT speculation/deoptimization owns the wrong type assumption;
- bounds/offset arithmetic alone explains the invalid access;
- debug metadata differs but runtime identity is correct;
- sanitizer instrumentation created the observation;
- receipt belongs to another object/storage generation.

Any unresolved material alternative caps evidence at TCF2.

## Expected repository scope

1. `README.md`
2. `docs/operator-depth-contract.md`
3. `docs/superpowers/plans/2026-09-18-wave10-type-confusion-depth.md`
4. `docs/superpowers/specs/2026-09-18-wave10-type-confusion-depth-design.md`
5. `operator-depth/profiles.json`
6. `skills/type-confusion-analysis/SKILL.md`
7. `skills/type-confusion-analysis/references/operator-review-cases.json`
8. `skills/type-confusion-analysis/references/operator-runbook.md`
9. `tests/test_type_confusion_depth.py`
10. `tests/test_bounds_integer_depth.py` only if behavioral CI proves its exact global-count assertion is the sole extensibility defect.

Do not change `skill.meta.json`, graph edges, packs, routing domains, benchmark authority, agent-eval authority, superiority-court authority, or workflow semantics.

## Success criterion

Profile #31 is complete only when the merge tree contains exactly 31 profiles, exactly one valid `type-confusion-analysis` entry, TCF0–TCF5 is published, exact-head and post-merge CI are fully GREEN, and the final scope remains bounded to the intended paths.
