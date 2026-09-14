# Container Isolation Operator Runbook

Use this runbook only for owned clusters, isolated labs, benchmark fixtures, or explicitly authorized deployments. Prefer source/configuration review, policy simulation, read-only runtime inspection, synthetic workloads, mock resources, and disposable namespaces. Do not weaken host controls, access unrelated tenant data, or attempt host compromise to prove a point.

The objective is to verify a stated isolation guarantee from authored intent through the state that actually executes. The review must distinguish configuration exposure from a failure of an isolation invariant and must identify which layer created the effective capability.

A complete review correlates four evidence families:

1. **policy evidence** — the threat principal, isolation objective, and intended invariant;
2. **control-plane evidence** — requested state, controller output, admission/defaulting, and admitted state;
3. **runtime evidence** — effective namespaces, identity, privilege, mediation, mounts, devices, sockets, credentials, and network state;
4. **control evidence** — neighboring workloads and counterfactuals that isolate the causal state difference.

## Isolation guarantee semantics

Write the guarantee before inspecting suspicious configuration. A useful guarantee identifies who is being contained, what capability must remain unavailable, and which layer is expected to enforce that separation.

Record at minimum:

```text
threat principal
isolation objective
protected host/workload/resource class
expected namespace separation
expected privilege ceiling
expected syscall/LSM mediation
expected mount/device/socket boundary
expected credential scope
expected network boundary
allowed controller/admission mutations
runtime-class/node assumptions
```

A guarantee is falsifiable. "Runs in a container" is not a guarantee. "A tenant build process must not receive a host-control socket, writable host-backed path, or credential scope outside its project" is a meaningful guarantee.

### Threat principal

Define the **threat principal** precisely: application process, compromised service, untrusted build step, tenant workload, plugin, generated code, sidecar, or another actor. The principal determines which already-granted capabilities count as expected trust and which count as a boundary violation.

### Isolation objective

The **isolation objective** is the exact separation claim under review. State the forbidden capability in semantic terms rather than as a configuration keyword.

Examples of objective forms include:

- cannot observe host/peer process identity beyond the approved boundary;
- cannot write an unapproved host-backed path;
- cannot access a runtime or node-control interface;
- cannot receive credentials outside the workload identity scope;
- cannot reach a neighboring protected synthetic service class;
- cannot gain a broader privilege envelope through controller/admission/runtime mutation.

### Requested state

The **requested state** is what the workload or controller asks the platform to create. Preserve the relevant security fields exactly enough to compare later: identity, namespace sharing, privilege mode, capabilities, security profiles, user namespace behavior, mounts, mount propagation, devices, sockets, service account behavior, network attributes, and runtime class.

Requested state shows intent. It does not prove what runs.

### Admitted state

The **admitted state** is the workload after defaulting, mutation, validation, policy engines, and controller expansion. Attribute every policy-relevant change to the responsible component when possible.

A mutation can narrow privilege, widen privilege, attach identity, change runtime class, inject storage, or create a documented exception. The review question is whether the resulting admitted state still satisfies the isolation objective and whether later runtime behavior preserves it.

### Effective runtime state

The **effective runtime state** is the state actually enforced for the running workload. Collect only what is necessary to answer the objective, using read-only sources where possible.

Relevant runtime dimensions can include:

- effective UID/GID and user namespace mapping;
- namespace membership and sharing;
- effective/permitted/bounding capability state;
- no-new-privileges and privilege mode;
- attached seccomp/LSM policy;
- mount table and mount propagation;
- device exposure;
- runtime socket or other host interface visibility;
- projected/mounted credential exposure;
- network namespace, policy, proxy/mesh, and controlled reachability;
- runtime class, node pool, or sandbox implementation.

The effective runtime state is the central evidence layer. If it differs from requested or admitted state, identify the mutator or runtime behavior that produced the difference.

## Attack surface

Model the boundary as the composition of workload identity, namespace placement, runtime class, kernel privilege, filesystem exposure, device exposure, control interfaces, credentials, network reach, controller templates, admission policy, and cluster authorization.

For every surface, record both **what exists** and **what authority it represents**. A path, socket, capability, token, or route is only security-relevant when its semantics can be connected to the isolation objective.

## Hypothesis matrix

Turn broad concerns into falsifiable invariant hypotheses.

| Hypothesis class | Invariant question | Strong evidence | Main disambiguation |
| --- | --- | --- | --- |
| requested/admitted drift | did control-plane mutation create a broader state than authored policy permits? | requested vs admitted diff with mutator attribution | documented exception/default versus unintended mutation |
| admitted/runtime drift | did runtime execution differ from admitted security state? | admitted state + effective runtime state on pinned runtime/node | stale workload or different runtime class/node pool |
| namespace boundary | does namespace ownership cross the stated host/tenant separation? | effective membership + neighboring workload comparison | intentional shared namespace design |
| privilege envelope | does the principal gain a kernel-relevant operation beyond the objective? | identity/capability/NNP/profile composition + safe oracle | capability present but still mediated/irrelevant |
| host interface exposure | does a mount/device/socket expose authority forbidden by the objective? | effective interface state + semantic classification | harmless data mount versus control interface |
| credential scope | does the workload receive broader identity material than policy intends? | effective credential projection + policy simulation | token present but correctly scoped |
| network boundary | can the workload reach a protected synthetic class contrary to policy? | controlled receiver correlation + policy state | route exists but policy still denies traffic |
| controller consistency | does controller-generated state preserve the same invariant as the direct workload? | paired direct/controller effective state | different workload class intentionally uses different policy |

Every hypothesis should predict one specific state difference and one neighboring control that should behave differently.

## Runtime state model

Represent the reviewed workload as a sequence of policy and execution states:

```text
S0 threat principal + isolation objective
S1 requested state
S2 controller-expanded state
S3 admitted/defaulted state
S4 scheduled runtime class / node policy
S5 effective identity + namespace ownership
S6 privilege envelope + syscall mediation
S7 mounts + propagation + devices + host interfaces
S8 credential exposure + network boundary
S9 bounded observable capability
```

Not every platform exposes every state separately. Preserve the distinctions that matter to the reviewed invariant.

### State attribution

For each state change record:

- component responsible;
- revision/policy version;
- before/after security-relevant fields;
- whether the change narrows, preserves, or widens the guarantee;
- evidence source;
- relation to the isolation objective.

### Namespace ownership

**Namespace ownership** means more than listing namespace types. Record which principal and peer classes share PID, mount, network, user, IPC, UTS, or other relevant isolation domains and whether that sharing violates the objective.

A shared namespace can be intentional. Promotion requires a contradiction with the reviewed invariant, not merely presence of a sharing flag.

### Privilege envelope

Derive the **privilege envelope** compositionally from:

- effective identity and user namespace mapping;
- privileged mode;
- permitted/effective/bounding capabilities;
- no-new-privileges;
- seccomp policy;
- LSM policy;
- runtime restrictions;
- relevant filesystem/device/control-interface state.

Do not equate a capability name with a proven exploit path. The review asks whether the principal can perform a controlled operation that the isolation objective says must remain unavailable after all mediation is considered.

### Syscall mediation

**Syscall mediation** covers seccomp and LSM enforcement as actually attached to the workload. Record profile identity and effective attachment, not just source manifest intent.

Profile presence without attachment evidence is configuration evidence only. A validated finding requires a safe contradiction of the relevant invariant or a stronger effective-state proof.

## Kernel and host-interface binding

The strongest container-isolation evidence binds runtime policy to the kernel/host-facing interface actually available to the principal.

### Mount state and mount propagation

Record effective mount source/type, target, writeability, and **mount propagation** only where they matter to the objective. Distinguish:

- image/ephemeral data;
- projected configuration/secret material;
- host-backed data path;
- proc/sysfs-like views;
- control socket mount;
- device-related mount.

A host-backed mount is not automatically a vulnerability. Classify the authority it exposes and whether that authority violates the stated guarantee.

### Device exposure

**Device exposure** is policy-relevant when the workload can access a device class outside its intended workload contract or when the device interface materially changes the privilege boundary.

Use read-only inventory or synthetic device fixtures where possible. Do not attempt unsafe device operations to prove impact.

### Runtime socket and control interfaces

A **runtime socket** or equivalent node/control interface should be classified by authority. Record whether it is present, which principal can access it, whether access is read-only or control-capable, and whether such access is explicitly part of the trust model.

Do not invoke destructive or host-mutating operations. A controlled policy simulation, socket metadata plus authorization model, or disposable mock control endpoint is preferred.

### Credential exposure

**Credential exposure** includes projected service identity, mounted secrets, cloud/registry identity, client certificates, and synthetic equivalents. Record effective presence and intended scope separately.

Use policy simulation or synthetic resource classes to test scope. Do not access unrelated real data merely because a credential is present.

### Network boundary

The **network boundary** is the effective reachability and identity relation after network namespace, policy, proxy/mesh, node-local routes, and documented exceptions are applied.

A route or DNS result is not sufficient evidence of policy-violating reachability. Bind the test to a controlled receiver or deterministic policy oracle.

### Host-interface binding requirement

A strong host-interface claim connects:

```text
isolation objective
-> effective runtime state
-> interface or privilege actually available
-> controlled capability represented by that interface
-> neighboring control that lacks the capability
```

If the interface is intentionally granted, classify it as exposure/trust rather than an isolation defect unless a separate policy invariant prohibits it.

## Controlled validation

1. Pin cluster, node/runtime, controller, admission, policy, image, and workload revisions.
2. Create or select a disposable synthetic workload matching the reviewed class.
3. State the threat principal and isolation objective before dynamic inspection.
4. Capture requested state.
5. Capture controller-expanded/admitted state and attribute mutations/defaults.
6. Capture only the effective runtime state necessary to evaluate the invariant.
7. Compare requested, admitted, and effective state explicitly.
8. Exercise one boundary at a time with read-only inspection, policy simulation, mock services, synthetic markers, or other inert oracles.
9. Use one intended allowed neighboring workload and one denied neighboring workload under the same pinned environment.
10. When a controller is involved, compare controller-generated state with the equivalent direct synthetic workload if both are intended to share the same policy.
11. Promote evidence only when the effective state contradicts the isolation objective and controls rule out fixture/configuration error.
12. Stop once the smallest sufficient safe proof exists.

## Counterfactual controls

A **counterfactual** changes one isolation-relevant state while keeping the rest of the review comparable.

### Neighboring control

A strong **neighboring control** differs in one decision-relevant dimension, for example:

- same workload, one namespace-sharing state differs;
- same workload, one admission mutation differs;
- same workload class, one host interface is absent;
- same identity, one synthetic resource class changes;
- same controller template, direct versus controller-generated workload;
- same network path, approved versus protected synthetic receiver;
- same runtime policy, one node/runtime class changes only when that difference is the causal hypothesis.

### Requested/admitted counterfactual

If the hypothesis is admission drift, keep workload intent fixed and compare the state before and after admission. A policy-relevant widening should be attributable to a specific rule/default/controller path.

### Runtime counterfactual

If the hypothesis is runtime drift, hold admitted state fixed and compare effective state under the pinned expected runtime class versus the observed runtime context. Do not compare unrelated node pools and call the difference causal.

### Privilege counterfactual

Hold workload identity and application path fixed while changing one privilege-relevant condition in a disposable fixture. The predicted controlled capability should change only if that condition is causally relevant after syscall/LSM mediation.

### Host-interface counterfactual

Hold the workload class fixed and vary only the synthetic mount/device/runtime-socket exposure. This separates the authority carried by the interface from unrelated application behavior.

### Credential counterfactual

Hold workload execution fixed and compare the synthetic/policy-simulated resource decision with the intended versus neighboring protected resource class. This separates credential presence from credential over-scope.

### Alternative explanation

For every promoted finding, record at least one plausible **alternative explanation** and its control. Common alternatives include:

- stale workload from an earlier policy revision;
- a different runtime class or node pool;
- controller revision mismatch;
- documented exception or maintenance workload class;
- synthetic fixture accidentally granted broad permissions;
- admission/defaulting intentionally normalizes the field;
- policy simulation used the wrong identity or resource class;
- network proxy/mesh behavior explained the observed reachability.

Stronger wording does not compensate for missing disambiguation.

## False-positive controls

Use controls aligned to the isolation model:

- requested versus admitted versus effective state from the same workload instance;
- direct versus controller-generated equivalent workload;
- intended shared namespace versus neighboring isolated namespace;
- broad-looking capability with mediation intact versus a controlled capability actually enabled;
- host interface absent versus present in a disposable fixture;
- credential present versus policy-simulated scope;
- route exists versus controlled receiver is actually reachable;
- expected runtime class versus accidental different runtime class/node pool;
- documented exception path versus standard workload path.

Reject or downgrade a case when reviewed configuration, explicit trust, stale state, runtime-class difference, controller mismatch, documented exception, or an over-broad test fixture fully explains the observation.

A scanner label, manifest keyword, or capability string alone is never enough for a validated isolation claim.

## Evidence ladder

### Hypothesis

Use when source/configuration or requested/admitted state suggests a possible guarantee failure but effective runtime capability has not been safely established.

Record the suspected violated invariant and the missing runtime evidence.

### Observed

Use when a policy-relevant effective state or controlled capability is reproduced but causality, policy contradiction, or controls remain incomplete.

Examples include unexpected namespace membership, a broader mount, a runtime socket visible, a credential projected, or a protected synthetic service reachable when the owner-approved invariant is not yet fully established.

### Validated

Use only when:

- threat principal and isolation objective are explicit;
- requested, admitted, and effective runtime state are distinguished;
- the relevant namespace/privilege/mediation/interface/credential/network state is identified;
- the effective capability is demonstrated by a benign read-only/synthetic oracle;
- the capability contradicts the reviewed isolation invariant;
- positive and neighboring controls isolate the relevant state difference;
- material alternative explanations are addressed;
- intentional exposure is distinguished from product/orchestration/runtime defect.

### Regression verified

Use only after the fixed revision restores the invariant in effective runtime state, the intended neighboring workload remains functional, the denied neighbor remains denied, and the original causal state trace can no longer produce the prohibited controlled capability.

## Evidence capture

Preserve a compact but reconstructable ledger:

```text
case_id:
cluster_controller_admission_runtime_revisions:
threat_principal:
isolation_objective:
requested_state:
controller_expansion:
admitted_state:
runtime_class_and_node_policy:
effective_runtime_state:
namespace_ownership:
privilege_envelope:
syscall_mediation:
mount_state_and_mount_propagation:
device_exposure:
runtime_socket_or_host_interface:
credential_exposure:
network_boundary:
controlled_or_policy_oracle:
positive_control:
neighboring_control:
counterfactual_prediction:
alternative_explanation:
alternative_explanation_control:
configuration_vs_defect:
evidence_state:
causal_invariant_violation:
```

Evidence must identify the exact intended boundary and the effective state that contradicts it. Preserve state provenance so a reviewer can reproduce why the conclusion follows.

## Remediation checks

Prefer the smallest change that restores the violated invariant at the controlling layer rather than adding a superficial deny rule elsewhere.

Review whether remediation:

1. aligns controller templates with the intended workload class;
2. makes admission/defaulting behavior explicit and least-privilege;
3. ensures effective namespace ownership matches the policy;
4. narrows the privilege envelope without breaking required operations;
5. restores expected seccomp/LSM attachment and syscall mediation;
6. removes or narrows unnecessary host-backed mounts and mount propagation;
7. removes unnecessary device or runtime/control-interface exposure;
8. narrows credential projection and effective authorization scope;
9. restores intended network policy/reachability;
10. prevents runtime-class/node drift from silently widening the boundary where that is part of the cause;
11. preserves enough non-secret runtime evidence to audit future drift.

## Remediation proof

A remediation is proven by restoring the invariant in **effective runtime state**, not merely by editing a manifest.

### 1. Replay the original isolation state trace

Use the same synthetic threat principal, workload class, and pinned environment. Confirm where the fixed controller/admission/runtime path now preserves or restores the intended invariant.

### 2. Verify effective state

Re-capture requested state, admitted state, and **effective runtime state**. Confirm the policy-relevant field is actually narrowed at execution time.

### 3. Replay the prohibited controlled capability

Use the same benign synthetic/read-only oracle. Confirm the prohibited capability is unavailable for the intended reason, without attempting host compromise or unrelated access.

### 4. Preserve the positive neighbor

The intended workload must continue to perform the allowed synthetic operation. A fix that disables the workload entirely is not a valid isolation remediation.

### 5. Preserve the denied neighbor

The neighboring denied workload/resource/interface class must remain denied. This guards against a change that merely moves the gap.

### 6. Recheck causal neighbors

Choose regressions based on the original cause:

- admission drift -> direct and controller-generated workloads;
- namespace issue -> intended shared and isolated neighboring classes;
- privilege issue -> neighboring capability/profile state;
- mount propagation issue -> approved mount plus forbidden neighboring propagation/exposure;
- device exposure -> intended device assignment plus protected device class;
- runtime socket issue -> ordinary workload plus explicitly trusted maintenance class;
- credential issue -> intended synthetic resource plus protected neighboring resource;
- network issue -> approved receiver plus protected synthetic receiver.

Regression verification requires the effective isolation guarantee to hold across these causal neighbors, not just one textual configuration.
