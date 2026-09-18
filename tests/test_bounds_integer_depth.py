import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "bounds-and-integer-analysis" / "SKILL.md"
RUNBOOK = ROOT / "skills" / "bounds-and-integer-analysis" / "references" / "operator-runbook.md"
CASES = ROOT / "skills" / "bounds-and-integer-analysis" / "references" / "operator-review-cases.json"
PROFILES = ROOT / "operator-depth" / "profiles.json"


class BoundsIntegerDepthTests(unittest.TestCase):
    def test_skill_exposes_causal_bounds_integer_model(self):
        text = SKILL.read_text(encoding="utf-8")
        for section in (
            "## Causal bounds-and-integer model",
            "## Value identity, units, and representation generations",
            "## Arithmetic expression and conversion binding",
            "## Check-domain and use-domain binding",
            "## Allocation, object, region, and usable-size binding",
            "## Index, offset, stride, and access-width binding",
            "## Aggregate, alignment, and nested-size arithmetic",
            "## Bounds-and-integer evidence ladder",
            "## Counterfactual arithmetic controls",
            "## Alternative explanations",
            "## Evidence ceiling",
        ):
            self.assertIn(section, text)

        lower = text.lower()
        for concept in (
            "source value identity",
            "source generation",
            "source units",
            "mathematical value",
            "representation/type chain",
            "width/signedness",
            "cast/promotion/truncation",
            "arithmetic expression identity",
            "arithmetic generation",
            "check-domain value",
            "check predicate",
            "allocation/object identity",
            "object generation",
            "usable size",
            "index/offset identity",
            "access width",
            "access range equation",
            "final consumer identity",
            "effective invalid-range capability",
            "bounded result",
            "receipt/result",
            "suspicious cast != integer vulnerability",
            "integer overflow != out-of-bounds access",
            "truncation != undersized allocation",
            "signed-to-unsigned conversion != huge allocation",
            "negative value != invalid range until representation and use are bound",
            "check passes != access safe",
            "allocation succeeds != allocation is large enough",
            "allocation failure != memory corruption",
            "large allocation != integer overflow",
            "outer length mismatch != invalid access",
            "one-past-end pointer formation != out-of-bounds dereference",
            "different units != unit confusion when conversion is correct",
            "alignment rounding != overflow unless the rounded representation diverges",
            "object size != usable payload size",
            "sanitizer report != exploitability",
            "undefined or implementation-defined arithmetic != demonstrated security effect",
            "dead-code wraparound != reachable vulnerability",
            "invalid arithmetic != attacker-controlled arithmetic",
            "arithmetic divergence != downstream dangerous consumption",
            "bnd0",
            "bnd1",
            "bnd2",
            "bnd3",
            "bnd4",
            "bnd5",
            "counterfactual",
            "alternative explanation",
            "evidence ceiling",
            "local/owned/sandboxed",
        ):
            self.assertIn(concept, lower)

    def test_runbook_requires_arithmetic_range_reasoning(self):
        self.assertTrue(RUNBOOK.is_file(), "bounds/integer operator runbook must exist before depth can pass")
        text = RUNBOOK.read_text(encoding="utf-8")
        for section in (
            "## Attack surface",
            "## Hypothesis matrix",
            "## Value/unit/representation trace",
            "## Arithmetic and conversion trace",
            "## Check-domain versus use-domain trace",
            "## Allocation/object/usable-size trace",
            "## Index/offset/stride/access-width trace",
            "## Aggregate/alignment/nested-size trace",
            "## Controlled validation",
            "## False-positive controls",
            "## Counterfactual arithmetic controls",
            "## Alternative explanations",
            "## Evidence capture",
            "## Evidence promotion and ceiling",
            "## Remediation checks",
        ):
            self.assertIn(section, text)

        lower = text.lower()
        for phrase in (
            "mathematical value",
            "source units",
            "signedness",
            "truncation",
            "overflow",
            "check-domain",
            "use-domain",
            "usable size",
            "access width",
            "alignment",
            "synthetic",
            "fake",
            "shadow",
            "read-only",
            "counterfactual",
            "alternative explanation",
            "evidence ceiling",
            "bnd5",
        ):
            self.assertIn(phrase, lower)

    def test_review_cases_encode_bounds_integer_reasoning(self):
        self.assertTrue(CASES.is_file(), "bounds/integer review-case matrix must exist before depth can pass")
        payload = json.loads(CASES.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 1)
        self.assertGreaterEqual(len(payload["scenarios"]), 4)

        required_ids = {
            "multiply-truncate-underallocation",
            "signed-negative-to-unsigned-range",
            "alignment-rounding-wrap",
            "inclusive-end-access-width-mismatch",
        }
        self.assertTrue(required_ids.issubset({scenario["id"] for scenario in payload["scenarios"]}))

        required = (
            "hypothesis",
            "safe_oracle",
            "positive_control",
            "negative_control",
            "stop_condition",
            "remediation_oracle",
            "value_unit_representation_trace",
            "arithmetic_conversion_trace",
            "check_use_domain_binding",
            "allocation_object_usable_size",
            "index_offset_stride_access_width",
            "aggregate_alignment_nested_size",
            "downstream_consumer_identity",
            "effective_invalid_range_capability",
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
            self.assertRegex(scenario["evidence_level"], r"\bBND[0-5]\b")
            self.assertRegex(scenario["evidence_ceiling"], r"\bBND[0-5]\b")

    def test_skill_is_registered_as_thirtieth_operator_depth_profile(self):
        payload = json.loads(PROFILES.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 2)
        profiles = payload["profiles"]
        self.assertGreaterEqual(len(profiles), 30)
        matching = [p for p in profiles if p["skill"] == "bounds-and-integer-analysis"]
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
