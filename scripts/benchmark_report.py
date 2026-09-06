from __future__ import annotations

from collections import Counter
from typing import Any


def _fmt_score(value: Any) -> str:
    try:
        return f'{float(value):.2f}'
    except (TypeError, ValueError):
        return 'n/a'


def render_report(result: dict[str, Any]) -> str:
    suite = str(result.get('suite', ''))
    status = 'PASS' if result.get('passed') is True else 'FAIL'
    lines = [
        f'# Benchmark Report: {suite}',
        '',
        f'**Status:** {status}',
        f"**Overall score:** {_fmt_score(result.get('overall_score'))} / 100.00",
        f"**Minimum score:** {_fmt_score(result.get('minimum_score'))}",
        f"**Fixtures:** {result.get('passed_fixture_count', 0)} passed, {result.get('failed_fixture_count', 0)} failed, {result.get('fixture_count', 0)} total",
        f"**Hard-gate failures:** {result.get('hard_gate_failures', 0)}",
        '',
        '## Metrics',
        '',
        '| Metric | Score |',
        '| --- | ---: |',
    ]
    for name, score in sorted((result.get('metrics') or {}).items()):
        lines.append(f'| `{name}` | {_fmt_score(score)} |')

    fixtures = list(result.get('fixtures') or [])
    failed = [item for item in fixtures if item.get('passed') is not True]
    lines.extend(['', '## Failed fixtures', ''])
    if not failed:
        lines.append('None.')
    else:
        for item in sorted(failed, key=lambda x: str(x.get('benchmark_id', ''))):
            benchmark_id = str(item.get('benchmark_id', ''))
            category = str(item.get('category', ''))
            lines.append(f'### `{benchmark_id}` ({category})')
            gates = sorted(str(x) for x in item.get('hard_gate_failures', []))
            diagnostics = sorted(str(x) for x in item.get('diagnostics', []))
            lines.append(f"- Hard gates: {', '.join(f'`{x}`' for x in gates) if gates else 'none'}")
            if diagnostics:
                lines.append('- Diagnostics:')
                lines.extend(f'  - {message}' for message in diagnostics)
            else:
                lines.append('- Diagnostics: none')
            lines.append('')

    counts = Counter(str(item.get('category', '')) for item in fixtures)
    failures = Counter(str(item.get('category', '')) for item in failed)
    lines.extend(['## Category summary', '', '| Category | Total | Failed |', '| --- | ---: | ---: |'])
    for category in sorted(counts):
        lines.append(f'| `{category}` | {counts[category]} | {failures[category]} |')
    return '\n'.join(lines).rstrip() + '\n'
