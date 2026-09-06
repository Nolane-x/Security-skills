from __future__ import annotations

import json
from collections import defaultdict
from typing import Any


def _round(value: float) -> float:
    return round(float(value) + 0.0, 2)


def normalize_matrix(matrix: dict[str, Any]) -> str:
    return json.dumps(matrix, ensure_ascii=False, sort_keys=True, separators=(',', ':')) + '\n'


def _mean(values: list[float]) -> float:
    return _round(sum(values) / len(values)) if values else 0.0


def build_agent_matrix(suite_name: str, expected_ids: list[str], results: list[dict[str, Any]]) -> dict[str, Any]:
    expected = sorted(set(expected_ids))
    seen: set[tuple[str, str]] = set()
    task_digests: dict[str, str] = {}
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for result in results:
        agent = result.get('agent') if isinstance(result.get('agent'), dict) else {}
        agent_id = agent.get('id')
        benchmark_id = result.get('benchmark_id')
        digest = result.get('task_digest')
        if not isinstance(agent_id, str) or not agent_id or not isinstance(benchmark_id, str) or not benchmark_id:
            raise ValueError('every result must contain agent.id and benchmark_id')
        pair = (agent_id, benchmark_id)
        if pair in seen:
            raise ValueError(f'duplicate agent/benchmark result: {agent_id}/{benchmark_id}')
        seen.add(pair)
        if benchmark_id in task_digests and task_digests[benchmark_id] != digest:
            raise ValueError(f'task digest mismatch across agents for benchmark {benchmark_id}')
        task_digests[benchmark_id] = digest
        grouped[agent_id].append(result)

    agents: list[dict[str, Any]] = []
    for agent_id in sorted(grouped):
        items = sorted(grouped[agent_id], key=lambda x: x['benchmark_id'])
        present = {item['benchmark_id'] for item in items}
        metrics: dict[str, list[float]] = defaultdict(list)
        categories: dict[str, list[float]] = defaultdict(list)
        hard_count = 0
        passed_count = 0
        for item in items:
            for name, value in sorted(item.get('metrics', {}).items()):
                if isinstance(value, (int, float)):
                    metrics[name].append(float(value))
            category = str(item.get('category', ''))
            if category:
                categories[category].append(float(item.get('score', 0.0)))
            hard_count += len(item.get('hard_gate_failures', []))
            if item.get('passed') is True:
                passed_count += 1
        agents.append({
            'agent_id': agent_id,
            'evaluated_fixture_count': len(items),
            'passed_fixture_count': passed_count,
            'failed_fixture_count': len(items) - passed_count,
            'hard_gate_failure_count': hard_count,
            'overall_score': _mean([float(item.get('score', 0.0)) for item in items]),
            'metrics': {name: _mean(values) for name, values in sorted(metrics.items())},
            'category_scores': {name: _mean(values) for name, values in sorted(categories.items())},
            'missing_fixture_ids': sorted(set(expected) - present),
        })

    complete = bool(agents) and all(not agent['missing_fixture_ids'] for agent in agents)
    passed = complete and all(agent['failed_fixture_count'] == 0 and agent['hard_gate_failure_count'] == 0 for agent in agents)
    return {
        'schema_version': 1,
        'suite': suite_name,
        'expected_fixture_count': len(expected),
        'task_digests': {key: task_digests[key] for key in sorted(task_digests)},
        'agents': agents,
        'passed': passed,
    }
