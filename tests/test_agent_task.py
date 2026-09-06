import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'scripts'
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from agent_task import build_agent_task, canonical_json, task_digest  # noqa: E402
from prepare_agent_tasks import prepare_suite_tasks  # noqa: E402


FIXTURE = {
    'schema_version': 1,
    'benchmark_id': 'agent-task-fixture',
    'category': 'routing',
    'description': 'Synthetic fixture.',
    'case': {
        'schema_version': 1,
        'case_id': 'agent-task-case',
        'title': 'Synthetic task',
        'scope': {'authorized': True, 'kind': 'sandbox', 'target': 'synthetic-fixture'},
        'domains': ['parsers'],
        'goal': 'discover',
        'state': 'hypothesis',
        'claim': 'Synthetic claim.',
        'environment': {'target_revision': 'rev-a', 'platform': 'fixture'},
        'observations': [],
        'controls': {'positive': [], 'negative': []},
        'reproducer': {'steps': [], 'fixture_digest': ''},
        'root_cause': '',
        'security_consequence': '',
        'uncertainties': [],
        'fix_validation': {},
    },
    'expect': {
        'required_skills': ['oracle-secret-skill'],
        'forbidden_skills': ['oracle-forbidden-skill'],
        'required_issue_paths': ['oracle.issue.path'],
    },
    'weights': {'routing_recall': 9.0},
}


def all_keys(value):
    keys = set()
    if isinstance(value, dict):
        for key, child in value.items():
            keys.add(key)
            keys.update(all_keys(child))
    elif isinstance(value, list):
        for child in value:
            keys.update(all_keys(child))
    return keys


class AgentTaskTests(unittest.TestCase):
    def test_task_strips_all_oracle_fields(self):
        task = build_agent_task(copy.deepcopy(FIXTURE))
        dumped = canonical_json(task)
        self.assertNotIn('expect', task)
        self.assertNotIn('weights', task)
        self.assertNotIn('oracle-secret-skill', dumped)
        self.assertNotIn('oracle-forbidden-skill', dumped)
        self.assertNotIn('oracle.issue.path', dumped)
        self.assertEqual(task['research_case'], FIXTURE['case'])

    def test_task_digest_is_stable_and_self_excluding(self):
        first = build_agent_task(copy.deepcopy(FIXTURE))
        second = build_agent_task(copy.deepcopy(FIXTURE))
        self.assertEqual(first, second)
        digest = first['task_digest']
        self.assertEqual(len(digest), 64)
        payload = dict(first)
        payload.pop('task_digest')
        self.assertEqual(digest, task_digest(payload))

    def test_task_digest_changes_when_public_case_changes(self):
        first = build_agent_task(copy.deepcopy(FIXTURE))
        changed = copy.deepcopy(FIXTURE)
        changed['case']['claim'] = 'Different public claim.'
        second = build_agent_task(changed)
        self.assertNotEqual(first['task_digest'], second['task_digest'])

    def test_instructions_preserve_synthetic_scope_and_json_contract(self):
        task = build_agent_task(copy.deepcopy(FIXTURE))
        instructions = task['instructions'].lower()
        self.assertIn('synthetic', instructions)
        self.assertIn('authorized', instructions)
        self.assertIn('json', instructions)
        self.assertIn('no live', instructions)

    def test_real_portability_suite_prepares_twelve_sorted_tasks(self):
        suite_path = ROOT / 'benchmarks' / 'suites' / 'portability.json'
        with tempfile.TemporaryDirectory() as tmp:
            tasks = prepare_suite_tasks(ROOT, suite_path, Path(tmp))
            self.assertEqual(len(tasks), 12)
            ids = [x['benchmark_id'] for x in tasks]
            self.assertEqual(ids, sorted(ids))
            files = sorted(Path(tmp).glob('*.json'))
            self.assertEqual(len(files), 12)
            oracle_keys = {
                'expect', 'weights', 'required_skills', 'optional_skills', 'forbidden_skills',
                'required_packs', 'optional_packs', 'forbidden_packs', 'required_issue_paths',
                'hard_gates', 'minimum_score', 'route_limit', 'ordered_before',
            }
            for path in files:
                loaded = json.loads(path.read_text(encoding='utf-8'))
                self.assertIn('task_digest', loaded)
                self.assertTrue(oracle_keys.isdisjoint(all_keys(loaded)))


if __name__ == '__main__':
    unittest.main()
