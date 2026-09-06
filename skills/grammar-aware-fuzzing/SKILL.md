---
name: grammar-aware-fuzzing
description: "Design structure-aware fuzzing for authorized parsers and file/message formats using explicit or inferred grammars, semantic constraints, and structure-preserving mutations. Use when byte-level mutation stalls at syntax checks or fails to reach deep parser states."
metadata:
  nolane-security-category: discovery
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Grammar-Aware Fuzzing

Grammar-aware fuzzing spends mutations on semantic depth rather than repeatedly breaking the first parser check. Model just enough structure to unlock deeper states; do not over-model until mutations lose novelty.

## When to use

Use when inputs have nested syntax, checksums, length fields, tagged unions, dependent counts, compression/container layers, or semantic cross-field constraints.

## Preconditions

1. Target and resource budget are authorized and isolated.
2. At least one valid sample or format description exists.
3. A coverage/state oracle and deterministic harness are available.
4. Preserve malformed-input exploration alongside grammar-valid generation.

## Workflow

1. **Map parse phases.** Container/header, table/index, body records, nested payloads, validation, post-parse semantic processing.
2. **Identify gating constraints.** Magic/version, lengths, checksums, counts, alignment, references, compression, signatures, or state-dependent fields.
3. **Choose representation.** Hand grammar, parser-derived AST, protobuf/schema, custom generator, or inferred chunks; prefer the smallest representation that preserves deep reachability.
4. **Separate syntax from semantics.** Encode hard syntax in the generator while leaving semantic relationships mutable unless they are pure gates.
5. **Create structure-level mutation operators.** Insert/delete/reorder records, mutate discriminants, duplicate references, alter nesting, cross-splice subtrees, and target boundary counts.
6. **Recompute only necessary derived fields.** Checksums and lengths may need repair; avoid automatically repairing the very field whose validation you want to test.
7. **Measure deep-state yield.** Compare edge/state coverage, parser phase reach, and unique failures against byte-level baseline.
8. **Maintain dual corpora.** Valid/deep seeds and intentionally malformed boundary seeds should both survive minimization.
9. **Learn from blockers.** When coverage plateaus, inspect comparisons/state transitions and add only the missing structural relation.
10. Route unique minimized failures to domain-specific parser analysis and validation.

## Evidence contract

Record grammar version, generator/mutator logic, repaired fields, seed provenance, harness identity, coverage/state delta over baseline, minimized reproducer, and oracle output. Increased coverage demonstrates campaign effectiveness, not vulnerability.

## Stop conditions

Stop or simplify when the grammar forces nearly all generated inputs into one shape, semantic repair masks target validation logic, throughput collapses without new states, or harness nondeterminism prevents stable coverage.

## Output

```text
format/parser:
modeled phases:
gating constraints:
grammar representation:
mutation operators:
fields auto-repaired:
baseline vs grammar-aware coverage:
unique failures:
next grammar refinement:
```
