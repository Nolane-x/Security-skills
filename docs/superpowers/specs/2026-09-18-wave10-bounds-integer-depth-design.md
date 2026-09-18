# Wave 10 Profile #30 — Bounds and Integer Causal Depth Design

**Date:** 2026-09-18  
**Base authority:** `main@a9608f01062666181a9e882fbcb96d696691887e`  
**Canonical skill:** `bounds-and-integer-analysis`

## Purpose

Promote `bounds-and-integer-analysis` into the thirtieth CI-enforced operator-depth profile while preserving all canonical routing, graph, pack, benchmark, agent-evaluation, superiority-court, and workflow authority.

The canonical skill already requires explicit arithmetic, unit tracking, signedness/width analysis, check-versus-use comparison, overflow reasoning, aggregate arithmetic, boundary classes, and first-invalid-access validation. The missing contract is causal identity across the full numeric pipeline: which logical value, units, representation, conversion, check-domain value, object range, and access equation produced the demonstrated effect.

This profile owns arithmetic/range causality. It does not own parser phase/state causality, temporal lifetime, runtime type identity, sanitizer-diagnostic interpretation, or JIT speculative-range invalidation.

## Causal model

Every promoted finding must bind one reconstructable tuple:

`source value identity + source generation + source units + mathematical value + representation/type chain + width/signedness at each step + cast/promotion/truncation event + arithmetic expression identity + arithmetic generation + check-domain value + check predicate + allocation/object identity + object generation + allocated/declared/usable size + index/offset identity + index/offset value + access width + access range equation + final consumer identity + effective invalid-range capability + bounded result + receipt/result`

The proof must identify the **first arithmetic or representation transition that makes the checked range differ from the consumed range**.

## Required distinctions

Freeze these non-equivalences:

- suspicious cast != integer vulnerability;
- integer overflow != out-of-bounds access;
- truncation != undersized allocation;
- signed-to-unsigned conversion != huge allocation;
- negative value != invalid range until representation and use are bound;
- check passes != access safe;
- allocation succeeds != allocation is large enough;
- allocation failure != memory corruption;
- large allocation != integer overflow;
- outer length mismatch != invalid access;
- one-past-end pointer formation != out-of-bounds dereference;
- different units != unit confusion when conversion is correct;
- alignment rounding != overflow unless the rounded representation diverges;
- object size != usable payload size;
- sanitizer report != exploitability;
- undefined or implementation-defined arithmetic != demonstrated security effect;
- dead-code wraparound != reachable vulnerability;
- invalid arithmetic != attacker-controlled arithmetic;
- arithmetic divergence != downstream dangerous consumption.

## Value identity, units, and representation generations

Track independently:

- source value identity and generation;
- source units;
- mathematical unbounded-integer value;
- parsed or loaded representation;
- machine type, width, and signedness;
- integer-promotion result;
- cast/truncation result;
- checked-arithmetic status;
- normalized/aligned representation;
- arithmetic-generation identity;
- check-domain representation;
- allocation/object generation;
- access-domain representation.

Do not collapse equal numeric bit patterns into equal semantic values when units, signedness, widths, or generations differ.

## Arithmetic expression and conversion binding

For every relevant chain record:

1. source mathematical value;
2. source representation;
3. each cast/promotion/truncation;
4. each addition/subtraction/multiplication/shift/alignment operation;
5. machine semantics for each operation;
6. intermediate mathematical result;
7. intermediate machine result;
8. overflow/underflow/truncation status;
9. final value used by the check;
10. final value used by allocation/range construction;
11. final value used by access.

The first representational divergence must be named explicitly.

## Check-domain and use-domain binding

Write both the intended and implemented constraints.

Examples:

`0 <= offset && width <= object_size - offset`

`count <= MAX / element_size`

`header + count * element_size <= buffer_size`

For each check bind:

- check value representation;
- units;
- inclusive/exclusive endpoint semantics;
- object/range identity checked;
- access width included or omitted;
- whether arithmetic is performed before or after validation;
- whether a later conversion changes the domain.

Check passes != access safe when the consumer uses a different unit, width, object generation, or arithmetic result.

## Allocation, object, region, and usable-size binding

Record separately:

- requested allocation size;
- actual allocation size;
- object identity/generation;
- metadata/header size;
- usable payload size;
- alignment/padding;
- region/view identity;
- declared logical size;
- downstream consumer's assumed size.

Allocation succeeds != allocation is large enough. Object size != usable payload size.

A range claim is promoted only when the final access or semantic consumer is bound to the exact object and generation whose bounds were checked.

## Index, offset, stride, and access-width binding

For each consumer record:

- base object/region identity;
- index or offset identity;
- index/offset representation and units;
- stride;
- access width;
- derived start and end;
- exact valid interval;
- whether end is inclusive/exclusive;
- first byte/element outside the intended range, if any;
- bounded effect or inert oracle.

An index equal to element count may be one-past-end and legal to form in some languages but illegal to dereference. Keep pointer formation separate from memory access.

## Aggregate, alignment, and nested-size arithmetic

Explicitly model:

- `count * element_size`;
- header + payload;
- cumulative record offsets;
- alignment-up expressions;
- page/sector/code-unit conversions;
- decompressed versus compressed sizes;
- nested parent/child sizes;
- repeated accumulation.

Parser-state ownership remains with `parser-state-machine-analysis`; this profile owns whether the numeric equations and machine representations are mutually consistent.

## Evidence ladder

Use **BND0–BND5**:

- **BND0 — Numeric surface mapped:** source values, units, representation widths/signedness, arithmetic expressions, checks, objects, and consumers are mapped.
- **BND1 — Arithmetic/representation divergence observed:** a repeatable wrap, truncation, signedness, unit, alignment, or endpoint divergence exists, but no controlled check/use mismatch reaches a final consumer.
- **BND2 — Controlled check/use mismatch:** a deterministic fixture proves the implemented check validates a different numeric domain, unit, width, endpoint, object size, or generation than the downstream allocation/access uses.
- **BND3 — Inert invalid-range acceptance:** a mock/read-only range consumer, checked shadow-memory oracle, or bounded sanitizer/assertion harness accepts or reaches a range that is invalid under the intended constraint.
- **BND4 — Bounded reversible invalid-range effect:** a synthetic canary, read-only shadow region, fake allocator/object, or reversible owner-controlled marker demonstrates a causally bound invalid range without weaponized exploitation.
- **BND5 — Regression-verified causal bounds proof:** BND4 plus complete value/type/unit/arithmetic provenance, first-divergence trace, object/access binding, meaningful counterfactuals, eliminated alternatives, receipt/result binding, and remediation replay.

A suspicious cast, overflow, sanitizer finding, crash, large allocation, or synthetic marker cannot skip missing causal bindings.

## Deterministic benign review cases

Freeze at least:

1. `multiply-truncate-underallocation` — a wider count×element-size mathematical result truncates in a narrower allocation domain while the later access uses the wider logical count.
2. `signed-negative-to-unsigned-range` — a negative synthetic length/index crosses a signed-to-unsigned boundary and passes a mismatched range or size guard.
3. `alignment-rounding-wrap` — an alignment-up expression wraps or truncates so checked/requested size differs from the object region later consumed.
4. `inclusive-end-access-width-mismatch` — a check validates the start offset at or below the endpoint but omits access width, allowing a bounded synthetic range to cross the exact end.

All cases use synthetic values, fake objects/allocators, shadow ranges, inert/read-only consumers, deterministic assertions, or bounded sanitizer fixtures. No exploit-chain development is required.

## Counterfactual requirements

Each case changes exactly one causal variable while holding the rest constant, such as:

- wide checked multiplication versus truncating multiplication;
- signed-domain rejection versus post-cast unsigned check;
- checked alignment-up versus wrapping alignment arithmetic;
- start-offset-only check versus width-aware end-range check;
- byte units versus element units with explicit conversion.

Generic input-size changes are insufficient unless they isolate the hypothesized arithmetic transition.

## Alternative explanations

Before BND4/BND5 eliminate:

- upstream invariant dominates every use;
- compiler/language semantics define and safely handle the arithmetic;
- allocation API rounds up enough to make the access valid;
- object includes hidden padding or metadata that changes usable bounds;
- access width differs from the assumed width;
- sanitizer instrumentation changes allocation/layout semantics;
- parser rejected the input before the numeric path;
- memory-lifetime issue, not bounds arithmetic, explains the fault;
- type confusion changes the object interpretation;
- JIT speculation or deoptimization owns the range divergence;
- fixture follows a different arithmetic path after minimization;
- receipt belongs to another object or input generation.

Any unresolved material alternative caps evidence at BND2.

## Ownership boundaries

- `parser-state-machine-analysis`: phase/state/order and semantic-object lineage.
- `memory-lifetime-analysis`: invalidation, free/reuse, alias lifetime, stale handles.
- `sanitizer-guided-memory-analysis`: runtime diagnostic interpretation and sanitizer sensitivity.
- `type-confusion-analysis`: runtime type identity/representation interpretation.
- `jit-invariant-analysis`: speculative range/type facts, guards, deoptimization, optimized-vs-baseline divergence.
- `bounds-and-integer-analysis`: mathematical/machine numeric domains, conversion chain, check/use equations, object bounds, and access range.

## Expected repository scope

1. `README.md`
2. `docs/operator-depth-contract.md`
3. `docs/superpowers/plans/2026-09-18-wave10-bounds-integer-depth.md`
4. `docs/superpowers/specs/2026-09-18-wave10-bounds-integer-depth-design.md`
5. `operator-depth/profiles.json`
6. `skills/bounds-and-integer-analysis/SKILL.md`
7. `skills/bounds-and-integer-analysis/references/operator-review-cases.json`
8. `skills/bounds-and-integer-analysis/references/operator-runbook.md`
9. `tests/test_bounds_integer_depth.py`
10. `tests/test_protocol_state_machine_depth.py` only if behavioral CI proves its exact global-count assertion is the sole extensibility defect.

Do not change `skill.meta.json`, graph edges, packs, routing domains, benchmark authority, agent-eval authority, superiority-court authority, or workflow semantics.

## Success criterion

Profile #30 is complete only when the merge tree contains exactly 30 profiles, exactly one valid `bounds-and-integer-analysis` entry, BND0–BND5 is published, exact-head and post-merge CI are fully GREEN, and scope remains bounded to the intended paths.
