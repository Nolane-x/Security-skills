import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "smart-contract-upgradeability-analysis" / "SKILL.md"
RUNBOOK = ROOT / "skills" / "smart-contract-upgradeability-analysis" / "references" / "operator-runbook.md"
CASES = ROOT / "skills" / "smart-contract-upgradeability-analysis" / "references" / "operator-review-cases.json"
PROFILES = ROOT / "operator-depth" / "profiles.json"


class SmartContractUpgradeabilityDepthTests(unittest.TestCase):
    def test_skill_exposes_causal_smart_contract_upgradeability_model(self):
        text = SKILL.read_text(encoding="utf-8")
        for section in (
            "## Causal smart-contract-upgradeability model",
            "## Proxy, implementation, governance, and lifecycle generations",
            "## Upgrade authorization and commit binding",
            "## Storage-layout and state-interpretation binding",
            "## Initializer, reinitializer, and migration binding",
            "## Selector, fallback, beacon, and facet routing binding",
            "## Upgrade invariant and bounded consequence binding",
            "## Smart-contract upgradeability evidence ladder",
            "## Counterfactual upgradeability controls",
            "## Alternative explanations",
            "## Evidence ceiling",
        ):
            self.assertIn(section, text)

        lower = text.lower()
        for concept in (
            "protocol/system identity",
            "local chain/environment identity/generation",
            "deployment/proxy identity/generation",
            "proxy model",
            "proxy/admin/governance identity/generation",
            "current implementation identity/generation",
            "candidate implementation identity/generation",
            "implementation code revision",
            "implementation registry/beacon/facet-set identity/generation",
            "upgrade proposal/operation identity/generation",
            "authorization path identity/generation",
            "timelock/multisig/governance state generation",
            "implementation/admin slot or registry identity",
            "selector/fallback routing identity/generation",
            "delegatecall/context identity",
            "storage-layout identity/version",
            "storage slot/type/packing identity",
            "initializer/reinitializer identity/generation",
            "initialized-version state",
            "upgrade hook/migration identity/generation",
            "pre-upgrade state snapshot",
            "upgrade commit identity",
            "post-upgrade state snapshot",
            "rollback/downgrade identity/generation",
            "invariant/result identity",
            "downstream proxy consumer identity",
            "effective upgradeability capability",
            "bounded result",
            "receipt/result",
            "upgradeability != vulnerability",
            "upgrade authorization != upgrade correctness",
            "admin role possession != unauthorized upgrade",
            "governance proposal != committed implementation change",
            "timelock queued != timelock executed",
            "implementation deployed != proxy upgraded",
            "proxy implementation slot value != active behavior without routing/delegate binding",
            "implementation address equality != implementation code-generation equality",
            "same proxy address != same implementation generation",
            "delegatecall exists != storage corruption",
            "storage-layout diff != storage corruption without state-slot interpretation mismatch",
            "slot collision != harmful collision without consumer evidence",
            "reserved storage gap change != corruption by itself",
            "added variable != incompatible layout by itself",
            "compiler layout metadata != runtime storage proof by itself",
            "initializer exists != initialization flaw",
            "implementation instance uninitialized != proxy instance uninitialized",
            "proxy initialized != new implementation/reinitializer state valid by assumption",
            "reinitializer callable != unauthorized or repeated state mutation without version/policy proof",
            "disabled initializer != all initialization paths disabled",
            "selector collision != reachable unintended function without routing proof",
            "facet added != selector ownership conflict by itself",
            "stale implementation abi != reachable stale implementation",
            "implementation self-call != proxy-context delegatecall by assumption",
            "implementation function success != proxy-context success",
            "upgrade hook success != state migration correctness",
            "migration state change != invariant break",
            "rollback possible != rollback unsafe",
            "downgrade != vulnerability without version/invariant consequence",
            "emergency bypass exists != unauthorized bypass",
            "multisig threshold != effective signer authorization without signer/epoch binding",
            "governance vote result != execution authority without execution-path binding",
            "upgrade event != committed implementation/state change",
            "storage write != active implementation switch without final consumer proof",
            "local synthetic state corruption != real asset loss",
            "local admin control != production governance compromise",
            "invariant violation after upgrade != upgrade root cause until transition/layout/initializer causality is established",
            "reentrancy after upgrade != upgradeability root cause unless the upgrade introduced the relevant call/order semantics",
            "scu0",
            "scu1",
            "scu2",
            "scu3",
            "scu4",
            "scu5",
            "counterfactual",
            "alternative explanation",
            "evidence ceiling",
            "local/owned/test",
        ):
            self.assertIn(concept, lower)

    def test_runbook_requires_upgradeability_generation_reasoning(self):
        self.assertTrue(RUNBOOK.is_file(), "smart-contract upgradeability operator runbook must exist before depth can pass")
        text = RUNBOOK.read_text(encoding="utf-8")
        for section in (
            "## Attack surface",
            "## Hypothesis matrix",
            "## Proxy/implementation/governance-generation trace",
            "## Upgrade-authorization/commit trace",
            "## Storage-layout/state-interpretation trace",
            "## Initializer/reinitializer/migration trace",
            "## Selector/fallback/beacon/facet trace",
            "## Upgrade-invariant/bounded-consequence trace",
            "## Controlled validation",
            "## False-positive controls",
            "## Counterfactual upgradeability controls",
            "## Alternative explanations",
            "## Evidence capture",
            "## Evidence promotion and ceiling",
            "## Remediation checks",
        ):
            self.assertIn(section, text)

        lower = text.lower()
        for phrase in (
            "proxy generation",
            "implementation generation",
            "governance generation",
            "upgrade commit",
            "storage layout",
            "state interpretation",
            "initializer",
            "reinitializer",
            "migration",
            "selector",
            "beacon",
            "facet",
            "rollback",
            "synthetic",
            "test chain",
            "read-only",
            "counterfactual",
            "alternative explanation",
            "evidence ceiling",
            "scu5",
        ):
            self.assertIn(phrase, lower)

    def test_review_cases_encode_upgradeability_reasoning(self):
        self.assertTrue(CASES.is_file(), "smart-contract upgradeability review-case matrix must exist before depth can pass")
        payload = json.loads(CASES.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 1)
        self.assertGreaterEqual(len(payload["scenarios"]), 4)

        required_ids = {
            "storage-layout-slot-reinterpreted-after-upgrade",
            "reinitializer-version-replayed-after-upgrade",
            "selector-routing-generation-targets-unintended-facet",
            "rollback-restores-code-but-not-migrated-state-generation",
        }
        self.assertTrue(required_ids.issubset({scenario["id"] for scenario in payload["scenarios"]}))

        required = (
            "hypothesis",
            "safe_oracle",
            "positive_control",
            "negative_control",
            "stop_condition",
            "remediation_oracle",
            "proxy_implementation_governance_generation",
            "upgrade_authorization_commit_trace",
            "storage_layout_state_interpretation",
            "initializer_reinitializer_migration_state",
            "selector_fallback_beacon_facet_state",
            "upgrade_invariant_bounded_consequence",
            "downstream_proxy_consumer_identity",
            "effective_upgradeability_capability",
            "bounded_result",
            "receipt_result_binding",
            "counterfactual_control",
            "alternative_explanation",
            "evidence_level",
            "evidence_ceiling",
        )
        safe_terms = ("synthetic", "mock", "inert", "read-only", "controlled", "fake", "local", "test chain", "test-chain", "shadow")
        for scenario in payload["scenarios"]:
            for field in required:
                self.assertIn(field, scenario)
                self.assertIsInstance(scenario[field], str)
                self.assertGreaterEqual(len(scenario[field].strip()), 40)
            self.assertTrue(any(term in scenario["safe_oracle"].lower() for term in safe_terms))
            self.assertTrue(any(term in scenario["stop_condition"].lower() for term in ("stop", "abort", "do not proceed")))
            self.assertRegex(scenario["evidence_level"], r"\bSCU[0-5]\b")
            self.assertRegex(scenario["evidence_ceiling"], r"\bSCU[0-5]\b")

    def test_skill_is_registered_as_fortieth_operator_depth_profile(self):
        payload = json.loads(PROFILES.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 2)
        profiles = payload["profiles"]
        self.assertEqual(len(profiles), 40)
        matching = [p for p in profiles if p["skill"] == "smart-contract-upgradeability-analysis"]
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
