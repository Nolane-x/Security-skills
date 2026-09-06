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
