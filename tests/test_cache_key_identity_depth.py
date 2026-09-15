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
