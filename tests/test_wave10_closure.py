import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class Wave10ClosureTests(unittest.TestCase):
    def test_architecture_counts_are_frozen(self):
        skills = sorted((ROOT / "skills").glob("*/SKILL.md"))
        packs = sorted((ROOT / "packs").glob("*.json"))
        registry = json.loads(
            (ROOT / "operator-depth" / "profiles.json").read_text(encoding="utf-8")
        )
        profiles = registry["profiles"]

        self.assertEqual(len(skills), 83)
        self.assertEqual(len(packs), 20)
        self.assertEqual(registry["version"], 2)
        self.assertEqual(len(profiles), 40)

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

    def test_public_readmes_publish_one_wave10_baseline(self):
        required = (
            "83",
            "20",
            "40",
            "Wave 10",
            "Apache-2.0",
        )
        for name in ("README.md", "README-VN.md", "README-CN.md"):
            text = (ROOT / name).read_text(encoding="utf-8")
            with self.subTest(readme=name):
                for token in required:
                    self.assertIn(token, text)

    def test_apache_2_license_is_present(self):
        text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("Apache License", text)
        self.assertIn("Version 2.0, January 2004", text)
        self.assertIn("TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION", text)
        self.assertIn("END OF TERMS AND CONDITIONS", text)


if __name__ == "__main__":
    unittest.main()
