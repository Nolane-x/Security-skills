import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "secrets-and-token-flow-analysis" / "SKILL.md"
RUNBOOK = ROOT / "skills" / "secrets-and-token-flow-analysis" / "references" / "operator-runbook.md"
CASES = ROOT / "skills" / "secrets-and-token-flow-analysis" / "references" / "operator-review-cases.json"
PROFILES = ROOT / "operator-depth" / "profiles.json"


class SecretsTokenFlowDepthTests(unittest.TestCase):
    def test_skill_exposes_causal_credential_authority_model(self):
        text = SKILL.read_text(encoding="utf-8")
        for section in (
            "## Causal credential-authority model",
            "## Credential-class model",
            "## Issuance provenance and binding",
            "## Possession, storage, and propagation",
            "## Verifier-decision trace",
            "## Token-class integrity",
            "## Authority representation and attenuation",
            "## Lifecycle, rotation, and revocation generation",
            "## Credential-authority evidence ladder",
            "## Counterfactual proof",
            "## Alternative explanations",
            "## Evidence ceiling",
        ):
            self.assertIn(section, text)

        lower = text.lower()
        for concept in (
            "credential origin -> issuer identity -> subject identity -> credential class -> issuance constraints -> possession channel -> storage representation -> propagation hop -> verifier identity -> verification decision -> audience/resource binding -> represented authority -> downstream exchange/delegation -> attenuated effective authority -> bounded action/result -> lifecycle/revocation generation",
            "secret bytes != authority semantics",
            "issuer identity != subject identity",
            "possession != permission",
            "valid signature/mac != valid authorization context",
            "identity token != access token",
            "delegated authority != deputy/downstream ambient authority",
            "audience validity != resource authorization",
            "expiry time != revocation generation",
            "s0",
            "s1",
            "s2",
            "s3",
            "s4",
            "s5",
            "counterfactual",
            "evidence ceiling",
        ):
            self.assertIn(concept, lower)

    def test_runbook_requires_transition_level_credential_reasoning(self):
        self.assertTrue(RUNBOOK.is_file(), "secrets/token operator runbook must exist before depth can pass")
        text = RUNBOOK.read_text(encoding="utf-8")
        for section in (
            "## Attack surface",
            "## Hypothesis matrix",
            "## Credential-class trace",
            "## Issuance provenance trace",
            "## Possession and storage trace",
            "## Propagation-boundary trace",
            "## Verifier-decision trace",
            "## Audience and resource binding",
            "## Authority representation trace",
            "## Delegation and attenuation trace",
            "## Lifecycle and revocation-generation trace",
            "## Result and receipt binding",
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
            "credential class",
            "issuer identity",
            "subject identity",
            "audience/resource",
            "verifier identity",
            "represented authority",
            "attenuated effective authority",
            "revocation generation",
            "token class",
            "counterfactual",
            "alternative explanation",
            "evidence ceiling",
        ):
            self.assertIn(phrase, lower)

    def test_review_cases_encode_credential_authority_reasoning(self):
        self.assertTrue(CASES.is_file(), "secrets/token review-case matrix must exist before depth can pass")
        payload = json.loads(CASES.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 1)
        self.assertGreaterEqual(len(payload["scenarios"]), 3)
        required = (
            "hypothesis",
            "safe_oracle",
            "positive_control",
            "negative_control",
            "stop_condition",
            "remediation_oracle",
            "credential_origin",
            "issuer_identity",
            "subject_identity",
            "credential_class",
            "issuance_constraints",
            "possession_channel",
            "storage_representation",
            "propagation_hop",
            "verifier_identity",
            "verification_decision",
            "audience_resource_binding",
            "represented_authority",
            "downstream_exchange",
            "attenuated_effective_authority",
            "bounded_result",
            "lifecycle_generation",
            "revocation_generation",
            "token_class_control",
            "counterfactual_control",
            "alternative_explanation",
            "evidence_level",
            "evidence_ceiling",
        )
        for scenario in payload["scenarios"]:
            for field in required:
                self.assertIn(field, scenario)
                self.assertIsInstance(scenario[field], str)
                self.assertGreaterEqual(len(scenario[field].strip()), 40)

    def test_skill_is_registered_as_sixteenth_operator_depth_profile(self):
        payload = json.loads(PROFILES.read_text(encoding="utf-8"))
        profiles = payload["profiles"]
        self.assertGreaterEqual(len(profiles), 16)
        matching = [p for p in profiles if p["skill"] == "secrets-and-token-flow-analysis"]
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
