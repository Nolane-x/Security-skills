import importlib.util
import json
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS_PATH = ROOT / 'superiority' / 'corpus.json'
SUITE_PATH = ROOT / 'superiority' / 'suites' / 'core.json'
MODULE_PATH = ROOT / 'scripts' / 'superiority_court.py'


def load_module():
    spec = importlib.util.spec_from_file_location('superiority_court', MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SuperiorityCorpusTests(unittest.TestCase):
    def test_core_corpus_is_balanced_and_oracle_free_tasks_are_buildable(self):
        self.assertTrue(CORPUS_PATH.is_file())
        self.assertTrue(SUITE_PATH.is_file())
        corpus = json.loads(CORPUS_PATH.read_text(encoding='utf-8'))
        suite = json.loads(SUITE_PATH.read_text(encoding='utf-8'))
        fixtures = corpus['fixtures']
        self.assertEqual(corpus['schema_version'], 1)
        self.assertEqual(len(fixtures), 12)
        ids = [item['fixture_id'] for item in fixtures]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(
            Counter(item['category'] for item in fixtures),
            Counter({'scope': 3, 'evidence': 3, 'checks': 3, 'resolution': 3}),
        )
        self.assertEqual(sorted(suite['fixture_ids']), sorted(ids))

        court = load_module()
        for fixture in fixtures:
            self.assertGreaterEqual(len(fixture['private_expected']), 4)
            self.assertTrue(fixture['rules'])
            self.assertGreaterEqual(float(fixture['minimum']), 0.0)
            task = court.build_task(fixture)
            serialized = json.dumps(task, sort_keys=True)
            self.assertNotIn('private_expected', serialized)
            self.assertNotIn('rules', serialized)
            self.assertNotIn('minimum', serialized)


if __name__ == '__main__':
    unittest.main()
