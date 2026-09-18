---
name: bounds-and-integer-analysis
description: "Analyze size, index, offset, count, stride, truncation, signedness, overflow, alignment, and allocation/access relationships in authorized code. Use for suspected out-of-bounds access, undersized allocation, wraparound, length confusion, or boundary-check mismatch."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Bounds and Integer Analysis

Turn every spatial-safety hypothesis into explicit arithmetic. Most subtle bounds bugs live in a mismatch between the type/units used for validation and the type/units used for allocation or access.

## When to use

Use when untrusted or derived numeric values influence allocation size, array index, pointer offset, copy length, loop bound, serialization size, or protocol/file offsets.

## Preconditions

Only test authorized local/owned/sandboxed targets. Record architecture, integer widths, compiler semantics, and relevant structure sizes.

## Workflow

1. **Name units.** Bytes, elements, records, code units, sectors, pages, bits, or protocol words.
2. **Write the full expression chain.** Input → parse → cast → arithmetic → check → allocation → pointer/index → access width.
3. **Record type at every step.** Signedness, bit width, promotions, truncation, saturation, checked arithmetic, enum/storage type.
4. **Compare check equation to use equation.** Look for different units, omitted multipliers, inclusive/exclusive endpoints, or access width not included in the guard.
5. **Analyze overflow before comparison.** A post-overflow bounds check may validate the wrapped value rather than the mathematical value.
6. **Inspect subtraction and negative values.** Underflow and signed-to-unsigned conversion frequently create huge positive sizes/offsets.
7. **Inspect aggregate arithmetic.** count * element_size + header + alignment, nested lengths, accumulated offsets, and repeated records.
8. **Check parser/container consistency.** Outer length, inner length, actual buffer, decompressed size, and referenced region must agree.
9. **Build boundary classes.** -1/0/1, max representable, max-safe-before-multiply, exact end, one-past-end, alignment edges.
10. **Validate the first invalid access or undersized object** with sanitizer/assertion/log evidence and near-neighbor controls.
11. **Propose invariant-level remediation.** Checked arithmetic, widened validation, central slice/range helper, or unit-safe type.

## Evidence contract

Provide the mathematical intended constraint, concrete machine arithmetic, type widths, check expression, use expression, object bounds, and a reproducer showing the mismatch. Do not label a suspicious cast a vulnerability without a security-relevant invalid range reaching use.

## Causal bounds-and-integer model

Treat every promoted bounds/integer finding as one causal tuple:

`source value identity + source generation + source units + mathematical value + representation/type chain + width/signedness at each step + cast/promotion/truncation event + arithmetic expression identity + arithmetic generation + check-domain value + check predicate + allocation/object identity + object generation + allocated/declared/usable size + index/offset identity + index/offset value + access width + access range equation + final consumer identity + effective invalid-range capability + bounded result + receipt/result`.

The proof must identify the first arithmetic or representation transition that causes the checked numeric domain to diverge from the domain later allocated, indexed, copied, sliced, or consumed.

Preserve these distinctions explicitly:

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

All dynamic testing remains local/owned/sandboxed or explicitly authorized and uses synthetic values, fake objects, shadow ranges, deterministic assertions, read-only consumers, or bounded local sanitizer evidence.

## Value identity, units, and representation generations

Track independently:

- source value identity and source generation;
- source units;
- mathematical value before machine representation;
- representation/type chain;
- width/signedness at each step;
- cast/promotion/truncation event;
- normalized or aligned representation;
- arithmetic generation;
- check-domain value;
- allocation-domain value;
- use-domain value;
- object generation.

Equal bit patterns do not imply equal semantic values when units, signedness, widths, or generations differ.

## Arithmetic expression and conversion binding

For each relevant numeric chain record:

1. source mathematical value;
2. source representation;
3. every cast, promotion, and truncation;
4. every addition, subtraction, multiplication, shift, alignment, or accumulation;
5. machine semantics for each operation;
6. mathematical intermediate result;
7. machine intermediate result;
8. overflow/underflow/truncation status;
9. arithmetic expression identity;
10. arithmetic generation;
11. final check-domain value;
12. final allocation/use-domain value.

Name the first representational divergence explicitly.

## Check-domain and use-domain binding

Write the intended constraint and implemented check side by side.

Examples:

`0 <= offset && access_width <= object_size - offset`

`count <= MAX / element_size`

`header + count * element_size <= buffer_size`

Bind the check predicate to:

- exact value representation;
- units;
- inclusive/exclusive endpoint semantics;
- checked object/range identity and object generation;
- whether access width is included;
- whether arithmetic occurs before or after validation;
- whether later casts or unit conversions change the use-domain.

A check passing in one representation does not prove the later access is safe in another.

## Allocation, object, region, and usable-size binding

Record separately:

- requested allocation size;
- actual allocation size;
- allocation/object identity;
- object generation;
- metadata/header size;
- alignment/padding;
- usable size;
- declared logical size;
- region/view identity;
- downstream assumed size.

Allocation succeeds != allocation is large enough. Object size != usable payload size.

The final access must be bound to the exact object generation whose numeric bounds were validated.

## Index, offset, stride, and access-width binding

For each final consumer capture:

- base object/region identity;
- index/offset identity;
- index/offset representation and units;
- stride;
- access width;
- start equation;
- end equation;
- access range equation;
- exact valid interval;
- endpoint convention;
- final consumer identity;
- effective invalid-range capability;
- bounded result;
- receipt/result.

Keep pointer or iterator formation distinct from dereference or actual range consumption.

## Aggregate, alignment, and nested-size arithmetic

Model aggregate expressions explicitly:

- `count * element_size`;
- header + payload;
- repeated accumulated offsets;
- alignment-up operations;
- page/sector/code-unit conversion;
- compressed/decompressed length relationships;
- parent/child sizes;
- stride and repeated-record arithmetic.

For alignment, record the pre-round value, addend/mask, intermediate width, rounded result, and final allocation/use representation.

Parser phase/order remains owned by `parser-state-machine-analysis`; this profile owns the numeric consistency of the values propagated through those phases.

## Bounds-and-integer evidence ladder

Use BND0–BND5 exactly:

- **BND0 — Numeric surface mapped.** Source values, units, widths/signedness, representations, arithmetic expressions, checks, objects, and consumers are identified.
- **BND1 — Arithmetic/representation divergence observed.** A repeatable wrap, truncation, signedness, unit, alignment, or endpoint divergence exists without a controlled check/use mismatch reaching the final consumer.
- **BND2 — Controlled check/use mismatch.** A deterministic fixture proves the implemented check validates a different numeric domain, unit, width, endpoint, object size, or generation than the downstream allocation/access uses.
- **BND3 — Inert invalid-range acceptance.** A mock/read-only range consumer, checked shadow-memory oracle, bounded assertion, or local sanitizer harness reaches a range invalid under the intended constraint.
- **BND4 — Bounded reversible invalid-range effect.** A synthetic canary, read-only shadow region, fake allocator/object, or reversible owner-controlled marker demonstrates a causally bound invalid range without weaponized exploitation.
- **BND5 — Regression-verified causal bounds proof.** BND4 plus complete value/type/unit/arithmetic provenance, first-divergence trace, object/access binding, meaningful counterfactual controls, eliminated alternative explanations, receipt/result binding, and remediation replay.

A suspicious cast, arithmetic overflow, sanitizer finding, crash, large allocation, or synthetic marker cannot skip missing causal bindings.

## Counterfactual arithmetic controls

Hold all unrelated variables constant and change exactly one numeric assumption:

- wide checked multiplication versus truncating multiplication;
- signed-domain rejection versus post-cast unsigned comparison;
- checked alignment-up versus wrapping alignment arithmetic;
- start-offset-only guard versus access-width-aware range guard;
- bytes versus elements with explicit conversion;
- same mathematical value through narrow versus wide representation.

Generic “smaller input” or “bigger input” controls are insufficient unless they isolate the hypothesized arithmetic transition.

## Alternative explanations

Before BND4/BND5 explicitly eliminate:

- an upstream invariant dominates every use;
- compiler/language semantics define and safely handle the arithmetic;
- allocator rounding makes the actual access valid;
- hidden padding or object metadata changes usable size;
- actual access width differs from the assumed width;
- sanitizer instrumentation changes allocation/layout semantics;
- parser rejects the input before the numeric path;
- memory-lifetime failure explains the fault;
- runtime type confusion changes object interpretation;
- JIT speculation/deoptimization owns the range divergence;
- minimization changed the arithmetic path;
- receipt belongs to another object or input generation.

Any unresolved material alternative caps evidence at BND2.

## Evidence ceiling

Apply the narrowest supported level:

- numeric surface only: BND0 maximum;
- arithmetic/representation divergence without controlled check/use mismatch: BND1 maximum;
- deterministic check/use mismatch without final consumer acceptance: BND2 maximum;
- inert/read-only invalid-range acceptance: BND3 maximum;
- bounded causally bound invalid-range effect: BND4 maximum;
- only complete provenance, first-divergence reasoning, object/access binding, counterfactuals, receipts, and remediation replay reaches BND5.

Do not promote a cast, overflow, warning, allocation failure, sanitizer report, or crash into a stronger security claim without the missing causal bindings.

## Stop conditions

Stop when the value is proven bounded by an upstream invariant that dominates every use, the suspected overflow is defined and safely handled, or only dead/unreachable code exhibits the arithmetic pattern.

## Output

```text
value + units:
type/width chain:
intended mathematical constraint:
implemented check:
allocation/object size:
access equation:
boundary trigger:
first invalid effect:
controls:
fix invariant:
```
