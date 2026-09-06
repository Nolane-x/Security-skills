import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from skilllib import parse_skill, validate_skill


VALID = """---
name: example-skill
description: "Analyze a safe example. Use when testing the validator."
metadata:
  nolane-security-category: foundation
  nolane-security-version: "1"
  nolane-security-authorization: not-applicable
---
# Example

## When to use
Use for tests.

## Preconditions
Use local fixtures.

## Workflow
1. Inspect input.
2. Produce evidence.

## Evidence contract
A deterministic assertion is evidence.

## Stop conditions
Stop if input is missing.

## Output
Return a concise report.
"""


class SkillLibTests(unittest.TestCase):
    def make_skill(self, text=VALID, dirname="example-skill"):
        td = tempfile.TemporaryDirectory()
        path = Path(td.name) / "skills" / dirname / "SKILL.md"
        path.parent.mkdir(parents=True)
        path.write_text(text, encoding="utf-8")
        self.addCleanup(td.cleanup)
        return path

    def test_parse_skill_reads_metadata(self):
        skill = parse_skill(self.make_skill())
        self.assertEqual(skill.name, "example-skill")
        self.assertEqual(skill.metadata["nolane-security-category"], "foundation")
        self.assertEqual(skill.metadata["nolane-security-authorization"], "not-applicable")

    def test_validate_accepts_contract(self):
        path = self.make_skill()
        skill = parse_skill(path)
        issues = validate_skill(skill, path.parents[2])
        self.assertEqual([], [i for i in issues if i.level == "error"])

    def test_validate_rejects_directory_name_mismatch(self):
        path = self.make_skill(dirname="wrong-dir")
        issues = validate_skill(parse_skill(path), path.parents[2])
        self.assertTrue(any("directory" in i.message.lower() for i in issues))

    def test_validate_rejects_missing_required_section(self):
        path = self.make_skill(VALID.replace("## Evidence contract\nA deterministic assertion is evidence.\n\n", ""))
        issues = validate_skill(parse_skill(path), path.parents[2])
        self.assertTrue(any("Evidence contract" in i.message for i in issues))

    def test_validate_rejects_experimental_allowed_tools(self):
        text = VALID.replace(
            "metadata:\n",
            "allowed-tools: Bash(git:*)\nmetadata:\n",
        )
        path = self.make_skill(text)
        issues = validate_skill(parse_skill(path), path.parents[2])
        self.assertTrue(any("allowed-tools" in i.message for i in issues))


if __name__ == "__main__":
    unittest.main()
