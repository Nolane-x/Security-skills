import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "browser-process-boundary-analysis" / "SKILL.md"
RUNBOOK = ROOT / "skills" / "browser-process-boundary-analysis" / "references" / "operator-runbook.md"
CASES = ROOT / "skills" / "browser-process-boundary-analysis" / "references" / "operator-review-cases.json"
PROFILES = ROOT / "operator-depth" / "profiles.json"


class BrowserProcessBoundaryDepthTests(unittest.TestCase):
    def test_skill_exposes_causal_browser_process_model(self):
        text = SKILL.read_text(encoding="utf-8")
        for section in (
            "## Causal browser-process model",
            "## Process, origin, and object identity",
            "## IPC and routed-object validation",
            "## Brokered capability and authority",
            "## Lifecycle and generation reasoning",
            "## Browser-process evidence ladder",
            "## Counterfactual proof",
            "## Alternative explanations",
            "## Evidence ceiling",
        ):
            self.assertIn(section, text)

        lower = text.lower()
        for concept in (
            "request origin -> browser principal -> origin/site/frame security context -> site/process assignment -> process identity and process generation -> routed object/interface identity -> ipc schema plus normalized message state -> object ownership/lifecycle validation -> broker or privileged service identity -> requested capability/resource identity -> policy/authorization decision -> effective brokered authority -> privileged consumer/action -> bounded synthetic effect -> receipt/result binding -> lifecycle/revocation/process-generation state",
            "process role != process identity",
            "process identity != origin/site/frame identity",
            "route/interface identifier != routed object identity",
            "message deserialization success != policy authorization",
            "object reference != object ownership",
            "shared-memory access != resource authority",
            "ambient privileged-service authority != delegated request authority",
            "requested capability != policy-approved effective capability",
            "current object/process generation != stale generation",
            "renderer reachability != browser-process compromise",
            "b0",
            "b1",
            "b2",
            "b3",
            "b4",
            "b5",
            "counterfactual",
            "evidence ceiling",
        ):
            self.assertIn(concept, lower)

    def test_runbook_requires_transition_level_browser_reasoning(self):
        self.assertTrue(RUNBOOK.is_file(), "browser-process operator runbook must exist before depth can pass")
        text = RUNBOOK.read_text(encoding="utf-8")
        for section in (
            "## Attack surface",
            "## Hypothesis matrix",
            "## Process graph and sandbox-profile trace",
            "## Origin/site/frame context trace",
            "## Process identity and generation trace",
            "## IPC schema and normalized-message trace",
            "## Routed object and lifecycle trace",
            "## Ownership and authorization decision trace",
            "## Brokered capability and resource trace",
            "## Ambient-versus-delegated authority trace",
            "## Privileged-consumer and result trace",
            "## Lifecycle/revocation generation trace",
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
            "process generation",
            "object generation",
            "origin/site/frame",
            "routed object",
            "brokered capability",
            "ambient authority",
            "delegated authority",
            "receipt/result",
            "debug-only",
            "unsandboxed",
            "release-boundary proof",
            "alternative explanation",
            "evidence ceiling",
        ):
            self.assertIn(phrase, lower)

    def test_review_cases_encode_browser_process_reasoning(self):
        self.assertTrue(CASES.is_file(), "browser-process review-case matrix must exist before depth can pass")
        payload = json.loads(CASES.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 1)
        self.assertGreaterEqual(len(payload["scenarios"]), 3)
        required_ids = {
            "origin-process-object-binding",
            "ipc-capability-broker-binding",
            "process-generation-lifecycle-binding",
        }
        self.assertTrue(required_ids.issubset({scenario["id"] for scenario in payload["scenarios"]}))
        required = (
            "hypothesis",
            "safe_oracle",
            "positive_control",
            "negative_control",
            "stop_condition",
            "remediation_oracle",
            "request_origin",
            "browser_principal",
            "origin_site_frame_context",
            "process_assignment",
            "process_identity",
            "process_generation",
            "sandbox_profile",
            "ipc_channel",
            "message_state",
            "routed_object_identity",
            "object_generation",
            "ownership_authorization_check",
            "broker_identity",
            "requested_capability_resource",
            "policy_decision",
            "effective_brokered_authority",
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
            self.assertRegex(scenario["evidence_level"], r"\bB[0-5]\b")
            self.assertRegex(scenario["evidence_ceiling"], r"\bB[0-5]\b")

    def test_skill_is_registered_as_nineteenth_operator_depth_profile(self):
        payload = json.loads(PROFILES.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 2)
        profiles = payload["profiles"]
        self.assertGreaterEqual(len(profiles), 19)
        matching = [p for p in profiles if p["skill"] == "browser-process-boundary-analysis"]
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
