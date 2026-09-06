import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'scripts'
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from agent_run import semantic_output_digest, validate_agent_run  # noqa: E402


TASK = {
    'schema_version': 1,
    'benchmark_id': 'run-fixture',
    'category': 'routing',
    'research_case': {'schema_version': 1, 'state': 'hypothesis'},
    'instructions': 'Synthetic authorized task.',
    'response_contract': {},
    'task_digest': 'a' * 64,
}


def base_run():
    run = {
        'schema_version': 1,
        'benchmark_id': 'run-fixture',
        'agent': {'id': 'reference-agent', 'version': '1'},
        'adapter': {'id': 'replay', 'version': '1'},
        'task_digest': 'a' * 64,
        'decision': 'route',
        'case_valid': True,
        'declared_state': 'hypothesis',
        'selected_skills': ['security-scope-and-authorization'],
        'selected_packs': [],
        'issue_paths': [],
        'notes': 'human-readable note',
        'provenance': {'source': 'replay', 'output_digest': ''},
        'telemetry': {'duration_ms': 1},
    }
    run['provenance']['output_digest'] = semantic_output_digest(run)
    return run


def refresh_digest(run):
    run['provenance']['output_digest'] = semantic_output_digest(run)
    return run


class AgentRunTests(unittest.TestCase):
    def test_valid_minimal_route_run_has_no_errors(self):
        self.assertEqual(validate_agent_run(ROOT, base_run(), TASK), [])

    def test_unknown_and_duplicate_skills_are_rejected(self):
        run = base_run()
        run['selected_skills'] = ['no-such-skill', 'no-such-skill']
        refresh_digest(run)
        errors = validate_agent_run(ROOT, run, TASK)
        self.assertTrue(any('duplicate' in x for x in errors))
        self.assertTrue(any('unknown skill' in x for x in errors))

    def test_task_identity_mismatch_is_rejected(self):
        run = base_run()
        run['task_digest'] = 'b' * 64
        refresh_digest(run)
        errors = validate_agent_run(ROOT, run, TASK)
        self.assertTrue(any('task_digest' in x for x in errors))

    def test_digest_fields_require_lowercase_hex(self):
        run = base_run()
        run['task_digest'] = 'A' * 64
        refresh_digest(run)
        errors = validate_agent_run(ROOT, run, TASK)
        self.assertIn('task_digest must be a lowercase 64-character SHA-256 hex string', errors)

        run = base_run()
        run['provenance']['output_digest'] = 'A' * 64
        errors = validate_agent_run(ROOT, run, TASK)
        self.assertIn('provenance.output_digest must be a lowercase 64-character SHA-256 hex string', errors)

    def test_route_requires_declared_state_matching_task(self):
        run = base_run()
        run['declared_state'] = 'observed'
        refresh_digest(run)
        errors = validate_agent_run(ROOT, run, TASK)
        self.assertTrue(any('route' in x and 'declared_state' in x and 'task state' in x for x in errors))

    def test_reject_cannot_select_route_or_claim_valid(self):
        run = base_run()
        run['decision'] = 'reject'
        run['case_valid'] = True
        refresh_digest(run)
        errors = validate_agent_run(ROOT, run, TASK)
        self.assertTrue(any('reject' in x for x in errors))

    def test_reject_requires_null_state_and_issue_path(self):
        run = base_run()
        run.update({
            'decision': 'reject',
            'case_valid': False,
            'declared_state': 'hypothesis',
            'selected_skills': [],
            'selected_packs': [],
            'issue_paths': [],
        })
        refresh_digest(run)
        errors = validate_agent_run(ROOT, run, TASK)
        self.assertTrue(any('reject' in x and 'declared_state' in x for x in errors))
        self.assertTrue(any('reject' in x and 'issue_paths' in x for x in errors))

    def test_valid_reject_contract_has_null_state_and_issue_path(self):
        run = base_run()
        run.update({
            'decision': 'reject',
            'case_valid': False,
            'declared_state': None,
            'selected_skills': [],
            'selected_packs': [],
            'issue_paths': ['scope.authorized'],
        })
        refresh_digest(run)
        self.assertEqual(validate_agent_run(ROOT, run, TASK), [])

    def test_needs_evidence_cannot_claim_case_invalid(self):
        run = base_run()
        run['decision'] = 'needs-evidence'
        run['case_valid'] = False
        run['selected_skills'] = []
        refresh_digest(run)
        errors = validate_agent_run(ROOT, run, TASK)
        self.assertTrue(any('needs-evidence' in x for x in errors))

    def test_needs_evidence_requires_true_case_and_matching_state(self):
        run = base_run()
        run.update({
            'decision': 'needs-evidence',
            'case_valid': None,
            'declared_state': None,
            'selected_skills': [],
            'selected_packs': [],
        })
        refresh_digest(run)
        errors = validate_agent_run(ROOT, run, TASK)
        self.assertTrue(any('needs-evidence' in x and 'case_valid true' in x for x in errors))
        self.assertTrue(any('needs-evidence' in x and 'declared_state' in x and 'task state' in x for x in errors))

    def test_valid_needs_evidence_contract_matches_task_state(self):
        run = base_run()
        run.update({
            'decision': 'needs-evidence',
            'case_valid': True,
            'declared_state': 'hypothesis',
            'selected_skills': [],
            'selected_packs': [],
        })
        refresh_digest(run)
        self.assertEqual(validate_agent_run(ROOT, run, TASK), [])

    def test_semantic_digest_ignores_telemetry_notes_and_versions(self):
        first = base_run()
        second = copy.deepcopy(first)
        second['telemetry'] = {'duration_ms': 9999, 'tokens': 123}
        second['notes'] = 'different note'
        second['agent']['version'] = 'other'
        second['adapter']['version'] = 'other'
        self.assertEqual(semantic_output_digest(first), semantic_output_digest(second))

    def test_wrong_provenance_digest_is_rejected(self):
        run = base_run()
        run['provenance']['output_digest'] = '0' * 64
        errors = validate_agent_run(ROOT, run, TASK)
        self.assertTrue(any('output_digest' in x for x in errors))


if __name__ == '__main__':
    unittest.main()
