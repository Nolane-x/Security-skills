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
