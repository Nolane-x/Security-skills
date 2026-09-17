import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "certificate-and-hostname-validation-analysis" / "SKILL.md"
RUNBOOK = ROOT / "skills" / "certificate-and-hostname-validation-analysis" / "references" / "operator-runbook.md"
CASES = ROOT / "skills" / "certificate-and-hostname-validation-analysis" / "references" / "operator-review-cases.json"
PROFILES = ROOT / "operator-depth" / "profiles.json"


class CertificateHostnameValidationDepthTests(unittest.TestCase):
    def test_skill_exposes_causal_peer_authentication_model(self):
        text = SKILL.read_text(encoding="utf-8")
        for section in (
            "## Causal peer-authentication model",
            "## Reference identity and endpoint binding",
            "## Certificate path and trust-anchor binding",
            "## SAN and hostname/reference-identity reasoning",
            "## Callback, pin, and revocation composition",
            "## Authenticated session and consumer binding",
            "## Lifecycle and generation reasoning",
            "## Certificate evidence ladder",
            "## Counterfactual proof",
            "## Alternative explanations",
            "## Evidence ceiling",
        ):
            self.assertIn(section, text)

        lower = text.lower()
        for concept in (
            "intended peer identity -> endpoint/redirect/sni state -> verifier configuration -> trust-store identity -> trust-store generation -> presented chain identity -> path-building state -> selected trust-anchor identity -> certificate constraints/validity/eku/ku/name-constraints state -> san/reference-identity state -> canonical reference identity -> hostname/identity match decision -> pin/revocation policy state -> callback/override state -> effective accept/reject decision -> authenticated peer/session identity -> privileged consumer boundary -> bounded synthetic result -> receipt/result binding -> trust/pin/revocation/session lifecycle generation",
            "chain validation success != hostname/reference-identity validation success",
            "trusted root != authorized peer identity",
            "sni value != verification hostname/reference identity",
            "signature validity != policy authorization",
            "san text != canonical reference identity",
            "pin match != complete pki validation",
            "callback reachability != justified verification override",
            "certificate acceptance != mtls account/principal authorization",
            "cached/resumed session != current trust-store/pin/revocation policy generation",
            "redirect target != original authenticated peer identity",
            "verifier success != application-level authenticated-session binding",
            "connection success != receipt/result binding",
            "benign synthetic wrong-peer acceptance != broad interception capability",
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

    def test_runbook_requires_transition_level_pki_reasoning(self):
        self.assertTrue(RUNBOOK.is_file(), "certificate/hostname operator runbook must exist before depth can pass")
        text = RUNBOOK.read_text(encoding="utf-8")
        for section in (
            "## Attack surface",
            "## Hypothesis matrix",
            "## Reference identity, endpoint, redirect, and SNI trace",
            "## Trust store, path building, and trust-anchor trace",
            "## Certificate constraints and validity trace",
            "## SAN/canonical reference-identity and name-match trace",
            "## Callback/override, pin, and revocation trace",
            "## Authenticated peer/session and privileged-consumer trace",
            "## Lifecycle/trust/pin/revocation/session generation trace",
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
            "verification reference identity",
            "selected trust anchor",
            "trust-store generation",
            "canonical reference identity",
            "effective accept/reject decision",
            "authenticated peer/session identity",
            "receipt/result",
            "synthetic ca",
            "wrong-peer",
            "session resumption",
            "alternative explanation",
            "evidence ceiling",
            "pki5",
        ):
            self.assertIn(phrase, lower)

    def test_review_cases_encode_peer_identity_and_policy_reasoning(self):
        self.assertTrue(CASES.is_file(), "certificate/hostname review-case matrix must exist before depth can pass")
        payload = json.loads(CASES.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 1)
        self.assertGreaterEqual(len(payload["scenarios"]), 3)
        required_ids = {
            "chain-vs-reference-identity-binding",
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
            "endpoint_redirect_sni_state",
            "verification_reference_identity",
            "verifier_configuration",
            "trust_store_identity",
            "trust_store_generation",
            "presented_chain_identity",
            "path_building_state",
            "selected_trust_anchor",
            "certificate_constraints_state",
            "san_reference_identity_state",
            "canonical_reference_identity",
            "hostname_identity_match_decision",
            "pin_policy_state",
            "revocation_policy_state",
            "callback_override_state",
            "effective_accept_reject_decision",
            "authenticated_peer_session_identity",
            "privileged_consumer",
            "bounded_result",
            "receipt_result_binding",
            "lifecycle_generation",
            "counterfactual_control",
            "alternative_explanation",
            "evidence_level",
            "evidence_ceiling",
        )
        safe_terms = ("synthetic", "mock", "inert", "read-only", "controlled", "canary")
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
        self.assertEqual(len(profiles), 22)
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
