# Wave 10 Confused Deputy Depth Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add Wave 10 operator-depth profile #14 by turning `confused-deputy-analysis` into a causal authority-transfer method with deterministic audit artifacts, evidence ceilings, and CI-enforced contracts.

**Architecture:** Keep the existing canonical skill identity and routing intact. Add a deputy-specific causal model, operator runbook, audit-only deterministic review cases, one additive registry entry, and one dedicated contract test; update public docs only after behavioral GREEN. Preserve all graph, pack, routing, benchmark, agent-eval, and superiority-court authority unchanged.

**Tech Stack:** Markdown Agent Skills, JSON registry/review fixtures, Python `unittest`, GitHub Actions matrix validation.

**Spec:** `docs/superpowers/specs/2026-09-15-wave10-confused-deputy-depth-design.md`

## Global Constraints

- Base is `main@be7a59bf725949eaceb346894b4c2a6f53093577`.
- Only the nine paths enumerated in the spec may change.
- Do not modify `skill.meta.json`, graph edges, packs, routing domains, benchmark fixtures/thresholds, agent-eval authority, or superiority-court authority.
- Dynamic validation is restricted to synthetic principals, mock/read-only deputies, inert markers, or reversible owner-controlled state.
- No real credentials, persistence, destructive action, evasion, malware, or third-party effects.
- Registry schema remains version `2`.
- Dedicated profile test uses additive `>= 14`, never an exact global profile count.
- README and `docs/operator-depth-contract.md` are changed only after behavioral GREEN.

---

### Task 1: Lock a dedicated RED contract

**Files:**
- Create: `tests/test_confused_deputy_depth.py`

**Interfaces:**
- Consumes: current canonical skill, `operator-depth/profiles.json`.
- Produces: four dedicated assertions that fail until canonical depth, runbook, review cases, and profile #14 exist.

- [ ] **Step 1: Create the dedicated test first**

Use this structure:

```python
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "confused-deputy-analysis" / "SKILL.md"
RUNBOOK = ROOT / "skills" / "confused-deputy-analysis" / "references" / "operator-runbook.md"
CASES = ROOT / "skills" / "confused-deputy-analysis" / "references" / "operator-review-cases.json"
PROFILES = ROOT / "operator-depth" / "profiles.json"


class ConfusedDeputyDepthTests(unittest.TestCase):
    def test_skill_exposes_causal_authority_transfer_model(self):
        text = SKILL.read_text(encoding="utf-8")
        for section in (
            "## Causal authority-transfer model",
            "## Authority conservation and attenuation",
            "## Delegation as structured authority",
            "## Multi-hop authority trace",
            "## Deputy ambient authority",
            "## Operation and resource binding",
            "## Result and receipt binding",
            "## Delegation generation and lifecycle",
            "## Deputy evidence ladder",
            "## Counterfactual proof",
            "## Alternative explanations",
            "## Evidence ceiling",
        ):
            self.assertIn(section, text)

        lower = text.lower()
        for concept in (
            "request origin -> authenticated principal -> initiating authority -> delegation artifact -> requested operation -> requested resource -> deputy identity -> deputy ambient authority -> policy decision -> attenuated effective authority -> resolved target identity -> bounded effect -> receipt/result binding",
            "authenticated principal != delegated authority != deputy ambient authority != attenuated effective authority",
            "authority attenuation",
            "delegation generation",
            "resolved target identity",
            "result binding",
            "d0",
            "d1",
            "d2",
            "d3",
            "d4",
            "d5",
            "counterfactual",
            "evidence ceiling",
        ):
            self.assertIn(concept, lower)

    def test_runbook_requires_transition_level_authority_reasoning(self):
        self.assertTrue(RUNBOOK.is_file(), "confused-deputy operator runbook must exist before depth can pass")
        text = RUNBOOK.read_text(encoding="utf-8")
        for section in (
            "## Attack surface",
            "## Hypothesis matrix",
            "## Authority-transfer trace",
            "## Delegation trace",
            "## Ambient-authority and attenuation trace",
            "## Operation/resource binding",
            "## Multi-hop authority trace",
            "## Target identity binding",
            "## Result and receipt binding",
            "## Delegation generation and lifecycle trace",
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
            "initiating principal",
            "initiating authority",
            "delegation artifact",
            "deputy ambient authority",
            "attenuated effective authority",
            "resolved target identity",
            "delegation generation",
            "result binding",
            "counterfactual",
            "alternative explanation",
            "evidence ceiling",
        ):
            self.assertIn(phrase, lower)

    def test_review_cases_encode_authority_transfer_reasoning(self):
        self.assertTrue(CASES.is_file(), "confused-deputy review-case matrix must exist before depth can pass")
        payload = json.loads(CASES.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 1)
        self.assertGreaterEqual(len(payload["scenarios"]), 3)
        for scenario in payload["scenarios"]:
            for field in (
                "hypothesis",
                "safe_oracle",
                "positive_control",
                "negative_control",
                "stop_condition",
                "remediation_oracle",
                "request_origin",
                "authenticated_principal",
                "initiating_authority",
                "delegation_artifact",
                "requested_operation",
                "requested_resource",
                "deputy_identity",
                "deputy_ambient_authority",
                "policy_decision",
                "attenuated_effective_authority",
                "resolved_target_identity",
                "bounded_effect",
                "result_binding",
                "delegation_generation",
                "counterfactual_control",
                "alternative_explanation",
                "evidence_level",
                "evidence_ceiling",
            ):
                self.assertIn(field, scenario)
                self.assertIsInstance(scenario[field], str)
                self.assertGreaterEqual(len(scenario[field].strip()), 40)

    def test_skill_is_registered_as_fourteenth_operator_depth_profile(self):
        payload = json.loads(PROFILES.read_text(encoding="utf-8"))
        profiles = payload["profiles"]
        self.assertGreaterEqual(len(profiles), 14)
        matching = [p for p in profiles if p["skill"] == "confused-deputy-analysis"]
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

- [ ] **Step 2: Commit only the test**

Commit message: `test: specify confused deputy operator depth`.

- [ ] **Step 3: Open a Draft PR against `main`**

The Draft PR body records the base SHA and test-first commit SHA. Do not claim GREEN.

- [ ] **Step 4: Verify clean RED in CI**

Expected dedicated outcome: exactly four intended assertion failures and zero unittest errors. Existing canonical validation, 13-profile central validator, graph/index checks, benchmark validation, portability, and agent-eval smoke must remain green before the dedicated test fails.

### Task 2: Add the canonical authority-transfer methodology

**Files:**
- Modify: `skills/confused-deputy-analysis/SKILL.md`

**Interfaces:**
- Consumes: existing skill frontmatter, preconditions, high-level purpose, and the design spec.
- Produces: canonical causal authority-transfer model and D0-D5 evidence semantics used by the runbook and review cases.

- [ ] **Step 1: Preserve frontmatter and authorization boundary**

Keep the existing skill name/category/version/authorization metadata. Preserve the owned/local/sandboxed/explicitly-authorized constraint.

- [ ] **Step 2: Replace shallow workflow-only reasoning with the causal model**

Add these exact headings:

```text
## Causal authority-transfer model
## Authority conservation and attenuation
## Delegation as structured authority
## Multi-hop authority trace
## Deputy ambient authority
## Operation and resource binding
## Result and receipt binding
## Delegation generation and lifecycle
## Deputy evidence ladder
## Counterfactual proof
## Alternative explanations
## Evidence ceiling
```

Include the exact causal chain and authority inequality from the spec. Define the ten invariants, delegation fields, per-hop trace, lifecycle state, result binding, D0-D5 ladder, and ceiling rules. Keep guidance defensive and audit-oriented.

- [ ] **Step 3: Preserve routing boundaries**

Explicitly route general authorization, connector provenance, tool confirmation, canonical target identity, and cloud IAM details to their existing canonical skills rather than duplicating them.

- [ ] **Step 4: Commit the canonical skill**

Commit message: `feat: deepen confused deputy authority reasoning`.

### Task 3: Add audit-only operator artifacts and registry entry

**Files:**
- Create: `skills/confused-deputy-analysis/references/operator-runbook.md`
- Create: `skills/confused-deputy-analysis/references/operator-review-cases.json`
- Modify: `operator-depth/profiles.json`

**Interfaces:**
- Consumes: canonical D0-D5 methodology.
- Produces: CI-valid runbook, deterministic synthetic cases, and exactly one profile #14 registry entry.

- [ ] **Step 1: Create the runbook**

The runbook must contain these exact headings:

```text
## Attack surface
## Hypothesis matrix
## Authority-transfer trace
## Delegation trace
## Ambient-authority and attenuation trace
## Operation/resource binding
## Multi-hop authority trace
## Target identity binding
## Result and receipt binding
## Delegation generation and lifecycle trace
## Controlled validation
## False-positive controls
## Counterfactual controls
## Evidence capture
## Evidence promotion and ceiling
## Remediation checks
```

Each trace is written as an audit worksheet. It must use the terms `initiating principal`, `initiating authority`, `delegation artifact`, `deputy ambient authority`, `attenuated effective authority`, `resolved target identity`, `delegation generation`, `result binding`, `counterfactual`, `alternative explanation`, and `evidence ceiling`.

- [ ] **Step 2: Create deterministic review cases**

Create JSON object:

```json
{
  "version": 1,
  "scenarios": [
    {"id": "principal-authority-binding"},
    {"id": "delegation-attenuation-consistency"},
    {"id": "deputy-result-binding"}
  ]
}
```

Expand each scenario with every string field required by the dedicated test and spec. Every field value must contain at least 40 non-whitespace characters. Use only synthetic principals, mock/read-only deputies, inert markers, or reversible owner-controlled state. Each scenario has explicit safe oracle, positive and negative controls, stop condition, remediation oracle, counterfactual, alternative explanation, current evidence level, and evidence ceiling.

- [ ] **Step 3: Register profile #14 additively**

Add exactly one entry for `confused-deputy-analysis` to `operator-depth/profiles.json` with:

```json
{
  "skill": "confused-deputy-analysis",
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

Keep version `2`. Do not reorder unrelated entries unless required by the existing registry convention.

- [ ] **Step 4: Commit operator artifacts and registry**

Commit message: `feat: add confused deputy operator profile`.

### Task 4: Prove behavioral GREEN before docs

**Files:**
- No new files.

**Interfaces:**
- Consumes: Task 1-3 behavioral tree.
- Produces: fixed behavioral checkpoint SHA and CI evidence.

- [ ] **Step 1: Freeze the behavioral SHA**

Do not update README or public operator-depth docs yet.

- [ ] **Step 2: Verify the full six-job matrix**

Require SUCCESS on Ubuntu/macOS/Windows × Python 3.11/3.13. Confirm canonical validation, 14-profile operator-depth validator, graph/index checks, benchmark validation, portability, agent-eval contracts/smoke, and full tests.

- [ ] **Step 3: Verify the three core determinism jobs**

Require SUCCESS for:

- `benchmark-core`, including double-run byte-identical result;
- `agent-eval-core`, including task/eval/matrix determinism and cautious/faulty controls;
- `superiority-court-core`, including contestant view/task/score/court determinism.

Stop and debug any failure before public docs.

### Task 5: Synchronize public docs only after behavioral GREEN

**Files:**
- Modify: `README.md`
- Modify: `docs/operator-depth-contract.md`

**Interfaces:**
- Consumes: proven behavioral checkpoint.
- Produces: public 14-profile documentation without changing authority contracts.

- [ ] **Step 1: Update the operator-depth contract**

Change the current registry count from 13 to 14 and add the confused-deputy Wave 10 entry. Describe causal authority transfer, attenuation, delegation generation, result binding, counterfactual controls, and D0-D5 ceilings.

- [ ] **Step 2: Update README**

Change public count/list/architecture references from 13 to 14 where they describe operator-depth profiles. Add one concise #14 description without claiming empirical superiority over an external system.

- [ ] **Step 3: Commit docs only**

Commit message: `docs: publish confused deputy operator depth`.

### Task 6: Exact-head verification, provenance, and merge

**Files:**
- No additional code-tree changes.

**Interfaces:**
- Consumes: final candidate SHA.
- Produces: merged and post-merge verified `main`.

- [ ] **Step 1: Review changed-file scope**

Compare the feature branch to the original base. Require exactly the nine allowed paths from the spec. Reject any metadata, graph, pack, routing, benchmark, evaluator, or court authority drift.

- [ ] **Step 2: Freeze final exact-head SHA**

No further commit may be added after this point unless verification fails and the cycle restarts with a new SHA.

- [ ] **Step 3: Run exact-head CI**

Require 6/6 matrix plus all three core jobs SUCCESS on the exact final SHA.

- [ ] **Step 4: Update Draft PR provenance**

Record base SHA, spec commit, plan commit, test-first RED commit/run, behavioral GREEN SHA/run, final exact head/run, nine-file scope, safety boundary, and explicit no-authority-drift statement.

- [ ] **Step 5: Mark PR Ready and merge with expected-head guard**

Use the exact final SHA as `expected_head_sha`. Do not merge if the head moved.

- [ ] **Step 6: Verify merged `main` and post-merge CI**

Confirm `main` has the expected merge commit whose parents include the prior main and exact verified PR head. Then require the push-triggered workflow on merged `main` to pass 6/6 matrix, `benchmark-core`, `agent-eval-core`, and `superiority-court-core`.

- [ ] **Step 7: Claim completion only after fresh post-merge evidence**

Report profile #14 as closed only after all post-merge jobs are completed with `success`.