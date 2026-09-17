# Deserialization Trust Analysis — Operator Runbook

Use this runbook only for local, owned, sandboxed, benchmark/CTF, or explicitly authorized systems. The objective is causal reconstruction-trust validation using synthetic serialized artifacts, mock registries and services, inert callback markers, read-only synthetic resources, and bounded reversible effects. It is not a recipe for unsafe gadget development or harmful execution.

## Attack surface

Inventory every place structured or serialized state crosses a trust boundary: network/RPC messages, uploaded documents, session or token payloads, cache entries, databases, local config, saved application state, persisted object graphs, model/config loaders, plugin manifests, message queues, clipboard/import formats, and inter-service envelopes.

For each surface, record the concrete parser/format implementation, schema identity and schema version, polymorphic selector or discriminator, registry/resolver, registry generation, object-construction mechanism, post-load hooks, secondary interpreters, reconstruction policy, and final privileged consumer. Reachability alone is DT0.

## Hypothesis matrix

Write a falsifiable hypothesis before testing. Each hypothesis must name the expected authoritative tuple and the single mismatch under review. Useful classes include:

| Hypothesis class | Intended invariant | Safe control |
| --- | --- | --- |
| Type binding | normalized selector + schema + registry generation resolves only to an authorized runtime type identity | neighboring synthetic allowed type |
| Hook capability | construction/post-load behavior stays within the sender's approved reconstructed authority | inert callback disabled or safe data-only mapping |
| Secondary interpretation | a field validated as data cannot silently acquire broader path/template/query/plugin semantics | same object with secondary interpreter constrained |
| Lifecycle | stale schema/registry/policy/object generations do not inherit current authority | current-generation synthetic artifact |
| Authenticity scope | signed/authenticated payload authority is limited to its declared purpose | same sender with narrower synthetic scope |

Do not define the hypothesis as “serializer is dangerous.” Define the exact transition expected to differ.

## Artifact origin and authenticity trace

Record where the artifact came from, which principal or synthetic fixture controls each field, the transport/storage envelope identity, and the authenticity/integrity mechanism. State what that mechanism actually authorizes.

A valid signature or authenticated envelope is not blanket reconstruction permission. Distinguish artifact authenticity from capability authorization and record the sender's allowed schema/type/capability scope. If authenticity is absent, say so rather than inferring an identity.

## Parser and canonical-field trace

Pin the concrete parser implementation and configuration. Record framing, syntax acceptance, duplicate-key behavior if relevant, normalization, default insertion, alias expansion, case/Unicode/canonicalization rules, and the canonical field state presented to schema/type resolution.

Parser acceptance is representation evidence only. Preserve the canonical field state so a later mismatch cannot be attributed to a different parse result.

## Schema identity and version trace

Record schema identity, schema version, compatibility/migration rules, variant/discriminator declarations, permitted unknown fields, and where schema validation occurs relative to canonicalization and type lookup.

Schema validity does not prove runtime type authorization. If two compatible schema versions have different security semantics, treat their versions as distinct identities and include the transition in lifecycle evidence.

## Discriminator and registry-resolution trace

Trace the exact selector from serialized representation through normalization and schema policy into the type registry/resolver. Record aliases, namespace/package rules, inheritance/base-class checks, reflection/plugin lookup, the resolver identity, and the registry generation.

The security-relevant output is the canonical runtime type identity, not merely the incoming class name, tag, alias, or registry key. A textual allowlist must be evaluated against the final resolved identity.

## Runtime type and object-construction trace

Record the resolved runtime type identity, allocation/constructor path, object identity, object-graph placement, ownership semantics, setters/property binding, and any factories or dependency injection involved in reconstruction.

Object construction is not side-effect authorization. Also record whether reachable child objects expose capabilities beyond the initiating principal's reconstructed authority.

## Hook/callback and secondary-interpretation trace

Trace constructors, setters, post-load hooks, validators, callbacks, finalizers, resource openers, plugin initialization, and any later interpretation of reconstructed fields as paths, templates, expressions, queries, policy names, callback identifiers, module/plugin keys, or resource selectors.

Use an inert callback or mock consumer to prove an unexpected behavior boundary. A benign marker is sufficient; do not escalate proof to arbitrary execution. Record secondary interpretation as a separate transition because schema-valid inert data may acquire new semantics later.

## Authority and reconstruction-policy trace

Record caller/request authority, authenticated purpose/scope, requested reconstructed capability, policy or allowlist inputs, the policy decision, and effective reconstructed authority. The effective authority must be no broader than the exact tuple the initiating principal is permitted to request.

Separate data ownership from authority to select behavior-bearing types. Separate payload authenticity from authority to invoke a callback, plugin, resource opener, policy, template, or other privileged behavior.

## Privileged-consumer and result trace

Identify the final consumer or behavior boundary. Prefer a mock service, inert sink, read-only synthetic capability, or reversible owner-controlled effect. Record the bounded result and bind it to the initiating artifact, schema version, registry generation, runtime type identity, authority tuple, and request correlation identity.

A successful action without receipt/result binding may belong to another concurrent request and cannot promote the evidence ceiling.

## Lifecycle/schema/registry generation trace

Track schema version and generation, registry generation, resolver table changes, alias remapping, plugin/module reload, policy/allowlist revision, signing-scope revocation, cache/session restoration, persisted-object migration, service/runtime restart, and capability revocation.

For lifecycle hypotheses, pair a stale artifact/reference with a current-generation control while holding the rest of the fixture constant. Reuse of a logical alias, schema name, or object label does not prove continuity of authority.

## Controlled validation

Use deterministic, bounded fixtures. A preferred sequence is:

1. Pin parser, schema version, registry generation, reconstruction policy, and synthetic principal.
2. Run the intended positive control and capture the canonical type and inert result.
3. Change one security-relevant variable: discriminator, canonical type binding, sender scope, hook enablement, secondary interpreter, or lifecycle generation.
4. Capture parser/schema decisions separately from registry/type/policy decisions.
5. If the wrong context is accepted, use only an inert callback, synthetic canary, mock plugin, read-only synthetic capability, or reversible fixture state to establish the bounded effect.
6. Bind every result to the exact causal tuple with a deterministic receipt.
7. Repeat after remediation and prove the intended neighboring flow remains valid.

Do not broaden the experiment merely to raise an evidence level.

## False-positive controls

Before promotion, verify that the observation is not caused by:

- a test harness registering the wrong synthetic type;
- parser fallback/default-type behavior unrelated to the hypothesis;
- schema migration or compatibility transformation;
- stale fixture cache/session state;
- registry reload race or alias collision;
- an expected benign hook documented by the application;
- rejection or mutation at an earlier parse/schema boundary;
- marker output from another concurrent request;
- debug-only permissive configuration;
- data-only mode failing for an unrelated syntax/schema reason;
- logging, timestamp, or receipt-correlation error.

Run at least one positive and one negative control that distinguish the hypothesis from the strongest plausible alternative explanation.

## Counterfactual controls

Use single-variable counterfactuals where possible:

- same canonical payload, neighboring allowed discriminator;
- same discriminator and schema, different registry generation;
- same selector with canonical resolver pinned to a neighboring runtime type identity;
- same authenticated synthetic sender with narrower allowed reconstruction scope;
- same runtime type with inert callback disabled but data construction preserved;
- same object graph with secondary interpretation disabled or narrowed;
- same stale artifact before and after schema/registry/policy generation advance;
- same result shape with an intentionally different receipt/correlation identity.

Counterfactual proof is strongest when parser/schema acceptance remains constant while the authoritative type or policy decision changes.

## Alternative explanations

Maintain an explicit list of alternative explanations and evidence that excludes each one. Do not silently discard a plausible explanation because the observed type or callback is surprising.

At minimum consider harness registration mistakes, schema migration, parser fallback, alias collision, registry reload races, benign post-load behavior, stale caches, debug-only configuration, concurrent marker effects, and result-correlation errors. If a material alternative explanation survives, cap the claim below causal proof.

## Evidence capture

Capture enough deterministic evidence to reconstruct the claim:

```text
artifact fixture identity and digest
artifact origin / synthetic principal
transport or storage envelope identity
authenticity mechanism and represented scope
parser implementation/configuration
canonical field state
schema identity and schema version
discriminator/variant state
registry/resolver identity and registry generation
resolved runtime type identity
object construction path and object-graph identity
hook/callback state
secondary interpretation state
requested reconstructed capability
policy decision and effective reconstructed authority
privileged consumer identity
bounded result and receipt/result tuple
lifecycle generations
positive/negative/counterfactual results
alternative explanations and eliminations
remediation revision and regression result
```

Prefer machine-readable fixture values and synthetic identifiers. Do not collect production secrets or third-party data when a controlled fixture can establish the same transition.

## Evidence promotion and ceiling

Apply the DT0–DT5 ladder conservatively:

- **DT0:** surface mapped only.
- **DT1:** identity/interpreter/generation divergence observed.
- **DT2:** bounded reconstruction or policy mismatch demonstrated.
- **DT3:** inert wrong-context acceptance demonstrated.
- **DT4:** bounded synthetic authority effect causally bound to the initiating tuple.
- **DT5:** DT4 plus full artifact/parser/schema/type/registry/construction/authority/generation/result provenance, counterfactual proof, alternative-explanation elimination, and remediation regression.

The evidence ceiling is the weakest unproven material link. Parser success, a polymorphic feature, a signed payload, a suspicious class, or hook reachability cannot by themselves establish DT4/DT5. Debug-only behavior can explain architecture but cannot prove a release-boundary condition.

## Remediation checks

Prefer fixes that reduce ambiguity at the causal boundary rather than merely blocking one serialized sample. Depending on the root cause, remediation can include explicit schema-to-data mapping, closed canonical type registries, resolver decisions on canonical type identity, purpose-scoped authentication, least-capability reconstruction, side-effect-free construction, delayed/authorized secondary interpretation, and generation-aware invalidation.

Regression verification must demonstrate both sides:

1. the previously accepted wrong-context synthetic artifact is now denied before unauthorized trust promotion; and
2. the intended neighboring data-only or explicit-schema behavior still succeeds under the current schema version, registry generation, and reconstruction policy.

Stop the experiment if validation would require real stolen credentials, production secrets, third-party accounts, command execution, arbitrary file writes, external network effects, persistence, malware, destructive behavior, public dependency/registry manipulation, or an unauthorized target.
