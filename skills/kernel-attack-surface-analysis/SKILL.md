---
name: kernel-attack-surface-analysis
description: "Inventory and prioritize kernel or kernel-like attack surfaces in an authorized lab: syscalls, device interfaces, filesystems, network stacks, ioctls, virtualization, parsers, privilege transitions, and user-controlled object lifecycles. Use before kernel fuzzing, review, or root-cause analysis."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Kernel Attack Surface Analysis

Kernel analysis starts by mapping which untrusted principals can cause privileged code to parse, copy, allocate, schedule, or mutate state. Keep all dynamic work in disposable lab guests or owned test hardware.

## When to use

Use for operating-system kernels, kernel modules/drivers, hypervisor-adjacent kernel components, eBPF/verifier-like subsystems, filesystems, networking, or device interfaces.

## Preconditions

1. Dynamic testing is limited to owned/sandboxed lab systems or explicit authorization.
2. Use snapshots/recovery because crashes can corrupt state or require reboot.
3. Pin kernel/module/config revision, architecture, mitigations, and device model.
4. Prefer synthetic users/devices/data over real host resources.

## Workflow

1. **Enumerate entry families.** Syscalls, ioctls, netlink/socket operations, filesystems, proc/sysfs/debugfs, device mmap/read/write, packet paths, hypercalls, firmware tables.
2. **Map principal and privilege.** Unprivileged user, namespace-contained process, device owner, admin, guest, remote peer.
3. **Map copy/parse boundaries.** User pointers, iovecs, lengths, nested attributes, descriptor arrays, packet metadata, shared memory.
4. **Map object lifecycles.** File/socket/device objects, refs, RCU/epochs, work queues, interrupts, completion callbacks.
5. **Identify concurrency boundaries.** Close versus operation, unregister versus callback, teardown versus worker, interrupt versus process context.
6. **Identify privilege-sensitive sinks.** Credential changes, mappings, arbitrary object lookup, DMA/IOMMU interaction, namespace crossing, host/guest shared structures.
7. **Rank surfaces.** Reachability × parser complexity × lifetime/concurrency × privilege delta × historical churn.
8. **Choose technique per surface.** syzkaller-style syscall modeling, structure-aware fuzzing, targeted static/dataflow review, sanitizer/KASAN evidence, or model-based state exploration.
9. **Define recovery and observability.** Serial logs, crash dump, KASAN/KCSAN/lockdep, VM snapshot, deterministic config.
10. **Route findings** to lifetime/bounds/concurrency/driver-specific skills and evidence validation.

## Evidence contract

Output must distinguish reachable interface evidence from suspected bug evidence. Record principal, entrypoint, required config/device, copied/parsed data, object lifetime, privilege boundary, and chosen oracle. Do not infer a vulnerability from kernel complexity alone.

## Stop conditions

Stop if testing could affect non-lab hosts, recovery is unreliable, required hardware cannot be safely virtualized/isolated, or the analyzed interface is not reachable by the stated principal.

## Output

```text
kernel/build/config:
principal:
entry surfaces:
copy/parse boundaries:
object lifetimes:
concurrency edges:
privilege-sensitive sinks:
ranked targets:
recommended oracle/technique:
recovery plan:
```
