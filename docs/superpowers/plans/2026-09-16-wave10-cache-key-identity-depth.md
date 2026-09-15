# Wave 10 Cache-Key Identity Depth Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add Wave 10 operator-depth profile #15 by turning `cache-key-identity-analysis` into a causal cache-identity method with deterministic audit artifacts, K0-K5 evidence ceilings, lifecycle reasoning, and CI-enforced contracts.

**Architecture:** Keep the existing canonical skill identity and routing unchanged. Add a cache-specific causal model, operator runbook, deterministic synthetic review cases, one additive operator-depth registry entry, and one dedicated contract test; synchronize public docs only after behavioral GREEN. Preserve graph, packs, routing, benchmark, agent-eval, and superiority-court authority unchanged.

**Tech Stack:** Markdown Agent Skills, JSON registry/review fixtures, Python `unittest`, GitHub Actions matrix validation.

**Spec:** `docs/superpowers/specs/2026-09-16-wave10-cache-key-identity-depth-design.md`

## Global Constraints

- Base is `main@787fb28377f51edd3799ee5bd1e12881b94abd27`.
- Only the nine paths enumerated in the spec may change.
- Do not modify `skill.meta.json`, graph edges, packs, routing domains, benchmark fixtures/thresholds, agent-eval authority, or superiority-court authority.
- Dynamic validation is restricted to synthetic principals/tenants, mock or read-only caches, inert markers, deterministic policy simulators, or reversible owner-controlled state.
- No real credentials, third-party data, persistence mechanisms, destructive actions, evasion, malware, or unauthorized targets.
- Registry schema remains version `2`.
- Dedicated profile test uses additive `>= 15`, never an exact global profile count.
- README and `docs/operator-depth-contract.md` are changed only after behavioral GREEN.
- Do not claim empirical superiority over Claude-Red or any external system without an actual contestant run through the repository superiority court.

---

### Task 1: Lock the dedicated RED contract

**Files:**
- Create: `tests/test_cache_key_identity_depth.py`

**Interfaces:**
- Consumes: current canonical `skills/cache-key-identity-analysis/SKILL.md` and `operator-depth/profiles.json`.
- Produces: four dedicated assertions that fail until causal skill depth, runbook, review cases, and profile #15 registration exist.

- [ ] **Step 1: Create the dedicated test first**

Use this exact structure:

```python
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "cache-key-identity-analysis" / "SKILL.md"
RUNBOOK = ROOT / "skills" / "cache-key-identity-analysis" / "references" / "operator-runbook.md"
CASES = ROOT / "skills" / "cache-key-identity-analysis" / "references" / "operator-review-cases.json"
PROFILES = ROOT / "operator-depth" / "profiles.json"


class CacheKeyIdentityDepthTests(unittest.TestCase):
    def test_skill_exposes_causal_cache_identity_model(self):
        text = SKILL.read_text(encoding="utf-8")
        for section in (
            "## Causal cache-identity model",
            "## Dependency completeness",
            "## Key construction and canonicalization",
            "## Namespace and entry identity",
            "## Writer and reader provenance",
            "## First-writer and replay order",
            "## Lifecycle and invalidation generation",
            "## Cache identity evidence ladder",
            "## Counterfactual proof",
            "## Alternative explanations",
            "## Evidence ceiling",
        ):
            self.assertIn(section, text)

        lower = text.lower()
        for concept in (
            "semantic invocation -> security-relevant dependency set -> canonical key inputs -> serialized key -> cache namespace -> cache entry identity -> writer principal/context -> stored result provenance -> reader principal/context -> freshness/invalidation generation -> replayed result -> bounded security decision/effect",
            "semantic invocation != serialized key",
            "serialized key != cache entry identity",
            "cache entry identity != security identity",
            "writer context != reader context",
            "key equality != dependency equivalence",
            "freshness timestamp != invalidation generation",
            "k0",
            "k1",
            "k2",
            "k3",
            "k4",
            "k5",
            "counterfactual",
            "evidence ceiling",
        ):
            self.assertIn(concept, lower)

    def test_runbook_requires_transition_level_cache_identity_reasoning(self):
        self.assertTrue(RUNBOOK.is_file(), "cache-key operator runbook must exist before depth can pass")
        text = RUNBOOK.read_text(encoding="utf-8")
        for section in (
            "## Attack surface",
            "## Hypothesis matrix",
            "## Semantic dependency trace",
            "## Key-construction trace",
            "## Canonicalization and serialization trace",
            "## Namespace and entry-identity trace",
            "## Writer and reader provenance trace",
            "## First-writer and replay-order trace",
            "## Lifecycle and invalidation-generation trace",
            "## Result and effect binding",
            "## Controlled validation",
            "## False-positive controls",
            "## Counterfactual controls",
            "## Evidence capture",
            "## Evidence promotion and ceiling",
            "## Remediation checks",
        ):
            self.assertIn(section, text)

        lower = text.lower()
        for phrase in (
            "security-relevant dependency",
            "serialized key",
            "cache namespace",
            "cache entry identity",
            "writer context",
            "reader context",
            "invalidation generation",
            "reverse order",
            "counterfactual",
            "alternative explanation",
            "evidence ceiling",
        ):
            self.assertIn(phrase, lower)

    def test_review_cases_encode_cache_identity_reasoning(self):
        self.assertTrue(CASES.is_file(), "cache-key review-case matrix must exist before depth can pass")
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
            "semantic_invocation",
            "security_dependency_set",
            "canonical_key_inputs",
            "serialized_key",
            "cache_namespace",
            "cache_entry_identity",
            "writer_context",
            "stored_result_provenance",
            "reader_context",
            "invalidation_generation",
            "replayed_result",
            "bounded_effect",
            "reverse_order_control",
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

    def test_skill_is_registered_as_fifteenth_operator_depth_profile(self):
        payload = json.loads(PROFILES.read_text(encoding="utf-8"))
        profiles = payload["profiles"]
        self.assertGreaterEqual(len(profiles), 15)
        matching = [p for p in profiles if p["skill"] == "cache-key-identity-analysis"]
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

- [ ] **Step 2: Commit the test without implementation artifacts**

Commit message:

```text
test: lock cache-key identity depth contract
```

- [ ] **Step 3: Run the full repository workflow and record clean RED**

Expected dedicated failures:

- missing causal cache-identity sections/concepts in the current skill;
- missing `references/operator-runbook.md`;
- missing `references/operator-review-cases.json`;
- no `cache-key-identity-analysis` entry and fewer than 15 profiles.

The RED run is valid only if existing canonical-skill, current operator-depth, graph/index, benchmark, portability, and agent-eval prechecks remain healthy before the dedicated test fails. Unexpected unittest errors or unrelated failures must be debugged rather than accepted.

---

### Task 2: Implement the causal cache-identity depth artifacts

**Files:**
- Modify: `skills/cache-key-identity-analysis/SKILL.md`
- Create: `skills/cache-key-identity-analysis/references/operator-runbook.md`
- Create: `skills/cache-key-identity-analysis/references/operator-review-cases.json`
- Modify: `operator-depth/profiles.json`
- Test: `tests/test_cache_key_identity_depth.py`

**Interfaces:**
- Consumes: the exact RED contract from Task 1 and the causal model in the design spec.
- Produces: canonical skill depth, operator runbook, deterministic review cases, and additive profile registration #15.

- [ ] **Step 1: Replace the short workflow-oriented skill body with the causal model while preserving frontmatter identity**

The resulting `SKILL.md` must contain these exact headings:

```text
## When to use
## Preconditions
## Causal cache-identity model
## Dependency completeness
## Key construction and canonicalization
## Namespace and entry identity
## Writer and reader provenance
## First-writer and replay order
## Lifecycle and invalidation generation
## Workflow
## Cache identity evidence ladder
## Counterfactual proof
## Alternative explanations
## Evidence contract
## Evidence ceiling
## Stop conditions
## Output
```

It must include the exact causal chain and distinctions frozen by the test, define K0-K5 exactly as the spec, explain that omitted dimensions may be safe only when proven invariant, and keep dynamic validation synthetic/owned/read-only/reversible.

- [ ] **Step 2: Create the operator runbook**

`operator-runbook.md` must include every section required by the test. For each trace, require capture of both the observed value and the proof source. The controlled-validation section must prescribe synthetic A->B and B->A ordering, one-dimension counterfactuals, generation advancement, corrected-key/corrected-generation remediation, and preservation of legitimate same-context hits.

- [ ] **Step 3: Create deterministic review cases**

Create JSON version `1` with exactly three initial scenarios named:

```text
dependency-to-key-completeness
canonical-key-and-namespace-identity
writer-reader-lifecycle-binding
```

Every required field in Task 1 must be a substantive string of at least 40 characters. Use only synthetic principals/tenants, inert markers, mock cache entries, deterministic policy generations, and reversible owner-controlled effects. Each scenario must contain a safe oracle, positive/negative controls, stop condition, remediation oracle, counterfactual, alternative explanation, evidence level, and evidence ceiling.

- [ ] **Step 4: Register profile #15 additively**

Add exactly one entry to `operator-depth/profiles.json`:

```json
{
  "skill": "cache-key-identity-analysis",
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

Preserve schema version `2` and all existing profile entries unchanged.

- [ ] **Step 5: Run the dedicated test and operator-depth validator**

Expected:

```text
python -m unittest tests.test_cache_key_identity_depth -v
# 4 tests, all PASS

python scripts/validate_operator_depth.py
# PASS with >= 15 profiles and no schema/path errors
```

- [ ] **Step 6: Commit the behavioral implementation**

Commit message:

```text
feat: deepen cache-key identity reasoning
```

- [ ] **Step 7: Run the full GitHub Actions workflow and require behavioral GREEN**

All six Ubuntu/macOS/Windows x Python 3.11/3.13 matrix jobs plus `benchmark-core`, `agent-eval-core`, and `superiority-court-core` must succeed. Do not touch public docs until this GREEN run is recorded on the behavioral implementation SHA.

---

### Task 3: Synchronize public documentation after behavioral GREEN

**Files:**
- Modify: `README.md`
- Modify: `docs/operator-depth-contract.md`

**Interfaces:**
- Consumes: verified profile #15 behavioral implementation from Task 2.
- Produces: public snapshot and operator-depth history synchronized to 15 profiles without changing behavior.

- [ ] **Step 1: Update README counts and Wave 10 narrative**

Change every current operator-depth total from 14 to 15 where it describes the current baseline. Add `cache-key-identity-analysis` as the fifteenth profile and summarize its causal contribution as dependency-to-key completeness, serialized-key/namespace identity, writer/reader provenance, replay order, lifecycle/invalidation generations, counterfactual controls, deterministic audit-only review cases, and K0-K5 evidence ceilings.

- [ ] **Step 2: Update `docs/operator-depth-contract.md`**

Append `cache-key-identity-analysis` as the fifteenth Wave 10 profile and update the current registry count to 15. Preserve the historical Wave 8 count and all prior profile descriptions unchanged.

- [ ] **Step 3: Verify the docs-only delta**

Compare the behavioral GREEN SHA to the docs commit and require exactly these two paths:

```text
README.md
docs/operator-depth-contract.md
```

No skill, test, registry, workflow, benchmark, agent-eval, or superiority-court artifact may change after behavioral GREEN.

- [ ] **Step 4: Commit docs**

Commit message:

```text
docs: publish cache-key identity depth
```

---

### Task 4: Exact-head verification and PR closure

**Files:**
- No new behavioral files.
- PR metadata/provenance only after the final candidate SHA is fixed.

**Interfaces:**
- Consumes: final candidate containing Tasks 1-3 only.
- Produces: exact-head CI evidence, reviewable PR provenance, and guarded merge.

- [ ] **Step 1: Open a Draft PR from `wave10-cache-key-identity-depth` to `main`**

PR body must record base SHA, design/plan commits, RED run, behavioral GREEN SHA/run, final candidate SHA, exact nine-file scope, unchanged authority surfaces, and safety boundary. Explicitly state that no empirical superiority over external systems is claimed.

- [ ] **Step 2: Verify exact changed-file scope**

Require exactly the nine paths from the design spec and no others.

- [ ] **Step 3: Require exact-head full CI GREEN**

On the final candidate SHA, require all six matrix jobs plus `benchmark-core`, `agent-eval-core`, and `superiority-court-core` to complete successfully. If any job fails, inspect steps/logs and debug the root cause before changing the branch.

- [ ] **Step 4: Mark Ready only after exact-head GREEN**

Re-read PR head/base immediately before the transition. Head must still equal the exact verified candidate and base must remain the intended `main` lineage.

- [ ] **Step 5: Merge with expected-head SHA guard**

Use the final candidate SHA as `expected_head_sha`. Abort rather than merge if GitHub reports drift.

---

### Task 5: Post-merge verification

**Files:**
- No source changes.

**Interfaces:**
- Consumes: actual merge commit returned by GitHub.
- Produces: final closure evidence for operator-depth profile #15.

- [ ] **Step 1: Verify `main` points to the merge commit**

Confirm the merge commit has the previous `main` and final candidate as parents.

- [ ] **Step 2: Locate the push-triggered workflow on the merge SHA**

Require event `push`, branch `main`, and exact merge `head_sha`.

- [ ] **Step 3: Require post-merge full GREEN**

All six matrix jobs plus `benchmark-core`, `agent-eval-core`, and `superiority-court-core` must succeed on the merge commit.

- [ ] **Step 4: Record final provenance on the PR**

Record merge SHA and post-merge run ID. Only after this fresh evidence may profile #15 be called fully closed and the main registry described as 15 operator-depth profiles.
