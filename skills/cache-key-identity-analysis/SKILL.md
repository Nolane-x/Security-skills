---
name: cache-key-identity-analysis
description: "Analyze whether cache keys, memoization identities, deduplication keys, or persistence indexes omit security-relevant input state or collapse distinct principals/requests. Use for cross-user data replay, stale authorization results, first-writer behavior, object serialization collisions, or tenant confusion."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Cache-Key Identity Analysis

A cache is safe only when its key represents every input dimension that can change the security-relevant result—or the cached result is independent of omitted dimensions.

## When to use

Use when request-scoped data, principal identity, headers/cookies, query/form values, feature flags, locale, authorization context, or mutable object contents influence a cached computation.

## Preconditions

Test with synthetic users/tenants and owned/local/sandboxed or explicitly authorized deployments. Avoid real user data in cache experiments.

## Workflow

1. **Define the cached function semantically.** Inputs read directly and indirectly, side state, environment, principal context.
2. **Extract actual key construction.** Serialization, stable hash, argument list, tags, namespace, version, tenant prefix.
3. **Compare dependency set to key set.** Every result-affecting security dimension must either be keyed or proven invariant.
4. **Inspect object serialization.** Some request/wrapper objects stringify to empty/generic forms while callbacks can still read live contents.
5. **Inspect canonicalization collisions.** Different values can normalize to the same key or same value to multiple keys.
6. **Test first-writer/replay order.** A→B and B→A controls distinguish persistent first-result reuse from accidental equality.
7. **Restart/process-boundary test when relevant.** Determine whether the cache persists across worker or deployment lifecycle.
8. **Check invalidation.** Authorization/role/resource changes must evict or version dependent entries.
9. **Check tenant/user scoping** separately from function arguments.
10. **Validate primitive-value extraction controls** or explicit key material as remediation evidence.

## Evidence contract

Show two semantically distinct invocations whose result should differ, the identical/equivalent cache key, first-result replay or wrong cached decision, reverse-order control, and a corrected-key control.

## Stop conditions

Stop if the result is intentionally global and independent of omitted state, the framework documents non-serializable arguments as unsupported with safe failure, or the apparent replay comes from a different persistence layer.

## Output

```text
cached computation:
result dependencies:
key material:
omitted/colliding dimension:
A->B result:
B->A result:
restart/invalidation behavior:
corrected-key control:
security impact:
```
