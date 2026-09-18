import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "jit-invariant-analysis" / "SKILL.md"
RUNBOOK = ROOT / "skills" / "jit-invariant-analysis" / "references" / "operator-runbook.md"
CASES = ROOT / "skills" / "jit-invariant-analysis" / "references" / "operator-review-cases.json"
PROFILES = ROOT / "operator-depth" / "profiles.json"


class JITInvariantDepthTests(unittest.TestCase):
    def test_skill_exposes_causal_jit_invariant_model(self):
        text = SKILL.read_text(encoding="utf-8")
        for section in (
            "## Causal JIT-invariant model",
            "## Runtime, program, tier, and compilation generations",
            "## Feedback, speculation, and dependency binding",
            "## Guard, invalidation, and optimization-transform binding",
            "## OSR, inlining, and specialization binding",
            "## Deoptimization and frame-state reconstruction binding",
            "## Baseline/reference and semantic-consumer binding",
            "## JIT-invariant evidence ladder",
            "## Counterfactual JIT controls",
            "## Alternative explanations",
            "## Evidence ceiling",
        ):
            self.assertIn(section, text)

        lower = text.lower()
        for concept in (
            "runtime/build identity",
            "language/specification semantics",
            "program/input identity/generation",
            "compilation unit/function identity",
            "execution tier identity/generation",
            "optimized code identity/generation",
            "optimization pipeline/pass identity",
            "feedback/profile identity/generation",
            "speculative invariant identity",
            "assumption/dependency generation",
            "guard/check identity",
            "invalidation/watchpoint identity/generation",
            "osr/inlining/specialization state",
            "representation state",
            "side-effect/alias state",
            "deopt trigger identity",
            "deopt metadata/frame-state generation",
            "baseline/reference result",
            "optimized result",
            "first semantic divergence",
            "downstream semantic consumer",
            "effective optimized-divergence capability",
            "bounded result",
            "receipt/result",
            "optimized execution != optimization bug",
            "baseline/optimized mismatch != jit bug when language semantics permit the difference",
            "tier activation != specific pass causality",
            "optimization log != semantic divergence",
            "stale feedback != harmful stale assumption",
            "stale type feedback != type confusion without wrong runtime interpretation",
            "stale range fact != out-of-bounds effect",
            "missing guard != required guard proven absent",
            "guard elimination != unsound elimination",
            "deoptimization occurred != incorrect deoptimization",
            "deopt metadata mismatch != wrong reconstructed state without consumer evidence",
            "osr entry != equivalent full-function entry state by assumption",
            "inlining != preserved call semantics without dependency proof",
            "representation transition != semantic divergence",
            "same source function != same optimized code generation",
            "same code address != same compilation generation",
            "different machine code != different language semantics",
            "debug assertion != production semantic mismatch",
            "sanitizer finding != optimizer root cause",
            "crash != jit invariant violation",
            "minimized trigger != same optimizer path unless tier/pass activation is preserved",
            "differential mismatch != security relevance",
            "wrong optimized result != arbitrary memory corruption or code execution",
            "language-level undefined/implementation-defined behavior != optimizer unsoundness",
            "jit0",
            "jit1",
            "jit2",
            "jit3",
            "jit4",
            "jit5",
            "counterfactual",
            "alternative explanation",
            "evidence ceiling",
            "local/owned/sandboxed",
        ):
            self.assertIn(concept, lower)

    def test_runbook_requires_optimizer_generation_reasoning(self):
        self.assertTrue(RUNBOOK.is_file(), "JIT-invariant operator runbook must exist before depth can pass")
        text = RUNBOOK.read_text(encoding="utf-8")
        for section in (
            "## Attack surface",
            "## Hypothesis matrix",
            "## Runtime/program/tier-generation trace",
            "## Feedback/speculation/dependency trace",
            "## Guard/invalidation/optimization-transform trace",
            "## OSR/inlining/specialization trace",
            "## Deopt/frame-state reconstruction trace",
            "## Baseline/reference/semantic-consumer trace",
            "## Controlled validation",
            "## False-positive controls",
            "## Counterfactual JIT controls",
            "## Alternative explanations",
            "## Evidence capture",
            "## Evidence promotion and ceiling",
            "## Remediation checks",
        ):
            self.assertIn(section, text)

        lower = text.lower()
        for phrase in (
            "tier generation",
            "optimized code generation",
            "feedback generation",
            "speculative invariant",
            "dependency",
            "guard",
            "invalidation",
            "osr",
            "inlining",
            "deopt",
            "frame state",
            "baseline",
            "semantic consumer",
            "synthetic",
            "read-only",
            "shadow",
            "counterfactual",
            "alternative explanation",
            "evidence ceiling",
            "jit5",
        ):
            self.assertIn(phrase, lower)

    def test_review_cases_encode_jit_invariant_reasoning(self):
        self.assertTrue(CASES.is_file(), "JIT-invariant review-case matrix must exist before depth can pass")
        payload = json.loads(CASES.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 1)
        self.assertGreaterEqual(len(payload["scenarios"]), 4)

        required_ids = {
            "stale-type-feedback-after-shape-transition",
            "range-fact-invalidated-by-side-effect",
            "deopt-frame-state-reconstruction-mismatch",
            "osr-tier-generation-assumption-leak",
        }
        self.assertTrue(required_ids.issubset({scenario["id"] for scenario in payload["scenarios"]}))

        required = (
            "hypothesis",
            "safe_oracle",
            "positive_control",
            "negative_control",
            "stop_condition",
            "remediation_oracle",
            "runtime_program_tier_generation",
            "feedback_speculation_dependency",
            "guard_invalidation_transform_trace",
            "osr_inlining_specialization_state",
            "deopt_frame_state_reconstruction",
            "baseline_reference_semantics",
            "downstream_semantic_consumer",
            "effective_optimized_divergence_capability",
            "bounded_result",
            "receipt_result_binding",
            "counterfactual_control",
            "alternative_explanation",
            "evidence_level",
            "evidence_ceiling",
        )
        safe_terms = ("synthetic", "mock", "inert", "read-only", "controlled", "shadow", "toy")
        for scenario in payload["scenarios"]:
            for field in required:
                self.assertIn(field, scenario)
                self.assertIsInstance(scenario[field], str)
                self.assertGreaterEqual(len(scenario[field].strip()), 40)
            self.assertTrue(any(term in scenario["safe_oracle"].lower() for term in safe_terms))
            self.assertTrue(any(term in scenario["stop_condition"].lower() for term in ("stop", "abort", "do not proceed")))
            self.assertRegex(scenario["evidence_level"], r"\bJIT[0-5]\b")
            self.assertRegex(scenario["evidence_ceiling"], r"\bJIT[0-5]\b")

    def test_skill_is_registered_as_thirty_second_operator_depth_profile(self):
        payload = json.loads(PROFILES.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 2)
        profiles = payload["profiles"]
        self.assertGreaterEqual(len(profiles), 32)
        matching = [p for p in profiles if p["skill"] == "jit-invariant-analysis"]
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
