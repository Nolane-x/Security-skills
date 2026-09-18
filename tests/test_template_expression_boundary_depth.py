import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "template-expression-boundary-analysis" / "SKILL.md"
RUNBOOK = ROOT / "skills" / "template-expression-boundary-analysis" / "references" / "operator-runbook.md"
CASES = ROOT / "skills" / "template-expression-boundary-analysis" / "references" / "operator-review-cases.json"
PROFILES = ROOT / "operator-depth" / "profiles.json"


class TemplateExpressionBoundaryDepthTests(unittest.TestCase):
    def test_skill_exposes_causal_template_expression_model(self):
        text = SKILL.read_text(encoding="utf-8")
        for section in (
            "## Causal template-expression model",
            "## Principal, transaction, source, and data generations",
            "## Data-to-source construction binding",
            "## Compile, cache, and source-trust binding",
            "## Evaluation context, helper, and object-graph binding",
            "## Include, import, inheritance, and nested evaluation lineage",
            "## Escaping, output context, and downstream interpretation binding",
            "## Template-expression evidence ladder",
            "## Counterfactual template-expression controls",
            "## Alternative explanations",
            "## Evidence ceiling",
        ):
            self.assertIn(section, text)

        lower = text.lower()
        for concept in (
            "principal/tenant identity",
            "request/render transaction identity/generation",
            "template ownership/trust class",
            "template source identity/generation",
            "data/value identity/generation",
            "source-construction transform identity/generation",
            "parser/compiler identity/version",
            "compiled template/expression identity/generation",
            "expression node/source-position identity",
            "evaluation context identity/generation",
            "lexical/environment scope generation",
            "helper/function registry identity/generation",
            "object-graph root identity/generation",
            "sandbox/evaluation policy identity/generation",
            "escaping/output-context identity/generation",
            "include/import/inheritance identity/generation",
            "compiled-cache key/entry generation",
            "final evaluator identity",
            "evaluation result",
            "downstream renderer/consumer identity",
            "effective expression-boundary capability",
            "bounded result",
            "receipt/result",
            "template source control != plain data control",
            "expression source control != variable-value control",
            "expression evaluation != injection",
            "intended user-authored templating != unauthorized source promotion",
            "string interpolation != source promotion by itself",
            "escaping failure != expression evaluation",
            "expression syntax accepted != expression executed",
            "compilation success != evaluation",
            "evaluation result != boundary escape",
            "helper registered != helper reachable from this context",
            "helper reachable != unsafe capability",
            "object graph reachable != sandbox escape",
            "denied capability probe != complete confinement",
            "sandbox escape primitive != arbitrary host execution",
            "arithmetic/string marker evaluation != code execution",
            "template error != exploitability",
            "reflected expression text != evaluation",
            "autoescape disabled != source-code boundary failure by itself",
            "safe-string/trusted-markup marker != trusted template source by assumption",
            "trusted parent template != trusted child/include by inheritance",
            "include/import path != canonical resolved resource identity",
            "same template name != same source generation",
            "same compiled cache key != same trust/policy generation",
            "cache hit != current helper/sandbox policy generation",
            "helper registry mutation != current compiled template awareness by assumption",
            "tenant-owned template != cross-tenant template authority",
            "renderer output != downstream active interpretation by assumption",
            "local benign policy mismatch != production exploitability",
            "teb0",
            "teb1",
            "teb2",
            "teb3",
            "teb4",
            "teb5",
            "counterfactual",
            "alternative explanation",
            "evidence ceiling",
            "local/owned/sandboxed",
        ):
            self.assertIn(concept, lower)

    def test_runbook_requires_template_expression_generation_reasoning(self):
        self.assertTrue(RUNBOOK.is_file(), "template-expression operator runbook must exist before depth can pass")
        text = RUNBOOK.read_text(encoding="utf-8")
        for section in (
            "## Attack surface",
            "## Hypothesis matrix",
            "## Principal/source/data-generation trace",
            "## Data-to-source construction trace",
            "## Compile/cache/source-trust trace",
            "## Evaluation-context/helper/object-graph trace",
            "## Include/import/inheritance trace",
            "## Escaping/output-context/downstream trace",
            "## Controlled validation",
            "## False-positive controls",
            "## Counterfactual template-expression controls",
            "## Alternative explanations",
            "## Evidence capture",
            "## Evidence promotion and ceiling",
            "## Remediation checks",
        ):
            self.assertIn(section, text)

        lower = text.lower()
        for phrase in (
            "template source",
            "data generation",
            "source promotion",
            "compiled artifact",
            "cache entry",
            "trust class",
            "evaluation context",
            "helper registry",
            "object graph",
            "sandbox policy",
            "include",
            "inheritance",
            "escaping",
            "synthetic",
            "mock",
            "read-only",
            "counterfactual",
            "alternative explanation",
            "evidence ceiling",
            "teb5",
        ):
            self.assertIn(phrase, lower)

    def test_review_cases_encode_template_expression_reasoning(self):
        self.assertTrue(CASES.is_file(), "template-expression review-case matrix must exist before depth can pass")
        payload = json.loads(CASES.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 1)
        self.assertGreaterEqual(len(payload["scenarios"]), 4)

        required_ids = {
            "data-concatenation-reparsed-as-expression-source",
            "compiled-template-cache-reused-after-policy-generation-change",
            "trusted-parent-includes-lower-trust-child-as-source",
            "helper-registry-generation-exposes-new-synthetic-capability",
        }
        self.assertTrue(required_ids.issubset({scenario["id"] for scenario in payload["scenarios"]}))

        required = (
            "hypothesis",
            "safe_oracle",
            "positive_control",
            "negative_control",
            "stop_condition",
            "remediation_oracle",
            "principal_source_data_generation",
            "data_to_source_construction",
            "compile_cache_source_trust",
            "evaluation_context_helper_object_graph",
            "include_import_inheritance_lineage",
            "escaping_output_downstream_state",
            "downstream_consumer_identity",
            "effective_template_expression_capability",
            "bounded_result",
            "receipt_result_binding",
            "counterfactual_control",
            "alternative_explanation",
            "evidence_level",
            "evidence_ceiling",
        )
        safe_terms = ("synthetic", "mock", "inert", "read-only", "controlled", "fake", "local", "shadow")
        for scenario in payload["scenarios"]:
            for field in required:
                self.assertIn(field, scenario)
                self.assertIsInstance(scenario[field], str)
                self.assertGreaterEqual(len(scenario[field].strip()), 40)
            self.assertTrue(any(term in scenario["safe_oracle"].lower() for term in safe_terms))
            self.assertTrue(any(term in scenario["stop_condition"].lower() for term in ("stop", "abort", "do not proceed")))
            self.assertRegex(scenario["evidence_level"], r"\bTEB[0-5]\b")
            self.assertRegex(scenario["evidence_ceiling"], r"\bTEB[0-5]\b")

    def test_skill_is_registered_as_thirty_seventh_operator_depth_profile(self):
        payload = json.loads(PROFILES.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 2)
        profiles = payload["profiles"]
        self.assertEqual(len(profiles), 37)
        matching = [p for p in profiles if p["skill"] == "template-expression-boundary-analysis"]
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
