# Wave 10 Multi-Tenant Data Isolation Depth Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add Wave 10 operator-depth profile #17 by turning `multi-tenant-data-isolation-analysis` into a causal tenant-isolation proof method with deterministic synthetic review artifacts, M0-M5 evidence ceilings, async-context propagation reasoning, namespace-to-object binding, and lifecycle/migration-generation controls.

**Architecture:** Keep the existing canonical skill identity and routing metadata unchanged. Add a tenant-isolation causal model, operator runbook, deterministic synthetic review cases, one additive operator-depth registry entry, and one dedicated contract test; synchronize public docs only after behavioral GREEN. Preserve graph, packs, routing, benchmark, agent-eval, and superiority-court authority unchanged.

**Tech Stack:** Markdown Agent Skills, JSON registry/review fixtures, Python `unittest`, GitHub Actions matrix validation.

**Spec:** `docs/superpowers/specs/2026-09-16-wave10-multi-tenant-isolation-depth-design.md`

## Global Constraints

- Base is `main@4d2c6be108303a538f0f62cd8f45d8dca09fb90c`.
- Only the nine paths enumerated in the spec may change.
- Do not modify `skills/multi-tenant-data-isolation-analysis/skill.meta.json`, graph edges, packs, routing domains, benchmark fixtures/thresholds, agent-eval authority, superiority-court authority, or workflow semantics.
- Dynamic validation is restricted to synthetic tenants, synthetic principals, synthetic objects, inert markers, deterministic mock/read-only services, policy simulators, or reversible owner-controlled state.
- No real customer data, production tenant identifiers, production support/admin paths, real credentials, third-party accounts, destructive actions, persistence, evasion, malware, or unauthorized targets.
- Registry schema remains version `2`.
- Dedicated profile test uses additive `>= 17`, never an exact global profile count.
- README and `docs/operator-depth-contract.md` are changed only after behavioral GREEN.
- Do not claim empirical superiority over Claude-Red or any external system without an actual contestant run through the repository superiority court.

---

### Task 1: Lock the dedicated RED contract

**Files:**
- Create: `tests/test_multi_tenant_data_isolation_depth.py`

**Interfaces:**
- Consumes: current canonical `skills/multi-tenant-data-isolation-analysis/SKILL.md` and `operator-depth/profiles.json`.
- Produces: four dedicated assertions that fail until causal tenant-isolation skill depth, runbook, review cases, and profile #17 registration exist.

- [ ] **Step 1: Create the dedicated test first**

Use this exact structure:

```python
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "multi-tenant-data-isolation-analysis" / "SKILL.md"
RUNBOOK = ROOT / "skills" / "multi-tenant-data-isolation-analysis" / "references" / "operator-runbook.md"
CASES = ROOT / "skills" / "multi-tenant-data-isolation-analysis" / "references" / "operator-review-cases.json"
PROFILES = ROOT / "operator-depth" / "profiles.json"


class MultiTenantDataIsolationDepthTests(unittest.TestCase):
    def test_skill_exposes_causal_tenant_isolation_model(self):
        text = SKILL.read_text(encoding="utf-8")
        for section in (
            "## Causal tenant-isolation model",
            "## Principal and tenant identity",
            "## Membership and role binding",
            "## Representation and propagation",
            "## Policy, filter, and namespace decisions",
            "## Resolved object and result identity",
            "## Async and job context",
            "## Lifecycle and migration generation",
            "## Administrative and ambient authority",
            "## Tenant-isolation evidence ladder",
            "## Counterfactual proof",
            "## Alternative explanations",
            "## Evidence ceiling",
        ):
            self.assertIn(section, text)

        lower = text.lower()
        for concept in (
            "request origin -> authenticated principal -> claimed tenant -> canonical tenant identity -> membership/role binding -> tenant-context generation -> representation/propagation hop -> policy/filter decision -> namespace/query/cache/job/index key -> resolved object/result identity -> bounded read/write/list effect -> receipt/result binding -> lifecycle/migration generation",
            "authenticated principal != tenant membership",
            "claimed tenant != canonical tenant identity",
            "tenant hint/header != canonical tenant identity",
            "membership/role binding != ambient admin/support authority",
            "filter present != tenant-correct result",
            "namespace/key != resolved object identity",
            "same logical tenant != same lifecycle/migration generation",
            "queued job tenant context != execution-time ambient tenant context",
            "caller authority != admin/support ambient authority",
            "m0",
            "m1",
            "m2",
            "m3",
            "m4",
            "m5",
            "counterfactual",
            "evidence ceiling",
        ):
            self.assertIn(concept, lower)

    def test_runbook_requires_transition_level_tenant_reasoning(self):
        self.assertTrue(RUNBOOK.is_file(), "multi-tenant operator runbook must exist before depth can pass")
        text = RUNBOOK.read_text(encoding="utf-8")
        for section in (
            "## Attack surface",
            "## Hypothesis matrix",
            "## Principal and tenant-identity trace",
            "## Membership and role-binding trace",
            "## Tenant-context generation trace",
            "## Representation and propagation trace",
            "## Policy and filter-decision trace",
            "## Namespace and selector trace",
            "## Resolved object/result identity",
            "## Async/job context trace",
            "## Lifecycle and migration-generation trace",
            "## Administrative and ambient-authority trace",
            "## Result and receipt binding",
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
            "canonical tenant identity",
            "membership/role binding",
            "tenant-context generation",
            "policy/filter decision",
            "namespace selector",
            "resolved object/result identity",
            "async context",
            "migration generation",
            "ambient authority",
            "counterfactual",
            "alternative explanation",
            "evidence ceiling",
        ):
            self.assertIn(phrase, lower)

    def test_review_cases_encode_tenant_isolation_reasoning(self):
        self.assertTrue(CASES.is_file(), "multi-tenant review-case matrix must exist before depth can pass")
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
            "request_origin",
            "authenticated_principal",
            "claimed_tenant",
            "canonical_tenant_identity",
            "membership_role_binding",
            "tenant_context_generation",
            "representation_propagation_hop",
            "policy_filter_decision",
            "namespace_selector",
            "resolved_object_result_identity",
            "bounded_effect",
            "receipt_result_binding",
            "lifecycle_migration_generation",
            "async_context_control",
            "ambient_authority_control",
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

    def test_skill_is_registered_as_seventeenth_operator_depth_profile(self):
        payload = json.loads(PROFILES.read_text(encoding="utf-8"))
        profiles = payload["profiles"]
        self.assertGreaterEqual(len(profiles), 17)
        matching = [p for p in profiles if p["skill"] == "multi-tenant-data-isolation-analysis"]
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
test: lock multi-tenant isolation depth contract
```

- [ ] **Step 3: Open a Draft PR on the test-first SHA and run the full repository workflow**

Expected dedicated failures:

- missing causal tenant-isolation sections/concepts in the current skill;
- missing `references/operator-runbook.md`;
- missing `references/operator-review-cases.json`;
- no `multi-tenant-data-isolation-analysis` registry entry and fewer than 17 profiles.

The RED run is valid only if canonical-skill validation, current 16-profile operator-depth validation, graph/generated-index checks, benchmark validation, portability benchmark, and agent-eval portability smoke remain healthy before the dedicated contract fails. Unexpected unittest errors or unrelated failures must be debugged rather than accepted.

---

### Task 2: Implement the causal tenant-isolation depth artifacts

**Files:**
- Modify: `skills/multi-tenant-data-isolation-analysis/SKILL.md`
- Create: `skills/multi-tenant-data-isolation-analysis/references/operator-runbook.md`
- Create: `skills/multi-tenant-data-isolation-analysis/references/operator-review-cases.json`
- Modify: `operator-depth/profiles.json`
- Test: `tests/test_multi_tenant_data_isolation_depth.py`

**Interfaces:**
- Consumes: the exact RED contract from Task 1 and causal model in the design spec.
- Produces: canonical skill depth, operator runbook, deterministic review cases, and additive profile registration #17.

- [ ] **Step 1: Replace the short checklist-oriented skill body while preserving frontmatter identity**

The resulting `SKILL.md` must contain these exact headings:

```text
## When to use
## Preconditions
## Causal tenant-isolation model
## Principal and tenant identity
## Membership and role binding
## Representation and propagation
## Policy, filter, and namespace decisions
## Resolved object and result identity
## Async and job context
## Lifecycle and migration generation
## Administrative and ambient authority
## Workflow
## Tenant-isolation evidence ladder
## Counterfactual proof
## Alternative explanations
## Evidence contract
## Evidence ceiling
## Stop conditions
## Output
```

It must include the exact causal chain and distinctions frozen by the test, define M0-M5 as in the spec, route cache-specific issues to cache-key reasoning, route generic permission failures to authorization-boundary reasoning, require resolved object/result identity proof rather than mere filter presence, and keep all dynamic validation synthetic/owned/read-only/reversible.

- [ ] **Step 2: Create the operator runbook**

`operator-runbook.md` must include every exact heading required by Task 1. Each trace must request both observed value and evidence source. Controlled validation must prescribe one-dimension synthetic controls for principal, claimed/canonical tenant identity, membership/role, tenant-context generation, namespace selector, async propagation, lifecycle generation, ambient authority, resolved result identity, and remediation regression. It must explicitly prohibit real-customer access and production support/admin testing.

- [ ] **Step 3: Create deterministic review cases**

Create JSON version `1` with exactly three initial scenarios named:

```text
tenant-context-binding
async-context-propagation
namespace-to-resolved-object-binding
```

Every required field in Task 1 must be a substantive string of at least 40 characters. Use two or more synthetic tenants, fake principals/roles, identical synthetic object names or IDs where useful, inert result markers, deterministic mock queues/indexes/storage, bounded policy decisions, and reversible owner-controlled effects. Each scenario must include a safe oracle, positive/negative controls, stop condition, remediation oracle, async/ambient controls, counterfactual, alternative explanation, evidence level, and evidence ceiling.

- [ ] **Step 4: Register profile #17 additively**

Add exactly one entry to `operator-depth/profiles.json`:

```json
{
  "skill": "multi-tenant-data-isolation-analysis",
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

Preserve schema version `2` and every existing profile unchanged.

- [ ] **Step 5: Run the dedicated test and operator-depth validator**

Expected:

```text
python -m unittest tests.test_multi_tenant_data_isolation_depth -v
# 4 tests, all PASS

python scripts/validate_operator_depth.py
# PASS with >= 17 profiles and no schema/path errors
```

- [ ] **Step 6: Commit the behavioral implementation**

Commit message:

```text
feat: deepen multi-tenant isolation reasoning
```

- [ ] **Step 7: Run full GitHub Actions and require behavioral GREEN**

All six Ubuntu/macOS/Windows × Python 3.11/3.13 matrix jobs plus `benchmark-core`, `agent-eval-core`, and `superiority-court-core` must succeed. Public docs remain untouched until this full GREEN run is recorded on the behavioral SHA.

---

### Task 3: Synchronize public documentation after behavioral GREEN

**Files:**
- Modify: `README.md`
- Modify: `docs/operator-depth-contract.md`

**Interfaces:**
- Consumes: verified profile #17 behavioral implementation from Task 2.
- Produces: public snapshot and operator-depth history synchronized to 17 profiles without changing behavior.

- [ ] **Step 1: Update README counts and Wave 10 narrative**

Change every current operator-depth total from 16 to 17 where it describes the current baseline. Add `multi-tenant-data-isolation-analysis` as the seventeenth profile and summarize its contribution as canonical tenant identity, membership/role binding, tenant-context generations, propagation traces, policy/filter and namespace decisions, resolved object/result identity, async context, lifecycle/migration generations, ambient-authority controls, deterministic audit-only review cases, counterfactual controls, and M0-M5 evidence ceilings.

- [ ] **Step 2: Update `docs/operator-depth-contract.md`**

Append `multi-tenant-data-isolation-analysis` as the seventeenth Wave 10 profile and update the current registry count to 17. Preserve Wave 8 history and all descriptions for profiles #9-#16 unchanged.

- [ ] **Step 3: Verify the docs-only delta**

Compare behavioral GREEN SHA to docs head and require exactly:

```text
README.md
docs/operator-depth-contract.md
```

No skill, test, registry, workflow, benchmark, agent-eval, or superiority-court artifact may change after behavioral GREEN.

- [ ] **Step 4: Commit docs**

Commit message:

```text
docs: publish multi-tenant isolation depth
```

---

### Task 4: Exact-head verification and guarded merge

**Files:**
- No new behavioral files.
- PR metadata/provenance only after the final candidate SHA is fixed.

**Interfaces:**
- Consumes: final candidate containing Tasks 1-3 only.
- Produces: exact-head CI evidence, reviewable PR provenance, and guarded merge.

- [ ] **Step 1: Update Draft PR provenance**

PR body must record base SHA, design/plan commits, test-first SHA, clean RED run, behavioral GREEN SHA/run, final candidate SHA, exact nine-file scope, unchanged authority surfaces, and safety boundary. Explicitly state that no empirical superiority over external systems is claimed.

- [ ] **Step 2: Verify exact changed-file scope**

Require exactly the nine paths in the spec and no others.

- [ ] **Step 3: Require exact-head full CI GREEN**

On the final candidate SHA, require all six matrix jobs plus `benchmark-core`, `agent-eval-core`, and `superiority-court-core` to complete successfully. If any job fails, inspect steps/logs and debug the root cause before changing the branch.

- [ ] **Step 4: Mark Ready only after exact-head GREEN**

Re-read PR head/base immediately before transition. Head must equal the exact verified candidate and base must remain intended `main` lineage.

- [ ] **Step 5: Merge with expected-head SHA guard**

Use the final candidate SHA as `expected_head_sha`. Abort rather than merge if GitHub reports drift.

---

### Task 5: Post-merge verification and closure provenance

**Files:**
- No repository file changes after merge.
- PR conversation comment for closure provenance only.

**Interfaces:**
- Consumes: merge SHA returned by guarded merge.
- Produces: post-merge evidence proving `main` contains the intended tree and remains GREEN.

- [ ] **Step 1: Verify merge lineage**

Require `main` to point at the merge commit and verify its two parents are the previous main base and exact final candidate head.

- [ ] **Step 2: Find the push-triggered workflow for the merge SHA**

Use the GitHub Actions runs endpoint filtered by `head_sha=<merge-sha>&event=push` and require exactly the intended `main` validation run.

- [ ] **Step 3: Require post-merge full GREEN**

Require all six matrix jobs plus `benchmark-core`, `agent-eval-core`, and `superiority-court-core` to complete successfully on the merge SHA.

- [ ] **Step 4: Verify public closure state on the merge SHA**

Read `operator-depth/profiles.json` and require version `2`, at least 17 profiles, and exactly one `multi-tenant-data-isolation-analysis` entry. Read README and `docs/operator-depth-contract.md` and require both to state 17 profiles and identify `multi-tenant-data-isolation-analysis` as the seventeenth profile.

- [ ] **Step 5: Record closure provenance**

Add a PR conversation comment containing final candidate SHA, exact-head run, merge SHA, post-merge push run, 9-file scope, registry/public-doc verification, and the continued no-superiority-claim caveat.
