# Supply-Chain Dependency Review — Operator Runbook

This runbook is for owned, local, sandboxed, benchmark/CTF, simulated, or explicitly authorized systems only. All dynamic validation should use synthetic package names, local/mock registries or mirrors, inert artifacts, deterministic fixtures, synthetic CI principals, fake signing identities, read-only provenance inspection, or reversible owner-controlled state.

The goal is to prove or falsify a supply-chain hypothesis by tracing artifact identity and trust context end to end. It is not a package-publishing playbook and must not use public look-alike packages, real release credentials, production artifact substitution, or unauthorized infrastructure.

## Attack surface

Map every place where dependency or artifact identity can be selected, transformed, reused, approved, or replaced:

- manifests, lockfiles, workspace manifests, package-manager configuration, registry/mirror configuration, vendored trees, submodules, git/archive URLs, system packages, generated code, build images, toolchains, plugins, and bootstrap downloads;
- resolver precedence, scoped namespaces, internal/public package routing, mirrors, fallbacks, aliases, proxy caches, and offline/vendor modes;
- integrity checks, checksums, signatures, provenance attestations, SBOMs, transparency metadata, signer/build identities, and verifier policy;
- install scripts, lifecycle hooks, code generation, package-manager plugins, native compilation, reusable workflow actions, build containers, compilers/linkers, and fetched tools;
- CI principals, fork/PR jobs, protected-branch jobs, reusable workflows, artifact uploads/downloads, shared workspaces, caches, secret-bearing jobs, release jobs, and environment promotion;
- build outputs, release approval, signer/publisher authority, registries, package indexes, image registries, release assets, object storage, CDNs, update services, deployment controllers, and runtime artifacts;
- signing-key generations, release generations, mirror-policy changes, dependency withdrawal, publisher compromise response, rollback policy, update policy, and deployed-state generation.

For each surface, capture the expected authority and the evidence source that can prove the actual transition.

## Hypothesis matrix

Write each hypothesis as a transition that can be falsified with synthetic evidence. Examples:

| Hypothesis | Transition under test | Safe proof signal | Minimum negative control |
| --- | --- | --- | --- |
| An internal dependency can resolve from the wrong source | declared requirement -> source resolution policy -> selected namespace/source | local mock resolver selects neighboring synthetic source | explicit scoped-source policy selects intended synthetic source |
| A mutable build input can change trusted output without appearing in provenance | build hook/toolchain -> produced artifact identity | deterministic fixture produces different digest while provenance omits changed input | immutable toolchain/input yields stable expected digest |
| Untrusted CI output can enter a trusted release path | CI principal/trust context -> produced/released artifact | inert artifact from synthetic untrusted principal is accepted by release fixture | trusted-only provenance policy rejects untrusted artifact |
| Released bytes can diverge from distributed/deployed bytes | released -> distributed -> deployed artifact identity | inert marker digest changes at a bounded local distribution/deployment hop | exact-digest binding preserves intended artifact |
| Stale artifact trust survives invalidation | lifecycle generation -> verifier/deployment decision | withdrawn synthetic generation remains accepted in local policy simulator | advanced generation rejects stale artifact and accepts current one |

A hypothesis is not validated because a risky configuration exists. It must be tied to the exact transition that produces the security-relevant artifact or decision.

## Dependency declaration and graph trace

Record:

- declared requirement as written in the manifest or build configuration;
- whether the dependency is direct, transitive, vendored, generated, system-provided, image/toolchain-provided, or fetched at build time;
- the resolver and version-selection rules;
- the resolved graph as observed from lock/build metadata;
- duplicate embedded copies that can remain independently vulnerable or stale;
- whether runtime/container artifacts match the expected graph.

For each node, capture both declared identity and resolved identity. Treat a dependency graph as an observed artifact, not as proof that the shipped bytes match it.

## Namespace and source-resolution trace

For every security-relevant dependency, record the source resolution policy in a table with:

- package or component name;
- scope/namespace;
- allowed source(s);
- mirror/proxy order;
- fallback behavior;
- selected namespace/source;
- canonical upstream identity if mirrored;
- resolver evidence;
- current policy generation.

Use local/mock registries to test precedence. A useful synthetic control keeps the package name constant while changing only the namespace/source mapping. Never publish a look-alike package or claim a third-party namespace.

Distinguish these explicitly:

- package name/version from artifact identity;
- registry namespace from publisher identity;
- mirror origin from canonical upstream identity;
- declared source policy from the resolver's actual selected source.

## Artifact identity and immutable-pin trace

Reduce each selected source to an immutable artifact identity where supported. Capture:

- exact package archive/content digest;
- exact commit for git dependencies;
- digest for build images and toolchain containers;
- archive checksum plus expected source/publisher context;
- vendored tree digest or revision;
- installed/embedded/runtime digest where feasible;
- whether tags, branches, aliases, semantic ranges, mutable images, generated outputs, or downloaded installers remain mutable.

Record an immutable pin as an evidence tuple, not a label. For example: `source identity + artifact digest + verifier context + generation`.

A version pin is not an immutable artifact if the backing object can be replaced. A lockfile entry is not installed/shipped bytes until the corresponding artifact identity is observed.

## Integrity, signature, and provenance-verifier trace

For each verifier step, capture:

- artifact identity presented to the verifier;
- expected publisher, signer, builder, workflow, or provenance subject;
- trust root or policy source;
- signature/checksum/attestation input;
- source revision and build inputs claimed by provenance where available;
- verifier decision;
- verifier policy generation;
- evidence that the exact artifact—not merely metadata—was bound to the decision.

Use the phrase `provenance verifier` in notes for the component or policy that decides whether provenance is acceptable.

Do not collapse cryptographic validity and authorization. Checksum match proves equality to a reference. Signature validity proves possession of a key. Neither alone proves that the reference, signer, builder, or release path was authorized for this artifact.

## Install and build-hook trace

Inventory every build hook that can affect source or output identity:

- pre/post-install scripts;
- code generation;
- package-manager plugins;
- compiler/linker plugins;
- native extension builds;
- reusable workflow actions;
- bootstrap scripts;
- downloaded tools or SDKs;
- network fetches during build;
- generated dependency manifests or vendor steps.

For each build hook, record its source identity, mutable/immutable state, execution trust context, inputs, outputs, and whether provenance includes it.

A disabled or no-op hook is still a useful control. Compare the produced artifact identity with one relevant hook changed at a time.

## Toolchain and build-environment trace

Capture the toolchain identity and build environment identity separately:

- compiler/interpreter/package-manager version;
- build-image digest or host image identity;
- linker/build-system version;
- package-manager plugin set;
- environment variables that alter resolution/output but do not contain secret values in evidence;
- architecture/platform;
- reproducibility flags;
- source-date or timestamp normalization where relevant.

Use deterministic local builds when possible. If two outputs differ, distinguish security-relevant input drift from harmless timestamp/non-security metadata before promoting evidence.

## CI principal and trust-boundary trace

Map the CI principal for each workflow/job that can affect trusted artifacts. Record:

- trigger and repository/ref context;
- principal or trust class, such as synthetic `untrusted-pr`, `trusted-main`, or `release`;
- permissions/capabilities relevant to artifact creation, upload, attestation, signing, publishing, or promotion;
- inbound artifacts, workspace state, caches, and reusable workflow inputs;
- outbound artifacts and provenance;
- boundary that upgrades trust, if any;
- required review/approval or protected-environment condition.

A CI principal that can execute code is not automatically a release authority. Treat untrusted PR/fork output as untrusted until a separate trusted build or verifier policy establishes acceptable provenance.

Never use or expose real credentials in this trace. Capability names and synthetic identities are sufficient.

## Cache and reuse-input trace

For any cache/reuse mechanism that can affect output identity, capture the cache/reuse binding:

- producer principal/trust context;
- source revision;
- resolved dependency identities;
- toolchain/build image;
- relevant build hook inputs;
- platform/architecture;
- policy/lifecycle generation;
- cache namespace/key/entry identity;
- consumer principal/trust context;
- resulting artifact identity.

A cache hit is not a trusted build input. If the root cause is that a key omits a security-relevant dependency, route the detailed identity proof to `cache-key-identity-analysis` and retain the supply-chain consequence here.

Useful controls include cache disabled, cache namespace separated by trust context, generation advanced, and known-good synthetic cache provenance.

## Produced-artifact identity trace

For each produced artifact, record:

- exact digest/object identity;
- source revision;
- resolved dependency graph digest or referenced identities;
- build-hook set;
- toolchain/build-environment identity;
- CI principal/trust context;
- cache/reuse provenance;
- workflow identity;
- provenance/attestation identity if generated;
- whether the artifact is the one later approved for release.

Source revision != produced artifact identity. The same source can produce different artifacts under different dependencies, hooks, toolchains, environments, or trust contexts.

## Release, signing, and publishing-authority trace

Record the release authority independently from build execution:

- principal/policy allowed to approve release;
- artifact digest being approved;
- signer identity or fake signer identity used in a synthetic fixture;
- publisher/channel authority;
- protected environment/review condition;
- release metadata identity;
- signature/attestation subject;
- whether the exact produced artifact digest is bound to the approval/signature/publish action.

A synthetic release authority can be a deterministic local policy rule; real keys are not required. Do not attempt to gain or exercise real release authority beyond explicit scope.

## Distribution and deployment binding

Capture the chain from released artifact to the bytes consumers receive and run:

- released artifact digest;
- distribution source/channel;
- distributed artifact identity as fetched from the bounded fixture;
- any authorized repackaging/transformation and its digest chain;
- deployed artifact identity;
- runtime/embedded artifact identity where relevant;
- policy decision that accepted the artifact;
- receipt or deployment evidence.

Use inert local artifacts. A safe SC3 control can substitute a marker file or metadata-bearing archive and prove wrong-artifact selection without executing untrusted code.

Released artifact != deployed artifact. Preserve each identity separately even when they happen to share the same digest.

## Lifecycle and revocation/update-generation trace

Record the lifecycle/revocation/update generation for events that can invalidate trust:

- signing-key rotation;
- publisher or builder compromise response;
- artifact withdrawal;
- dependency replacement;
- mirror-policy update;
- release revocation;
- compromised-build notification;
- required dependency update;
- rollback-policy change;
- deployed artifact generation.

For each relevant state, record who advances the generation, which verifiers/resolvers/caches/distribution/deployment components consume it, and the bounded convergence rule.

A timestamp alone is not the generation. Test stale acceptance by advancing only the synthetic generation while holding artifact identity constant.

## Controlled validation

All dynamic validation must remain synthetic, local/mock, read-only, or reversible. Preferred experiments:

1. **Source-resolution control:** same synthetic package name, two local namespaces, one intended source policy. Capture selected source and artifact digest.
2. **Immutable-identity control:** same version label, two inert archives with different digests. Confirm the policy accepts only the intended digest/source tuple.
3. **Publisher/provenance control:** same artifact bytes, two fake signer or builder identities. Confirm provenance verifier policy accepts only the authorized synthetic authority.
4. **Build-input control:** same source/dependencies, change one local build hook or toolchain identity. Capture produced digest and provenance input set.
5. **CI trust control:** same inputs, synthetic `untrusted-pr` versus `trusted-main` producer. Confirm release policy distinguishes them.
6. **Cache/reuse control:** same build with trusted cache, untrusted cache, and cache disabled. Capture cache/reuse binding and produced artifact digest.
7. **Release binding control:** same produced artifact with intended versus neighboring fake release authority. Confirm exact artifact + authority tuple.
8. **Distribution control:** same release metadata, swap only inert distributed artifact digest in a local fixture. Confirm deployment rejects mismatch.
9. **Lifecycle control:** same artifact before and after revocation/update generation advances. Confirm stale generation is rejected where policy requires.
10. **Remediation regression:** repeat the failing synthetic path after the fix and verify legitimate resolution/build/release/update behavior remains intact.

Stop if the next proof step would require a public namespace, real credential, real downstream installation, third-party artifact replacement, or irreversible state.

## False-positive controls

Require controls that separate a causal supply-chain defect from normal variation:

- intended source/namespace path succeeds;
- neighboring synthetic source is rejected;
- immutable digest match succeeds while mismatched digest fails;
- authorized fake publisher/builder succeeds while neighboring authority fails;
- trusted CI producer succeeds while untrusted synthetic producer is rejected or rebuilt;
- cache-disabled result distinguishes cache state from resolver/build state;
- deterministic rebuild or normalized comparison separates timestamps/non-security metadata;
- documented mirror/vendor equivalence preserves the same immutable digest chain;
- intended platform-specific artifact is accepted while unintended platform identity fails;
- documented repackaging preserves an auditable released-to-distributed digest chain;
- legitimate rollback/update path still works when policy explicitly permits it.

Do not treat a scanner warning, package age, mutable tag, or public CVE as a confirmed exploit path without shipped-artifact and causal evidence.

## Counterfactual controls

Vary one material dimension at a time:

- source namespace;
- mirror/fallback precedence;
- immutable artifact digest;
- expected publisher/build authority;
- build hook;
- toolchain identity;
- build image;
- CI principal/trust class;
- cache/reuse provenance;
- release authority;
- distributed artifact digest;
- deployed artifact digest;
- lifecycle/revocation/update generation.

Keep the remaining fixture state identical. A counterfactual supports causality only when the changed dimension tracks the observed acceptance, rejection, or artifact identity change.

## Alternative explanations

Before promoting evidence, test whether the observation is explained by:

- intentionally mirrored or vendored content with documented immutable equivalence;
- platform-specific authorized resolution;
- stale resolver metadata or lockfile regeneration;
- eventual mirror synchronization delay;
- harmless timestamp/non-security metadata differences in builds;
- cache-key identity defect better handled by the cache profile;
- intentionally public/shared dependency source;
- documented release repackaging or signing transformation with an auditable digest chain;
- intentionally permitted rollback window;
- stale synthetic fixture or test contamination;
- vulnerable inventory that is not actually shipped, loaded, or reachable.

Record each alternative explanation and the evidence that excludes, retains, or delegates it.

## Evidence capture

Use a compact evidence ledger. For every material transition capture:

```text
transition:
expected identity / authority / generation:
observed identity / authority / generation:
evidence source:
synthetic fixture id:
positive control:
negative control:
counterfactual:
alternative explanation status:
resulting evidence level:
evidence ceiling:
```

Prefer hashes, synthetic IDs, policy decisions, resolver traces, provenance metadata, build manifests, read-only logs, and deterministic fixture outputs. Never store real secret values.

## Evidence promotion and ceiling

Apply the supply-chain evidence ladder conservatively:

- **SC0:** surface mapped only;
- **SC1:** direct resolution/provenance/build/lifecycle divergence;
- **SC2:** deterministic identity or trust-context collision;
- **SC3:** inert wrong-artifact acceptance or propagation;
- **SC4:** bounded reversible synthetic effect on build/release/distribution/deployment;
- **SC5:** full causal proof with remediation and regression.

Promotion stops at the first unproven transition. Signature, checksum, SBOM, attestation, lockfile, or manifest evidence cannot skip missing artifact, authority, distribution, deployment, or lifecycle bindings.

The evidence ceiling must name the exact missing proof when the safe boundary prevents further promotion.

## Remediation checks

Prefer fixes at the earliest causal trust boundary:

- make source/namespace policy explicit and fail closed on unexpected sources;
- pin immutable artifact identities and remove mutable fetches from trusted builds;
- bind checksum/signature/provenance verification to expected publisher/builder and exact artifact subject;
- pin or attest build hooks, toolchains, build images, and generated inputs;
- separate untrusted CI outputs/caches from trusted build and release contexts;
- rebuild trusted artifacts rather than promoting unverifiable untrusted outputs;
- bind release approval/signature/publish steps to the exact produced artifact digest;
- verify distributed and deployed artifact identities against the approved release chain;
- propagate revocation/update generations through resolver, verifier, cache, distribution, deployment, and rollback policy.

Regression verification must show both sides: the previously failing synthetic path is blocked, and the intended dependency resolution/build/release/update path still succeeds. If remediation only adds detection while leaving the causal ambiguity or mutable trust path intact, do not mark the issue regression-verified.
