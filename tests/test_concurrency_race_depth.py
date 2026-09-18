import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "concurrency-race-analysis" / "SKILL.md"
RUNBOOK = ROOT / "skills" / "concurrency-race-analysis" / "references" / "operator-runbook.md"
CASES = ROOT / "skills" / "concurrency-race-analysis" / "references" / "operator-review-cases.json"
PROFILES = ROOT / "operator-depth" / "profiles.json"


class ConcurrencyRaceDepthTests(unittest.TestCase):
    def test_skill_exposes_causal_concurrency_model(self):
        text = SKILL.read_text(encoding="utf-8")
        for section in (
            "## Causal concurrency model",
            "## Shared invariant and state generations",
            "## Actor, scheduler, and operation generations",
            "## Synchronization and happens-before binding",
            "## Check/use, publication, and commit binding",
            "## Cancellation, retry, and teardown binding",
            "## Final consumer and bounded effect binding",
            "## Concurrency evidence ladder",
            "## Counterfactual schedules",
            "## Alternative explanations",
            "## Evidence ceiling",
        ):
            self.assertIn(section, text)

        lower = text.lower()
        for concept in (
            "shared invariant",
            "shared state identity",
            "state generation",
            "actor identity",
            "operation generation",
            "scheduler",
            "executor",
            "synchronization epoch",
            "happens-before",
            "check observation",
            "interfering transition",
            "commit transition",
            "cancellation generation",
            "teardown generation",
            "final consumer",
            "effective concurrent capability",
            "bounded result",
            "receipt/result",
            "data race != higher-level race",
            "atomic access != atomic invariant",
            "lock present != protected operation",
            "thread/task overlap != harmful interleaving",
            "timing correlation != causal schedule",
            "toctou window != demonstrated stale decision use",
            "cancellation requested != work revoked",
            "queue order != execution order",
            "retry overlap != duplicate effect",
            "sanitizer race report != complete causal concurrency proof",
            "crash != exploitability",
            "cr0",
            "cr1",
            "cr2",
            "cr3",
            "cr4",
            "cr5",
            "counterfactual",
            "alternative explanation",
            "evidence ceiling",
            "local/owned/sandboxed",
        ):
            self.assertIn(concept, lower)

    def test_runbook_requires_transition_level_concurrency_reasoning(self):
        self.assertTrue(RUNBOOK.is_file(), "concurrency-race operator runbook must exist before depth can pass")
        text = RUNBOOK.read_text(encoding="utf-8")
        for section in (
            "## Attack surface",
            "## Hypothesis matrix",
            "## Shared invariant and state-generation trace",
            "## Actor and operation-generation trace",
            "## Synchronization and happens-before trace",
            "## Check/use and commit-point trace",
            "## Queue, executor, and publication trace",
            "## Cancellation, retry, and teardown trace",
            "## Final consumer and single-effect trace",
            "## Deterministic schedule control",
            "## Controlled validation",
            "## False-positive controls",
            "## Counterfactual schedules",
            "## Alternative explanations",
            "## Evidence capture",
            "## Evidence promotion and ceiling",
            "## Remediation checks",
        ):
            self.assertIn(section, text)

        lower = text.lower()
        for phrase in (
            "shared invariant",
            "state generation",
            "actor",
            "operation generation",
            "scheduler",
            "executor",
            "happens-before",
            "check/use",
            "commit",
            "publication",
            "cancellation",
            "retry",
            "teardown",
            "single effect",
            "final consumer",
            "deterministic barrier",
            "synthetic",
            "inert",
            "counterfactual",
            "alternative explanation",
            "evidence ceiling",
            "cr5",
        ):
            self.assertIn(phrase, lower)

    def test_review_cases_encode_concurrency_reasoning(self):
        self.assertTrue(CASES.is_file(), "concurrency-race review-case matrix must exist before depth can pass")
        payload = json.loads(CASES.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 1)
        self.assertGreaterEqual(len(payload["scenarios"]), 4)

        required_ids = {
            "check-use-generation-race",
            "duplicate-completion-single-effect",
            "cancellation-commit-epoch-race",
            "publication-initialization-order-race",
        }
        self.assertTrue(required_ids.issubset({scenario["id"] for scenario in payload["scenarios"]}))

        required = (
            "hypothesis",
            "safe_oracle",
            "positive_control",
            "negative_control",
            "stop_condition",
            "remediation_oracle",
            "shared_invariant_state_generation",
            "actor_operation_generations",
            "scheduler_executor_identity",
            "synchronization_happens_before",
            "check_use_commit_trace",
            "queue_publication_state",
            "cancellation_retry_teardown_state",
            "final_consumer_identity",
            "effective_concurrent_capability",
            "bounded_result",
            "receipt_result_binding",
            "counterfactual_schedule",
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
            self.assertRegex(scenario["evidence_level"], r"\bCR[0-5]\b")
            self.assertRegex(scenario["evidence_ceiling"], r"\bCR[0-5]\b")

    def test_skill_is_registered_as_twenty_sixth_operator_depth_profile(self):
        payload = json.loads(PROFILES.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 2)
        profiles = payload["profiles"]
        self.assertEqual(len(profiles), 26)
        matching = [p for p in profiles if p["skill"] == "concurrency-race-analysis"]
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
