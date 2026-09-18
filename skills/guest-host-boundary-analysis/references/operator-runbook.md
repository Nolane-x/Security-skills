# Guest/Host Boundary Operator Runbook

This runbook is restricted to local/owned/sandboxed, nested, benchmark, CTF, or explicitly authorized virtualization environments. Prefer synthetic guests and objects, mock backends, inert markers, read-only resources, and bounded reversible owner-controlled effects.

## Attack surface

Inventory hypercalls, MMIO/PIO, PCI configuration, virtqueues, virtual devices, guest-agent RPC, shared folders/clipboard, shared pages/rings, grants, DMA/IOMMU translations, management channels, accelerators, backend workers, emulation threads, reset paths, migration, snapshot/restore, reconnect, and hot-unplug. Record which guest principal can reach each interface and which host consumer receives the transition.

## Hypothesis matrix

For each hypothesis record the authoritative guest principal, interface/device/channel identity, device and queue generation, guest-controlled object, translation/shared-object generation, host consumer, ownership/lifetime state, validation decision, effective host capability, lifecycle state, bounded oracle, positive control, negative control, counterfactual, alternative explanation, and evidence ceiling.

## Guest principal and boundary intent trace

Freeze the guest fixture, guest principal/security domain, intended delegated capability, VMM/hypervisor build, and lab authorization. Distinguish in-guest privilege from cross-boundary authority and record the boundary intent before testing.

## Interface, device, queue, and channel identity trace

Record interface, virtual device, queue, channel, endpoint, backend attachment, device generation, and queue generation. Treat reset, reconnect, device recreation, and queue reinitialization as new generations.

## Guest-controlled object and descriptor trace

Record the exact synthetic descriptor, register write, message, hypercall, queue entry, grant, page reference, or guest address. Capture creation generation, parser/validator path, ownership transfer, and whether host code copies, pins, references, or re-reads guest state.

## Address translation and IOMMU/memory-slot trace

Trace each guest-visible address through the current memory-slot, IOMMU, grant, translation, and address-space generation. Record both guest-visible identity and resolved host-object identity.

## Shared-memory ownership and lifetime trace

Record shared page/ring/grant identity, ownership, reference holders, pin state, revocation state, fencing/ordering requirements, and lifetime generation. Shared-memory reachability alone does not prove ownership/lifetime safety or current consumer authorization.

## Backend/emulation-thread consumer trace

Identify the exact backend process, worker, emulation thread, host module, callback, or device model consuming the state. Bind handler entry to the initiating guest tuple and distinguish mere backend reachability from the final decision that exercises host authority.

## Effective host capability trace

Derive the smallest effective host capability exercised by the consumer: inert counter update, read-only synthetic lookup, bounded mock-device state change, or another owner-controlled effect. Compare it with the capability intentionally delegated by the guest interface.

## Reset, hot-unplug, and async revocation trace

For reset and hot-unplug, enumerate outstanding descriptors, async work, callbacks, mappings, references, queue state, and cached translations. Record the revocation generation and verify that stale work converges to rejection.

## Migration and snapshot lifecycle trace

Across migration or snapshot restore, bind device state, backend identity, memory-slot/IOMMU generation, object lifetime, queue generation, and policy generation. Use synthetic neighboring-generation controls.

## Privileged-consumer and result trace

Record the final host decision, consumer identity, effective capability, bounded host result, and receipt/result correlation. The receipt must distinguish the current run from stale or unrelated activity.

## Controlled validation

Use disposable nested guests, synthetic descriptors/pages/grants/addresses, mock or loopback backends, and inert/read-only host resources. Vary one causal variable at a time and never expand impact merely to chase a higher evidence label.

## False-positive controls

Use a valid current-generation positive control, a neighboring-generation negative control, a revoked-object control, a current-translation control, and an inert backend with only documented authority. Confirm debug-only settings, unrelated host activity, intended retry/replay, fixture drift, and stale logs cannot explain the result.

## Counterfactual controls

Hold the guest request stable while changing exactly one authoritative binding: device generation, queue generation, mapping generation, memory-slot/IOMMU generation, ownership/lifetime state, backend capability, or lifecycle generation. If two bindings differ, split the experiment.

## Alternative explanations

Explicitly test and eliminate stale receipts, in-guest failures, host crashes before the target consumer, debug-only permissiveness, stale translation caches, a different backend after migration/restore, device-local bugs without effective host authority, shared-memory corruption without consumer use, intended idempotent completion, and unrelated host activity.

## Evidence capture

Capture fixture identity, VMM/hypervisor revision, guest principal, device/channel/queue identity and generation, guest-controlled object, translation/IOMMU/memory-slot generation, shared-object ownership/lifetime, host consumer, validation/pinning/copy/TOCTOU decision, effective host capability, lifecycle transition, final decision, bounded result, and receipt/result.

## Evidence promotion and ceiling

GH0 maps the surface. GH1 observes divergence. GH2 proves a controlled boundary-policy mismatch. GH3 requires inert wrong-context acceptance by the final host consumer. GH4 requires a bounded reversible owner-controlled host-side effect bound to the exact tuple. GH5 additionally requires complete provenance, lifecycle/revocation evidence, meaningful counterfactuals, eliminated alternative explanations, receipt/result binding, and remediation regression.

## Remediation checks

Re-run the exact synthetic fixture after remediation. Confirm the formerly accepted wrong-context tuple is rejected, the legitimate current-generation positive control still succeeds, neighboring-generation and revoked-object controls still fail, lifecycle revocation converges, and receipts bind to the repaired decision. Promote to GH5 only when the fix and non-regression behavior are both verified.
