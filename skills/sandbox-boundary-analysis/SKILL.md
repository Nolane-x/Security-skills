---
name: sandbox-boundary-analysis
description: "Analyze sandbox, broker, renderer/worker, plugin, container-like, or restricted-process boundaries in an authorized environment. Use to map privileged broker APIs, shared resources, namespace exposure, capability leaks, confused-deputy paths, and assumptions required for a sandbox escape claim."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Sandbox Boundary Analysis

A sandbox is a set of denied capabilities plus explicitly brokered exceptions. Analyze the exceptions first: every broker, inherited handle, shared mapping, namespace object, and privileged helper is part of the boundary.

## When to use

Use for browser renderers, document/media sandboxes, plugin workers, build sandboxes, mobile app sandboxes, restricted tokens, seccomp/capability profiles, or brokered file/device/network access.

## Preconditions

All tests stay on owned/local/sandboxed targets or explicit authorization. Use benign boundary proofs such as access to a synthetic broker resource; do not pursue persistence or host compromise.

## Workflow

1. **Define sandboxed principal and threat model.** Starting privileges, assumed code execution inside sandbox, assets outside.
2. **Enumerate broker interfaces.** IPC methods, file chooser/broker, network service, GPU/media service, font/printing, updater, crash service.
3. **Enumerate inherited capabilities.** Handles/fds, shared memory, environment, namespace membership, device access, tokens, sockets.
4. **Map policy enforcement layers.** OS sandbox, broker authorization, path filters, object capabilities, seccomp/syscall policy.
5. **Check identity binding.** Broker must bind request to the sandboxed caller/session and intended resource.
6. **Check resource naming/canonicalization.** Path/namespace aliases can undermine broker filters.
7. **Check shared-memory/state validation.** Lengths, object ids, ring buffers, command streams, generation counters.
8. **Check privileged service parser surfaces.** Compromise of a broker/service may be a separate boundary step; validate independently.
9. **Demonstrate only benign boundary crossing** to a synthetic asset if needed for validation.
10. **Separate primitive from complete escape.** A broker logic flaw may broaden capability without constituting arbitrary host execution.

## Evidence contract

State sandbox assumptions, denied capability, broker/inherited path, caller identity, policy check, benign external asset reached, and controls. “Process outside sandbox crashed” is not an escape unless causally tied to attacker-controlled sandbox input and a security boundary effect.

## Causal sandbox-boundary model

Treat every promoted finding as one causal tuple:

`sandbox principal + principal/session generation + policy identity + policy generation + request generation + broker/service identity + caller-to-request binding + requested resource identity + canonical/resolved resource identity + inherited/delegated capability + namespace/object generation + shared-state generation + privileged consumer + policy decision + effective crossed capability + bounded result + receipt/result`.

The tuple must explain the denied capability that defines the sandbox, the exception path that is exercised, the exact identity and generation the policy decision applies to, the privileged consumer that turns the decision into an effect, and the bounded result that proves capability broadening. A reachable IPC endpoint or privileged helper is only attack surface until that binding is demonstrated.

Preserve these distinctions explicitly:

- broker reachability != broker authority;
- inherited handle/fd != ambient host authority;
- mapped shared memory != authorized privileged use;
- namespace alias != policy bypass without a resolved-resource mismatch that reaches the decisive policy or consumer;
- sandbox policy present != policy applied to the decisive operation;
- restricted token/seccomp profile != proof of complete confinement;
- sandboxed-process crash != sandbox escape;
- privileged-service crash != sandbox escape;
- privileged-service code execution != arbitrary host compromise;
- broadened broker capability != arbitrary code execution;
- process outside sandbox != privileged process;
- policy mismatch != complete escape;
- stale session/request identity != current authority.

## Sandboxed principal, policy, and lifecycle generations

Record the sandbox principal as a concrete security domain rather than a process label. Bind it to:

- process/session generation;
- sandbox profile or policy identity;
- policy generation or reload generation;
- broker/service instance generation;
- namespace or mount-view generation;
- inherited/delegated capability generation;
- object-table/shared-state generation;
- lifecycle/revocation generation.

Restart, navigation, worker recycle, plugin reload, broker reconnect, service restart, policy reload, namespace remount, sandbox teardown, or handle closure can invalidate earlier authority. A request accepted under generation N does not automatically remain authorized under generation N+1.

## Broker request and caller-session binding

For every brokered operation, bind the transport message to the current sandbox principal and caller session before reasoning about the resource:

1. caller principal and session generation;
2. broker/service identity and instance generation;
3. transport/channel identity;
4. request generation and operation identity;
5. requested resource identity;
6. policy identity/generation consulted;
7. attenuation or rights reduction performed;
8. final privileged consumer;
9. result and receipt/result.

Broker parsing != broker authorization. A syntactically valid request is not evidence that the broker validated the current caller, current session generation, intended operation, and current resource identity together.

## Resource, namespace, and canonical identity binding

Track the complete name-to-object chain:

`raw identifier -> normalized/canonical identifier -> namespace/view -> resolution step -> resolved resource identity -> resource/object generation -> privileged consumer`.

Paths, device names, object IDs, URLs, registry-like names, mount-relative names, or handles can refer to different objects across namespace or lifecycle generations. Namespace alias != policy bypass unless the approved representation and the consumed resolved resource diverge in a security-relevant way and the final consumer accepts the mismatch.

Use the canonicalization skill for representation mechanics, but keep the sandbox-specific question here: did the mismatch broaden a capability the sandbox policy intended to deny?

## Inherited and delegated capability provenance

Track each inherited/delegated capability by creator or delegator, object identity, rights, creation generation, intended recipient, transfer/duplication path, lifetime, revocation event, and final consumer.

Possession != ambient host authority. The capability must be interpreted according to the concrete rights it confers. An inherited handle/fd != ambient host authority, and a delegated token/socket/object is not a sandbox break if it stays within the documented sandbox contract.

Where rights are attenuated, bind requested rights, granted rights, duplicated rights, and the exact policy generation authorizing the transfer. A stale object that survives teardown must be treated as a lifecycle question, not assumed to be current authority.

## Shared state and privileged-service consumer binding

For shared memory, ring buffers, GPU/media command streams, IPC object tables, broker caches, or command queues, record:

- shared-state identity and shared-state generation;
- producer principal/session generation;
- object/slot identifier and generation;
- ownership and validation rule;
- privileged service and consumer identity;
- copy/pin/snapshot semantics where relevant;
- decision point and effective capability;
- bounded result and receipt/result.

Mapped shared memory != authorized privileged use. Malformed or stale shared state is only evidence of a boundary failure after the privileged consumer accepts the wrong principal/object/generation context and produces a capability beyond the sandbox contract.

Privileged-service crash != sandbox escape. Privileged-service code execution != arbitrary host compromise; privilege level, containment, broker role, and reachable capabilities must be established separately.

## Final capability and bounded effect binding

Name the final privileged consumer that converts the policy or identity mismatch into a capability. Record the intended denied capability, actual effective crossed capability, resource/object identity, sandbox principal/session generation, policy generation, and a bounded result.

Prefer synthetic assets, inert privileged markers, read-only results, mock services, or reversible owner-controlled state. A synthetic crossed capability proves only the capability demonstrated; it does not imply persistence, arbitrary host execution, credential access, or unrestricted host compromise.

Policy mismatch != complete escape. Broadened broker capability != arbitrary code execution. Process outside sandbox != privileged process. Promotion must stop at the strongest capability actually bound to evidence.

## Sandbox-boundary evidence ladder

Use SB0–SB5 exactly:

- **SB0 — Surface mapped.** Sandboxed principals, policies, brokers, inherited/delegated capabilities, namespaces, shared state, privileged consumers, and lifecycle transitions are identified.
- **SB1 — Boundary divergence observed.** A repeatable caller/session, policy, namespace, generation, ownership, or lifecycle divergence exists, but the final privileged consumer has not accepted the wrong context.
- **SB2 — Controlled boundary-policy mismatch.** A deterministic local experiment proves the documented policy, attenuation, identity-binding, namespace-binding, or revocation rule can be misapplied.
- **SB3 — Inert wrong-context privileged acceptance.** The final inert/read-only privileged consumer accepts a synthetic request, resource, or capability under the wrong sandbox principal, session, policy, namespace, or generation.
- **SB4 — Bounded reversible crossed capability.** An owner-controlled synthetic asset, inert privileged marker, read-only result, or reversible state transition is causally bound to the exact sandbox principal/policy/request/resource/consumer tuple.
- **SB5 — Regression-verified causal boundary proof.** SB4 plus complete principal/policy/request/resource/capability provenance, lifecycle/revocation trace, final effective capability, meaningful counterfactual controls, eliminated alternative explanations, receipt/result binding, and remediation replay.

Crashes, policy configuration, broker reachability, mapped objects, callbacks, or synthetic markers cannot skip missing causal bindings.

## Counterfactual boundary controls

Hold the semantic fixture constant and change exactly one boundary variable:

- current versus stale session generation;
- current versus stale policy generation;
- same raw identifier resolving to controlled object A versus B;
- attenuated versus unattenuated delegated rights;
- current versus stale shared-object generation;
- revoked versus non-revoked inherited capability;
- caller-bound request versus identical request with mismatched session identity.

A useful counterfactual changes the hypothesized causal edge, not merely timing or log verbosity.

## Alternative explanations

Before SB4 or SB5, test and reject material alternatives:

- the positive control created the marker;
- logs or receipts belong to another process/session generation;
- the capability is intentionally delegated by the sandbox contract;
- cross-session persistence is documented behavior;
- namespace fixture drift, not the target policy, changed resolution;
- the mock service does not preserve the relevant target semantics;
- a policy reload independently changed authorization;
- the supposedly privileged service has no capability advantage over the sandbox;
- a neighboring canonicalization or confused-deputy bug fully explains the effect without a sandbox-boundary failure;
- the result was produced before revocation or lifecycle transition.

Any unresolved material alternative caps evidence at SB2.

## Evidence ceiling

Apply the narrowest supported ceiling:

- reachable broker/service only: SB0 maximum;
- identity/policy/namespace/generation divergence without final acceptance: SB1 maximum;
- deterministic policy or attenuation mismatch without final consumer: SB2 maximum;
- inert/read-only wrong-context privileged acceptance: SB3 maximum;
- bounded causally bound crossed capability: SB4 maximum;
- only complete provenance, lifecycle, counterfactual, receipt/result, and remediation regression reaches SB5.

Never promote a crash, privileged process label, sandbox configuration, or service compromise into a stronger escape claim without the missing causal bindings.
## Stop conditions

Stop if proof requires destructive host actions, the assumed in-sandbox capability is not part of the threat model, or the tested service runs with no privilege/capability advantage over the sandboxed process.

## Output

```text
sandbox principal:
assumed starting capability:
asset/boundary:
broker/inherited surfaces:
policy layers:
identity/resource binding:
benign crossed capability:
controls:
primitive vs complete escape gap:
```
