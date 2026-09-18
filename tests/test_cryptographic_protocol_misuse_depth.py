import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "cryptographic-protocol-misuse-analysis" / "SKILL.md"
RUNBOOK = ROOT / "skills" / "cryptographic-protocol-misuse-analysis" / "references" / "operator-runbook.md"
CASES = ROOT / "skills" / "cryptographic-protocol-misuse-analysis" / "references" / "operator-review-cases.json"
PROFILES = ROOT / "operator-depth" / "profiles.json"


class CryptographicProtocolMisuseDepthTests(unittest.TestCase):
    def test_skill_exposes_causal_protocol_composition_model(self):
        text = SKILL.read_text(encoding="utf-8")
        for section in (
            "## Causal protocol-composition model",
            "## Negotiation and transcript binding",
            "## Key schedule, role, epoch, and domain separation",
            "## Protocol phase and authenticated-context binding",
            "## Authenticate-before-use ordering",
            "## Replay, freshness, and early-data reasoning",
            "## Rekey, resumption, and lifecycle generations",
            "## Cryptographic protocol evidence ladder",
            "## Counterfactual proof",
            "## Alternative explanations",
            "## Evidence ceiling",
        ):
            self.assertIn(section, text)

        lower = text.lower()
        for concept in (
            "security goal/protocol intent -> peer/role/session identities -> protocol version and feature negotiation -> selected algorithm/suite -> transcript identity -> authenticated negotiation binding -> key-schedule root/context -> derived key role/direction/epoch -> domain-separation labels -> nonce/sequence/record identity -> protocol phase/state -> authenticated context/aad -> verification/decryption/authentication order -> replay/freshness state -> final verifier/application accept-or-reject decision -> authenticated protocol/session state -> privileged consumer/use -> bounded result/receipt -> protocol/key/replay/resumption/rekey lifecycle generation",
            "approved primitive != safe protocol composition",
            "signature valid != intended role/context authorized",
            "decrypt success != authenticated acceptance",
            "handshake success != authenticated negotiation transcript",
            "selected suite != authenticated selected suite",
            "unique nonce != correct key/nonce/context binding",
            "same key material != same role/direction/epoch authorization",
            "mac/tag valid != message phase/action/context authorized",
            "replay-cache miss != message fresh",
            "resumed session != current protocol/key/policy generation",
            "0-rtt accepted != replay-safe application action",
            "bounded synthetic wrong-context acceptance != key recovery or broad cryptanalytic compromise",
            "action/result success != receipt binding",
            "cp0",
            "cp1",
            "cp2",
            "cp3",
            "cp4",
            "cp5",
            "counterfactual",
            "alternative explanation",
            "evidence ceiling",
            "local/owned/sandboxed",
        ):
            self.assertIn(concept, lower)

    def test_runbook_requires_transition_level_crypto_protocol_reasoning(self):
        self.assertTrue(RUNBOOK.is_file(), "cryptographic protocol operator runbook must exist before depth can pass")
        text = RUNBOOK.read_text(encoding="utf-8")
        for section in (
            "## Attack surface",
            "## Hypothesis matrix",
            "## Protocol intent and role/session trace",
            "## Negotiation and downgrade trace",
            "## Transcript and authenticated-negotiation trace",
            "## Key schedule, role, direction, epoch, and domain-separation trace",
            "## Nonce, sequence, and record identity trace",
            "## Protocol phase and authenticated-context trace",
            "## Verification and authentication-order trace",
            "## Replay and freshness trace",
            "## Rekey, resumption, and early-data lifecycle trace",
            "## Privileged-consumer and result trace",
            "## Controlled validation",
            "## False-positive controls",
            "## Counterfactual controls",
            "## Alternative explanations",
            "## Evidence capture",
            "## Evidence promotion and ceiling",
            "## Remediation checks",
        ):
            self.assertIn(section, text)

        lower = text.lower()
        for phrase in (
            "authenticated negotiation",
            "transcript identity",
            "key role",
            "domain separation",
            "auth-before-use",
            "replay",
            "early-data",
            "rekey",
            "resumption",
            "receipt/result",
            "synthetic key",
            "mock peer",
            "alternative explanation",
            "evidence ceiling",
            "cp5",
        ):
            self.assertIn(phrase, lower)

    def test_review_cases_encode_crypto_protocol_reasoning(self):
        self.assertTrue(CASES.is_file(), "cryptographic protocol review-case matrix must exist before depth can pass")
        payload = json.loads(CASES.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 1)
        self.assertGreaterEqual(len(payload["scenarios"]), 4)
        required_ids = {
            "negotiation-transcript-binding",
            "key-role-domain-separation",
            "authenticate-before-use",
            "replay-context-lifecycle-binding",
        }
        self.assertTrue(required_ids.issubset({scenario["id"] for scenario in payload["scenarios"]}))

        required = (
            "hypothesis",
            "safe_oracle",
            "positive_control",
            "negative_control",
            "stop_condition",
            "remediation_oracle",
            "security_goal_protocol_intent",
            "peer_role_session_identity",
            "protocol_version_suite_negotiation_state",
            "transcript_identity_binding",
            "key_schedule_root_context",
            "key_role_direction_epoch",
            "domain_separation_labels",
            "nonce_sequence_record_identity",
            "protocol_phase_state",
            "authenticated_context_binding",
            "verification_authentication_order",
            "replay_freshness_state",
            "final_application_decision",
            "authenticated_protocol_session_state",
            "privileged_consumer",
            "bounded_result",
            "receipt_result_binding",
            "lifecycle_generation",
            "counterfactual_control",
            "alternative_explanation",
            "evidence_level",
            "evidence_ceiling",
        )
        safe_terms = ("synthetic", "mock", "inert", "read-only", "controlled", "loopback")
        for scenario in payload["scenarios"]:
            for field in required:
                self.assertIn(field, scenario)
                self.assertIsInstance(scenario[field], str)
                self.assertGreaterEqual(len(scenario[field].strip()), 40)
            self.assertTrue(any(term in scenario["safe_oracle"].lower() for term in safe_terms))
            self.assertTrue(any(term in scenario["stop_condition"].lower() for term in ("stop", "abort", "do not proceed")))
            self.assertRegex(scenario["evidence_level"], r"\bCP[0-5]\b")
            self.assertRegex(scenario["evidence_ceiling"], r"\bCP[0-5]\b")

    def test_skill_is_registered_as_twenty_third_operator_depth_profile(self):
        payload = json.loads(PROFILES.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 2)
        profiles = payload["profiles"]
        self.assertGreaterEqual(len(profiles), 23)
        matching = [p for p in profiles if p["skill"] == "cryptographic-protocol-misuse-analysis"]
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
