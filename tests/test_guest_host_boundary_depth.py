import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "guest-host-boundary-analysis" / "SKILL.md"
RUNBOOK = ROOT / "skills" / "guest-host-boundary-analysis" / "references" / "operator-runbook.md"
CASES = ROOT / "skills" / "guest-host-boundary-analysis" / "references" / "operator-review-cases.json"
PROFILES = ROOT / "operator-depth" / "profiles.json"


class GuestHostBoundaryDepthTests(unittest.TestCase):
    def test_skill_exposes_causal_guest_host_boundary_model(self):
        text = SKILL.read_text(encoding="utf-8")
        for section in (
            "## Causal guest-to-host boundary model",
            "## Guest, interface, and device-generation identity",
            "## Address translation and shared-object binding",
            "## Host consumer, ownership, and effective authority",
            "## Reset, unplug, migration, and snapshot lifecycle",
            "## Guest-host evidence ladder",
            "## Counterfactual proof",
            "## Alternative explanations",
            "## Evidence ceiling",
        ):
            self.assertIn(section, text)

        lower = text.lower()
        for concept in (
            "guest principal/security domain -> interface/device/channel identity and generation -> guest-controlled descriptor/register/message/address -> guest-physical/shared-object identity -> translation/iommu/memory-slot generation -> backend/emulation-thread consumer -> host object identity/ownership/lifetime -> validation/pinning/copy/toctou decision -> effective host capability/authority -> bounded host-side result/receipt -> reset/hot-unplug/migration/snapshot/device lifecycle generation",
            "guest-controlled input != host-owned object authority",
            "guest crash != host boundary crossing",
            "host process crash != guest-to-host escape",
            "host sanitizer finding != bounded cross-boundary security consequence",
            "valid descriptor != current queue/device generation",
            "guest physical address != stable host mapping identity",
            "mapped address != authorized backend use",
            "shared memory reachable != ownership/lifetime safe",
            "backend handler reachability != effective host capability",
            "emulation-thread execution != privileged host effect",
            "device reset complete != stale asynchronous work revoked",
            "hot-unplug complete != outstanding mapping/reference revoked",
            "snapshot restore != same device/object/lifecycle generation",
            "migration success != current host policy/iommu/memory-slot generation",
            "bounded synthetic host marker != arbitrary host code execution",
            "result success != receipt/result binding",
            "gh0",
            "gh1",
            "gh2",
            "gh3",
            "gh4",
            "gh5",
            "counterfactual",
            "alternative explanation",
            "evidence ceiling",
            "local/owned/sandboxed",
        ):
            self.assertIn(concept, lower)

    def test_runbook_requires_transition_level_guest_host_reasoning(self):
        self.assertTrue(RUNBOOK.is_file(), "guest-host operator runbook must exist before depth can pass")
        text = RUNBOOK.read_text(encoding="utf-8")
        for section in (
            "## Attack surface",
            "## Hypothesis matrix",
            "## Guest principal and boundary intent trace",
            "## Interface, device, queue, and channel identity trace",
            "## Guest-controlled object and descriptor trace",
            "## Address translation and IOMMU/memory-slot trace",
            "## Shared-memory ownership and lifetime trace",
            "## Backend/emulation-thread consumer trace",
            "## Effective host capability trace",
            "## Reset, hot-unplug, and async revocation trace",
            "## Migration and snapshot lifecycle trace",
            "## Privileged-consumer and result trace",
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
            "guest principal",
            "device generation",
            "queue generation",
            "iommu",
            "memory-slot",
            "ownership",
            "lifetime",
            "effective host capability",
            "reset",
            "hot-unplug",
            "migration",
            "snapshot",
            "receipt/result",
            "synthetic",
            "inert",
            "alternative explanation",
            "evidence ceiling",
            "gh5",
        ):
            self.assertIn(phrase, lower)

    def test_review_cases_encode_guest_host_boundary_reasoning(self):
        self.assertTrue(CASES.is_file(), "guest-host review-case matrix must exist before depth can pass")
        payload = json.loads(CASES.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 1)
        self.assertGreaterEqual(len(payload["scenarios"]), 4)
        required_ids = {
            "stale-descriptor-reset-generation",
            "shared-memory-revocation-lifetime",
            "address-translation-generation-binding",
            "migration-snapshot-stale-capability",
        }
        self.assertTrue(required_ids.issubset({scenario["id"] for scenario in payload["scenarios"]}))

        required = (
            "hypothesis",
            "safe_oracle",
            "positive_control",
            "negative_control",
            "stop_condition",
            "remediation_oracle",
            "guest_principal_boundary_intent",
            "interface_device_channel_identity",
            "device_queue_channel_generation",
            "guest_controlled_object_identity",
            "address_translation_generation",
            "shared_object_ownership_lifetime",
            "host_consumer_identity",
            "effective_host_capability",
            "validation_ownership_decision",
            "lifecycle_transition_generation",
            "final_host_decision",
            "bounded_host_result",
            "receipt_result_binding",
            "counterfactual_control",
            "alternative_explanation",
            "evidence_level",
            "evidence_ceiling",
        )
        safe_terms = ("synthetic", "mock", "inert", "read-only", "controlled", "nested")
        for scenario in payload["scenarios"]:
            for field in required:
                self.assertIn(field, scenario)
                self.assertIsInstance(scenario[field], str)
                self.assertGreaterEqual(len(scenario[field].strip()), 40)
            self.assertTrue(any(term in scenario["safe_oracle"].lower() for term in safe_terms))
            self.assertTrue(any(term in scenario["stop_condition"].lower() for term in ("stop", "abort", "do not proceed")))
            self.assertRegex(scenario["evidence_level"], r"\bGH[0-5]\b")
            self.assertRegex(scenario["evidence_ceiling"], r"\bGH[0-5]\b")

    def test_skill_is_registered_as_twenty_fourth_operator_depth_profile(self):
        payload = json.loads(PROFILES.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 2)
        profiles = payload["profiles"]
        self.assertGreaterEqual(len(profiles), 24)
        matching = [p for p in profiles if p["skill"] == "guest-host-boundary-analysis"]
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
