---
name: regression-matrix-testing
description: "Verify a security fix across affected and unaffected versions, build modes, platforms, feature flags, and entrypoints using a controlled reproduction matrix. Use when a patch may be incomplete, configuration-specific, backported inconsistently, or vulnerable only in certain packaging/runtime combinations."
metadata:
  nolane-security-category: verification
  nolane-security-version: "1"
  nolane-security-authorization: conditional
---
# Regression Matrix Testing

A single patched build passing one reproducer is weak closure. Build a matrix that distinguishes vulnerable, fixed, unaffected, unsupported, and indeterminate cells.

## When to use

Use after remediation, when triaging version ranges, or when vendor/backport/build differences may change reachability.

## Preconditions

1. A deterministic benign reproducer or security invariant test exists.
2. Version/build artifacts are obtained from authorized or public sources.
3. Matrix dimensions are chosen for causal relevance, not completeness theater.
4. Preserve exact hashes/build flags for every tested cell.

## Workflow

1. **Choose dimensions from root cause.** Version, commit, architecture, allocator, compiler, feature flag, protocol mode, sandbox, packaging, static/dynamic dependency, or caller path.
2. **Define expected classes.** Vulnerable, fixed, unaffected-by-design, unsupported, or unknown.
3. **Select boundary versions.** Last known good/bad, first fixed, backport points, latest maintained branches, and representative downstream bundles.
4. **Automate the same oracle.** Keep reproducer semantics identical across cells; adapt only environment plumbing.
5. **Run positive and negative controls per environment family.** Verify that the test harness itself can distinguish success/failure there.
6. **Record non-comparable cells explicitly.** Build failure, missing feature, changed API, or unavailable dependency should not become “fixed.”
7. **Investigate surprising transitions.** A regression that disappears before the claimed patch or reappears later may reveal alternate paths or test drift.
8. **Check static consumers/dependencies.** System package upgrades may not fix bundled copies.
9. **Add matrix-critical cases to CI/release validation.** Prioritize causal boundaries over every platform permutation.
10. Publish the tested range separately from inferred range.

## Evidence contract

Every claimed cell needs artifact identity, environment, oracle result, and control result. Version-range claims distinguish directly tested evidence from inference based on source history or packaging metadata.

## Stop conditions

Stop when artifacts cannot be provenance-verified, reproducer semantics drift across versions, environment emulation changes the relevant security boundary, or matrix growth no longer tests a causal variable.

## Output

```text
root-cause-sensitive dimensions:
reproducer/oracle:
artifact provenance:
results matrix:
directly tested vulnerable range:
directly tested fixed range:
inferred range + basis:
indeterminate cells:
CI cases retained:
```
