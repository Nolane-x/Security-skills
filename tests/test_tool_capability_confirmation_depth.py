import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "tool-capability-and-confirmation-analysis" / "SKILL.md"
RUNBOOK = ROOT / "skills" / "tool-capability-and-confirmation-analysis" / "references" / "operator-runbook.md"
CASES = ROOT / "skills" / "tool-capability-and-confirmation-analysis" / "references" / "operator-review-cases.json"
PROFILES = ROOT / "operator-depth" / "profiles.json"


class ToolCapabilityConfirmationDepthTests(unittest.TestCase):
    def test_skill_exposes_action_binding_and_confirmation_model(self):
        text = SKILL.read_text(encoding="utf-8")
        for section in (
            "## Action-binding causal model",
            "## Intent and capability model",
            "## Argument normalization and binding",
            "## Effective authority model",
            "## Confirmation tuple",
            "## Execution binding and state drift",
            "## Transaction, retry, and idempotency model",
            "## Post-action verification",
            "## Tool evidence ladder",
            "## Counterfactual proof",
            "## Alternative explanations",
            "## Evidence ceiling",
        ):
            self.assertIn(section, text)

        lower = text.lower()
        for concept in (
            "request intent -> capability proposal -> normalized arguments -> effective authority -> policy decision -> confirmation snapshot -> execution binding -> observable bounded effect -> receipt/state -> retry/rollback state",
            "confirmation tuple",
            "effective authority",
            "read-only",
            "write/effect",
            "policy generation",
            "confirmation generation",
            "idempotency",
            "post-action",
            "proposal != accepted execution != receipt != durable final state",
            "t0",
            "t1",
            "t2",
            "t3",
            "t4",
            "t5",
            "counterfactual",
            "evidence ceiling",
        ):
            self.assertIn(concept, lower)

    def test_runbook_requires_transition_level_tool_reasoning(self):
        self.assertTrue(RUNBOOK.is_file(), "tool confirmation operator runbook must exist before depth can pass")
        text = RUNBOOK.read_text(encoding="utf-8")
        for section in (
            "## Attack surface",
            "## Hypothesis matrix",
            "## Intent and capability binding",
            "## Argument normalization trace",
            "## Effective authority trace",
            "## Confirmation tuple trace",
            "## Execution binding and state drift",
            "## Transaction, retry, and idempotency",
            "## Post-action verification",
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
            "request intent",
            "capability proposal",
            "argument normalization",
            "effective authority",
            "confirmation tuple",
            "policy generation",
            "confirmation generation",
            "execution binding",
            "transaction identity",
            "idempotency",
            "receipt",
            "durable final state",
            "alternative explanation",
            "evidence ceiling",
        ):
            self.assertIn(phrase, lower)

    def test_review_cases_encode_action_binding_reasoning(self):
        self.assertTrue(CASES.is_file(), "tool confirmation review-case matrix must exist before depth can pass")
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
                "request_intent",
                "capability_trace",
                "argument_trace",
                "effective_authority",
                "confirmation_tuple",
                "execution_binding",
                "transaction_state",
                "post_action_verification",
                "counterfactual_control",
                "alternative_explanation",
                "evidence_level",
                "evidence_ceiling",
            ):
                self.assertIn(field, scenario)
                self.assertIsInstance(scenario[field], str)
                self.assertGreaterEqual(len(scenario[field].strip()), 40)

    def test_skill_is_registered_as_twelfth_operator_depth_profile(self):
        payload = json.loads(PROFILES.read_text(encoding="utf-8"))
        profiles = payload["profiles"]
        self.assertGreaterEqual(len(profiles), 12)
        matching = [p for p in profiles if p["skill"] == "tool-capability-and-confirmation-analysis"]
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
