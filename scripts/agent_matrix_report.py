from __future__ import annotations

from typing import Any


def render_agent_matrix_report(matrix: dict[str, Any]) -> str:
    lines = [
        f"# Cross-Agent Security Conformance: {matrix.get('suite', '')}",
        '',
        f"**Status:** {'PASS' if matrix.get('passed') else 'FAIL'}",
        f"**Expected fixtures:** {matrix.get('expected_fixture_count', 0)}",
        '',
        '## Agents',
        '',
        '| Agent | Score | Passed | Failed | Hard gates | Missing |',
        '| --- | ---: | ---: | ---: | ---: | --- |',
    ]
    for agent in matrix.get('agents', []):
        missing = ', '.join(agent.get('missing_fixture_ids', [])) or 'none'
        lines.append(
            f"| `{agent.get('agent_id', '')}` | {float(agent.get('overall_score', 0.0)):.2f} | "
            f"{agent.get('passed_fixture_count', 0)} | {agent.get('failed_fixture_count', 0)} | "
            f"{agent.get('hard_gate_failure_count', 0)} | {missing} |"
        )
        if agent.get('category_scores'):
            lines.extend(['', f"### `{agent.get('agent_id', '')}` category scores", ''])
            for name, score in sorted(agent['category_scores'].items()):
                lines.append(f"- `{name}`: {float(score):.2f}")
    lines.extend([
        '',
        '> Scores measure conformance to this benchmark contract. They are not a universal ranking of model intelligence or security capability.',
        '',
    ])
    return '\n'.join(lines)
