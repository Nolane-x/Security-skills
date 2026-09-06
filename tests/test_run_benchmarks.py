import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'scripts'
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from benchmark_core import normalize_result  # noqa: E402
from run_benchmarks import main, run_suite_file  # noqa: E402


def research_case(*, case_id='runner-case'):
    return {
        'schema_version': 1,
        'case_id': case_id,
        'title': 'Synthetic runner case',
        'scope': {'authorized': True, 'kind': 'sandbox', 'target': 'fixture'},
        'domains': ['parsers'],
        'goal': 'discover',
        'state': 'hypothesis',
        'claim': 'Synthetic claim.',
        'environment': {'target_revision': 'rev', 'platform': 'fixture'},
        'observations': [],
        'controls': {'positive': [], 'negative': []},
        'reproducer': {'steps': [], 'fixture_digest': ''},
        'root_cause': '',
        'security_consequence': '',
        'uncertainties': [],
        'fix_validation': {},
    }


def fixture(benchmark_id, *, required=None, forbidden=None):
    return {
        'schema_version': 1,
        'benchmark_id': benchmark_id,
        'category': 'routing',
        'description': 'Synthetic runner fixture.',
        'case': research_case(case_id=benchmark_id),
        'expect': {
            'case_valid': True,
            'required_skills': required or ['security-scope-and-authorization', 'attack-surface-mapping'],
            'optional_skills': ['vulnerability-hypothesis-generation'],
            'forbidden_skills': forbidden or [],
            'required_packs': [],
            'optional_packs': ['research-foundation'],
            'forbidden_packs': [],
            'ordered_before': [['security-scope-and-authorization', 'attack-surface-mapping']],
            'route_limit': 8,
            'required_issue_paths': [],
            'hard_gates': ['prerequisite-integrity', 'determinism'],
        },
        'weights': {},
        'tags': ['synthetic'],
    }


def suite(paths, *, name='unit-suite', minimum=95.0):
    return {
        'schema_version': 1,
        'name': name,
        'description': 'Synthetic runner suite.',
        'fixtures': paths,
        'minimum_score': minimum,
        'weights': {'routing_recall': 1.0, 'evidence_conformance': 2.0, 'reproducibility': 1.0},
        'hard_gates': ['authorization', 'evidence-promotion', 'domain-isolation', 'prerequisite-integrity', 'determinism'],
    }


def write_suite_tree(base: Path, fixtures, manifest):
    bench = base / 'benchmarks'
    (bench / 'cases/routing').mkdir(parents=True)
    (bench / 'suites').mkdir()
    rels = []
    for item in fixtures:
        rel = f"cases/routing/{item['benchmark_id']}.json"
        rels.append(rel)
        (bench / rel).write_text(json.dumps(item), encoding='utf-8')
    manifest = copy.deepcopy(manifest)
    manifest['fixtures'] = rels
    suite_path = bench / 'suites/unit.json'
    suite_path.write_text(json.dumps(manifest), encoding='utf-8')
    return suite_path


class BenchmarkRunnerTests(unittest.TestCase):
    def test_run_suite_is_byte_stable_and_sorts_fixture_results(self):
        with tempfile.TemporaryDirectory() as td:
            items = [fixture('z-last'), fixture('a-first')]
            suite_path = write_suite_tree(Path(td), items, suite([]))
            first = run_suite_file(ROOT, suite_path)
            second = run_suite_file(ROOT, suite_path)
            self.assertEqual(normalize_result(first), normalize_result(second))
            self.assertEqual(['a-first', 'z-last'], [x['benchmark_id'] for x in first['fixtures']])

    def test_main_returns_zero_and_writes_identical_json_and_report_for_passing_suite(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            suite_path = write_suite_tree(root, [fixture('passing')], suite([], minimum=90.0))
            json_a = root / 'a.json'
            json_b = root / 'b.json'
            report = root / 'report.md'
            self.assertEqual(0, main([str(suite_path), '--root', str(ROOT), '--json', str(json_a), '--report', str(report)]))
            self.assertEqual(0, main([str(suite_path), '--root', str(ROOT), '--json', str(json_b)]))
            self.assertEqual(json_a.read_bytes(), json_b.read_bytes())
            self.assertIn('PASS', report.read_text(encoding='utf-8'))

    def test_main_returns_one_for_benchmark_failure(self):
        with tempfile.TemporaryDirectory() as td:
            bad = fixture('failing', forbidden=['attack-surface-mapping'])
            suite_path = write_suite_tree(Path(td), [bad], suite([]))
            self.assertEqual(1, main([str(suite_path), '--root', str(ROOT)]))

    def test_main_returns_two_for_malformed_or_missing_suite_input(self):
        with tempfile.TemporaryDirectory() as td:
            missing = Path(td) / 'missing.json'
            self.assertEqual(2, main([str(missing), '--root', str(ROOT)]))


if __name__ == '__main__':
    unittest.main()
