# Wave 10 Supply-Chain Dependency Depth Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add Wave 10 operator-depth profile #18 by turning `supply-chain-dependency-review` into a causal artifact-provenance proof method with deterministic synthetic review artifacts, SC0-SC5 evidence ceilings, build/CI trust reasoning, and release-to-deployment binding.

**Architecture:** Keep the canonical skill identity and routing metadata unchanged. Add a causal supply-chain model, operator runbook, deterministic review cases, one additive operator-depth registry entry, and one dedicated unittest contract; synchronize public docs only after behavioral GREEN. Preserve graph, packs, routing, benchmark, agent-eval, superiority-court, and workflow authority unchanged.

**Tech Stack:** Markdown Agent Skills, JSON registry/review fixtures, Python `unittest`, GitHub Actions matrix validation.

**Spec:** `docs/superpowers/specs/2026-09-16-wave10-supply-chain-dependency-depth-design.md`

## Global Constraints

- Base is `main@c4d43c4e5afd50cbec2a1337930f7a5de79b8137`.
- Only the nine paths enumerated in the spec may change.
- Do not modify `skills/supply-chain-dependency-review/skill.meta.json`, graph edges, packs, routing domains, benchmark fixtures/thresholds, agent-eval authority, superiority-court authority, or workflow semantics.
- Validation uses synthetic package names, local/mock registries or mirrors, inert artifact markers, deterministic builds, synthetic CI principals, fake signing identities, read-only provenance inspection, or bounded reversible owner-controlled state only.
- Never publish look-alike packages, claim third-party namespaces, poison public registries, touch real CI/release credentials, replace third-party artifacts, interfere with production dependency infrastructure, or test unauthorized targets.
- Registry schema remains version `2`.
- Dedicated profile test uses additive `>= 18`, never an exact global profile count.
- README and `docs/operator-depth-contract.md` are changed only after behavioral GREEN.
- No empirical superiority claim over Claude-Red or any external system without an actual external contestant run through the repository superiority court.

---

### Task 1: Lock the dedicated RED contract

**Files:**
- Create: `tests/test_supply_chain_dependency_depth.py`

**Interfaces:**
- Consumes: current canonical `skills/supply-chain-dependency-review/SKILL.md` and `operator-depth/profiles.json`.
- Produces: four dedicated assertions that fail until causal supply-chain skill depth, runbook, review cases, and profile #18 registration exist.

- [ ] **Step 1: Create the dedicated test first**

Create this exact test structure:

```python
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "supply-chain-dependency-review" / "SKILL.md"
RUNBOOK = ROOT / "skills" / "supply-chain-dependency-review" / "references" / "operator-runbook.md"
CASES = ROOT / "skills" / "supply-chain-dependency-review" / "references" / "operator-review-cases.json"
PROFILES = ROOT / "operator-depth" / "profiles.json"


class SupplyChainDependencyDepthTests(unittest.TestCase):
    def test_skill_exposes_causal_supply_chain_model(self):
        text = SKILL.read_text(encoding="utf-8")
        for section in (
            "## Causal supply-chain model",
            "## Dependency and source resolution",
            "## Artifact identity and immutable pinning",
            "## Integrity, signature, and provenance verification",
            "## Build hooks and toolchain identity",
            "## CI trust and cache reuse",
            "## Produced, released, distributed, and deployed artifacts",
            "## Lifecycle and revocation/update generation",
            "## Supply-chain evidence ladder",
            "## Counterfactual proof",
            "## Alternative explanations",
            "## Evidence ceiling",
        ):
            self.assertIn(section, text)

        lower = text.lower()
        for concept in (
            "declared dependency requirement -> source/namespace resolution policy -> selected package/source identity -> immutable version/ref/digest binding -> fetch origin or mirror -> integrity/signature/provenance verification -> install/build hook -> toolchain/build-environment identity -> ci principal/trust context -> cache/reuse input binding -> produced artifact identity -> release/signing/publishing authority -> distributed artifact identity -> deployed/runtime artifact identity -> bounded security-relevant effect -> lifecycle/revocation/update generation",
            "declared dependency != resolved dependency",
            "package name/version != artifact identity",
            "version pin != immutable artifact",
            "checksum match != authorized publisher provenance",
            "signature validity != release-policy authorization",
            "registry namespace != publisher identity",
            "lockfile entry != installed/shipped bytes",
            "source revision != produced artifact identity",
            "build success != hermetic or trusted build",
            "ci execution authority != release/publishing authority",
            "cache hit != trusted build input",
            "released artifact != deployed artifact",
            "sc0",
            "sc1",
            "sc2",
            "sc3",
            "sc4",
            "sc5",
            "counterfactual",
            "evidence ceiling",
        ):
            self.assertIn(concept, lower)

    def test_runbook_requires_transition_level_supply_chain_reasoning(self):
        self.assertTrue(RUNBOOK.is_file(), "supply-chain operator runbook must exist before depth can pass")
        text = RUNBOOK.read_text(encoding="utf-8")
        for section in (
            "## Attack surface",
            "## Hypothesis matrix",
            "## Dependency declaration and graph trace",
            "## Namespace and source-resolution trace",
            "## Artifact identity and immutable-pin trace",
            "## Integrity, signature, and provenance-verifier trace",
            "## Install and build-hook trace",
            "## Toolchain and build-environment trace",
            "## CI principal and trust-boundary trace",
            "## Cache and reuse-input trace",
            "## Produced-artifact identity trace",
            "## Release, signing, and publishing-authority trace",
            "## Distribution and deployment binding",
            "## Lifecycle and revocation/update-generation trace",
            "## Controlled validation",
            "## False-positive controls",
            "## Counterfactual controls",
            "## Alternative explanations",
            "## Evidence capture",
            "## Evidence promotion and ceiling",
            "## Remediation checks",
        ):
            self.assertIn(section, text)

        lower = text.lower()
        for phrase in (
            "source resolution policy",
            "artifact identity",
            "immutable pin",
            "provenance verifier",
            "build hook",
            "toolchain identity",
            "ci principal",
            "cache/reuse",
            "release authority",
            "distributed artifact",
            "deployed artifact",
            "revocation/update generation",
            "alternative explanation",
            "evidence ceiling",
        ):
            self.assertIn(phrase, lower)

    def test_review_cases_encode_supply_chain_reasoning(self):
        self.assertTrue(CASES.is_file(), "supply-chain review-case matrix must exist before depth can pass")
        payload = json.loads(CASES.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 1)
        self.assertGreaterEqual(len(payload["scenarios"]), 3)
        required = (
            "hypothesis",
            "safe_oracle",
            "positive_control",
            "negative_control",
            "stop_condition",
            "remediation_oracle",
            "declared_requirement",
            "source_resolution_policy",
            "selected_namespace_source",
            "selected_artifact_identity",
            "immutable_pin_integrity_state",
            "provenance_verifier_decision",
            "install_build_hook",
            "toolchain_build_environment",
            "ci_principal_trust_context",
            "cache_reuse_input_binding",
            "produced_artifact_identity",
            "release_signing_publishing_authority",
            "distributed_artifact_identity",
            "deployed_runtime_artifact_identity",
            "bounded_effect",
            "lifecycle_revocation_update_generation",
            "counterfactual_control",
            "alternative_explanation",
            "evidence_level",
            "evidence_ceiling",
        )
        for scenario in payload["scenarios"]:
            for field in required:
                self.assertIn(field, scenario)
                self.assertIsInstance(scenario[field], str)
                self.assertGreaterEqual(len(scenario[field].strip()), 40)

    def test_skill_is_registered_as_eighteenth_operator_depth_profile(self):
        payload = json.loads(PROFILES.read_text(encoding="utf-8"))
        profiles = payload["profiles"]
        self.assertGreaterEqual(len(profiles), 18)
        matching = [p for p in profiles if p["skill"] == "supply-chain-dependency-review"]
        self.assertEqual(len(matching), 1)
        profile = matching[0]
        self.assertEqual(profile["runbook"], "references/operator-runbook.md")
        self.assertEqual(profile["scenario_matrix"], "references/operator-review-cases.json")
        self.assertTrue(profile["lab_only"])
        self.assertEqual(
            profile["required_runbook_sections"],
            [
                "Attack surface",
                "Hypothesis matrix",
                "Controlled validation",
                "False-positive controls",
                "Evidence capture",
                "Remediation checks",
            ],
        )


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Commit test-first without implementation artifacts**

Commit message: `test: lock supply-chain dependency depth contract`.

- [ ] **Step 3: Open a Draft PR on the test-first SHA and run the full workflow**

A valid RED run has exactly four dedicated assertion failures and zero unittest errors. Canonical-skill validation, current 17-profile operator-depth validation, graph/generated-index checks, benchmark validation, portability, and agent-eval portability smoke must remain healthy before the dedicated contract fails. Unexpected failures must be debugged, never normalized away.

---

### Task 2: Implement the causal supply-chain depth artifacts

**Files:**
- Modify: `skills/supply-chain-dependency-review/SKILL.md`
- Create: `skills/supply-chain-dependency-review/references/operator-runbook.md`
- Create: `skills/supply-chain-dependency-review/references/operator-review-cases.json`
- Modify: `operator-depth/profiles.json`
- Test: `tests/test_supply_chain_dependency_depth.py`

**Interfaces:**
- Consumes: the exact RED contract from Task 1 and the causal model in the design spec.
- Produces: canonical skill depth, operator runbook, deterministic review cases, and additive profile registration #18.

- [ ] **Step 1: Deepen `SKILL.md` while preserving the existing frontmatter exactly**

The body must include these headings:

```text
## When to use
## Preconditions
## Causal supply-chain model
## Dependency and source resolution
## Artifact identity and immutable pinning
## Integrity, signature, and provenance verification
## Build hooks and toolchain identity
## CI trust and cache reuse
## Produced, released, distributed, and deployed artifacts
## Lifecycle and revocation/update generation
## Workflow
## Supply-chain evidence ladder
## Counterfactual proof
## Alternative explanations
## Evidence contract
## Evidence ceiling
## Stop conditions
## Output
```

Include the exact causal chain and distinctions frozen by Task 1; define SC0-SC5 exactly enough to preserve the evidence ceiling; route pure cache-key, generic authorization, secret-flow, and canonicalization failures to adjacent skills; forbid public package publication, real credential use, and unauthorized registry/release interaction.

- [ ] **Step 2: Create the operator runbook**

Include all exact headings required by Task 1. Each trace records observed value, expected value, evidence source, trust generation, and whether the transition is authoritative. Controlled validation uses synthetic package names, local/mock registries/mirrors, inert artifact bytes, deterministic build manifests, synthetic CI principals, fake signer identities, and reversible deployment fixtures only.

- [ ] **Step 3: Create deterministic review cases**

Create JSON version `1` with exactly these three initial scenario IDs:

```text
dependency-resolution-and-namespace-binding
build-input-and-ci-trust-provenance
release-artifact-and-lifecycle-binding
```

Every field required by Task 1 must be a substantive string of at least 40 characters. Each case includes a safe oracle, positive/negative controls, explicit stop condition, remediation oracle, counterfactual, alternative explanation, evidence level, and evidence ceiling. No case may require publishing to a public registry, using a real release credential, or altering third-party artifacts.

- [ ] **Step 4: Register profile #18 additively**

Add exactly one entry:

```json
{
  "skill": "supply-chain-dependency-review",
  "runbook": "references/operator-runbook.md",
  "scenario_matrix": "references/operator-review-cases.json",
  "lab_only": true,
  "required_runbook_sections": [
    "Attack surface",
    "Hypothesis matrix",
    "Controlled validation",
    "False-positive controls",
    "Evidence capture",
    "Remediation checks"
  ]
}
```

Preserve registry version `2` and every existing profile unchanged.

- [ ] **Step 5: Verify dedicated behavior**

Run:

```text
python -m unittest tests.test_supply_chain_dependency_depth -v
python scripts/validate_operator_depth.py
```

Expected: all four dedicated tests pass and operator-depth validation passes with at least 18 profiles.

- [ ] **Step 6: Commit behavioral implementation**

Commit message: `feat: deepen supply-chain dependency reasoning`.

- [ ] **Step 7: Require behavioral full GREEN**

All six Ubuntu/macOS/Windows × Python 3.11/3.13 matrix jobs plus `benchmark-core`, `agent-eval-core`, and `superiority-court-core` must succeed. Public docs remain untouched until this exact behavioral SHA is fully GREEN.

---

### Task 3: Synchronize public documentation after behavioral GREEN

**Files:**
- Modify: `README.md`
- Modify: `docs/operator-depth-contract.md`

**Interfaces:**
- Consumes: verified profile #18 behavioral implementation.
- Produces: public snapshot synchronized to 18 profiles without changing behavior.

- [ ] **Step 1: Update README current counts and Wave 10 narrative**

Change current operator-depth totals from 17 to 18. Add `supply-chain-dependency-review` as the eighteenth profile and summarize source/namespace resolution, immutable artifact identity, provenance verification, build/toolchain identity, CI trust, cache/reuse binding, release authority, distribution/deployment binding, lifecycle generation, deterministic audit-only cases, counterfactual controls, and SC0-SC5 evidence ceilings.

- [ ] **Step 2: Update `docs/operator-depth-contract.md`**

Append `supply-chain-dependency-review` as the eighteenth Wave 10 profile and update the current registry count to 18, preserving Wave 8 history and profiles #9-#17 unchanged.

- [ ] **Step 3: Prove post-GREEN delta is docs-only**

Compare behavioral GREEN SHA to docs head and require exactly:

```text
README.md
docs/operator-depth-contract.md
```

- [ ] **Step 4: Commit docs-only finalization**

Commit message: `docs: publish supply-chain dependency depth`.

---

### Task 4: Exact-head verification, guarded merge, and post-merge closure

**Files:**
- No additional repository files after the final candidate is fixed.
- PR metadata/comments only.

**Interfaces:**
- Consumes: final candidate with exactly the nine scoped paths.
- Produces: exact-head CI evidence, guarded merge, post-merge CI evidence, and closure provenance.

- [ ] **Step 1: Update Draft PR provenance**

Record base SHA, spec commit, plan commit, test-first SHA, RED run, behavioral GREEN SHA/run, final candidate SHA, exact nine-file scope, unchanged authority surfaces, and safety boundary.

- [ ] **Step 2: Verify exact scope**

Require exactly the nine paths in the spec and no others. Confirm post-behavioral-GREEN delta contains only the two public docs.

- [ ] **Step 3: Require final exact-head full GREEN**

On the final candidate SHA require 6/6 matrix SUCCESS plus `benchmark-core`, `agent-eval-core`, and `superiority-court-core` SUCCESS.

- [ ] **Step 4: Fresh integration checks**

Verify PR head still equals the exact final candidate, base is still `main`, PR is mergeable, changed files remain exactly nine, and `main` has not drifted from the expected base. If `main` moved, stop merge and reconcile lineage before integration.

- [ ] **Step 5: Mark Ready and merge with expected-head guard**

Use merge method `merge` and exact `expected_head_sha=<final-candidate-sha>`.

- [ ] **Step 6: Verify merge commit lineage**

Require `main` to point at the returned merge SHA and require the merge commit parents to be the prior base SHA and exact final candidate SHA.

- [ ] **Step 7: Require post-merge push CI full GREEN**

Find the workflow run with `event=push`, `head_branch=main`, and `head_sha=<merge-sha>`. Require 6/6 matrix SUCCESS plus all three core jobs SUCCESS.

- [ ] **Step 8: Verify closure state on merge SHA**

Fetch `operator-depth/profiles.json` at the merge SHA and require version `2`, at least 18 profiles, and exactly one `supply-chain-dependency-review`. Verify README and operator-depth contract both publish 18 profiles and identify supply-chain review as the eighteenth profile.

- [ ] **Step 9: Record final closure provenance**

Add one top-level PR comment containing merge SHA, exact-head run, post-merge run, scope proof, registry proof, docs proof, and explicit statement that no external-superiority claim was made without an external contestant run.
