import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "web-routing-and-middleware-analysis" / "SKILL.md"
RUNBOOK = (
    ROOT
    / "skills"
    / "web-routing-and-middleware-analysis"
    / "references"
    / "operator-runbook.md"
)
SCENARIOS = (
    ROOT
    / "skills"
    / "web-routing-and-middleware-analysis"
    / "references"
    / "operator-scenarios.json"
)


class WebRoutingMiddlewareDepthTests(unittest.TestCase):
    def test_skill_exposes_request_policy_invariant_model(self):
        text = SKILL.read_text(encoding="utf-8")
        for section in (
            "## Request-policy invariant model",
            "## Interpretation and policy discipline",
            "## Evidence ladder",
        ):
            self.assertIn(section, text)

        for concept in (
            "semantic-equivalence class",
            "interpretation snapshot",
            "policy attachment point",
            "identity binding",
            "mutation provenance",
            "middleware partial order",
            "handler reachability",
            "fallback route",
            "error route",
            "counterfactual",
        ):
            self.assertIn(concept, text.lower())

    def test_runbook_requires_hopwise_interpretation_and_causal_policy_proof(self):
        text = RUNBOOK.read_text(encoding="utf-8")
        for section in (
            "## Request-policy invariant semantics",
            "## Hopwise interpretation model",
            "## Policy attachment and identity timing",
            "## Counterfactual controls",
            "## Evidence ladder",
            "## Remediation proof",
        ):
            self.assertIn(section, text)

        for phrase in (
            "semantic-equivalence class",
            "interpretation snapshot",
            "rewrite provenance",
            "mount provenance",
            "middleware partial order",
            "identity binding",
            "tenant binding",
            "method semantics",
            "host semantics",
            "proxy trust",
            "fallback route",
            "error route",
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
