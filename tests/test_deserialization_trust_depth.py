import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "deserialization-trust-analysis" / "SKILL.md"
RUNBOOK = ROOT / "skills" / "deserialization-trust-analysis" / "references" / "operator-runbook.md"
CASES = ROOT / "skills" / "deserialization-trust-analysis" / "references" / "operator-review-cases.json"
PROFILES = ROOT / "operator-depth" / "profiles.json"


class DeserializationTrustDepthTests(unittest.TestCase):
    def test_skill_exposes_causal_reconstruction_trust_model(self):
        text = SKILL.read_text(encoding="utf-8")
        for section in (
            "## Causal reconstruction-trust model",
            "## Reconstruction identity and type binding",
            "## Construction, hooks, and secondary interpretation",
            "## Authenticity and reconstructed authority",
            "## Lifecycle and generation reasoning",
            "## Deserialization evidence ladder",
            "## Counterfactual proof",
            "## Alternative explanations",
            "## Evidence ceiling",
        ):
            self.assertIn(section, text)

        lower = text.lower()
        for concept in (
            "serialized artifact origin -> transport/storage envelope identity -> authenticity/integrity context -> format/parser identity -> syntax and canonical field state -> schema identity and schema version -> discriminator/variant state -> type registry/resolver identity and registry generation -> resolved runtime type identity -> object construction path and object-graph identity -> constructor/setter/post-load hook state -> secondary interpretation state -> caller/request authority context -> requested reconstructed capability -> policy/allowlist decision -> effective reconstructed authority -> privileged consumer or behavior boundary -> bounded synthetic effect -> receipt/result binding -> schema/registry/object lifecycle generation",
            "parser acceptance != schema authorization",
            "schema validation != runtime type authorization",
            "discriminator/alias string != resolved runtime type identity",
            "payload authenticity != capability authorization",
            "object construction != side-effect authorization",
            "constructor/hook reachability != security impact",
            "data field != later secondary interpretation",
            "current schema/registry/object generation != stale generation",
            "unexpected type selection != exploitability",
            "dt0",
            "dt1",
            "dt2",
            "dt3",
            "dt4",
            "dt5",
            "counterfactual",
            "evidence ceiling",
        ):
            self.assertIn(concept, lower)

    def test_runbook_requires_transition_level_deserialization_reasoning(self):
        self.assertTrue(RUNBOOK.is_file(), "deserialization operator runbook must exist before depth can pass")
        text = RUNBOOK.read_text(encoding="utf-8")
        for section in (
            "## Attack surface",
            "## Hypothesis matrix",
            "## Artifact origin and authenticity trace",
            "## Parser and canonical-field trace",
            "## Schema identity and version trace",
            "## Discriminator and registry-resolution trace",
            "## Runtime type and object-construction trace",
            "## Hook/callback and secondary-interpretation trace",
            "## Authority and reconstruction-policy trace",
            "## Privileged-consumer and result trace",
            "## Lifecycle/schema/registry generation trace",
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
            "registry generation",
            "schema version",
            "runtime type identity",
            "secondary interpretation",
            "reconstructed authority",
            "receipt/result",
            "inert callback",
            "data-only",
            "debug-only",
            "alternative explanation",
            "evidence ceiling",
        ):
            self.assertIn(phrase, lower)

    def test_review_cases_encode_reconstruction_trust_reasoning(self):
        self.assertTrue(CASES.is_file(), "deserialization review-case matrix must exist before depth can pass")
        payload = json.loads(CASES.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 1)
        self.assertGreaterEqual(len(payload["scenarios"]), 3)
        required_ids = {
            "type-registry-binding",
            "construction-hook-capability-binding",
            "schema-registry-generation-binding",
        }
        self.assertTrue(required_ids.issubset({scenario["id"] for scenario in payload["scenarios"]}))
        required = (
            "hypothesis",
            "safe_oracle",
            "positive_control",
            "negative_control",
            "stop_condition",
            "remediation_oracle",
            "artifact_origin",
            "envelope_authentication_context",
            "format_parser_identity",
            "canonical_field_state",
            "schema_identity_version",
            "discriminator_state",
            "registry_resolver_identity",
            "registry_generation",
            "runtime_type_identity",
            "object_construction_path",
            "hook_callback_surface",
            "secondary_interpretation",
            "authority_context",
            "requested_reconstructed_capability",
            "policy_decision",
            "effective_reconstructed_authority",
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
            self.assertRegex(scenario["evidence_level"], r"\bDT[0-5]\b")
            self.assertRegex(scenario["evidence_ceiling"], r"\bDT[0-5]\b")

    def test_skill_is_registered_as_twentieth_operator_depth_profile(self):
        payload = json.loads(PROFILES.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 2)
        profiles = payload["profiles"]
        self.assertGreaterEqual(len(profiles), 20)
        matching = [p for p in profiles if p["skill"] == "deserialization-trust-analysis"]
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
