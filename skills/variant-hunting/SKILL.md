---
name: variant-hunting
description: "Systematically search an authorized codebase or version family for siblings of a validated vulnerability by abstracting the root-cause invariant rather than matching surface syntax. Use after one real bug is understood well enough to define sources, sinks, guards, ownership, or trust-boundary mistakes."
metadata:
  nolane-security-category: discovery
  nolane-security-version: "1"
  nolane-security-authorization: conditional
---
# Variant Hunting

Variant hunting begins with a validated root cause. Generalize the broken invariant only as far as the evidence supports, then search for sibling paths and prove each independently.

## When to use

Use after validation or patch review reveals a reusable vulnerability pattern across call sites, data types, protocol handlers, products, or branches.

## Preconditions

1. At least one seed issue has a validated causal explanation.
2. Source code, binaries, or version diffs are authorized for analysis.
3. Separate the invariant from incidental names, constants, and file paths.
4. Do not automatically inherit severity or exploitability from the seed issue.

## Workflow

1. **Write the seed invariant.** Example shape: untrusted length reaches allocation arithmetic without checked widening; generic trust substitutes for caller identity; cache key omits security-relevant object state.
2. **Identify structural roles.** Sources, transformations, sanitizers/guards, sinks, ownership transitions, privilege boundaries, and error paths.
3. **Generate search representations.** Text query, AST pattern, dataflow query, code property graph traversal, callgraph slice, patch-neighborhood query, or binary xref pattern.
4. **Search nearest siblings first.** Same helper, same subsystem, alternate protocol command, sibling object type, platform-specific implementation, backport branch.
5. **Model guard equivalence.** Determine whether a different check genuinely enforces the invariant or merely looks similar.
6. **Rank candidates by causal similarity.** Favor same roles and missing invariant over same syntax.
7. **Validate each candidate independently.** Build a minimal reproducer or static proof and run controls; do not call it a variant merely because the query matches.
8. **Refine the abstraction.** False positives reveal over-generalization; missed known siblings reveal overly narrow roles.
9. **Check fix completeness.** Ask whether the patch repaired the invariant centrally or one call site only.
10. **Turn validated variants into regression and reusable query artifacts.**

## Evidence contract

For each candidate preserve seed invariant, search representation, matched causal roles, guard analysis, independent reproducer/proof, and controls. A query match is a candidate, not a vulnerability.

## Stop conditions

Stop expansion when the abstraction becomes “anything unsafe,” candidate validation rate collapses, target scope changes, or the search would require unauthorized access/testing.

## Output

```text
seed finding:
abstract invariant:
structural roles:
search representation:
candidates ranked:
validated variants:
false-positive lessons:
fix completeness:
regression/query artifacts:
```
