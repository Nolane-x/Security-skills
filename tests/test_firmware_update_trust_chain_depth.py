import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "firmware-update-trust-chain-analysis" / "SKILL.md"
RUNBOOK = ROOT / "skills" / "firmware-update-trust-chain-analysis" / "references" / "operator-runbook.md"
CASES = ROOT / "skills" / "firmware-update-trust-chain-analysis" / "references" / "operator-review-cases.json"
PROFILES = ROOT / "operator-depth" / "profiles.json"


class FirmwareUpdateTrustChainDepthTests(unittest.TestCase):
    def test_skill_exposes_causal_firmware_update_model(self):
        text = SKILL.read_text(encoding="utf-8")
        for section in (
            "## Causal firmware-update trust model",
            "## Device, policy, update-attempt, and artifact generations",
            "## Manifest, signer, hardware, and version binding",
            "## Component-set and transformed-artifact binding",
            "## Staging, activation, and transaction binding",
            "## Rollback/version-state commit binding",
            "## Recovery and fallback policy binding",
            "## Final update-state consumer",
            "## Firmware-update evidence ladder",
            "## Counterfactual update controls",
            "## Alternative explanations",
            "## Evidence ceiling",
        ):
            self.assertIn(section, text)

        lower = text.lower()
        for concept in (
            "device/revision identity",
            "update path/mode identity",
            "update attempt generation",
            "acquired bundle identity",
            "authenticated object/envelope identity",
            "signer/root identity",
            "signer/policy generation",
            "canonical manifest identity",
            "manifest field generation",
            "hardware target identity",
            "current version/rollback generation",
            "target version",
            "rollback domain",
            "component-set identity",
            "component identity/generation",
            "authenticated component digest/metadata",
            "transform/extraction/delta identity",
            "delta-base identity/generation",
            "transformed component identity",
            "staging target/slot identity",
            "staging generation",
            "activation transaction identity/generation",
            "rollback/version-state commit identity/generation",
            "recovery/fallback path identity",
            "recovery policy generation",
            "final activated component-set identity",
            "update-state consumer",
            "effective update-trust capability",
            "bounded result",
            "receipt/result",
            "downloaded bundle != authenticated bundle",
            "authenticated bundle != authorized update",
            "signature validity != authorized signer for current policy generation",
            "authenticated manifest != consumed component by assumption",
            "manifest field != canonical security identity until normalization/binding is proven",
            "component name/version != component artifact identity",
            "authenticated compressed/archive bytes != authenticated extracted object by assumption",
            "authenticated delta != authenticated final reconstructed component",
            "valid delta signature != correct delta base generation",
            "component digest match != hardware-target authorization",
            "accepted target version != monotonic rollback enforcement",
            "rollback metadata presence != rollback-state commit",
            "version check before staging != version check at activation by assumption",
            "staged component != activated component",
            "activation request != committed activation",
            "update success flag != complete multi-component activation",
            "partial component success != atomic update transaction",
            "slot write != slot selection or boot execution",
            "recovery path != normal-path policy equivalence by assumption",
            "recovery signer != production signer authorization by assumption",
            "rollback/fallback != stale-version acceptance without policy evidence",
            "failed update != known recoverable state by assumption",
            "power-loss recovery != transaction rollback by assumption",
            "post-verification parsing != safe parsing",
            "archive extraction success != path/component binding",
            "hardware identifier string match != canonical hardware identity",
            "same version number != same artifact generation",
            "update receipt != installed/activated identity unless correlated",
            "boot of an activated component != update-chain proof",
            "fwu0",
            "fwu1",
            "fwu2",
            "fwu3",
            "fwu4",
            "fwu5",
            "counterfactual",
            "alternative explanation",
            "evidence ceiling",
            "local/owned/sandboxed",
        ):
            self.assertIn(concept, lower)

    def test_runbook_requires_update_chain_reasoning(self):
        self.assertTrue(RUNBOOK.is_file(), "firmware-update operator runbook must exist before depth can pass")
        text = RUNBOOK.read_text(encoding="utf-8")
        for section in (
            "## Attack surface",
            "## Hypothesis matrix",
            "## Device/policy/update-generation trace",
            "## Manifest/signer/hardware/version trace",
            "## Component-set/transformed-artifact trace",
            "## Staging/activation/transaction trace",
            "## Rollback/version-state commit trace",
            "## Recovery/fallback policy trace",
            "## Final update-state consumer trace",
            "## Controlled validation",
            "## False-positive controls",
            "## Counterfactual update controls",
            "## Alternative explanations",
            "## Evidence capture",
            "## Evidence promotion and ceiling",
            "## Remediation checks",
        ):
            self.assertIn(section, text)

        lower = text.lower()
        for phrase in (
            "device identity",
            "policy generation",
            "update attempt generation",
            "canonical manifest",
            "hardware target",
            "rollback domain",
            "component-set",
            "delta base",
            "staging generation",
            "activation transaction",
            "rollback state",
            "recovery policy",
            "final update-state consumer",
            "synthetic",
            "fake",
            "mock",
            "in-memory",
            "counterfactual",
            "alternative explanation",
            "evidence ceiling",
            "fwu5",
        ):
            self.assertIn(phrase, lower)

    def test_review_cases_encode_firmware_update_reasoning(self):
        self.assertTrue(CASES.is_file(), "firmware-update review-case matrix must exist before depth can pass")
        payload = json.loads(CASES.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 1)
        self.assertGreaterEqual(len(payload["scenarios"]), 4)

        required_ids = {
            "manifest-component-resolution-substitution",
            "delta-base-generation-mismatch",
            "rollback-counter-activation-commit-order",
            "recovery-policy-generation-drift",
        }
        self.assertTrue(required_ids.issubset({scenario["id"] for scenario in payload["scenarios"]}))

        required = (
            "hypothesis",
            "safe_oracle",
            "positive_control",
            "negative_control",
            "stop_condition",
            "remediation_oracle",
            "device_policy_update_generation",
            "manifest_signer_hardware_version",
            "component_set_transformed_artifact",
            "staging_activation_transaction",
            "rollback_version_state_commit",
            "recovery_fallback_policy",
            "final_update_state_consumer",
            "effective_update_trust_capability",
            "bounded_result",
            "receipt_result_binding",
            "counterfactual_control",
            "alternative_explanation",
            "evidence_level",
            "evidence_ceiling",
        )
        safe_terms = ("synthetic", "mock", "inert", "read-only", "controlled", "fake", "in-memory")
        for scenario in payload["scenarios"]:
            for field in required:
                self.assertIn(field, scenario)
                self.assertIsInstance(scenario[field], str)
                self.assertGreaterEqual(len(scenario[field].strip()), 40)
            self.assertTrue(any(term in scenario["safe_oracle"].lower() for term in safe_terms))
            self.assertTrue(any(term in scenario["stop_condition"].lower() for term in ("stop", "abort", "do not proceed")))
            self.assertRegex(scenario["evidence_level"], r"\bFWU[0-5]\b")
            self.assertRegex(scenario["evidence_ceiling"], r"\bFWU[0-5]\b")

    def test_skill_is_registered_as_thirty_third_operator_depth_profile(self):
        payload = json.loads(PROFILES.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 2)
        profiles = payload["profiles"]
        self.assertGreaterEqual(len(profiles), 33)
        matching = [p for p in profiles if p["skill"] == "firmware-update-trust-chain-analysis"]
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
