import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'scripts'
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import prepare_agent_tasks  # noqa: E402
import validate_agent_runs  # noqa: E402
from agent_run import semantic_output_digest  # noqa: E402
from agent_task import build_agent_task  # noqa: E402


class AgentCliTests(unittest.TestCase):
    def test_prepare_agent_tasks_cli_writes_portability_tasks(self):
        suite = ROOT / 'benchmarks' / 'suites' / 'portability.json'
        with tempfile.TemporaryDirectory() as tmp:
            rc = prepare_agent_tasks.main([str(suite), '--out', tmp])
            self.assertEqual(rc, 0)
            self.assertEqual(len(list(Path(tmp).glob('*.json'))), 12)

    def test_prepare_agent_tasks_cli_returns_two_for_missing_suite(self):
        with tempfile.TemporaryDirectory() as tmp:
            rc = prepare_agent_tasks.main([str(Path(tmp) / 'missing.json'), '--out', tmp])
            self.assertEqual(rc, 2)

    def test_validate_agent_runs_cli_accepts_valid_run_and_rejects_bad_run(self):
        fixture = json.loads((ROOT / 'benchmarks' / 'cases' / 'routing' / 'routing-memory-safety.json').read_text(encoding='utf-8'))
        task = build_agent_task(fixture)
        run = {
            'schema_version': 1,
            'benchmark_id': task['benchmark_id'],
            'agent': {'id': 'cli-agent'},
            'adapter': {'id': 'imported'},
            'task_digest': task['task_digest'],
            'decision': 'route',
            'case_valid': True,
            'declared_state': task['research_case']['state'],
            'selected_skills': ['security-scope-and-authorization'],
            'selected_packs': [],
            'issue_paths': [],
            'provenance': {'source': 'imported', 'output_digest': ''},
        }
        run['provenance']['output_digest'] = semantic_output_digest(run)
        with tempfile.TemporaryDirectory() as tmp:
            valid_path = Path(tmp) / 'valid.json'
            valid_path.write_text(json.dumps(run), encoding='utf-8')
            self.assertEqual(validate_agent_runs.main([str(valid_path)]), 0)
            run['selected_skills'] = ['no-such-skill']
            run['provenance']['output_digest'] = semantic_output_digest(run)
            bad_path = Path(tmp) / 'bad.json'
            bad_path.write_text(json.dumps(run), encoding='utf-8')
            self.assertEqual(validate_agent_runs.main([str(bad_path)]), 2)


if __name__ == '__main__':
    unittest.main()
