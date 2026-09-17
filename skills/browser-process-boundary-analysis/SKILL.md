---
name: browser-process-boundary-analysis
description: "Analyze modern multi-process browser security boundaries in an authorized local build: renderer, browser, GPU, network, utility, extension, site isolation, IPC serialization, object routing, and brokered capabilities. Use for browser security review without assuming a renderer bug automatically becomes a sandbox escape."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Browser Process Boundary Analysis

Treat browser security as a chain of typed identities, lifecycle generations, policy decisions, and brokered capabilities. A renderer bug, IPC validation defect, privileged-service issue, browser-process authorization flaw, and host-level effect are distinct claims unless evidence connects each material hop.

## When to use

Use for browser engines, Electron-like shells, embedded webviews, site-isolated renderers, privileged utility services, extension/native messaging, shared-memory interfaces, brokered platform capabilities, or browser IPC reviews.

## Preconditions

Use only local instrumented browser builds, owned test shells, deterministic fixtures, or explicitly authorized environments. Prefer synthetic origins, fake process/object identities, mock brokers, inert capability sinks, read-only resources, and bounded reversible owner-controlled effects. Never test real users or third-party websites, use production profiles or credentials, or disable sandboxing as proof of a release-boundary finding.

## Causal browser-process model

Trace the complete security-relevant chain:

```text
request origin -> browser principal -> origin/site/frame security context -> site/process assignment -> process identity and process generation -> routed object/interface identity -> IPC schema plus normalized message state -> object ownership/lifecycle validation -> broker or privileged service identity -> requested capability/resource identity -> policy/authorization decision -> effective brokered authority -> privileged consumer/action -> bounded synthetic effect -> receipt/result binding -> lifecycle/revocation/process-generation state
```

A claim may stop at any proven point in this chain, but it must not silently infer later hops. Missing provenance lowers the evidence ceiling.

## Process, origin, and object identity

Keep these distinctions explicit:

- **process role != process identity** — two renderers of the same role are not interchangeable principals;
- **process identity != origin/site/frame identity** — process assignment is an implementation decision, not the security principal itself;
- **route/interface identifier != routed object identity** — a numeric or named route must resolve to the intended current object;
- **object reference != object ownership** — possession of an ID, handle, or endpoint does not prove the sender owns or may use it;
- **shared-memory access != resource authority** — mapping bytes does not imply authority over every referenced resource;
- **current object/process generation != stale generation** — reused IDs after navigation, restart, object destruction, or service restart must not inherit authority.

Record the process instance, process generation/start epoch, sandbox profile, site instance or browsing-context identity, frame/document generation, origin/security principal, routed object identity and generation, IPC endpoint, broker/service identity, target resource, policy decision, effective authority, and result correlation where applicable.

## IPC and routed-object validation

A valid message is not enough. Trace:

```text
sender process/context
-> schema and decoding
-> normalized message state
-> route/interface lookup
-> current object-generation lookup
-> ownership/authorization check
-> authoritative origin/site/frame lookup
-> capability/resource normalization
-> policy decision
-> privileged consumer
-> result/receipt
```

**message deserialization success != policy authorization**. Parsing, type checks, sequence validity, and generated-schema conformance prove only representation validity. They do not establish that the sender owns the routed object, carries the authoritative security context, or may request the capability.

## Brokered capability and authority

Model brokered authority as:

```text
caller represented authority
+ authoritative browser security context
+ requested operation/resource
+ broker policy
-> policy-approved effective capability
-> bounded privileged action
```

**ambient privileged-service authority != delegated request authority**. A browser, network, GPU, utility, extension, or native-messaging service may possess broad ambient privilege, but the initiating caller receives only the authority explicitly permitted by policy.

**requested capability != policy-approved effective capability**. Normalize operation and resource identities before the decision, and preserve the approved tuple through the privileged consumer and result.

## Lifecycle and generation reasoning

Track generation changes caused by navigation/document replacement, process swap, renderer reuse, crash/restart, object destruction/recreation, shared-buffer remapping, broker/service restart, extension/native-host reconnect, permission revocation, or cached policy/context refresh.

A stale route, object ID, handle, frame token, process ID, or cached context accepted after the authoritative generation advances is a separate hypothesis. Use paired synthetic old/current generations and prove which one the policy decision consumed.

## Browser-process evidence ladder

- **B0 — surface mapped:** process graph, sandbox profile, IPC channel, route, object, broker, or privileged consumer is identified; no boundary failure is established.
- **B1 — identity/context divergence observed:** a process, origin/site/frame, routed object, generation, or capability differs from the intended binding, but no policy mismatch is yet shown.
- **B2 — policy/routing mismatch demonstrated:** a controlled fixture shows the resolved object/context/capability or policy decision diverges from the intended binding without requiring a privileged effect.
- **B3 — inert wrong-context acceptance:** a benign synthetic marker, mock service, inert sink, read-only resource, controlled fixture, or canary is accepted under a process/origin/object/generation context that should be denied.
- **B4 — bounded synthetic authority effect:** wrong-context acceptance causes a reversible owner-controlled effect or returns a read-only synthetic resource through the exact broker/consumer path, with the result bound to the initiating tuple.
- **B5 — causal process-boundary proof:** B4 plus exact process/origin/site/frame provenance, route and object-generation binding, normalized IPC decision trace, broker/consumer identity, requested-vs-effective capability binding, ambient-vs-delegated authority separation, lifecycle/process-generation controls, a meaningful counterfactual, alternative-explanation elimination, and remediation regression preserving intended neighboring behavior.

## Counterfactual proof

Change one security-relevant identity at a time. Useful controls include the same IPC shape under a neighboring synthetic origin, the same origin under a different process generation, the same process role under a different instance, the same route number under a stale object generation, the same caller under a neighboring capability/resource, or the same result channel under a different correlation identity.

A remediation regression must block the failing synthetic tuple while preserving the intended current-process/current-object path.

## Alternative explanations

Before promoting evidence, eliminate plausible alternatives such as attaching to the wrong process instance, expected site/process reuse, expected navigation/process swap, route-number reuse after object destruction, stale logs or delayed telemetry, broker cache or policy propagation delay, benign retry behavior, shared-memory synchronization lag, synthetic fixture collision, extension/native-host reconnect semantics, or correlating a result from an unrelated concurrent request.

## Evidence ceiling

**renderer reachability != browser-process compromise** and neither implies host-level effect. Reachability, schema parsing, a crash, a permissive-looking interface, a debug-only endpoint, an unsandboxed development configuration, or a single surprising response cannot by itself establish B4 or B5.

Every claimed cross-process hop needs independent evidence. Debug-only or intentionally unsandboxed configurations may help map architecture but cannot prove a release-boundary violation.

## Workflow

1. Map the process graph, sandbox profiles, IPC endpoints, and brokered services.
2. Identify the authoritative origin/site/frame principal and current process/object generations.
3. Trace sender-controlled fields separately from authoritative browser-side context.
4. Resolve route/interface identifiers to current object identity and verify ownership/lifecycle checks.
5. Trace requested capability/resource normalization and the policy decision.
6. Separate caller represented authority from privileged-service ambient authority.
7. Bind the privileged consumer and bounded result to the initiating causal tuple.
8. Exercise paired synthetic counterfactual and lifecycle-generation controls.
9. Record alternative explanations and evidence ceiling before promotion.
10. Re-run the failing synthetic path after remediation while preserving intended neighboring behavior.

## Evidence contract

Preserve browser/build identity, process role and instance, process generation, sandbox profile, origin/site/frame context, IPC schema/channel, normalized message state, routed object identity/generation, ownership/authorization decision, broker identity, requested/effective capability, privileged consumer, bounded result, receipt/correlation identity, lifecycle generation, positive/negative controls, counterfactuals, and eliminated alternative explanations.

## Stop conditions

Stop when the process topology or sandbox profile differs materially from the claimed release, when proof would require a real-user profile, third-party site, production credential, public extension abuse, sandbox disabling, host privilege escalation, arbitrary code execution, persistent host modification, destructive action, evasion, malware, or any unauthorized target.

## Output

```text
browser/build:
request origin / browser principal:
origin-site-frame context:
process role / identity / generation:
sandbox profile:
ipc channel / normalized message state:
routed object / object generation:
ownership and authorization decision:
broker / requested capability-resource:
effective brokered authority:
privileged consumer:
bounded result / receipt binding:
lifecycle generation:
controls / counterfactuals:
alternative explanations:
evidence level and ceiling:
remediation regression:
```
