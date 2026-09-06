import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'scripts'
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from research_case import CaseIssue, validate_case, validate_transition  # noqa: E402


def base_case(state='hypothesis'):
    return {
        'schema_version': 1,
        'case_id': 'case-001',
        'title': 'Synthetic parser state issue',
        'scope': {'authorized': True, 'kind': 'sandbox', 'target': 'local fixture'},
        'domains': ['parsers', 'memory-safety'],
        'goal': 'validate',
        'state': state,
        'claim': 'A length/state mismatch may reach an invalid access.',
        'environment': {'target_revision': 'abc123', 'platform': 'linux-x64'},
        'observations': [],
        'controls': {'positive': [], 'negative': []},
        'reproducer': {'steps': [], 'fixture_digest': ''},
        'root_cause': '',
        'security_consequence': '',
        'uncertainties': ['impact is not yet established'],
        'fix_validation': {},
    }


class ResearchCaseTests(unittest.TestCase):
    def test_hypothesis_case_requires_authorized_scope(self):
        case = base_case()
        case['scope']['authorized'] = False
        issues = validate_case(case)
        self.assertTrue(any('authorized scope' in x.message for x in issues))

    def test_observed_requires_environment_and_observation(self):
        case = base_case('observed')
        case['environment'] = {}
        issues = validate_case(case)
        messages = '\n'.join(x.message for x in issues)
        self.assertIn('environment', messages)
        self.assertIn('observation', messages)

    def test_validated_requires_causal_and_control_evidence(self):
        case = base_case('validated')
        case['observations'] = ['sanitizer invalid-read at parser.c:42']
        issues = validate_case(case)
        messages = '\n'.join(x.message for x in issues)
        self.assertIn('root cause', messages)
        self.assertIn('security consequence', messages)
        self.assertIn('positive control', messages)
        self.assertIn('negative control', messages)
        self.assertIn('reproducer', messages)

    def test_validated_case_can_pass(self):
        case = base_case('validated')
        case['observations'] = ['sanitizer invalid-read at parser.c:42']
        case['controls'] = {'positive': ['known-valid fixture parses'], 'negative': ['same-length safe state does not fault']}
        case['reproducer'] = {'steps': ['run fixture under ASan'], 'fixture_digest': 'sha256:deadbeef'}
        case['root_cause'] = 'state transition preserves a stale length across record replacement'
        case['security_consequence'] = 'out-of-bounds read in the authorized harness'
        self.assertEqual([], [x for x in validate_case(case) if x.level == 'error'])

    def test_regression_verified_requires_fixed_revision_and_controls(self):
        case = base_case('regression-verified')
        case['observations'] = ['sanitizer invalid-read at parser.c:42']
        case['controls'] = {'positive': ['known-valid fixture parses'], 'negative': ['same-length safe state does not fault']}
        case['reproducer'] = {'steps': ['run fixture under ASan'], 'fixture_digest': 'sha256:deadbeef'}
        case['root_cause'] = 'stale length'
        case['security_consequence'] = 'out-of-bounds read'
        issues = validate_case(case)
        self.assertTrue(any('fix validation' in x.message for x in issues))

    def test_regression_verified_case_can_pass(self):
        case = base_case('regression-verified')
        case['observations'] = ['sanitizer invalid-read at parser.c:42']
        case['controls'] = {'positive': ['known-valid fixture parses'], 'negative': ['same-length safe state does not fault']}
        case['reproducer'] = {'steps': ['run fixture under ASan'], 'fixture_digest': 'sha256:deadbeef'}
        case['root_cause'] = 'stale length'
        case['security_consequence'] = 'out-of-bounds read'
        case['fix_validation'] = {
            'fixed_revision': 'def456',
            'vulnerability_no_longer_reproduces': True,
            'controls_still_pass': True,
        }
        self.assertEqual([], [x for x in validate_case(case) if x.level == 'error'])

    def test_transition_cannot_skip_evidence_stage(self):
        old = base_case('hypothesis')
        new = copy.deepcopy(old)
        new['state'] = 'validated'
        issues = validate_transition(old, new)
        self.assertTrue(any('cannot skip' in x.message for x in issues))

    def test_transition_allows_next_stage_when_case_valid(self):
        old = base_case('observed')
        old['observations'] = ['crash reproduced']
        new = copy.deepcopy(old)
        new['state'] = 'validated'
        new['controls'] = {'positive': ['valid fixture'], 'negative': ['safe-state fixture']}
        new['reproducer'] = {'steps': ['run fixture'], 'fixture_digest': 'sha256:1'}
        new['root_cause'] = 'stale length'
        new['security_consequence'] = 'invalid read'
        self.assertEqual([], [x for x in validate_transition(old, new) if x.level == 'error'])


if __name__ == '__main__':
    unittest.main()
