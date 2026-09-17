import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "certificate-and-hostname-validation-analysis" / "SKILL.md"
RUNBOOK = ROOT / "skills" / "certificate-and-hostname-validation-analysis" / "references" / "operator-runbook.md"
CASES = ROOT / "skills" / "certificate-and-hostname-validation-analysis" / "references" / "operator-review-cases.json"
PROFILES = ROOT / "operator-depth" / "profiles.json"


class CertificateHostnameValidationDepthTests(unittest.TestCase):
    def test_skill_exposes_causal_certificate_identity_model(self):
        text = SKILL.read_text(encoding="utf-8")
        for section in (
            "## Causal certificate and peer-identity model",
            "## Peer identity and reference binding",
            "## Path construction and trust-anchor authority",
            "## Certificate policy and application decision",
            "## Pinning and mutual TLS binding",
            "## Session, revocation, and lifecycle reasoning",
            "## Certificate identity evidence ladder",
            "## Counterfactual proof",
            "## Alternative explanations",
            "## Evidence ceiling",
        ):
            self.assertIn(section, text)

        lower = text.lower()
        for concept in (
            "connection intent -> intended peer/service identity -> reference identifier and endpoint authority -> transport endpoint after routing/redirect/proxy selection -> tls role/context -> presented certificate chain identity -> constructed validation path -> trust-anchor identity and trust-store generation -> signature/path validation -> certificate time state -> eku/key-usage/policy and name-constraints state -> san/reference-identifier binding -> library verifier result -> application callback/override decision -> pin policy and pin generation when required -> mtls certificate identity and principal mapping when applicable -> final accept/reject decision -> bounded synthetic connection result -> session/resumption/reuse binding -> revocation/trust-store/pin/certificate lifecycle generation",
            "presented chain != constructed validation path",
            "chain-valid != hostname-valid",
            "hostname/san match != complete certificate-policy acceptance",
            "trusted root presence != selected trust-anchor identity",
            "trust-anchor identity != trust-store generation",
            "certificate time validity != revocation freshness",
            "library verifier success != final application acceptance",
            "application callback allow != correct peer-identity binding",
            "pin match != complete pki identity proof",
            "pinning absence != vulnerability",
            "transport peer != application service identity",
            "mtls certificate possession != application principal authorization",
            "cached verification result != current policy generation",
            "session resumption/reuse != automatic revalidation under a changed policy generation",
            "revocation status unavailable != proof of either validity or revocation",
            "redirected/rerouted endpoint != original reference authority",
            "pki0",
            "pki1",
            "pki2",
            "pki3",
            "pki4",
            "pki5",
            "counterfactual",
            "evidence ceiling",
        ):
            self.assertIn(concept, lower)

    def test_runbook_requires_transition_level_certificate_reasoning(self):
        self.assertTrue(RUNBOOK.is_file(), "certificate/hostname operator runbook must exist before depth can pass")
        text = RUNBOOK.read_text(encoding="utf-8")
        for section in (
            "## Attack surface",
            "## Hypothesis matrix",
            "## Connection intent and reference identity trace",
            "## Endpoint routing and TLS context trace",
            "## Presented chain and constructed path trace",
            "## Trust anchor and trust-store generation trace",
            "## Certificate policy and name-binding trace",
            "## Verifier callback and final-decision trace",
            "## Pin policy and pin-generation trace",
            "## mTLS identity and principal-mapping trace",
            "## Session cache and resumption trace",
            "## Revocation and lifecycle-generation trace",
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
            "reference identifier",
            "constructed path",
            "trust-anchor identity",
            "trust-store generation",
            "san/reference-identifier",
            "application override",
            "pin generation",
            "principal mapping",
            "session resumption",
            "revocation policy",
            "sni",
            "debug-only",
            "alternative explanation",
            "evidence ceiling",
        ):
            self.assertIn(phrase, lower)

    def test_review_cases_encode_certificate_identity_reasoning(self):
        self.assertTrue(CASES.is_file(), "certificate/hostname review-case matrix must exist before depth can pass")
        payload = json.loads(CASES.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 1)
        self.assertGreaterEqual(len(payload["scenarios"]), 3)
        required_ids = {
            "peer-identity-chain-hostname-binding",
            "callback-pin-policy-binding",
            "lifecycle-resumption-mtls-binding",
        }
        self.assertTrue(required_ids.issubset({scenario["id"] for scenario in payload["scenarios"]}))
        required = (
            "hypothesis",
            "safe_oracle",
            "positive_control",
            "negative_control",
            "stop_condition",
            "remediation_oracle",
            "connection_intent",
            "reference_identifier",
            "endpoint_authority",
            "transport_peer",
            "tls_role_context",
            "presented_chain",
            "constructed_path",
            "trust_anchor_identity",
            "trust_store_generation",
            "chain_validation_result",
            "certificate_time_state",
            "eku_key_usage_policy",
            "name_constraints_state",
            "san_identity_binding",
            "library_verifier_result",
            "application_override",
            "pin_policy_state",
            "pin_generation",
            "client_certificate_identity",
            "principal_mapping",
            "final_accept_reject",
            "bounded_result",
            "session_resumption_state",
            "revocation_state",
            "lifecycle_generation",
            "counterfactual_control",
            "alternative_explanation",
            "evidence_level",
            "evidence_ceiling",
        )
        safe_terms = ("synthetic", "mock", "inert", "read-only", "controlled", "local", "canary")
        for scenario in payload["scenarios"]:
            for field in required:
                self.assertIn(field, scenario)
                self.assertIsInstance(scenario[field], str)
                self.assertGreaterEqual(len(scenario[field].strip()), 40)
            self.assertTrue(any(term in scenario["safe_oracle"].lower() for term in safe_terms))
            self.assertTrue(any(term in scenario["stop_condition"].lower() for term in ("stop", "abort", "do not proceed")))
            self.assertRegex(scenario["evidence_level"], r"\bPKI[0-5]\b")
            self.assertRegex(scenario["evidence_ceiling"], r"\bPKI[0-5]\b")

    def test_skill_is_registered_as_twentieth_operator_depth_profile(self):
        payload = json.loads(PROFILES.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 2)
        profiles = payload["profiles"]
        self.assertEqual(len(profiles), 20)
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
