import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'scripts'
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from benchmark_report import render_report  # noqa: E402


class BenchmarkReportTests(unittest.TestCase):
    def test_report_exposes_hard_gate_and_failed_fixture_details(self):
        result = {
            'schema_version': 1,
            'suite': 'unit',
            'fixture_count': 1,
            'passed_fixture_count': 0,
            'failed_fixture_count': 1,
            'overall_score': 72.5,
            'minimum_score': 95.0,
            'hard_gate_failures': 1,
            'metrics': {'evidence_conformance': 50.0, 'reproducibility': 100.0},
            'fixtures': [{
                'benchmark_id': 'bad-evidence',
                'category': 'evidence',
                'case_valid': True,
                'issue_paths': [],
                'route': None,
                'metrics': {'evidence_conformance': 0.0},
                'hard_gate_failures': ['evidence-promotion'],
                'diagnostics': ['case validity mismatch: expected false got true'],
                'passed': False,
            }],
            'passed': False,
        }
        report = render_report(result)
        self.assertIn('# Benchmark Report: unit', report)
        self.assertIn('FAIL', report)
        self.assertIn('evidence-promotion', report)
        self.assertIn('bad-evidence', report)
        self.assertIn('case validity mismatch', report)
        self.assertIn('evidence_conformance', report)

    def test_report_is_deterministic_for_same_result(self):
        result = {
            'schema_version': 1,
            'suite': 'unit',
            'fixture_count': 0,
            'passed_fixture_count': 0,
            'failed_fixture_count': 0,
            'overall_score': 100.0,
            'minimum_score': 95.0,
            'hard_gate_failures': 0,
            'metrics': {'reproducibility': 100.0},
            'fixtures': [],
            'passed': True,
        }
        self.assertEqual(render_report(result), render_report(result))


if __name__ == '__main__':
    unittest.main()
