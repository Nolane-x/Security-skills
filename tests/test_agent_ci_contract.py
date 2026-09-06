import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / '.github' / 'workflows' / 'validate.yml'


class AgentCiContractTests(unittest.TestCase):
    def test_matrix_runs_agent_contract_and_portability_smoke(self):
        text = WORKFLOW.read_text(encoding='utf-8')
        self.assertIn('Validate agent evaluation contracts', text)
        self.assertIn('Run agent evaluation portability smoke', text)

    def test_workflow_has_single_agent_eval_core_job_with_determinism_checks(self):
        text = WORKFLOW.read_text(encoding='utf-8')
        self.assertIn('agent-eval-core:', text)
        self.assertIn('needs: [validate, benchmark-core]', text)
        for phrase in (
            'Prepare agent tasks twice',
            'Check byte-identical agent tasks',
            'Evaluate reference replay twice',
            'Check byte-identical agent evaluation',
            'Build cross-agent matrix twice',
            'Check byte-identical cross-agent matrix',
        ):
            self.assertIn(phrase, text)


if __name__ == '__main__':
    unittest.main()
