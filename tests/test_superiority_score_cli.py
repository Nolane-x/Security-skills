import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts' / 'score_superiority_runs.py'
PREPARE = ROOT / 'scripts' / 'prepare_superiority_tasks.py'
SUITE = ROOT / 'superiority' / 'suites' / 'core.json'
CORPUS = ROOT / 'superiority' / 'corpus.json'
COURT_MODULE = ROOT / 'scripts' / 'superiority_court.py'
SURFACE_A = '1' * 64
SURFACE_B = '2' * 64


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_reference_runs(runs: Path, fixtures: dict, court, *, mixed_surface=False):
    for index, (fixture_id, fixture) in enumerate(sorted(fixtures.items())):
        task = court.build_task(fixture)
        run = {
            'schema_version': 1,
            'fixture_id': fixture_id,
            'contestant_id': 'opaque-a',
            'contestant_surface_digest': SURFACE_B if mixed_surface and index == 0 else SURFACE_A,
            'task_digest': task['task_digest'],
            'answers': fixture['private_expected'],
        }
        (runs / f'{fixture_id}.json').write_text(
            json.dumps(run, sort_keys=True), encoding='utf-8'
        )


def prepare_manifest(base: Path) -> Path:
    prepare = load(PREPARE, f'prepare_superiority_tasks_{base.name}')
    tasks = base / 'tasks'
    prepare.prepare_suite_tasks(ROOT, SUITE, tasks)
    return tasks / 'SUITE_MANIFEST.json'


class SuperiorityScoreCliTests(unittest.TestCase):
    def test_reference_runs_score_to_one_hundred_deterministically(self):
        self.assertTrue(SCRIPT.is_file())
        scorer = load(SCRIPT, 'score_superiority_runs')
        court = load(COURT_MODULE, 'superiority_court_for_score_test')
        corpus = json.loads(CORPUS.read_text(encoding='utf-8'))
        fixtures = {item['fixture_id']: item for item in corpus['fixtures']}

        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            manifest = prepare_manifest(base)
            runs = base / 'runs'
            runs.mkdir()
            write_reference_runs(runs, fixtures, court)

            out_a = base / 'scores-a.json'
            out_b = base / 'scores-b.json'
            argv = [str(SUITE), str(runs), '--manifest', str(manifest)]
            self.assertEqual(scorer.main([*argv, '--json', str(out_a)]), 0)
            self.assertEqual(scorer.main([*argv, '--json', str(out_b)]), 0)
            self.assertEqual(out_a.read_bytes(), out_b.read_bytes())
            result = json.loads(out_a.read_text(encoding='utf-8'))
            public_manifest = json.loads(manifest.read_text(encoding='utf-8'))
            self.assertEqual(result['contestant_id'], 'opaque-a')
            self.assertEqual(result['contestant_surface_digest'], SURFACE_A)
            self.assertEqual(result['authority_commitment'], public_manifest['authority_commitment'])
            self.assertEqual(len(result['results']), 12)
            self.assertTrue(all(item['score'] == 100.0 for item in result['results']))
            self.assertTrue(all(item['passed'] for item in result['results']))

    def test_scorer_rejects_missing_or_mixed_surface_digest(self):
        scorer = load(SCRIPT, 'score_superiority_runs_surface_test')
        court = load(COURT_MODULE, 'superiority_court_surface_test')
        corpus = json.loads(CORPUS.read_text(encoding='utf-8'))
        fixtures = {item['fixture_id']: item for item in corpus['fixtures']}

        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            manifest = prepare_manifest(base)
            mixed = base / 'mixed'
            mixed.mkdir()
            write_reference_runs(mixed, fixtures, court, mixed_surface=True)
            with self.assertRaises(ValueError):
                scorer.score_suite_runs(ROOT, SUITE, mixed, manifest)

            missing = base / 'missing'
            missing.mkdir()
            write_reference_runs(missing, fixtures, court)
            path = sorted(missing.glob('*.json'))[0]
            data = json.loads(path.read_text(encoding='utf-8'))
            data.pop('contestant_surface_digest')
            path.write_text(json.dumps(data, sort_keys=True), encoding='utf-8')
            with self.assertRaises(ValueError):
                scorer.score_suite_runs(ROOT, SUITE, missing, manifest)

    def test_scorer_rejects_authority_commitment_drift(self):
        scorer = load(SCRIPT, 'score_superiority_runs_authority_test')
        court = load(COURT_MODULE, 'superiority_court_authority_score_test')
        corpus = json.loads(CORPUS.read_text(encoding='utf-8'))
        fixtures = {item['fixture_id']: item for item in corpus['fixtures']}

        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            manifest = prepare_manifest(base)
            runs = base / 'runs'
            runs.mkdir()
            write_reference_runs(runs, fixtures, court)

            tampered = base / 'tampered-manifest.json'
            data = json.loads(manifest.read_text(encoding='utf-8'))
            data['authority_commitment'] = '0' * 64
            tampered.write_text(json.dumps(data, sort_keys=True), encoding='utf-8')
            with self.assertRaises(ValueError):
                scorer.score_suite_runs(ROOT, SUITE, runs, tampered)


if __name__ == '__main__':
    unittest.main()
