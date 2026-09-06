import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'scripts'
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from validate_benchmarks import validate_corpus, validate_fixture, validate_suite  # noqa: E402


def valid_case(authorized=True):
    return {
        'schema_version': 1,
        'case_id': 'validator-case',
        'title': 'Synthetic validator case',
        'scope': {'authorized': authorized, 'kind': 'sandbox', 'target': 'fixture'},
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


def fixture(benchmark_id='fixture-one'):
    return {
        'schema_version': 1,
        'benchmark_id': benchmark_id,
        'category': 'routing',
        'description': 'Synthetic fixture for validator tests.',
        'case': valid_case(),
        'expect': {
            'case_valid': True,
            'required_skills': ['security-scope-and-authorization'],
            'optional_skills': ['attack-surface-mapping'],
            'forbidden_skills': [],
            'required_packs': ['research-foundation'],
            'optional_packs': [],
            'forbidden_packs': [],
            'ordered_before': [['security-scope-and-authorization', 'attack-surface-mapping']],
            'route_limit': 8,
            'required_issue_paths': [],
            'hard_gates': ['prerequisite-integrity', 'determinism'],
        },
        'weights': {'routing_recall': 1.25},
        'tags': ['synthetic'],
    }


def suite(paths=None, minimum=95.0):
    return {
        'schema_version': 1,
        'name': 'unit-suite',
        'description': 'Synthetic suite.',
        'fixtures': paths or ['cases/routing/one.json'],
        'minimum_score': minimum,
        'weights': {'routing_recall': 1.0, 'evidence_conformance': 2.0},
        'hard_gates': ['authorization', 'evidence-promotion', 'domain-isolation', 'prerequisite-integrity', 'determinism'],
    }


class BenchmarkValidatorTests(unittest.TestCase):
    def test_valid_fixture_has_no_errors(self):
        self.assertEqual([], [x for x in validate_fixture(ROOT, fixture(), 'fixture.json') if x.level == 'error'])

    def test_unknown_skill_and_pack_references_are_errors(self):
        f = fixture()
        f['expect']['required_skills'].append('not-a-real-skill')
        f['expect']['required_packs'].append('not-a-real-pack')
        messages = [x.message for x in validate_fixture(ROOT, f, 'fixture.json')]
        self.assertTrue(any('unknown skill' in x for x in messages))
        self.assertTrue(any('unknown pack' in x for x in messages))

    def test_ordered_before_must_be_known_two_item_skill_pair(self):
        f = fixture()
        f['expect']['ordered_before'] = [['security-scope-and-authorization'], ['nope', 'attack-surface-mapping']]
        messages = [x.message for x in validate_fixture(ROOT, f, 'fixture.json')]
        self.assertTrue(any('ordered_before' in x for x in messages))
        self.assertTrue(any('unknown skill' in x for x in messages))

    def test_unknown_hard_gate_and_metric_are_errors(self):
        f = fixture()
        f['expect']['hard_gates'].append('magic-gate')
        f['weights']['magic-score'] = 1.0
        messages = [x.message for x in validate_fixture(ROOT, f, 'fixture.json')]
        self.assertTrue(any('unknown hard gate' in x for x in messages))
        self.assertTrue(any('unknown metric' in x for x in messages))

    def test_invalid_case_is_allowed_only_when_expected_invalid(self):
        f = fixture()
        f['case']['scope']['authorized'] = False
        f['expect']['case_valid'] = False
        f['expect']['required_issue_paths'] = ['scope.authorized']
        self.assertEqual([], [x for x in validate_fixture(ROOT, f, 'fixture.json') if x.level == 'error'])
        f['expect']['case_valid'] = True
        messages = [x.message for x in validate_fixture(ROOT, f, 'fixture.json')]
        self.assertTrue(any('expected valid' in x for x in messages))

    def test_suite_rejects_invalid_minimum_and_unknown_names(self):
        s = suite(minimum=101.0)
        s['weights']['magic-score'] = 1.0
        s['hard_gates'].append('magic-gate')
        messages = [x.message for x in validate_suite(ROOT, s, 'suite.json')]
        self.assertTrue(any('minimum_score' in x for x in messages))
        self.assertTrue(any('unknown metric' in x for x in messages))
        self.assertTrue(any('unknown hard gate' in x for x in messages))

    def test_corpus_rejects_duplicate_ids(self):
        with tempfile.TemporaryDirectory() as td:
            bench = Path(td) / 'benchmarks'
            (bench / 'cases/routing').mkdir(parents=True)
            (bench / 'suites').mkdir()
            (bench / 'cases/routing/one.json').write_text(json.dumps(fixture('duplicate')), encoding='utf-8')
            (bench / 'cases/routing/two.json').write_text(json.dumps(fixture('duplicate')), encoding='utf-8')
            (bench / 'suites/core.json').write_text(json.dumps(suite(['cases/routing/one.json', 'cases/routing/two.json'])), encoding='utf-8')
            messages = [x.message for x in validate_corpus(ROOT, bench)]
            self.assertTrue(any('duplicate benchmark_id' in x for x in messages))

    def test_corpus_requires_every_fixture_in_core_and_portability_subset_of_core(self):
        with tempfile.TemporaryDirectory() as td:
            bench = Path(td) / 'benchmarks'
            (bench / 'cases/routing').mkdir(parents=True)
            (bench / 'suites').mkdir()
            (bench / 'cases/routing/core.json').write_text(json.dumps(fixture('core-one')), encoding='utf-8')
            (bench / 'cases/routing/port-only.json').write_text(json.dumps(fixture('port-only')), encoding='utf-8')
            core = suite(['cases/routing/core.json'])
            core['name'] = 'core'
            portability = suite(['cases/routing/port-only.json'])
            portability['name'] = 'portability'
            (bench / 'suites/core.json').write_text(json.dumps(core), encoding='utf-8')
            (bench / 'suites/portability.json').write_text(json.dumps(portability), encoding='utf-8')
            messages = [x.message for x in validate_corpus(ROOT, bench)]
            self.assertTrue(any('not listed in core' in x for x in messages))
            self.assertTrue(any('portability fixture is not in core' in x for x in messages))

    def test_real_wave5_corpus_enforces_core_size_and_category_balance(self):
        errors = [x for x in validate_corpus(ROOT) if x.level == 'error']
        self.assertEqual([], errors)

    def test_corpus_rejects_orphan_fixture_but_allows_suite_overlap(self):
        with tempfile.TemporaryDirectory() as td:
            bench = Path(td) / 'benchmarks'
            (bench / 'cases/routing').mkdir(parents=True)
            (bench / 'suites').mkdir()
            (bench / 'cases/routing/one.json').write_text(json.dumps(fixture('one')), encoding='utf-8')
            (bench / 'cases/routing/orphan.json').write_text(json.dumps(fixture('orphan')), encoding='utf-8')
            shared = ['cases/routing/one.json']
            (bench / 'suites/core.json').write_text(json.dumps(suite(shared)), encoding='utf-8')
            portability = suite(shared)
            portability['name'] = 'portability'
            (bench / 'suites/portability.json').write_text(json.dumps(portability), encoding='utf-8')
            messages = [x.message for x in validate_corpus(ROOT, bench)]
            self.assertTrue(any('orphan fixture' in x for x in messages))
            self.assertFalse(any('multiple suites' in x for x in messages))


if __name__ == '__main__':
    unittest.main()
