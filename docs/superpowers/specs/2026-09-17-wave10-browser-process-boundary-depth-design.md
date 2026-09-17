# Wave 10 Profile #19 — Browser Process Boundary Depth Design

## Status

Design authority for Wave 10 operator-depth profile #19. This profile deepens the existing canonical `browser-process-boundary-analysis` skill without changing canonical metadata, graph edges, packs, routing domains, benchmark authority, agent-eval authority, superiority-court authority, or workflow semantics.

Base authority: `main@82dab4efefcecc3bea86a2bdf523a3359dfb275c`.

## Goal

Turn browser multi-process review from a process/IPC checklist into a causal identity-and-authority proof model. A reviewer must be able to explain exactly how an unprivileged browser-side principal, origin/site context, process instance, routed object, IPC message, brokered capability, privileged consumer, sandbox state, and bounded result are connected before promoting evidence.

The profile must prevent common overclaims such as treating renderer reachability as browser-process compromise, treating message parsing as authorization, treating process type as principal identity, or treating a stale routed object as equivalent to the current object generation.

## Selected approach

Three approaches were considered:

1. **IPC parser depth only.** Focus on schemas, serializers, size/type checks, and parser failures. Rejected as too close to protocol/parser analysis and too weak on authority semantics.
2. **Sandbox-escape chain depth.** Focus on exploit chains from renderer to host. Rejected because it overlaps exploitability triage, encourages proof by escalation, and would make safe deterministic cases harder.
3. **Causal process-boundary identity and authority depth.** Selected. It treats browser security as a chain of typed identities, authority transitions, object generations, policy decisions, brokered capabilities, and bounded effects.

## Causal model

The binding chain is:

```text
external/request origin
-> authenticated or synthetic browser principal
-> origin/site/frame security context
-> site/process assignment
-> process identity and process generation
-> routed object/interface identity
-> IPC schema plus normalized message state
-> object ownership/lifecycle validation
-> broker or privileged service identity
-> requested capability/resource identity
-> policy/authorization decision
-> effective brokered authority
-> privileged consumer/action
-> bounded synthetic effect
-> receipt/result binding
-> lifecycle/revocation/process-generation state
```

Evidence must preserve every material transition used by the claim. Missing links lower the evidence ceiling.

## Core invariants

1. Process type is not process identity.
2. Process identity is not origin/site/frame identity.
3. A renderer-controlled field is not authority to use the referenced capability.
4. Message deserialization success is not policy authorization.
5. A valid route/interface identifier is not proof that the current sender owns the routed object.
6. Object identity must be bound to its lifecycle generation; stale IDs or reused handles cannot inherit current authority by assumption.
7. Site/origin context must survive cross-process propagation or be reconstructed from an authoritative source before a policy decision.
8. Brokered authority must be no broader than the policy-approved capability/resource tuple.
9. Shared-memory or command-buffer possession is not equivalent to ownership of every referenced object/resource.
10. Debug-only, test-only, privileged-development, or intentionally unsandboxed configurations cannot prove release-boundary impact.
11. A bounded effect must be bound to the same process/object/capability chain under review; unrelated concurrent effects do not promote evidence.
12. Restart, process swap, navigation, renderer reuse, crash recovery, BFCache-style restoration, extension reload, or service restart may create a new generation and must not silently preserve stale authority.
13. Browser-process or service ambient authority must be distinguished from delegated authority represented by the initiating request.
14. Cross-process chain claims require independent evidence for each hop; one proven hop cannot stand in for the full chain.

## Required distinctions

The canonical skill and runbook must explicitly distinguish:

- process role vs process instance identity;
- origin/site/frame identity vs process assignment;
- route/interface name vs routed object identity;
- parsing/schema validity vs policy authorization;
- object possession/reference vs object ownership;
- shared-memory access vs resource authority;
- sender-controlled fields vs authoritative browser-side context;
- broker identity vs caller identity;
- ambient privileged-service authority vs delegated request authority;
- requested capability vs policy-approved effective capability;
- current object/process generation vs stale generation;
- renderer reachability vs browser-process compromise vs host-level effect;
- successful action vs receipt/result binding to the initiating causal chain.

## Process and object identity model

A review must record, where applicable:

- process role;
- process instance identifier;
- process generation/start epoch;
- sandbox/profile identity;
- site instance / browsing context / frame or synthetic equivalent;
- origin/security principal;
- routed interface/object identifier;
- routed object generation/lifetime;
- IPC endpoint/channel identity;
- broker or privileged service identity;
- target capability/resource identity;
- policy decision context;
- resulting effective authority;
- bounded result or receipt identity.

Synthetic identifiers are preferred. Real user browsing state is not required.

## IPC and object-routing reasoning

The review must trace:

```text
sender process/context
-> message schema
-> normalization/decoding
-> route/interface lookup
-> object generation lookup
-> sender ownership or authorization check
-> security-context lookup
-> capability/resource normalization
-> broker/policy decision
-> privileged consumer
-> result/receipt
```

Schema correctness alone may establish only low-level observation. Evidence promotion requires identity and authority binding.

## Origin/site-context propagation

A reviewer must identify which component is authoritative for origin/site/frame context at the final decision point. Context copied from an untrusted process is insufficient unless independently validated.

Counterfactuals should vary one security-relevant identity at a time, such as same message with a neighboring synthetic origin, same origin with a different process generation, or same route number with a stale object generation.

## Brokered capability model

Represent brokered authority as:

```text
caller represented authority
+ authoritative security context
+ requested operation/resource
+ broker policy
-> approved effective capability
-> bounded privileged action
```

The approved effective capability must not exceed the intended tuple. Privileged consumer ambient authority must not be silently inherited by the caller.

## Lifecycle and generation model

Track generation changes for:

- renderer/process restart;
- process swap/site reassignment;
- frame/document/navigation lifetime;
- routed object/interface lifetime;
- shared-memory/buffer mapping;
- broker/service restart;
- extension/native-messaging host reload;
- permission/capability revocation;
- cached policy/context state.

A stale reference accepted after the authoritative generation advances is a distinct hypothesis and requires a generation-aware control.

## Evidence ladder B0–B5

### B0 — surface mapped

Process graph, IPC/channel, object route, sandbox profile, or broker surface is identified. No boundary failure is established.

### B1 — context or identity divergence observed

A process/origin/object/generation/capability difference is observed, but no policy or privileged-consumer mismatch is yet demonstrated.

### B2 — policy or routing mismatch demonstrated

The controlled fixture shows that the resolved process/object/context/capability or policy decision diverges from the intended binding. No privileged effect is required.

### B3 — inert wrong-context acceptance

A benign synthetic marker, mock service, inert capability sink, read-only resource, or controlled fixture is accepted under a sender/origin/object/generation context that should be rejected.

### B4 — bounded synthetic authority effect

The wrong-context acceptance causes a reversible owner-controlled effect or returns a read-only synthetic resource through the exact broker/consumer path under review. The result must be bound to the initiating causal tuple.

### B5 — causal process-boundary proof

Requires B4 plus:

- exact process/origin/site/frame identity provenance;
- route/interface and object-generation binding;
- IPC normalization and decision trace;
- broker/privileged-consumer identity;
- requested vs effective capability/resource binding;
- ambient-vs-delegated authority separation;
- lifecycle/process-generation control;
- at least one meaningful counterfactual;
- elimination of plausible alternative explanations;
- remediation regression proving the failing synthetic path is blocked while intended neighboring behavior remains valid.

No evidence may be promoted to B4/B5 solely from reachability, schema parsing, a crash, a permissive-looking interface, sandbox configuration, or a single surprising response.

## Counterfactual controls

At least one case should exercise each relevant pattern across the profile:

- same IPC shape, neighboring synthetic origin;
- same origin, different process generation;
- same process role, different process instance;
- same route/interface numeric value, different object generation;
- same request, narrower broker policy;
- same object, different requesting process;
- same caller, neighboring capability/resource;
- same action result, different receipt/correlation identity;
- post-remediation intended neighboring flow still succeeds.

## Alternative explanations

The runbook must actively eliminate plausible alternatives such as:

- debug-only or test-only privileged interface;
- expected site/process reuse;
- harness attaching to the wrong process instance;
- stale logging or delayed telemetry;
- expected navigation/process swap;
- route-number reuse after object destruction;
- broker cache or policy propagation delay;
- benign service retry;
- shared-memory synchronization lag;
- synthetic fixture collision;
- extension/native host reconnect semantics;
- result correlation to an unrelated concurrent request.

## Deterministic review cases

`skills/browser-process-boundary-analysis/references/operator-review-cases.json` must contain at least these three cases.

### 1. `origin-process-object-binding`

Proves that an origin/site/frame security context is causally bound to the correct process instance, routed object, and current object generation before the privileged side accepts the request.

### 2. `ipc-capability-broker-binding`

Proves that a syntactically valid IPC request cannot acquire broader brokered capability than the authoritative caller/context/resource tuple allows, and that privileged-service ambient authority is not inherited by the caller.

### 3. `process-generation-lifecycle-binding`

Proves that restart, process swap, route/object reuse, service restart, or revocation generation changes invalidate stale authority while preserving the current intended synthetic flow.

## Machine-readable case contract

Each deterministic case must provide substantive values for:

- `id`
- `hypothesis`
- `safe_oracle`
- `positive_control`
- `negative_control`
- `stop_condition`
- `remediation_oracle`
- `request_origin`
- `browser_principal`
- `origin_site_frame_context`
- `process_assignment`
- `process_identity`
- `process_generation`
- `sandbox_profile`
- `ipc_channel`
- `message_state`
- `routed_object_identity`
- `object_generation`
- `ownership_authorization_check`
- `broker_identity`
- `requested_capability_resource`
- `policy_decision`
- `effective_brokered_authority`
- `privileged_consumer`
- `bounded_result`
- `receipt_result_binding`
- `lifecycle_generation`
- `counterfactual_control`
- `alternative_explanation`
- `evidence_level`
- `evidence_ceiling`

Textual fields must be sufficiently substantive for deterministic tests and review, not placeholders.

## Runbook sections

The deep runbook must contain the common operator-depth sections plus browser-specific sections covering:

- Attack surface
- Hypothesis matrix
- Process graph and sandbox-profile trace
- Origin/site/frame context trace
- Process identity and generation trace
- IPC schema and normalized-message trace
- Routed object and lifecycle trace
- Ownership and authorization decision trace
- Brokered capability and resource trace
- Ambient-versus-delegated authority trace
- Privileged-consumer and result trace
- Lifecycle/revocation generation trace
- Controlled validation
- False-positive controls
- Counterfactual controls
- Evidence capture
- Evidence promotion and ceiling
- Remediation checks

## Safety boundary

All profile validation is limited to local instrumented browser builds, owned Electron/webview test shells, deterministic benchmark fixtures, synthetic origins/sites/frames, mock brokers, inert capability sinks, fake extension identities, read-only synthetic resources, or bounded reversible owner-controlled effects.

Do not require real-user browsing data, production browser profiles, third-party websites, real credentials, public extensions, persistent host modification, sandbox disabling as proof, privilege escalation, arbitrary code execution, evasion, malware, destructive effects, or unauthorized targets.

A debug-only or intentionally unsandboxed build may be used only to understand architecture, never to promote an evidence claim about a release boundary.

## Registry contract

Add exactly one `browser-process-boundary-analysis` entry to `operator-depth/profiles.json`:

- `runbook`: `references/operator-runbook.md`
- `scenario_matrix`: `references/operator-review-cases.json`
- `lab_only`: `true`
- common required runbook sections unchanged

Registry schema remains version 2.

## Dedicated test contract

Add `tests/test_browser_process_boundary_depth.py` with four groups:

1. canonical skill freezes the causal model, required distinctions, B0–B5 ladder, counterfactual discipline, and evidence ceiling;
2. runbook freezes browser-specific transition-level sections and safety/evidence controls;
3. review matrix requires at least three cases, the three required IDs, all required fields, substantive textual values, safe bounded oracles, stop conditions, and B-level ceilings;
4. registry is additive, contains exactly one browser-process profile, points to the required artifacts, keeps `lab_only: true`, and has at least 19 profiles.

The test must be committed and observed RED before production behavior is implemented.

## Exact scope

The complete profile #19 PR must change exactly these nine paths:

1. `README.md`
2. `docs/operator-depth-contract.md`
3. `docs/superpowers/plans/2026-09-17-wave10-browser-process-boundary-depth.md`
4. `docs/superpowers/specs/2026-09-17-wave10-browser-process-boundary-depth-design.md`
5. `operator-depth/profiles.json`
6. `skills/browser-process-boundary-analysis/SKILL.md`
7. `skills/browser-process-boundary-analysis/references/operator-review-cases.json`
8. `skills/browser-process-boundary-analysis/references/operator-runbook.md`
9. `tests/test_browser_process_boundary_depth.py`

Explicitly out of scope:

- `skills/browser-process-boundary-analysis/skill.meta.json`;
- graph edges;
- packs;
- routing domains;
- benchmark fixtures or thresholds;
- agent-eval authority;
- superiority-court authority;
- workflow semantics;
- external-vendor superiority claims.

## TDD and integration gates

1. Create isolated branch from exact base SHA.
2. Commit this design spec and self-review it.
3. Write and commit implementation plan.
4. Add dedicated test only.
5. Open Draft PR on exact test-first SHA.
6. Observe a clean RED: intended dedicated assertions fail, pre-existing validators/gates remain green, and there are no unittest errors.
7. Implement canonical skill, runbook, review cases, and registry entry without changing the dedicated test.
8. Require full behavioral GREEN across six matrix jobs and all three deterministic core jobs.
9. Lock the behavioral GREEN SHA as authority.
10. After behavioral GREEN only, update `README.md` and `docs/operator-depth-contract.md`.
11. Verify post-GREEN delta is exactly those two documentation paths.
12. Verify PR total scope is exactly the nine paths above.
13. Run full exact-head CI on the final candidate and require all jobs green.
14. Freshly verify head, base, scope, mergeability, and that `main` has not drifted.
15. Mark Ready and merge with an expected-head SHA guard.
16. Verify merge commit parents.
17. Require post-merge push CI on the exact merge SHA to be fully green.
18. Verify registry/docs at the merge SHA and write closure provenance to the PR.

## Non-goals

This profile does not claim browser exploitability, provide a sandbox-escape recipe, prove host compromise, or establish superiority over an external security system. It deepens causal review quality for authorized browser-process boundary analysis only.
