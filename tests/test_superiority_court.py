import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / 'scripts' / 'superiority_court.py'


def load_module():
    spec = importlib.util.spec_from_file_location('superiority_court', MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SuperiorityCourtTests(unittest.TestCase):
    def test_court_module_exists(self):
        self.assertTrue(MODULE_PATH.is_file())

    def test_build_task_is_public_and_stable(self):
        court = load_module()
        source = {
            'schema_version': 1,
            'fixture_id': 'case-1',
            'category': 'review',
            'task': {'text': 'Classify this synthetic case.'},
            'private_expected': {'choice': 'defer'},
            'rules': ['choice'],
            'minimum': 100.0,
        }
        first = court.build_task(source)
        second = court.build_task(dict(source))
        self.assertEqual(first, second)
        self.assertNotIn('private_expected', first)
        self.assertNotIn('rules', first)
        self.assertNotIn('minimum', first)
        self.assertRegex(first['task_digest'], r'^[0-9a-f]{64}$')


if __name__ == '__main__':
    unittest.main()
