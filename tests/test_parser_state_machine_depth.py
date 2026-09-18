import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "parser-state-machine-analysis" / "SKILL.md"
RUNBOOK = ROOT / "skills" / "parser-state-machine-analysis" / "references" / "operator-runbook.md"
CASES = ROOT / "skills" / "parser-state-machine-analysis" / "references" / "operator-review-cases.json"
PROFILES = ROOT / "operator-depth" / "profiles.json"


class ParserStateMachineDepthTests(unittest.TestCase):
    def test_skill_exposes_causal_parser_state_model(self):
        text = SKILL.read_text(encoding="utf-8")
        for section in (
            "## Causal parser-state model",
            "## Parser, input, phase, and state generations",
            "## Transition and invariant binding",
            "## Structural metadata and semantic-object binding",
            "## Error recovery and deferred-validation binding",
            "## Nested parser and cross-record provenance",
            "## Downstream consumer and bounded semantic effect",
            "## Parser-state evidence ladder",
            "## Counterfactual parser controls",
            "## Alternative explanations",
            "## Evidence ceiling",
        ):
            self.assertIn(section, text)

        lower = text.lower()
        for concept in (
            "input artifact identity",
            "input generation",
            "parser instance identity",
            "parser configuration/version",
            "phase identity",
            "state generation",
            "transition identity",
            "token/record identity",
            "semantic object identity",
            "semantic object generation",
            "invariant expected",
            "invariant observed",
            "recovery/deferred-validation state",
            "downstream consumer identity",
            "effective semantic capability",
            "bounded result",
            "receipt/result",
            "malformed input != parser vulnerability",
            "parse acceptance != semantic acceptance",
            "parser crash != exploitability",
            "harness crash != parser crash",
            "phase reach != invariant violation",
            "duplicate record != duplicate semantic effect",
            "warning/recovery != successful validation",
            "deferred validation != omitted validation",
            "outer length mismatch != out-of-bounds access",
            "integer wrap != security consequence",
            "overlapping regions != harmful aliasing",
            "forward reference != dangling reference",
            "partial object != privileged semantic object",
            "state divergence != downstream dangerous consumption",
            "grammar mismatch != parser-state bug",
            "minimized crash != same causal phase path",
            "ps0",
            "ps1",
            "ps2",
            "ps3",
            "ps4",
            "ps5",
            "counterfactual",
            "alternative explanation",
            "evidence ceiling",
            "local/owned/sandboxed",
        ):
            self.assertIn(concept, lower)

    def test_runbook_requires_transition_level_parser_reasoning(self):
        self.assertTrue(RUNBOOK.is_file(), "parser-state operator runbook must exist before depth can pass")
        text = RUNBOOK.read_text(encoding="utf-8")
        for section in (
            "## Attack surface",
            "## Hypothesis matrix",
            "## Parser/input/phase-generation trace",
            "## Transition and invariant trace",
            "## Structural metadata and semantic-object trace",
            "## Error-recovery and deferred-validation trace",
            "## Nested parser and cross-record trace",
            "## Downstream consumer and bounded-effect trace",
            "## Controlled validation",
            "## False-positive controls",
            "## Counterfactual parser controls",
            "## Alternative explanations",
            "## Evidence capture",
            "## Evidence promotion and ceiling",
            "## Remediation checks",
        ):
            self.assertIn(section, text)

        lower = text.lower()
        for phrase in (
            "input generation",
            "parser instance",
            "phase generation",
            "state generation",
            "transition identity",
            "invariant",
            "semantic object",
            "error recovery",
            "deferred validation",
            "nested parser",
            "cross-record",
            "downstream consumer",
            "synthetic",
            "mock",
            "read-only",
            "counterfactual",
            "alternative explanation",
            "evidence ceiling",
            "ps5",
        ):
            self.assertIn(phrase, lower)

    def test_review_cases_encode_parser_state_reasoning(self):
        self.assertTrue(CASES.is_file(), "parser-state review-case matrix must exist before depth can pass")
        payload = json.loads(CASES.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 1)
        self.assertGreaterEqual(len(payload["scenarios"]), 4)

        required_ids = {
            "recovery-state-trust-promotion",
            "duplicate-record-semantic-selection",
            "nested-length-phase-drift",
            "deferred-reference-resolution-generation",
        }
        self.assertTrue(required_ids.issubset({scenario["id"] for scenario in payload["scenarios"]}))

        required = (
            "hypothesis",
            "safe_oracle",
            "positive_control",
            "negative_control",
            "stop_condition",
            "remediation_oracle",
            "parser_input_phase_generation",
            "transition_invariant_trace",
            "structural_metadata_semantic_object",
            "recovery_deferred_validation_state",
            "nested_cross_record_provenance",
            "downstream_consumer_identity",
            "effective_semantic_capability",
            "bounded_result",
            "receipt_result_binding",
            "counterfactual_control",
            "alternative_explanation",
            "evidence_level",
            "evidence_ceiling",
        )
        safe_terms = ("synthetic", "mock", "inert", "read-only", "controlled")
        for scenario in payload["scenarios"]:
            for field in required:
                self.assertIn(field, scenario)
                self.assertIsInstance(scenario[field], str)
                self.assertGreaterEqual(len(scenario[field].strip()), 40)
            self.assertTrue(any(term in scenario["safe_oracle"].lower() for term in safe_terms))
            self.assertTrue(any(term in scenario["stop_condition"].lower() for term in ("stop", "abort", "do not proceed")))
            self.assertRegex(scenario["evidence_level"], r"\bPS[0-5]\b")
            self.assertRegex(scenario["evidence_ceiling"], r"\bPS[0-5]\b")

    def test_skill_is_registered_as_twenty_eighth_operator_depth_profile(self):
        payload = json.loads(PROFILES.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 2)
        profiles = payload["profiles"]
        self.assertGreaterEqual(len(profiles), 28)
        matching = [p for p in profiles if p["skill"] == "parser-state-machine-analysis"]
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
