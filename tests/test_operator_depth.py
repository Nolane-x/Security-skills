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


def make_fixture(root: Path, *, runbook="references/operator-runbook.md", sections=None):
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
        "version": 1,
        "profiles": [
            {
                "skill": "fixture-skill",
                "runbook": runbook,
                "lab_only": True,
                "required_runbook_sections": sections,
            }
        ],
    }
    (root / "operator-depth" / "profiles.json").write_text(
        json.dumps(manifest), encoding="utf-8"
    )
    return skill


class OperatorDepthCliTests(unittest.TestCase):
    def test_repository_contract_passes(self):
        proc = run_validator(ROOT)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_rejects_missing_runbook(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            make_fixture(root)
            proc = run_validator(root)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("missing runbook", (proc.stdout + proc.stderr).lower())

    def test_rejects_runbook_path_escape(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            make_fixture(root, runbook="../outside.md")
            proc = run_validator(root)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("escapes skill directory", (proc.stdout + proc.stderr).lower())

    def test_rejects_missing_required_section(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            skill = make_fixture(root)
            (skill / "references" / "operator-runbook.md").write_text(
                "# Runbook\n\nAuthorized lab only. Evidence must include controls.\n\n"
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


if __name__ == "__main__":
    unittest.main()
