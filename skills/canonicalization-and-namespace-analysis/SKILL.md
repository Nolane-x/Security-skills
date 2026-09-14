---
name: canonicalization-and-namespace-analysis
description: "Analyze mismatches between policy representations and runtime-resolved identities across paths, URLs, encodings, case rules, aliases, archive members, hostnames, Unicode, object namespaces, and mutable name-to-object bindings. Use when multiple representations may denote one resource or one representation may change meaning across layers."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Canonicalization and Namespace Analysis

Security checks must authorize the same identity that the sink later resolves. The central question is not whether a string looks unusual; it is whether the policy key, resolver semantics, namespace root, and final object identity remain causally consistent.

## When to use

Use for path containment, archive extraction, filesystem streams, URL/host validation, case-insensitive stores, Unicode identifiers, cloud resource names, IPC/object-manager namespaces, parser-to-OS name translation, or any system where a name crosses multiple parsing and resolution layers.

## Preconditions

1. Use only owned, local, sandboxed, synthetic, mock, read-only, test-only, or explicitly authorized resources for dynamic validation.
2. Record platform, filesystem, runtime, parser, namespace-root, and resolver semantics that affect identity.
3. Prefer benign fixture identities and immutable observations over sensitive targets or uncontrolled side effects.
4. Separate representation differences from authorization consequences; unusual syntax alone is not a validated defect.

## Representation and identity graph

Model the system as typed representations and identity transitions rather than one canonical string:

```text
raw input -> parsed representation -> decoded representation -> normalized representation -> policy key -> resolver input -> resolved identity -> opened handle/object identity
```

A system may skip stages or branch, so record only transitions that actually occur. Keep these relations distinct:

- **representation equality** — byte/string forms are identical;
- **normalized equality** — a selected normalizer maps representations to one form;
- **resolver equivalence** — the sink resolves different representations to the same identity;
- **policy equivalence** — policy intentionally assigns the same decision to multiple identities or representations;
- **object identity** — the bound handle/object is the same final object.

Resolver equivalence does not imply policy equivalence, and policy equivalence does not prove that two independently resolved names remain bound to one object.

## Transformation ordering and non-commutativity

Record every transformation in the order actually applied: parsing, percent decoding, Unicode normalization, case mapping, separator conversion, dot-segment processing, IDNA handling, archive-member normalization, alias expansion, platform translation, or domain-specific resolution.

Treat transform ordering as observable behavior. **Non-commutativity** matters: applying transform A then B can yield a different representation or resolved identity from applying B then A. Do not collapse an ordered transform chain into an unordered checklist.

## Normalization idempotence

When the design relies on a stable normalizer `N`, verify the controlled invariant `N(N(x)) == N(x)` for representative fixtures. **Idempotence** is a stability property, not a security verdict. A non-idempotent representation remains at a low evidence level until policy and resolver consequences are demonstrated.

## Equivalence, collision, ambiguity, and aliasing

Classify the observed relation before assigning impact:

- **equivalence** — distinct representations intentionally resolve to the same identity;
- **collision** — distinct policy keys unexpectedly map to one resolved identity;
- **ambiguity** — one representation is interpreted differently across layers or configurations;
- **aliasing** — a secondary name/reference resolves to another identity by design or mutable namespace state.

This distinction is a false-positive control: a surprising encoding or alias is not itself proof of a policy-boundary failure.

## Policy-key to resolved-identity invariant

A security decision is meaningful only if the **policy key** denotes the same authorized identity that the sink resolves. Trace:

```text
policy key -> resolver input -> resolved identity -> opened handle/object identity
```

Record where the policy decision occurs, whether the sink resolves the same representation, and whether any later stage re-resolves a name instead of using an already-bound object.

## Namespace-root and authority binding

Every name is interpreted inside a namespace or authority context. Record the relevant **namespace root**: filesystem root, archive root, URL authority, tenant namespace, object-manager namespace, cloud scope, or equivalent domain root.

Policy and sink must agree not only on the child representation but on the root/authority that gives that representation meaning. A normalized child name does not prove identity consistency when policy and resolver use different roots.

## Boundary-preserving normalization

Record which boundaries normalization must preserve: path components, hostname labels, archive roots, tenant/resource separators, identifier domains, or platform object namespaces. Do not treat string prefix/suffix checks as containment unless they match the sink's actual boundary semantics.

## Name-to-object transition

The **name-to-object** transition is often the strongest identity boundary. Record the stage where a re-resolvable name becomes an opened handle/object identity and whether subsequent logic continues using that object or resolves the name again.

Prefer evidence tied to the opened handle/object identity because it reduces ambiguity from presentation-only differences and later namespace mutation.

## Mutable namespace and identity drift

A checked name can change meaning through rename, remount, alias update, link/reparse change, object rebinding, or another namespace transition. Record a **namespace generation**, version, mount identifier, or equivalent bounded state marker when available.

This skill does not replace general concurrency/race analysis. Its narrower concern is identity drift: whether the checked policy representation still denotes the same object identity at use time.

## Namespace evidence ladder

Use the highest level directly supported by evidence and controls:

- **N0 — representation note:** unusual spelling, encoding, alias, or theoretical equivalence only; no reproduced semantic difference.
- **N1 — transform difference:** a controlled fixture reproduces a parse/decode/normalization difference, but policy/resolver impact is not established.
- **N2 — policy/resolver divergence:** policy representation and resolver semantics differ reproducibly in a synthetic or read-only fixture without a demonstrated identity-boundary consequence.
- **N3 — benign identity divergence:** a controlled alias, collision, root, containment, or resolution difference reaches a different benign fixture identity than policy intended.
- **N4 — bounded policy-boundary consequence:** the identity divergence crosses the intended synthetic policy boundary and the causal transform/resolution chain is demonstrated with paired controls.
- **N5 — lifecycle/composition proof:** mutable-namespace or cross-layer identity drift is reproduced with generation/state evidence, counterfactual controls, and remediation regression while neighboring intended behavior remains intact.

## Counterfactual proof

A promoted finding requires at least one controlled **counterfactual** that changes one causal variable while holding the rest of the synthetic fixture stable. Suitable variables include transform order, namespace root, alias target, normalization mode, resolver configuration, or namespace generation.

Use the counterfactual to establish causality, not to broaden the test beyond the authorized fixture.

## Alternative explanations

Before promotion, evaluate benign explanations such as documented platform normalization, expected case-insensitive lookup, intended Unicode equivalence, stale cache or namespace snapshot, display-only differences, expected propagation/remount delay, fixture error, or policy intentionally granting multiple equivalent names.

If an alternative explanation fits the evidence equally well, keep the finding below the level that assumes a policy-boundary consequence.

## Workflow

1. Record the full representation chain from raw input to opened handle/object identity.
2. Record transformations in observed order and identify potentially non-commutative stages.
3. Test normalization idempotence when the design depends on stable normalized output.
4. Define the relevant equivalence class and distinguish equivalence, collision, ambiguity, and aliasing.
5. Identify the exact policy key and the resolver input consumed by the sink.
6. Bind both policy and resolver to the same namespace root/authority context.
7. Record the resolved benign identity and the name-to-object transition.
8. Record namespace generation/state when names can be rebound or re-resolved.
9. Run paired positive/negative controls and at least one one-variable counterfactual.
10. Assign N0-N5 conservatively and verify remediation without regressing intended neighboring behavior.

## Evidence contract

Record raw, parsed, decoded, normalized, policy, resolver, and resolved identity states; transform order; equivalence classification; namespace root; object binding; namespace generation; positive/negative controls; counterfactual; alternative explanations; evidence level; and remediation result.

A finding must not be promoted solely because two strings differ, one representation is unusual, or a tool reports a normalization mismatch. Show the causal relation between representation handling and the resolved benign identity.

## Evidence ceiling

The **evidence ceiling** is the strongest N0-N5 level directly supported by the observed representation chain, resolver evidence, namespace/root state, object binding, controls, and counterfactuals. Missing identity evidence, stale namespace state, unknown transform ordering, or unbound object identity lowers the ceiling.

## Stop conditions

Stop when the sink operates on an immutable already-open handle/object and no re-resolution occurs, all equivalent forms are normalized under the same root before policy, the environment cannot reproduce behavior safely, or further proof would require production/sensitive resources or uncontrolled side effects.

## Output

```text
namespace/platform:
representation chain:
transform order:
normalization idempotence:
equivalence/collision/ambiguity/aliasing:
policy key:
resolver input:
namespace root/authority:
resolved benign identity:
object binding:
namespace generation/state:
positive control:
negative control:
counterfactual:
alternative explanation:
evidence level N0-N5:
evidence ceiling:
remediation oracle:
```
