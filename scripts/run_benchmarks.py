from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

from benchmark_core import evaluate_suite, normalize_result
from benchmark_report import render_report
from validate_benchmarks import validate_fixture, validate_suite


def _read_object(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(data, dict):
        raise ValueError(f'{path}: expected a JSON object')
    return data


def load_suite_inputs(root: Path, suite_path: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    root = Path(root).resolve()
    suite_path = Path(suite_path).resolve()
    suite = _read_object(suite_path)
    suite_issues = [x for x in validate_suite(root, suite, suite_path.as_posix()) if x.level == 'error']
    if suite_issues:
        raise ValueError('; '.join(f'{x.path}: {x.message}' for x in suite_issues))

    benchmark_root = suite_path.parent.parent
    fixtures: list[dict[str, Any]] = []
    for rel in suite.get('fixtures', []):
        fixture_path = benchmark_root / rel
        if not fixture_path.is_file():
            raise ValueError(f'{suite_path}: suite references missing fixture: {rel}')
        fixture = _read_object(fixture_path)
        fixture_issues = [x for x in validate_fixture(root, fixture, rel) if x.level == 'error']
        if fixture_issues:
            raise ValueError('; '.join(f'{x.path}: {x.message}' for x in fixture_issues))
        fixtures.append(fixture)
    return suite, fixtures


def run_suite_file(root: Path, suite_path: Path) -> dict[str, Any]:
    suite, fixtures = load_suite_inputs(root, suite_path)
    return evaluate_suite(Path(root).resolve(), suite, fixtures)


def _write_text(path: Path, content: str) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8', newline='\n')


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description='Run a deterministic Security Skills benchmark suite.')
    parser.add_argument('suite', type=Path, help='benchmark suite manifest JSON')
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--json', dest='json_output', type=Path, default=None, help='write normalized result JSON')
    parser.add_argument('--report', type=Path, default=None, help='write Markdown benchmark report')
    args = parser.parse_args(argv)

    try:
        result = run_suite_file(args.root, args.suite)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2

    normalized = normalize_result(result)
    report = render_report(result)
    try:
        if args.json_output is not None:
            _write_text(args.json_output, normalized)
        if args.report is not None:
            _write_text(args.report, report)
    except OSError as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2

    if args.json_output is None and args.report is None:
        sys.stdout.write(report)
    return 0 if result.get('passed') is True else 1


if __name__ == '__main__':
    raise SystemExit(main())
