import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts' / 'score_superiority_runs.py'
SUITE = ROOT / 'superiority' / 'suites' / 'core.json'
CORPUS = ROOT / 'superiority' / 'corpus.json'
COURT_MODULE = ROOT / 'scripts' / 'superiority_court.py'


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SuperiorityScoreCliTests(unittest.TestCase):
    def test_reference_runs_score_to_one_hundred_deterministically(self):
        self.assertTrue(SCRIPT.is_file())
        scorer = load(SCRIPT, 'score_superiority_runs')
        court = load(COURT_MODULE, 'superiority_court_for_score_test')
        corpus = json.loads(CORPUS.read_text(encoding='utf-8'))
        fixtures = {item['fixture_id']: item for item in corpus['fixtures']}

        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            runs = base / 'runs'
            runs.mkdir()
            for fixture_id, fixture in fixtures.items():
                task = court.build_task(fixture)
                run = {
                    'schema_version': 1,
                    'fixture_id': fixture_id,
                    'contestant_id': 'opaque-a',
                    'task_digest': task['task_digest'],
                    'answers': fixture['private_expected'],
                }
                (runs / f'{fixture_id}.json').write_text(
                    json.dumps(run, sort_keys=True), encoding='utf-8'
                )

            out_a = base / 'scores-a.json'
            out_b = base / 'scores-b.json'
            self.assertEqual(scorer.main([str(SUITE), str(runs), '--json', str(out_a)]), 0)
            self.assertEqual(scorer.main([str(SUITE), str(runs), '--json', str(out_b)]), 0)
            self.assertEqual(out_a.read_bytes(), out_b.read_bytes())
            result = json.loads(out_a.read_text(encoding='utf-8'))
            self.assertEqual(result['contestant_id'], 'opaque-a')
            self.assertEqual(len(result['results']), 12)
            self.assertTrue(all(item['score'] == 100.0 for item in result['results']))
            self.assertTrue(all(item['passed'] for item in result['results']))


if __name__ == '__main__':
    unittest.main()
