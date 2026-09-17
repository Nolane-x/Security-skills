# Wave 10 Profile #21 — Deserialization Trust Depth Design

## Status

Design authority for Wave 10 operator-depth profile #21, based on exact `main@e4979d27272ea059464b9285b5e452643b8f36f1` after closure of profile #20 (`boot-chain-and-secure-boot-analysis`).

Target canonical skill: `deserialization-trust-analysis`.

This change deepens an existing canonical capability. It does not add a new skill, alter `skill.meta.json`, graph edges, packs, routing domains, benchmark authority, agent-eval authority, superiority-court authority, workflow semantics, or the repository authorization boundary.

## Problem

The canonical skill already recognizes decode layers, polymorphic type selection, side-effecting construction, allowlists, integrity/authentication context, schema/runtime mismatch, and benign marker proofs. It remains observation-oriented, however. It does not force an operator to bind the exact serialized artifact and authenticity context to a canonical schema identity, resolver/registry generation, resolved runtime type, object-construction path, hook/secondary interpretation, represented authority, effective reconstructed capability, privileged consumer, bounded result, and lifecycle generation before promoting evidence.

That gap permits false promotions such as:

- parser acceptance being treated as schema authorization;
- schema validity being treated as runtime type authorization;
- a discriminator/alias string being treated as the resolved runtime type identity;
- textual allowlists being treated as canonical type binding;
- a correctly signed payload being treated as authorized for every behavior-bearing type or reconstructed capability;
- benign hook reachability being promoted directly to arbitrary code execution or broad exploitability;
- cached/restored serialized state being assumed current after schema, registry, policy, plugin, credential-scope, or object-lifecycle generations change;
- an observed bounded effect being attributed to the wrong serialized artifact or concurrent execution because receipt/result binding is missing.

Profile #21 therefore needs a causal reconstruction-trust model, transition-level identity and authority traces, deterministic benign controls, lifecycle generation reasoning, counterfactual proof, explicit alternative explanations, and a strict evidence ceiling.

## Why this profile and why now

The merge tree currently contains 20 CI-enforced operator-depth profiles. The twentieth profile deepens boot-chain root/policy/component identity, signer authority, rollback/freshness generations, verified-to-loaded binding, authenticated handoff, recovery equivalence, and BC0–BC5 evidence ceilings.

`deserialization-trust-analysis` remains an existing high-value canonical skill with metadata evidence stage `observed` and no operator-depth registration. It is broadly reusable across RPC codecs, configuration loaders, session/object stores, saved models, plugin systems, inter-service messages, and structured-data frameworks.

It is materially distinct from existing profiles:

- `canonicalization-and-namespace-analysis` focuses on representation-to-identity normalization and namespace resolution; profile #21 focuses on schema/type resolution, object construction, hooks, secondary interpretation, and behavior/authority acquisition.
- `authorization-boundary-analysis` focuses on whether an already identified action/resource is authorized; profile #21 proves how data reconstruction itself creates or selects behavior-bearing authority.
- `confused-deputy-analysis` focuses on delegated versus ambient authority at a deputy boundary; profile #21 focuses on authority represented by serialized state and the exact reconstruction policy that converts it into an effective capability.
- `connector-plugin-trust-analysis` focuses on integration permission/schema/response boundaries; profile #21 can include plugin/type resolvers as one reconstruction mechanism but remains format/schema/type/object specific.
- `secrets-and-token-flow-analysis` focuses on credential issuance, possession, propagation, and verifier decisions; payload authenticity here is only one input and never substitutes for reconstruction authorization.
- `supply-chain-dependency-review` and `boot-chain-and-secure-boot-analysis` focus on artifact provenance/signing/loading authority; profile #21 focuses on runtime reconstruction of structured state and acquired behavior/capability.
- `exploitability-triage` remains the authority for broader exploitability claims; profile #21 deliberately proves trust-promotion failures with inert or reversible effects without requiring command execution or gadget-chain development.

Compared with the certificate/hostname candidate considered for this slot, deserialization has broader cross-domain reuse and less semantic overlap with the new boot-chain profile's signing/trust-root/lifecycle model. Certificate/hostname remains a valid later Wave 10 promotion.

## Scope

Expected final PR scope is exactly nine paths:

1. `README.md`
2. `docs/operator-depth-contract.md`
3. `docs/superpowers/specs/2026-09-17-wave10-deserialization-trust-depth-design.md`
4. `docs/superpowers/plans/2026-09-17-wave10-deserialization-trust-depth.md`
5. `operator-depth/profiles.json`
6. `skills/deserialization-trust-analysis/SKILL.md`
7. `skills/deserialization-trust-analysis/references/operator-review-cases.json`
8. `skills/deserialization-trust-analysis/references/operator-runbook.md`
9. `tests/test_deserialization_trust_depth.py`

Explicitly out of scope unless an existing authority gate proves a real requirement:

- `skill.meta.json`;
- graph edges;
- packs;
- routing domains;
- benchmark fixtures or thresholds;
- agent-eval authority;
- superiority-court authority;
- CI workflow semantics;
- external superiority claims.

## Selected approach

Three approaches were considered.

### Parser-hardening depth only

This would focus on syntax, malformed input, recursion, parser errors, or framing. It is rejected because parser acceptance and memory-safety concerns are not the missing trust-promotion semantics.

### Exploit/gadget depth

This would focus on gadget chains, command execution, arbitrary file writes, or network side effects. It is rejected because it overlaps exploitability triage, raises unnecessary safety risk, and is not needed to prove an incorrect reconstruction boundary.

### Causal reconstruction identity and authority depth

Selected. Deserialization is modeled as a sequence of representation, schema, type identity, object construction, behavior acquisition, policy/authority, consumer, result, and lifecycle transitions. Each material transition can be frozen deterministically with synthetic inert fixtures.

## Causal model

The canonical causal chain is:

`serialized artifact origin -> transport/storage envelope identity -> authenticity/integrity context -> format/parser identity -> syntax/canonical field state -> schema identity and schema version -> discriminator/variant state -> type registry/resolver identity -> registry generation -> resolved runtime type identity -> object construction path and object-graph identity -> constructor/setter/post-load/validator callback state -> secondary interpretation state -> caller/principal/request authority context -> requested reconstructed capability -> reconstruction policy/allowlist decision -> effective reconstructed authority -> privileged consumer/behavior boundary -> bounded synthetic effect or read-only capability -> receipt/result binding -> schema/registry/policy/object lifecycle generation`

Evidence must preserve every material transition required by the claim. Missing identity, authority, consumer, result, or lifecycle bindings lower the evidence ceiling.

## Core distinctions and invariants

The canonical skill and runbook must preserve at least these distinctions:

1. `parser acceptance != schema authorization`.
2. `schema validation != runtime type authorization`.
3. `discriminator/tag/alias/class-name text != resolved runtime type identity`.
4. `registry lookup success != authorized registry binding`.
5. `textual allowlist match != canonical resolved-type authorization`.
6. `payload authenticity/signature validity != authorization for every reconstructed capability`.
7. `data ownership != authority to select behavior-bearing runtime types`.
8. `object construction success != side-effect authorization`.
9. `constructor/hook reachability != broad exploitability`.
10. `data-field validation != authorization for later secondary interpretation as a path/template/expression/query/policy/plugin key`.
11. `requested reconstructed capability != policy-approved effective reconstructed authority`.
12. `schema version compatibility != equivalent security semantics`.
13. `registry/type identity != current registry generation`.
14. `persisted/cached/replayed object state != current policy/schema/registry/object generation`.
15. `object-graph reachability != principal authorization to consume all reachable capabilities`.
16. `benign bounded marker effect != arbitrary code execution`.
17. `action success != receipt/result binding to the initiating artifact/schema/type/authority tuple`.
18. `authenticated sender identity != unrestricted reconstruction purpose/scope`.

Core invariants:

- runtime type authorization is evaluated against the final canonical resolved type and current registry generation;
- authenticity and represented sender authority are inputs to reconstruction policy, never blanket authorization for behavior;
- side-effecting hooks and secondary interpreters remain separate transitions with explicit policy and consumer binding;
- effective reconstructed authority cannot silently exceed the principal/purpose/schema policy authorized for the artifact;
- lifecycle-sensitive state cannot inherit authority across authoritative generation changes by assumption;
- bounded results are correlated back to the exact initiating reconstruction tuple before evidence promotion;
- intended data-only/explicit-schema behavior remains functional after remediation.

## Reconstruction identity model

A review records, where applicable:

- serialized artifact origin and ownership;
- envelope/transport/storage identity;
- authenticity or integrity mechanism and represented authority;
- parser/format identity and configuration;
- canonical field state;
- schema identity and version;
- discriminator/variant/alias selector;
- registry/resolver identity and generation;
- resolved runtime type/class/variant identity;
- object construction path and object-graph placement;
- constructors, setters, post-load hooks, validators, callbacks, finalizers, resource openers, or plugin resolvers;
- secondary interpretation after reconstruction;
- principal/request authority context;
- requested capability and reconstruction policy decision;
- effective reconstructed authority;
- privileged consumer/behavior boundary;
- bounded result/receipt identity;
- schema, registry, policy, credential-scope, plugin, and object-lifecycle generations.

## Type-registry and schema binding

The required identity trace is:

`serialized selector -> normalized selector -> schema rule -> registry/resolver lookup -> canonical runtime type identity -> registry generation -> construction policy -> constructed object identity`

String-prefix, namespace, package, alias, inheritance, or registry-based allowlists must be evaluated against final canonical runtime identity rather than only pre-resolution text.

## Construction and secondary interpretation

The behavior trace is:

`resolved runtime type -> allocation/constructor -> setters/property binding -> post-load/validator hooks -> callbacks/finalizers/resource openers -> secondary interpretation -> privileged consumer -> bounded result`

A synthetic marker callback, inert sink, mock plugin, or read-only synthetic capability is sufficient to prove a trust-promotion mismatch. Command execution, arbitrary file writes, external networking, persistence, or destructive effects are not required.

## Authenticity and represented authority

Authenticity is modeled separately from authority:

`artifact authenticity + sender/principal identity + signing/storage purpose/scope + schema/type policy + reconstruction policy -> authorized reconstructed capability set`

A correctly authenticated artifact may still exceed the sender's authority if it selects a behavior-bearing type or capability outside the authenticated purpose.

## Lifecycle and generation model

Track applicable generation changes for:

- schema deployment/version;
- registry/resolver table;
- alias/type remapping;
- plugin/module reload;
- policy/allowlist update;
- credential/signing scope revocation;
- cache/session restoration;
- persisted-object migration;
- object graph reconstruction after restart;
- service/runtime restart;
- capability revocation.

A stale artifact accepted after an authoritative generation changes is a distinct hypothesis and requires generation-aware controls.

## Evidence ladder DT0–DT5

### DT0 — surface mapped

A deserialization format, parser, schema, polymorphic selector, registry, hook, secondary interpreter, or lifecycle surface is identified. No trust-boundary failure is established.

### DT1 — identity or interpretation divergence observed

A concrete schema/type/registry/object/hook/generation difference is observed, but incorrect reconstruction-policy acceptance has not been demonstrated.

### DT2 — reconstruction or policy mismatch demonstrated

A controlled fixture proves that the resolved schema, runtime type, registry binding, object construction path, secondary interpretation, or policy decision diverges from the intended binding. No side effect is required.

### DT3 — inert wrong-context acceptance

A synthetic marker type, inert callback, mock plugin, read-only synthetic capability, or controlled object is reconstructed or invoked under a selector/principal/schema/generation context that should be rejected.

### DT4 — bounded synthetic authority effect

The wrong-context reconstruction causes a reversible owner-controlled effect or returns a read-only synthetic capability through the exact privileged consumer path. The result must be bound to the initiating artifact/schema/type/authority tuple.

### DT5 — causal reconstruction-trust proof

Requires DT4 plus exact artifact/authenticity context, parser/canonical-field provenance, schema identity/version, discriminator-to-runtime-type resolution, registry/resolver identity and generation, object-construction/hook/secondary-interpretation trace, requested versus effective reconstructed authority, privileged-consumer identity, lifecycle-generation control, receipt/result binding, at least one meaningful counterfactual, elimination of plausible alternative explanations, and remediation regression preserving neighboring intended behavior.

The evidence ceiling is always the highest level directly supported by captured transitions and controls. Parser acceptance, a suspicious class name, a signed payload, a hook definition, a crash, or a single surprising object type cannot independently justify DT3–DT5.

## Counterfactual proof

Cases select transition-specific counterfactuals such as:

- same bytes with a neighboring allowed discriminator;
- same schema with a different registry generation;
- same selector while the canonical resolver maps to a different runtime identity;
- same authenticated sender under a narrower reconstruction purpose/scope;
- same runtime type with side-effecting hook disabled while data construction remains valid;
- same object graph with the secondary interpreter removed or constrained;
- same stale artifact after schema/registry/policy generation advances;
- same bounded result with a different correlation/receipt identity;
- post-remediation explicit-schema/data-only flow still succeeding.

A counterfactual must isolate one causal transition. Broad fixture changes that alter several identities or authorities at once do not prove root cause.

## Alternative explanations

Before DT3+ promotion, the operator considers applicable alternatives including:

- harness registered the wrong synthetic type;
- parser fallback/default-type behavior is unrelated to the hypothesis;
- schema migration changed the fixture;
- stale cache/session fixture explains the result;
- registry reload race or alias collision occurred only in the test setup;
- the callback is expected by design and carries no unauthorized authority;
- validation failed or diverged before the claimed trust boundary;
- another concurrent action produced the marker/result;
- permissive behavior exists only in debug/test configuration;
- the safe-mode control failed for unrelated syntax/schema reasons;
- logging/correlation mismatch bound the result to the wrong artifact.

## Deterministic review cases

At least three benign synthetic cases are required.

### `type-registry-binding`

Proves a serialized discriminator/alias is bound through normalization, schema policy, resolver identity, registry generation, and canonical runtime type identity before construction is authorized.

### `construction-hook-capability-binding`

Proves that an authenticated or syntactically valid object cannot acquire behavior-bearing constructor/post-load/callback capability broader than the principal/purpose/reconstruction policy allows. Evidence uses inert markers or mock consumers only.

### `schema-registry-generation-binding`

Proves schema, registry, policy, plugin, or persisted-object generation changes invalidate stale reconstruction authority while preserving the current intended explicit-schema/data-only flow.

Every case includes the common operator-depth fields plus substantive domain fields for artifact origin, authentication context, parser identity, canonical fields, schema/version, discriminator, resolver, registry generation, runtime type, construction path, hooks, secondary interpretation, authority, requested capability, policy decision, effective authority, consumer, bounded result, receipt binding, lifecycle generation, counterfactual, alternative explanation, evidence level, and evidence ceiling.

## Runbook structure

The runbook must contain common required sections:

- `Attack surface`
- `Hypothesis matrix`
- `Controlled validation`
- `False-positive controls`
- `Evidence capture`
- `Remediation checks`

It additionally contains domain sections for artifact origin/authenticity, parser/canonical fields, schema/version, discriminator/registry resolution, runtime type/object construction, hooks/secondary interpretation, authority/reconstruction policy, privileged consumer/result, lifecycle generations, counterfactuals, alternative explanations, and evidence promotion/ceiling.

## Safety boundary

All validation is limited to local/owned/sandboxed decoders, mock RPC/config/session services, deterministic benchmark fixtures, synthetic serialized artifacts, fake identities, inert callback markers, mock plugin/type registries, read-only synthetic capabilities, or bounded reversible owner-controlled effects.

Stop before any proof requiring:

- gadget-chain development;
- command execution;
- arbitrary file writes;
- external network effects;
- real credentials or production secrets;
- persistence or malware;
- destructive action;
- public-registry manipulation;
- evasion;
- unauthorized targets.

A permissive debug/test decoder may help understand architecture but cannot by itself promote a production claim.

## TDD contract

The dedicated test is committed before production profile artifacts. Clean RED requires:

- dedicated semantic groups fail for missing new profile semantics/artifacts;
- zero unexpected unittest errors;
- pre-existing canonical-skill, 20-profile operator-depth, graph/index, benchmark, portability, agent-eval, and superiority-court authorities remain valid before the intended dedicated failure.

The dedicated test freezes four groups:

1. canonical skill causal model, distinctions, DT0–DT5 ladder, counterfactuals, alternatives, evidence ceiling, and safety boundary;
2. runbook transition methodology and required sections;
3. at least three substantive deterministic review cases with safe oracles, stop conditions, remediation oracles, and domain fields;
4. exactly one new registry entry, correct artifact paths, `lab_only: true`, registry schema version 2, and profile count increasing from 20 to 21.

The dedicated test is not weakened after valid RED merely to accommodate an incomplete implementation.

## Integration and closure gates

1. Start from exact `main@e4979d27272ea059464b9285b5e452643b8f36f1` on a dedicated branch.
2. Commit this design spec and self-review it for placeholders, contradictions, scope drift, and ambiguous evidence claims.
3. Commit an implementation plan.
4. Commit the dedicated test before production profile artifacts.
5. Open a Draft PR at exact test-first SHA and observe RED.
6. Implement the canonical skill, runbook, review cases, and one registry entry without changing public docs.
7. Require full behavioral GREEN across six OS/Python matrix jobs and `benchmark-core`, `agent-eval-core`, and `superiority-court-core`.
8. Lock the behavioral GREEN SHA as authority.
9. Only then update `README.md` and `docs/operator-depth-contract.md`.
10. Prove the post-GREEN delta is exactly those two docs and total PR scope exactly nine paths.
11. Run full CI on the exact final candidate SHA.
12. Create no further commit after exact-head GREEN.
13. Fresh-check current `main`, PR base/head, changed paths, mergeability, and base drift.
14. Mark Ready and merge only with `expected_head_sha=<exact-final-head>`.
15. Verify merge parent 1 equals pre-merge `main` and parent 2 equals exact final PR head.
16. Require post-merge push CI full GREEN on the exact merge SHA.
17. Read registry, README, and operator-depth contract directly on the merge SHA and record closure provenance.

## Success criteria

Profile #21 is complete only after all closure gates pass. Acceptable claims are deterministic internal contract conformance and stronger causal deserialization/reconstruction reasoning. No empirical claim that this repository beats an external system is permitted without an actual external contestant evaluated under the repository protocol.