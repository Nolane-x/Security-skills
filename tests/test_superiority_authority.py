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


def fixture(fixture_id, *, minimum=80.0):
    return {
        'schema_version': 1,
        'fixture_id': fixture_id,
        'category': 'evidence',
        'task': {'text': f'Public task {fixture_id}'},
        'private_expected': {
            'scope_choice': 'allow',
            'evidence_level': 'observed',
            'next_step': 'collect',
            'claim_level': 'provisional',
            'checks': ['positive-check', 'negative-check'],
        },
        'rules': ['claim_level', 'scope_choice'],
        'minimum': minimum,
    }


class SuperiorityAuthorityTests(unittest.TestCase):
    def test_authority_commitment_is_stable_and_semantic(self):
        court = load_module()
        first = fixture('case-a')
        second = fixture('case-b', minimum=100.0)

        digest = court.build_authority_commitment('suite-1', [first, second])
        self.assertRegex(digest, r'^[0-9a-f]{64}$')

        reordered_first = copy.deepcopy(first)
        reordered_first['rules'].reverse()
        reordered_first['private_expected']['checks'].reverse()
        self.assertEqual(
            digest,
            court.build_authority_commitment('suite-1', [second, reordered_first]),
        )

    def test_authority_commitment_changes_on_private_authority_change(self):
        court = load_module()
        source = fixture('case-a')
        baseline = court.build_authority_commitment('suite-1', [source])

        answer_change = copy.deepcopy(source)
        answer_change['private_expected']['claim_level'] = 'validated'
        self.assertNotEqual(
            baseline,
            court.build_authority_commitment('suite-1', [answer_change]),
        )

        rule_change = copy.deepcopy(source)
        rule_change['rules'] = ['scope_choice']
        self.assertNotEqual(
            baseline,
            court.build_authority_commitment('suite-1', [rule_change]),
        )

        threshold_change = copy.deepcopy(source)
        threshold_change['minimum'] = 100.0
        self.assertNotEqual(
            baseline,
            court.build_authority_commitment('suite-1', [threshold_change]),
        )


if __name__ == '__main__':
    unittest.main()
