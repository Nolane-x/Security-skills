import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "type-confusion-analysis" / "SKILL.md"
RUNBOOK = ROOT / "skills" / "type-confusion-analysis" / "references" / "operator-runbook.md"
CASES = ROOT / "skills" / "type-confusion-analysis" / "references" / "operator-review-cases.json"
PROFILES = ROOT / "operator-depth" / "profiles.json"


class TypeConfusionDepthTests(unittest.TestCase):
    def test_skill_exposes_causal_type_confusion_model(self):
        text = SKILL.read_text(encoding="utf-8")
        for section in (
            "## Causal type-confusion model",
            "## Object, storage, and type generations",
            "## Type-identity source and transition binding",
            "## Cast, downcast, and validator binding",
            "## Representation, layout, and active-member binding",
            "## Consumer interpretation and bounded effect",
            "## Type-confusion evidence ladder",
            "## Counterfactual type controls",
            "## Alternative explanations",
            "## Evidence ceiling",
        ):
            self.assertIn(section, text)

        lower = text.lower()
        for concept in (
            "logical object identity",
            "object/storage generation",
            "logical type identity",
            "actual dynamic type identity",
            "type-identity mechanism",
            "type-identity generation",
            "representation/layout identity",
            "representation generation",
            "producer/transition identity",
            "cast/downcast/variant transition",
            "validator/check identity",
            "validator generation",
            "consumer identity",
            "interpreted type",
            "field/dispatch/operation identity",
            "actual storage member/field identity",
            "type/layout expectation",
            "observed interpretation",
            "effective wrong-type capability",
            "bounded result",
            "receipt/result",
            "cast exists != type confusion",
            "unchecked cast != wrong dynamic type",
            "failed cast != unsafe interpretation",
            "stale tag != stale payload",
            "tag mismatch != wrong-field access",
            "wrong logical type != memory corruption",
            "different representation != invalid interpretation when layouts are compatible by contract",
            "shared prefix != whole-object type equivalence",
            "union member switch != stale-member use",
            "discriminator change != active-member transition",
            "vtable/class pointer change != valid object transition",
            "handle value reuse != type confusion without table/type-generation mismatch",
            "object reuse != type confusion without current-lifetime identity mismatch",
            "shape/map change != wrong payload interpretation",
            "polymorphic dispatch != wrong dispatch",
            "debug metadata mismatch != runtime type confusion",
            "sanitizer type report != exploitability",
            "assertion failure != wrong-type capability",
            "wrong-field interpretation != arbitrary code execution",
            "wrong dispatch class != control-flow hijack",
            "corrupted type metadata != logic-created confusion",
            "same bit pattern != same semantic type",
            "nominal type != current dynamic type",
            "parser tag != current runtime type unless reconstruction binding is proven",
            "tcf0",
            "tcf1",
            "tcf2",
            "tcf3",
            "tcf4",
            "tcf5",
            "counterfactual",
            "alternative explanation",
            "evidence ceiling",
            "local/owned/sandboxed",
        ):
            self.assertIn(concept, lower)

    def test_runbook_requires_type_identity_reasoning(self):
        self.assertTrue(RUNBOOK.is_file(), "type-confusion operator runbook must exist before depth can pass")
        text = RUNBOOK.read_text(encoding="utf-8")
        for section in (
            "## Attack surface",
            "## Hypothesis matrix",
            "## Object/storage/type-generation trace",
            "## Type-identity and transition trace",
            "## Cast/downcast/validator trace",
            "## Representation/layout/active-member trace",
            "## Consumer interpretation/bounded-effect trace",
            "## Controlled validation",
            "## False-positive controls",
            "## Counterfactual type controls",
            "## Alternative explanations",
            "## Evidence capture",
            "## Evidence promotion and ceiling",
            "## Remediation checks",
        ):
            self.assertIn(section, text)

        lower = text.lower()
        for phrase in (
            "dynamic type",
            "type-identity generation",
            "storage generation",
            "active member",
            "downcast",
            "validator",
            "representation",
            "layout",
            "wrong-field",
            "dispatch",
            "synthetic",
            "fake",
            "mock",
            "read-only",
            "shadow",
            "counterfactual",
            "alternative explanation",
            "evidence ceiling",
            "tcf5",
        ):
            self.assertIn(phrase, lower)

    def test_review_cases_encode_type_confusion_reasoning(self):
        self.assertTrue(CASES.is_file(), "type-confusion review-case matrix must exist before depth can pass")
        payload = json.loads(CASES.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 1)
        self.assertGreaterEqual(len(payload["scenarios"]), 4)

        required_ids = {
            "stale-discriminant-after-union-transition",
            "handle-slot-type-generation-reuse",
            "unchecked-downcast-dynamic-type-mismatch",
            "shape-payload-generation-skew",
        }
        self.assertTrue(required_ids.issubset({scenario["id"] for scenario in payload["scenarios"]}))

        required = (
            "hypothesis",
            "safe_oracle",
            "positive_control",
            "negative_control",
            "stop_condition",
            "remediation_oracle",
            "object_storage_type_generation",
            "type_identity_transition_trace",
            "cast_downcast_validator_state",
            "representation_layout_active_member",
            "consumer_interpretation",
            "downstream_consumer_identity",
            "effective_wrong_type_capability",
            "bounded_result",
            "receipt_result_binding",
            "counterfactual_control",
            "alternative_explanation",
            "evidence_level",
            "evidence_ceiling",
        )
        safe_terms = ("synthetic", "mock", "inert", "read-only", "controlled", "fake", "shadow")
        for scenario in payload["scenarios"]:
            for field in required:
                self.assertIn(field, scenario)
                self.assertIsInstance(scenario[field], str)
                self.assertGreaterEqual(len(scenario[field].strip()), 40)
            self.assertTrue(any(term in scenario["safe_oracle"].lower() for term in safe_terms))
            self.assertTrue(any(term in scenario["stop_condition"].lower() for term in ("stop", "abort", "do not proceed")))
            self.assertRegex(scenario["evidence_level"], r"\bTCF[0-5]\b")
            self.assertRegex(scenario["evidence_ceiling"], r"\bTCF[0-5]\b")

    def test_skill_is_registered_as_thirty_first_operator_depth_profile(self):
        payload = json.loads(PROFILES.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 2)
        profiles = payload["profiles"]
        self.assertGreaterEqual(len(profiles), 31)
        matching = [p for p in profiles if p["skill"] == "type-confusion-analysis"]
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
