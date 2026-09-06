---
name: container-isolation-review
description: "Review container isolation, runtime configuration, namespaces, capabilities, seccomp, mounts, devices, sockets, credentials, and host integration for owned or authorized deployments. Use to identify configuration and design paths that weaken intended tenant/workload isolation without attempting host compromise."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Container Isolation Review

Container security is the composition of kernel isolation and deployment capabilities. Review what the workload can already access before treating any path as an “escape.”

## When to use

Use for Docker/containerd/CRI-style workloads, Kubernetes pods, build runners, CI sandboxes, developer containers, or service workloads with host integrations.

## Preconditions

Assess only owned/local/lab clusters or explicitly authorized environments. Use read-only/synthetic checks where possible and do not modify host security controls to prove a point.

## Workflow

1. **Define workload threat model.** Untrusted code? compromised app? tenant boundary? build job?
2. **Inventory namespaces and sharing.** PID, network, mount, user, IPC, UTS; host namespace sharing.
3. **Inventory Linux capabilities/privilege mode** and no-new-privileges behavior.
4. **Inspect seccomp/AppArmor/SELinux policy** and whether default profiles are disabled.
5. **Inspect mounts.** Host paths, writable system paths, container runtime sockets, device nodes, proc/sysfs exposure, propagation modes.
6. **Inspect credentials and metadata access.** Service account tokens, cloud metadata, registry credentials, mounted secrets.
7. **Inspect runtime/control sockets** and APIs reachable from workload.
8. **Inspect devices and kernel feature exposure.** GPUs, accelerators, FUSE, eBPF-related capability, nested virtualization.
9. **Map cluster-level authorization** for pod creation/update, privileged workloads, hostPath, daemonsets, exec/debug.
10. **Classify findings by existing granted capability versus unintended isolation break.**

## Evidence contract

Record workload identity, isolation expectation, effective namespaces/capabilities/mounts/policies, specific host/cluster capability exposed, and a benign read-only/synthetic validation. A privileged container having broad host rights by design is a dangerous configuration, not necessarily a runtime vulnerability.

## Stop conditions

Stop if validation requires changing host state, touching unrelated tenant data, disabling controls, or testing outside approved cluster/workload scope.

## Output

```text
workload/threat model:
namespaces:
capabilities/privileged:
seccomp/LSM:
mounts/devices/sockets:
credentials/metadata:
cluster permissions:
unintended capability:
benign validation:
configuration vs product bug:
```
