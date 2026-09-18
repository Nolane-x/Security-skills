# Wave 10 Profile #27 — Sandbox Boundary Causal Depth Design

**Date:** 2026-09-18  
**Base authority:** `main@b2b6e163ae9690925bbe7db497922ebb6b748f40`  
**Canonical skill:** `sandbox-boundary-analysis`

## Purpose

Promote the existing canonical sandbox-boundary skill into the twenty-seventh CI-enforced operator-depth profile without creating a duplicate sandbox capability or changing routing, graph, benchmark, evaluator, or superiority-court authority.

The current skill correctly enumerates brokers, inherited capabilities, policy layers, namespace/resource naming, shared state, and privileged services. What it does not yet freeze is the causal chain required to distinguish a reachable privileged surface from a proven sandbox-boundary violation.

## Causal model

Every promoted finding must bind one reconstructable tuple:

`sandbox principal + principal/session generation + sandbox policy identity/generation + request/operation generation + broker/service identity + caller-to-request binding + requested resource identity + canonical/resolved resource identity + inherited/delegated capability provenance + namespace/object generation + shared-state generation + privileged consumer + policy decision + effective crossed capability + bounded result + receipt/result`

The proof must explain which denied capability the sandbox is supposed to lack, which exception path is exercised, why the final privileged consumer attributes the request to the wrong or insufficiently constrained sandbox context, and what bounded capability becomes available as a result.

## Required distinctions

The profile must explicitly preserve these non-equivalences:

- broker reachability != broker authority;
- inherited handle/fd != ambient host authority;
- mapped shared memory != authorized privileged use;
- namespace alias != policy bypass without resolved-object divergence and acceptance;
- sandbox policy present != policy applied to the decisive operation;
- restricted token/seccomp profile != proof of complete confinement;
- sandboxed-process crash != sandbox escape;
- privileged-service crash != sandbox escape;
- privileged-service code execution != arbitrary host compromise;
- broadened broker capability != arbitrary code execution;
- process outside the sandbox != privileged process;
- policy mismatch != complete escape;
- synthetic crossed capability != persistence or host compromise;
- stale session/request identity != current authority.

## Identity and generation model

Track independently:

- sandbox principal identity and security domain;
- process/session generation after restart, navigation, worker recycle, plugin reload, or sandbox reinitialization;
- policy profile identity and generation;
- broker/service instance generation;
- request/operation generation;
- resource/object generation;
- namespace/mount/view generation;
- inherited handle/fd/token generation where applicable;
- shared-memory/ring-buffer/command-stream generation;
- lifecycle/revocation generation.

An old broker authorization decision or inherited object must not silently survive a lifecycle transition unless the target contract explicitly allows that continuity.

## Broker and caller binding

For brokered operations, record:

1. caller principal and session generation;
2. transport/channel identity;
3. request generation;
4. requested operation and raw resource identifier;
5. normalized/canonical identifier;
6. resolved object identity;
7. policy identity/generation consulted;
8. decision and attenuation performed by the broker;
9. privileged consumer identity;
10. bounded result and receipt.

The model must distinguish a broker parsing a request from a broker authorizing that request for the current caller and current resource generation.

## Inherited and delegated capability provenance

Capabilities entering the sandbox through inheritance or delegation must have explicit provenance: creator/delegator, object identity, access rights, creation generation, intended consumer, lifetime, revocation semantics, and whether later duplication/transfer widens authority.

Possession is not automatically ambient authority. The profile must reason about what the capability actually permits and whether that permission exceeds the sandbox contract.

## Resource and namespace binding

Policy checks often operate on names while effects occur on resolved objects. Freeze the sequence from raw identifier through normalization/canonicalization, namespace selection, resolution, object identity, and final privileged consumer. Path strings, mount views, object IDs, device names, URLs, or registry-like names must not be promoted as equivalent to the resolved privileged object without evidence.

## Shared-state and privileged-service boundary

Shared memory, ring buffers, GPU/media command streams, broker-owned registries, IPC object tables, and service-side caches need generation-aware ownership and validation. A malformed shared-state element is not enough; the proof must show the privileged consumer accepted a stale, cross-session, cross-object, or policy-inconsistent state and that the resulting effective capability crosses the sandbox contract.

## Lifecycle and revocation

Model restart, navigation, worker recycle, broker reconnect, service crash/restart, policy reload, namespace remount, token/handle close, object-table reset, and sandbox teardown. Evidence must identify which generations become invalid and where stale requests/capabilities are rejected.

## Evidence ladder

- **SB0 — surface mapped:** principals, policies, brokers, inherited/delegated capabilities, namespaces, shared state, privileged consumers, and lifecycle transitions are identified.
- **SB1 — boundary divergence observed:** a repeatable identity, policy, namespace, generation, ownership, or lifecycle divergence exists, but wrong-context privileged acceptance is not shown.
- **SB2 — controlled boundary-policy mismatch:** a deterministic local experiment proves the documented sandbox policy, attenuation, identity binding, or revocation rule can be bypassed or misapplied.
- **SB3 — inert wrong-context privileged acceptance:** the final inert/read-only privileged consumer accepts a synthetic request/resource/capability under the wrong sandbox principal, session, policy, namespace, or generation.
- **SB4 — bounded reversible crossed capability:** an owner-controlled synthetic asset, inert privileged marker, read-only result, or reversible state transition is causally bound to the exact sandbox principal/policy/request/resource/consumer tuple.
- **SB5 — regression-verified causal boundary proof:** SB4 plus complete provenance, generation/lifecycle trace, final effective capability, meaningful counterfactuals, eliminated alternatives, receipt/result binding, and remediation replay.

Crashes, broker reachability, policy configuration, a mapped handle, a privileged callback, or a synthetic marker cannot skip missing causal bindings.

## Safe review cases

At minimum freeze four deterministic benign cases:

1. `stale-session-broker-authorization` — a request authorized for an old sandbox session is replayed after session generation changes.
2. `namespace-alias-resolved-object-mismatch` — a policy-approved synthetic name resolves to a different controlled object generation under a changed namespace view.
3. `inherited-capability-rights-drift` — a synthetic inherited/delegated handle carries broader rights or survives longer than the sandbox contract allows.
4. `shared-object-generation-confusion` — a privileged mock consumer accepts a stale shared-memory/object-table entry from another generation.

Each case must use synthetic identities/resources, mock or loopback brokers/services, inert/read-only consumers, or bounded reversible owner-controlled state.

## Counterfactual requirements

Each CR-style proof must include a boundary-specific counterfactual that changes one causal variable while holding the others fixed, for example current versus stale session generation, canonical resolved object A versus B, attenuated versus unattenuated rights, current versus stale object-table generation, or policy generation before versus after reload.

## Alternative explanations

Before SB4/SB5 reject material alternatives including stale logs, wrong process attribution, intended capability delegation, documented cross-session persistence, namespace test-fixture drift, mock service behavior not matching the target contract, policy reload racing independently, benign service privilege equivalence, marker creation by the positive control, or a neighboring canonicalization/confused-deputy bug that fully explains the result without a sandbox-boundary failure.

Any unresolved material alternative caps evidence at SB2.

## Repository scope

Expected final scope:

1. `README.md`
2. `docs/operator-depth-contract.md`
3. `docs/superpowers/plans/2026-09-18-wave10-sandbox-boundary-depth.md`
4. `docs/superpowers/specs/2026-09-18-wave10-sandbox-boundary-depth-design.md`
5. `operator-depth/profiles.json`
6. `skills/sandbox-boundary-analysis/SKILL.md`
7. `skills/sandbox-boundary-analysis/references/operator-review-cases.json`
8. `skills/sandbox-boundary-analysis/references/operator-runbook.md`
9. `tests/test_sandbox_boundary_depth.py`
10. `tests/test_concurrency_race_depth.py` only if behavioral CI proves its exact global-count assertion is the sole extensibility defect.

Do not modify `skill.meta.json`, graph edges, packs, routing domains, benchmark fixtures/thresholds, agent-eval authority, superiority-court authority, or workflow semantics.

## Verification sequence

1. commit this design;
2. commit the implementation plan;
3. add the dedicated #27 test before production depth artifacts;
4. open a Draft PR at the exact test-first SHA;
5. require intentional RED caused only by the four #27 groups;
6. implement SKILL, runbook, review cases, and registry;
7. repair only a proven stale #26 global-count assertion if needed;
8. require full behavioral 9/9 GREEN;
9. publish only README and operator-depth contract;
10. require exact-head 9/9 GREEN;
11. fresh integration check against unchanged base;
12. guarded merge with expected head SHA;
13. verify merge parents;
14. require post-merge 9/9 GREEN;
15. read registry/README/contract from the merge SHA and record closure provenance.

## Success criterion

Profile #27 is complete only when the merge tree has exactly 27 profiles, exactly one valid `sandbox-boundary-analysis` registration, SB0–SB5 is published, exact-head and post-merge CI are fully green, and no unrelated authority surface changes.