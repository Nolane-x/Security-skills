# Wave 10 Profile #24 — Guest/Host Boundary Causal Depth Design

**Date:** 2026-09-18  
**Base authority:** `main@6030025f045b170faccc61d99a836c6c86b0d6b8`  
**Canonical skill:** `guest-host-boundary-analysis`

## Purpose

Promote the existing canonical `guest-host-boundary-analysis` skill into the twenty-fourth CI-enforced operator-depth profile without creating a duplicate virtualization capability.

The profile must deepen cross-domain causal reasoning: a guest-controlled value or even a host-side crash is not, by itself, evidence of a guest-to-host security boundary consequence. Evidence must bind the initiating guest principal and virtual interface to the exact translation/shared-object/device generation, host consumer and ownership state, effective host capability, bounded result, and lifecycle generation.

## Scope

This is a bounded depth promotion of an existing canonical skill.

Production behavior is limited to:

- deepening `skills/guest-host-boundary-analysis/SKILL.md`;
- adding `references/operator-runbook.md`;
- adding deterministic benign `references/operator-review-cases.json`;
- adding exactly one operator-depth registry entry;
- adding one dedicated profile #24 test;
- minimally repairing the profile #23 global-count assertion if it still freezes the registry at exactly 23;
- publishing README and operator-depth-contract documentation only after behavioral GREEN.

No changes are intended to:

- `skill.meta.json`;
- graph edges;
- packs;
- routing domains;
- benchmark fixtures or thresholds;
- cross-agent evaluation authority;
- superiority-court authority;
- workflow semantics.

## Relationship to adjacent canonical skills

This profile coordinates causal boundary evidence; it does not absorb neighboring skills.

- `virtual-device-model-analysis` owns device-local register/message, descriptor, DMA, reset, migration, callback, and backend invariants.
- `hypervisor-shared-memory-analysis` owns shared-ring/page ownership, index arithmetic, ordering/fencing, mapping, revocation, and shared-object lifetime invariants.
- `bounds-and-integer-analysis`, `memory-lifetime-analysis`, `concurrency-race-analysis`, and `type-confusion-analysis` own corresponding root-cause classes once a concrete invariant failure is established.
- `guest-host-boundary-analysis` owns the cross-boundary proof that a guest-controlled transition reaches a host consumer under the wrong identity, generation, ownership, or effective authority and causes a bounded host-side consequence.

## Causal guest-to-host model

The canonical chain is:

`guest principal/security domain -> interface/device/channel identity and generation -> guest-controlled descriptor/register/message/address -> guest-physical/shared-object identity -> translation/IOMMU/memory-slot generation -> backend/emulation-thread consumer -> host object identity/ownership/lifetime -> validation/pinning/copy/TOCTOU decision -> effective host capability/authority -> bounded host-side result/receipt -> reset/hot-unplug/migration/snapshot/device lifecycle generation`

A profile claim must preserve every material identity and transition relevant to the hypothesis.

## Required distinctions

The skill and runbook must make the following separations explicit:

- guest-controlled input != host-owned object authority;
- guest crash != host boundary crossing;
- host process crash != guest-to-host escape;
- host sanitizer finding != bounded cross-boundary security consequence;
- valid descriptor != current queue/device generation;
- guest physical address != stable host mapping identity;
- mapped address != authorized backend use;
- shared memory reachable != ownership/lifetime safe;
- backend handler reachability != effective host capability;
- emulation-thread execution != privileged host effect;
- device reset complete != stale asynchronous work revoked;
- hot-unplug complete != outstanding mapping/reference revoked;
- snapshot restore != same device/object/lifecycle generation;
- migration success != current host policy/IOMMU/memory-slot generation;
- bounded synthetic host marker != arbitrary host code execution;
- result success != receipt/result binding.

## Guest/host identity model

Each bounded experiment records at minimum:

- guest fixture and principal/security-domain identity;
- VMM/hypervisor build and configuration;
- virtual interface/device/channel identity;
- device/queue/channel generation;
- guest-controlled request/descriptor/register/message identity;
- guest physical address, grant, shared page, memory slot, or mapped-object identity where relevant;
- translation/IOMMU/address-space generation;
- backend/emulation-thread consumer identity;
- host object identity, ownership state, and lifetime generation;
- effective host capability exercised by the consumer;
- lifecycle transition identity such as reset, hot-unplug, snapshot, migration, reconnect, or device recreation;
- bounded result and correlated receipt.

## Invariants

### GH-I1 — Interface/generation binding

A request or descriptor is valid only for the exact interface/device/queue generation in which its authority was established.

### GH-I2 — Address/translation binding

Guest-visible addresses, grants, or shared-object references must resolve through the current authoritative translation/memory-slot/IOMMU generation before host use.

### GH-I3 — Ownership/lifetime binding

A host consumer may use a guest-controlled/shared object only while the recorded ownership and lifetime state permits that use.

### GH-I4 — Capability attenuation

A guest-visible interface grants only its documented effective host-side capability; backend ambient host authority must not silently widen it.

### GH-I5 — Revocation convergence

Reset, unplug, migration, snapshot restore, mapping revocation, or device recreation must invalidate stale asynchronous work and stale object capabilities within the documented lifecycle boundary.

### GH-I6 — Result provenance

A bounded host-side marker, state transition, or read-only result proves only the exact initiating guest/interface/object/generation tuple recorded in its receipt.

## Evidence ladder — GH0 through GH5

### GH0 — Surface mapped

Guest-controlled interfaces, host consumers, shared objects, privilege contexts, and lifecycle transitions are enumerated. No causal consequence is claimed.

### GH1 — Divergence observed

An identity, ownership, translation, ordering, or generation divergence is reproducibly observed, but final host-side acceptance/effect is not established.

### GH2 — Boundary-policy mismatch

A deterministic controlled experiment demonstrates that a guest-controlled request or object is evaluated under a mismatched identity, ownership, translation, or lifecycle policy. This is not yet a host-side security consequence.

### GH3 — Inert wrong-context host acceptance

The final host-side consumer accepts a synthetic guest request/object in the wrong identity/generation/ownership context and exposes only an inert or read-only oracle.

### GH4 — Bounded reversible host-side effect

A bounded, reversible owner-controlled host-side marker, synthetic object transition, or read-only result is causally bound to the exact guest/interface/object/generation tuple.

### GH5 — Regression-verified causal boundary proof

GH4 plus complete principal/interface/device-generation provenance, translation/shared-object identity, host consumer and ownership/lifetime trace, effective capability, lifecycle/revocation trace, meaningful counterfactuals, eliminated alternative explanations, receipt/result binding, and remediation regression.

A host crash, assertion, sanitizer finding, malformed descriptor, mapped page, backend callback, or synthetic marker cannot skip missing causal bindings.

## Counterfactual strategy

Each case changes one material causal variable while holding all others stable.

Examples:

- same descriptor and guest principal, neighboring queue/device generation;
- same shared page and backend consumer, current versus revoked mapping generation;
- same guest physical address and request, neighboring memory-slot/IOMMU generation;
- same asynchronous completion, before versus after reset/hot-unplug;
- same migrated/snapshotted device state, current versus stale host object generation;
- same guest request with an inert consumer that has only documented capability versus a deliberately over-privileged synthetic backend.

If two authoritative variables change, split the experiment before promoting evidence.

## Alternative explanations

Before GH4/GH5, explicitly eliminate:

- stale logs or receipts from another run;
- in-guest failure mistaken for host-boundary transition;
- host crash before the targeted consumer;
- debug-only permissive configuration;
- stale device model/configuration mismatch;
- stale memory-slot/IOMMU or mapping cache;
- intended retry/replay/idempotent completion;
- synthetic fixture mismatch;
- a local device-model bug not causally connected to host authority;
- a shared-memory invariant failure without current consumer use;
- migration/snapshot restore using a different fixture or backend;
- unrelated host service activity.

If an alternative remains plausible, evidence stays at or below GH2.

## Deterministic benign review cases

At least these four case IDs are required:

1. `stale-descriptor-reset-generation`
   - same synthetic descriptor across neighboring device/queue generations;
   - inert host counter/marker;
   - proves whether stale work survives reset under the wrong generation.

2. `shared-memory-revocation-lifetime`
   - same synthetic shared page/grant before and after controlled revocation;
   - read-only/inert backend;
   - proves ownership/lifetime and stale-reference convergence.

3. `address-translation-generation-binding`
   - same guest-visible address under neighboring synthetic memory-slot/IOMMU generations;
   - no real host device passthrough;
   - proves translation identity is revalidated before consumer use.

4. `migration-snapshot-stale-capability`
   - same synthetic device/backend state across controlled migration or snapshot restore;
   - bounded marker only;
   - proves stale host capability/object generations are not inherited silently.

Every case includes positive and negative controls, explicit stop condition, remediation oracle, counterfactual, alternative explanation, GH evidence level and GH evidence ceiling.

## Runbook methodology

Required sections include the common operator-depth sections plus:

- Guest principal and boundary intent trace
- Interface, device, queue, and channel identity trace
- Guest-controlled object and descriptor trace
- Address translation and IOMMU/memory-slot trace
- Shared-memory ownership and lifetime trace
- Backend/emulation-thread consumer trace
- Effective host capability trace
- Reset, hot-unplug, and async revocation trace
- Migration and snapshot lifecycle trace
- Privileged-consumer and result trace
- Counterfactual controls
- Alternative explanations
- Evidence promotion and ceiling

## Safety boundary

Dynamic validation is restricted to:

- disposable/nested/owned guest-host labs;
- synthetic guest principals and device identities;
- synthetic descriptors, pages, grants, addresses, queues, and device state;
- mock or loopback backends;
- inert host counters/markers and read-only synthetic resources;
- bounded reversible owner-controlled effects;
- sanitizers/debug traces when they do not require expanding impact.

Explicitly out of scope:

- production or unrelated hosts/guests;
- passthrough to real devices or production filesystems;
- other tenants;
- real host credentials or secrets;
- persistence;
- arbitrary host code execution as a proof requirement;
- privilege escalation as a proof requirement;
- destructive action;
- malware;
- evasion;
- unauthorized targets.

## TDD and release gates

1. Commit this design.
2. Commit the implementation plan.
3. Add the dedicated #24 test before production artifacts.
4. Open a Draft PR at the exact test-first SHA.
5. Require RED with existing gates green and only intended new profile semantics failing.
6. Implement the skill/runbook/review-cases/registry and only the minimal prior-profile count compatibility fix if required.
7. Do not change the dedicated #24 test after valid RED.
8. Require full behavioral 9/9 GREEN.
9. After behavioral GREEN, change only README and operator-depth contract.
10. Prove the post-behavioral delta is exactly two paths.
11. Require exact-head 9/9 GREEN.
12. Fresh-check main/base/head/scope/mergeability.
13. Guarded merge with `expected_head_sha`.
14. Require post-merge 9/9 GREEN on the exact merge SHA.
15. Verify registry/README/contract directly on the merge tree.
16. Record closure provenance.

## Success criteria

Profile #24 is complete only when the merge-tree registry has exactly 24 profiles with one valid `guest-host-boundary-analysis` entry, README and operator-depth contract publish the GH0–GH5 semantics, exact-head and post-merge CI are fully green, and closure provenance is recorded without claiming external-system superiority.
