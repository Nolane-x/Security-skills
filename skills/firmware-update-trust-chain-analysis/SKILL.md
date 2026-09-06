---
name: firmware-update-trust-chain-analysis
description: "Analyze firmware update authenticity, rollback policy, component selection, manifest binding, version transitions, recovery images, and post-verification parsing. Use to test update trust without producing malicious firmware."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Firmware Update Trust Chain Analysis

## When to use

Use when a device accepts OTA/local/recovery updates, capsules, manifests, signed bundles, delta patches, component images, or staged boot updates.

## Preconditions

1. Use vendor-authorized test images or synthetic fixtures.
2. Pin current/target versions, hardware identifiers, signer/root configuration, and recovery path.
3. Never deploy altered unsigned payloads to production/shared devices.

## Workflow

1. Map update acquisition, transport, manifest parsing, signature verification, component/version/hardware binding, staging, activation, rollback, and recovery.
2. Identify exactly which bytes/metadata are authenticated and which fields are consumed before or after verification.
3. Check anti-rollback/version comparisons, downgrade exceptions, recovery-mode policy, and multi-component version coupling.
4. Review archive/path/canonicalization and decompression steps after signature verification for authenticated-but-unsafe parsing.
5. Use harmless mutations of synthetic/test bundles to verify rejection of wrong signer, changed manifest, wrong hardware, stale version, and component substitution.
6. Verify failed updates leave a recoverable, known state and do not silently accept partial components.

## Evidence contract

Record authenticated object, signer/root, version/hardware bindings, mutated field, rejection/acceptance point, and resulting boot/update state. Signature verification existing somewhere is not enough; prove binding to the consumed artifact.

## Stop conditions

Stop if a test risks unrecoverable flash state, requires real signing-key compromise, or would bypass production update policy outside explicit authorization.

## Output

```text
update format/path:
authenticated bytes/metadata:
signer/root:
version/hardware policy:
mutation matrix:
accept/reject point:
recovery result:
evidence status:
```
