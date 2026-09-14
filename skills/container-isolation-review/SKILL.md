---
name: container-isolation-review
description: "Review container isolation, runtime configuration, namespaces, capabilities, seccomp, mounts, devices, sockets, credentials, and host integration for owned or authorized deployments. Use to identify configuration and design paths that weaken intended tenant/workload isolation without attempting host compromise."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Container Isolation Review

Container isolation is not a property of a manifest keyword. It is a security guarantee produced by the composition of control-plane policy, admission mutation, runtime configuration, kernel isolation, mounted interfaces, credentials, network reachability, and the actual privileges available to the workload at execution time.

Review the guarantee that the deployment claims to provide, then compare that guarantee with the **effective runtime state**. Do not call a broad but intentionally granted configuration a runtime escape. Conversely, do not treat a restrictive-looking manifest as proof when admission, runtime defaults, host integration, or controller mutation produces a broader effective state.

Use only owned, local, sandboxed, benchmark, or explicitly authorized environments. Prefer source/configuration review, read-only runtime inspection, policy simulation, synthetic workloads, inert markers, and disposable namespaces. Do not alter host security controls, access unrelated tenant data, or attempt host compromise to prove a boundary issue.

## When to use

Use for Docker/containerd/CRI-style workloads, Kubernetes pods, CI/build runners, developer containers, service workloads, sandboxed agents, or other workloads that rely on operating-system or orchestrator isolation.

Use this skill when the security question involves one or more of these relations:

- declared workload intent versus admitted workload state;
- admitted state versus effective runtime state;
- workload identity versus namespace ownership;
- workload privilege versus kernel-mediated operation;
- mount/device/socket exposure versus intended host separation;
- credential exposure versus intended workload identity scope;
- workload network reach versus intended service/tenant boundary;
- controller/admission/runtime mutation versus the reviewed policy;
- a configuration exposure versus a defect in the product or isolation mechanism.

## Preconditions

1. Define the **threat principal**: ordinary application process, compromised service, untrusted build job, tenant workload, plugin, generated code, or another bounded actor.
2. Define the **isolation objective** before inspecting behavior: what host, peer workload, credential, device, network, or control-plane capability must remain unavailable to that principal.
3. Pin the relevant cluster, controller, admission, runtime, node-policy, image, and workload revisions.
4. Use read-only inspection or synthetic fixtures whenever possible. If proving stronger impact would require changing host state or reading unrelated data, stop at the strongest lower evidence state.
5. Separate intentionally granted capabilities from unintended boundary violations.

## Isolation guarantee model

Model the effective guarantee as a composition of states and enforcement layers rather than a checklist.

```text
threat principal P
isolation objective O
requested state Rq
admitted state Ra
effective runtime state Re
namespace ownership N
privilege envelope V
syscall mediation S
filesystem/mount state M
device and host-interface exposure H
credential exposure C
network boundary W
control-plane/runtime mutation D
-> bounded observable capability B
```

A finding exists when the effective capability available to the threat principal contradicts the stated isolation objective for the reviewed workload class and that contradiction is supported by controlled evidence.

### Threat principal

The **threat principal** is the actor whose available capability is being reasoned about. Avoid vague language such as "the container can" when the relevant distinction is the application UID, a process with a particular capability set, a sidecar, an init container, a debug workload, or a controller-authorized mutation path.

The same runtime state can be acceptable for a trusted maintenance workload and unacceptable for an untrusted tenant workload. Severity follows the principal and objective, not the keyword alone.

### Isolation objective

The **isolation objective** states the boundary that must hold. Examples include separation from host process identity, inability to write a host-backed path, inability to control the runtime API, inability to receive a broader credential set, or inability to reach a neighboring synthetic service class.

Make the objective falsifiable. "Secure container" is not an objective. "An untrusted build process must not receive a host-control interface or writable host-backed path" is testable.

### Requested state

The **requested state** is what the workload/controller asks the platform to create: namespace sharing, identity, privilege mode, capabilities, seccomp/LSM settings, mounts, devices, service account behavior, network attributes, runtime class, and related fields.

Requested state is evidence of intent, not proof of the effective guarantee.

### Admitted state

The **admitted state** is the policy-processed workload after defaults, mutation, validation, policy engines, and controller expansion have been applied.

Record policy-relevant differences between requested and admitted state. A mutation may narrow the boundary, widen it intentionally, or introduce drift. Do not infer runtime behavior until the effective state is also checked.

### Effective runtime state

The **effective runtime state** is what the workload actually runs with on the selected node/runtime. It includes effective namespace membership, IDs and identity mappings, privilege/capability state, no-new-privileges behavior, syscall/LSM mediation, mounts and propagation, device access, runtime/control sockets, credentials, network attachment, and runtime-class behavior.

When requested, admitted, and effective state differ, the finding must identify which component caused the difference and whether that difference violates the isolation objective.

### Namespace ownership

**Namespace ownership** describes which security-relevant namespaces the threat principal inhabits and who else shares them. Record PID, mount, network, user, IPC, UTS, and other relevant isolation domains when they matter to the objective.

A namespace-sharing flag is not automatically a defect. The question is whether the resulting membership crosses the stated workload/host/tenant boundary.

### Privilege envelope

The **privilege envelope** is the set of kernel-relevant operations the principal is permitted to request after accounting for process identity, capabilities, privilege mode, no-new-privileges, user namespace mapping, runtime settings, and security profiles.

Do not equate a single capability name with a proven boundary break. Relate the capability to the isolation objective and the other mediation layers that still constrain it.

### Syscall mediation

**Syscall mediation** is the effective set of kernel operations allowed or denied by seccomp and applicable LSM policy such as AppArmor/SELinux, interpreted together with the privilege envelope and runtime defaults.

Profile presence is not sufficient evidence; confirm which profile is effectively attached to the reviewed workload class and whether the relevant operation class is actually mediated as intended.

### Host interface

A **host interface** is any workload-visible object that exposes host, node, runtime, or control-plane authority: host-backed mounts, runtime/control sockets, device nodes, proc/sysfs views, debug/control endpoints, sidecar/gateway interfaces, or equivalent integration surfaces.

Classify each interface by semantics: read-only observation, data-plane access, device access, identity material, or control authority. Do not collapse all mounts or sockets into one severity class.

### Credential exposure

**Credential exposure** includes workload identity tokens, mounted secrets, registry/cloud credentials, projected identity material, metadata-derived identity, client certificates, or synthetic equivalents used during tests.

Separate "credential is present" from "credential grants broader capability than the isolation objective permits." Validate scope using policy simulation or synthetic resources rather than unrelated production data.

### Network boundary

The **network boundary** describes which controlled service or tenant classes the workload should be able to reach and under what identity. Evaluate runtime network namespace, policy enforcement, service-mesh/proxy behavior, node-local interfaces, and documented exceptions together.

A listening socket or route entry is not by itself proof of policy-violating reachability. Correlate a controlled request with a synthetic receiver or equivalent safe oracle.

### Control-plane drift

**Control-plane drift** is a policy-relevant difference introduced between authored intent and execution by controllers, admission, defaults, runtime class selection, node policy, debug/exec paths, or other authorized control-plane behavior.

Drift is important because a secure-looking source manifest may not represent the state actually executed. Attribute the mutation before assigning the defect to the wrong component.

## Runtime-state reasoning discipline

1. **Define the guarantee first.** State the threat principal and isolation objective before looking for suspicious flags.
2. **Trace three configuration states.** Compare requested state, admitted state, and effective runtime state; never substitute one for another.
3. **Reason about composition.** Namespace membership, capabilities, seccomp/LSM, mounts, devices, credentials, and network policy interact; a single broad field does not determine the whole guarantee.
4. **Bind privileges to operations.** A privilege matters only when it enables an operation relevant to the objective after all mediation layers are considered.
5. **Bind host interfaces to authority.** A mount/socket/device finding should state what controlled capability the interface exposes, not merely that the path exists.
6. **Separate exposure from defect.** An intentionally privileged maintenance workload is a risky configuration or trust choice unless a separate invariant says it must be isolated from that capability.
7. **Trace mutators.** Name the controller, admission rule, runtime default, or node policy responsible for every policy-relevant state difference.
8. **Use counterfactual reasoning.** Change one isolation-relevant dimension and predict which effective capability should change while neighboring intended behavior remains stable.
9. **Use neighboring controls.** Compare the same workload class with an approved and denied neighboring configuration under the same pinned environment.
10. **Search for alternative explanations.** Stale workloads, different node pools, runtime-class drift, test fixture over-grant, documented exception paths, or controller revision mismatch can mimic an isolation defect.
11. **Calibrate evidence.** Configuration keywords support hypotheses; effective state supports observations; a controlled contradiction of the isolation objective with matched controls supports validation.
12. **Stop at the first sufficient safe proof.** Do not attempt host compromise or access unrelated tenant data when a synthetic marker or read-only policy oracle proves the boundary.

## Workflow

1. Pin cluster, node/runtime, admission, controller, image, and policy revisions.
2. State the threat principal and isolation objective for the exact workload class.
3. Capture requested state.
4. Capture admitted state and attribute mutations/defaults.
5. Capture effective runtime state using read-only inspection where possible.
6. Map namespace ownership relevant to the objective.
7. Derive the effective privilege envelope from identity, capabilities, privilege mode, user namespace mapping, no-new-privileges, seccomp, and LSM policy.
8. Inventory mounts, mount propagation, devices, runtime sockets, proc/sysfs views, and other host interfaces; classify their authority semantics.
9. Record credential exposure and evaluate only against synthetic or policy-simulated resource scope.
10. Record the network boundary and use controlled receivers for any dynamic reachability confirmation.
11. Trace controller/admission/runtime mutations that explain requested→admitted→effective differences.
12. Establish one intended positive control and one neighboring denied control.
13. Change one state dimension at a time for counterfactuals.
14. Distinguish configuration exposure, policy drift, orchestration defect, runtime defect, and product defect before promotion.
15. Remediate the violated invariant at the narrowest controlling layer and replay the original trace plus neighboring controls.

## Operator depth

For a full authorized review, load the [operator runbook](references/operator-runbook.md). It expands the guarantee model into requested/admitted/effective state, namespace ownership, privilege composition, syscall mediation, mount propagation, device and runtime-socket exposure, credential/network boundaries, control-plane drift, counterfactual controls, evidence calibration, and remediation proof.

The [operator scenarios](references/operator-scenarios.json) retain the existing three scenario classes while adding an explicit isolation-state trace, violated invariant, false-positive guard, evidence-upgrade rule, and neighboring regression requirement.

## Evidence ladder

### Hypothesis

Use when requested/admitted configuration, source review, or policy composition suggests that an isolation objective may not hold but the relevant effective capability has not been safely confirmed.

Record the suspected layer and the missing evidence. Example: a controller appears able to inject a host interface, but the effective workload state has not yet shown that the interface is present.

### Observed

Use when a policy-relevant effective runtime state or controlled capability is reproduced, but the contradiction with the isolation objective, causal component, or false-positive controls remain incomplete.

Examples include unexpected namespace sharing, a broader-than-expected mount, a runtime socket present in the synthetic workload, or a controlled resource authorization that is broader than expected.

### Validated

Use only when:

- the threat principal and isolation objective are explicit;
- requested, admitted, and effective runtime state are distinguished;
- the relevant namespace/privilege/mediation/interface/credential/network state is identified;
- a benign read-only or synthetic oracle proves the policy-relevant effective capability;
- an intended positive control shows the workload class remains healthy;
- a neighboring denied control or counterfactual isolates the causal state difference;
- material alternative explanations are addressed;
- the classification distinguishes intentional exposure from an unintended defect.

### Regression verified

Use only after remediation when the original isolation-state trace is blocked or narrowed for the intended reason, the approved neighboring workload remains functional, the denied neighboring state remains denied, and the effective runtime state now matches the reviewed isolation invariant.

## Evidence contract

A strong finding is an isolation-invariant statement:

> For threat principal P, objective O requires invariant I. Requested state Rq becomes admitted state Ra through mutator M and effective runtime state Re on runtime/node N. Re exposes controlled capability C because isolation layer L does not enforce I. Neighboring control K differs only in decision-relevant state D and does not expose C. Alternative explanation A is excluded by control B.

Record configuration and runtime evidence separately. A scanner label, manifest keyword, or theoretical capability name alone is not sufficient for a validated isolation claim.

## Stop conditions

Stop or downgrade when:

- the threat principal or isolation objective is undefined;
- the observed capability is explicitly part of the reviewed trust model and violates no separate invariant;
- effective runtime state cannot be tied to the reviewed workload/revision;
- stronger proof would require changing host security controls or host state;
- proof would require unrelated tenant data, real secrets, or non-disposable production resources;
- a stale workload, different runtime class/node pool, test fixture over-grant, documented exception, or controller revision mismatch explains the observation;
- a synthetic/read-only proof already establishes the boundary and further action would add risk rather than evidence.

## Output

```text
case_id:
threat_principal:
isolation_objective:
cluster_controller_runtime_revisions:
requested_state:
admitted_state:
effective_runtime_state:
namespace_ownership:
privilege_envelope:
syscall_mediation:
mount_and_propagation_state:
device_exposure:
host_interfaces:
credential_exposure:
network_boundary:
control_plane_drift:
controlled_capability_or_oracle:
positive_control:
neighboring_control:
counterfactual:
alternative_explanations_checked:
configuration_vs_defect:
evidence_state:
causal_invariant_violation:
remediation_invariant:
regression_neighbors:
```
