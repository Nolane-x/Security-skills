import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "container-isolation-review" / "SKILL.md"
RUNBOOK = (
    ROOT
    / "skills"
    / "container-isolation-review"
    / "references"
    / "operator-runbook.md"
)
SCENARIOS = (
    ROOT
    / "skills"
    / "container-isolation-review"
    / "references"
    / "operator-scenarios.json"
)


class ContainerIsolationDepthTests(unittest.TestCase):
    def test_skill_exposes_isolation_guarantee_model(self):
        text = SKILL.read_text(encoding="utf-8")
        for section in (
            "## Isolation guarantee model",
            "## Runtime-state reasoning discipline",
            "## Evidence ladder",
        ):
            self.assertIn(section, text)

        for concept in (
            "threat principal",
            "isolation objective",
            "requested state",
            "admitted state",
            "effective runtime state",
            "namespace ownership",
            "privilege envelope",
            "syscall mediation",
            "host interface",
            "credential exposure",
            "network boundary",
            "control-plane drift",
            "counterfactual",
        ):
            self.assertIn(concept, text.lower())

    def test_runbook_requires_runtime_state_and_host_binding(self):
        text = RUNBOOK.read_text(encoding="utf-8")
        for section in (
            "## Isolation guarantee semantics",
            "## Runtime state model",
            "## Kernel and host-interface binding",
            "## Counterfactual controls",
            "## Evidence ladder",
            "## Remediation proof",
        ):
            self.assertIn(section, text)

        for phrase in (
            "requested state",
            "admitted state",
            "effective runtime state",
            "namespace ownership",
            "privilege envelope",
            "syscall mediation",
            "mount propagation",
            "device exposure",
            "runtime socket",
            "credential exposure",
            "network boundary",
            "alternative explanation",
            "neighboring control",
        ):
            self.assertIn(phrase, text.lower())

    def test_scenarios_encode_isolation_state_reasoning(self):
        payload = json.loads(SCENARIOS.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 1)
        self.assertGreaterEqual(len(payload["scenarios"]), 3)
        for scenario in payload["scenarios"]:
            for field in (
                "isolation_state_trace",
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
