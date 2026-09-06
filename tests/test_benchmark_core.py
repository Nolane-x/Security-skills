import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'scripts'
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from benchmark_core import evaluate_fixture, evaluate_suite, normalize_result  # noqa: E402


def research_case(*, domains=None, state='hypothesis', goal='discover', authorized=True):
    case = {
        'schema_version': 1,
        'case_id': 'bench-case',
        'title': 'Synthetic benchmark case',
        'scope': {'authorized': authorized, 'kind': 'sandbox', 'target': 'synthetic-fixture'},
        'domains': domains or ['parsers'],
        'goal': goal,
        'state': state,
        'claim': 'Synthetic claim for deterministic benchmark evaluation.',
        'environment': {'target_revision': 'rev-a', 'platform': 'fixture-linux'},
        'observations': [],
        'controls': {'positive': [], 'negative': []},
        'reproducer': {'steps': [], 'fixture_digest': ''},
        'root_cause': '',
        'security_consequence': '',
        'uncertainties': [],
        'fix_validation': {},
    }
    if state != 'hypothesis':
        case['observations'] = ['controlled observation']
    if state in {'validated', 'regression-verified'}:
        case['controls'] = {'positive': ['known-good control'], 'negative': ['known-negative control']}
        case['reproducer'] = {'steps': ['run synthetic fixture'], 'fixture_digest': 'sha256:fixture'}
        case['root_cause'] = 'synthetic causal root cause'
        case['security_consequence'] = 'bounded synthetic consequence'
    if state == 'regression-verified':
        case['fix_validation'] = {
            'fixed_revision': 'rev-b',
            'vulnerability_no_longer_reproduces': True,
            'controls_still_pass': True,
        }
    return case


def fixture(case, *, required_skills=None, optional_skills=None, forbidden_skills=None,
            required_packs=None, optional_packs=None, forbidden_packs=None,
            ordered_before=None, case_valid=True, required_issue_paths=None,
            hard_gates=None, benchmark_id='fixture-1', route_limit=12):
    return {
        'schema_version': 1,
        'benchmark_id': benchmark_id,
        'category': 'routing',
        'description': 'Synthetic benchmark fixture.',
        'case': case,
        'expect': {
            'case_valid': case_valid,
            'required_skills': required_skills or [],
            'optional_skills': optional_skills or [],
            'forbidden_skills': forbidden_skills or [],
            'required_packs': required_packs or [],
            'optional_packs': optional_packs or [],
            'forbidden_packs': forbidden_packs or [],
            'ordered_before': ordered_before or [],
            'route_limit': route_limit,
            'required_issue_paths': required_issue_paths or [],
            'hard_gates': hard_gates or [],
        },
        'tags': ['synthetic'],
    }


class BenchmarkCoreTests(unittest.TestCase):
    def test_valid_routing_scores_required_and_allowed_outputs(self):
        f = fixture(
            research_case(domains=['mobile', 'android', 'routing'], goal='root-cause'),
            required_skills=['security-scope-and-authorization', 'android-intent-and-deeplink-analysis'],
            optional_skills=[
                'attack-surface-mapping',
                'vulnerability-hypothesis-generation',
                'static-dataflow-analysis',
                'android-component-exposure-analysis',
                'android-keystore-and-local-storage-analysis',
                'android-webview-bridge-analysis',
                'mobile-network-trust-analysis',
                'security-research-case-management',
                'research-route-selection',
            ],
            forbidden_skills=['ios-entitlement-and-sandbox-analysis', 'ios-url-scheme-and-universal-link-analysis'],
            required_packs=['mobile-security'],
            optional_packs=['program-analysis', 'research-foundation', 'web-framework-internals'],
            hard_gates=['domain-isolation', 'prerequisite-integrity', 'determinism'],
        )
        result = evaluate_fixture(ROOT, f)
        self.assertTrue(result['passed'])
        self.assertEqual(100.0, result['metrics']['routing_recall'])
        self.assertEqual(100.0, result['metrics']['routing_precision'])
        self.assertEqual(100.0, result['metrics']['pack_recall'])
        self.assertEqual([], result['hard_gate_failures'])

    def test_mandatory_goal_and_state_anchors_are_allowed_for_precision(self):
        f = fixture(
            research_case(domains=['parsers'], goal='discover'),
            required_skills=['parser-state-machine-analysis'],
            optional_skills=['fuzzing-workflow', 'grammar-aware-fuzzing'],
        )
        result = evaluate_fixture(ROOT, f)
        self.assertTrue(result['passed'])
        self.assertEqual(100.0, result['metrics']['routing_precision'])

    def test_forbidden_output_penalizes_false_positive_control(self):
        f = fixture(
            research_case(domains=['mobile', 'android', 'routing'], goal='root-cause'),
            required_skills=['security-scope-and-authorization'],
            forbidden_skills=['android-intent-and-deeplink-analysis'],
        )
        result = evaluate_fixture(ROOT, f)
        self.assertFalse(result['passed'])
        self.assertLess(result['metrics']['false_positive_control'], 100.0)
        self.assertTrue(any('forbidden skill' in x for x in result['diagnostics']))

    def test_invalid_unauthorized_fixture_passes_when_rejected(self):
        f = fixture(
            research_case(authorized=False),
            case_valid=False,
            required_issue_paths=['scope.authorized'],
            hard_gates=['authorization', 'determinism'],
        )
        result = evaluate_fixture(ROOT, f)
        self.assertTrue(result['passed'])
        self.assertEqual(100.0, result['metrics']['evidence_conformance'])
        self.assertEqual(100.0, result['metrics']['false_positive_control'])
        self.assertEqual([], result['hard_gate_failures'])
        self.assertIsNone(result['route'])

    def test_validated_case_missing_controls_is_rejected_without_promotion(self):
        c = research_case(state='validated', goal='validate')
        c['controls'] = {'positive': [], 'negative': []}
        f = fixture(
            c,
            case_valid=False,
            required_issue_paths=['controls.positive', 'controls.negative'],
            hard_gates=['evidence-promotion', 'determinism'],
        )
        result = evaluate_fixture(ROOT, f)
        self.assertTrue(result['passed'])
        self.assertEqual(100.0, result['metrics']['evidence_conformance'])
        self.assertEqual([], result['hard_gate_failures'])

    def test_prerequisite_integrity_is_checked_against_graph(self):
        f = fixture(
            research_case(domains=['mobile', 'android', 'routing'], goal='root-cause'),
            required_skills=['android-intent-and-deeplink-analysis'],
            ordered_before=[['android-component-exposure-analysis', 'android-intent-and-deeplink-analysis']],
            hard_gates=['prerequisite-integrity'],
        )
        result = evaluate_fixture(ROOT, f)
        self.assertEqual(100.0, result['metrics']['prerequisite_integrity'])
        self.assertEqual([], result['hard_gate_failures'])

    def test_normalized_result_is_byte_stable_and_sorted(self):
        f = fixture(
            research_case(domains=['virtualization', 'shared-memory'], state='observed', goal='validate'),
            required_skills=['security-scope-and-authorization'],
            hard_gates=['determinism'],
        )
        a = evaluate_fixture(ROOT, copy.deepcopy(f))
        b = evaluate_fixture(ROOT, copy.deepcopy(f))
        self.assertEqual(normalize_result(a), normalize_result(b))
        parsed = json.loads(normalize_result(a))
        self.assertEqual('fixture-1', parsed['benchmark_id'])

    def test_fixture_metric_weights_produce_a_fixture_score(self):
        f = fixture(
            research_case(domains=['mobile', 'android'], goal='root-cause'),
            required_skills=['security-scope-and-authorization'],
            forbidden_skills=['android-intent-and-deeplink-analysis'],
        )
        f['weights'] = {
            'routing_precision': 0.0,
            'routing_recall': 0.0,
            'pack_precision': 0.0,
            'pack_recall': 0.0,
            'prerequisite_integrity': 0.0,
            'domain_isolation': 0.0,
            'evidence_conformance': 0.0,
            'false_positive_control': 1.0,
            'reproducibility': 0.0,
        }
        result = evaluate_fixture(ROOT, f)
        self.assertEqual(0.0, result['score'])

    def test_suite_hard_gates_are_applied_even_when_fixture_omits_them(self):
        f = fixture(research_case(), case_valid=False, hard_gates=[])
        suite = {
            'schema_version': 1,
            'name': 'hard-gate-suite',
            'minimum_score': 0.0,
            'weights': {},
            'hard_gates': ['evidence-promotion'],
        }
        result = evaluate_suite(ROOT, suite, [f])
        self.assertEqual(1, result['hard_gate_failures'])
        self.assertFalse(result['passed'])

    def test_suite_aggregates_applicable_metrics_and_hard_gates(self):
        good = fixture(
            research_case(),
            required_skills=['security-scope-and-authorization', 'attack-surface-mapping'],
            optional_skills=['vulnerability-hypothesis-generation'],
            benchmark_id='a-good',
            hard_gates=['prerequisite-integrity', 'determinism'],
        )
        invalid = fixture(
            research_case(authorized=False),
            benchmark_id='b-invalid',
            case_valid=False,
            required_issue_paths=['scope.authorized'],
            hard_gates=['authorization', 'determinism'],
        )
        suite = {
            'schema_version': 1,
            'name': 'unit',
            'minimum_score': 95.0,
            'weights': {
                'routing_precision': 1.0,
                'routing_recall': 1.0,
                'pack_precision': 0.5,
                'pack_recall': 0.5,
                'prerequisite_integrity': 1.5,
                'domain_isolation': 1.5,
                'evidence_conformance': 2.0,
                'false_positive_control': 2.0,
                'reproducibility': 1.0,
            },
        }
        result = evaluate_suite(ROOT, suite, [invalid, good])
        self.assertEqual(2, result['fixture_count'])
        self.assertEqual(['a-good', 'b-invalid'], [x['benchmark_id'] for x in result['fixtures']])
        self.assertEqual(0, result['hard_gate_failures'])
        self.assertTrue(result['passed'])
        self.assertGreaterEqual(result['overall_score'], 95.0)


if __name__ == '__main__':
    unittest.main()
