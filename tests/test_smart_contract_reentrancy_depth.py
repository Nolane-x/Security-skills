import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "smart-contract-reentrancy-state-analysis" / "SKILL.md"
RUNBOOK = ROOT / "skills" / "smart-contract-reentrancy-state-analysis" / "references" / "operator-runbook.md"
CASES = ROOT / "skills" / "smart-contract-reentrancy-state-analysis" / "references" / "operator-review-cases.json"
PROFILES = ROOT / "operator-depth" / "profiles.json"


class SmartContractReentrancyDepthTests(unittest.TestCase):
    def test_skill_exposes_causal_smart_contract_reentrancy_model(self):
        text = SKILL.read_text(encoding="utf-8")
        for section in (
            "## Causal smart-contract-reentrancy model",
            "## Outer transaction, call-frame, and callback generations",
            "## External-call, callback, and reentrant-entry binding",
            "## Transient-state and update-ordering binding",
            "## Lock, guard, and invariant-scope binding",
            "## Cross-function, cross-contract, hook, and read-only lineage",
            "## Outer continuation, commit, and duplicate-effect binding",
            "## Smart-contract reentrancy evidence ladder",
            "## Counterfactual reentrancy controls",
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
            "outer actor/account identity",
            "outer transaction/call generation",
            "outer entrypoint identity",
            "call-frame/stack generation",
            "pre-call state generation",
            "external-call site identity",
            "external callee/callback target identity/generation",
            "callback authority/capability",
            "callback trigger identity",
            "reentrant entrypoint identity",
            "reentry generation/depth",
            "lock/guard identity/generation",
            "lock scope/domain",
            "transient state identity/generation",
            "expected update/commit ordering",
            "observed callback/interleaving ordering",
            "cross-function/cross-contract path identity",
            "read-only observer identity",
            "outer-call continuation identity",
            "final commit/terminal point",
            "post-state identity",
            "expected invariant result",
            "observed invariant result",
            "first reentrant causal divergence",
            "downstream protocol/accounting consumer identity",
            "effective reentrancy-state capability",
            "bounded result",
            "receipt/result",
            "external call != reentrancy",
            "callback reachability != harmful reentrancy",
            "reentrant entrypoint reachability != invariant violation",
            "invariant violation != exploitable economic loss",
            "same-function recursion != unauthorized reentrancy by assumption",
            "callback before return != state-ordering defect by itself",
            "transient state != invalid terminal state when explicitly permitted",
            "checks-effects-interactions heuristic != proof of safety or defect",
            "lock present != protected invariant",
            "per-function lock != cross-function invariant lock",
            "lock acquired != correct lock scope",
            "reentrancy guard bypass != complete exploitability",
            "token hook support != vulnerability",
            "fallback/receive callback != asset-loss proof",
            "multicall nesting != reentrancy by itself",
            "cross-contract callback != cross-contract invariant break without shared-state binding",
            "read-only callback != read-only reentrancy defect until a consumer trusts transient state",
            "view function call != harmless by assumption when its result drives another state transition",
            "delegatecall/proxy context != reentrancy root cause by assumption",
            "callback contract code execution != authority over protocol state",
            "callback depth > 1 != stronger evidence by itself",
            "gas exhaustion != reentrancy proof",
            "revert != proof that no transient observation occurred",
            "event emission != committed state",
            "duplicate-looking state delta != duplicate effect without generation/commit binding",
            "local bounded accounting divergence != real financial loss",
            "synthetic callback marker != arbitrary control flow",
            "local test-chain exploitability != production reachability",
            "fuzzed callback sequence != root cause until minimized and replayed",
            "concurrency race != smart-contract reentrancy unless call-stack callback semantics are the causal mechanism",
            "scr0",
            "scr1",
            "scr2",
            "scr3",
            "scr4",
            "scr5",
            "counterfactual",
            "alternative explanation",
            "evidence ceiling",
            "local/owned/test-chain",
        ):
            self.assertIn(concept, lower)

    def test_runbook_requires_reentrancy_generation_reasoning(self):
        self.assertTrue(RUNBOOK.is_file(), "smart-contract reentrancy operator runbook must exist before depth can pass")
        text = RUNBOOK.read_text(encoding="utf-8")
        for section in (
            "## Attack surface",
            "## Hypothesis matrix",
            "## Outer-transaction/call-frame/callback-generation trace",
            "## External-call/callback/reentrant-entry trace",
            "## Transient-state/update-ordering trace",
            "## Lock/guard/invariant-scope trace",
            "## Cross-function/cross-contract/hook/read-only trace",
            "## Outer-continuation/commit/duplicate-effect trace",
            "## Controlled validation",
            "## False-positive controls",
            "## Counterfactual reentrancy controls",
            "## Alternative explanations",
            "## Evidence capture",
            "## Evidence promotion and ceiling",
            "## Remediation checks",
        ):
            self.assertIn(section, text)

        lower = text.lower()
        for phrase in (
            "outer transaction",
            "call frame",
            "callback generation",
            "external call",
            "reentrant entrypoint",
            "transient state",
            "update ordering",
            "lock scope",
            "cross-function",
            "cross-contract",
            "read-only",
            "synthetic",
            "test chain",
            "bounded depth",
            "counterfactual",
            "alternative explanation",
            "evidence ceiling",
            "scr5",
        ):
            self.assertIn(phrase, lower)

    def test_review_cases_encode_reentrancy_reasoning(self):
        self.assertTrue(CASES.is_file(), "smart-contract reentrancy review-case matrix must exist before depth can pass")
        payload = json.loads(CASES.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 1)
        self.assertGreaterEqual(len(payload["scenarios"]), 4)

        required_ids = {
            "cross-function-callback-consumes-transient-accounting-state",
            "per-function-guard-misses-cross-function-invariant",
            "hook-enabled-token-callback-before-balance-commit",
            "read-only-callback-observer-consumes-transient-share-state",
        }
        self.assertTrue(required_ids.issubset({scenario["id"] for scenario in payload["scenarios"]}))

        required = (
            "hypothesis",
            "safe_oracle",
            "positive_control",
            "negative_control",
            "stop_condition",
            "remediation_oracle",
            "outer_transaction_callback_generation",
            "external_call_reentrant_entry_trace",
            "transient_state_update_ordering",
            "lock_guard_invariant_scope",
            "cross_function_contract_hook_lineage",
            "outer_continuation_commit_state",
            "downstream_protocol_consumer_identity",
            "effective_reentrancy_state_capability",
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
            self.assertRegex(scenario["evidence_level"], r"\bSCR[0-5]\b")
            self.assertRegex(scenario["evidence_ceiling"], r"\bSCR[0-5]\b")

    def test_skill_is_registered_as_thirty_ninth_operator_depth_profile(self):
        payload = json.loads(PROFILES.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 2)
        profiles = payload["profiles"]
        self.assertGreaterEqual(len(profiles), 39)
        matching = [p for p in profiles if p["skill"] == "smart-contract-reentrancy-state-analysis"]
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
