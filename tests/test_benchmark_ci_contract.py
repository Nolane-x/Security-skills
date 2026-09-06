import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / '.github/workflows/validate.yml'


class BenchmarkCiContractTests(unittest.TestCase):
    def test_matrix_runs_benchmark_validator_and_portability_suite(self):
        text = WORKFLOW.read_text(encoding='utf-8')
        self.assertIn('python scripts/validate_benchmarks.py', text)
        self.assertIn('python scripts/run_benchmarks.py benchmarks/suites/portability.json', text)

    def test_workflow_has_single_core_benchmark_job_on_python_313(self):
        text = WORKFLOW.read_text(encoding='utf-8')
        self.assertIn('benchmark-core:', text)
        self.assertIn('python-version: "3.13"', text)
        self.assertIn('python scripts/run_benchmarks.py benchmarks/suites/core.json --json core-a.json', text)
        self.assertIn('python scripts/run_benchmarks.py benchmarks/suites/core.json --json core-b.json', text)
        self.assertIn("Path('core-a.json').read_bytes() == Path('core-b.json').read_bytes()", text)


if __name__ == '__main__':
    unittest.main()
