import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts' / 'prepare_superiority_tasks.py'
SUITE = ROOT / 'superiority' / 'suites' / 'core.json'


def load_script():
    spec = importlib.util.spec_from_file_location('prepare_superiority_tasks', SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def snapshot(root: Path):
    return [(p.name, p.read_bytes()) for p in sorted(root.glob('*.json'))]


class SuperiorityCliTests(unittest.TestCase):
    def test_prepare_cli_is_deterministic_and_oracle_free(self):
        self.assertTrue(SCRIPT.is_file())
        module = load_script()
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            out_a = base / 'a'
            out_b = base / 'b'
            self.assertEqual(module.main([str(SUITE), '--out', str(out_a)]), 0)
            self.assertEqual(module.main([str(SUITE), '--out', str(out_b)]), 0)
            self.assertEqual(snapshot(out_a), snapshot(out_b))
            self.assertEqual(len(snapshot(out_a)), 13)

            manifest_path = out_a / 'SUITE_MANIFEST.json'
            self.assertTrue(manifest_path.is_file())
            manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
            self.assertEqual(manifest['kind'], 'superiority-public-suite-manifest')
            self.assertEqual(manifest['task_count'], 12)
            self.assertRegex(manifest['authority_commitment'], r'^[0-9a-f]{64}$')
            manifest_text = json.dumps(manifest, sort_keys=True)
            self.assertNotIn('private_expected', manifest_text)
            self.assertNotIn('rules', manifest_text)
            self.assertNotIn('minimum', manifest_text)

            task_paths = sorted(
                path for path in out_a.glob('*.json') if path.name != 'SUITE_MANIFEST.json'
            )
            self.assertEqual(len(task_paths), 12)
            task_digests = {}
            for path in task_paths:
                task = json.loads(path.read_text(encoding='utf-8'))
                text = json.dumps(task, sort_keys=True)
                self.assertNotIn('private_expected', text)
                self.assertNotIn('rules', text)
                self.assertNotIn('minimum', text)
                self.assertRegex(task['task_digest'], r'^[0-9a-f]{64}$')
                task_digests[task['fixture_id']] = task['task_digest']

            self.assertEqual(
                manifest['tasks'],
                [
                    {'fixture_id': fixture_id, 'task_digest': task_digests[fixture_id]}
                    for fixture_id in sorted(task_digests)
                ],
            )

    def test_prepare_suite_refuses_nonempty_destination(self):
        module = load_script()
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'tasks'
            out.mkdir()
            stale = out / 'stale.json'
            sentinel = b'{"stale": true}\n'
            stale.write_bytes(sentinel)
            with self.assertRaises(ValueError):
                module.prepare_suite_tasks(ROOT, SUITE, out)
            self.assertEqual(stale.read_bytes(), sentinel)
            self.assertEqual(snapshot(out), [('stale.json', sentinel)])


if __name__ == '__main__':
    unittest.main()
