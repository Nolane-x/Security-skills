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


def scored(contestant_id, fixture_id='case-1', category='review', score=100.0, digest=None):
    digest = digest or ({'case-1': 'a', 'case-2': 'b', 'case-3': 'c'}[fixture_id] * 64)
    return {
        'schema_version': 1,
        'contestant_id': contestant_id,
        'fixture_id': fixture_id,
        'category': category,
        'task_digest': digest,
        'score': float(score),
        'metrics': {'choice': float(score)},
        'rule_failures': [],
        'passed': True,
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

    def test_court_rejects_task_drift_between_contestants(self):
        court = load_module()
        results = [
            scored('contestant-a', digest='a' * 64),
            scored('contestant-b', digest='b' * 64),
        ]
        with self.assertRaises(ValueError):
            court.build_court('suite-1', ['case-1'], results)

    def test_absolute_superiority_requires_paired_and_category_dominance(self):
        court = load_module()
        results = [
            scored('contestant-a', 'case-1', 'scope', 100),
            scored('contestant-a', 'case-2', 'evidence', 100),
            scored('contestant-a', 'case-3', 'checks', 100),
            scored('contestant-b', 'case-1', 'scope', 100),
            scored('contestant-b', 'case-2', 'evidence', 80),
            scored('contestant-b', 'case-3', 'checks', 80),
        ]
        result = court.build_court('suite-1', ['case-1', 'case-2', 'case-3'], results)
        self.assertEqual(result['absolute_winner'], 'contestant-a')
        pair = result['pairwise'][0]
        self.assertEqual(pair['verdict'], 'left-absolute-superiority')
        self.assertEqual(pair['fixture_wins'], {'left': 2, 'right': 0, 'ties': 1})
        self.assertTrue(pair['left_no_category_regression'])
        self.assertTrue(pair['absolute_superiority'])

    def test_higher_average_with_category_regression_is_not_absolute(self):
        court = load_module()
        results = [
            scored('contestant-a', 'case-1', 'scope', 100),
            scored('contestant-a', 'case-2', 'evidence', 100),
            scored('contestant-a', 'case-3', 'checks', 70),
            scored('contestant-b', 'case-1', 'scope', 80),
            scored('contestant-b', 'case-2', 'evidence', 80),
            scored('contestant-b', 'case-3', 'checks', 90),
        ]
        result = court.build_court('suite-1', ['case-1', 'case-2', 'case-3'], results)
        self.assertIsNone(result['absolute_winner'])
        pair = result['pairwise'][0]
        self.assertEqual(pair['verdict'], 'left-score-lead')
        self.assertFalse(pair['left_no_category_regression'])
        self.assertFalse(pair['absolute_superiority'])


if __name__ == '__main__':
    unittest.main()
