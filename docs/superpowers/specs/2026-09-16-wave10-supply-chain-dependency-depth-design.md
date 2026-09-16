# Wave 10 Supply-Chain Dependency Depth Design

## Status

Approved by standing user instruction to continue Wave 10 without per-step approval. This document freezes the intended semantics before implementation.

Base authority: `main@c4d43c4e5afd50cbec2a1337930f7a5de79b8137`.

Target canonical skill: `supply-chain-dependency-review`.

## Goal

Deepen the existing `supply-chain-dependency-review` skill from dependency/build checklist coverage into a causal artifact-provenance proof method. The profile must distinguish declared dependency intent from the package/artifact that actually resolves, builds, is released, is distributed, and is deployed. It must reason about namespace ambiguity, mutable sources, integrity/provenance verification, build hooks/toolchains, CI trust, cache/reuse, release authority, artifact substitution, and lifecycle invalidation without becoming a CVE inventory or offensive package-publishing workflow.

The profile remains deterministic, evidence-first, portable, and restricted to synthetic or explicitly authorized environments.

## Why this profile is distinct

The canonical skill already maps dependency sources, lockfiles, registries, build scripts, generated artifacts, CI trust, release provenance, duplicate embedded copies, and safe validation. That is useful breadth, but it does not yet require the operator to prove the complete causal chain from declared requirement to deployed artifact identity.

This profile adds supply-chain-specific causal reasoning rather than duplicating adjacent profiles:

- `canonicalization-and-namespace-analysis` reasons about representation/namespace resolution generally;
- `cache-key-identity-analysis` reasons about whether reuse keys represent every security-relevant dependency;
- `secrets-and-token-flow-analysis` reasons about credential authority and propagation;
- `authorization-boundary-analysis` reasons about principals and operations;
- `supply-chain-dependency-review` will reason about whether the artifact that is selected, built, attested, released, distributed, and deployed is the authorized artifact implied by the dependency/build/release contract.

When a failure is primarily cache-key identity, credential leakage, generic authorization, or canonicalization, the profile should compose with the adjacent skill rather than silently redefining it.

## Causal supply-chain model

The canonical causal chain is:

`declared dependency requirement -> source/namespace resolution policy -> selected package/source identity -> immutable version/ref/digest binding -> fetch origin or mirror -> integrity/signature/provenance verification -> install/build hook -> toolchain/build-environment identity -> CI principal/trust context -> cache/reuse input binding -> produced artifact identity -> release/signing/publishing authority -> distributed artifact identity -> deployed/runtime artifact identity -> bounded security-relevant effect -> lifecycle/revocation/update generation`

The operator must trace every transition material to the observed result. A manifest entry, lockfile, checksum, signature, SBOM, attestation, tag, or release label is not sufficient by itself: the final artifact identity must remain causally bound to the intended source, trusted build context, authorized release authority, and current lifecycle generation.

## Mandatory distinctions

The skill and runbook must make these distinctions explicit:

1. `declared dependency != resolved dependency`
2. `package name/version != artifact identity`
3. `version pin != immutable artifact`
4. `checksum match != authorized publisher provenance`
5. `signature validity != release-policy authorization`
6. `registry namespace != publisher identity`
7. `mirror origin != canonical upstream identity`
8. `lockfile entry != installed/shipped bytes`
9. `source revision != produced artifact identity`
10. `build success != hermetic or trusted build`
11. `CI execution authority != release/publishing authority`
12. `cache hit != trusted build input`
13. `SBOM presence != provenance correctness`
14. `attestation presence != verifier-policy acceptance`
15. `released artifact != deployed artifact`
16. `expiry/update timestamp != revocation/update generation`

## Core invariants

A profile-compliant analysis must reason about these invariants:

1. Every security-relevant dependency must resolve through an explicit source policy to a concrete package/source identity and an immutable artifact identity.
2. Namespace and registry/mirror routing must be unambiguous for the dependency contract; silent fallback or precedence changes must not select a neighboring synthetic source.
3. Integrity, signature, or provenance verification must validate the intended artifact identity and expected publisher/build authority, not merely cryptographic validity in isolation.
4. Mutable tags, branches, floating versions, unpinned archives, mutable build images, fetched toolchains, plugins, and generated-code inputs must be treated as unresolved identity until reduced to immutable evidence.
5. Build/install hooks and fetched tooling that can affect output identity must be included in the causal input graph.
6. Untrusted CI contexts such as pull requests, forks, or lower-trust jobs must not silently provide trusted artifacts, caches, attestations, signatures, or release inputs to higher-trust build/release contexts.
7. Cache/reuse decisions that affect built artifact identity must bind to the security-relevant source, dependency, toolchain, trust-context, and lifecycle inputs; cache-specific defects should compose with `cache-key-identity-analysis`.
8. Produced artifact identity must be traceable to source revision, resolved dependency graph, relevant build hooks, toolchain/build environment, workflow identity, and trust context.
9. Release/signing/publishing authority must be separately authorized and must bind the exact produced artifact that is approved for distribution.
10. Distributed artifacts must match the authorized released artifact identity, and deployed/runtime artifacts must match the verified distributed artifact or an auditable authorized transformation.
11. Rotation, revocation, compromised-publisher response, signing-key generation changes, mirror-policy changes, dependency replacement, release withdrawal, rollback, and update events must advance or invalidate a lifecycle generation where stale trust could alter the security result.
12. Remediation must block the ambiguous/mutable/untrusted path while preserving legitimate dependency resolution, builds, releases, distribution, and updates.
13. Evidence promotion must never exceed the directly demonstrated transition; inventory suspicion, public vulnerability metadata, or theoretical dependency confusion cannot be promoted to a confirmed supply-chain effect without bounded proof.

## Evidence ladder SC0-SC5

### SC0 — Supply-chain surface identified

Dependency sources, namespaces, lock/pin state, build inputs, hooks, CI boundaries, release authority, provenance metadata, or distribution paths are identified, but no security-relevant identity divergence is directly demonstrated.

### SC1 — Resolution or provenance divergence

A direct mismatch is observed between declared requirement and resolved source/package/artifact identity, expected provenance and verifier decision, expected build context and observed context, or expected lifecycle generation and accepted generation.

### SC2 — Artifact identity or trust-context collision

A deterministic synthetic control shows two dependency/build/release contexts that should remain distinct can resolve, reuse, attest, sign, publish, distribute, or deploy the same trusted identity state when they should not.

### SC3 — Inert wrong-artifact acceptance

A synthetic inert artifact, canary file, mock package, read-only fixture, or metadata marker from the wrong synthetic source/trust context is accepted, selected, propagated, or surfaced without causing a meaningful state change.

### SC4 — Bounded synthetic supply-chain effect

A controlled, reversible, owner-operated fixture demonstrates that the wrong synthetic dependency/artifact/build context can affect a bounded build, release, distribution, or deployment decision or output. The effect must remain inert or reversible and must not involve publishing to third-party namespaces or touching real credentials.

### SC5 — Full causal supply-chain proof

The complete causal chain is demonstrated with direct evidence of the failing transition, source-resolution and artifact-identity proof, verifier/provenance trace, CI/build trust context, release/distribution/deployment binding where applicable, lifecycle-generation control, paired positive/negative controls, counterfactual controls, alternative-explanation elimination, remediation evidence, and regression verification. SC5 never permits claims beyond the synthetic/authorized scope actually tested.

## Deterministic review cases

The profile will ship at least three machine-readable review cases.

### 1. `dependency-resolution-and-namespace-binding`

Purpose: prove that declared requirement, source/namespace policy, registry or mirror routing, selected package/source identity, immutable artifact identity, and verifier decision remain bound.

Expected failure classes include ambiguous internal/public namespace resolution, mirror precedence drift, mutable tags/versions, aliasing, checksum-only trust without publisher provenance, or resolver fallback to a neighboring synthetic source.

Required controls include two synthetic namespaces with the same logical package name, explicit source-policy pinning, immutable artifact identity capture, corrected precedence, and a benign intended-source success case. Validation uses local/mock resolver fixtures only; it never publishes or claims third-party package names.

### 2. `build-input-and-ci-trust-provenance`

Purpose: prove that build hooks, fetched tools, build images, compiler/plugins, generated code, cache/reuse state, workflow identity, and CI trust context all bind to the produced artifact identity.

Expected failure classes include untrusted PR/fork outputs entering trusted builds, mutable fetched toolchains, stale/untrusted caches, generated artifacts without source binding, or a build whose output provenance omits a security-relevant input.

Required controls include trusted versus untrusted synthetic CI principals, changed toolchain/build-image identities, cache-disabled or trust-separated controls, deterministic produced-artifact digests, and corrected provenance binding.

### 3. `release-artifact-and-lifecycle-binding`

Purpose: prove that produced artifact identity, release approval, signer/publisher authority, distributed artifact identity, deployed/runtime artifact identity, and lifecycle generation remain bound end to end.

Expected failure classes include signing the wrong artifact, release metadata referring to a neighboring synthetic artifact, distribution substitution, deployment of a stale/withdrawn generation, rollback to an invalidated artifact, or verifier acceptance after revocation/update generation changes.

Required controls include exact digest binding, synthetic release authority, neighboring artifact identities, generation advancement, corrected distribution/deployment binding, and a legitimate rollback/update control where policy explicitly allows it.

## Runbook structure

The operator runbook must include at least these sections:

1. `Attack surface`
2. `Hypothesis matrix`
3. `Dependency declaration and graph trace`
4. `Namespace and source-resolution trace`
5. `Artifact identity and immutable-pin trace`
6. `Integrity, signature, and provenance-verifier trace`
7. `Install and build-hook trace`
8. `Toolchain and build-environment trace`
9. `CI principal and trust-boundary trace`
10. `Cache and reuse-input trace`
11. `Produced-artifact identity trace`
12. `Release, signing, and publishing-authority trace`
13. `Distribution and deployment binding`
14. `Lifecycle and revocation/update-generation trace`
15. `Controlled validation`
16. `False-positive controls`
17. `Counterfactual controls`
18. `Alternative explanations`
19. `Evidence capture`
20. `Evidence promotion and ceiling`
21. `Remediation checks`

## Counterfactual controls

A strong analysis should choose counterfactuals appropriate to the suspected transition, including:

- same declared package name with two synthetic source namespaces;
- same version label with different immutable artifact digests;
- same artifact bytes with a different expected publisher/build authority;
- same source revision with a different build hook, toolchain, or build-image identity;
- same dependency graph with trusted versus untrusted synthetic CI principal;
- same build with cache disabled, cache trust partitioned, or cache generation advanced;
- same produced artifact with neighboring release metadata or signer identity;
- same release metadata with a different distributed artifact digest;
- same distributed artifact after revocation/update generation advances;
- remediated source/provenance/release binding that preserves the legitimate build and release path.

## Alternative explanations

Before promoting evidence, the operator must consider and distinguish when applicable:

- intentionally mirrored or vendored content with documented immutable equivalence;
- deterministic rebuild differences caused only by timestamps or non-security metadata;
- platform-specific dependency resolution intentionally selecting different artifacts;
- stale local resolver metadata or lockfile regeneration;
- eventual mirror synchronization delay;
- cache behavior better explained by cache-key identity;
- public/shared packages intentionally resolving from a public source;
- documented release repackaging or signing transformation that preserves an auditable digest chain;
- intentionally permitted rollback windows;
- test-fixture contamination or stale synthetic artifacts;
- vulnerability inventory that does not demonstrate reachability or shipped-artifact presence.

## Machine-readable scenario contract

Each deterministic review case must carry substantive strings for at least these fields:

- `hypothesis`
- `safe_oracle`
- `positive_control`
- `negative_control`
- `stop_condition`
- `remediation_oracle`
- `declared_requirement`
- `source_resolution_policy`
- `selected_namespace_source`
- `selected_artifact_identity`
- `immutable_pin_integrity_state`
- `provenance_verifier_decision`
- `install_build_hook`
- `toolchain_build_environment`
- `ci_principal_trust_context`
- `cache_reuse_input_binding`
- `produced_artifact_identity`
- `release_signing_publishing_authority`
- `distributed_artifact_identity`
- `deployed_runtime_artifact_identity`
- `bounded_effect`
- `lifecycle_revocation_update_generation`
- `counterfactual_control`
- `alternative_explanation`
- `evidence_level`
- `evidence_ceiling`

The dedicated test may require a minimum non-trivial string length for each field, consistent with recent Wave 10 profiles.

## Skill output contract

The canonical skill should produce or request a structured output that can capture:

- build/release target;
- declared direct/transitive dependency requirement;
- source/namespace and mirror policy;
- selected package/source identity;
- immutable version/ref/digest identity;
- integrity/signature/provenance verifier result;
- build/install hooks and fetched tooling;
- toolchain/build environment identity;
- CI principal/trust context;
- cache/reuse input binding;
- produced artifact identity;
- release/signing/publishing authority;
- distributed and deployed/runtime artifact identity;
- lifecycle/revocation/update generation;
- bounded observation/effect;
- counterfactual results;
- alternative explanations considered;
- evidence level and evidence ceiling;
- remediation and regression result.

## Safety boundary

Dynamic validation is limited to owned, local, sandboxed, benchmark/CTF, simulated, or explicitly authorized environments.

Use only synthetic package names reserved to the test fixture, local/mock registries, mock mirrors, inert artifact markers, deterministic builds, synthetic CI principals, fake signing identities, read-only provenance inspection, or bounded reversible owner-controlled state.

Do not publish look-alike packages, claim third-party namespaces, poison public registries, alter external mirrors, access real CI/release credentials, replace third-party artifacts, interfere with production dependency infrastructure, perform persistence/evasion/malware actions, or test unauthorized targets.

If proof would require a public namespace, real release credential, real downstream victim, or irreversible artifact substitution, stop at the strongest lower evidence level supported by safe evidence.

## Implementation scope

Exactly these nine paths are expected to change for profile #18:

1. `README.md`
2. `docs/operator-depth-contract.md`
3. `docs/superpowers/specs/2026-09-16-wave10-supply-chain-dependency-depth-design.md`
4. `docs/superpowers/plans/2026-09-16-wave10-supply-chain-dependency-depth.md`
5. `operator-depth/profiles.json`
6. `skills/supply-chain-dependency-review/SKILL.md`
7. `skills/supply-chain-dependency-review/references/operator-review-cases.json`
8. `skills/supply-chain-dependency-review/references/operator-runbook.md`
9. `tests/test_supply_chain_dependency_depth.py`

## Explicit non-scope

The implementation must not change:

- `skills/supply-chain-dependency-review/skill.meta.json`;
- graph edges;
- packs;
- routing domains;
- benchmark fixtures or thresholds;
- agent-eval authority;
- superiority-court authority;
- GitHub workflow semantics.

The profile may compose with adjacent skills but must not silently redefine their authority.

## Dedicated test contract

The dedicated test follows the same four-part structure used by recent Wave 10 profiles:

1. `test_skill_exposes_causal_supply_chain_model`
2. `test_runbook_requires_transition_level_supply_chain_reasoning`
3. `test_review_cases_encode_supply_chain_reasoning`
4. `test_skill_is_registered_as_eighteenth_operator_depth_profile`

The registry assertion is additive (`>= 18`) and requires exactly one matching `supply-chain-dependency-review` registration. It must not globally assert an exact profile count in a way that blocks later additive profiles.

## Verification and merge discipline

Implementation follows the established Wave 10 provenance sequence:

1. commit this design spec;
2. self-review the spec for placeholders, contradictions, ambiguity, and scope;
3. write and commit the implementation plan;
4. add the dedicated test first;
5. obtain a clean RED CI proving the intended assertions fail for missing depth artifacts while unrelated repository gates remain healthy;
6. implement behavioral artifacts without weakening the test;
7. obtain full behavioral GREEN across Linux/macOS/Windows on Python 3.11/3.13 plus `benchmark-core`, `agent-eval-core`, and `superiority-court-core`;
8. update only public docs after behavioral GREEN;
9. prove the post-GREEN delta is documentation-only and the PR scope is exactly the nine paths above;
10. obtain full exact-head GREEN on the final candidate;
11. merge with an expected-head SHA guard;
12. obtain full post-merge push CI on the merge SHA;
13. verify registry/public-doc closure state and record final provenance.

No empirical superiority claim over Claude-Red or any external system is permitted without an actual external contestant run through the repository superiority court.
