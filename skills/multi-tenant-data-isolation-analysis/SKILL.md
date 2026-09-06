---
name: multi-tenant-data-isolation-analysis
description: "Analyze multi-tenant identity and data partitioning across request context, ORM/query filters, caches, object storage, background jobs, search indexes, exports, and administrative paths. Use to validate isolation with synthetic tenants."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Multi Tenant Data Isolation Analysis

Perform any dynamic validation only in an authorized, owned lab or equivalent explicitly scoped test environment.

## When to use

Use when one service hosts multiple organizations/accounts/projects and tenant identity influences reads, writes, caches, jobs, files, or indexes.

## Preconditions

1. Create at least two synthetic test tenants and principals.
2. Pin roles, tenancy model, region/shard configuration, and relevant cache/job infrastructure.
3. Never use production tenant identifiers or data.

## Workflow

1. Identify canonical tenant identity source and every derived representation (claims, headers, DB schema/key, cache prefix, bucket/key, search filter, job payload).
2. Trace read/write paths and where tenant filters are attached or may be omitted.
3. Review background jobs, exports/imports, admin/support paths, webhooks, search and caches for context loss.
4. Test paired synthetic tenants using identical object names/IDs where possible to expose key-collision or missing-filter behavior.
5. Use negative controls across read, write, list/search, cache, and async/job paths.
6. Route cache collisions to cache-key analysis and policy gaps to authorization analysis.

## Evidence contract

Record tenant/principal pair, object identifiers, data path, isolation key/filter, observed cross-tenant result, and negative-control matrix. ID predictability alone is not an isolation failure.

## Stop conditions

Stop if reproduction would access real customer data, require production support/admin functions, or create irreversible cross-tenant state.

## Output

```text
tenancy model:
principal/tenant pair:
identity representations:
storage/cache/job keys:
isolation checks:
synthetic control matrix:
evidence status:
```
