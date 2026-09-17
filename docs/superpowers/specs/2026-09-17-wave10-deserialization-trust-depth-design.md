# Wave 10 Profile #20 — Deserialization Trust Depth Design

## Status

Design authority for Wave 10 operator-depth profile #20. This profile deepens the existing canonical `deserialization-trust-analysis` skill without changing canonical metadata, graph edges, packs, routing domains, benchmark authority, agent-eval authority, superiority-court authority, or workflow semantics.

Base authority: `main@6b8e0f36fee255a985d39aa8178598d58e1e21ad`.

## Goal

Turn deserialization review from a checklist about formats, polymorphism, and hooks into a causal reconstruction-trust proof model. A reviewer must be able to explain exactly how serialized bytes or structured fields acquire schema meaning, runtime type identity, object-graph position, construction behavior, secondary interpretation, effective authority, and a bounded observable result before promoting evidence.

The profile must prevent common overclaims such as treating parser acceptance as authorization, treating a discriminator string as runtime type identity, treating a signed payload as trusted for every reconstructed capability, or treating an unexpected callback as proof of arbitrary code execution.

## Why this profile is the next gap

The registry already has nineteen profiles covering AI-agent security, authorization, browser-process boundaries, cache identity, canonicalization/namespaces, cloud IAM, confused deputy, connector/plugin trust, container isolation, driver surfaces, exploitability triage, multi-tenant isolation, prompt injection, RAG/memory isolation, secrets/token flow, SSRF boundaries, supply-chain review, tool confirmation, and web routing/middleware.

`deserialization-trust-analysis` is canonical, broadly reusable across RPC, configuration, session, object-storage, model-loading, plugin, and inter-service boundaries, but remains at metadata evidence stage `observed` and has no operator-depth registration. Its current workflow identifies decode layers, polymorphism, allowlists, side-effecting construction, and schema/runtime mismatch, but does not yet freeze causal identity, registry binding, lifecycle generation, authority attenuation, counterfactual proof, or an evidence ceiling.

## Selected approach

Three approaches were considered:

1. **Parser-hardening depth only.** Focus on syntax, framing, parser errors, recursion, and malformed payloads. Rejected because parser/protocol analysis already covers representation safety and would not deepen trust promotion.
2. **Unsafe-deserialization exploitability depth.** Focus on gadget chains and command/file/network side effects. Rejected because it overlaps exploitability triage, encourages unnecessarily risky proof, and is not required for deterministic causal validation.
3. **Causal reconstruction identity and authority depth.** Selected. It treats deserialization as a sequence of typed identity resolutions, construction transitions, behavior/capability acquisition, lifecycle generations, and bounded effects that can be proven using synthetic inert fixtures.

## Causal model

The binding chain is:

```text
serialized artifact origin
-> transport/storage envelope identity
-> authenticity/integrity context
-> format/parser identity
-> syntax and canonical field state
-> schema identity and schema version
-> discriminator/variant state
-> type registry/resolver identity and registry generation
-> resolved runtime type identity
-> object construction path and object-graph identity
-> constructor/setter/post-load hook state
-> secondary interpretation state
-> caller/request authority context
-> requested reconstructed capability
-> policy/allowlist decision
-> effective reconstructed authority
-> privileged consumer or behavior boundary
-> bounded synthetic effect
-> receipt/result binding
-> schema/registry/object lifecycle generation
```

Evidence must preserve every material transition used by the claim. Missing identity, authority, or lifecycle links lower the evidence ceiling.

## Core invariants

1. Parser acceptance is not schema authorization.
2. Schema validation is not runtime type authorization.
3. A discriminator, tag, alias, class name, or registry key is not itself the resolved runtime type identity.
4. A textual allowlist match is not sufficient if canonical type resolution can select a different runtime identity.
5. Payload authenticity or signature validity does not imply authorization for every reconstructed capability.
6. Data ownership is not equivalent to authority to select behavior-bearing runtime types.
7. Object construction success is not proof that constructor, setter, post-load, validator, finalizer, or callback side effects were authorized.
8. A field validated as inert data may acquire new semantics when later interpreted as a path, template, expression, query, policy name, callback, or plugin key.
9. Runtime type identity must be bound to the correct registry/resolver generation; stale aliases or reused identifiers cannot inherit current authority by assumption.
10. Schema version compatibility is not proof of equivalent security semantics.
11. Cached, restored, or replayed serialized state must not silently preserve authority across revocation, schema, registry, policy, or object-lifecycle generation changes.
12. A reconstructed object reference is not proof that the initiating principal is authorized to use every capability reachable from that object graph.
13. An unexpected benign hook execution is not arbitrary code execution, system compromise, or broad exploitability.
14. A bounded effect must be bound to the same artifact/schema/type/construction/authority tuple under review; unrelated concurrent behavior does not promote evidence.
15. Safe data-only or explicit-schema controls must preserve intended neighboring behavior while preventing unauthorized trust promotion.

## Required distinctions

The canonical skill and runbook must explicitly distinguish:

- serialized representation vs canonical field state;
- parser/format identity vs schema identity;
- schema validity vs runtime type authorization;
- discriminator/alias string vs resolved runtime type identity;
- registry lookup success vs authorized registry binding;
- type allowlist text vs canonical resolved type identity;
- payload authenticity vs capability authorization;
- data ownership vs authority to reconstruct behavior;
- object construction vs side-effect authorization;
- constructor/hook reachability vs security impact;
- data field vs later secondary interpretation;
- requested reconstructed capability vs policy-approved effective authority;
- current schema/registry/object generation vs stale generation;
- unexpected type selection vs exploitability;
- successful bounded marker effect vs arbitrary code execution;
- object graph reachability vs authorization to consume reachable capabilities;
- action success vs receipt/result binding to the initiating causal tuple.

## Reconstruction identity model

A review must record, where applicable:

- serialized artifact origin and owner;
- transport or storage envelope identity;
- authenticity/integrity mechanism and represented authority;
- concrete parser/format identity and configuration;
- normalized/canonical field state;
- schema identity and version;
- discriminator, variant, alias, or polymorphic selector;
- type registry/resolver identity and generation;
- resolved runtime type/class/variant identity;
- object-construction pathway;
- object-graph placement and ownership semantics;
- constructors, setters, post-load hooks, validators, callbacks, finalizers, resource openers, or plugin resolvers;
- secondary interpretation of fields after reconstruction;
- policy/allowlist decision context;
- requested and effective reconstructed capability;
- privileged consumer or behavior boundary;
- bounded result/receipt identity;
- schema, registry, policy, and object-lifecycle generations.

Synthetic identities and local fixtures are preferred. Real secrets, production data, and external services are not required.

## Type registry and schema binding

The review must trace:

```text
serialized selector
-> normalized selector
-> schema rule
-> registry/resolver lookup
-> canonical runtime type identity
-> registry generation
-> construction policy
-> constructed object identity
```

A string-prefix, namespace, package, alias, or inheritance-based allowlist must be evaluated against the final canonical runtime identity, not merely the pre-resolution selector.

## Construction and side-effect reasoning

The review must distinguish construction from authorized behavior:

```text
resolved runtime type
-> constructor/allocation path
-> setters/property binding
-> post-load/validation hooks
-> callbacks/finalizers/resource openers
-> secondary interpretation
-> bounded effect
```

A benign marker callback or inert sink is sufficient to prove a trust-promotion mismatch. No command execution, arbitrary file write, external network access, persistence, or destructive effect is required.

## Authenticity and represented authority

Represent authenticity separately from authority:

```text
artifact authenticity
+ sender/principal identity
+ purpose/scope of signing or storage authority
+ reconstruction policy
-> allowed schema/type/capability set
```

A correctly authenticated payload can still exceed the sender's intended authority if it selects a behavior-bearing type or capability outside the authenticated purpose.

## Lifecycle and generation model

Track generation changes for:

- schema version deployment;
- registry/resolver table changes;
- alias/type remapping;
- plugin/module reload;
- policy/allowlist update;
- credential or signing-scope revocation;
- cache/session restoration;
- persisted object migration;
- object graph reconstruction after restart;
- service/runtime restart;
- capability revocation.

A stale artifact accepted after an authoritative generation advances is a distinct hypothesis and requires generation-aware controls.

## Evidence ladder DT0–DT5

### DT0 — surface mapped

A deserialization format, parser, schema, polymorphic selector, registry, hook, or secondary interpreter is identified. No trust-boundary failure is established.

### DT1 — identity or interpretation divergence observed

A schema/type/registry/object/hook/generation difference is observed, but no incorrect policy or behavior acceptance is yet demonstrated.

### DT2 — reconstruction or policy mismatch demonstrated

A controlled fixture proves that the resolved schema, runtime type, registry binding, object construction path, secondary interpretation, or policy decision diverges from the intended binding. No side effect is required.

### DT3 — inert wrong-context acceptance

A synthetic marker type, inert callback, mock plugin, read-only synthetic capability, or controlled object is reconstructed or invoked under a selector/principal/schema/generation context that should be rejected.

### DT4 — bounded synthetic authority effect

The wrong-context reconstruction causes a reversible owner-controlled effect or returns a read-only synthetic capability through the exact consumer path under review. The result must be bound to the initiating artifact/schema/type/authority tuple.

### DT5 — causal reconstruction-trust proof

Requires DT4 plus:

- exact artifact-origin and authenticity context;
- parser and canonical field-state provenance;
- schema identity/version binding;
- discriminator-to-runtime-type resolution trace;
- registry/resolver identity and generation;
- object-construction and hook/secondary-interpretation trace;
- requested vs effective reconstructed authority;
- privileged-consumer identity;
- lifecycle-generation control;
- receipt/result binding;
- at least one meaningful counterfactual;
- elimination of plausible alternative explanations;
- remediation regression proving the failing synthetic path is blocked while intended neighboring behavior remains valid.

No evidence may be promoted to DT4/DT5 solely from parser acceptance, presence of a polymorphic feature, a suspicious class name, a signed payload, a hook definition, a crash, or a single surprising object type.

## Counterfactual controls

Across the profile, deterministic cases should exercise relevant patterns such as:

- same bytes, neighboring allowed discriminator;
- same schema, different registry generation;
- same discriminator, canonical resolver forced to a different type identity;
- same authenticated sender, narrower reconstruction purpose/scope;
- same runtime type, side-effecting hook disabled while data construction remains valid;
- same object graph, secondary interpreter removed or constrained;
- same stale artifact after policy/schema/registry generation advances;
- same bounded result with a different correlation/receipt identity;
- post-remediation intended data-only or explicit-schema flow still succeeds.

## Alternative explanations

The runbook must actively eliminate plausible alternatives such as:

- test harness registering the wrong synthetic type;
- parser fallback or default-type behavior unrelated to the hypothesis;
- schema migration artifact;
- stale cache/session fixture;
- registry reload race;
- alias collision in the test setup;
- benign post-load callback expected by design;
- validation failure occurring before the claimed trust boundary;
- marker effect produced by unrelated concurrent activity;
- debug-only permissive configuration;
- safe-mode control rejecting the payload for an unrelated syntax/schema reason;
- logging or correlation mismatch.

## Deterministic review cases

`skills/deserialization-trust-analysis/references/operator-review-cases.json` must contain at least these three cases.

### 1. `type-registry-binding`

Proves that a serialized discriminator/alias is bound through normalization, schema policy, resolver identity, registry generation, and canonical runtime type identity before construction is authorized.

### 2. `construction-hook-capability-binding`

Proves that an authenticated or syntactically valid object cannot acquire behavior-bearing constructor/post-load/callback capability broader than the sender/principal and reconstruction policy allow, using only inert markers or mock consumers.

### 3. `schema-registry-generation-binding`

Proves that schema, registry, policy, plugin, or persisted-object generation changes invalidate stale reconstruction authority while preserving the current intended explicit-schema/data-only flow.

## Machine-readable case contract

Each deterministic case must provide substantive string values for:

- `id`
- `hypothesis`
- `safe_oracle`
- `positive_control`
- `negative_control`
- `stop_condition`
- `remediation_oracle`
- `artifact_origin`
- `envelope_authentication_context`
- `format_parser_identity`
- `canonical_field_state`
- `schema_identity_version`
- `discriminator_state`
- `registry_resolver_identity`
- `registry_generation`
- `runtime_type_identity`
- `object_construction_path`
- `hook_callback_surface`
- `secondary_interpretation`
- `authority_context`
- `requested_reconstructed_capability`
- `policy_decision`
- `effective_reconstructed_authority`
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

The deep runbook must contain the common operator-depth sections plus deserialization-specific sections covering:

- Attack surface
- Hypothesis matrix
- Artifact origin and authenticity trace
- Parser and canonical-field trace
- Schema identity and version trace
- Discriminator and registry-resolution trace
- Runtime type and object-construction trace
- Hook/callback and secondary-interpretation trace
- Authority and reconstruction-policy trace
- Privileged-consumer and result trace
- Lifecycle/schema/registry generation trace
- Controlled validation
- False-positive controls
- Counterfactual controls
- Alternative explanations
- Evidence capture
- Evidence promotion and ceiling
- Remediation checks

## Safety boundary

All profile validation is limited to local/owned/sandboxed decoders, mock RPC/config/session services, deterministic benchmark fixtures, synthetic serialized artifacts, fake identities, inert callback markers, mock plugin/type registries, read-only synthetic capabilities, or bounded reversible owner-controlled effects.

Do not require gadget-chain development, command execution, arbitrary file writes, external network access, credential theft, production secrets, persistence, malware, destructive effects, public-registry manipulation, or unauthorized targets.

A permissive debug/test decoder may be used to understand architecture, but cannot by itself promote a claim about a production reconstruction boundary.

## Registry contract

Add exactly one `deserialization-trust-analysis` entry to `operator-depth/profiles.json`:

- `runbook`: `references/operator-runbook.md`
- `scenario_matrix`: `references/operator-review-cases.json`
- `lab_only`: `true`
- common required runbook sections unchanged

Registry schema remains version 2.

## Dedicated test contract

Add `tests/test_deserialization_trust_depth.py` with four groups:

1. canonical skill freezes the causal model, required distinctions, DT0–DT5 ladder, counterfactual discipline, and evidence ceiling;
2. runbook freezes deserialization-specific transition-level sections, safety boundary, alternatives, and evidence controls;
3. review matrix requires at least three cases, the three required IDs, all required fields, substantive textual values, safe bounded oracles, explicit stop conditions, and DT-level ceilings;
4. registry is additive, contains exactly one deserialization profile, points to the required artifacts, keeps `lab_only: true`, and has at least 20 profiles.

The test must be committed and observed RED before production behavior is implemented.

## Exact scope

The complete profile #20 PR must change exactly these nine paths:

1. `README.md`
2. `docs/operator-depth-contract.md`
3. `docs/superpowers/plans/2026-09-17-wave10-deserialization-trust-depth.md`
4. `docs/superpowers/specs/2026-09-17-wave10-deserialization-trust-depth-design.md`
5. `operator-depth/profiles.json`
6. `skills/deserialization-trust-analysis/SKILL.md`
7. `skills/deserialization-trust-analysis/references/operator-review-cases.json`
8. `skills/deserialization-trust-analysis/references/operator-runbook.md`
9. `tests/test_deserialization_trust_depth.py`

Explicitly out of scope:

- `skills/deserialization-trust-analysis/skill.meta.json`;
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

This profile does not provide unsafe gadget-chain recipes, claim arbitrary code execution from hook reachability, require production data, prove broad exploitability from type selection alone, or establish superiority over an external security system. It deepens causal review quality for authorized deserialization trust analysis only.
