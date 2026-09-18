---
name: type-confusion-analysis
description: "Analyze runtime type identity, tagged unions, downcasts, object headers, discriminants, polymorphic dispatch, serialization tags, and representation reuse in authorized code. Use when data may be interpreted as the wrong object/type or a stale/corrupted tag controls unsafe access."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Type Confusion Analysis

Type confusion is an invariant failure between representation and interpretation. Track who establishes type identity, who is allowed to change it, and which consumers trust it.

## When to use

Use for tagged unions, variants, dynamic object models, JIT/runtime values, protocol discriminants, opaque handles, object pools, downcasts, or custom RTTI.

## Preconditions

Testing stays on local, owned, sandboxed, or explicitly authorized targets. Identify the logical type system and concrete representation being analyzed.

## Workflow

1. **Define type identity.** Vtable/class pointer, tag/discriminant, enum, schema id, object map/shape, handle table entry, opcode.
2. **Map representation layout.** Fields whose offsets/meaning differ between candidate types.
3. **Trace producers of identity.** Construction, deserialization, allocation class, transition, cast, cache, object reuse.
4. **Trace consumers.** Field reads/writes, dispatch, destructor, copy, size calculation, barrier/GC logic.
5. **Find trust gaps.** Missing tag check, stale tag after state change, unchecked downcast, inconsistent validation between layers.
6. **Inspect union transitions.** Old fields must be destroyed/cleared before a new active member is trusted.
7. **Check identity/data atomicity.** Concurrent updates can expose a new tag with old payload or vice versa.
8. **Separate corrupted-tag bugs from logic-created confusion.** Root cause matters for fix and variant search.
9. **Use benign evidence.** Demonstrate wrong-field interpretation, wrong dispatch target class, or invariant assertion without constructing harmful control flow.
10. **Search sibling consumers** that trust the same identity source.

## Evidence contract

Show two distinct logical types/representations, the identity mechanism, the path that makes identity disagree with actual storage/state, and a consumer whose interpretation becomes invalid. A cast alone is not evidence if a dominating invariant proves the dynamic type.

## Causal type-confusion model

Treat every promoted type-confusion finding as one causal tuple:

`logical object identity + object/storage generation + logical type identity + actual dynamic type identity + type-identity mechanism + type-identity generation + representation/layout identity + representation generation + producer/transition identity + cast/downcast/variant transition + validator/check identity + validator generation + consumer identity + interpreted type + field/dispatch/operation identity + actual storage member/field identity + type/layout expectation + observed interpretation + effective wrong-type capability + bounded result + receipt/result`.

The proof must identify the first type-identity/representation divergence and bind it to the exact consumer whose interpretation becomes invalid.

Preserve these distinctions explicitly:

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

All dynamic testing remains local/owned/sandboxed or explicitly authorized and uses synthetic objects, fake handle tables, shadow type metadata, deterministic assertions, inert dispatch sinks, read-only consumers, or bounded reversible owner-controlled markers.

## Object, storage, and type generations

Track independently:

- logical object identity;
- allocation/storage identity;
- object/storage generation;
- logical type identity;
- actual dynamic type identity;
- type-identity mechanism;
- type-identity generation;
- active union/variant member and member generation;
- representation/layout identity;
- representation generation;
- validator generation;
- consumer generation.

Equal addresses, handles, tags, maps, shapes, vtable pointers, or bit patterns do not prove the same logical type generation.

## Type-identity source and transition binding

For each producer or transition record:

1. source logical type and actual dynamic type;
2. source storage representation;
3. type-identity mechanism and type-identity generation;
4. producer/transition identity;
5. cast/downcast/variant transition, if any;
6. resulting logical/dynamic type;
7. active member or representation expected after the transition;
8. fields destroyed, cleared, or reinitialized;
9. identity metadata written;
10. validator/check identity and validator generation;
11. consumer that first trusts the new type.

For tagged unions and variants, bind the discriminant generation and active payload/member generation separately.

For fake or real handle tables, bind handle value, slot identity, slot generation, stored runtime type, and resolved object generation.

## Cast, downcast, and validator binding

For each cast or dynamic interpretation record:

- source static type;
- target/interpreted type;
- actual dynamic type;
- validator/check identity;
- whether the validator dominates every consumer;
- validator generation;
- cast/downcast result;
- post-cast representation transformations;
- final consumer identity.

A cast alone is not evidence. A failed safe cast is a control, not a vulnerability. An unchecked cast is not proof of confusion until the target type differs from the actual dynamic type and a consumer trusts the mismatch.

Keep deserialization reconstruction ownership with `deserialization-trust-analysis`; this skill begins at the live runtime object/type boundary.

## Representation, layout, and active-member binding

Record separately:

- candidate type-A representation/layout identity;
- candidate type-B representation/layout identity;
- representation generation;
- shared prefix, if any;
- field/member identities and semantic meanings;
- active union/variant member;
- active-member generation;
- object/header metadata;
- runtime type identity;
- actual storage member/field identity;
- exact field/dispatch/operation identity consumed.

Representation compatibility must be established by contract, not inferred merely because bytes overlap or sizes match.

Keep numeric size/offset/access-width proof with `bounds-and-integer-analysis`; this profile owns the semantic interpretation of the representation.

## Consumer interpretation and bounded effect

For the final consumer capture:

- consumer identity;
- object/storage generation consumed;
- type-identity mechanism value and type-identity generation observed;
- interpreted type;
- type/layout expectation;
- actual storage member/field identity;
- observed interpretation;
- field/dispatch/operation identity;
- effective wrong-type capability;
- bounded result;
- receipt/result.

Prefer read-only wrong-field interpretation, fake handle-table resolution, inert dispatch sinks, shadow-type oracles, deterministic assertions, and reversible owner-controlled markers.

Wrong-field interpretation != arbitrary code execution. Wrong dispatch class != control-flow hijack. Promote only the strongest effect actually demonstrated.

## Type-confusion evidence ladder

Use TCF0–TCF5 exactly:

- **TCF0 — Type surface mapped.** Identity mechanisms, object/storage generations, layouts, producers/transitions, validators, casts, active members, and consumers are identified.
- **TCF1 — Identity/representation divergence observed.** A repeatable tag/type/layout/member/generation divergence exists, but no final wrong-type consumer acceptance is shown.
- **TCF2 — Controlled type-invariant mismatch.** A deterministic fixture proves a documented dynamic-type, active-member, handle-table-type, validator, or representation invariant can be violated.
- **TCF3 — Inert wrong-type interpretation.** A mock/read-only consumer performs wrong-field interpretation or wrong-class/inert dispatch under the wrong type identity or generation.
- **TCF4 — Bounded reversible wrong-type effect.** A synthetic canary, fake object/handle table, inert dispatch target, read-only shadow object, or reversible owner-controlled marker is causally bound to the exact object/type/representation/consumer tuple.
- **TCF5 — Regression-verified causal type-confusion proof.** TCF4 plus complete object/storage/type-generation provenance, first-divergence trace, transition/validator binding, meaningful counterfactuals, eliminated alternative explanations, receipt/result binding, and remediation replay.

A cast, tag mismatch, sanitizer finding, assertion, crash, wrong-field observation, or synthetic marker cannot skip missing causal bindings.

## Counterfactual type controls

Hold unrelated state constant and change exactly one causal type variable:

- current versus stale discriminant generation;
- current versus stale handle-slot type generation;
- validated versus unchecked downcast;
- synchronized versus skewed shape/map and payload generations;
- active member cleared/reinitialized versus stale member payload retained;
- current versus stale validator generation.

Generic byte corruption or arbitrary object mutation is not a sufficient counterfactual.

## Alternative explanations

Before TCF4 or TCF5 explicitly eliminate:

- a dominating runtime type check covers every consumer;
- language/runtime cast semantics fail safely;
- shared-prefix or representation-punning behavior is explicitly permitted;
- the consumer accesses only representation-compatible fields;
- deserialization reconstruction explains the wrong runtime type before live-object use;
- memory-lifetime reuse fully explains the observation;
- concurrency/race interleaving owns the identity/payload skew;
- JIT speculation/deoptimization owns the wrong type assumption;
- bounds/offset arithmetic alone explains the invalid access;
- debug metadata differs but runtime identity is correct;
- sanitizer instrumentation created the observation;
- the receipt belongs to another object/storage generation.

Any unresolved material alternative caps evidence at TCF2.

## Evidence ceiling

Apply the narrowest supported level:

- mapped type surface only: TCF0 maximum;
- identity/representation divergence without consumer acceptance: TCF1 maximum;
- deterministic type-invariant mismatch without final consumer: TCF2 maximum;
- inert/read-only wrong-type interpretation: TCF3 maximum;
- bounded causally bound wrong-type effect: TCF4 maximum;
- only complete object/type provenance, first-divergence reasoning, transition/validator binding, counterfactuals, receipts, and remediation replay reaches TCF5.

Do not promote a cast, tag mismatch, assertion, sanitizer report, crash, or wrong-field observation into a stronger security claim without the missing causal bindings.

## Stop conditions

Stop if language/runtime checks make the cast fail safely, all consumers revalidate identity, the mismatch exists only in debug metadata, or the target is outside authorized scope.

## Output

```text
type system:
identity mechanism:
representations compared:
producer/transition:
missing/stale check:
confused consumer:
observable invalid interpretation:
controls:
variant search surface:
```
