---
name: boot-chain-and-secure-boot-analysis
description: "Analyze embedded/firmware boot trust chains from immutable root through loaders, configuration, measured/verified boot, handoff state, recovery, and runtime policy. Use to reason about verification gaps without weaponizing boot bypasses."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Boot Chain And Secure Boot Analysis

## When to use

Use when reviewing ROM/first-stage boot, UEFI-like flows, secure boot, measured boot, verified partitions, recovery loaders, anti-rollback, or handoff configuration.

## Preconditions

1. Use owned lab hardware/emulation and documented recovery.
2. Pin fuse/root-key state, firmware versions, boot mode, and relevant policy configuration.
3. Use benign test images/config mutations only.

## Workflow

1. Model each boot stage and the root/measurement/verification it relies on.
2. For every transition, record authenticated code/data, version policy, mutable configuration, and which values are trusted by the next stage.
3. Review alternate boot/recovery/manufacturing paths and whether they enforce equivalent trust.
4. Check whether verified code later consumes mutable unauthenticated configuration that changes security policy or image selection.
5. Model rollback counters and update/boot interaction, including power-loss or partial-state transitions.
6. Use safe negative test fixtures where possible to demonstrate rejection of wrong signature/version/config without modifying persistent trust roots.

## Evidence contract

Evidence must identify a specific trust-chain edge, what is verified/measured, what remains mutable, and a controlled acceptance/rejection result. Missing measurement alone does not imply execution bypass.

## Stop conditions

Stop if testing would alter irreversible fuses/keys, disable platform security permanently, or risk unrecoverable device state.

## Output

```text
boot stages:
root keys/policy:
verified/measured artifacts:
mutable handoff state:
alternate paths:
rollback policy:
control results:
evidence status:
```
