import os
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'scripts'
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from run_agent_adapter import AdapterError, run_adapter  # noqa: E402


TASK = {
    'schema_version': 1,
    'benchmark_id': 'adapter-fixture',
    'category': 'routing',
    'research_case': {},
    'instructions': 'Synthetic authorized task.',
    'response_contract': {},
    'task_digest': 'a' * 64,
}


def write_script(directory: Path, source: str) -> Path:
    path = directory / 'adapter.py'
    path.write_text(textwrap.dedent(source), encoding='utf-8')
    return path


class RunAgentAdapterTests(unittest.TestCase):
    def test_valid_json_protocol_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            script = write_script(Path(tmp), """
                import json, sys
                task = json.load(sys.stdin)
                print(json.dumps({'benchmark_id': task['benchmark_id'], 'ok': True}))
            """)
            result = run_adapter(TASK, [sys.executable, str(script)])
            self.assertEqual(result, {'benchmark_id': 'adapter-fixture', 'ok': True})

    def test_shell_metacharacters_are_not_interpreted(self):
        with tempfile.TemporaryDirectory() as tmp:
            marker = Path(tmp) / 'pwned.txt'
            script = write_script(Path(tmp), """
                import json, sys
                json.load(sys.stdin)
                print(json.dumps({'arg': sys.argv[1]}))
            """)
            arg = f'; touch {marker}'
            result = run_adapter(TASK, [sys.executable, str(script), arg])
            self.assertEqual(result['arg'], arg)
            self.assertFalse(marker.exists())

    def test_timeout_nonzero_invalid_json_and_output_cap_are_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            sleeper = write_script(directory, """
                import time
                time.sleep(2)
            """)
            with self.assertRaises(AdapterError):
                run_adapter(TASK, [sys.executable, str(sleeper)], timeout=0.05)

            failing = write_script(directory, """
                raise SystemExit(7)
            """)
            with self.assertRaises(AdapterError):
                run_adapter(TASK, [sys.executable, str(failing)])

            invalid = write_script(directory, """
                print('not-json')
            """)
            with self.assertRaises(AdapterError):
                run_adapter(TASK, [sys.executable, str(invalid)])

            huge = write_script(directory, """
                print('x' * 5000)
            """)
            with self.assertRaises(AdapterError):
                run_adapter(TASK, [sys.executable, str(huge)], max_output_bytes=128)

    def test_environment_is_sanitized_and_allowlist_is_explicit(self):
        old = os.environ.get('OPENAI_API_KEY')
        os.environ['OPENAI_API_KEY'] = 'synthetic-secret'
        try:
            with tempfile.TemporaryDirectory() as tmp:
                script = write_script(Path(tmp), """
                    import json, os, sys
                    json.load(sys.stdin)
                    print(json.dumps({'seen': os.environ.get('OPENAI_API_KEY')}))
                """)
                hidden = run_adapter(TASK, [sys.executable, str(script)])
                shown = run_adapter(TASK, [sys.executable, str(script)], allow_env=['OPENAI_API_KEY'])
                self.assertIsNone(hidden['seen'])
                self.assertEqual(shown['seen'], 'synthetic-secret')
        finally:
            if old is None:
                os.environ.pop('OPENAI_API_KEY', None)
            else:
                os.environ['OPENAI_API_KEY'] = old


if __name__ == '__main__':
    unittest.main()
