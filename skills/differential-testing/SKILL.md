---
name: differential-testing
description: "Design differential tests that compare implementations, versions, configurations, parsers, compilers, or execution modes to expose semantic inconsistencies. Use when no single implementation has a complete oracle but peers should agree on normalized behavior or invariants."
metadata:
  nolane-security-category: discovery
  nolane-security-version: "1"
  nolane-security-authorization: conditional
---
# Differential Testing

A differential mismatch is a lead. The hard part is defining what should be equivalent and filtering intentional differences before calling anything a defect.

## When to use

Use when two or more implementations, versions, modes, or normalization paths should preserve a shared semantic contract.

## Preconditions

All testing that can affect a target must remain on local, owned, sandboxed, or explicitly authorized systems.

1. Define the equivalence relation before generating test cases.
2. Pin versions/configurations and normalize nondeterministic output.
3. For remote systems, stay within explicit authorization and rate/resource limits.
4. Maintain known-different fixtures so the comparator does not erase meaningful distinctions.

## Workflow

1. **Name the compared systems.** Implementation A/B, old/new version, parser/runtime pair, debug/release, interpreter/JIT, serializer/deserializer, or local/remote policy engine.
2. **Define normalized observables.** Return value, parsed tree, canonical bytes, error class, state transition, emitted requests, permissions decision, or invariant set.
3. **Specify allowed divergence.** Version banners, ordering without semantic meaning, timestamps, randomized identifiers, diagnostic text, or documented feature differences.
4. **Build seed equivalence classes.** Include valid, boundary, malformed, ambiguous, and canonicalization-sensitive inputs.
5. **Generate one dimension at a time.** Mutate length, nesting, encoding, type, state order, duplicate fields, numeric width, or feature flags while preserving attribution.
6. **Cluster mismatches by semantic signature.** Avoid treating cosmetic output differences as separate findings.
7. **Reduce each mismatch.** Find the smallest input/configuration that preserves the semantic divergence.
8. **Add a third oracle when possible.** Specification text, independent implementation, reference parser, or explicit invariant can break A-versus-B ambiguity.
9. **Trace the divergence point.** Identify where internal state first differs rather than only comparing final outputs.
10. Promote only causally explained, security-relevant mismatches to validation.

## Evidence contract

Preserve compared versions, configurations, normalization rules, minimized input, raw outputs before normalization, normalized outputs, first known divergence, and controls. “A differs from B” is observed evidence; a vulnerability requires a violated security contract and causal explanation.

## Stop conditions

Stop when the equivalence relation is undefined, differences are documented behavior, nondeterminism dominates, normalization hides the suspected bug, or test generation is affecting systems outside scope.

## Output

```text
systems compared:
equivalence contract:
normalization:
minimized mismatch:
raw observations:
first divergence:
security relevance:
controls/third oracle:
next step:
```
