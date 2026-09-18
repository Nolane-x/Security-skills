import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "file-upload-processing-analysis" / "SKILL.md"
RUNBOOK = ROOT / "skills" / "file-upload-processing-analysis" / "references" / "operator-runbook.md"
CASES = ROOT / "skills" / "file-upload-processing-analysis" / "references" / "operator-review-cases.json"
PROFILES = ROOT / "operator-depth" / "profiles.json"


class FileUploadProcessingDepthTests(unittest.TestCase):
    def test_skill_exposes_causal_upload_pipeline_model(self):
        text = SKILL.read_text(encoding="utf-8")
        for section in (
            "## Causal upload-pipeline model",
            "## Upload transaction, principal, and artifact generations",
            "## Representation and classification binding",
            "## Validation, scanning, and quarantine binding",
            "## Parser, delegate, transformation, and derived-artifact provenance",
            "## Storage promotion, object-version, and serving binding",
            "## Cleanup, derivative, and lifecycle binding",
            "## Consumer and bounded-effect binding",
            "## Upload-pipeline evidence ladder",
            "## Counterfactual upload controls",
            "## Alternative explanations",
            "## Evidence ceiling",
        ):
            self.assertIn(section, text)

        lower = text.lower()
        for concept in (
            "uploader principal/tenant identity",
            "upload request/transaction identity/generation",
            "fixture/content hash",
            "raw artifact identity/generation",
            "client filename representation",
            "declared content-type/extension metadata",
            "normalized name/storage-key result",
            "temporary/quarantine object identity/generation",
            "classification/sniff identity/generation",
            "validator/scanner identity/version",
            "validator/scanner verdict generation",
            "parser/delegate identity/version",
            "transform/extraction identity/generation",
            "derived artifact/child identity/generation",
            "promotion decision identity/generation",
            "permanent storage object/key/version",
            "metadata-to-bytes binding",
            "serving/download policy identity/generation",
            "serving origin/content-type/disposition identity",
            "authorization/tenant binding",
            "cleanup/tombstone lifecycle generation",
            "downstream consumer identity",
            "effective upload-pipeline capability",
            "bounded result",
            "receipt/result",
            "upload request accepted != artifact validated",
            "artifact validated != artifact promoted",
            "artifact promoted != artifact served",
            "served artifact != executable active content by assumption",
            "client filename != canonical storage identity",
            "normalized path != authorized storage namespace by assumption",
            "generated object key != tenant authorization",
            "same filename != same artifact generation",
            "same content hash != same metadata/serving policy generation",
            "declared mime != observed content type",
            "extension match != content validation",
            "magic-byte match != complete format safety",
            "content sniffing != parser validation",
            "validator success != downstream delegate safety",
            "scanner clean verdict != unchanged bytes",
            "clean original != clean transformed derivative",
            "clean parent archive != clean extracted child",
            "parser success != safe serving policy",
            "parser crash != code execution",
            "converter invocation != unsafe delegate effect",
            "harmless malformed fixture != active payload",
            "temporary storage != quarantine guarantee",
            "quarantine flag != immutable quarantined bytes",
            "validation receipt != current artifact generation",
            "transformed artifact != validated original by inheritance",
            "derived preview != source artifact identity",
            "archive child path != final canonical storage identity",
            "object-store write success != intended object/version selected",
            "permanent storage != public accessibility",
            "public url != authorization bypass by itself",
            "inline serving != active-content execution by assumption",
            "attachment disposition != safe content type by itself",
            "cache hit != current serving-policy generation",
            "cleanup requested != object inaccessible",
            "tombstone written != all replicas/derivatives removed",
            "duplicate upload != duplicate object effect by assumption",
            "oversized metadata != resource-exhaustion proof",
            "local benign policy difference != production exploitability",
            "upl0",
            "upl1",
            "upl2",
            "upl3",
            "upl4",
            "upl5",
            "counterfactual",
            "alternative explanation",
            "evidence ceiling",
            "local/owned/sandboxed",
        ):
            self.assertIn(concept, lower)

    def test_runbook_requires_upload_generation_reasoning(self):
        self.assertTrue(RUNBOOK.is_file(), "upload operator runbook must exist before depth can pass")
        text = RUNBOOK.read_text(encoding="utf-8")
        for section in (
            "## Attack surface",
            "## Hypothesis matrix",
            "## Upload/principal/artifact-generation trace",
            "## Representation/classification trace",
            "## Validation/scanning/quarantine trace",
            "## Parser/delegate/derived-artifact trace",
            "## Storage/object-version/serving trace",
            "## Cleanup/derivative lifecycle trace",
            "## Consumer/bounded-effect trace",
            "## Controlled validation",
            "## False-positive controls",
            "## Counterfactual upload controls",
            "## Alternative explanations",
            "## Evidence capture",
            "## Evidence promotion and ceiling",
            "## Remediation checks",
        ):
            self.assertIn(section, text)

        lower = text.lower()
        for phrase in (
            "upload transaction",
            "artifact generation",
            "classification",
            "quarantine",
            "scanner verdict",
            "derived artifact",
            "object version",
            "serving policy",
            "cleanup",
            "tombstone",
            "synthetic",
            "mock",
            "read-only",
            "counterfactual",
            "alternative explanation",
            "evidence ceiling",
            "upl5",
        ):
            self.assertIn(phrase, lower)

    def test_review_cases_encode_upload_pipeline_reasoning(self):
        self.assertTrue(CASES.is_file(), "upload review-case matrix must exist before depth can pass")
        payload = json.loads(CASES.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 1)
        self.assertGreaterEqual(len(payload["scenarios"]), 4)

        required_ids = {
            "scanner-verdict-reused-after-artifact-generation-change",
            "derived-preview-inherits-source-verdict-without-revalidation",
            "declared-mime-sniffed-type-serving-policy-mismatch",
            "cleanup-removes-source-but-leaves-served-derivative-generation",
        }
        self.assertTrue(required_ids.issubset({scenario["id"] for scenario in payload["scenarios"]}))

        required = (
            "hypothesis",
            "safe_oracle",
            "positive_control",
            "negative_control",
            "stop_condition",
            "remediation_oracle",
            "upload_principal_artifact_generation",
            "representation_classification_trace",
            "validation_scanning_quarantine_state",
            "parser_delegate_derived_artifact",
            "storage_object_version_serving_state",
            "cleanup_derivative_lifecycle",
            "consumer_bounded_effect",
            "downstream_consumer_identity",
            "effective_upload_pipeline_capability",
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
            self.assertRegex(scenario["evidence_level"], r"\bUPL[0-5]\b")
            self.assertRegex(scenario["evidence_ceiling"], r"\bUPL[0-5]\b")

    def test_skill_is_registered_as_thirty_sixth_operator_depth_profile(self):
        payload = json.loads(PROFILES.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 2)
        profiles = payload["profiles"]
        self.assertEqual(len(profiles), 36)
        matching = [p for p in profiles if p["skill"] == "file-upload-processing-analysis"]
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
