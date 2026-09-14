import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "ai-agent-security-assessment" / "SKILL.md"
RUNBOOK = (
    ROOT
    / "skills"
    / "ai-agent-security-assessment"
    / "references"
    / "operator-runbook.md"
)
SCENARIOS = (
    ROOT
    / "skills"
    / "ai-agent-security-assessment"
    / "references"
    / "operator-scenarios.json"
)


class AiAgentSecurityDepthTests(unittest.TestCase):
    def test_skill_exposes_causal_agent_security_model(self):
        text = SKILL.read_text(encoding="utf-8")
        for section in (
            "## Causal security state model",
            "## Authority-capability model",
            "## Provenance continuity",
            "## Evidence ladder",
            "## Evidence ceiling",
            "## Counterfactual discipline",
        ):
            self.assertIn(section, text)

        for concept in (
            "source -> provenance -> interpretation -> proposal -> authority -> policy -> confirmation -> execution -> effect -> persistence",
            "initiating principal",
            "credential authority",
            "effective authority",
            "compound authority",
            "normalized arguments",
            "policy decision",
            "confirmation state",
            "transient effect",
            "delegated authority",
            "counterfactual",
            "evidence ceiling",
        ):
            self.assertIn(concept, text.lower())

    def test_runbook_requires_transition_level_agent_reasoning(self):
        text = RUNBOOK.read_text(encoding="utf-8")
        for section in (
            "## Causal decision trace",
            "## Authority-capability matrix",
            "## Provenance continuity",
            "## Persistence and delegation",
            "## Counterfactual boundary proof",
            "## Evidence ceiling",
            "## Remediation proof",
        ):
            self.assertIn(section, text)

        for phrase in (
            "source provenance",
            "normalized arguments",
            "effective authority",
            "compound authority",
            "re-authorization",
            "context compression",
            "persistent write",
            "later retrieval",
            "alternative explanation",
            "neighboring allowed control",
            "evidence ceiling",
        ):
            self.assertIn(phrase, text.lower())

    def test_scenarios_encode_causal_agent_security_reasoning(self):
        payload = json.loads(SCENARIOS.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 1)
        self.assertEqual(len(payload["scenarios"]), 3)
        for scenario in payload["scenarios"]:
            for field in (
                "provenance_trace",
                "authority_capability_profile",
                "decision_effect_trace",
                "persistence_trace",
                "delegation_trace",
                "counterfactual_control",
                "alternative_explanation",
                "evidence_ceiling",
                "neighbor_regression",
            ):
                self.assertIn(field, scenario)
                self.assertIsInstance(scenario[field], str)
                self.assertGreaterEqual(len(scenario[field].strip()), 50)


if __name__ == "__main__":
    unittest.main()
