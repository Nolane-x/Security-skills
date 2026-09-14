import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts' / 'prepare_superiority_replays.py'
PREPARE = ROOT / 'scripts' / 'prepare_superiority_tasks.py'
SUITE = ROOT / 'superiority' / 'suites' / 'core.json'
SCORER = ROOT / 'scripts' / 'score_superiority_runs.py'
SURFACE_DIGEST = '3' * 64


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SuperiorityReplayTests(unittest.TestCase):
    def test_reference_and_degraded_profiles_are_deterministic_and_valid(self):
        self.assertTrue(SCRIPT.is_file())
        replay = load(SCRIPT, 'prepare_superiority_replays')
        prepare = load(PREPARE, 'prepare_superiority_tasks_replay_test')
        scorer = load(SCORER, 'score_superiority_runs_replay_test')
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            tasks = base / 'tasks'
            prepare.prepare_suite_tasks(ROOT, SUITE, tasks)
            manifest = tasks / 'SUITE_MANIFEST.json'
            reference = base / 'reference'
            degraded = base / 'degraded'
            self.assertEqual(
                replay.main([
                    str(SUITE),
                    '--profile', 'reference',
                    '--contestant-id', 'opaque-a',
                    '--surface-digest', SURFACE_DIGEST,
                    '--out', str(reference),
                ]),
                0,
            )
            self.assertEqual(
                replay.main([
                    str(SUITE),
                    '--profile', 'degraded',
                    '--contestant-id', 'opaque-b',
                    '--surface-digest', SURFACE_DIGEST,
                    '--out', str(degraded),
                ]),
                0,
            )
            ref_score = scorer.score_suite_runs(ROOT, SUITE, reference, manifest)
            deg_score = scorer.score_suite_runs(ROOT, SUITE, degraded, manifest)
            self.assertEqual(ref_score['authority_commitment'], deg_score['authority_commitment'])
            self.assertEqual(ref_score['contestant_surface_digest'], SURFACE_DIGEST)
            self.assertEqual(deg_score['contestant_surface_digest'], SURFACE_DIGEST)
            self.assertTrue(all(item['score'] == 100.0 for item in ref_score['results']))
            self.assertTrue(all(item['passed'] for item in deg_score['results']))
            self.assertTrue(any(item['score'] < 100.0 for item in deg_score['results']))
            before = [(p.name, p.read_bytes()) for p in sorted(degraded.glob('*.json'))]
            self.assertEqual(
                replay.main([
                    str(SUITE),
                    '--profile', 'degraded',
                    '--contestant-id', 'opaque-b',
                    '--surface-digest', SURFACE_DIGEST,
                    '--out', str(degraded),
                ]),
                0,
            )
            after = [(p.name, p.read_bytes()) for p in sorted(degraded.glob('*.json'))]
            self.assertEqual(before, after)

    def test_replay_requires_valid_explicit_surface_digest(self):
        replay = load(SCRIPT, 'prepare_superiority_replays_surface_test')
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'runs'
            with self.assertRaises(ValueError):
                replay.prepare_replays(
                    ROOT,
                    SUITE,
                    profile='reference',
                    contestant_id='opaque-a',
                    surface_digest='not-a-sha256',
                    out_dir=out,
                )


if __name__ == '__main__':
    unittest.main()
