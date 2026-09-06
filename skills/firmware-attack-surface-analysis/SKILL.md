---
name: firmware-attack-surface-analysis
description: "Inventory firmware and embedded attack surfaces across boot stages, update paths, parsers, IPC, management planes, hardware buses, debug interfaces, persistent configuration, and network services. Use before firmware fuzzing or trust-chain review."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Firmware Attack Surface Analysis

## When to use

Use for device firmware images, bootloaders, embedded Linux/RTOS products, BMC-like management components, appliances, or update packages.

## Preconditions

1. Use owned hardware, vendor-authorized images, emulation, or disposable lab devices.
2. Record hardware revision, boot/update version, image hashes, partitions, and recovery method.
3. Ensure a reliable recovery path before dynamic tests.

## Workflow

1. Decompose image and runtime into boot stages, partitions/filesystems, privileged daemons, network services, parsers, update components, and hardware-facing interfaces.
2. Map attacker principals: remote peer, LAN user, authenticated admin, local user, peripheral, physical operator, compromised guest/component.
3. Map trust boundaries between immutable roots, mutable storage, signed modules, coprocessors, and management processors.
4. Inventory parser-heavy surfaces: image formats, config, certificates, protocols, media, diagnostic messages.
5. Inventory physical/debug surfaces: UART/JTAG/SWD, USB modes, recovery consoles, test pads, exposed buses, but treat physical access as a separate threat model.
6. Rank surfaces by reachability, privilege delta, parser complexity, updateability, and recovery cost.
7. Route update/boot/debug-specific hypotheses to specialized firmware skills.

## Evidence contract

Produce an attack-surface map with principal, interface, parser/state machine, privilege context, persistence, and recovery implications. A discovered service/debug header is not a vulnerability by itself.

## Stop conditions

Stop dynamic work when recovery is uncertain, a test could brick shared/production hardware, or authorization does not cover physical/debug access.

## Output

```text
device/revision/firmware hash:
boot/update topology:
principals:
network/local/physical surfaces:
trust boundaries:
ranked hypotheses:
recovery plan:
```
