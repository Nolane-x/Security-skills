---
name: guest-host-boundary-analysis
description: "Model virtualization guest-to-host trust boundaries across hypercalls, virtual devices, shared memory, emulation threads, management channels, accelerators, and host integrations. Use before fuzzing virtualized interfaces or evaluating escape claims."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Guest Host Boundary Analysis

## When to use

Use for hypervisors, VMMs, container-VM hybrids, device emulators, guest agents, shared folders/clipboard, paravirtual interfaces, or confidential-computing host interactions.

## Preconditions

1. Use disposable lab guests and an owned host or nested environment.
2. Pin hypervisor/VMM build, host kernel, guest config, virtual devices, accelerators, and mitigation state.
3. Snapshot host/guest and avoid mapping production files/devices.

## Workflow

1. Enumerate guest-controlled interfaces: port/MMIO/PIO, PCI config, virtqueues, hypercalls, shared pages, guest-agent RPC, clipboard/filesystem integrations, device backends.
2. Map where guest-controlled data crosses into host processes/kernel modules and which thread/privilege context consumes it.
3. Identify shared object lifetimes, DMA/IOMMU assumptions, descriptor/ring validation, reset/hot-unplug races, and migration/snapshot state.
4. Separate in-guest privilege transitions from host-boundary transitions.
5. Rank interfaces by reachability, parser complexity, memory ownership, concurrency, and host privilege.
6. Define safe oracles such as sanitizer/crash/assertion/marker in nested lab rather than destructive host effects.

## Evidence contract

Document guest principal, interface/register/message, host consumer, trust/validation boundary, configuration dependency, and oracle. A guest crash or host log warning is not a guest-to-host escape by itself.

## Stop conditions

Stop if testing could affect a non-lab host, passthrough device, shared production filesystem, or other tenants.

## Output

```text
VMM/hypervisor build:
guest config:
guest-controlled interfaces:
host consumers:
shared state/lifetimes:
ranked hypotheses:
oracle/recovery plan:
```
