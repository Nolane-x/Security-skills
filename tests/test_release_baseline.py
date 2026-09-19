import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_release_baseline.py"


def run_validator(root: Path):
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(root)],
        text=True,
        capture_output=True,
    )


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def make_fixture(root: Path) -> None:
    skill_dir = root / "skills" / "fixture-skill"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("# Fixture\n", encoding="utf-8")

    (root / "packs").mkdir()
    write_json(root / "packs" / "fixture.json", {"name": "fixture"})

    write_json(
        root / "operator-depth" / "profiles.json",
        {
            "version": 2,
            "profiles": [
                {
                    "skill": "fixture-skill",
                    "lab_only": True,
                }
            ],
        },
    )

    fixture_path = root / "benchmarks" / "cases" / "fixture.json"
    write_json(fixture_path, {"id": "fixture"})
    for name in ("core", "portability"):
        write_json(
            root / "benchmarks" / "suites" / f"{name}.json",
            {
                "schema_version": 1,
                "name": name,
                "fixtures": ["cases/fixture.json"],
            },
        )

    readme_text = "Wave 10\n1\nApache-2.0\n"
    for name in ("README.md", "README-VN.md", "README-CN.md"):
        (root / name).write_text(readme_text, encoding="utf-8")

    (root / "LICENSE").write_text(
        "Apache License\n"
        "Version 2.0, January 2004\n"
        "TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION\n"
        "END OF TERMS AND CONDITIONS\n",
        encoding="utf-8",
    )
    (root / "SECURITY.md").write_text("# Security\n", encoding="utf-8")
    (root / "CONTRIBUTING.md").write_text("# Contributing\n", encoding="utf-8")
    (root / "docs").mkdir()
    (root / "docs" / "wave10-closure-audit.md").write_text(
        "Wave 10\n1\nApache-2.0\n", encoding="utf-8"
    )
    (root / "docs" / "repository-metadata.md").write_text(
        "Wave 10\n1\nApache-2.0\n", encoding="utf-8"
    )

    write_json(
        root / "release-baseline.json",
        {
            "schema_version": 1,
            "release": "test-closure",
            "status": "closed",
            "counts": {
                "canonical_skills": 1,
                "packs": 1,
                "operator_depth_profiles": 1,
                "benchmark_core_fixtures": 1,
                "benchmark_portability_fixtures": 1,
            },
            "operator_depth_registry_version": 2,
            "license": "Apache-2.0",
            "published_release_documents": [
                "README.md",
                "README-VN.md",
                "README-CN.md",
                "docs/repository-metadata.md",
                "docs/wave10-closure-audit.md",
            ],
            "required_readme_tokens": ["Wave 10", "1", "Apache-2.0"],
            "required_paths": [
                "LICENSE",
                "SECURITY.md",
                "CONTRIBUTING.md",
                "operator-depth/profiles.json",
                "benchmarks/suites/core.json",
                "benchmarks/suites/portability.json",
                "docs/wave10-closure-audit.md",
            ],
        },
    )


class ReleaseBaselineValidatorTests(unittest.TestCase):
    def test_repository_contract_passes(self):
        proc = run_validator(ROOT)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("Release baseline validation passed", proc.stdout)

    def test_rejects_canonical_skill_count_drift(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            make_fixture(root)
            (root / "skills" / "fixture-skill" / "SKILL.md").unlink()
            proc = run_validator(root)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("canonical skill count drifted", proc.stderr)

    def test_rejects_benchmark_fixture_count_drift(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            make_fixture(root)
            suite_path = root / "benchmarks" / "suites" / "core.json"
            suite = json.loads(suite_path.read_text(encoding="utf-8"))
            suite["fixtures"].append("cases/fixture.json")
            write_json(suite_path, suite)
            proc = run_validator(root)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("core benchmark fixture count drifted", proc.stderr)
            self.assertIn("core benchmark fixtures must be unique", proc.stderr)

    def test_rejects_public_readme_drift(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            make_fixture(root)
            (root / "README-VN.md").write_text("Wave 10\n1\n", encoding="utf-8")
            proc = run_validator(root)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn(
                "README-VN.md is missing release-baseline token 'Apache-2.0'",
                proc.stderr,
            )

    def test_rejects_incomplete_license(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            make_fixture(root)
            (root / "LICENSE").write_text("Apache License\n", encoding="utf-8")
            proc = run_validator(root)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("root LICENSE is missing Apache-2.0 marker", proc.stderr)

    def test_rejects_open_release_status(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            make_fixture(root)
            baseline_path = root / "release-baseline.json"
            baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
            baseline["status"] = "active"
            write_json(baseline_path, baseline)
            proc = run_validator(root)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("release baseline status must be 'closed'", proc.stderr)


if __name__ == "__main__":
    unittest.main()
