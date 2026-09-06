---
name: patch-diff-variant-analysis
description: "Analyze a security-relevant patch or commit to recover the repaired invariant, identify sibling code paths, and search for related unfixed variants. Use for patch diffing, vulnerability archaeology, regression analysis, or secure backport review."
metadata:
  nolane-security-category: verification
  nolane-security-version: "1"
  nolane-security-authorization: conditional
---
# Patch-Diff Variant Analysis

Treat a security patch as evidence about an invariant, not merely a list of changed lines.

## When to use

Use when a fix, advisory-linked commit, backport, or behavior-changing security patch is available.

## Preconditions

- Obtain vulnerable and fixed revisions when possible.
- Static patch analysis is non-intrusive; any runtime validation must stay within local/owned/sandboxed/authorized scope.
- Do not assume the patch message fully describes the root cause.

## Workflow

1. Isolate behaviorally relevant changes from formatting, refactors, and tests.
2. Infer the repaired invariant: bounds relation, canonicalization, lifetime rule, authorization predicate, state transition, identity key, etc.
3. Identify the old assumption that made the bug possible.
4. Find sibling APIs, alternate types, mirrored implementations, platform-specific branches, older backports, and nearby call sites that enforce the same invariant.
5. Build a structural/semantic search pattern from the invariant rather than exact changed text.
6. Rank variants by shared boundary and attacker influence.
7. Validate candidate variants independently; do not inherit the original vulnerability's status automatically.
8. Check the fix for bypasses caused by alternate encodings, types, normalization paths, error paths, or cleanup paths.
9. Use regression tests to compare vulnerable and fixed behavior when authorized/local.

## Evidence contract

For each candidate variant record:

- shared invariant;
- code path similarity;
- attacker/untrusted influence;
- differences from the original bug;
- validation status;
- why the existing patch does or does not cover it.

A matching code pattern alone remains a hypothesis.

## Stop conditions

Stop variant expansion when the search degenerates into lexical similarity without a shared security invariant, or when runtime confirmation would exceed scope.

## Output

Produce the repaired invariant, patch explanation, ranked variant candidates, validation status, and recommended regression coverage.
