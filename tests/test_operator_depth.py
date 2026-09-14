import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_operator_depth.py"

REQUIRED_SECTIONS = [
    "Attack surface",
    "Hypothesis matrix",
    "Controlled validation",
    "False-positive controls",
    "Evidence capture",
    "Remediation checks",
]


def run_validator(root: Path):
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(root)],
        text=True,
        capture_output=True,
    )


def scenario(scenario_id: str):
    return {
        "id": scenario_id,
        "hypothesis": "A synthetic principal may cross the modeled trust boundary.",
        "safe_oracle": "Observe a synthetic marker in a controlled test sink.",
        "positive_control": "Expected allowed synthetic request reaches the test sink.",
        "negative_control": "Expected denied synthetic request does not reach the test sink.",
        "stop_condition": "Stop before any production, third-party, or unauthorized target.",
        "remediation_oracle": "The denied synthetic path stays blocked while the allowed control still works.",
    }


def make_fixture(
    root: Path,
    *,
    runbook="references/operator-runbook.md",
    scenario_matrix="references/operator-scenarios.json",
    sections=None,
):
    sections = sections or REQUIRED_SECTIONS
    skill = root / "skills" / "fixture-skill"
    (skill / "references").mkdir(parents=True)
    (root / "operator-depth").mkdir()
    (skill / "SKILL.md").write_text(
        "---\nname: fixture-skill\ndescription: test\n---\n"
        "# Fixture\n\n## Operator depth\n"
        "See [operator runbook](references/operator-runbook.md).\n",
        encoding="utf-8",
    )
    manifest = {
        "version": 2,
        "profiles": [
            {
                "skill": "fixture-skill",
                "runbook": runbook,
                "scenario_matrix": scenario_matrix,
                "lab_only": True,
                "required_runbook_sections": sections,
            }
        ],
    }
    (root / "operator-depth" / "profiles.json").write_text(
        json.dumps(manifest), encoding="utf-8"
    )
    return skill


def write_complete_scenarios(path: Path, scenarios=None):
    payload = {
        "version": 1,
        "scenarios": scenarios
        or [scenario("boundary-a"), scenario("boundary-b"), scenario("boundary-c")],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def write_complete_runbook(path: Path):
    body = [
        "# Runbook",
        "",
        "Authorized lab only. Evidence must include controls.",
        "",
        "Scenario matrix: `references/operator-scenarios.json`.",
        "",
    ]
    for section in REQUIRED_SECTIONS:
        body.extend([f"## {section}", f"Evidence and control notes for {section}.", ""])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(body), encoding="utf-8")


class OperatorDepthCliTests(unittest.TestCase):
    def test_repository_contract_passes(self):
        proc = run_validator(ROOT)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_rejects_missing_runbook(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            skill = make_fixture(root)
            write_complete_scenarios(skill / "references" / "operator-scenarios.json")
            proc = run_validator(root)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("missing runbook", (proc.stdout + proc.stderr).lower())

    def test_rejects_runbook_path_escape(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            skill = make_fixture(root, runbook="../outside.md")
            write_complete_scenarios(skill / "references" / "operator-scenarios.json")
            proc = run_validator(root)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("escapes skill directory", (proc.stdout + proc.stderr).lower())

    def test_rejects_skill_path_escape(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            escaped = root / "escaped-skill"
            write_complete_runbook(escaped / "references" / "operator-runbook.md")
            write_complete_scenarios(escaped / "references" / "operator-scenarios.json")
            (escaped / "SKILL.md").write_text(
                "---\nname: escaped-skill\ndescription: test\n---\n"
                "# Escaped\n\n## Operator depth\n"
                "See [operator runbook](references/operator-runbook.md).\n",
                encoding="utf-8",
            )
            (root / "skills").mkdir()
            (root / "operator-depth").mkdir()
            manifest = {
                "version": 2,
                "profiles": [
                    {
                        "skill": "../escaped-skill",
                        "runbook": "references/operator-runbook.md",
                        "scenario_matrix": "references/operator-scenarios.json",
                        "lab_only": True,
                        "required_runbook_sections": REQUIRED_SECTIONS,
                    }
                ],
            }
            (root / "operator-depth" / "profiles.json").write_text(
                json.dumps(manifest), encoding="utf-8"
            )
            proc = run_validator(root)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("skill path escapes skills directory", (proc.stdout + proc.stderr).lower())

    def test_rejects_missing_required_section(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            skill = make_fixture(root)
            write_complete_scenarios(skill / "references" / "operator-scenarios.json")
            (skill / "references" / "operator-runbook.md").write_text(
                "# Runbook\n\nAuthorized lab only. Evidence must include controls.\n\n"
                "Scenario matrix: `references/operator-scenarios.json`.\n\n"
                "## Attack surface\nA\n"
                "## Hypothesis matrix\nB\n"
                "## Controlled validation\nC\n"
                "## False-positive controls\nD\n"
                "## Evidence capture\nE\n",
                encoding="utf-8",
            )
            proc = run_validator(root)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("remediation checks", (proc.stdout + proc.stderr).lower())

    def test_rejects_missing_scenario_matrix(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            skill = make_fixture(root)
            write_complete_runbook(skill / "references" / "operator-runbook.md")
            proc = run_validator(root)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("missing scenario matrix", (proc.stdout + proc.stderr).lower())

    def test_rejects_scenario_path_escape(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            skill = make_fixture(root, scenario_matrix="../outside.json")
            write_complete_runbook(skill / "references" / "operator-runbook.md")
            proc = run_validator(root)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("scenario matrix path escapes skill directory", (proc.stdout + proc.stderr).lower())

    def test_rejects_duplicate_scenario_ids(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            skill = make_fixture(root)
            write_complete_runbook(skill / "references" / "operator-runbook.md")
            write_complete_scenarios(
                skill / "references" / "operator-scenarios.json",
                [scenario("duplicate"), scenario("duplicate"), scenario("third")],
            )
            proc = run_validator(root)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("duplicate scenario id", (proc.stdout + proc.stderr).lower())

    def test_rejects_missing_scenario_control(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            skill = make_fixture(root)
            write_complete_runbook(skill / "references" / "operator-runbook.md")
            scenarios = [scenario("a"), scenario("b"), scenario("c")]
            scenarios[1]["negative_control"] = ""
            write_complete_scenarios(skill / "references" / "operator-scenarios.json", scenarios)
            proc = run_validator(root)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("negative_control", (proc.stdout + proc.stderr).lower())

    def test_rejects_unsafe_scenario_oracle(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            skill = make_fixture(root)
            write_complete_runbook(skill / "references" / "operator-runbook.md")
            scenarios = [scenario("a"), scenario("b"), scenario("c")]
            scenarios[0]["safe_oracle"] = "Demonstrate impact."
            write_complete_scenarios(skill / "references" / "operator-scenarios.json", scenarios)
            proc = run_validator(root)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("safe_oracle", (proc.stdout + proc.stderr).lower())


if __name__ == "__main__":
    unittest.main()
