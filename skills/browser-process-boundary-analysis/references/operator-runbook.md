# Browser Process Boundary Operator Runbook

This runbook is for local instrumented browser builds, owned Electron/webview shells, deterministic benchmarks, synthetic origins and identities, mock brokers, inert sinks, read-only resources, and explicitly authorized targets only. It does not require or justify testing real users, third-party websites, production profiles or credentials, public extensions, host privilege escalation, arbitrary code execution, persistence, destructive actions, evasion, or malware.

## Attack surface

Map renderer, browser, GPU, network, storage, utility, extension, native-messaging, crash/update, and platform-broker processes. Record sandbox profile, process role, process identity, process generation, IPC endpoint, shared-memory surfaces, routed object/interface types, authoritative origin/site/frame state, brokers, privileged consumers, and bounded resources. A process graph is a map, not a finding.

## Hypothesis matrix

Write falsifiable hypotheses as transition failures rather than generic “IPC insecure” claims. Examples: a stale routed object generation is accepted by a current process; an untrusted sender-supplied origin overrides authoritative browser context; or a mock broker grants a wider synthetic capability than policy permits. For every hypothesis define the exact process/context/object tuple, safe oracle, paired current/neighbor control, expected decision, evidence ceiling, and stop condition.

## Process graph and sandbox-profile trace

Trace each process role to a concrete process instance and process generation. Capture the release-equivalent sandbox profile, OS-level restriction summary, relevant broker boundaries, and whether any debug-only or intentionally unsandboxed mode is enabled. Debug-only and unsandboxed configurations may explain architecture but are not release-boundary proof.

Do not infer identity from role names. Two renderer processes can have different site instances, origins, generations, ownership, and effective authority despite identical process roles.

## Origin/site/frame context trace

Record the authoritative origin/security principal, site instance or equivalent browsing-context grouping, frame/document identity, and navigation/document generation. Identify the component that supplies authoritative origin/site/frame context at the final policy decision. Values copied from a sender-controlled renderer are observations only until independently bound to authoritative browser state.

Use synthetic origins such as `https://tenant-a.test` and `https://tenant-b.test`; never require real browsing history or third-party sites.

## Process identity and generation trace

Record process instance identifier, process role, start epoch or synthetic generation, renderer reuse/process-swap state, and the event that advances generation. Treat crash/restart, process swap, renderer reuse, service restart, extension/native-host reconnect, and equivalent transitions as potential identity changes. A stale PID-like value or recycled process slot must not inherit current authority by assumption.

## IPC schema and normalized-message trace

Capture IPC endpoint/channel identity, schema/interface version, sender-controlled fields, decoder/normalizer decisions, and the normalized state actually consumed by routing and policy. Separate representation validity from authorization: successful decoding, type checks, sequence legality, or generated-schema validation do not establish ownership or permission.

## Routed object and lifecycle trace

Resolve route/interface IDs, handles, frame tokens, endpoint IDs, shared-buffer references, or synthetic equivalents to the current routed object identity and object generation. Record creation, ownership transfer if any, destruction, reuse, and generation advance. Route-number reuse after object destruction is an explicit alternative explanation and counterfactual target.

## Ownership and authorization decision trace

Record the ownership or sender-authorization check independently from route lookup. Identify which principal/process/context is authorized to reference the routed object and which authoritative state is used. A valid route identifier or object reference is not proof of ownership. A missing or stale ownership check can establish at most the evidence supported by the controlled decision trace.

## Brokered capability and resource trace

Represent the decision as caller represented authority + authoritative browser context + requested operation/resource + broker policy -> approved effective capability. Record the requested capability/resource identity before and after normalization and the exact policy result. The approved capability must be no broader than the authorized tuple.

Use a mock broker, inert capability sink, synthetic resource, or read-only controlled fixture. Do not invoke real host-sensitive operations for proof.

## Ambient-versus-delegated authority trace

Record the ambient authority held by the browser process, broker, utility service, native host, or other privileged consumer separately from authority delegated by the initiating request. Ambient authority is an implementation property of the service; it must not silently become caller authority.

Compare the requested operation/resource to the effective brokered authority actually passed to the privileged consumer. This distinction is required before B4 or B5 promotion.

## Privileged-consumer and result trace

Identify the privileged consumer/action and bind its bounded result to the initiating process, origin/site/frame context, routed object generation, capability/resource tuple, and request correlation identity. Preserve explicit receipt/result binding so the observed output is attributable to that same causal tuple. Prefer a read-only synthetic resource, inert marker, mock callback, or reversible owner-controlled state. A concurrent unrelated result cannot promote evidence.

## Lifecycle/revocation generation trace

Record generation changes for processes, frames/documents, routed objects, shared mappings, broker/service instances, extension/native hosts, permissions, cached policy state, and revocation. Exercise paired stale/current generations where relevant. A legitimate propagation delay must be measured and distinguished from stale-authority acceptance.

## Controlled validation

Use a deterministic local fixture. Start from a positive current-context flow, then change exactly one security-relevant identity: neighboring synthetic origin, different process instance, stale process generation, stale object generation, different requesting process, narrower broker policy, neighboring capability/resource, or mismatched receipt identity. Observe only mock, inert, controlled, canary, or read-only effects.

Stop immediately if the test would require sandbox disabling as proof, real credentials, a production profile, a third-party site, public extension abuse, host privilege escalation, arbitrary code execution, persistent modification, destructive effects, evasion, malware, or any target outside explicit authorization.

## False-positive controls

Confirm the harness attached to the intended process instance and generation. Verify expected site/process reuse, process-swap behavior, navigation state, route reuse, broker cache timing, shared-memory synchronization, service retry behavior, extension/native-host reconnect semantics, and telemetry freshness. Use unique synthetic marker and correlation IDs so a result from another request cannot be mistaken for the tested action.

## Counterfactual controls

Run meaningful paired controls: same IPC message under a neighboring synthetic origin; same origin under a different process generation; same role under another process instance; same route number under a stale object generation; same caller with a neighboring capability/resource; same request under narrower broker policy; and same result channel with a mismatched receipt/correlation identity. Remediation must preserve the intended current-process/current-object neighbor while rejecting the failing tuple.

## Alternative explanations

Actively eliminate wrong-process attachment, expected site/process reuse, expected navigation/process swap, route-number reuse after destruction, stale logging or delayed telemetry, broker cache or policy propagation delay, benign retries, shared-memory synchronization lag, synthetic fixture collision, extension/native-host reconnect semantics, and correlation to an unrelated concurrent request. Record unresolved alternatives explicitly and cap evidence accordingly.

## Evidence capture

Capture build/revision, release-equivalent sandbox profile, process role/identity/generation, authoritative origin/site/frame context, IPC channel/schema and normalized message state, routed object identity/generation, ownership/authorization decision, broker identity, requested capability/resource, policy decision, effective brokered authority, privileged consumer, bounded result, receipt binding, lifecycle generation, controls, and eliminated alternatives. Preserve synthetic IDs; secret or personal data is unnecessary.

## Evidence promotion and ceiling

Use the browser-process ladder strictly. B0 maps the surface. B1 records context/identity divergence. B2 proves routing or policy mismatch. B3 requires inert wrong-context acceptance. B4 requires a bounded reversible effect or read-only synthetic resource through the exact reviewed broker/consumer path. B5 additionally requires end-to-end identity provenance, object/process generation binding, normalized IPC decision trace, broker/consumer identity, requested-vs-effective capability binding, ambient-vs-delegated authority separation, lifecycle controls, a meaningful counterfactual, alternative-explanation elimination, and remediation regression.

Renderer reachability, parser acceptance, a crash, a permissive interface, debug-only behavior, an unsandboxed configuration, or a single surprising response cannot by itself establish B4/B5. Every claimed cross-process hop requires independent evidence.

## Remediation checks

Fix the causal boundary rather than hiding the oracle. Appropriate remediations may bind an IPC request to authoritative origin/site/frame context, current process/object generation, explicit ownership, normalized resource identity, or attenuated broker policy. Re-run the exact failing synthetic tuple and require denial or safe handling, then re-run the intended neighboring current-context flow and require success. Record the new lifecycle generation and verify no stale cache or reconnect path restores the old authority.
