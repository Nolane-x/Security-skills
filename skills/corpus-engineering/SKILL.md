---
name: corpus-engineering
description: "Build, minimize, stratify, and maintain fuzzing corpora for authorized targets using coverage, state, semantic diversity, and boundary-value intent. Use when a campaign has redundant seeds, shallow coverage, poor cold-start behavior, or regression inputs need curation."
metadata:
  nolane-security-category: discovery
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Corpus Engineering

A corpus is a compact map of useful program states, not an archive of every input ever seen. Optimize for distinct behavior and explainable semantic diversity.

## When to use

Use when creating a campaign, migrating fuzzers, reducing seed bloat, recovering from coverage plateaus, or preserving regression-triggering structures.

## Preconditions

All testing that can affect a target must remain on local, owned, sandboxed, or explicitly authorized systems.

1. Stable coverage/state measurement exists.
2. Seed provenance and licensing permit use in the research environment.
3. Sensitive production data is excluded or sanitized.
4. The target/harness version used for minimization is recorded.

## Workflow

1. **Inventory seed sources.** Unit tests, examples, real-but-sanitized samples, protocol captures from lab fixtures, generated structures, historical regressions.
2. **Normalize safely.** Remove irrelevant metadata only when it is not part of the parser/security surface.
3. **Measure behavior.** Edge coverage, state coverage, feature/value profiles, parser phases, or semantic tags.
4. **Minimize for behavior, not byte size alone.** Keep the smallest set that preserves distinct useful states.
5. **Stratify the corpus.** Minimal-valid, deep-valid, malformed-boundary, historical-regression, rare-feature, and state-sequence classes.
6. **Preserve boundary semantics.** Zero/max counts, near-overflow lengths, duplicate keys, recursion depth, alternative encodings, optional fields, and unusual state orders.
7. **Seed dictionaries/token sets from syntax evidence.** Keywords, tags, field names, opcodes, separators, and magic values should come from formats or target comparisons.
8. **Track corpus aging.** Re-minimize after target/harness changes and keep regression seeds pinned when they would otherwise be discarded.
9. **Detect dominance.** Large or expensive seeds that consume most execution time without unique states should be simplified or separated.
10. **Measure cold-start value.** Compare early coverage/state discovery with and without the engineered corpus.

## Evidence contract

Record target/harness revision, corpus source classes, minimization metric, before/after input count and bytes, coverage/state retained, pinned regressions, and cold-start comparison. Corpus size reduction without retained behavior is not success.

## Stop conditions

Stop when minimization is unstable across repeated runs, private/sensitive data cannot be sanitized safely, seed transformations alter the targeted semantics, or coverage metrics are too noisy to justify pruning.

## Output

```text
corpus provenance:
behavior metric:
classes:
before -> after size/count:
coverage/state retained:
pinned regressions:
dictionary/tokens:
cold-start delta:
next campaign use:
```
