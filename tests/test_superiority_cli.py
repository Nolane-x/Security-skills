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
            self.assertEqual(len(snapshot(out_a)), 12)
            for path in out_a.glob('*.json'):
                task = json.loads(path.read_text(encoding='utf-8'))
                text = json.dumps(task, sort_keys=True)
                self.assertNotIn('private_expected', text)
                self.assertNotIn('rules', text)
                self.assertNotIn('minimum', text)
                self.assertRegex(task['task_digest'], r'^[0-9a-f]{64}$')


if __name__ == '__main__':
    unittest.main()
