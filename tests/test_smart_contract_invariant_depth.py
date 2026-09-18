import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "smart-contract-invariant-analysis" / "SKILL.md"
RUNBOOK = ROOT / "skills" / "smart-contract-invariant-analysis" / "references" / "operator-runbook.md"
CASES = ROOT / "skills" / "smart-contract-invariant-analysis" / "references" / "operator-review-cases.json"
PROFILES = ROOT / "operator-depth" / "profiles.json"


class SmartContractInvariantDepthTests(unittest.TestCase):
    def test_skill_exposes_causal_smart_contract_invariant_model(self):
        text = SKILL.read_text(encoding="utf-8")
        for section in (
            "## Causal smart-contract-invariant model",
            "## Protocol, deployment, contract, and state generations",
            "## Invariant identity and domain binding",
            "## Entrypoint, actor, and transition binding",
            "## Asset, accounting, and conservation binding",
            "## External dependency and assumption binding",
            "## Reachability, witness, and bounded consequence binding",
            "## Smart-contract invariant evidence ladder",
            "## Counterfactual invariant controls",
            "## Alternative explanations",
            "## Evidence ceiling",
        ):
            self.assertIn(section, text)

        lower = text.lower()
        for concept in (
            "protocol/system identity",
            "local chain/environment identity/generation",
            "deployment/configuration identity/generation",
            "contract-set identity/generation",
            "contract/code revision identity",
            "invariant identity/version",
            "invariant domain/scope",
            "actor/account identity/generation",
            "role/authorization state generation",
            "asset/accounting domain identity",
            "state snapshot/block/transaction generation",
            "entrypoint/operation identity",
            "call/transition sequence identity",
            "pre-state identity",
            "required precondition",
            "external dependency/assumption identity/generation",
            "state-write/commit identity",
            "post-state identity",
            "invariant predicate",
            "expected invariant result",
            "observed invariant result",
            "first invalid transition/state delta",
            "violation witness identity",
            "downstream protocol/accounting consumer identity",
            "effective invariant-break capability",
            "bounded result",
            "receipt/result",
            "suspicious pattern != invariant violation",
            "invariant violation != exploitable economic loss",
            "local property failure != production reachability",
            "reachable entrypoint != reachable violating state",
            "state change != invalid state transition",
            "balance difference != conservation failure without accounting-domain binding",
            "asset balance != protocol accounting balance by assumption",
            "token transfer success != protocol solvency",
            "share-price movement != accounting violation by itself",
            "temporary imbalance != terminal invariant break when the protocol explicitly permits transient state",
            "precondition failure != postcondition violation",
            "revert != invariant preservation proof",
            "event emission != state commitment",
            "storage write != committed protocol state by itself",
            "duplicate-looking identifier != uniqueness violation without generation/domain binding",
            "counter decrease != monotonicity violation when reset/epoch semantics permit it",
            "role possession != authorization invariant violation",
            "stale role state != current authority without generation binding",
            "external call exists != reentrancy root cause",
            "callback reachability != invariant violation",
            "oracle value change != external-data trust defect by itself",
            "synthetic price movement != market-manipulation proof",
            "upgradeability != invariant failure",
            "storage-layout change != invariant failure without upgrade transition proof",
            "gas difference != liveness failure",
            "bounded local progress delay != permanent liveness failure",
            "fuzz counterexample != root cause until minimized and replayed",
            "symbolic path != runtime reachability by assumption",
            "mainnet-like fork state != authorization to transact on live systems",
            "local synthetic accounting consequence != real financial loss",
            "sci0",
            "sci1",
            "sci2",
            "sci3",
            "sci4",
            "sci5",
            "counterfactual",
            "alternative explanation",
            "evidence ceiling",
            "local/owned/test",
        ):
            self.assertIn(concept, lower)

    def test_runbook_requires_invariant_generation_reasoning(self):
        self.assertTrue(RUNBOOK.is_file(), "smart-contract invariant operator runbook must exist before depth can pass")
        text = RUNBOOK.read_text(encoding="utf-8")
        for section in (
            "## Attack surface",
            "## Hypothesis matrix",
            "## Protocol/deployment/state-generation trace",
            "## Invariant/domain/observation-point trace",
            "## Entrypoint/actor/transition trace",
            "## Asset/accounting/conservation trace",
            "## External-dependency/assumption trace",
            "## Reachability/witness/bounded-consequence trace",
            "## Controlled validation",
            "## False-positive controls",
            "## Counterfactual invariant controls",
            "## Alternative explanations",
            "## Evidence capture",
            "## Evidence promotion and ceiling",
            "## Remediation checks",
        ):
            self.assertIn(section, text)

        lower = text.lower()
        for phrase in (
            "protocol generation",
            "deployment generation",
            "state generation",
            "invariant identity",
            "observation point",
            "entrypoint",
            "actor",
            "transition",
            "conservation",
            "solvency",
            "external dependency",
            "violation witness",
            "synthetic",
            "test chain",
            "read-only",
            "counterfactual",
            "alternative explanation",
            "evidence ceiling",
            "sci5",
        ):
            self.assertIn(phrase, lower)

    def test_review_cases_encode_invariant_reasoning(self):
        self.assertTrue(CASES.is_file(), "smart-contract invariant review-case matrix must exist before depth can pass")
        payload = json.loads(CASES.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 1)
        self.assertGreaterEqual(len(payload["scenarios"]), 4)

        required_ids = {
            "conservation-ledger-supply-divergence",
            "claim-uniqueness-epoch-generation-reuse",
            "phase-transition-skips-required-accounting-state",
            "solvency-accounting-domain-omits-pending-liability",
        }
        self.assertTrue(required_ids.issubset({scenario["id"] for scenario in payload["scenarios"]}))

        required = (
            "hypothesis",
            "safe_oracle",
            "positive_control",
            "negative_control",
            "stop_condition",
            "remediation_oracle",
            "protocol_deployment_state_generation",
            "invariant_domain_observation_point",
            "entrypoint_actor_transition_trace",
            "asset_accounting_conservation_state",
            "external_dependency_assumption_state",
            "reachability_violation_witness",
            "downstream_protocol_consumer_identity",
            "effective_invariant_break_capability",
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
            self.assertRegex(scenario["evidence_level"], r"\bSCI[0-5]\b")
            self.assertRegex(scenario["evidence_ceiling"], r"\bSCI[0-5]\b")

    def test_skill_is_registered_as_thirty_eighth_operator_depth_profile(self):
        payload = json.loads(PROFILES.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 2)
        profiles = payload["profiles"]
        self.assertGreaterEqual(len(profiles), 38)
        matching = [p for p in profiles if p["skill"] == "smart-contract-invariant-analysis"]
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
