import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "certificate-and-hostname-validation-analysis" / "SKILL.md"
RUNBOOK = ROOT / "skills" / "certificate-and-hostname-validation-analysis" / "references" / "operator-runbook.md"
CASES = ROOT / "skills" / "certificate-and-hostname-validation-analysis" / "references" / "operator-review-cases.json"
PROFILES = ROOT / "operator-depth" / "profiles.json"


class CertificateHostnameDepthTests(unittest.TestCase):
    def test_skill_exposes_causal_peer_trust_model(self):
        text = SKILL.read_text(encoding="utf-8")
        for section in (
            "## Causal peer-trust model",
            "## Endpoint and reference-identity binding",
            "## Certification path and trust-anchor binding",
            "## Certificate constraints and peer authorization",
            "## Pinning, revocation, and callback semantics",
            "## Authenticated peer, session, and mTLS mapping",
            "## Lifecycle and generation reasoning",
            "## Certificate and hostname evidence ladder",
            "## Counterfactual proof",
            "## Alternative explanations",
            "## Evidence ceiling",
        ):
            self.assertIn(section, text)

        lower = text.lower()
        for concept in (
            "request/service intent -> original endpoint identity -> redirect/alternate-endpoint state -> transport target -> sni state -> verification reference identity -> verifier/library identity and configuration -> trust-store identity -> trust-store generation -> presented leaf/chain identity -> path-building inputs -> selected certification path -> selected trust anchor -> chain-signature/validity constraints -> eku/key-usage/policy/name-constraints state -> san/reference-name state -> canonical reference identity -> hostname/service-identity match -> pin policy and pin generation -> revocation/soft-fail policy state -> verification callback/override input -> callback decision -> final verifier/application accept-or-reject decision -> authenticated peer identity -> authenticated session identity -> mtls peer-to-account mapping where applicable -> privileged consumer/use -> bounded result/receipt -> certificate/trust/pin/revocation/policy/session/account-mapping lifecycle generation",
            "chain-valid != hostname-valid",
            "trusted-root != authorized-peer",
            "certificate signature valid != certificate policy authorized",
            "sni != verification reference identity",
            "url/original host != redirect target != transport target",
            "san/cn text != canonical reference identity",
            "path-building success != intended trust-anchor selection",
            "eku/key-usage validity != hostname/service authorization",
            "pin match != complete pki validation",
            "revocation unavailable != revocation good",
            "callback invoked != callback controls the final decision",
            "callback accept != application/session authenticated-peer binding",
            "certificate accepted != mtls account authorized",
            "connection success != proof of which certificate/path/reference identity was accepted",
            "session resumed != current trust/pin/revocation/policy generation",
            "bounded synthetic wrong-peer acceptance != broad interception capability",
            "action/result success != receipt binding",
            "pki0",
            "pki1",
            "pki2",
            "pki3",
            "pki4",
            "pki5",
            "counterfactual",
            "alternative explanation",
            "evidence ceiling",
            "local/owned/sandboxed",
        ):
            self.assertIn(concept, lower)

    def test_runbook_requires_transition_level_peer_trust_reasoning(self):
        self.assertTrue(RUNBOOK.is_file(), "certificate/hostname operator runbook must exist before depth can pass")
        text = RUNBOOK.read_text(encoding="utf-8")
        for section in (
            "## Attack surface",
            "## Hypothesis matrix",
            "## Peer and endpoint intent trace",
            "## Reference-identity and SNI trace",
            "## Verifier and trust-store trace",
            "## Certification-path and trust-anchor trace",
            "## Certificate-constraint trace",
            "## SAN and hostname binding trace",
            "## Pinning and revocation trace",
            "## Callback and final-decision trace",
            "## Authenticated-peer/session and mTLS mapping trace",
            "## Lifecycle and generation trace",
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
            "canonical reference identity",
            "selected trust anchor",
            "trust-store generation",
            "pin generation",
            "soft-fail",
            "final application decision",
            "authenticated peer identity",
            "authenticated session identity",
            "receipt/result",
            "synthetic ca",
            "wrong-host",
            "debug-only",
            "alternative explanation",
            "evidence ceiling",
            "pki5",
        ):
            self.assertIn(phrase, lower)

    def test_review_cases_encode_peer_trust_reasoning(self):
        self.assertTrue(CASES.is_file(), "certificate/hostname review-case matrix must exist before depth can pass")
        payload = json.loads(CASES.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 1)
        self.assertGreaterEqual(len(payload["scenarios"]), 3)
        required_ids = {
            "peer-reference-identity-binding",
            "callback-pin-effective-decision-binding",
            "trust-policy-session-generation-binding",
        }
        self.assertTrue(required_ids.issubset({scenario["id"] for scenario in payload["scenarios"]}))
        required = (
            "hypothesis",
            "safe_oracle",
            "positive_control",
            "negative_control",
            "stop_condition",
            "remediation_oracle",
            "intended_peer_identity",
            "endpoint_redirect_transport_state",
            "sni_state",
            "canonical_reference_identity",
            "verifier_identity_configuration",
            "trust_store_identity_generation",
            "presented_leaf_chain_identity",
            "path_building_selected_path_anchor",
            "certificate_constraint_state",
            "san_hostname_match_state",
            "pin_policy_generation",
            "revocation_soft_fail_state",
            "callback_override_state",
            "final_application_decision",
            "authenticated_peer_identity",
            "authenticated_session_identity",
            "mtls_account_mapping",
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
            self.assertRegex(scenario["evidence_level"], r"\bPKI[0-5]\b")
            self.assertRegex(scenario["evidence_ceiling"], r"\bPKI[0-5]\b")

    def test_skill_is_registered_as_twenty_second_operator_depth_profile(self):
        payload = json.loads(PROFILES.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 2)
        profiles = payload["profiles"]
        self.assertGreaterEqual(len(profiles), 22)
        matching = [p for p in profiles if p["skill"] == "certificate-and-hostname-validation-analysis"]
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
