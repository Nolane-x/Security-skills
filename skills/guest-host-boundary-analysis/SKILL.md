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

Use this skill when a hypothesis crosses a virtualization boundary: hypervisors, VMMs, container-VM hybrids, virtual devices, paravirtual queues, guest agents, shared memory, clipboard/filesystem integrations, confidential-computing host services, or management channels. The purpose is to prove the guest-to-host transition and its effective authority, not merely to collect crashes.

## Preconditions

1. Work only in a local/owned/sandboxed, disposable, nested, benchmark, CTF, or explicitly authorized guest-host environment.
2. Pin the VMM/hypervisor build, host kernel, guest image/configuration, virtual devices, accelerators, backend configuration, and mitigation state.
3. Use synthetic guest identities, descriptors, pages, grants, addresses, queues, and device state wherever possible.
4. Keep host-side oracles inert, read-only, or bounded and reversible; do not map production filesystems, real passthrough devices, unrelated tenants, or real credentials.
5. Define recovery and stop conditions before dynamic validation.

## Causal guest-to-host boundary model

The canonical causal chain is:

guest principal/security domain -> interface/device/channel identity and generation -> guest-controlled descriptor/register/message/address -> guest-physical/shared-object identity -> translation/iommu/memory-slot generation -> backend/emulation-thread consumer -> host object identity/ownership/lifetime -> validation/pinning/copy/toctou decision -> effective host capability/authority -> bounded host-side result/receipt -> reset/hot-unplug/migration/snapshot/device lifecycle generation

Preserve every material identity and generation that can change the meaning or authority of the transition. A report is incomplete if it skips from a guest-controlled value directly to a host consequence.

Required distinctions:

- guest-controlled input != host-owned object authority
- guest crash != host boundary crossing
- host process crash != guest-to-host escape
- host sanitizer finding != bounded cross-boundary security consequence
- valid descriptor != current queue/device generation
- guest physical address != stable host mapping identity
- mapped address != authorized backend use
- shared memory reachable != ownership/lifetime safe
- backend handler reachability != effective host capability
- emulation-thread execution != privileged host effect
- device reset complete != stale asynchronous work revoked
- hot-unplug complete != outstanding mapping/reference revoked
- snapshot restore != same device/object/lifecycle generation
- migration success != current host policy/iommu/memory-slot generation
- bounded synthetic host marker != arbitrary host code execution
- result success != receipt/result binding

## Guest, interface, and device-generation identity

Record the guest fixture, guest principal/security domain, VMM/hypervisor revision, virtual interface, device, queue, channel, and their active generations. Bind every descriptor, register write, message, hypercall, or queue entry to the exact generation in which it was created and authorized.

A request or descriptor is valid only for the exact interface/device/queue generation in which its authority was established. Queue identifiers, ring indices, handles, and callback registrations are generation-scoped capabilities rather than timeless names.

## Address translation and shared-object binding

Separate guest-visible identity from host-resolved identity. Record guest physical addresses, grants, shared pages, memory slots, IOMMU/address-space mappings, translation-cache state, and their generations.

The host consumer must resolve and validate against the current authoritative translation generation immediately before use when the design requires it. A numerically identical guest address can name a different host object after memory-slot updates, migration, restore, revocation, or remapping.

For shared objects, record ownership, reference holders, pin state, revocation state, lifetime generation, and the exact backend operation that consumes the object. Reachability alone is not authority.

## Host consumer, ownership, and effective authority

Identify the exact backend process/thread/module, emulation thread, worker, host object, ownership state, and privilege context that consumes the guest-controlled state. Then derive the effective host capability exercised by that consumer.

A guest-visible interface grants only its documented capability. Ambient host filesystem, process, device, network, or management authority held by the backend must not be treated as implicitly delegated to the guest. Bind guest intent -> consumer decision -> effective host capability -> bounded result.

When ownership or lifetime can change concurrently, capture validation, pinning, copying, reference acquisition, and TOCTOU boundaries explicitly.

## Reset, unplug, migration, and snapshot lifecycle

Treat reset, queue reinitialization, hot-unplug, device recreation, mapping revocation, snapshot restore, migration, reconnect, backend restart, and policy reconfiguration as lifecycle-generation transitions.

For each transition, record which descriptors, async completions, mappings, references, callbacks, capabilities, and cached translations must be revoked. Verify convergence with neighboring-generation controls instead of assuming a lifecycle API call synchronously invalidated every stale object.

Snapshot or migration success proves only that state moved; it does not prove that stale host objects, IOMMU mappings, backend capabilities, or pre-transition asynchronous work were rebound to the current generation.

## Workflow

1. Enumerate guest-controlled interfaces and identify the exact host consumer for each transition.
2. Freeze guest principal, device/interface/channel identity, queue/device generation, guest-controlled object identity, and lifecycle state.
3. Trace guest-visible addresses or shared objects through the current translation/IOMMU/memory-slot generation to the resolved host object.
4. Record host ownership/lifetime state, validation/pinning/copy decisions, and any TOCTOU window.
5. Derive the backend's effective host capability and compare it with the capability the guest interface is intended to delegate.
6. Build positive, negative, neighboring-generation, and lifecycle counterfactual controls.
7. Use synthetic/inert/read-only/bounded host-side oracles and correlate every result with a receipt.
8. Promote evidence only according to GH0-GH5 and verify remediation with the same controls.

## Guest-host evidence ladder

### GH0 — Surface mapped

Map guest principals, interfaces, devices, channels, host consumers, shared objects, privilege contexts, translation layers, and lifecycle transitions. No host-side security consequence is claimed.

### GH1 — Divergence observed

Reproduce an identity, generation, ownership, translation, ordering, or lifecycle divergence. Final host-side acceptance or effect is not yet established.

### GH2 — Boundary-policy mismatch

Demonstrate deterministically that a guest-controlled request or shared object is evaluated under the wrong identity, generation, ownership, translation, or lifecycle policy. This remains a policy mismatch, not a host escape.

### GH3 — Inert wrong-context host acceptance

Show that the final host-side consumer accepts a synthetic guest request/object in the wrong context while the oracle remains inert or read-only. Bind the acceptance to the exact guest/interface/object/generation tuple.

### GH4 — Bounded reversible host-side effect

Show a bounded reversible owner-controlled host marker, synthetic object transition, or read-only result caused by the exact wrong-context tuple. GH4 does not require or imply arbitrary host code execution, privilege escalation, credential access, persistence, or destructive impact.

### GH5 — Regression-verified causal boundary proof

Require GH4 plus complete guest-principal and interface provenance, device/queue/channel generation, translation/shared-object identity, host consumer identity, ownership/lifetime state, effective host capability, lifecycle/revocation trace, meaningful counterfactuals, eliminated alternative explanations, receipt/result binding, and remediation regression.

## Counterfactual proof

Change one authoritative variable at a time while holding all other inputs stable. Useful controls include the same descriptor under neighboring queue/device generations, the same shared page before and after revocation, the same guest-visible address under neighboring memory-slot/IOMMU generations, and the same asynchronous completion before and after reset or hot-unplug.

If multiple identity or generation variables change together, split the experiment before promotion.

## Alternative explanations

Before GH4 or GH5, eliminate stale logs/receipts, an in-guest failure mistaken for a host transition, a host crash before the targeted consumer, debug-only permissive configuration, a different device model, stale translation caches, intended retry/replay behavior, synthetic fixture mismatch, a device-local bug without host-authority use, shared-memory corruption without current consumer use, a different backend after migration/restore, or unrelated host activity.

If a material alternative remains plausible, cap the result at GH2 or lower.

## Evidence contract

Capture the pinned environment, guest principal, interface/device/channel identity, device/queue generation, guest-controlled object identity, translation/shared-object generation, host consumer, ownership/lifetime state, validation decision, effective capability, lifecycle transition, bounded result, and correlated receipt.

Crashes, sanitizer reports, assertions, malformed descriptors, backend callbacks, mapped pages, or synthetic markers are observations. They do not by themselves establish a guest-to-host security consequence.

## Evidence ceiling

GH0-GH2 may be supported by mapping, traces, state divergence, and controlled policy mismatches. GH3 requires inert final-consumer wrong-context acceptance. GH4 requires a bounded reversible host-side effect causally bound to the exact initiating tuple. GH5 requires full transition provenance, counterfactual proof, alternative-explanation elimination, receipt/result binding, and regression verification.

No evidence level may be promoted because a tool, crash, sanitizer, or model assigns a stronger label.

## Stop conditions

Stop or abort if validation could affect a non-lab host, unrelated guest, real passthrough device, production filesystem, other tenant, real host credential, persistent host state, or any target outside explicit authorization. Do not proceed when the only proposed proof requires arbitrary host code execution, privilege escalation, malware behavior, destructive action, evasion, or credential theft.

## Output

```text
authorization / lab boundary:
guest principal / security domain:
VMM / hypervisor build:
interface / device / channel identity:
device / queue generation:
guest-controlled object:
translation / IOMMU / memory-slot generation:
shared-object ownership / lifetime:
backend / emulation-thread consumer:
effective host capability:
lifecycle transition generation:
controls and counterfactuals:
bounded result / receipt:
alternative explanations eliminated:
GH evidence level / ceiling:
remediation regression:
```
