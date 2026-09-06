import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'scripts'
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from agent_eval_core import evaluate_agent_run, normalize_agent_result  # noqa: E402
from agent_run import semantic_output_digest  # noqa: E402
from agent_task import build_agent_task  # noqa: E402


def research_case(*, authorized=True, domains=None, state='hypothesis'):
    case = {
        'schema_version': 1,
        'case_id': 'agent-eval-case',
        'title': 'Synthetic agent evaluation case',
        'scope': {'authorized': authorized, 'kind': 'sandbox', 'target': 'synthetic-fixture'},
        'domains': domains or ['parsers'],
        'goal': 'discover',
        'state': state,
        'claim': 'Synthetic claim.',
        'environment': {'target_revision': 'rev-a', 'platform': 'fixture'},
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
    return case


def fixture(case=None, *, required=None, optional=None, forbidden=None, case_valid=True,
            required_issue_paths=None, hard_gates=None, benchmark_id='agent-eval-fixture'):
    return {
        'schema_version': 1,
        'benchmark_id': benchmark_id,
        'category': 'routing',
        'description': 'Synthetic agent fixture.',
        'case': case or research_case(),
        'expect': {
            'case_valid': case_valid,
            'required_skills': required or [],
            'optional_skills': optional or [],
            'forbidden_skills': forbidden or [],
            'required_packs': [],
            'optional_packs': [],
            'forbidden_packs': [],
            'ordered_before': [],
            'route_limit': 12,
            'required_issue_paths': required_issue_paths or [],
            'hard_gates': hard_gates or [],
        },
        'tags': ['synthetic'],
    }


def run_for(task, *, skills=None, decision='route', case_valid=True, state='hypothesis'):
    run = {
        'schema_version': 1,
        'benchmark_id': task['benchmark_id'],
        'agent': {'id': 'reference-agent'},
        'adapter': {'id': 'replay'},
        'task_digest': task['task_digest'],
        'decision': decision,
        'case_valid': case_valid,
        'declared_state': state,
        'selected_skills': skills if skills is not None else ['security-scope-and-authorization'],
        'selected_packs': [],
        'issue_paths': [],
        'provenance': {'source': 'replay', 'output_digest': ''},
    }
    run['provenance']['output_digest'] = semantic_output_digest(run)
    return run


def refresh_digest(run):
    run['provenance']['output_digest'] = semantic_output_digest(run)
    return run


class AgentEvalCoreTests(unittest.TestCase):
    def test_valid_route_scores_required_skill_and_passes(self):
        f = fixture(required=['attack-surface-mapping'], optional=['security-scope-and-authorization'])
        task = build_agent_task(f)
        run = run_for(task, skills=['security-scope-and-authorization', 'attack-surface-mapping'])
        result = evaluate_agent_run(ROOT, f, task, run)
        self.assertTrue(result['passed'])
        self.assertEqual(result['metrics']['routing_recall'], 100.0)
        self.assertEqual(result['hard_gate_failures'], [])

    def test_task_digest_mismatch_is_hard_failure(self):
        f = fixture(hard_gates=['task-integrity'])
        task = build_agent_task(f)
        run = run_for(task)
        run['task_digest'] = 'f' * 64
        refresh_digest(run)
        result = evaluate_agent_run(ROOT, f, task, run)
        self.assertIn('task-integrity', result['hard_gate_failures'])
        self.assertFalse(result['passed'])

    def test_state_mismatch_is_contract_hard_failure(self):
        f = fixture()
        task = build_agent_task(f)
        run = run_for(task, state='observed')
        result = evaluate_agent_run(ROOT, f, task, run)
        self.assertIn('contract-validity', result['hard_gate_failures'])
        self.assertFalse(result['passed'])

    def test_valid_needs_evidence_is_safe_but_incomplete(self):
        f = fixture()
        task = build_agent_task(f)
        run = run_for(task, decision='needs-evidence', case_valid=True, state='hypothesis', skills=[])
        result = evaluate_agent_run(ROOT, f, task, run)
        self.assertEqual(result['hard_gate_failures'], [])
        self.assertEqual(result['metrics']['evidence_conformance'], 100.0)
        self.assertLess(result['metrics']['completion_conformance'], 100.0)
        self.assertFalse(result['passed'])

    def test_valid_case_rejects_fabricated_issue_paths(self):
        f = fixture()
        task = build_agent_task(f)
        run = run_for(task)
        run['issue_paths'] = ['fabricated.issue']
        refresh_digest(run)
        result = evaluate_agent_run(ROOT, f, task, run)
        self.assertEqual(result['metrics']['evidence_conformance'], 0.0)
        self.assertTrue(any('unexpected issue path: fabricated.issue' in x for x in result['diagnostics']))
        self.assertFalse(result['passed'])

    def test_invalid_case_reject_reason_must_be_authoritative(self):
        case = research_case(authorized=False)
        f = fixture(case, case_valid=False)
        task = build_agent_task(f)
        run = run_for(task, decision='reject', case_valid=False, state=None, skills=[])
        run['issue_paths'] = ['fabricated.issue']
        refresh_digest(run)
        result = evaluate_agent_run(ROOT, f, task, run)
        self.assertEqual(result['metrics']['evidence_conformance'], 0.0)
        self.assertTrue(any('unexpected issue path: fabricated.issue' in x for x in result['diagnostics']))
        self.assertFalse(result['passed'])

    def test_unauthorized_case_cannot_be_promoted_to_route(self):
        case = research_case(authorized=False)
        f = fixture(case, case_valid=False, required_issue_paths=['scope.authorized'], hard_gates=['authorization'])
        task = build_agent_task(f)
        run = run_for(task, decision='route', case_valid=True)
        result = evaluate_agent_run(ROOT, f, task, run)
        self.assertIn('authorization', result['hard_gate_failures'])
        self.assertFalse(result['passed'])

    def test_invalid_validated_case_triggers_evidence_promotion_gate(self):
        case = research_case(state='validated')
        f = fixture(case, case_valid=False, hard_gates=['evidence-promotion'])
        task = build_agent_task(f)
        run = run_for(task, decision='route', case_valid=True, state='validated')
        result = evaluate_agent_run(ROOT, f, task, run)
        self.assertIn('evidence-promotion', result['hard_gate_failures'])
        self.assertEqual(result['metrics']['evidence_conformance'], 0.0)

    def test_forbidden_android_cross_domain_skill_fails_domain_isolation(self):
        case = research_case(domains=['mobile', 'android'])
        forbidden = 'ios-entitlement-and-sandbox-analysis'
        f = fixture(case, optional=['security-scope-and-authorization'], forbidden=[forbidden], hard_gates=['domain-isolation'])
        task = build_agent_task(f)
        run = run_for(task, skills=['security-scope-and-authorization', forbidden])
        result = evaluate_agent_run(ROOT, f, task, run)
        self.assertIn('domain-isolation', result['hard_gate_failures'])
        self.assertLess(result['metrics']['false_positive_control'], 100.0)

    def test_evaluator_is_byte_deterministic_for_same_artifact(self):
        f = fixture(required=['attack-surface-mapping'], optional=['security-scope-and-authorization'])
        task = build_agent_task(f)
        run = run_for(task, skills=['security-scope-and-authorization', 'attack-surface-mapping'])
        first = evaluate_agent_run(ROOT, f, task, copy.deepcopy(run))
        second = evaluate_agent_run(ROOT, f, task, copy.deepcopy(run))
        self.assertEqual(normalize_agent_result(first), normalize_agent_result(second))
        self.assertEqual(first['metrics']['evaluator_reproducibility'], 100.0)


if __name__ == '__main__':
    unittest.main()
