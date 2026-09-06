from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from agent_eval_core import evaluate_agent_run
from agent_matrix import build_agent_matrix, normalize_matrix
from agent_matrix_report import render_agent_matrix_report
from agent_task import build_agent_task, load_suite_fixtures


ROOT = Path(__file__).resolve().parents[1]


def _run_paths(values: list[str]) -> list[Path]:
    paths: list[Path] = []
    for value in values:
        path = Path(value)
        if path.is_file():
            paths.append(path)
        elif path.is_dir():
            paths.extend(sorted(path.rglob('*.json')))
        else:
            raise FileNotFoundError(path)
    return sorted(set(paths))


def evaluate_paths(root: Path, suite_path: Path, run_paths: list[Path]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    suite, fixtures = load_suite_fixtures(root, suite_path)
    fixture_by_id = {fixture['benchmark_id']: fixture for fixture in fixtures}
    task_by_id = {benchmark_id: build_agent_task(fixture) for benchmark_id, fixture in fixture_by_id.items()}
    results: list[dict[str, Any]] = []
    for path in run_paths:
        run = json.loads(path.read_text(encoding='utf-8'))
        if not isinstance(run, dict):
            raise ValueError(f'{path}: run must be a JSON object')
        benchmark_id = run.get('benchmark_id')
        if benchmark_id not in fixture_by_id:
            raise ValueError(f'{path}: unknown benchmark_id {benchmark_id!r}')
        results.append(evaluate_agent_run(root, fixture_by_id[benchmark_id], task_by_id[benchmark_id], run))
    matrix = build_agent_matrix(
        str(suite.get('name', '')),
        [fixture['benchmark_id'] for fixture in fixtures],
        results,
    )
    return matrix, results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description='Evaluate normalized agent-run artifacts against a benchmark suite.')
    parser.add_argument('suite')
    parser.add_argument('runs', nargs='+')
    parser.add_argument('--json', dest='json_out')
    parser.add_argument('--report')
    args = parser.parse_args(argv)
    try:
        paths = _run_paths(args.runs)
        if not paths:
            raise ValueError('no agent-run JSON artifacts found')
        matrix, _ = evaluate_paths(ROOT, Path(args.suite), paths)
        if args.json_out:
            Path(args.json_out).write_text(normalize_matrix(matrix), encoding='utf-8')
        report = render_agent_matrix_report(matrix)
        if args.report:
            Path(args.report).write_text(report, encoding='utf-8')
        else:
            print(report, end='')
        return 0 if matrix.get('passed') else 1
    except (OSError, json.JSONDecodeError, ValueError, KeyError, TypeError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
