import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "protocol-state-machine-analysis" / "SKILL.md"
RUNBOOK = ROOT / "skills" / "protocol-state-machine-analysis" / "references" / "operator-runbook.md"
CASES = ROOT / "skills" / "protocol-state-machine-analysis" / "references" / "operator-review-cases.json"
PROFILES = ROOT / "operator-depth" / "profiles.json"


class ProtocolStateMachineDepthTests(unittest.TestCase):
    def test_skill_exposes_causal_protocol_state_model(self):
        text = SKILL.read_text(encoding="utf-8")
        for section in (
            "## Causal protocol-state model",
            "## Peer, connection, session, and role generations",
            "## Transition guard and authenticated-context binding",
            "## Replay, retry, idempotency, and duplicate-effect binding",
            "## Timeout, cancellation, reset, reconnect, and late-completion binding",
            "## Commit, terminal-state, and downstream-action binding",
            "## Protocol-state evidence ladder",
            "## Counterfactual protocol controls",
            "## Alternative explanations",
            "## Evidence ceiling",
        ):
            self.assertIn(section, text)

        lower = text.lower()
        for concept in (
            "peer identity",
            "peer role generation",
            "connection identity/generation",
            "session identity/generation",
            "stream/transaction identity/generation",
            "protocol version/feature generation",
            "message identity/generation",
            "request/response correlation",
            "transition identity",
            "transition guard",
            "authenticated context",
            "authorization context",
            "replay/retry/cancellation generation",
            "commit/terminal state",
            "downstream consumer/action",
            "effective protocol capability",
            "bounded result",
            "receipt/result",
            "syntactically valid message != legal state transition",
            "authenticated once != authenticated current session",
            "connection identity != session identity",
            "message id != operation identity",
            "response correlation != causal authorization",
            "duplicate request != duplicate side effect",
            "retry != idempotent replay",
            "acknowledgment != commit",
            "timeout != rollback",
            "reset != state revocation",
            "reconnect != same session",
            "negotiated feature != authorized feature use",
            "role label != current authority",
            "stream id != ownership",
            "out-of-order message != forbidden transition without protocol evidence",
            "weird response != invariant violation",
            "terminal state != cleanup complete",
            "stale background completion != current operation",
            "protocol crash != protocol-state exploitability",
            "pst0",
            "pst1",
            "pst2",
            "pst3",
            "pst4",
            "pst5",
            "counterfactual",
            "alternative explanation",
            "evidence ceiling",
            "local/owned/sandboxed",
        ):
            self.assertIn(concept, lower)

    def test_runbook_requires_transition_level_protocol_reasoning(self):
        self.assertTrue(RUNBOOK.is_file(), "protocol-state operator runbook must exist before depth can pass")
        text = RUNBOOK.read_text(encoding="utf-8")
        for section in (
            "## Attack surface",
            "## Hypothesis matrix",
            "## Peer/session/role-generation trace",
            "## Transition-guard and authenticated-context trace",
            "## Replay/retry/idempotency trace",
            "## Timeout/cancellation/reset/reconnect trace",
            "## Commit/terminal-state/downstream-action trace",
            "## Controlled validation",
            "## False-positive controls",
            "## Counterfactual protocol controls",
            "## Alternative explanations",
            "## Evidence capture",
            "## Evidence promotion and ceiling",
            "## Remediation checks",
        ):
            self.assertIn(section, text)

        lower = text.lower()
        for phrase in (
            "peer identity",
            "session generation",
            "role generation",
            "transition guard",
            "authenticated context",
            "retry",
            "idempotency",
            "replay",
            "timeout",
            "cancellation",
            "reset",
            "reconnect",
            "late completion",
            "commit",
            "terminal state",
            "downstream action",
            "synthetic",
            "mock",
            "read-only",
            "counterfactual",
            "alternative explanation",
            "evidence ceiling",
            "pst5",
        ):
            self.assertIn(phrase, lower)

    def test_review_cases_encode_protocol_state_reasoning(self):
        self.assertTrue(CASES.is_file(), "protocol-state review-case matrix must exist before depth can pass")
        payload = json.loads(CASES.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 1)
        self.assertGreaterEqual(len(payload["scenarios"]), 4)

        required_ids = {
            "stale-session-replay-after-reconnect",
            "retry-duplicate-commit",
            "role-change-stale-authority",
            "timeout-late-completion-cross-generation",
        }
        self.assertTrue(required_ids.issubset({scenario["id"] for scenario in payload["scenarios"]}))

        required = (
            "hypothesis",
            "safe_oracle",
            "positive_control",
            "negative_control",
            "stop_condition",
            "remediation_oracle",
            "peer_session_role_generation",
            "transition_guard_authenticated_context",
            "replay_retry_idempotency_state",
            "timeout_cancel_reset_reconnect_state",
            "commit_terminal_downstream_action",
            "downstream_consumer_identity",
            "effective_protocol_capability",
            "bounded_result",
            "receipt_result_binding",
            "counterfactual_control",
            "alternative_explanation",
            "evidence_level",
            "evidence_ceiling",
        )
        safe_terms = ("synthetic", "mock", "inert", "read-only", "controlled")
        for scenario in payload["scenarios"]:
            for field in required:
                self.assertIn(field, scenario)
                self.assertIsInstance(scenario[field], str)
                self.assertGreaterEqual(len(scenario[field].strip()), 40)
            self.assertTrue(any(term in scenario["safe_oracle"].lower() for term in safe_terms))
            self.assertTrue(any(term in scenario["stop_condition"].lower() for term in ("stop", "abort", "do not proceed")))
            self.assertRegex(scenario["evidence_level"], r"\bPST[0-5]\b")
            self.assertRegex(scenario["evidence_ceiling"], r"\bPST[0-5]\b")

    def test_skill_is_registered_as_twenty_ninth_operator_depth_profile(self):
        payload = json.loads(PROFILES.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 2)
        profiles = payload["profiles"]
        self.assertEqual(len(profiles), 29)
        matching = [p for p in profiles if p["skill"] == "protocol-state-machine-analysis"]
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
