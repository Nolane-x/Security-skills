import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "rag-memory-data-isolation-analysis" / "SKILL.md"
RUNBOOK = (
    ROOT
    / "skills"
    / "rag-memory-data-isolation-analysis"
    / "references"
    / "operator-runbook.md"
)
SCENARIOS = (
    ROOT
    / "skills"
    / "rag-memory-data-isolation-analysis"
    / "references"
    / "operator-scenarios.json"
)
PROFILES = ROOT / "operator-depth" / "profiles.json"


class RagMemoryIsolationDepthTests(unittest.TestCase):
    def test_skill_exposes_identity_lifecycle_and_leakage_model(self):
        text = SKILL.read_text(encoding="utf-8")
        for section in (
            "## Isolation state model",
            "## Identity-binding model",
            "## Derived-state lineage",
            "## Lifecycle and revocation model",
            "## Leakage evidence ladder",
            "## Counterfactual and contamination controls",
            "## Evidence ceiling",
        ):
            self.assertIn(section, text)

        lower = text.lower()
        for concept in (
            "principal -> source object -> authorization snapshot -> chunk/summary -> embedding/index/cache key -> retrieval candidate -> acl/filter decision -> rerank/context -> model output -> memory writeback -> retention/revocation/deletion state",
            "effective retrieval principal",
            "source owner",
            "derived representation",
            "lifecycle generation",
            "bounded convergence window",
            "unique synthetic canary",
            "r0",
            "r1",
            "r2",
            "r3",
            "r4",
            "r5",
            "evidence ceiling",
        ):
            self.assertIn(concept, lower)

    def test_runbook_requires_lifecycle_aware_isolation_reasoning(self):
        self.assertTrue(
            RUNBOOK.is_file(),
            "RAG/memory operator runbook must exist before depth can pass",
        )
        text = RUNBOOK.read_text(encoding="utf-8")
        for section in (
            "## Attack surface",
            "## Hypothesis matrix",
            "## Identity and ownership binding",
            "## Derived-state lineage",
            "## Retrieval decision trace",
            "## Lifecycle and revocation trace",
            "## Cache and memory coherence",
            "## Controlled validation",
            "## False-positive controls",
            "## Counterfactual isolation controls",
            "## Evidence capture",
            "## Evidence promotion and ceiling",
            "## Remediation checks",
        ):
            self.assertIn(section, text)

        lower = text.lower()
        for phrase in (
            "effective retrieval principal",
            "authorization snapshot",
            "source lineage",
            "lifecycle generation",
            "revocation generation",
            "bounded convergence window",
            "stale cache",
            "memory compaction",
            "unique synthetic canary",
            "alternative explanation",
            "evidence ceiling",
        ):
            self.assertIn(phrase, lower)

    def test_scenarios_encode_identity_and_lifecycle_reasoning(self):
        self.assertTrue(
            SCENARIOS.is_file(),
            "RAG/memory scenario matrix must exist before depth can pass",
        )
        payload = json.loads(SCENARIOS.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 1)
        self.assertGreaterEqual(len(payload["scenarios"]), 3)
        for scenario in payload["scenarios"]:
            for field in (
                "hypothesis",
                "safe_oracle",
                "positive_control",
                "negative_control",
                "stop_condition",
                "remediation_oracle",
                "principal_binding",
                "source_lineage",
                "derived_state_trace",
                "retrieval_policy_trace",
                "lifecycle_state",
                "cache_memory_state",
                "counterfactual_control",
                "alternative_explanation",
                "leakage_level",
                "evidence_ceiling",
            ):
                self.assertIn(field, scenario)
                self.assertIsInstance(scenario[field], str)
                self.assertGreaterEqual(len(scenario[field].strip()), 40)

    def test_skill_is_registered_as_tenth_operator_depth_profile(self):
        payload = json.loads(PROFILES.read_text(encoding="utf-8"))
        profiles = payload["profiles"]
        self.assertEqual(len(profiles), 10)
        matching = [
            profile
            for profile in profiles
            if profile["skill"] == "rag-memory-data-isolation-analysis"
        ]
        self.assertEqual(len(matching), 1)
        profile = matching[0]
        self.assertEqual(profile["runbook"], "references/operator-runbook.md")
        self.assertEqual(profile["scenario_matrix"], "references/operator-scenarios.json")
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
