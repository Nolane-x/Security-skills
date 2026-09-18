import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "nonce-and-randomness-lifecycle-analysis" / "SKILL.md"
RUNBOOK = ROOT / "skills" / "nonce-and-randomness-lifecycle-analysis" / "references" / "operator-runbook.md"
CASES = ROOT / "skills" / "nonce-and-randomness-lifecycle-analysis" / "references" / "operator-review-cases.json"
PROFILES = ROOT / "operator-depth" / "profiles.json"


class NonceRandomnessLifecycleDepthTests(unittest.TestCase):
    def test_skill_exposes_causal_randomness_lifecycle_model(self):
        text = SKILL.read_text(encoding="utf-8")
        for section in (
            "## Causal randomness-lifecycle model",
            "## Value class, property, and security-scope binding",
            "## Generator, seed, entropy, and reseed generations",
            "## Fork, snapshot, restart, and clone lifecycle",
            "## Counter, namespace, reservation, and concurrency binding",
            "## Persistence and crash/restart binding",
            "## Transform, encoding, and truncation binding",
            "## Consumer/construction and bounded consequence binding",
            "## Randomness-lifecycle evidence ladder",
            "## Counterfactual randomness controls",
            "## Alternative explanations",
            "## Evidence ceiling",
        ):
            self.assertIn(section, text)

        lower = text.lower()
        for concept in (
            "value class",
            "required security property",
            "security scope identity",
            "key/session/device/tenant identity",
            "generator implementation identity/version",
            "generator instance identity/generation",
            "generator state identity/generation",
            "entropy source identity",
            "seed material identity/generation",
            "reseed epoch",
            "process/runtime identity/generation",
            "fork/snapshot/restart identity/generation",
            "counter namespace identity",
            "counter/reservation generation",
            "allocation/synchronization identity",
            "persistence checkpoint identity/generation",
            "raw generated value identity",
            "raw value generation",
            "transform/encoding/truncation identity",
            "final consumed value identity",
            "consumer/cryptographic construction identity",
            "duplicate/reuse/collision relation",
            "effective randomness-lifecycle capability",
            "bounded result",
            "receipt/result",
            "duplicate value != vulnerability without a non-repetition requirement in the same security scope",
            "repeated nonce under different independent keys != same-key nonce reuse by assumption",
            "predictability != repetition",
            "repetition != predictability",
            "statistical bias != practical prediction",
            "small-sample duplicate absence != uniqueness proof",
            "small-sample collision != generator-wide collision-rate proof",
            "rng api name != actual entropy/state provenance",
            "deterministic generator != insecure generator when deterministic behavior is the intended contract",
            "fixed seed in a test fixture != production seed reuse",
            "forked process != cloned output stream when child diversification/reseed is proven",
            "snapshot restore != nonce reuse when generation/domain separation changes",
            "restart state reset != security failure when scope intentionally resets with a new independent key/session",
            "counter reset != duplicate consumed value when namespace/key generation changes",
            "counter wrap possibility != observed wrap within an affected scope",
            "concurrent callers != collision without shared allocator/state evidence",
            "reservation overlap != duplicate consumption unless overlapping ranges are actually consumed",
            "timestamp input != predictability proof",
            "low entropy estimate != recovered/predicted value by itself",
            "raw rng duplicate != final-value duplicate when transforms include unique domain data",
            "final display-id collision != security-token collision when a distinct full value governs security",
            "truncation != dangerous collision until consumed security domain and width are bound",
            "encoding alias != duplicate underlying random value by assumption",
            "same salt != unsafe nonce reuse",
            "same iv != nonce misuse unless the primitive/mode requires uniqueness or unpredictability under the bound key",
            "sequence-number reuse != cryptographic nonce reuse unless construction binding is proven",
            "nonce reuse observation != cryptographic exploitability",
            "token duplication != token authority confusion without consumer binding",
            "crash != randomness-lifecycle failure",
            "nrl0",
            "nrl1",
            "nrl2",
            "nrl3",
            "nrl4",
            "nrl5",
            "counterfactual",
            "alternative explanation",
            "evidence ceiling",
            "local/owned/sandboxed",
        ):
            self.assertIn(concept, lower)

    def test_runbook_requires_generator_lifecycle_reasoning(self):
        self.assertTrue(RUNBOOK.is_file(), "nonce/randomness operator runbook must exist before depth can pass")
        text = RUNBOOK.read_text(encoding="utf-8")
        for section in (
            "## Attack surface",
            "## Hypothesis matrix",
            "## Value/property/security-scope trace",
            "## Generator/seed/entropy/reseed trace",
            "## Fork/snapshot/restart lifecycle trace",
            "## Counter/namespace/reservation trace",
            "## Persistence/crash-restart trace",
            "## Transform/encoding/truncation trace",
            "## Consumer/construction trace",
            "## Controlled validation",
            "## False-positive controls",
            "## Counterfactual randomness controls",
            "## Alternative explanations",
            "## Evidence capture",
            "## Evidence promotion and ceiling",
            "## Remediation checks",
        ):
            self.assertIn(section, text)

        lower = text.lower()
        for phrase in (
            "security scope",
            "required property",
            "generator state generation",
            "seed generation",
            "reseed epoch",
            "fork",
            "snapshot",
            "restart",
            "counter namespace",
            "reservation",
            "persistence checkpoint",
            "truncation",
            "final consumed value",
            "synthetic",
            "fake",
            "mock",
            "in-memory",
            "counterfactual",
            "alternative explanation",
            "evidence ceiling",
            "nrl5",
        ):
            self.assertIn(phrase, lower)

    def test_review_cases_encode_randomness_lifecycle_reasoning(self):
        self.assertTrue(CASES.is_file(), "nonce/randomness review-case matrix must exist before depth can pass")
        payload = json.loads(CASES.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 1)
        self.assertGreaterEqual(len(payload["scenarios"]), 4)

        required_ids = {
            "fork-cloned-generator-state-reuse",
            "restart-counter-persistence-reset",
            "concurrent-counter-reservation-overlap",
            "truncation-encoding-domain-collapse",
        }
        self.assertTrue(required_ids.issubset({scenario["id"] for scenario in payload["scenarios"]}))

        required = (
            "hypothesis",
            "safe_oracle",
            "positive_control",
            "negative_control",
            "stop_condition",
            "remediation_oracle",
            "value_property_security_scope",
            "generator_seed_entropy_reseed",
            "fork_snapshot_restart_lifecycle",
            "counter_namespace_reservation",
            "persistence_crash_restart",
            "transform_encoding_truncation",
            "consumer_construction_identity",
            "effective_randomness_lifecycle_capability",
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
            self.assertRegex(scenario["evidence_level"], r"\bNRL[0-5]\b")
            self.assertRegex(scenario["evidence_ceiling"], r"\bNRL[0-5]\b")

    def test_skill_is_registered_as_thirty_fourth_operator_depth_profile(self):
        payload = json.loads(PROFILES.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 2)
        profiles = payload["profiles"]
        self.assertGreaterEqual(len(profiles), 34)
        matching = [p for p in profiles if p["skill"] == "nonce-and-randomness-lifecycle-analysis"]
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
