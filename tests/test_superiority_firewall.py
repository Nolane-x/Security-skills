import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts' / 'build_contestant_view.py'


def load_script():
    spec = importlib.util.spec_from_file_location('build_contestant_view', SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SuperiorityFirewallTests(unittest.TestCase):
    def test_contestant_view_is_deterministic_and_oracle_free(self):
        self.assertTrue(SCRIPT.is_file())
        module = load_script()
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            out_a = base / 'a'
            out_b = base / 'b'
            manifest_a = module.build_contestant_view(ROOT, out_a)
            manifest_b = module.build_contestant_view(ROOT, out_b)

            self.assertEqual(manifest_a, manifest_b)
            self.assertRegex(manifest_a['surface_digest'], r'^[0-9a-f]{64}$')
            self.assertGreater(manifest_a['file_count'], 80)

            required = {
                'AGENTS.md',
                'SECURITY.md',
                'scripts/research_case.py',
                'scripts/route_skills.py',
                'scripts/security_graph.py',
                'scripts/skilllib.py',
                'scripts/validate_case.py',
            }
            paths = {
                path.relative_to(out_a).as_posix()
                for path in out_a.rglob('*')
                if path.is_file()
            }
            self.assertTrue(required <= paths)

            forbidden_roots = {'superiority', 'benchmarks', 'agent-eval', 'tests', '.github'}
            judge_scripts = {
                'scripts/superiority_court.py',
                'scripts/prepare_superiority_tasks.py',
                'scripts/prepare_superiority_replays.py',
                'scripts/score_superiority_runs.py',
                'scripts/build_superiority_court.py',
            }
            self.assertTrue(paths.isdisjoint(judge_scripts))
            for path in paths:
                self.assertNotIn(path.split('/', 1)[0], forbidden_roots)

            for path in out_a.rglob('*'):
                if not path.is_file():
                    continue
                text = path.read_text(encoding='utf-8')
                self.assertNotIn('private_expected', text)
                self.assertNotIn('superiority-core-corpus', text)

    def test_contestant_view_refuses_nonempty_destination(self):
        self.assertTrue(SCRIPT.is_file())
        module = load_script()
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'view'
            out.mkdir()
            (out / 'keep.txt').write_text('do not delete', encoding='utf-8')
            with self.assertRaises(ValueError):
                module.build_contestant_view(ROOT, out)
            self.assertEqual((out / 'keep.txt').read_text(encoding='utf-8'), 'do not delete')


if __name__ == '__main__':
    unittest.main()
