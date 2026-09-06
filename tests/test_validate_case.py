import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts' / 'validate_case.py'


def valid_case():
    return {
        'schema_version': 1,
        'case_id': 'cli-1',
        'title': 'CLI fixture',
        'scope': {'authorized': True, 'kind': 'sandbox', 'target': 'fixture'},
        'domains': ['testing'],
        'goal': 'discover',
        'state': 'hypothesis',
        'claim': 'Synthetic claim.',
        'environment': {},
        'observations': [],
        'controls': {'positive': [], 'negative': []},
        'reproducer': {'steps': [], 'fixture_digest': ''},
        'root_cause': '',
        'security_consequence': '',
        'uncertainties': [],
        'fix_validation': {},
    }


class ValidateCaseCliTests(unittest.TestCase):
    def test_valid_case_exits_zero(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / 'case.json'
            path.write_text(json.dumps(valid_case()), encoding='utf-8')
            proc = subprocess.run([sys.executable, str(SCRIPT), str(path)], text=True, capture_output=True)
            self.assertEqual(0, proc.returncode, proc.stderr)
            self.assertIn('Case validation passed', proc.stdout)

    def test_invalid_case_exits_one(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / 'case.json'
            case = valid_case()
            case['scope']['authorized'] = False
            path.write_text(json.dumps(case), encoding='utf-8')
            proc = subprocess.run([sys.executable, str(SCRIPT), str(path)], text=True, capture_output=True)
            self.assertEqual(1, proc.returncode)
            self.assertIn('authorized scope', proc.stderr)


if __name__ == '__main__':
    unittest.main()
