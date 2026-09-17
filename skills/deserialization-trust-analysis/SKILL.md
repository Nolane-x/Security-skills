---
name: deserialization-trust-analysis
description: "Analyze how serialized or structured untrusted data becomes typed objects, callbacks, paths, classes, templates, commands, policies, or privileged actions. Use for unsafe polymorphism, object reconstruction, schema confusion, gadget-like side effects, or trust promotion during decoding."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Deserialization Trust Analysis

Deserialization review is a reconstruction-trust problem, not merely a parser checklist. Serialized representation can pass syntax and schema checks while still resolving to the wrong runtime identity, acquiring behavior outside the sender's authority, or carrying stale authority across a lifecycle transition.

## When to use

Use for object serializers, RPC codecs, YAML/XML/JSON frameworks with polymorphism, binary object formats, session/token payloads, saved models/configs, plugin manifests, persisted object graphs, and inter-service messages where decoded data can influence runtime types, callbacks, paths, templates, expressions, queries, policies, plugins, resource selection, or other behavior-bearing state.

## Preconditions

1. Work only on local/owned/sandboxed, benchmark/CTF, or explicitly authorized targets.
2. Pin decoder/runtime version, parser configuration, schema version, resolver/registry state, and relevant policy generation.
3. Prefer synthetic serialized artifacts, fake identities, mock type registries, inert callback markers, read-only synthetic capabilities, and bounded reversible owner-controlled effects.
4. Do not require harmful payload behavior to prove a reconstruction-trust mismatch.

## Workflow

1. Record serialized artifact origin, envelope identity, authenticated sender/owner, and the exact authority represented by authenticity or integrity protection.
2. Trace parser identity, canonical field state, schema identity/version, discriminator/variant selection, and normalization before type resolution.
3. Trace resolver/registry identity and generation through aliases, inheritance, namespace/package rules, plugin lookup, reflection, or other mapping to the canonical runtime type identity.
4. Trace object construction and graph placement separately from constructors, setters, post-load hooks, validators, callbacks, finalizers, resource openers, and plugin initialization.
5. Trace secondary interpretation where schema-valid data later becomes a path, template, expression, query, policy name, callback identifier, plugin key, or resource selector.
6. Separate payload authenticity from authorization to request a behavior-bearing type or reconstructed capability.
7. Bind requested reconstructed capability to reconstruction policy/allowlist decision and record the narrower effective reconstructed authority reaching the privileged consumer.
8. Track schema, registry, policy, plugin, credential-scope, cache/session, persisted-object, and runtime generations.
9. Validate using positive, negative, and transition-specific counterfactual controls that vary one material identity, authority, or generation at a time.
10. Bind any bounded result to the same artifact/schema/type/authority tuple with a deterministic receipt, then verify remediation preserves intended data-only or explicit-schema behavior.

## Causal reconstruction-trust model

For any claim above surface mapping, preserve this complete causal chain:

```text
serialized artifact origin -> transport/storage envelope identity -> authenticity/integrity context -> format/parser identity -> syntax/canonical field state -> schema identity and schema version -> discriminator/variant state -> type registry/resolver identity -> registry generation -> resolved runtime type identity -> object construction path and object-graph identity -> constructor/setter/post-load/validator callback state -> secondary interpretation state -> caller/principal/request authority context -> requested reconstructed capability -> reconstruction policy/allowlist decision -> effective reconstructed authority -> privileged consumer/behavior boundary -> bounded synthetic effect or read-only capability -> receipt/result binding -> schema/registry/policy/object lifecycle generation
```

Every material transition used by the claim needs direct evidence or a bounded control. Missing identity, authority, generation, consumer, or result binding lowers the evidence ceiling.

The following distinctions are invariants:

- parser acceptance != schema authorization
- schema validation != runtime type authorization
- discriminator/tag/alias/class-name text != resolved runtime type identity
- registry lookup success != authorized registry binding
- textual allowlist match != canonical resolved-type authorization
- payload authenticity/signature validity != authorization for every reconstructed capability
- data ownership != authority to select behavior-bearing runtime types
- object construction success != side-effect authorization
- constructor/hook reachability != broad exploitability
- data-field validation != authorization for later secondary interpretation
- requested reconstructed capability != policy-approved effective reconstructed authority
- schema version compatibility != equivalent security semantics
- registry/type identity != current registry generation
- persisted/cached/replayed object state != current policy/schema/registry/object generation
- object-graph reachability != principal authorization to consume every reachable capability
- benign bounded marker effect != arbitrary code execution
- action success != receipt/result binding to the initiating artifact/schema/type/authority tuple
- authenticated sender identity != unrestricted reconstruction purpose/scope

## Reconstruction identity and type binding

Treat serialized selectors as representations, not identities. Resolve the exact chain:

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

Prefix, namespace, package, inheritance, alias, or registry-key allowlists are evidence about predicates, not proof of the final runtime type. Authorization must be evaluated against canonical resolved identity and current registry generation.

Object-graph placement matters independently. A correctly resolved object can expose a reachable child capability that the initiating principal is not authorized to consume. Graph reachability alone cannot promote authority.

## Construction, hooks, and secondary interpretation

Trace behavior acquisition separately from type resolution:

```text
resolved runtime type
-> allocation/constructor
-> property/setter binding
-> post-load/validator hooks
-> callback/finalizer/resource opener
-> secondary interpretation
-> privileged consumer
-> bounded result
```

An inert marker is sufficient to prove that a behavior boundary was crossed unexpectedly. Do not promote an inert callback to command execution, arbitrary code execution, host compromise, or broad exploitability.

A field can change meaning after schema validation. Data later interpreted as a path, template, expression, query, callback identifier, policy name, module key, or plugin selector enters a new authorization transition with its own consumer and policy.

## Authenticity and reconstructed authority

Authenticity answers who produced or protected an artifact under a particular mechanism. It does not automatically authorize every behavior that reconstruction can select.

Use this authority model:

```text
artifact authenticity
+ sender/principal identity
+ authenticated purpose/scope
+ requested schema/type/capability
+ reconstruction policy
-> effective reconstructed authority
```

A correctly authenticated artifact can still exceed purpose-scoped authority if it selects a behavior-bearing type, callback, plugin, policy, or resource outside the sender's allowed reconstruction set. Conversely, exact authorization for the same canonical type/capability can serve as positive evidence when downstream bindings hold.

## Lifecycle and generation reasoning

Track authoritative generation changes for schema deployments, resolver/registry tables, alias remapping, plugin/module reloads, allowlists, signing or credential scope, policy revisions, cache/session restoration, persisted-object migration, runtime restart, and capability revocation.

A stale artifact accepted after any authoritative generation advances is a separate hypothesis. Logical name reuse does not prove identity continuity: the same alias, schema label, plugin key, or object name may bind to a different current identity or authority.

Generation-aware controls should keep parser/principal/request stable while advancing one authoritative generation at a time.

## Deserialization evidence ladder

### DT0 — surface mapped

A format, parser, schema, discriminator, registry, hook, secondary interpreter, lifecycle surface, or privileged consumer is identified. No trust-boundary failure is established.

### DT1 — identity or interpretation divergence observed

A concrete schema, runtime type, registry generation, object path, hook state, secondary interpretation, or lifecycle difference is observed, but incorrect reconstruction-policy acceptance has not been demonstrated.

### DT2 — reconstruction or policy mismatch demonstrated

A controlled fixture proves the resolved schema, runtime type, registry binding, object construction path, secondary interpretation, or policy decision diverges from the intended binding. No side effect is required.

### DT3 — inert wrong-context acceptance

A synthetic marker type, inert callback, mock plugin, read-only synthetic capability, or controlled object is reconstructed or invoked under a selector, principal, schema, registry generation, or lifecycle context that should be rejected.

### DT4 — bounded synthetic authority effect

Wrong-context reconstruction produces a reversible owner-controlled effect or read-only synthetic capability through the exact privileged consumer path. The result is bound to the initiating artifact/schema/type/authority tuple.

### DT5 — causal reconstruction-trust proof

DT5 requires DT4 plus exact artifact-origin/authenticity context, parser and canonical-field provenance, schema identity/version, discriminator-to-runtime-type resolution, registry/resolver identity and generation, object-construction and hook/secondary-interpretation trace, requested-to-effective authority binding, privileged-consumer identity, lifecycle control, receipt/result binding, a meaningful counterfactual, elimination of plausible alternative explanations, and remediation regression that preserves intended neighboring behavior.

Parser success, a polymorphic feature, suspicious class name, valid signature, hook definition, crash, or surprising object type cannot independently establish DT3–DT5.

## Counterfactual proof

Prefer paired controls that alter one causal transition while holding the remaining decode path stable:

- same canonical bytes with a neighboring allowed discriminator;
- same schema/selector under a different registry generation;
- same discriminator while canonical resolution maps to a different runtime type identity;
- same authenticated sender under a narrower reconstruction purpose/scope;
- same runtime type with the inert hook disabled while data construction remains valid;
- same object graph with secondary interpretation removed or constrained;
- same stale artifact before and after a schema/registry/policy generation change;
- same bounded result shape with a deliberately different receipt/correlation identity;
- post-remediation intended data-only or explicit-schema flow remains valid.

A broad fixture change that alters multiple identities or authorities cannot isolate root cause.

## Alternative explanations

Before DT3+ promotion, explicitly test plausible alternative explanation classes: harness registration error, parser fallback/default type, schema migration, stale fixture cache, registry reload race, alias collision, expected benign post-load behavior, earlier-layer validation divergence, unrelated concurrent marker activity, debug-only permissive configuration, safe-mode rejection for an unrelated syntax/schema reason, or receipt/log correlation error.

If a material alternative explanation remains open, keep evidence at the lower justified level.

## Evidence ceiling

The evidence ceiling is the weakest unproven material link in the causal chain. DT0/DT1 support investigation hypotheses; DT2 establishes a bounded reconstruction/policy mismatch; DT3 requires inert wrong-context acceptance; DT4 requires a causally bound bounded effect; DT5 requires end-to-end identity, authority, generation, consumer/result, counterfactual, alternative-explanation, and remediation proof.

Do not promote evidence because a scanner, model, serializer feature, class registry, signature, callback, or debug-only configuration looks dangerous. Debug behavior may explain architecture but does not by itself prove a production reconstruction boundary.

## Evidence contract

A validated finding must show lower-authority-influenced serialized state, exact parser/schema/type-resolution path, the canonical runtime identity or later interpretation selected, the policy/authority mismatch, the privileged consumer, and a benign bounded observation with positive and negative controls. Preserve pinned state sufficient for deterministic replay.

Regression-verified evidence additionally proves remediation blocks the failing synthetic path while intended neighboring behavior still succeeds under the current schema/registry/policy generation.

## Stop conditions

Stop or reduce the claim when runtime type selection is closed and side-effect free for the exact context, the authenticated sender is explicitly authorized for the exact reconstructed capability, the observation cannot be causally bound to the claimed consumer/result, or proof would require gadget-chain development, harmful execution, unauthorized systems, real credentials, production secrets, persistence, destructive actions, malware, evasion, public-registry manipulation, or external side effects.

## Output

```text
artifact origin / envelope identity:
authenticity / represented purpose:
parser / canonical fields:
schema identity / version:
discriminator / resolver / registry generation:
resolved runtime type:
object construction / graph placement:
hooks / secondary interpretation:
requested vs effective reconstructed authority:
privileged consumer:
bounded result / receipt binding:
lifecycle generation:
positive / negative / counterfactual controls:
alternative explanations eliminated:
DT evidence level and ceiling:
remediation oracle:
```
