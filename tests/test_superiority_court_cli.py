import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURT_CLI = ROOT / 'scripts' / 'build_superiority_court.py'
SCORER = ROOT / 'scripts' / 'score_superiority_runs.py'
COURT_MODULE = ROOT / 'scripts' / 'superiority_court.py'
SUITE = ROOT / 'superiority' / 'suites' / 'core.json'
CORPUS = ROOT / 'superiority' / 'corpus.json'


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SuperiorityCourtCliTests(unittest.TestCase):
    def test_court_artifact_is_deterministic_and_declares_strict_winner(self):
        self.assertTrue(COURT_CLI.is_file())
        court_cli = load(COURT_CLI, 'build_superiority_court')
        scorer = load(SCORER, 'score_superiority_runs_for_court')
        court = load(COURT_MODULE, 'superiority_court_for_court_cli')
        corpus = json.loads(CORPUS.read_text(encoding='utf-8'))
        fixtures = {item['fixture_id']: item for item in corpus['fixtures']}
        degraded_fields = {
            'scope-authorized-sandbox': ('evidence_level', 'observed'),
            'evidence-single-signal': ('next_step', 'check'),
            'checks-contradictory-control': ('next_step', 'check'),
            'resolution-fix-unverified': ('claim_level', 'provisional'),
        }

        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            score_paths = []
            for contestant_id, surface_digest, degraded in [
                ('opaque-a', '1' * 64, False),
                ('opaque-b', '2' * 64, True),
            ]:
                runs = base / f'runs-{contestant_id}'
                runs.mkdir()
                for fixture_id, fixture in fixtures.items():
                    task = court.build_task(fixture)
                    answers = json.loads(json.dumps(fixture['private_expected']))
                    if degraded and fixture_id in degraded_fields:
                        field, value = degraded_fields[fixture_id]
                        answers[field] = value
                    run = {
                        'schema_version': 1,
                        'fixture_id': fixture_id,
                        'contestant_id': contestant_id,
                        'contestant_surface_digest': surface_digest,
                        'task_digest': task['task_digest'],
                        'answers': answers,
                    }
                    (runs / f'{fixture_id}.json').write_text(
                        json.dumps(run, sort_keys=True), encoding='utf-8'
                    )
                scored = scorer.score_suite_runs(ROOT, SUITE, runs)
                path = base / f'{contestant_id}.json'
                path.write_text(json.dumps(scored, sort_keys=True), encoding='utf-8')
                score_paths.append(path)

            out_a = base / 'court-a.json'
            out_b = base / 'court-b.json'
            argv = [str(SUITE), *(str(path) for path in score_paths)]
            self.assertEqual(court_cli.main([*argv, '--json', str(out_a)]), 0)
            self.assertEqual(court_cli.main([*argv, '--json', str(out_b)]), 0)
            self.assertEqual(out_a.read_bytes(), out_b.read_bytes())
            result = json.loads(out_a.read_text(encoding='utf-8'))
            self.assertEqual(result['absolute_winner'], 'opaque-a')
            self.assertEqual(result['pairwise'][0]['verdict'], 'left-absolute-superiority')
            contestants = {item['contestant_id']: item for item in result['contestants']}
            self.assertEqual(contestants['opaque-a']['contestant_surface_digest'], '1' * 64)
            self.assertEqual(contestants['opaque-b']['contestant_surface_digest'], '2' * 64)


if __name__ == '__main__':
    unittest.main()
