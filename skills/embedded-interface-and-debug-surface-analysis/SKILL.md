---
name: embedded-interface-and-debug-surface-analysis
description: "Analyze UART/JTAG/SWD, recovery consoles, USB device modes, diagnostic protocols, exposed buses, test interfaces, and production debug policy on owned embedded hardware. Use to distinguish intended serviceability from security-boundary bypass."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Embedded Interface And Debug Surface Analysis

## When to use

Use when physical or maintenance interfaces are within the threat model and explicitly authorized for a device assessment.

## Preconditions

1. Confirm physical/debug access is in scope.
2. Document board revision, strap/jumper state, production/manufacturing mode, and recovery procedure.
3. Avoid voltage/bus actions that can damage hardware or attached peripherals.

## Workflow

1. Inventory externally reachable headers, pads, connectors, USB modes, recovery key sequences, diagnostic listeners, and maintenance protocols.
2. Identify interface state and protection across production, recovery, manufacturing, and unlocked/service modes.
3. Map authentication/authorization for diagnostic commands and whether sensitive operations require physical presence plus credentials.
4. Review whether debug state persists across reboot or changes verified-boot/update policy.
5. Use read-only or benign diagnostic commands first; prove negative controls without dumping real secrets.
6. Correlate physical access findings with boot/update trust rather than automatically treating an exposed pad as compromise.

## Evidence contract

Record physical access assumptions, interface mode, authentication gate, benign command capability, persistence, and control behavior. Presence of UART/JTAG is attack surface, not automatically a vulnerability.

## Stop conditions

Stop before invasive hardware modification, secret extraction, irreversible state changes, or actions outside explicit physical-test authorization.

## Output

```text
device/board revision:
interface:
mode/strap state:
auth gate:
benign capability:
persistence/security-policy effect:
control result:
evidence status:
```
