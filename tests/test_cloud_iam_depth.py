import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "cloud-iam-path-analysis" / "SKILL.md"
RUNBOOK = (
    ROOT
    / "skills"
    / "cloud-iam-path-analysis"
    / "references"
    / "operator-runbook.md"
)
SCENARIOS = (
    ROOT
    / "skills"
    / "cloud-iam-path-analysis"
    / "references"
    / "operator-scenarios.json"
)


class CloudIamDepthTests(unittest.TestCase):
    def test_skill_exposes_effective_authorization_model(self):
        text = SKILL.read_text(encoding="utf-8")
        for section in (
            "## Effective authorization model",
            "## Path reasoning discipline",
            "## Evidence ladder",
        ):
            self.assertIn(section, text)
        for concept in (
            "policy source",
            "explicit deny",
            "maximum permission",
            "trust condition",
            "session context",
            "edge precondition",
            "effective decision",
            "counterfactual",
        ):
            self.assertIn(concept, text.lower())

    def test_runbook_requires_path_causality_and_composition(self):
        text = RUNBOOK.read_text(encoding="utf-8")
        for section in (
            "## Effective permission semantics",
            "## Edge proof model",
            "## Path causality",
            "## Counterfactual controls",
            "## Evidence ladder",
            "## Remediation proof",
        ):
            self.assertIn(section, text)

        for phrase in (
            "edge precondition",
            "effective decision",
            "explicit deny",
            "maximum-permission",
            "session context",
            "alternative explanation",
            "path-breaking control",
            "neighboring path",
        ):
            self.assertIn(phrase, text.lower())

    def test_scenarios_encode_edge_and_path_reasoning(self):
        payload = json.loads(SCENARIOS.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 1)
        self.assertGreaterEqual(len(payload["scenarios"]), 3)
        for scenario in payload["scenarios"]:
            for field in (
                "edge_preconditions",
                "path_causality",
                "false_positive_guard",
                "evidence_upgrade",
                "neighbor_regression",
            ):
                self.assertIn(field, scenario)
                self.assertIsInstance(scenario[field], str)
                self.assertGreaterEqual(len(scenario[field].strip()), 40)


if __name__ == "__main__":
    unittest.main()
