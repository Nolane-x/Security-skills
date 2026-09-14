# Canonicalization and Namespace Operator Runbook

This runbook defines a read-only consistency review for owned, sandboxed, synthetic, mock, test-only, or explicitly authorized fixtures. It records how names and identifiers are represented across layers and caps conclusions to directly observed evidence.

## Attack surface

List the review stages that can change representation or identity meaning: parser, decoder, normalizer, policy lookup, namespace context, resolver, and final object binding. For each stage, record its input type, output type, and the documented rule used by the fixture.

The review target is consistency between representations and identities. A display difference or unusual spelling is not sufficient evidence by itself.

## Hypothesis matrix

Write each hypothesis as a falsifiable consistency claim. Examples include transform-order consistency, policy-key and resolver consistency, namespace-root consistency, or name-to-object state consistency.

For each hypothesis record the expected relation, observed relation, positive control, negative control, counterfactual, alternative explanation, evidence level, and evidence ceiling.

## Representation and identity trace

Record the complete **representation chain** for the fixture:

```text
raw input -> parsed representation -> decoded representation -> normalized representation -> policy key -> resolver input -> resolved identity -> opened handle/object identity
```

Only include stages that actually exist. Keep representation equality, normalized equality, **resolver equivalence**, policy equivalence, and object identity as separate review concepts.

## Transformation-order trace

Record the exact **transform order** observed in the fixture. The review may include parsing, decoding, Unicode normalization, case mapping, separator conversion, domain-specific normalization, or other documented transformations.

When the same operations can produce different results in a different order, record non-commutativity as an observed property. Record **normalization idempotence** when stable normalized output is part of the intended contract.

## Equivalence and ambiguity trace

Classify the reviewed relationship as intended equivalence, collision, ambiguity, or aliasing. Record the sink-defined equivalence class and policy-defined equivalence class separately.

Do not promote a finding from syntax alone. The review must rely on directly observed identity and policy records from the controlled fixture.

## Policy-key and resolver binding

Record the exact **policy key**, the **resolver input**, and the resulting **resolved identity**. State whether the two representations are expected to be identical or merely equivalent under documented semantics.

If the system uses an already-bound object, record that object identity and treat it as stronger evidence than presentation text.

## Namespace-root binding

Record the **namespace root** or authority context used by policy and by resolution. Examples can be a test filesystem root, synthetic archive root, mock tenant scope, or another controlled namespace identifier.

A child representation is reviewed together with its root context so two records from different roots are not accidentally compared as if they belonged to the same namespace.

## Name-to-object and generation trace

Record the **object binding** step where a name or identifier becomes a stable object record. Record **namespace generation** or another version/state marker when the controlled namespace can change over time.

If the available records mix generations or the object binding is missing, lower the evidence ceiling rather than inferring continuity.

## Controlled validation

Use synthetic names and benign fixture objects with known identities. Prefer read-only metadata, mock resolvers, test namespaces, inert fixture stores, or already-created disposable records.

Change one review variable at a time and capture the policy key, resolver input, namespace root, resolved identity, object binding, and namespace generation. Stop the review if the next step would require production data, sensitive records, or an uncontrolled external action.

## False-positive controls

Require both a neighboring valid record and a negative control. Useful controls include a representation known to remain consistent, a distinct benign object that stays distinct, an intentionally equivalent synthetic alias, or a current namespace-generation record compared with a deliberately stale test record.

Evaluate expected normalization, documented case behavior, intended Unicode equivalence, stale cache state, display-only formatting, fixture setup error, expected propagation delay, and intentional multi-name policy as alternative explanations.

## Counterfactual controls

Use at least one **counterfactual** that changes one review variable while keeping the remaining synthetic fixture stable. Suitable variables include transform order, normalization mode, namespace root, resolver configuration, or namespace generation.

The counterfactual is used only to test whether the original observation depends on the proposed cause.

## Evidence capture

Capture a deterministic review record containing:

```text
representation chain
transform order
normalization idempotence
equivalence class
policy key
resolver input
resolved identity
namespace root
object binding
namespace generation
positive control
negative control
counterfactual
alternative explanation
```

Prefer stable fixture identifiers over presentation text alone.

## Evidence promotion and ceiling

Use the canonical N0-N5 ladder. N0 records representation notes; N1 records transform differences; N2 records policy/resolver divergence; N3 records benign resolved-identity divergence; N4 requires a bounded synthetic policy-state difference with paired controls; N5 additionally requires lifecycle/state evidence, counterfactuals, and remediation regression.

The **evidence ceiling** is the highest level directly supported by the representation chain, resolved identity records, namespace state, controls, and counterfactual. Unknown transform order, stale generation, missing object binding, or an unresolved alternative explanation lowers the ceiling.

## Remediation checks

Re-run the same synthetic review after remediation and confirm that the intended identity relation is restored while neighboring valid records remain unchanged. Preserve the same fixture identities, controls, and observation method so the comparison is deterministic.