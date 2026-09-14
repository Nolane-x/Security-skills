# Wave 10 Canonicalization and Namespace Depth Design

## Status

Design for Wave 10 operator-depth profile #13, based on `main@a917b24f6408539e388cdf3e17e8bb1db515b4bd`.

## Goal

Promote the existing canonical `canonicalization-and-namespace-analysis` skill into the thirteenth CI-enforced operator-depth profile without creating a duplicate capability, changing graph metadata, or weakening the repository authorization/evidence boundary.

The profile must reason about whether policy and the eventual sink refer to the same resource identity after parsing, decoding, normalization, namespace resolution, aliasing, and name-to-object transition.

## Scope boundary

This profile owns **representation-to-identity consistency**.

It does not replace:

- `authorization-boundary-analysis`, which owns who may perform which action on which resource;
- parser/state-machine skills, which own grammar and parser-state correctness;
- concurrency/race analysis, which owns general scheduling and race causality;
- URL/host, filesystem, archive, cloud, IPC, or platform-specific skills that own domain-specific sink semantics.

The canonicalization profile consumes those semantics when necessary and asks one narrower question: **did the policy representation and the sink-resolved identity remain equivalent under the actual transformation and resolution chain?**

## Recommended model: representation and identity graph

Do not model canonicalization as one "canonical string." Model it as a graph of typed representations and resolution transitions:

```text
raw input
  -> parsed representation
  -> decoded representation
  -> normalized representation
  -> policy key
  -> resolver input
  -> resolved identity
  -> opened handle/object identity
```

A real system may skip stages, branch, or perform multiple transforms. The operator records the exact observed path rather than assuming every stage exists.

The model must preserve the distinction between:

- **representation equality** — two byte/string forms are identical;
- **normalized equality** — a selected normalizer maps them to one representation;
- **resolver equivalence** — the sink resolves them to the same identity;
- **policy equivalence** — policy intentionally grants them the same decision;
- **object identity** — an already-open handle/object refers to the same final object.

No one equality relation is automatically interchangeable with another.

## Core invariants

### Policy-key to resolved-identity invariant

A security decision is valid only when the policy key denotes the same authorized identity that the sink later resolves. The evidence trace therefore binds:

```text
policy key -> resolver input -> resolved identity -> opened handle/object identity
```

If the sink can re-resolve a name after policy, the trace must state that explicitly rather than treating the policy key as final identity.

### Transformation ordering

Transforms are ordered operations, not an unordered checklist. The profile records operations such as parsing, percent decoding, Unicode normalization, case mapping, separator conversion, dot-segment processing, IDNA handling, archive-member normalization, alias expansion, or platform name translation in the sequence actually used.

The operator must consider **non-commutativity**: applying transform A then B may produce a different representation or identity from B then A.

### Idempotence

For a claimed canonicalization stage `N`, the profile checks whether the intended invariant `N(N(x)) == N(x)` holds for the controlled fixture when the design relies on stable normalized output. A failure of idempotence is evidence of representation instability, not automatically evidence of a security consequence.

### Equivalence, collision, ambiguity, and aliasing

The profile keeps four conditions distinct:

- **equivalence**: distinct representations intentionally resolve to the same identity;
- **collision**: distinct policy keys unintentionally map to one sink identity;
- **ambiguity**: one representation can be interpreted differently across layers or configurations;
- **aliasing**: a secondary name or reference intentionally or accidentally resolves to another identity.

These labels prevent unusual syntax from being overstated as a defect.

### Namespace-root and authority binding

Every resolution trace records the namespace root or authority context that gives a name meaning: filesystem root, archive root, URL authority, tenant namespace, object-manager namespace, cloud scope, or equivalent domain root.

A normalized child name is not enough if policy and sink resolve it beneath different roots or authorities.

### Boundary-preserving normalization

The profile records which boundaries must survive normalization: path components, hostname labels, archive member roots, tenant/resource separators, identifier domains, or platform object namespaces. A string prefix/suffix comparison is never assumed to prove containment without sink-equivalent semantics.

### Name-to-object transition

The strongest identity boundary is often the transition from a mutable or re-resolvable name to an opened handle/object identity. The profile records when that transition occurs and whether subsequent checks/actions continue using the bound object or re-resolve the name.

### Mutable namespace and identity drift

A namespace can change between policy and use through rename, remount, alias update, link/reparse change, object rebinding, or equivalent state transition. The profile records **namespace generation** or another bounded state marker when available.

The canonicalization profile does not own generic race-scheduling analysis. It owns the narrower question of whether the same checked name still denotes the same object identity at use time.

## Evidence ladder

Use the following domain-specific evidence ceiling:

- **N0 — representation note:** unusual spelling, encoding, alias, or theoretical equivalence only; no reproduced semantic difference.
- **N1 — transform difference:** a controlled fixture reproducibly shows a parsing/decoding/normalization difference, but policy and sink identity impact is not established.
- **N2 — policy/resolver divergence:** policy representation and resolver semantics differ reproducibly in a synthetic/read-only fixture, without a demonstrated identity-boundary consequence.
- **N3 — benign identity divergence:** a controlled alias/collision/containment/root mismatch reaches a different benign fixture identity than policy intended.
- **N4 — bounded policy-boundary consequence:** the identity divergence crosses the intended synthetic policy boundary and the causal transform/resolution chain is demonstrated with controls.
- **N5 — lifecycle/composition proof:** mutable-namespace or cross-layer identity drift is reproduced with generation/state evidence, counterfactual controls, and remediation regression while neighboring valid behavior remains intact.

The evidence ceiling forbids promotion above the highest stage directly supported by the trace, controls, resolved identity evidence, and namespace state.

## Counterfactual proof

A promoted finding requires at least one controlled counterfactual that changes one causal variable while holding the rest of the synthetic fixture stable. Examples include changing transform order, namespace root, alias target, normalization mode, or generation marker.

The counterfactual is used to test causality, not to generate broader or riskier payloads.

## Alternative explanations

Before promotion, explicitly consider benign causes such as:

- expected platform normalization;
- documented case-insensitive or Unicode-equivalent lookup;
- stale cache or stale namespace snapshot;
- display-only representation differences;
- fixture setup error;
- expected propagation or remount delay;
- policy intentionally granting multiple equivalent names;
- different namespace roots being part of the intended design.

## Safe operator artifacts

Create:

- `skills/canonicalization-and-namespace-analysis/references/operator-runbook.md`
- `skills/canonicalization-and-namespace-analysis/references/operator-review-cases.json`

The runbook must deepen representation/identity reasoning, false-positive controls, counterfactuals, evidence ceilings, and remediation verification.

The machine-readable artifact is deliberately named `operator-review-cases.json` because its cases are deterministic audit contracts, not action recipes.

## Deterministic review cases

At least three audit-only cases are required:

1. **transform-order-consistency** — verify that the recorded policy representation and resolver representation remain consistent across the intended transform sequence and controls;
2. **namespace-root-binding** — verify that policy and sink resolve a synthetic child name under the same recorded root/authority context;
3. **name-to-object-generation-binding** — verify that a checked synthetic name remains bound to the same benign object identity across the recorded namespace generation or that evidence is capped when state is stale.

Every case must include the common operator-depth fields plus domain-specific fields for representation chain, transform order, equivalence class, policy key, resolver input, resolved identity, namespace root, object binding, namespace generation, counterfactual control, alternative explanation, evidence level, and evidence ceiling.

All strings must be substantive enough for deterministic test assertions. Safe oracles must be synthetic, mock, inert, controlled, test-only, or read-only. Stop conditions must prevent transition to production/sensitive resources or uncontrolled side effects.

## Registry and documentation

Register `canonicalization-and-namespace-analysis` as profile #13 in `operator-depth/profiles.json` using:

- `references/operator-runbook.md`
- `references/operator-review-cases.json`
- `lab_only: true`
- the existing six required runbook sections.

Registry-count tests must use an additive invariant (`>= 13`) rather than owning the exact global profile count.

After behavioral GREEN, update `README.md` and `docs/operator-depth-contract.md` from 12 to 13 profiles and describe the new depth without changing benchmark counts or other authorities.

## Expected changed-file scope

Exactly these nine paths are intended:

1. `README.md`
2. `docs/operator-depth-contract.md`
3. `docs/superpowers/specs/2026-09-14-wave10-canonicalization-depth-design.md`
4. `docs/superpowers/plans/2026-09-14-wave10-canonicalization-depth.md`
5. `operator-depth/profiles.json`
6. `skills/canonicalization-and-namespace-analysis/SKILL.md`
7. `skills/canonicalization-and-namespace-analysis/references/operator-runbook.md`
8. `skills/canonicalization-and-namespace-analysis/references/operator-review-cases.json`
9. `tests/test_canonicalization_namespace_depth.py`

Do not change `skill.meta.json`, graph edges, packs, routing domains, benchmark fixtures or thresholds, agent-eval authority, or superiority-court authority.

## TDD and verification gates

1. Commit this design and implementation plan before behavioral changes.
2. Add the dedicated depth test first.
3. Obtain a clean RED in CI caused only by the four intentionally missing contracts: canonical depth, runbook, review-case matrix, and profile #13 registration.
4. Implement the minimum behavioral artifacts needed for GREEN.
5. Require behavioral GREEN on all six Ubuntu/macOS/Windows × Python 3.11/3.13 jobs plus `benchmark-core`, `agent-eval-core`, and `superiority-court-core`.
6. Update public docs only after behavioral GREEN.
7. Freeze the final PR head and repeat the complete exact-head gate.
8. Review changed filenames for scope drift.
9. Merge only with an expected-head SHA guard.
10. Verify the merge commit on `main` with the push-triggered six-job matrix and all three core determinism jobs.

## Success criteria

The work is complete only when profile #13 is present on `main`, the operator artifacts encode the approved representation/identity model, the dedicated test has demonstrated RED then GREEN, no unrelated authority changed, and both exact-head and post-merge CI complete successfully.