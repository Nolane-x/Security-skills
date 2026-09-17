---
name: deserialization-trust-analysis
description: "Analyze how serialized or structured untrusted data becomes typed objects, callbacks, paths, classes, templates, commands, policies, or privileged actions. Use for unsafe polymorphism, object reconstruction, schema confusion, gadget-like side effects, or trust promotion during decoding."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Deserialization Trust Analysis

Deserialization review is a reconstruction-trust problem, not merely a parser checklist. Serialized representation may pass syntax and schema checks while still selecting the wrong runtime identity, acquiring behavior that the sender was never authorized to request, or surviving a lifecycle transition with stale authority.

## When to use

Use for object serializers, RPC codecs, YAML/XML/JSON frameworks with polymorphism, binary object formats, session/token payloads, saved models/configs, plugin manifests, persisted object graphs, and inter-service messages where decoded data can influence runtime types, callbacks, resource selection, policy, templates, paths, queries, or other behavior-bearing state.

## Preconditions

1. Work only on local, owned, sandboxed, benchmark/CTF, or explicitly authorized targets.
2. Pin the decoder/runtime version, parser configuration, schema version, registry/resolver state, and relevant policy generation.
3. Prefer synthetic serialized artifacts, fake identities, mock type registries, inert callback markers, read-only synthetic capabilities, and bounded reversible owner-controlled effects.
4. Do not require harmful payload behavior to prove a trust-promotion mismatch.

## Workflow

1. Identify the serialized artifact origin, transport/storage envelope, authenticated sender or owner, and the exact authority that authenticity is supposed to represent.
2. Trace framing, parser identity, canonical field state, schema identity/version, discriminator or variant selection, and every normalization step before type resolution.
3. Trace the type registry/resolver identity and generation, aliases, inheritance rules, namespace/package rules, plugin lookup, reflection, or other mapping that produces the canonical runtime type identity.
4. Trace object construction, object-graph placement, setters, constructors, post-load hooks, validators, callbacks, finalizers, resource openers, and plugin initialization without assuming that construction success authorizes their effects.
5. Trace secondary interpretation after reconstruction: paths, templates, expressions, queries, policy names, callback identifiers, plugin keys, or other fields that acquire semantics later than schema validation.
6. Separate payload authenticity from reconstructed authority. Record what the sender is authorized to encode, not merely whether the bytes are signed or integrity-protected.
7. Bind the requested reconstructed capability to the policy/allowlist decision and record the narrower effective reconstructed authority that reaches the privileged consumer.
8. Track schema, registry, policy, plugin, cache/session, persisted-object, and runtime generations so stale state cannot inherit current authority by assumption.
9. Validate with synthetic positive, negative, and counterfactual controls that vary one material identity or generation at a time.
10. Capture a bounded receipt/result tied to the same artifact/schema/type/authority tuple and verify remediation while preserving the intended neighboring data-only or explicit-schema flow.

## Causal reconstruction-trust model

Use this complete binding chain for claims that reach beyond attack-surface observation:

```text
serialized artifact origin -> transport/storage envelope identity -> authenticity/integrity context -> format/parser identity -> syntax and canonical field state -> schema identity and schema version -> discriminator/variant state -> type registry/resolver identity and registry generation -> resolved runtime type identity -> object construction path and object-graph identity -> constructor/setter/post-load hook state -> secondary interpretation state -> caller/request authority context -> requested reconstructed capability -> policy/allowlist decision -> effective reconstructed authority -> privileged consumer or behavior boundary -> bounded synthetic effect -> receipt/result binding -> schema/registry/object lifecycle generation
```

Every material transition used by a security claim needs evidence. Missing identity, policy, generation, or result binding lowers the evidence ceiling.

The following distinctions are invariants, not stylistic wording:

- parser acceptance != schema authorization
- schema validation != runtime type authorization
- discriminator/alias string != resolved runtime type identity
- registry lookup success != authorized registry binding
- textual allowlist match != canonical resolved type identity
- payload authenticity != capability authorization
- data ownership != authority to reconstruct behavior
- object construction != side-effect authorization
- constructor/hook reachability != security impact
- data field != later secondary interpretation
- requested reconstructed capability != policy-approved effective reconstructed authority
- current schema/registry/object generation != stale generation
- unexpected type selection != exploitability
- bounded marker effect != arbitrary code execution
- object graph reachability != authority to consume every reachable capability
- action success != receipt/result binding to the initiating causal tuple

## Reconstruction identity and type binding

Record the serialized selector only as a representation. Resolve it through normalization, schema rules, the exact registry/resolver, and the registry generation before naming the runtime identity:

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

Prefix, package, namespace, base-class, alias, or inheritance checks are evidence about a policy predicate, not proof of the final runtime identity. If the resolver can map the same apparent selector differently across registry generations, the generation is part of the security identity.

Object-graph position also matters. A correctly resolved object can still expose a capability that the initiating principal is not authorized to consume merely because that object is reachable from another reconstructed node.

## Construction, hooks, and secondary interpretation

Trace behavior acquisition separately from type selection:

```text
resolved runtime type
-> allocation/constructor
-> property/setter binding
-> post-load/validation hooks
-> callback/finalizer/resource opener
-> secondary interpretation
-> bounded consumer effect
```

An inert callback marker is sufficient to prove that a behavior boundary was crossed unexpectedly. Do not promote a marker callback to a claim of command execution, arbitrary code execution, host compromise, or broad exploitability.

Fields can change meaning after schema validation. A string validated as data may later be interpreted as a path, template, expression, query, callback identifier, policy name, module key, or plugin selector. The later consumer and its policy are part of the causal chain.

## Authenticity and reconstructed authority

Integrity and authentication answer who produced or protected an artifact under a particular mechanism. They do not automatically answer what behavior the producer is authorized to reconstruct.

Model authority as:

```text
artifact authenticity
+ sender/principal identity
+ authenticated purpose/scope
+ requested schema/type/capability
+ reconstruction policy
-> effective reconstructed authority
```

A correctly signed payload can still exceed its intended authority if the signing principal is allowed to assert data but not select a behavior-bearing type, callback, plugin, policy, or privileged resource. Conversely, if the sender is explicitly authorized for the exact reconstructed capability and all downstream bindings hold, authenticity can be relevant positive evidence.

## Lifecycle and generation reasoning

Track generation changes for schema deployments, registry/resolver tables, aliases, plugin/module reloads, allowlists, signing scopes, policy revisions, cache/session restoration, persisted-object migrations, service/runtime restarts, and capability revocation.

A stale serialized artifact is a distinct hypothesis after the authoritative schema, registry, policy, plugin, or object generation advances. Replaying it safely can test whether old authority survives by mistake; replay alone does not establish impact.

Generation-aware review must distinguish logical names from current identities. The same alias, schema name, plugin key, or object label can refer to a different authoritative generation later.

## Deserialization evidence ladder

### DT0 — surface mapped

A format, parser, schema, discriminator, registry, hook, secondary interpreter, or reconstruction consumer is identified. No trust-boundary failure is established.

### DT1 — identity or interpretation divergence observed

A schema, runtime type, registry generation, object path, hook state, secondary interpretation, or lifecycle difference is observed, but no incorrect policy acceptance is yet shown.

### DT2 — reconstruction or policy mismatch demonstrated

A controlled fixture shows that the resolved schema/type/registry/object path, secondary interpretation, or reconstruction-policy decision differs from the intended binding. No side effect is required.

### DT3 — inert wrong-context acceptance

A synthetic marker type, inert callback, mock plugin, read-only synthetic capability, or controlled object is accepted under a selector, principal, schema, registry generation, or lifecycle context that should be rejected.

### DT4 — bounded synthetic authority effect

The wrong-context reconstruction produces a reversible owner-controlled effect or returns a read-only synthetic capability through the exact consumer path under review. The result is bound to the initiating artifact/schema/type/authority tuple.

### DT5 — causal reconstruction-trust proof

DT5 requires DT4 plus artifact-origin/authenticity context, parser and canonical-field provenance, schema identity/version binding, discriminator-to-runtime-type resolution, registry identity and generation, construction/hook/secondary-interpretation trace, requested-to-effective authority binding, privileged-consumer identity, lifecycle control, receipt/result binding, at least one meaningful counterfactual, alternative-explanation elimination, and remediation regression that preserves intended neighboring behavior.

A parser success, suspicious class name, polymorphic feature, signed payload, hook definition, crash, or surprising type by itself cannot establish DT4 or DT5.

## Counterfactual proof

Prefer paired controls that alter one security-relevant variable while leaving the rest of the decode path stable:

- same bytes with an allowed neighboring discriminator;
- same schema and selector under a different registry generation;
- same discriminator with canonical resolution pinned to a different runtime type identity;
- same authenticated sender under a narrower reconstruction purpose;
- same runtime type with the inert hook disabled while data construction stays valid;
- same object graph with secondary interpretation constrained;
- same stale artifact before and after a schema/policy/registry generation change;
- same bounded result shape with a different correlation receipt;
- post-remediation intended data-only or explicit-schema flow remains valid.

A useful counterfactual changes the causal decision, not merely the payload formatting.

## Alternative explanations

Before promotion, eliminate plausible non-security explanations such as a test harness registering the wrong synthetic type, parser fallback/default-type behavior, schema migration artifacts, stale fixture caches, registry reload races, alias collisions, expected benign post-load callbacks, validation failure at an earlier layer, unrelated concurrent marker activity, debug-only permissive configuration, or receipt/log correlation mistakes.

If one of these remains plausible, record it and keep the evidence at the lower justified level rather than forcing a vulnerability conclusion.

## Evidence ceiling

The evidence ceiling is determined by the weakest unproven material link in the causal chain. DT0/DT1 can support investigation hypotheses; DT2 establishes a bounded reconstruction or policy mismatch; DT3 requires safe wrong-context acceptance; DT4 requires a causally bound bounded effect; DT5 requires end-to-end identity, authority, generation, counterfactual, alternative-explanation, and remediation proof.

Do not promote evidence merely because a scanner, model, serializer feature, class registry, signature, or callback looks dangerous. A debug-only permissive decoder can help explain architecture but cannot by itself prove a production reconstruction boundary.

## Evidence contract

A validated finding must show the attacker- or lower-authority-influenced serialized state, the exact parser/schema/type-resolution path, the runtime identity or later interpretation actually selected, the policy/authority mismatch, and a benign bounded observation with positive and negative controls. Preserve enough pinned state to replay the claim deterministically.

Regression-verified evidence additionally requires that remediation blocks the failing synthetic path while intended neighboring behavior still works under the current schema/registry/policy generation.

## Stop conditions

Stop or reduce the claim when runtime type selection is closed and side-effect free for the exact context, when the authenticated sender is explicitly authorized for the exact reconstructed capability, when a mismatch cannot be causally bound to the claimed consumer, or when proof would require harmful execution, unauthorized systems, real stolen credentials, production secrets, persistence, destructive actions, public-registry manipulation, or external side effects.

## Output

```text
artifact origin / envelope identity:
authenticity and represented authority:
parser / canonical field state:
schema identity / version:
discriminator / registry / generation:
resolved runtime type:
object construction / graph position:
hook and secondary interpretation:
requested vs effective reconstructed authority:
privileged consumer:
bounded result / receipt binding:
lifecycle generation:
positive / negative / counterfactual controls:
alternative explanations eliminated:
DT evidence level and ceiling:
remediation oracle:
```
