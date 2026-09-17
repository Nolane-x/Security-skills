import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "boot-chain-and-secure-boot-analysis" / "SKILL.md"
RUNBOOK = ROOT / "skills" / "boot-chain-and-secure-boot-analysis" / "references" / "operator-runbook.md"
CASES = ROOT / "skills" / "boot-chain-and-secure-boot-analysis" / "references" / "operator-review-cases.json"
PROFILES = ROOT / "operator-depth" / "profiles.json"


class BootChainSecureBootDepthTests(unittest.TestCase):
    def test_skill_exposes_causal_boot_chain_model(self):
        text = SKILL.read_text(encoding="utf-8")
        for section in (
            "## Causal boot-chain model",
            "## Root, policy, and signer authority",
            "## Component selection and identity",
            "## Selected-versus-loaded binding",
            "## Rollback and freshness generation",
            "## Handoff and next-stage inheritance",
            "## Recovery and alternate-path reasoning",
            "## Boot-chain evidence ladder",
            "## Counterfactual proof",
            "## Alternative explanations",
            "## Evidence ceiling",
        ):
            self.assertIn(section, text)

        lower = text.lower()
        for concept in (
            "immutable or policy root-of-trust identity -> active verification-policy/key generation -> boot mode and path identity -> boot target/slot/component selection -> candidate component identity and digest -> signature/measurement result -> signer or verification authority decision -> version/rollback generation decision -> accepted component identity -> loaded/executed component identity -> verified-to-loaded binding -> handoff state and next-stage security context -> next-stage trust inheritance -> bounded synthetic boot outcome -> receipt/log/attestation binding -> lifecycle, revocation, rollback, and recovery generation",
            "measured boot != verified boot or enforcement",
            "signature validity != authorized boot signer",
            "candidate artifact identity != selected artifact identity",
            "selected artifact identity != loaded/executed artifact identity",
            "digest match != approved version or rollback generation",
            "rollback metadata presence != monotonic rollback enforcement",
            "verified update/install != boot selection or execution",
            "verification of one stage != authenticated handoff",
            "recovery/alternate slot path != equivalent verification policy",
            "valid key/certificate != active authorized key generation",
            "bc0",
            "bc1",
            "bc2",
            "bc3",
            "bc4",
            "bc5",
            "counterfactual",
            "evidence ceiling",
        ):
            self.assertIn(concept, lower)

    def test_runbook_requires_transition_level_boot_reasoning(self):
        self.assertTrue(RUNBOOK.is_file(), "boot-chain operator runbook must exist before depth can pass")
        text = RUNBOOK.read_text(encoding="utf-8")
        for section in (
            "## Attack surface",
            "## Hypothesis matrix",
            "## Root-of-trust and policy-generation trace",
            "## Boot-mode and path trace",
            "## Component selection and identity trace",
            "## Signature and signer-authority trace",
            "## Rollback and freshness-generation trace",
            "## Selected-versus-loaded binding trace",
            "## Handoff and next-stage inheritance trace",
            "## Recovery and alternate-path equivalence trace",
            "## Receipt, measurement, and attestation trace",
            "## Lifecycle/revocation generation trace",
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
            "measurement != enforcement",
            "signer authorization",
            "selected component",
            "loaded component",
            "verified-to-loaded",
            "rollback generation",
            "recovery path",
            "alternate path",
            "handoff state",
            "attestation",
            "debug/manufacturing",
            "alternative explanation",
            "evidence ceiling",
        ):
            self.assertIn(phrase, lower)

    def test_review_cases_encode_boot_chain_reasoning(self):
        self.assertTrue(CASES.is_file(), "boot-chain review-case matrix must exist before depth can pass")
        payload = json.loads(CASES.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 1)
        self.assertGreaterEqual(len(payload["scenarios"]), 3)
        required_ids = {
            "root-policy-component-binding",
            "rollback-slot-loaded-identity-binding",
            "recovery-handoff-generation-binding",
        }
        self.assertTrue(required_ids.issubset({scenario["id"] for scenario in payload["scenarios"]}))
        required = (
            "hypothesis",
            "safe_oracle",
            "positive_control",
            "negative_control",
            "stop_condition",
            "remediation_oracle",
            "root_of_trust_identity",
            "verification_policy_generation",
            "boot_mode_path",
            "selector_state",
            "candidate_component_identity",
            "candidate_digest_version",
            "signer_identity",
            "signer_authorization_decision",
            "rollback_domain_generation",
            "selected_component_identity",
            "loaded_component_identity",
            "verified_loaded_binding",
            "handoff_state_identity",
            "next_stage_consumer",
            "alternate_recovery_path",
            "bounded_boot_result",
            "receipt_attestation_binding",
            "lifecycle_generation",
            "counterfactual_control",
            "alternative_explanation",
            "evidence_level",
            "evidence_ceiling",
        )
        safe_terms = ("synthetic", "mock", "inert", "read-only", "controlled", "emulator")
        for scenario in payload["scenarios"]:
            for field in required:
                self.assertIn(field, scenario)
                self.assertIsInstance(scenario[field], str)
                self.assertGreaterEqual(len(scenario[field].strip()), 40)
            self.assertTrue(any(term in scenario["safe_oracle"].lower() for term in safe_terms))
            self.assertTrue(any(term in scenario["stop_condition"].lower() for term in ("stop", "abort", "do not proceed")))
            self.assertRegex(scenario["evidence_level"], r"\bBC[0-5]\b")
            self.assertRegex(scenario["evidence_ceiling"], r"\bBC[0-5]\b")

    def test_skill_is_registered_as_twentieth_operator_depth_profile(self):
        payload = json.loads(PROFILES.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 2)
        profiles = payload["profiles"]
        self.assertGreaterEqual(len(profiles), 20)
        matching = [p for p in profiles if p["skill"] == "boot-chain-and-secure-boot-analysis"]
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
