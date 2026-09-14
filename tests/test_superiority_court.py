import copy
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


def sample_fixture():
    return {
        'schema_version': 1,
        'fixture_id': 'case-1',
        'category': 'review',
        'task': {'text': 'Classify this synthetic case.'},
        'private_expected': {
            'scope_choice': 'defer',
            'evidence_level': 'observed',
            'next_step': 'collect',
            'claim_level': 'provisional',
            'checks': ['negative-check', 'positive-check'],
        },
        'rules': ['scope_choice'],
        'minimum': 80.0,
    }


class SuperiorityCourtTests(unittest.TestCase):
    def test_court_module_exists(self):
        self.assertTrue(MODULE_PATH.is_file())

    def test_build_task_is_public_and_stable(self):
        court = load_module()
        source = sample_fixture()
        first = court.build_task(source)
        second = court.build_task(copy.deepcopy(source))
        self.assertEqual(first, second)
        self.assertNotIn('private_expected', first)
        self.assertNotIn('rules', first)
        self.assertNotIn('minimum', first)
        self.assertRegex(first['task_digest'], r'^[0-9a-f]{64}$')

    def test_score_run_is_deterministic_and_rules_fail_closed(self):
        court = load_module()
        source = sample_fixture()
        task = court.build_task(source)
        run = {
            'schema_version': 1,
            'fixture_id': source['fixture_id'],
            'contestant_id': 'contestant-a',
            'task_digest': task['task_digest'],
            'answers': copy.deepcopy(source['private_expected']),
        }
        correct = court.score_run(source, task, run)
        self.assertEqual(correct, court.score_run(source, task, copy.deepcopy(run)))
        self.assertEqual(correct['score'], 100.0)
        self.assertEqual(correct['rule_failures'], [])
        self.assertTrue(correct['passed'])

        wrong = copy.deepcopy(run)
        wrong['contestant_id'] = 'contestant-b'
        wrong['answers']['scope_choice'] = 'continue'
        rejected = court.score_run(source, task, wrong)
        self.assertIn('scope_choice', rejected['rule_failures'])
        self.assertFalse(rejected['passed'])


if __name__ == '__main__':
    unittest.main()
