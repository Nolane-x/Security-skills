import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "memory-lifetime-analysis" / "SKILL.md"
RUNBOOK = ROOT / "skills" / "memory-lifetime-analysis" / "references" / "operator-runbook.md"
CASES = ROOT / "skills" / "memory-lifetime-analysis" / "references" / "operator-review-cases.json"
PROFILES = ROOT / "operator-depth" / "profiles.json"


class MemoryLifetimeDepthTests(unittest.TestCase):
    def test_skill_exposes_causal_memory_lifetime_model(self):
        text = SKILL.read_text(encoding="utf-8")
        for section in (
            "## Causal memory-lifetime model",
            "## Object identity, owner, and alias generations",
            "## Invalidation, destruction, and reuse binding",
            "## Callback, asynchronous work, and refcount lifecycle",
            "## Final consumer and bounded effect binding",
            "## Memory-lifetime evidence ladder",
            "## Counterfactual proof",
            "## Alternative explanations",
            "## Evidence ceiling",
        ):
            self.assertIn(section, text)

        lower = text.lower()
        for concept in (
            "logical object identity",
            "allocation generation",
            "acquisition generation",
            "owner",
            "alias",
            "borrowed reference",
            "retained ownership",
            "refcount",
            "invalidation",
            "retirement",
            "destruction generation",
            "release generation",
            "address reuse",
            "handle reuse",
            "asynchronous",
            "final consumer",
            "effective",
            "bounded result",
            "receipt/result",
            "address/handle equality != logical object identity",
            "alias reachability != lifetime validity",
            "memory freed != stale alias necessarily consumed",
            "callback queued != callback authorized after retirement",
            "sanitizer report != complete causal lifetime proof",
            "crash != exploitability",
            "ml0",
            "ml1",
            "ml2",
            "ml3",
            "ml4",
            "ml5",
            "counterfactual",
            "alternative explanation",
            "evidence ceiling",
            "local/owned/sandboxed",
        ):
            self.assertIn(concept, lower)

    def test_runbook_requires_transition_level_memory_lifetime_reasoning(self):
        self.assertTrue(RUNBOOK.is_file(), "memory-lifetime operator runbook must exist before depth can pass")
        text = RUNBOOK.read_text(encoding="utf-8")
        for section in (
            "## Attack surface",
            "## Hypothesis matrix",
            "## Object identity and allocation-generation trace",
            "## Ownership and alias trace",
            "## Retain, borrow, and refcount trace",
            "## Invalidation and destruction trace",
            "## Address and handle reuse trace",
            "## Callback and asynchronous-work trace",
            "## Cancellation, teardown, and error-path trace",
            "## Final consumer and effective capability trace",
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
            "logical object",
            "allocation generation",
            "owner",
            "alias",
            "borrow",
            "retain",
            "refcount",
            "invalidation",
            "destruction",
            "address reuse",
            "handle reuse",
            "callback",
            "asynchronous",
            "cancellation",
            "teardown",
            "final consumer",
            "effective capability",
            "receipt/result",
            "synthetic",
            "inert",
            "alternative explanation",
            "evidence ceiling",
            "ml5",
        ):
            self.assertIn(phrase, lower)

    def test_review_cases_encode_memory_lifetime_reasoning(self):
        self.assertTrue(CASES.is_file(), "memory-lifetime review-case matrix must exist before depth can pass")
        payload = json.loads(CASES.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 1)
        self.assertGreaterEqual(len(payload["scenarios"]), 4)

        required_ids = {
            "stale-callback-after-retirement",
            "address-reuse-object-identity-confusion",
            "duplicate-release-refcount-generation",
            "cancellation-completion-teardown-race",
        }
        self.assertTrue(required_ids.issubset({scenario["id"] for scenario in payload["scenarios"]}))

        required = (
            "hypothesis",
            "safe_oracle",
            "positive_control",
            "negative_control",
            "stop_condition",
            "remediation_oracle",
            "object_identity_generation",
            "owner_alias_state",
            "acquisition_release_trace",
            "invalidation_event",
            "destruction_generation",
            "reuse_generation",
            "retain_borrow_refcount_state",
            "async_work_identity",
            "cancellation_teardown_state",
            "final_consumer_identity",
            "effective_lifetime_capability",
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
            self.assertRegex(scenario["evidence_level"], r"\bML[0-5]\b")
            self.assertRegex(scenario["evidence_ceiling"], r"\bML[0-5]\b")

    def test_skill_is_registered_as_twenty_fifth_operator_depth_profile(self):
        payload = json.loads(PROFILES.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 2)
        profiles = payload["profiles"]
        self.assertGreaterEqual(len(profiles), 25)
        matching = [p for p in profiles if p["skill"] == "memory-lifetime-analysis"]
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
