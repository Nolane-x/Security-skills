import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "driver-ioctl-surface-analysis" / "SKILL.md"
RUNBOOK = (
    ROOT
    / "skills"
    / "driver-ioctl-surface-analysis"
    / "references"
    / "operator-runbook.md"
)
SCENARIOS = (
    ROOT
    / "skills"
    / "driver-ioctl-surface-analysis"
    / "references"
    / "operator-scenarios.json"
)


class DriverIoctlDepthTests(unittest.TestCase):
    def test_skill_exposes_privileged_request_contract_model(self):
        text = SKILL.read_text(encoding="utf-8")
        for section in (
            "## Privileged request-contract model",
            "## Contract interpretation discipline",
            "## Evidence ladder",
        ):
            self.assertIn(section, text)

        for concept in (
            "caller principal",
            "open/handle gate",
            "command selector",
            "transport provenance",
            "schema version",
            "normalized length",
            "object identity",
            "ownership binding",
            "state prerequisite",
            "asynchronous ownership",
            "completion authority",
            "privileged effect",
            "counterfactual",
        ):
            self.assertIn(concept, text.lower())

    def test_runbook_requires_validation_consumption_and_lifecycle_binding(self):
        text = RUNBOOK.read_text(encoding="utf-8")
        for section in (
            "## Privileged request-contract semantics",
            "## Request interpretation model",
            "## Validation-to-consumption binding",
            "## Object identity and lifecycle binding",
            "## Counterfactual controls",
            "## Evidence ladder",
            "## Remediation proof",
        ):
            self.assertIn(section, text)

        for phrase in (
            "open/handle gate",
            "transport provenance",
            "schema/version",
            "normalized length",
            "validation snapshot",
            "consumption snapshot",
            "object identity",
            "ownership binding",
            "state prerequisite",
            "asynchronous ownership",
            "completion authority",
            "alternative explanation",
            "neighboring control",
        ):
            self.assertIn(phrase, text.lower())

    def test_scenarios_encode_request_contract_reasoning(self):
        payload = json.loads(SCENARIOS.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 1)
        self.assertGreaterEqual(len(payload["scenarios"]), 3)
        for scenario in payload["scenarios"]:
            for field in (
                "contract_state_trace",
                "violated_invariant",
                "false_positive_guard",
                "evidence_upgrade",
                "neighbor_regression",
            ):
                self.assertIn(field, scenario)
                self.assertIsInstance(scenario[field], str)
                self.assertGreaterEqual(len(scenario[field].strip()), 40)


if __name__ == "__main__":
    unittest.main()
