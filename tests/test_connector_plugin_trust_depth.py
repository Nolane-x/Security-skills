import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "connector-plugin-trust-analysis" / "SKILL.md"
RUNBOOK = ROOT / "skills" / "connector-plugin-trust-analysis" / "references" / "operator-runbook.md"
CASES = ROOT / "skills" / "connector-plugin-trust-analysis" / "references" / "operator-review-cases.json"
PROFILES = ROOT / "operator-depth" / "profiles.json"


class ConnectorPluginTrustDepthTests(unittest.TestCase):
    def test_skill_exposes_connector_policy_and_provenance_model(self):
        text = SKILL.read_text(encoding="utf-8")
        for section in (
            "## Integration lifecycle and provenance model",
            "## Effective permission model",
            "## Schema and argument contract",
            "## Delegated access and response binding",
            "## Cross-connector composition",
            "## Lifecycle and revocation model",
            "## Connector evidence ladder",
            "## Counterfactual proof",
            "## Alternative explanations",
            "## Evidence ceiling",
        ):
            self.assertIn(section, text)

        lower = text.lower()
        for concept in (
            "integration identity -> provenance -> permission grant -> delegated scope -> tool/schema contract -> invocation principal -> policy gate -> observable bounded effect -> result provenance -> revocation state",
            "effective permission",
            "delegated scope",
            "dynamic schema",
            "response identity",
            "composition boundary",
            "grant generation",
            "update generation",
            "revocation generation",
            "c0",
            "c1",
            "c2",
            "c3",
            "c4",
            "c5",
            "counterfactual",
            "evidence ceiling",
        ):
            self.assertIn(concept, lower)

    def test_runbook_requires_transition_level_connector_reasoning(self):
        self.assertTrue(RUNBOOK.is_file(), "connector operator runbook must exist before depth can pass")
        text = RUNBOOK.read_text(encoding="utf-8")
        for section in (
            "## Attack surface",
            "## Hypothesis matrix",
            "## Integration lifecycle and provenance",
            "## Effective permission trace",
            "## Schema and argument trace",
            "## Delegated access and response binding",
            "## Cross-connector composition",
            "## Lifecycle and revocation trace",
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
            "integration identity",
            "publisher provenance",
            "permission grant",
            "effective permission",
            "delegated access",
            "schema drift",
            "response identity",
            "composition boundary",
            "revocation generation",
            "bounded convergence window",
            "alternative explanation",
            "evidence ceiling",
        ):
            self.assertIn(phrase, lower)

    def test_review_cases_encode_connector_lifecycle_reasoning(self):
        self.assertTrue(CASES.is_file(), "connector review-case matrix must exist before depth can pass")
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
                "integration_provenance",
                "permission_profile",
                "schema_argument_trace",
                "delegated_response_binding",
                "composition_trace",
                "lifecycle_state",
                "counterfactual_control",
                "alternative_explanation",
                "evidence_level",
                "evidence_ceiling",
            ):
                self.assertIn(field, scenario)
                self.assertIsInstance(scenario[field], str)
                self.assertGreaterEqual(len(scenario[field].strip()), 40)

    def test_skill_is_registered_as_eleventh_operator_depth_profile(self):
        payload = json.loads(PROFILES.read_text(encoding="utf-8"))
        profiles = payload["profiles"]
        self.assertGreaterEqual(len(profiles), 11)
        matching = [p for p in profiles if p["skill"] == "connector-plugin-trust-analysis"]
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
