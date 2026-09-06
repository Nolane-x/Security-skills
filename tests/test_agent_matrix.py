import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'scripts'
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from agent_matrix import build_agent_matrix, normalize_matrix  # noqa: E402


def result(agent, benchmark, *, digest='a' * 64, passed=True, score=100.0, category='routing'):
    return {
        'schema_version': 1,
        'benchmark_id': benchmark,
        'category': category,
        'agent': {'id': agent},
        'task_digest': digest,
        'score': score,
        'metrics': {'evidence_conformance': score},
        'hard_gate_failures': [] if passed else ['evidence-promotion'],
        'passed': passed,
    }


class AgentMatrixTests(unittest.TestCase):
    def test_matrix_orders_agents_and_benchmarks_deterministically(self):
        inputs = [result('z-agent', 'b2'), result('a-agent', 'b2'), result('a-agent', 'b1')]
        matrix = build_agent_matrix('suite', ['b1', 'b2'], inputs)
        self.assertEqual([x['agent_id'] for x in matrix['agents']], ['a-agent', 'z-agent'])
        self.assertEqual(matrix['agents'][0]['missing_fixture_ids'], [])
        self.assertEqual(matrix['agents'][1]['missing_fixture_ids'], ['b1'])
        self.assertEqual(normalize_matrix(matrix), normalize_matrix(build_agent_matrix('suite', ['b1', 'b2'], copy.deepcopy(inputs))))

    def test_duplicate_agent_benchmark_pair_is_rejected(self):
        with self.assertRaises(ValueError):
            build_agent_matrix('suite', ['b1'], [result('a', 'b1'), result('a', 'b1')])

    def test_cross_agent_digest_mismatch_is_rejected(self):
        with self.assertRaises(ValueError):
            build_agent_matrix('suite', ['b1'], [result('a', 'b1', digest='a' * 64), result('b', 'b1', digest='b' * 64)])

    def test_scores_and_category_aggregates_are_reported(self):
        matrix = build_agent_matrix('suite', ['b1', 'b2'], [
            result('a', 'b1', score=100.0, category='routing'),
            result('a', 'b2', score=80.0, category='evidence'),
        ])
        agent = matrix['agents'][0]
        self.assertEqual(agent['overall_score'], 90.0)
        self.assertEqual(agent['category_scores'], {'evidence': 80.0, 'routing': 100.0})
        self.assertEqual(agent['hard_gate_failure_count'], 0)


if __name__ == '__main__':
    unittest.main()
