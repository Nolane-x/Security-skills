# Bounds and Integer Operator Runbook

Use this runbook only for local, owned, sandboxed, benchmark/CTF, simulated, or explicitly authorized targets. Prefer synthetic numeric fixtures, fake allocators/objects, shadow ranges, deterministic assertions, read-only consumers, and bounded sanitizer evidence.

## Attack surface

Map:

- untrusted or derived numeric sources;
- source units and semantic meaning;
- machine type, width, and signedness;
- casts, promotions, truncations, shifts, multiplications, additions, subtraction, alignment, and accumulation;
- check predicates and check-domain values;
- allocation/requested/object/usable sizes;
- index/offset/stride/access-width consumers;
- region/view identities;
- final range consumers and bounded effects.

## Hypothesis matrix

| Hypothesis | Safe oracle | Control |
| --- | --- | --- |
| multiply truncates before allocation | fake allocator records narrow request while shadow consumer records wider logical range | checked wide multiplication rejects or allocates exact required size |
| negative value becomes huge unsigned domain | controlled read-only range oracle records post-cast value | reject in signed domain before conversion |
| alignment-up wraps/truncates | synthetic alignment helper reports machine and mathematical result | checked alignment arithmetic rejects overflow |
| start-offset check omits width | shadow range consumer reports exact start/end interval | width-aware guard rejects crossing end |

## Value/unit/representation trace

For every numeric source capture:

- source value identity and generation;
- source units;
- mathematical value;
- parsed/loaded representation;
- type width and signedness;
- promotion/cast/truncation chain;
- normalized/aligned representation;
- check-domain, allocation-domain, and use-domain values.

Do not infer semantic equality from matching bit patterns when units or signedness differ.

## Arithmetic and conversion trace

Record the exact chain:

1. mathematical input;
2. machine representation;
3. arithmetic expression identity;
4. each intermediate mathematical result;
5. each intermediate machine result;
6. overflow/underflow/truncation state;
7. conversion event;
8. arithmetic generation;
9. final check value;
10. final allocation/use value.

Pin architecture, language/compiler rules, and integer widths.

## Check-domain versus use-domain trace

Write:

- intended mathematical constraint;
- implemented check predicate;
- representation used by the check;
- units;
- endpoint convention;
- object generation checked;
- whether access width is included;
- arithmetic performed before/after validation;
- later conversions before allocation/access.

A passing check is not sufficient when the consumer uses another representation or equation.

## Allocation/object/usable-size trace

Record separately:

- requested allocation size;
- allocator-returned size if observable;
- object identity and generation;
- metadata/header overhead;
- alignment/padding;
- usable size;
- declared logical size;
- region/view identity;
- consumer-assumed size.

Use fake allocators or shadow objects whenever possible.

## Index/offset/stride/access-width trace

For the final range consumer record:

- base object identity;
- index/offset identity;
- numeric representation;
- units;
- stride;
- access width;
- start;
- end;
- access range equation;
- valid interval;
- endpoint semantics;
- bounded result.

Separate one-past-end formation from actual dereference/access.

## Aggregate/alignment/nested-size trace

Expand:

- count × element size;
- header + payload;
- repeated accumulated offsets;
- alignment-up;
- page/sector/code-unit conversions;
- compressed/decompressed sizes;
- parent/child sizes;
- stride-based repeated access.

Record every intermediate width and conversion.

## Controlled validation

Use deterministic benign fixtures:

- synthetic numeric inputs;
- fake allocator/object tables;
- checked shadow-memory ranges;
- inert/read-only copy or slice consumers;
- bounded assertions;
- local sanitizer harnesses with no exploit-chain development;
- exact before/after receipts.

Recommended sequence:

1. establish valid boundary positive control;
2. establish obviously rejected negative control;
3. change one arithmetic/conversion variable;
4. capture first mathematical-versus-machine divergence;
5. bind check-domain and use-domain;
6. bind exact object/range and final consumer;
7. apply the minimal checked-arithmetic or range fix;
8. replay identical fixtures.

## False-positive controls

Eliminate:

- dominating upstream bounds;
- defined safe arithmetic semantics;
- allocator rounding making range valid;
- hidden padding changing usable bounds;
- mistaken access width;
- sanitizer-only layout artifacts;
- parser rejection before use;
- lifetime failure;
- type-confusion root cause;
- JIT range-speculation root cause;
- minimization changing numeric path;
- stale receipt from another object generation.

## Counterfactual arithmetic controls

Change exactly one causal variable:

- wide checked multiplication vs truncating multiplication;
- signed rejection vs post-cast unsigned check;
- checked vs wrapping alignment-up;
- start-only vs width-aware range check;
- bytes vs elements with explicit conversion;
- narrow vs wide representation of the same mathematical value.

Generic size variation is insufficient without isolating one arithmetic transition.

## Alternative explanations

Before BND4/BND5 explicitly reject:

- upstream invariant dominates all consumers;
- language semantics make the operation defined and safe;
- allocator/object capacity exceeds the assumed bound;
- usable payload differs from nominal object size;
- consumer access width is smaller than modeled;
- sanitizer redzones or allocator replacement create the observation;
- parser/container path never reaches the consumer;
- temporal lifetime, runtime type, or JIT invariant fully explains the behavior;
- minimized reproducer follows a different arithmetic chain;
- receipt belongs to another input/object generation.

Any unresolved material alternative caps evidence at BND2.

## Evidence capture

Capture one reconstructable tuple:

`source value identity + source generation + units + mathematical value + representation/type chain + width/signedness + cast/promotion/truncation + arithmetic expression/generation + check-domain value/predicate + allocation/object identity/generation + usable size + index/offset/stride/access width + access range equation + final consumer + effective invalid-range capability + bounded result + receipt/result`

Useful artifacts include value traces, machine/mathematical arithmetic tables, fake-allocation receipts, shadow-range decisions, assertion/sanitizer diagnostics, and remediation replay.

## Evidence promotion and ceiling

### BND0 — Numeric surface mapped

Sources, units, representations, arithmetic expressions, checks, objects, and consumers are known.

### BND1 — Arithmetic/representation divergence observed

A repeatable wrap, truncation, signedness, unit, alignment, or endpoint divergence exists without a controlled check/use mismatch reaching the final consumer.

### BND2 — Controlled check/use mismatch

A deterministic fixture proves the check validates a different domain, unit, width, endpoint, object size, or generation than the allocation/access uses.

### BND3 — Inert invalid-range acceptance

A mock/read-only consumer, shadow-memory oracle, bounded assertion, or local sanitizer harness reaches a range invalid under the intended constraint.

### BND4 — Bounded reversible invalid-range effect

A synthetic canary, read-only shadow region, fake object, or reversible owner-controlled marker demonstrates a causally bound invalid range.

### BND5 — Regression-verified causal bounds proof

BND4 plus complete value/type/unit/arithmetic provenance, first-divergence trace, exact object/access binding, meaningful counterfactuals, eliminated alternatives, receipt/result binding, and remediation replay.

Evidence ceiling rules:

- numeric mapping only: BND0 maximum;
- arithmetic divergence only: BND1 maximum;
- controlled check/use mismatch without final consumer: BND2 maximum;
- inert invalid-range acceptance: BND3 maximum;
- bounded causal invalid-range effect: BND4 maximum;
- complete causal proof plus regression: BND5 only.

## Remediation checks

Verify the causal fix by replaying the exact fixture:

1. perform checked arithmetic before narrowing;
2. reject negative values before unsigned conversion where required;
3. centralize unit conversion;
4. include access width in the range predicate;
5. use overflow-safe alignment helpers;
6. distinguish nominal object size from usable payload;
7. bind checks and access to the same object generation;
8. preserve valid boundary behavior;
9. collect deterministic before/after receipts.

Prefer invariant-level remediation: checked arithmetic, widened validation, unit-safe types, or a central range/slice helper.

## Safety boundary

Only use local/owned/sandboxed/explicitly authorized targets. Stop if validation requires weaponized exploitation, uncontrolled invalid memory access outside a bounded harness, destructive actions, persistence, credential access, denial-of-service, malware, evasion, or unauthorized systems.
