import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "canonicalization-and-namespace-analysis" / "SKILL.md"
RUNBOOK = ROOT / "skills" / "canonicalization-and-namespace-analysis" / "references" / "operator-runbook.md"
CASES = ROOT / "skills" / "canonicalization-and-namespace-analysis" / "references" / "operator-review-cases.json"
PROFILES = ROOT / "operator-depth" / "profiles.json"


class CanonicalizationNamespaceDepthTests(unittest.TestCase):
    def test_skill_exposes_representation_to_identity_model(self):
        text = SKILL.read_text(encoding="utf-8")
        for section in (
            "## Representation and identity graph",
            "## Transformation ordering and non-commutativity",
            "## Normalization idempotence",
            "## Equivalence, collision, ambiguity, and aliasing",
            "## Policy-key to resolved-identity invariant",
            "## Namespace-root and authority binding",
            "## Boundary-preserving normalization",
            "## Name-to-object transition",
            "## Mutable namespace and identity drift",
            "## Namespace evidence ladder",
            "## Counterfactual proof",
            "## Alternative explanations",
            "## Evidence ceiling",
        ):
            self.assertIn(section, text)

        lower = text.lower()
        for concept in (
            "raw input -> parsed representation -> decoded representation -> normalized representation -> policy key -> resolver input -> resolved identity -> opened handle/object identity",
            "non-commutativity",
            "idempotence",
            "resolver equivalence",
            "policy equivalence",
            "namespace root",
            "namespace generation",
            "name-to-object",
            "n0",
            "n1",
            "n2",
            "n3",
            "n4",
            "n5",
            "counterfactual",
            "evidence ceiling",
        ):
            self.assertIn(concept, lower)

    def test_runbook_requires_transition_level_identity_reasoning(self):
        self.assertTrue(RUNBOOK.is_file(), "canonicalization operator runbook must exist before depth can pass")
        text = RUNBOOK.read_text(encoding="utf-8")
        for section in (
            "## Attack surface",
            "## Hypothesis matrix",
            "## Representation and identity trace",
            "## Transformation-order trace",
            "## Equivalence and ambiguity trace",
            "## Policy-key and resolver binding",
            "## Namespace-root binding",
            "## Name-to-object and generation trace",
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
            "representation chain",
            "transform order",
            "normalization idempotence",
            "resolver equivalence",
            "policy key",
            "resolved identity",
            "namespace root",
            "object binding",
            "namespace generation",
            "counterfactual",
            "alternative explanation",
            "evidence ceiling",
        ):
            self.assertIn(phrase, lower)

    def test_review_cases_encode_representation_identity_reasoning(self):
        self.assertTrue(CASES.is_file(), "canonicalization review-case matrix must exist before depth can pass")
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
                "representation_chain",
                "transform_order",
                "normalization_idempotence",
                "equivalence_class",
                "policy_key",
                "resolver_input",
                "resolved_identity",
                "namespace_root",
                "object_binding",
                "namespace_generation",
                "counterfactual_control",
                "alternative_explanation",
                "evidence_level",
                "evidence_ceiling",
            ):
                self.assertIn(field, scenario)
                self.assertIsInstance(scenario[field], str)
                self.assertGreaterEqual(len(scenario[field].strip()), 40)

    def test_skill_is_registered_as_thirteenth_operator_depth_profile(self):
        payload = json.loads(PROFILES.read_text(encoding="utf-8"))
        profiles = payload["profiles"]
        self.assertGreaterEqual(len(profiles), 13)
        matching = [p for p in profiles if p["skill"] == "canonicalization-and-namespace-analysis"]
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
