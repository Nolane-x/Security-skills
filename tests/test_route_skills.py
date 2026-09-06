import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'scripts'
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from route_skills import route_case  # noqa: E402


def case(domains=None, state='hypothesis', goal='discover', authorized=True):
    return {
        'schema_version': 1,
        'case_id': 'route-1',
        'title': 'Routing fixture',
        'scope': {'authorized': authorized, 'kind': 'sandbox', 'target': 'fixture'},
        'domains': domains or ['parsers'],
        'goal': goal,
        'state': state,
        'claim': 'Synthetic research claim.',
        'environment': {'target_revision': 'abc', 'platform': 'linux'},
        'observations': ['fixture behavior observed'] if state != 'hypothesis' else [],
        'controls': {'positive': [], 'negative': []},
        'reproducer': {'steps': [], 'fixture_digest': ''},
        'root_cause': '',
        'security_consequence': '',
        'uncertainties': [],
        'fix_validation': {},
    }


class RouteSkillTests(unittest.TestCase):
    def test_route_rejects_unauthorized_case(self):
        with self.assertRaises(ValueError):
            route_case(ROOT, case(authorized=False))

    def test_route_starts_with_scope_skill(self):
        result = route_case(ROOT, case(['parsers', 'protocols']), limit=8)
        self.assertEqual('security-scope-and-authorization', result['skills'][0])

    def test_route_matches_mobile_domain(self):
        result = route_case(ROOT, case(['mobile', 'android', 'routing'], goal='root-cause'), limit=10)
        self.assertIn('android-intent-and-deeplink-analysis', result['skills'])

    def test_android_route_excludes_ios_specific_skills(self):
        result = route_case(ROOT, case(['mobile', 'android', 'routing'], goal='root-cause'), limit=12)
        self.assertFalse(any(name.startswith('ios-') for name in result['skills']))

    def test_mobile_route_recommends_mobile_pack(self):
        result = route_case(ROOT, case(['mobile', 'android', 'routing'], goal='root-cause'), limit=10)
        self.assertIn('mobile-security', result['packs'])

    def test_route_closes_and_orders_prerequisites(self):
        result = route_case(ROOT, case(['mobile', 'android', 'routing'], goal='root-cause'), limit=10)
        skills = result['skills']
        self.assertLess(skills.index('security-scope-and-authorization'), skills.index('android-component-exposure-analysis'))
        self.assertLess(skills.index('android-component-exposure-analysis'), skills.index('android-intent-and-deeplink-analysis'))

    def test_validated_remediation_route_prioritizes_fix_skills(self):
        c = case(['remediation'], state='validated', goal='remediate')
        c['controls'] = {'positive': ['control'], 'negative': ['negative']}
        c['reproducer'] = {'steps': ['run fixture'], 'fixture_digest': 'sha256:1'}
        c['root_cause'] = 'validated synthetic cause'
        c['security_consequence'] = 'bounded synthetic consequence'
        result = route_case(ROOT, c, limit=8)
        self.assertIn('remediation-and-regression', result['skills'])
        self.assertIn('regression-matrix-testing', result['skills'])

    def test_generic_parser_route_excludes_web_specific_skills(self):
        result = route_case(ROOT, case(['parsers', 'memory-safety'], state='observed', goal='validate'), limit=12)
        self.assertNotIn('file-upload-processing-analysis', result['skills'])
        self.assertNotIn('web-routing-and-middleware-analysis', result['skills'])

    def test_observed_analysis_precedes_validation_stage(self):
        result = route_case(ROOT, case(['parsers', 'memory-safety'], state='observed', goal='validate'), limit=12)
        skills = result['skills']
        self.assertLess(skills.index('parser-state-machine-analysis'), skills.index('evidence-driven-vulnerability-validation'))

    def test_pack_recommendations_respect_case_domains(self):
        result = route_case(ROOT, case(['parsers', 'memory-safety'], state='observed', goal='validate'), limit=12)
        self.assertNotIn('virtualization-boundaries', result['packs'])
        self.assertNotIn('firmware-and-boot', result['packs'])
        self.assertIn('memory-safety', result['packs'])
        self.assertIn('parsers-and-protocols', result['packs'])

    def test_route_is_deterministic(self):
        c = case(['virtualization', 'shared-memory'], goal='validate')
        c['state'] = 'observed'
        c['observations'] = ['synthetic ring invariant mismatch']
        a = route_case(ROOT, copy.deepcopy(c), limit=12)
        b = route_case(ROOT, copy.deepcopy(c), limit=12)
        self.assertEqual(a, b)


if __name__ == '__main__':
    unittest.main()
