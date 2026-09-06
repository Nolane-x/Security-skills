---
name: android-keystore-and-local-storage-analysis
description: "Analyze Android secrets at rest: Keystore use, key authentication properties, SharedPreferences/databases/files, backup/export behavior, logs, and token lifecycle. Use to distinguish protected key material from recoverable application data."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Android Keystore And Local Storage Analysis

Perform any dynamic validation only in an authorized, owned lab or equivalent explicitly scoped test environment.

## When to use

Use for mobile secret storage, token caches, encryption keys, biometric-bound operations, local databases, backups, debug logs, or migration flows.

## Preconditions

1. Use synthetic test accounts and keys.
2. Pin device security state, API level, backup settings, and app build.
3. Do not attempt to extract third-party or real-user credentials.

## Workflow

1. Classify stored material by sensitivity, lifetime, rotation, and whether compromise requires confidentiality, integrity, or replay resistance.
2. Map each secret from acquisition to storage, use, refresh, revocation, backup, migration, and deletion.
3. Inspect Keystore key properties: hardware/security level when observable, user-auth requirements, invalidation, exportability assumptions, and alias scoping.
4. Inspect app-private files, preferences, databases, caches, logs, clipboard, screenshots, and backup/export surfaces for plaintext or replayable derivatives.
5. Test with synthetic secrets to verify what persists across logout, reinstall/restore, lock-state changes, and key invalidation.
6. Separate key protection from data protection: a non-exportable key does not protect plaintext cached elsewhere.

## Evidence contract

Record synthetic secret identifier, storage location, key properties, lifecycle event, observed persistence/exposure, and control state. Never include real secrets in evidence.

## Stop conditions

Stop if reproduction requires accessing another user/profile, bypassing device security outside scope, or preserving real credential material.

## Output

```text
secret class:
storage path:
key properties:
lifecycle:
backup/migration behavior:
synthetic control results:
evidence status:
```
