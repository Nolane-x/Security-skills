---
name: supply-chain-dependency-review
description: "Review software dependency and build provenance for owned or authorized projects: direct/transitive dependencies, lockfiles, registries, build scripts, generated artifacts, vendoring, release provenance, typosquatting/confusion exposure, and update controls. Use for secure build and dependency-risk analysis."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Supply Chain Dependency Review

Supply-chain review connects declared dependency intent to the exact artifact that is resolved, built, released, distributed, and deployed. Inventory is not proof: a manifest, lockfile, checksum, signature, SBOM, attestation, or release label is only one transition in the chain.

## When to use

Use for application/package builds, containers, CI pipelines, vendored native libraries, language package managers, generated code, build images/toolchains, release automation, artifact distribution, deployment provenance, or dependency incident response.

Use this skill when the question is whether the artifact that actually ships is the authorized artifact implied by the dependency/build/release contract. Compose with `cache-key-identity-analysis` for cache-key defects, `canonicalization-and-namespace-analysis` for generic name/namespace transformation defects, `secrets-and-token-flow-analysis` for credential propagation, and `authorization-boundary-analysis` for generic permission decisions.

## Preconditions

Operate only on owned repositories/builds, local or sandbox fixtures, benchmark/CTF environments, or targets with explicit authorization. Prefer synthetic package names, local/mock registries or mirrors, inert artifacts, deterministic build manifests, synthetic CI principals, fake signing identities, read-only provenance inspection, and reversible owner-controlled state.

Do not publish look-alike packages, claim third-party namespaces, poison public registries, alter external mirrors, use real CI/release credentials, replace third-party artifacts, interfere with production dependency infrastructure, or use unauthorized targets.

## Causal supply-chain model

Trace the security-relevant chain as:

`declared dependency requirement -> source/namespace resolution policy -> selected package/source identity -> immutable version/ref/digest binding -> fetch origin or mirror -> integrity/signature/provenance verification -> install/build hook -> toolchain/build-environment identity -> CI principal/trust context -> cache/reuse input binding -> produced artifact identity -> release/signing/publishing authority -> distributed artifact identity -> deployed/runtime artifact identity -> bounded security-relevant effect -> lifecycle/revocation/update generation`

Every material transition needs an observed value and evidence source. Do not skip directly from a manifest or signature to a claim about the deployed artifact.

Keep these distinctions explicit:

- `declared dependency != resolved dependency`
- `package name/version != artifact identity`
- `version pin != immutable artifact`
- `checksum match != authorized publisher provenance`
- `signature validity != release-policy authorization`
- `registry namespace != publisher identity`
- `mirror origin != canonical upstream identity`
- `lockfile entry != installed/shipped bytes`
- `source revision != produced artifact identity`
- `build success != hermetic or trusted build`
- `CI execution authority != release/publishing authority`
- `cache hit != trusted build input`
- `SBOM presence != provenance correctness`
- `attestation presence != verifier-policy acceptance`
- `released artifact != deployed artifact`
- `expiry/update timestamp != revocation/update generation`

## Dependency and source resolution

Record the declared direct/transitive dependency requirement, source type, source resolution policy, namespace scope, mirror/registry order, fallback behavior, selected package/source identity, and resolver evidence.

A package name or semantic version is not a security identity by itself. Verify which registry, git repository, archive origin, vendored tree, system package source, build image, compiler/plugin source, or generated-code source actually won resolution.

Where internal and public names can overlap, use only synthetic local/mock namespace fixtures. A safe review can prove ambiguity with deterministic resolver metadata; it never needs to publish or reserve a real third-party name.

## Artifact identity and immutable pinning

Reduce each security-relevant selected input to an immutable identity when the ecosystem supports it: exact commit, content digest, package checksum tied to the expected source, immutable image digest, verified archive digest, or equivalent artifact identity.

A version pin is not an immutable artifact if the backing object can be replaced. A mutable tag, branch, floating version, mirror alias, downloaded installer, fetched toolchain, plugin, generated artifact, or build image remains unresolved until the review captures the exact bytes or immutable identity that influenced the output.

Compare the lock/build metadata with installed, embedded, containerized, or runtime artifact evidence. Duplicate vendored or embedded copies are independent artifact identities even when the central package declaration has been upgraded.

## Integrity, signature, and provenance verification

Capture the integrity/signature/provenance verifier decision as a policy tuple, not a boolean. At minimum record the artifact identity, expected publisher/build authority, verifier/trust root, provenance subject, source revision or build inputs where available, and verification result.

A checksum can prove byte equality to a reference but not that the reference was authorized. A valid signature can prove possession of a signing key but not that this signer was authorized for this release path. An attestation can be syntactically valid while naming the wrong artifact, workflow, source revision, builder, or policy generation.

Evidence may advance only as far as the verifier binding directly proves.

## Build hooks and toolchain identity

Inventory install scripts, lifecycle hooks, code generators, plugins, native compilation, bootstrap downloads, compiler/linker versions, build containers, base images, package-manager plugins, reusable workflow actions, and any fetched tooling that can alter output bytes or trust state.

For every material build hook, record whether it is source-controlled, generated, fetched, mutable, sandboxed, and included in provenance. For every material toolchain identity, record immutable version/digest evidence where practical.

A source revision does not uniquely determine a produced artifact when hooks, toolchains, network fetches, environment state, generated inputs, or platform-specific resolution can change the output.

## CI trust and cache reuse

Trace the CI principal and trust context for every step that can create, approve, attest, sign, upload, publish, or promote an artifact. Distinguish untrusted pull-request/fork execution from trusted protected-branch/release execution.

Untrusted contexts must not silently become trusted build inputs through artifact upload, workspace persistence, mutable shared storage, reusable workflow confusion, environment inheritance, or cache/reuse. A cache hit is not a trusted build input merely because a key matched.

When reuse materially affects artifact identity, record the cache/reuse input binding: source revision, resolved dependency identity, toolchain/build image, trust context, relevant environment/policy generation, and producer provenance. If the defect is fundamentally a missing security dependency in the cache key, compose with `cache-key-identity-analysis`.

## Produced, released, distributed, and deployed artifacts

Record four distinct identities where they exist:

1. **Produced artifact identity** — digest/object created by the build, bound to source, dependencies, hooks, toolchain, workflow, and CI trust context.
2. **Released artifact identity** — exact produced artifact approved by the release policy and release authority.
3. **Distributed artifact identity** — bytes/object fetched from the release channel, mirror, registry, CDN, repository, image registry, or update service.
4. **Deployed artifact identity** — bytes/object actually installed, loaded, executed, or embedded in the bounded target.

Trace the release authority separately from CI execution authority. Capture which principal or policy may sign, approve, publish, move channels, replace tags/releases, promote images, or authorize rollback.

A secure claim requires a digest/provenance chain from produced to released to distributed to deployed artifact, or an explicit auditable transformation between stages.

## Lifecycle and revocation/update generation

Treat trust as generation-bound. Record the current lifecycle/revocation/update generation for security-relevant events such as signing-key rotation, publisher compromise response, mirror-policy change, dependency replacement, artifact withdrawal, release revocation, compromised build detection, rollback-policy change, or required update.

An artifact that was valid in generation N is not automatically trusted in generation N+1. Verify whether resolver metadata, caches, provenance/verifier state, distribution channels, deployment controls, and rollback policy converge on the new generation.

Where delayed propagation is explicitly allowed, record the bounded delay and its policy authority rather than treating stale acceptance as either automatically safe or automatically vulnerable.

## Workflow

1. Map declared direct/transitive dependencies and every source that can affect build output.
2. Trace source/namespace resolution policy to the selected package/source identity.
3. Reduce security-relevant selected inputs to immutable version/ref/digest evidence.
4. Capture integrity, signature, and provenance verifier policy and result.
5. Trace install/build hooks, generated inputs, fetched tools, toolchain/build environment, and mutable build inputs.
6. Trace CI principals and trust transitions from untrusted input through trusted build/release stages.
7. Trace cache/reuse provenance and separate cache-key defects into the cache-key profile where appropriate.
8. Capture produced artifact identity and bind it to build provenance.
9. Capture release/signing/publishing authority and bind approval/signature to the exact artifact.
10. Compare released, distributed, and deployed/runtime artifact identities.
11. Capture lifecycle/revocation/update generation and test stale-state controls safely.
12. Run synthetic counterfactuals one dimension at a time and eliminate alternative explanations.
13. Apply the evidence ladder conservatively; do not promote inventory or theoretical ambiguity into confirmed effect.
14. Verify remediation splits the unsafe path while preserving the legitimate build/release/update path.

## Supply-chain evidence ladder

- **SC0 — Supply-chain surface identified.** Dependency sources, namespaces, lock/pin state, build inputs, hooks, CI boundaries, release authority, provenance metadata, or distribution paths are mapped without a demonstrated security-relevant identity divergence.
- **SC1 — Resolution or provenance divergence.** Direct evidence shows a mismatch between declared and resolved source/package/artifact identity, expected and observed provenance/verifier state, expected and observed build trust context, or expected and accepted lifecycle generation.
- **SC2 — Artifact identity or trust-context collision.** Deterministic synthetic controls show two contexts that should remain distinct can resolve, reuse, attest, sign, publish, distribute, or deploy through the same trusted identity state.
- **SC3 — Inert wrong-artifact acceptance.** A synthetic inert artifact, canary, mock package, read-only fixture, or metadata marker from the wrong synthetic source/trust context is selected, accepted, propagated, or surfaced without meaningful state change.
- **SC4 — Bounded synthetic supply-chain effect.** A reversible owner-operated fixture proves that the wrong synthetic dependency/artifact/build context changes a bounded build, release, distribution, or deployment decision/output. No public namespace, real credential, third-party artifact, persistence, or destructive action is allowed.
- **SC5 — Full causal supply-chain proof.** SC4 plus the full source-resolution and artifact-identity chain, verifier/provenance trace, build/CI trust context, release/distribution/deployment binding where applicable, lifecycle-generation control, paired positive/negative controls, counterfactuals, alternative-explanation elimination, remediation, and regression evidence.

Never infer SC3-SC5 from a vulnerable-package inventory, a permissive-looking configuration, a checksum/signature alone, an SBOM entry, attestation presence, or theoretical dependency confusion.

## Counterfactual proof

Change one security-relevant dimension at a time and preserve the rest of the fixture. Useful counterfactuals include:

- same declared package name with two synthetic source namespaces;
- same version label with different immutable digests;
- same bytes with a different expected publisher/build authority;
- same source revision with a different build hook, toolchain identity, or build image;
- same dependency graph under trusted versus untrusted synthetic CI principal;
- same build with cache disabled, trust-separated, or generation advanced;
- same produced artifact with a neighboring synthetic release authority;
- same release metadata with a different distributed artifact digest;
- same distributed artifact before and after lifecycle/revocation/update generation advances;
- corrected source/provenance/release binding that preserves legitimate build and update behavior.

Counterfactuals are evidence only when the changed dimension causally explains the observed identity or trust transition.

## Alternative explanations

Before promotion, test whether the observation is better explained by:

- intentionally mirrored or vendored content with documented immutable equivalence;
- deterministic rebuild differences limited to timestamps or non-security metadata;
- platform-specific resolution intentionally selecting a different authorized artifact;
- stale resolver metadata or lockfile regeneration;
- expected mirror synchronization delay;
- cache behavior better explained by cache-key identity;
- public/shared packages intentionally sourced from a public registry;
- documented release repackaging or signing transformations with an auditable digest chain;
- explicitly permitted rollback windows;
- test-fixture contamination or stale synthetic artifacts;
- vulnerability inventory that does not establish shipped-artifact presence or reachability.

Record which alternatives were tested and the observation that excludes or retains each one.

## Evidence contract

Capture enough evidence to reconstruct the security-relevant chain without secret material:

- declared requirement and resolved dependency graph;
- source resolution policy, namespace, registry/mirror choice, and resolver evidence;
- selected package/source and immutable artifact identity;
- integrity/signature/provenance verifier policy and result;
- install/build hooks and toolchain/build environment identity;
- CI principal/trust context and cache/reuse provenance;
- produced artifact identity and build provenance;
- release/signing/publishing authority and released artifact identity;
- distributed and deployed/runtime artifact identities;
- lifecycle/revocation/update generation;
- positive, negative, counterfactual, and remediation controls;
- evidence level and evidence ceiling.

A public CVE, scanner finding, package age, mutable-looking configuration, or unverified dependency name is hypothesis/inventory evidence unless the causal artifact path is demonstrated.

## Evidence ceiling

State the strongest evidence level directly supported by captured observations. Do not promote beyond the first unproven causal transition.

If the safe boundary prevents proving a downstream stage, stop at the strongest lower level. For example, a deterministic namespace collision in a local resolver can justify SC2 or SC3 depending on the oracle; it does not justify a claim that a public victim would install a malicious package.

SC5 requires remediation and regression evidence that blocks the failing synthetic path while legitimate dependency resolution, build, release, distribution, deployment, rollback, and update behavior remain correct where applicable.

## Stop conditions

Stop or de-escalate immediately if proof would require:

- publishing or claiming a third-party/public package name;
- poisoning or altering an external registry, mirror, repository, CDN, or update service;
- obtaining, exposing, replaying, or using real CI/release/signing credentials;
- replacing real third-party or production artifacts;
- causing unapproved downstream installation or execution;
- destructive changes, persistence, evasion, malware, or unauthorized access.

When the next evidence step crosses one of these boundaries, record the evidence ceiling and use a local/mock/synthetic substitute instead.

## Output

```text
build/release target:
declared dependency requirements:
source resolution policy and selected source:
resolved graph and immutable artifact identities:
integrity/signature/provenance verifier decision:
build/install hooks:
toolchain/build environment identity:
CI principal/trust context:
cache/reuse input binding:
produced artifact identity:
release/signing/publishing authority:
released/distributed/deployed artifact identities:
lifecycle/revocation/update generation:
bounded observation or effect:
counterfactual controls:
alternative explanations:
evidence level / evidence ceiling:
remediation and regression result:
```
