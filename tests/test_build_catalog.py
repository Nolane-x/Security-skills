import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_catalog.py"

SKILL = """---
name: alpha-skill
description: "Alpha description."
metadata:
  nolane-security-category: foundation
  nolane-security-version: "1"
  nolane-security-authorization: not-applicable
---
# Alpha

## When to use
Testing.

## Preconditions
Local only.

## Workflow
1. Test.

## Evidence contract
Deterministic output.

## Stop conditions
Stop on invalid input.

## Output
Report.
"""


class CatalogTests(unittest.TestCase):
    def test_catalog_generation_is_deterministic_and_checkable(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            p = root / "skills" / "alpha-skill" / "SKILL.md"
            p.parent.mkdir(parents=True)
            p.write_text(SKILL, encoding="utf-8")

            first = subprocess.run(
                [sys.executable, str(SCRIPT), "--root", str(root)],
                text=True,
                capture_output=True,
            )
            self.assertEqual(first.returncode, 0, first.stderr)

            catalog = json.loads((root / "catalog.json").read_text(encoding="utf-8"))
            self.assertEqual(["alpha-skill"], [x["name"] for x in catalog["skills"]])

            before = (root / "CATALOG.md").read_text(encoding="utf-8")
            second = subprocess.run(
                [sys.executable, str(SCRIPT), "--root", str(root)],
                text=True,
                capture_output=True,
            )
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertEqual(before, (root / "CATALOG.md").read_text(encoding="utf-8"))

            check = subprocess.run(
                [sys.executable, str(SCRIPT), "--root", str(root), "--check"],
                text=True,
                capture_output=True,
            )
            self.assertEqual(check.returncode, 0, check.stderr)


if __name__ == "__main__":
    unittest.main()
