import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "oracle-and-external-data-trust-analysis" / "SKILL.md"
RUNBOOK = ROOT / "skills" / "oracle-and-external-data-trust-analysis" / "references" / "operator-runbook.md"
CASES = ROOT / "skills" / "oracle-and-external-data-trust-analysis" / "references" / "operator-review-cases.json"
PROFILES = ROOT / "operator-depth" / "profiles.json"


class OracleExternalDataTrustDepthTests(unittest.TestCase):
    def test_skill_exposes_causal_external_data_model(self):
        text = SKILL.read_text(encoding="utf-8")
        for section in (
            "## Causal external-data trust model",
            "## Datum class, trust property, and source generations",
            "## Round, timestamp, heartbeat, and freshness binding",
            "## Unit, decimal, scale, and normalization binding",
            "## Aggregation, source diversity, and quorum binding",
            "## Fallback, emergency, and liveness-state binding",
            "## Authenticity, replay, and origin-domain binding",
            "## Consumer snapshot and invariant-reference binding",
            "## External-data evidence ladder",
            "## Counterfactual external-data controls",
            "## Alternative explanations",
            "## Evidence ceiling",
        ):
            self.assertIn(section, text)

        lower = text.lower()
        for concept in (
            "datum class",
            "required trust property",
            "source/provider identity",
            "source/provider generation",
            "source-set/quorum identity/generation",
            "feed/configuration identity/generation",
            "observation/round identity",
            "observation generation",
            "publication timestamp",
            "retrieval/consumption timestamp",
            "heartbeat/freshness policy identity/generation",
            "unit/decimal/scale identity/generation",
            "normalization transform identity",
            "aggregation algorithm/configuration generation",
            "fallback/emergency-path identity/generation",
            "sequencer/liveness state generation",
            "origin chain/domain/contract/function identity",
            "authenticity/verifier identity/generation",
            "replay/order identity",
            "normalized external datum",
            "consumer snapshot/state generation",
            "downstream consumer identity",
            "consuming invariant reference",
            "effective external-data-trust capability",
            "bounded result",
            "receipt/result",
            "external datum accepted != external datum trusted for every consumer",
            "source configured != source observed at the consuming generation",
            "source identity != source-set/quorum identity",
            "authenticated source != fresh source",
            "fresh timestamp != fresh economic state by assumption",
            "heartbeat configured != heartbeat enforced",
            "round advanced != value current for the consuming snapshot",
            "timestamp monotonicity != round semantic validity",
            "nonzero value != valid value",
            "positive value != valid domain value",
            "source disagreement != aggregation failure by itself",
            "quorum met != independent source diversity",
            "multiple adapters != multiple independent data origins",
            "fallback available != fallback equivalent in trust guarantees",
            "fallback activation != safe downgrade",
            "primary failure != authorization to weaken freshness/source diversity",
            "unit label != unit binding",
            "decimal metadata != normalized-value correctness",
            "scale conversion != economic correctness",
            "normalized numeric mismatch != bounds/integer root cause by assumption",
            "stale oracle input != invariant violation until a consumer decision is bound",
            "threshold crossing != economic exploitability",
            "local synthetic consequence != real-market manipulability",
            "signed datum != intended domain/chain/contract/function binding",
            "signature valid != current round/freshness authorized",
            "cross-chain message valid != source-domain state current",
            "bridge relay success != final external-data trust decision",
            "sequencer up != sequencer state sufficiently aged for use",
            "sequencer down != all external data invalid by assumption",
            "randomness beacon output != randomness-lifecycle proof",
            "replayed datum != duplicate downstream effect by assumption",
            "cached datum != stale datum unless cache generation and policy are bound",
            "consumer read != immutable consumer snapshot",
            "same feed address != same configuration generation",
            "emergency override != production trust equivalence",
            "code-level trust assumption != price manipulability",
            "suspicious price != oracle compromise",
            "crash/revert != external-data trust failure",
            "oed0",
            "oed1",
            "oed2",
            "oed3",
            "oed4",
            "oed5",
            "counterfactual",
            "alternative explanation",
            "evidence ceiling",
            "local/owned/sandboxed",
        ):
            self.assertIn(concept, lower)

    def test_runbook_requires_external_data_generation_reasoning(self):
        self.assertTrue(RUNBOOK.is_file(), "external-data operator runbook must exist before depth can pass")
        text = RUNBOOK.read_text(encoding="utf-8")
        for section in (
            "## Attack surface",
            "## Hypothesis matrix",
            "## Datum/source/configuration-generation trace",
            "## Round/freshness/heartbeat trace",
            "## Unit/decimal/normalization trace",
            "## Aggregation/source-diversity/quorum trace",
            "## Fallback/liveness-state trace",
            "## Authenticity/replay/origin-domain trace",
            "## Consumer-snapshot/invariant-reference trace",
            "## Controlled validation",
            "## False-positive controls",
            "## Counterfactual external-data controls",
            "## Alternative explanations",
            "## Evidence capture",
            "## Evidence promotion and ceiling",
            "## Remediation checks",
        ):
            self.assertIn(section, text)

        lower = text.lower()
        for phrase in (
            "source generation",
            "configuration generation",
            "round",
            "freshness",
            "heartbeat",
            "decimal",
            "normalization",
            "source diversity",
            "quorum",
            "fallback",
            "liveness",
            "origin domain",
            "consumer snapshot",
            "synthetic",
            "mock",
            "read-only",
            "counterfactual",
            "alternative explanation",
            "evidence ceiling",
            "oed5",
        ):
            self.assertIn(phrase, lower)

    def test_review_cases_encode_external_data_reasoning(self):
        self.assertTrue(CASES.is_file(), "external-data review-case matrix must exist before depth can pass")
        payload = json.loads(CASES.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 1)
        self.assertGreaterEqual(len(payload["scenarios"]), 4)

        required_ids = {
            "stale-round-after-heartbeat-generation-change",
            "decimal-configuration-generation-drift",
            "fallback-source-diversity-downgrade",
            "cross-domain-report-binding-mismatch",
        }
        self.assertTrue(required_ids.issubset({scenario["id"] for scenario in payload["scenarios"]}))

        required = (
            "hypothesis",
            "safe_oracle",
            "positive_control",
            "negative_control",
            "stop_condition",
            "remediation_oracle",
            "datum_source_configuration_generation",
            "round_freshness_heartbeat_trace",
            "unit_decimal_normalization_state",
            "aggregation_source_diversity_quorum",
            "fallback_liveness_state",
            "authenticity_replay_origin_domain",
            "consumer_snapshot_invariant_reference",
            "downstream_consumer_identity",
            "effective_external_data_trust_capability",
            "bounded_result",
            "receipt_result_binding",
            "counterfactual_control",
            "alternative_explanation",
            "evidence_level",
            "evidence_ceiling",
        )
        safe_terms = ("synthetic", "mock", "inert", "read-only", "controlled", "fake", "local")
        for scenario in payload["scenarios"]:
            for field in required:
                self.assertIn(field, scenario)
                self.assertIsInstance(scenario[field], str)
                self.assertGreaterEqual(len(scenario[field].strip()), 40)
            self.assertTrue(any(term in scenario["safe_oracle"].lower() for term in safe_terms))
            self.assertTrue(any(term in scenario["stop_condition"].lower() for term in ("stop", "abort", "do not proceed")))
            self.assertRegex(scenario["evidence_level"], r"\bOED[0-5]\b")
            self.assertRegex(scenario["evidence_ceiling"], r"\bOED[0-5]\b")

    def test_skill_is_registered_as_thirty_fifth_operator_depth_profile(self):
        payload = json.loads(PROFILES.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 2)
        profiles = payload["profiles"]
        self.assertGreaterEqual(len(profiles), 35)
        matching = [p for p in profiles if p["skill"] == "oracle-and-external-data-trust-analysis"]
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
