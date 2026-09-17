import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "certificate-and-hostname-validation-analysis" / "SKILL.md"
RUNBOOK = ROOT / "skills" / "certificate-and-hostname-validation-analysis" / "references" / "operator-runbook.md"
CASES = ROOT / "skills" / "certificate-and-hostname-validation-analysis" / "references" / "operator-review-cases.json"
PROFILES = ROOT / "operator-depth" / "profiles.json"


class CertificateHostnameDepthTests(unittest.TestCase):
    def test_skill_exposes_causal_peer_identity_model(self):
        text = SKILL.read_text(encoding="utf-8")
        for section in (
            "## Causal peer-identity model",
            "## Application intent and reference identity",
            "## Route, redirect, proxy, and SNI binding",
            "## Trust-store and path authority",
            "## SAN, hostname, and service-role validation",
            "## Pinning and revocation lifecycle",
            "## Application callback and final decision",
            "## mTLS certificate-to-principal mapping",
            "## Peer-identity evidence ladder",
            "## Counterfactual proof",
            "## Alternative explanations",
            "## Evidence ceiling",
            "## Evidence contract",
        ):
            self.assertIn(section, text)

        lower = text.lower()
        for concept in (
            "application-intended peer/service identity -> reference identity and normalized verification name -> connection route/redirect/proxy target and tls sni context -> active trust-store and verification-policy generation -> candidate leaf/intermediate/root certificate identities -> chain/path-building result and selected trust anchor -> signature, validity-time, basic-constraints, path-length, and name-constraints decisions -> san/reference-name match decision -> eku/key-usage/service-role decision -> revocation policy/state generation and result -> pin policy/set generation and result -> library verification result -> application callback/override/fallback decision -> final accepted server-certificate identity -> established session peer/service identity -> request/consumer binding and bounded synthetic result -> receipt/log/correlation binding -> lifecycle rotation/revocation/pin/trust-store generation",
            "chain/path validity != hostname/reference-identity validity",
            "root present in a trust store != selected path anchored to the intended active root generation",
            "certificate signature validity != certificate authorization",
            "san presence != match to the application-intended reference identity",
            "sni value != hostname-verification reference identity",
            "pin match != complete pki/name validation",
            "revocation configuration != revocation enforcement/result",
            "library verification success != final application accept decision",
            "connection success != proof of intended peer identity",
            "accepted client certificate != correctly mapped application principal",
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

    def test_runbook_requires_transition_level_pki_reasoning(self):
        self.assertTrue(RUNBOOK.is_file(), "certificate-hostname operator runbook must exist before depth can pass")
        text = RUNBOOK.read_text(encoding="utf-8")
        for section in (
            "## Attack surface",
            "## Hypothesis matrix",
            "## Application intent and reference-identity trace",
            "## Route, redirect, proxy, and SNI trace",
            "## Trust-store and verification-policy generation trace",
            "## Chain/path-building and trust-anchor trace",
            "## SAN, hostname, wildcard, and IDNA decision trace",
            "## EKU, key-usage, and service-role trace",
            "## Pinning generation trace",
            "## Revocation policy, status, and freshness trace",
            "## Library verifier and application-callback trace",
            "## Established-session peer binding trace",
            "## mTLS certificate-to-principal mapping trace",
            "## Lifecycle/rotation/revocation generation trace",
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
            "application-intended identity",
            "reference name",
            "selected trust anchor",
            "trust-store generation",
            "hostname verification",
            "signer/path authority",
            "pin generation",
            "revocation freshness",
            "application callback",
            "established session",
            "mapped principal",
            "alternative explanation",
            "evidence ceiling",
        ):
            self.assertIn(phrase, lower)

    def test_review_cases_encode_peer_identity_reasoning(self):
        self.assertTrue(CASES.is_file(), "certificate-hostname review cases must exist before depth can pass")
        payload = json.loads(CASES.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 1)
        self.assertGreaterEqual(len(payload["scenarios"]), 3)
        required_ids = {
            "reference-name-chain-policy-binding",
            "pin-revocation-generation-binding",
            "mtls-certificate-principal-binding",
        }
        self.assertTrue(required_ids.issubset({scenario["id"] for scenario in payload["scenarios"]}))
        required = (
            "hypothesis",
            "safe_oracle",
            "positive_control",
            "negative_control",
            "stop_condition",
            "remediation_oracle",
            "intended_service_identity",
            "reference_identity",
            "normalized_verification_name",
            "route_redirect_proxy_identity",
            "sni_identity",
            "trust_store_generation",
            "verification_policy_generation",
            "leaf_certificate_identity",
            "chain_path_identity",
            "selected_trust_anchor_identity",
            "san_name_decision",
            "eku_key_usage_decision",
            "validation_time_identity",
            "revocation_policy_generation",
            "revocation_status_freshness",
            "pin_set_generation",
            "library_verification_result",
            "application_callback_decision",
            "final_accepted_certificate_identity",
            "established_session_peer_identity",
            "client_certificate_identity",
            "mapped_principal_identity",
            "bounded_session_result",
            "receipt_correlation_binding",
            "lifecycle_generation",
            "counterfactual_control",
            "alternative_explanation",
            "evidence_level",
            "evidence_ceiling",
        )
        safe_terms = ("synthetic", "mock", "local", "loopback", "inert", "controlled", "read-only")
        for scenario in payload["scenarios"]:
            for field in required:
                self.assertIn(field, scenario)
                self.assertIsInstance(scenario[field], str)
                self.assertGreaterEqual(len(scenario[field].strip()), 40)
            self.assertTrue(any(term in scenario["safe_oracle"].lower() for term in safe_terms))
            self.assertTrue(any(term in scenario["stop_condition"].lower() for term in ("stop", "abort", "do not proceed")))
            self.assertRegex(scenario["evidence_level"], r"\bPKI[0-5]\b")
            self.assertRegex(scenario["evidence_ceiling"], r"\bPKI[0-5]\b")

    def test_skill_is_registered_as_twenty_first_operator_depth_profile(self):
        payload = json.loads(PROFILES.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 2)
        profiles = payload["profiles"]
        self.assertGreaterEqual(len(profiles), 21)
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
