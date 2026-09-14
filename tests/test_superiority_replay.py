import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts' / 'prepare_superiority_replays.py'
SUITE = ROOT / 'superiority' / 'suites' / 'core.json'
SCORER = ROOT / 'scripts' / 'score_superiority_runs.py'


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SuperiorityReplayTests(unittest.TestCase):
    def test_reference_and_degraded_profiles_are_deterministic_and_valid(self):
        self.assertTrue(SCRIPT.is_file())
        replay = load(SCRIPT, 'prepare_superiority_replays')
        scorer = load(SCORER, 'score_superiority_runs_replay_test')
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            reference = base / 'reference'
            degraded = base / 'degraded'
            self.assertEqual(
                replay.main([str(SUITE), '--profile', 'reference', '--contestant-id', 'opaque-a', '--out', str(reference)]),
                0,
            )
            self.assertEqual(
                replay.main([str(SUITE), '--profile', 'degraded', '--contestant-id', 'opaque-b', '--out', str(degraded)]),
                0,
            )
            ref_score = scorer.score_suite_runs(ROOT, SUITE, reference)
            deg_score = scorer.score_suite_runs(ROOT, SUITE, degraded)
            self.assertTrue(all(item['score'] == 100.0 for item in ref_score['results']))
            self.assertTrue(all(item['passed'] for item in deg_score['results']))
            self.assertTrue(any(item['score'] < 100.0 for item in deg_score['results']))
            before = [(p.name, p.read_bytes()) for p in sorted(degraded.glob('*.json'))]
            self.assertEqual(
                replay.main([str(SUITE), '--profile', 'degraded', '--contestant-id', 'opaque-b', '--out', str(degraded)]),
                0,
            )
            after = [(p.name, p.read_bytes()) for p in sorted(degraded.glob('*.json'))]
            self.assertEqual(before, after)


if __name__ == '__main__':
    unittest.main()
