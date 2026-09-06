---
name: supply-chain-dependency-review
description: "Review software dependency and build provenance for owned or authorized projects: direct/transitive dependencies, lockfiles, registries, build scripts, generated artifacts, vendoring, release provenance, typosquatting/confusion exposure, and update controls. Use for secure build and dependency-risk analysis."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Supply Chain Dependency Review

Supply-chain review connects dependency identity to the artifact that actually ships. A clean manifest is insufficient if the build downloads mutable tools, executes unpinned scripts, or vendors a different revision.

## When to use

Use for application/package builds, containers, CI pipelines, vendored native libraries, language package managers, release automation, or dependency incident response.

## Preconditions

Operate on owned repositories/builds or explicit authorization. Do not publish look-alike packages, poison registries, or interact with third-party namespaces to demonstrate dependency confusion.

## Workflow

1. **Map dependency sources.** Registry, git URL, archive URL, system package, vendored source, generated code, build image, compiler/plugin.
2. **Resolve direct and transitive graph** from lockfiles/build metadata and compare to runtime/container artifacts.
3. **Check identity pinning.** Exact version, commit, digest, checksum, signature/provenance, immutable tag.
4. **Check namespace ambiguity.** Internal package names versus public registries, fallback order, scoped namespaces, mirror behavior.
5. **Inspect install/build hooks.** Scripts, plugins, code generation, post-install, native compilation, fetched toolchains.
6. **Inspect CI trust boundary.** Pull-request code, secrets, cache poisoning, artifact reuse, reusable workflows, runner persistence.
7. **Check release provenance.** Who can publish, sign, alter tags/releases, or replace build artifacts?
8. **Inventory duplicate embedded copies** that may remain vulnerable after central package update.
9. **Validate non-destructively.** Resolver dry-runs, lock verification, artifact SBOM/provenance comparison, controlled internal namespace fixtures.
10. **Prioritize controls** by removing ambiguity and mutable network fetches before adding detection-only layers.

## Evidence contract

Show the dependency/artifact identity gap or trust path using manifests, lock/provenance data, resolver behavior, and shipped artifact evidence. A package having a known vulnerability is inventory evidence; reachability/impact is a separate analysis.

## Stop conditions

Stop if proof would require publishing/claiming third-party package names, altering external registries, leaking CI secrets, or making unapproved changes to release infrastructure.

## Output

```text
build/release target:
dependency sources:
lock/pin/provenance status:
namespace ambiguity:
build/install hooks:
CI trust boundaries:
shipped artifact comparison:
validated supply-chain risk:
recommended control:
```
