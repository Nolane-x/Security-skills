import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "supply-chain-dependency-review" / "SKILL.md"
RUNBOOK = ROOT / "skills" / "supply-chain-dependency-review" / "references" / "operator-runbook.md"
CASES = ROOT / "skills" / "supply-chain-dependency-review" / "references" / "operator-review-cases.json"
PROFILES = ROOT / "operator-depth" / "profiles.json"


class SupplyChainDependencyDepthTests(unittest.TestCase):
    def test_skill_exposes_causal_supply_chain_model(self):
        text = SKILL.read_text(encoding="utf-8")
        for section in (
            "## Causal supply-chain model",
            "## Dependency and source resolution",
            "## Artifact identity and immutable pinning",
            "## Integrity, signature, and provenance verification",
            "## Build hooks and toolchain identity",
            "## CI trust and cache reuse",
            "## Produced, released, distributed, and deployed artifacts",
            "## Lifecycle and revocation/update generation",
            "## Supply-chain evidence ladder",
            "## Counterfactual proof",
            "## Alternative explanations",
            "## Evidence ceiling",
        ):
            self.assertIn(section, text)

        lower = text.lower()
        for concept in (
            "declared dependency requirement -> source/namespace resolution policy -> selected package/source identity -> immutable version/ref/digest binding -> fetch origin or mirror -> integrity/signature/provenance verification -> install/build hook -> toolchain/build-environment identity -> ci principal/trust context -> cache/reuse input binding -> produced artifact identity -> release/signing/publishing authority -> distributed artifact identity -> deployed/runtime artifact identity -> bounded security-relevant effect -> lifecycle/revocation/update generation",
            "declared dependency != resolved dependency",
            "package name/version != artifact identity",
            "version pin != immutable artifact",
            "checksum match != authorized publisher provenance",
            "signature validity != release-policy authorization",
            "registry namespace != publisher identity",
            "lockfile entry != installed/shipped bytes",
            "source revision != produced artifact identity",
            "build success != hermetic or trusted build",
            "ci execution authority != release/publishing authority",
            "cache hit != trusted build input",
            "released artifact != deployed artifact",
            "sc0",
            "sc1",
            "sc2",
            "sc3",
            "sc4",
            "sc5",
            "counterfactual",
            "evidence ceiling",
        ):
            self.assertIn(concept, lower)

    def test_runbook_requires_transition_level_supply_chain_reasoning(self):
        self.assertTrue(RUNBOOK.is_file(), "supply-chain operator runbook must exist before depth can pass")
        text = RUNBOOK.read_text(encoding="utf-8")
        for section in (
            "## Attack surface",
            "## Hypothesis matrix",
            "## Dependency declaration and graph trace",
            "## Namespace and source-resolution trace",
            "## Artifact identity and immutable-pin trace",
            "## Integrity, signature, and provenance-verifier trace",
            "## Install and build-hook trace",
            "## Toolchain and build-environment trace",
            "## CI principal and trust-boundary trace",
            "## Cache and reuse-input trace",
            "## Produced-artifact identity trace",
            "## Release, signing, and publishing-authority trace",
            "## Distribution and deployment binding",
            "## Lifecycle and revocation/update-generation trace",
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
            "source resolution policy",
            "artifact identity",
            "immutable pin",
            "provenance verifier",
            "build hook",
            "toolchain identity",
            "ci principal",
            "cache/reuse",
            "release authority",
            "distributed artifact",
            "deployed artifact",
            "revocation/update generation",
            "alternative explanation",
            "evidence ceiling",
        ):
            self.assertIn(phrase, lower)

    def test_review_cases_encode_supply_chain_reasoning(self):
        self.assertTrue(CASES.is_file(), "supply-chain review-case matrix must exist before depth can pass")
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
            "declared_requirement",
            "source_resolution_policy",
            "selected_namespace_source",
            "selected_artifact_identity",
            "immutable_pin_integrity_state",
            "provenance_verifier_decision",
            "install_build_hook",
            "toolchain_build_environment",
            "ci_principal_trust_context",
            "cache_reuse_input_binding",
            "produced_artifact_identity",
            "release_signing_publishing_authority",
            "distributed_artifact_identity",
            "deployed_runtime_artifact_identity",
            "bounded_effect",
            "lifecycle_revocation_update_generation",
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

    def test_skill_is_registered_as_eighteenth_operator_depth_profile(self):
        payload = json.loads(PROFILES.read_text(encoding="utf-8"))
        profiles = payload["profiles"]
        self.assertGreaterEqual(len(profiles), 18)
        matching = [p for p in profiles if p["skill"] == "supply-chain-dependency-review"]
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
