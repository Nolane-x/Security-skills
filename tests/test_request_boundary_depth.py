import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "server-side-request-boundary-analysis" / "SKILL.md"
RUNBOOK = (
    ROOT
    / "skills"
    / "server-side-request-boundary-analysis"
    / "references"
    / "operator-runbook.md"
)
SCENARIOS = (
    ROOT
    / "skills"
    / "server-side-request-boundary-analysis"
    / "references"
    / "operator-scenarios.json"
)


class RequestBoundaryDepthTests(unittest.TestCase):
    def test_skill_exposes_destination_decision_model(self):
        text = SKILL.read_text(encoding="utf-8")
        for section in (
            "## Destination decision model",
            "## Request-path reasoning discipline",
            "## Evidence ladder",
        ):
            self.assertIn(section, text)
        for concept in (
            "request provenance",
            "canonical destination",
            "resolution result",
            "redirect state",
            "policy checkpoint",
            "egress route",
            "final peer",
            "authority attachment",
            "counterfactual",
        ):
            self.assertIn(concept, text.lower())

    def test_runbook_requires_request_state_and_connection_binding(self):
        text = RUNBOOK.read_text(encoding="utf-8")
        for section in (
            "## Destination policy semantics",
            "## Request state machine",
            "## Resolution and connection binding",
            "## Counterfactual controls",
            "## Evidence ladder",
            "## Remediation proof",
        ):
            self.assertIn(section, text)

        for phrase in (
            "validation input",
            "canonical destination",
            "resolved address",
            "connection target",
            "final peer",
            "policy checkpoint",
            "authority attachment",
            "alternative explanation",
            "neighboring control",
        ):
            self.assertIn(phrase, text.lower())

    def test_scenarios_encode_request_state_reasoning(self):
        payload = json.loads(SCENARIOS.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 1)
        self.assertGreaterEqual(len(payload["scenarios"]), 3)
        for scenario in payload["scenarios"]:
            for field in (
                "request_state_trace",
                "policy_checkpoints",
                "false_positive_guard",
                "evidence_upgrade",
                "neighbor_regression",
            ):
                self.assertIn(field, scenario)
                self.assertIsInstance(scenario[field], str)
                self.assertGreaterEqual(len(scenario[field].strip()), 40)


if __name__ == "__main__":
    unittest.main()
