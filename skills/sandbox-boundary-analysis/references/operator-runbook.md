# Sandbox Boundary Operator Runbook

Use this runbook only for local, owned, sandboxed, benchmark/CTF, simulated, or explicitly authorized targets. The goal is causal boundary evidence with deterministic, bounded, benign effects—not uncontrolled escape development.

## Attack surface

Map the complete sandbox boundary before testing:

- sandbox principal/security domain and process/session generations;
- sandbox policy identity, version, reload generation, and OS enforcement layers;
- broker/service identities, channels, request methods, and privileged consumers;
- inherited handles/fds/tokens/sockets/device access and their rights;
- delegated object capabilities and attenuation steps;
- namespace, mount, path, object-table, device, and registry-like views;
- shared memory, ring buffers, command streams, GPU/media queues, caches, and generation counters;
- lifecycle transitions: restart, navigation, worker recycle, plugin reload, reconnect, service restart, policy reload, namespace remount, teardown, revocation.

Record the denied capability that defines the boundary and the exact exception mechanisms by which the sandbox may request privileged work.

## Hypothesis matrix

Convert every suspected boundary flaw into a falsifiable tuple.

| Hypothesis | Safe oracle | Control |
| --- | --- | --- |
| stale sandbox session can reuse an old broker authorization | mock broker returns an inert synthetic marker only if old session generation is accepted | identical request with current-session rebinding rejects stale generation |
| approved name resolves to a different resource under namespace drift | controlled namespace maps a synthetic alias to object B while policy saw object A | pin canonical resolved object before decision and require object A |
| inherited/delegated capability survives with excess rights | synthetic capability table exposes read-only excess-rights metadata without host mutation | rights attenuation and teardown close eliminate excess capability |
| stale shared-object generation is consumed by privileged service | mock privileged consumer emits a structured read-only receipt for stale object generation | generation validation rejects old object-table entry |

Do not write “sandbox escape” from reachability, crashes, policy configuration, or service compromise alone. Name the intended denied capability, exact exception path, decisive policy or identity mismatch, final privileged consumer, and bounded result.

## Principal and policy-generation trace

For every scenario record:

- sandbox principal identity and security domain;
- process/session generation;
- sandbox policy identity and policy generation;
- OS enforcement context such as token/profile/capability set where relevant;
- broker/service instance generation;
- lifecycle generation before and after restart, navigation, reload, or teardown;
- which generation the decisive authorization was derived from.

Treat process labels as insufficient. A new process instance may inherit the same textual role but carry a new session/policy generation. Likewise, a policy file or seccomp profile being present does not prove it controlled the decisive operation.

## Broker request and caller-session trace

For each broker request record:

1. sandbox principal and session generation;
2. channel/transport identity;
3. broker/service identity and instance generation;
4. request/operation generation;
5. raw requested resource and operation;
6. policy identity/generation consulted;
7. caller-session binding method;
8. attenuation or rights reduction;
9. privileged consumer identity;
10. bounded result and receipt/result.

Broker reachability is merely surface. Require proof that the final decision was made for the wrong caller/session, stale generation, wrong resource, or insufficiently attenuated capability.

## Resource and namespace-resolution trace

Capture the full path from representation to object:

`raw identifier -> normalization/canonicalization -> namespace/view generation -> resolution -> resolved resource identity -> resource/object generation -> policy decision -> privileged consumer`.

Record path roots, mount or namespace selection, aliases, symlink-like redirects, object IDs, device names, URLs, registry-like names, and any broker-side cache keys that influence resolution.

An alias is not automatically a bypass. The evidence must show the policy-approved identity differs from the privileged consumer's resolved object in a way that broadens the sandbox's denied capability.

## Inherited/delegated capability trace

For every inherited or delegated capability capture:

- creator/delegator identity;
- capability/object identity and generation;
- requested rights, granted rights, and duplicated/transferred rights;
- intended recipient and session generation;
- inheritance/transfer mechanism;
- lifetime and revocation event;
- final consumer and effective capability.

Distinguish possession from ambient authority. A handle, fd, token, socket, or object capability may be intentionally available inside the sandbox and still conform to policy.

## Shared-state and privileged-consumer trace

For shared memory, rings, command streams, object tables, GPU/media queues, or broker caches record:

- producer principal/session generation;
- shared-state identity and generation;
- object/slot ID and generation;
- ownership and validation rule;
- copy, pin, snapshot, or revalidation point;
- privileged service and exact final consumer;
- decision result and effective crossed capability;
- bounded output and receipt/result.

Mapped shared memory is not privileged authorization. A stale or malformed entry becomes sandbox evidence only when the privileged consumer accepts it under the wrong principal/object/generation context.

## Lifecycle revocation and restart trace

Trace:

- sandbox restart or process recycle;
- navigation/worker/plugin generation changes;
- broker reconnect and service restart;
- policy reload and generation advance;
- namespace/mount-view remap;
- handle/fd/token close or revocation;
- object-table/shared-state reset;
- teardown acknowledgement and final invalidation.

Record where stale requests or capabilities are rejected. If continuity is intentionally supported, capture the contract proving that persistence is expected rather than a boundary violation.

## Final capability and bounded-effect trace

Name the final privileged consumer and the exact capability the sandbox gains.

Record:

- intended denied capability;
- effective crossed capability actually demonstrated;
- principal/session generation;
- policy generation;
- request generation;
- canonical/resolved resource identity;
- final consumer identity;
- bounded result;
- receipt/result correlation.

Use synthetic assets, inert markers, read-only results, mock services, or reversible owner-controlled state. Do not infer arbitrary host execution, persistence, credential access, or full escape from a narrower capability.

## Controlled validation

Use deterministic, benign fixtures:

- synthetic principals and session IDs;
- mock or loopback brokers/services;
- controlled namespace views and synthetic object roots;
- fake handle/fd/token capability tables;
- generation-tagged shared-memory/object-table entries;
- inert/read-only privileged consumers;
- bounded reversible owner-controlled markers.

Recommended sequence:

1. prove normal current-generation behavior;
2. prove a negative denied/stale control;
3. change one identity/policy/namespace/capability generation;
4. observe the final inert/read-only privileged consumer;
5. add the minimal binding/revalidation/attenuation fix;
6. replay the identical controlled fixture;
7. capture deterministic before/after receipts.

## False-positive controls

Always eliminate:

- receipts from another process/session generation;
- intended capability delegation;
- documented cross-session persistence;
- a mock service whose semantics differ from the target contract;
- namespace fixture drift unrelated to the policy decision;
- policy reload changing authorization independently;
- a supposedly privileged service that has no authority advantage over the sandbox;
- positive-control marker emission;
- result creation before the lifecycle/revocation transition;
- a canonicalization/confused-deputy/lifetime bug that explains the result without a sandbox-boundary failure;
- instrumentation that itself changes handle inheritance or namespace state.

## Counterfactual boundary controls

Hold all semantic inputs constant and change one causal boundary variable:

- same request, current versus stale session generation;
- same resource, current versus stale policy generation;
- same raw name, resolved controlled object A versus object B;
- same capability, attenuated versus unattenuated rights;
- same shared entry, current versus stale object generation;
- same inherited object, revoked versus non-revoked lifecycle state;
- same request payload, correctly caller-bound versus caller-session mismatch.

A timing delay is not sufficient unless it directly controls the hypothesized lifecycle or generation edge.

## Alternative explanations

Before SB4 or SB5 explicitly test and reject:

- positive control emitted the marker;
- stale logs or wrong process attribution;
- capability is intentionally permitted;
- session continuity is contractually allowed;
- namespace fixture changed for an unrelated reason;
- mock broker semantics do not match the target;
- policy reload independently changed the result;
- privileged service has equal or lower authority than the sandbox;
- neighboring canonicalization/confused-deputy logic is the complete cause;
- effect occurred before revocation or generation transition.

Any unresolved material alternative caps evidence at SB2.

## Evidence capture

Capture one reconstructable tuple:

`sandbox principal + session generation + policy identity/generation + request generation + broker/service identity + caller-session binding + requested resource + canonical/resolved resource + inherited/delegated capability + namespace/object generation + shared-state generation + privileged consumer + policy decision + effective crossed capability + bounded result + receipt/result`

Useful artifacts:

- generation-tagged broker logs;
- synthetic principal/session records;
- policy-generation receipts;
- canonical and resolved object IDs;
- fake capability-table snapshots;
- shared-object generation traces;
- inert/read-only privileged-consumer output;
- revocation/teardown acknowledgements;
- pre/post remediation replay receipts.

## Evidence promotion and ceiling

Use SB0–SB5 exactly:

### SB0 — Surface mapped

Principals, policies, brokers, capabilities, namespaces, shared state, consumers, and lifecycle transitions are known. No boundary violation proven.

### SB1 — Boundary divergence observed

A repeatable identity, policy, namespace, ownership, generation, or lifecycle divergence exists, but final privileged wrong-context acceptance is not shown.

### SB2 — Controlled boundary-policy mismatch

A deterministic local experiment proves the documented caller binding, policy, attenuation, namespace binding, or revocation contract can be misapplied.

### SB3 — Inert wrong-context privileged acceptance

The final inert/read-only privileged consumer accepts a synthetic request, resource, or capability under the wrong principal, session, policy, namespace, or generation.

### SB4 — Bounded reversible crossed capability

A synthetic asset, inert privileged marker, read-only result, or reversible owner-controlled state transition is bound to the exact principal/policy/request/resource/consumer tuple.

### SB5 — Regression-verified causal boundary proof

SB4 plus complete provenance, lifecycle/revocation trace, effective capability, meaningful counterfactuals, eliminated alternatives, receipt/result binding, and remediation replay.

Evidence ceiling rules:

- broker/service reachability alone: SB0 maximum;
- divergence without final acceptance: SB1 maximum;
- deterministic policy mismatch without final consumer: SB2 maximum;
- inert/read-only wrong-context privileged acceptance: SB3 maximum;
- bounded causally bound crossed capability: SB4 maximum;
- only complete causal proof plus regression reaches SB5.

## Remediation checks

Verify the causal boundary fix:

1. replay the exact pre-fix synthetic fixture;
2. require stale/wrong-context acceptance or capability broadening to disappear;
3. require intended brokered positive behavior to remain;
4. bind caller/session and request generation explicitly;
5. bind policy decision to canonical/resolved resource identity;
6. attenuate inherited/delegated rights to the minimum required;
7. reject stale shared-state/object-table generations;
8. ensure restart/teardown/revocation invalidates prior authority;
9. preserve deterministic receipt/result evidence.

Minimal fixes may include caller-session binding, generation validation, canonical resolved-object binding, object-capability attenuation, revocation fences, ownership checks, or narrower broker policy. Choose the smallest fix that restores the documented sandbox invariant.

## Safety boundary

Only use local/owned/sandboxed/explicitly authorized environments and synthetic/mock/inert/read-only fixtures. Stop if validation would require uncontrolled host compromise, persistence, credential access, destructive changes, denial-of-service, malware, evasion, or unauthorized targets.

## Quick operator template

```text
sandbox principal/session generation:
policy identity/generation:
broker/service identity:
request generation:
caller-session binding:
requested resource:
canonical/resolved resource:
namespace/object generation:
inherited/delegated capability:
shared-state generation:
lifecycle/revocation transition:
privileged consumer:
effective crossed capability:
bounded result:
receipt/result:
counterfactual control:
alternative explanations rejected:
evidence level:
evidence ceiling:
minimal remediation:
regression replay:
```