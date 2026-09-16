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
