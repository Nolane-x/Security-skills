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
