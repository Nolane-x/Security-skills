from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from pathlib import Path, PurePosixPath
import sys
from typing import Any

from benchmark_core import HARD_GATES, METRIC_NAMES
from research_case import validate_case
from security_graph import load_graph_entries, load_packs

CATEGORIES = {
    'authorization',
    'domain-isolation',
    'evidence',
    'false-positive',
    'remediation',
    'routing',
}
EXPECT_LIST_KEYS = (
    'required_skills',
    'optional_skills',
    'forbidden_skills',
    'required_packs',
    'optional_packs',
    'forbidden_packs',
    'required_issue_paths',
    'hard_gates',
)


@dataclass(frozen=True)
class BenchmarkIssue:
    level: str
    path: str
    message: str


def _nonempty_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _string_list(value: Any, *, allow_empty: bool = True) -> bool:
    return (
        isinstance(value, list)
        and (allow_empty or bool(value))
        and all(_nonempty_text(x) for x in value)
        and len(value) == len(set(value))
    )


def _read_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(data, dict):
        raise ValueError('must contain a JSON object')
    return data


def _validate_weights(weights: Any, source: str) -> list[BenchmarkIssue]:
    issues: list[BenchmarkIssue] = []
    if weights is None:
        return issues
    if not isinstance(weights, dict):
        return [BenchmarkIssue('error', source, 'weights must be an object')]
    for name, value in weights.items():
        if name not in METRIC_NAMES:
            issues.append(BenchmarkIssue('error', source, f'unknown metric in weights: {name}'))
        if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0:
            issues.append(BenchmarkIssue('error', source, f'weight for {name} must be a non-negative number'))
    return issues


def validate_fixture(root: Path, fixture: dict[str, Any], source: str) -> list[BenchmarkIssue]:
    issues: list[BenchmarkIssue] = []
    if not isinstance(fixture, dict):
        return [BenchmarkIssue('error', source, 'benchmark fixture must be a JSON object')]
    if fixture.get('schema_version') != 1:
        issues.append(BenchmarkIssue('error', source, 'schema_version must be integer 1'))
    if not _nonempty_text(fixture.get('benchmark_id')):
        issues.append(BenchmarkIssue('error', source, 'benchmark_id must be non-empty text'))
    if fixture.get('category') not in CATEGORIES:
        issues.append(BenchmarkIssue('error', source, f'category must be one of: {", ".join(sorted(CATEGORIES))}'))
    if not _nonempty_text(fixture.get('description')):
        issues.append(BenchmarkIssue('error', source, 'description must be non-empty text'))
    if not _string_list(fixture.get('tags', [])):
        issues.append(BenchmarkIssue('error', source, 'tags must be a duplicate-free list of non-empty strings'))

    expect = fixture.get('expect')
    if not isinstance(expect, dict):
        issues.append(BenchmarkIssue('error', source, 'expect must be an object'))
        return issues
    if not isinstance(expect.get('case_valid'), bool):
        issues.append(BenchmarkIssue('error', source, 'expect.case_valid must be boolean'))

    for key in EXPECT_LIST_KEYS:
        if not _string_list(expect.get(key, [])):
            issues.append(BenchmarkIssue('error', source, f'expect.{key} must be a duplicate-free list of non-empty strings'))

    route_limit = expect.get('route_limit')
    if isinstance(route_limit, bool) or not isinstance(route_limit, int) or route_limit < 1:
        issues.append(BenchmarkIssue('error', source, 'expect.route_limit must be an integer >= 1'))

    ordered = expect.get('ordered_before')
    if not isinstance(ordered, list):
        issues.append(BenchmarkIssue('error', source, 'expect.ordered_before must be a list of two-item skill pairs'))
        ordered = []
    for pair in ordered:
        if not isinstance(pair, list) or len(pair) != 2 or not all(_nonempty_text(x) for x in pair):
            issues.append(BenchmarkIssue('error', source, 'expect.ordered_before entries must be two-item skill pairs'))

    graph_entries = load_graph_entries(root)
    skills = {x['name'] for x in graph_entries}
    packs = {x['name'] for x in load_packs(root)}
    for key in ('required_skills', 'optional_skills', 'forbidden_skills'):
        for name in expect.get(key, []) if isinstance(expect.get(key), list) else []:
            if name not in skills:
                issues.append(BenchmarkIssue('error', source, f'unknown skill reference in expect.{key}: {name}'))
    for key in ('required_packs', 'optional_packs', 'forbidden_packs'):
        for name in expect.get(key, []) if isinstance(expect.get(key), list) else []:
            if name not in packs:
                issues.append(BenchmarkIssue('error', source, f'unknown pack reference in expect.{key}: {name}'))
    for pair in ordered:
        if isinstance(pair, list) and len(pair) == 2:
            for name in pair:
                if isinstance(name, str) and name not in skills:
                    issues.append(BenchmarkIssue('error', source, f'unknown skill reference in expect.ordered_before: {name}'))

    for gate in expect.get('hard_gates', []) if isinstance(expect.get('hard_gates'), list) else []:
        if gate not in HARD_GATES:
            issues.append(BenchmarkIssue('error', source, f'unknown hard gate: {gate}'))

    issues.extend(_validate_weights(fixture.get('weights'), source))

    case = fixture.get('case')
    if not isinstance(case, dict):
        issues.append(BenchmarkIssue('error', source, 'case must be a research-case object'))
    else:
        case_errors = [x for x in validate_case(case) if x.level == 'error']
        expected_valid = expect.get('case_valid') is True
        if expected_valid and case_errors:
            issues.append(BenchmarkIssue('error', source, 'fixture expected valid but embedded research case is invalid'))
        if not expected_valid and not case_errors:
            issues.append(BenchmarkIssue('error', source, 'fixture expected invalid but embedded research case is valid'))
        actual_issue_paths = {x.path for x in case_errors}
        for path in expect.get('required_issue_paths', []) if isinstance(expect.get('required_issue_paths'), list) else []:
            if not expected_valid and path not in actual_issue_paths:
                issues.append(BenchmarkIssue('error', source, f'required_issue_paths entry not produced by embedded case: {path}'))

    return issues


def validate_suite(root: Path, suite: dict[str, Any], source: str) -> list[BenchmarkIssue]:
    issues: list[BenchmarkIssue] = []
    if not isinstance(suite, dict):
        return [BenchmarkIssue('error', source, 'benchmark suite must be a JSON object')]
    if suite.get('schema_version') != 1:
        issues.append(BenchmarkIssue('error', source, 'suite schema_version must be integer 1'))
    if not _nonempty_text(suite.get('name')):
        issues.append(BenchmarkIssue('error', source, 'suite name must be non-empty text'))
    if not _nonempty_text(suite.get('description')):
        issues.append(BenchmarkIssue('error', source, 'suite description must be non-empty text'))
    if not _string_list(suite.get('fixtures'), allow_empty=False):
        issues.append(BenchmarkIssue('error', source, 'suite fixtures must be a non-empty duplicate-free list of paths'))
    minimum = suite.get('minimum_score')
    if isinstance(minimum, bool) or not isinstance(minimum, (int, float)) or not (0 <= float(minimum) <= 100):
        issues.append(BenchmarkIssue('error', source, 'minimum_score must be between 0 and 100'))
    issues.extend(_validate_weights(suite.get('weights'), source))
    gates = suite.get('hard_gates', [])
    if not _string_list(gates):
        issues.append(BenchmarkIssue('error', source, 'suite hard_gates must be a duplicate-free list of non-empty strings'))
    else:
        for gate in gates:
            if gate not in HARD_GATES:
                issues.append(BenchmarkIssue('error', source, f'unknown hard gate: {gate}'))
    for rel in suite.get('fixtures', []) if isinstance(suite.get('fixtures'), list) else []:
        path = PurePosixPath(rel)
        if path.is_absolute() or '..' in path.parts or not rel.startswith('cases/') or not rel.endswith('.json'):
            issues.append(BenchmarkIssue('error', source, f'invalid fixture path in suite: {rel}'))
    return issues


def validate_corpus(root: Path, benchmark_root: Path | None = None) -> list[BenchmarkIssue]:
    root = Path(root).resolve()
    bench = Path(benchmark_root).resolve() if benchmark_root is not None else root / 'benchmarks'
    issues: list[BenchmarkIssue] = []
    cases_root = bench / 'cases'
    suites_root = bench / 'suites'
    fixture_paths = sorted(cases_root.glob('**/*.json')) if cases_root.exists() else []
    suite_paths = sorted(suites_root.glob('*.json')) if suites_root.exists() else []

    fixtures: dict[str, dict[str, Any]] = {}
    ids: dict[str, str] = {}
    for path in fixture_paths:
        rel = path.relative_to(bench).as_posix()
        try:
            data = _read_json(path)
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            issues.append(BenchmarkIssue('error', rel, f'invalid JSON: {exc}'))
            continue
        fixtures[rel] = data
        issues.extend(validate_fixture(root, data, rel))
        benchmark_id = data.get('benchmark_id')
        if isinstance(benchmark_id, str) and benchmark_id:
            if benchmark_id in ids:
                issues.append(BenchmarkIssue('error', rel, f'duplicate benchmark_id {benchmark_id}; first seen in {ids[benchmark_id]}'))
            else:
                ids[benchmark_id] = rel

    referenced: set[str] = set()
    suite_data: dict[str, dict[str, Any]] = {}
    for path in suite_paths:
        rel = path.relative_to(bench).as_posix()
        try:
            data = _read_json(path)
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            issues.append(BenchmarkIssue('error', rel, f'invalid JSON: {exc}'))
            continue
        suite_data[path.name] = data
        issues.extend(validate_suite(root, data, rel))
        for fixture_rel in data.get('fixtures', []) if isinstance(data.get('fixtures'), list) else []:
            if fixture_rel not in fixtures:
                issues.append(BenchmarkIssue('error', rel, f'suite references missing fixture: {fixture_rel}'))
            else:
                referenced.add(fixture_rel)

    for rel in sorted(set(fixtures) - referenced):
        issues.append(BenchmarkIssue('error', rel, f'orphan fixture is not listed in any suite: {rel}'))

    core = suite_data.get('core.json')
    portability = suite_data.get('portability.json')
    if core is None:
        issues.append(BenchmarkIssue('error', 'suites/core.json', 'required core benchmark suite is missing'))
    else:
        core_refs = core.get('fixtures', []) if isinstance(core.get('fixtures'), list) else []
        core_set = set(core_refs)
        for rel in sorted(set(fixtures) - core_set):
            issues.append(BenchmarkIssue('error', rel, f'fixture is not listed in core suite: {rel}'))
        if len(core_refs) != 36:
            issues.append(BenchmarkIssue('error', 'suites/core.json', f'Wave 5 core suite must contain exactly 36 fixtures; found {len(core_refs)}'))
        category_counts = {category: 0 for category in CATEGORIES}
        for rel in core_refs:
            fixture = fixtures.get(rel)
            if fixture is not None and fixture.get('category') in category_counts:
                category_counts[fixture['category']] += 1
        for category in sorted(CATEGORIES):
            if category_counts[category] != 6:
                issues.append(BenchmarkIssue('error', 'suites/core.json', f'Wave 5 core suite category {category} must contain exactly 6 fixtures; found {category_counts[category]}'))

    if portability is None:
        issues.append(BenchmarkIssue('error', 'suites/portability.json', 'required portability benchmark suite is missing'))
    elif core is not None:
        core_set = set(core.get('fixtures', []) if isinstance(core.get('fixtures'), list) else [])
        portability_refs = portability.get('fixtures', []) if isinstance(portability.get('fixtures'), list) else []
        for rel in sorted(set(portability_refs) - core_set):
            issues.append(BenchmarkIssue('error', 'suites/portability.json', f'portability fixture is not in core suite: {rel}'))
        if set(portability_refs) == core_set and core_set:
            issues.append(BenchmarkIssue('error', 'suites/portability.json', 'portability suite must be a proper subset of core'))

    if not fixture_paths:
        issues.append(BenchmarkIssue('error', str(cases_root), 'benchmark corpus contains no fixtures'))
    if not suite_paths:
        issues.append(BenchmarkIssue('error', str(suites_root), 'benchmark corpus contains no suites'))
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description='Validate Security Skills benchmark fixtures and suite manifests.')
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    issues = validate_corpus(args.root)
    for issue in issues:
        print(f'{issue.level.upper()}: {issue.path}: {issue.message}')
    errors = [x for x in issues if x.level == 'error']
    if errors:
        print(f'Benchmark validation failed: {len(errors)} error(s).', file=sys.stderr)
        return 1
    print('Benchmark validation passed: 0 errors.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
