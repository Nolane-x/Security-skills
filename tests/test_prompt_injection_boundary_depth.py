import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "prompt-injection-boundary-analysis" / "SKILL.md"
RUNBOOK = (
    ROOT
    / "skills"
    / "prompt-injection-boundary-analysis"
    / "references"
    / "operator-runbook.md"
)
SCENARIOS = (
    ROOT
    / "skills"
    / "prompt-injection-boundary-analysis"
    / "references"
    / "operator-scenarios.json"
)
PROFILES = ROOT / "operator-depth" / "profiles.json"


class PromptInjectionBoundaryDepthTests(unittest.TestCase):
    def test_skill_exposes_authority_provenance_and_effect_model(self):
        text = SKILL.read_text(encoding="utf-8")
        for section in (
            "## Instruction authority model",
            "## Transformation provenance model",
            "## Decision and effect ladder",
            "## Counterfactual proof",
            "## Alternative explanations",
            "## Evidence ceiling",
        ):
            self.assertIn(section, text)

        lower = text.lower()
        for concept in (
            "source -> provenance label -> transform -> effective context -> interpreted authority -> decision -> policy gate -> proposed capability -> accepted capability -> bounded effect",
            "intended authority",
            "protected invariant",
            "authority actually granted",
            "retrieval",
            "summarization",
            "memory",
            "context compaction",
            "p0",
            "p1",
            "p2",
            "p3",
            "p4",
            "p5",
            "counterfactual",
            "evidence ceiling",
        ):
            self.assertIn(concept, lower)

    def test_runbook_requires_transition_level_prompt_injection_reasoning(self):
        self.assertTrue(
            RUNBOOK.is_file(),
            "prompt-injection operator runbook must exist before depth can pass",
        )
        text = RUNBOOK.read_text(encoding="utf-8")
        for section in (
            "## Attack surface",
            "## Hypothesis matrix",
            "## Instruction lineage trace",
            "## Authority conflict analysis",
            "## Transformation boundary analysis",
            "## Decision and effect trace",
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
            "source identity",
            "intended authority",
            "effective context",
            "protected invariant",
            "provenance continuity",
            "authority reinterpretation",
            "deterministic policy",
            "bounded effect",
            "alternative explanation",
            "neighboring allowed control",
            "evidence ceiling",
        ):
            self.assertIn(phrase, lower)

    def test_scenarios_encode_causal_prompt_injection_reasoning(self):
        self.assertTrue(
            SCENARIOS.is_file(),
            "prompt-injection scenario matrix must exist before depth can pass",
        )
        payload = json.loads(SCENARIOS.read_text(encoding="utf-8"))
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
                "source_class",
                "intended_authority",
                "transformation_trace",
                "authority_conflict",
                "protected_invariant",
                "decision_trace",
                "effect_ceiling",
                "counterfactual_control",
                "alternative_explanation",
                "evidence_ceiling",
            ):
                self.assertIn(field, scenario)
                self.assertIsInstance(scenario[field], str)
                self.assertGreaterEqual(len(scenario[field].strip()), 40)

    def test_skill_is_registered_as_ninth_operator_depth_profile(self):
        payload = json.loads(PROFILES.read_text(encoding="utf-8"))
        profiles = payload["profiles"]
        self.assertEqual(len(profiles), 9)
        matching = [
            profile
            for profile in profiles
            if profile["skill"] == "prompt-injection-boundary-analysis"
        ]
        self.assertEqual(len(matching), 1)
        profile = matching[0]
        self.assertEqual(profile["runbook"], "references/operator-runbook.md")
        self.assertEqual(profile["scenario_matrix"], "references/operator-scenarios.json")
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
