import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "sandbox-boundary-analysis" / "SKILL.md"
RUNBOOK = ROOT / "skills" / "sandbox-boundary-analysis" / "references" / "operator-runbook.md"
CASES = ROOT / "skills" / "sandbox-boundary-analysis" / "references" / "operator-review-cases.json"
PROFILES = ROOT / "operator-depth" / "profiles.json"


class SandboxBoundaryDepthTests(unittest.TestCase):
    def test_skill_exposes_causal_sandbox_boundary_model(self):
        text = SKILL.read_text(encoding="utf-8")
        for section in (
            "## Causal sandbox-boundary model",
            "## Sandboxed principal, policy, and lifecycle generations",
            "## Broker request and caller-session binding",
            "## Resource, namespace, and canonical identity binding",
            "## Inherited and delegated capability provenance",
            "## Shared state and privileged-service consumer binding",
            "## Final capability and bounded effect binding",
            "## Sandbox-boundary evidence ladder",
            "## Counterfactual boundary controls",
            "## Alternative explanations",
            "## Evidence ceiling",
        ):
            self.assertIn(section, text)

        lower = text.lower()
        for concept in (
            "sandbox principal",
            "session generation",
            "policy identity",
            "policy generation",
            "request generation",
            "broker/service identity",
            "caller-to-request binding",
            "requested resource identity",
            "resolved resource identity",
            "inherited/delegated capability",
            "namespace/object generation",
            "shared-state generation",
            "privileged consumer",
            "effective crossed capability",
            "bounded result",
            "receipt/result",
            "broker reachability != broker authority",
            "inherited handle/fd != ambient host authority",
            "mapped shared memory != authorized privileged use",
            "namespace alias != policy bypass",
            "sandbox policy present != policy applied to the decisive operation",
            "restricted token/seccomp profile != proof of complete confinement",
            "sandboxed-process crash != sandbox escape",
            "privileged-service crash != sandbox escape",
            "privileged-service code execution != arbitrary host compromise",
            "broadened broker capability != arbitrary code execution",
            "process outside sandbox != privileged process",
            "policy mismatch != complete escape",
            "stale session/request identity != current authority",
            "sb0",
            "sb1",
            "sb2",
            "sb3",
            "sb4",
            "sb5",
            "counterfactual",
            "alternative explanation",
            "evidence ceiling",
            "local/owned/sandboxed",
        ):
            self.assertIn(concept, lower)

    def test_runbook_requires_transition_level_sandbox_reasoning(self):
        self.assertTrue(RUNBOOK.is_file(), "sandbox-boundary operator runbook must exist before depth can pass")
        text = RUNBOOK.read_text(encoding="utf-8")
        for section in (
            "## Attack surface",
            "## Hypothesis matrix",
            "## Principal and policy-generation trace",
            "## Broker request and caller-session trace",
            "## Resource and namespace-resolution trace",
            "## Inherited/delegated capability trace",
            "## Shared-state and privileged-consumer trace",
            "## Lifecycle revocation and restart trace",
            "## Final capability and bounded-effect trace",
            "## Controlled validation",
            "## False-positive controls",
            "## Counterfactual boundary controls",
            "## Alternative explanations",
            "## Evidence capture",
            "## Evidence promotion and ceiling",
            "## Remediation checks",
        ):
            self.assertIn(section, text)

        lower = text.lower()
        for phrase in (
            "sandbox principal",
            "policy generation",
            "session generation",
            "broker",
            "caller-session",
            "resolved resource",
            "namespace",
            "inherited",
            "delegated capability",
            "shared-state generation",
            "privileged consumer",
            "lifecycle",
            "revocation",
            "effective crossed capability",
            "synthetic",
            "mock",
            "inert",
            "read-only",
            "counterfactual",
            "alternative explanation",
            "evidence ceiling",
            "sb5",
        ):
            self.assertIn(phrase, lower)

    def test_review_cases_encode_sandbox_boundary_reasoning(self):
        self.assertTrue(CASES.is_file(), "sandbox-boundary review-case matrix must exist before depth can pass")
        payload = json.loads(CASES.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 1)
        self.assertGreaterEqual(len(payload["scenarios"]), 4)

        required_ids = {
            "stale-session-broker-authorization",
            "namespace-alias-resolved-object-mismatch",
            "inherited-capability-rights-drift",
            "shared-object-generation-confusion",
        }
        self.assertTrue(required_ids.issubset({scenario["id"] for scenario in payload["scenarios"]}))

        required = (
            "hypothesis",
            "safe_oracle",
            "positive_control",
            "negative_control",
            "stop_condition",
            "remediation_oracle",
            "sandbox_principal_policy_generation",
            "broker_request_caller_binding",
            "resource_namespace_resolution",
            "inherited_delegated_capability",
            "shared_state_privileged_consumer",
            "lifecycle_revocation_state",
            "final_consumer_identity",
            "effective_crossed_capability",
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
            self.assertRegex(scenario["evidence_level"], r"\bSB[0-5]\b")
            self.assertRegex(scenario["evidence_ceiling"], r"\bSB[0-5]\b")

    def test_skill_is_registered_as_twenty_seventh_operator_depth_profile(self):
        payload = json.loads(PROFILES.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 2)
        profiles = payload["profiles"]
        self.assertEqual(len(profiles), 27)
        matching = [p for p in profiles if p["skill"] == "sandbox-boundary-analysis"]
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