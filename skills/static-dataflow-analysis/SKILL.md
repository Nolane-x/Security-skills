---
name: static-dataflow-analysis
description: "Perform source-level interprocedural security reasoning using dataflow, taint, control-flow, call-graph, or code-property-graph techniques. Use for source-to-sink questions, authorization checks, unsafe data transformations, variant analysis, and large-codebase vulnerability review."
metadata:
  nolane-security-category: discovery
  nolane-security-version: "1"
  nolane-security-authorization: conditional
---
# Static and Dataflow Analysis

Use static analysis to answer a specific flow or invariant question, not to produce an unfiltered warning dump.

## When to use

Use when source is available and the security question spans functions/modules or repeated code patterns.

## Preconditions

- Identify language/build context sufficiently to resolve relevant symbols.
- Define source, transformations, sanitizers/guards, and sink where applicable.
- For follow-up live tests, establish authorization first; pure source analysis is non-intrusive.

## Workflow

1. State the security property and flow question.
2. Identify concrete sources of untrusted data or identity.
3. Identify sensitive sinks or decisions.
4. Trace transformations, aliases, wrappers, serialization, canonicalization, and state storage.
5. Model guards/sanitizers as semantic predicates rather than name-based assumptions.
6. Inspect path feasibility and required state.
7. Generalize the discovered shape into a reusable query/pattern only after understanding one representative path.
8. Run variant search across sibling APIs, call sites, generated code, and alternate input types.
9. Manually inspect high-confidence results and reject infeasible paths.
10. Route candidates requiring runtime proof to `evidence-driven-vulnerability-validation` or a more suitable dynamic skill.

Tool families may include CodeQL-style queries, code property graphs, AST/semantic search, compiler indexes, and language-specific analyzers.

## Evidence contract

A static finding should include:

- source;
- sink/security decision;
- interprocedural path;
- guards and why they do or do not hold;
- attacker/untrusted influence;
- required preconditions;
- code references;
- unresolved feasibility assumptions.

Static reachability alone remains a **hypothesis** unless the claim is purely structural.

## Stop conditions

Stop broad query expansion when:

- results are dominated by the same false-positive mechanism;
- unresolved build/type information makes the path unreliable;
- the query no longer expresses the original security property;
- dynamic confirmation would exceed authorized scope.

## Output

Produce a small set of ranked source-to-sink paths with guard analysis, feasibility assumptions, status, and next evidence step.
