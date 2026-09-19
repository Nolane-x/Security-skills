import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASELINE = json.loads((ROOT / "release-baseline.json").read_text(encoding="utf-8"))
COUNTS = BASELINE["counts"]


class Wave10ClosureTests(unittest.TestCase):
    def test_architecture_counts_match_release_authority(self):
        skills = sorted((ROOT / "skills").glob("*/SKILL.md"))
        packs = sorted((ROOT / "packs").glob("*.json"))
        registry = json.loads(
            (ROOT / "operator-depth" / "profiles.json").read_text(encoding="utf-8")
        )
        profiles = registry["profiles"]

        self.assertEqual(len(skills), COUNTS["canonical_skills"])
        self.assertEqual(len(packs), COUNTS["packs"])
        self.assertEqual(
            registry["version"], BASELINE["operator_depth_registry_version"]
        )
        self.assertEqual(len(profiles), COUNTS["operator_depth_profiles"])

        skill_names = {path.parent.name for path in skills}
        profile_names = [profile["skill"] for profile in profiles]

        self.assertEqual(len(profile_names), len(set(profile_names)))
        self.assertTrue(set(profile_names).issubset(skill_names))

    def test_registered_depth_artifacts_exist_and_remain_lab_only(self):
        registry = json.loads(
            (ROOT / "operator-depth" / "profiles.json").read_text(encoding="utf-8")
        )

        for profile in registry["profiles"]:
            with self.subTest(skill=profile["skill"]):
                self.assertIs(profile["lab_only"], True)
                skill_dir = ROOT / "skills" / profile["skill"]
                self.assertTrue((skill_dir / profile["runbook"]).is_file())
                self.assertTrue((skill_dir / profile["scenario_matrix"]).is_file())

    def test_published_documents_publish_release_authority(self):
        for name in BASELINE["published_release_documents"]:
            text = (ROOT / name).read_text(encoding="utf-8")
            with self.subTest(readme=name):
                for token in BASELINE["required_readme_tokens"]:
                    self.assertIn(token, text)

    def test_apache_2_license_is_present(self):
        self.assertEqual(BASELINE["license"], "Apache-2.0")
        text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("Apache License", text)
        self.assertIn("Version 2.0, January 2004", text)
        self.assertIn("TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION", text)
        self.assertIn("END OF TERMS AND CONDITIONS", text)


if __name__ == "__main__":
    unittest.main()
