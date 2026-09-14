import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / '.github' / 'workflows' / 'validate.yml'


class SuperiorityCiContractTests(unittest.TestCase):
    def test_workflow_has_single_superiority_core_job_with_determinism_gates(self):
        text = WORKFLOW.read_text(encoding='utf-8')
        self.assertEqual(text.count('  superiority-court-core:'), 1)
        section = text.split('  superiority-court-core:', 1)[1]
        self.assertIn('needs: [validate, benchmark-core, agent-eval-core]', section)
        self.assertIn('python-version: "3.13"', section)
        self.assertIn('build_contestant_view.py', section)
        self.assertIn('byte-identical contestant views', section)
        self.assertIn('CONTESTANT_VIEW.json', section)
        self.assertGreaterEqual(section.count('--surface-digest'), 2)
        self.assertIn('prepare_superiority_tasks.py', section)
        self.assertIn('SUITE_MANIFEST.json', section)
        self.assertGreaterEqual(section.count('--manifest'), 4)
        self.assertIn('prepare_superiority_replays.py', section)
        self.assertIn('score_superiority_runs.py', section)
        self.assertIn('build_superiority_court.py', section)
        self.assertIn('byte-identical superiority tasks', section)
        self.assertIn('byte-identical superiority scores', section)
        self.assertIn('byte-identical superiority court', section)
        self.assertIn("authority_commitment']", section)
        self.assertIn("contestant_surface_digest']", section)
        self.assertIn("absolute_winner'] == 'opaque-a'", section)


if __name__ == '__main__':
    unittest.main()
