from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from research_case import validate_case
from route_skills import GOAL_ANCHORS, STATE_ANCHORS, route_case
from security_graph import load_graph_entries

METRIC_NAMES = (
    'routing_precision',
    'routing_recall',
    'pack_precision',
    'pack_recall',
    'prerequisite_integrity',
    'domain_isolation',
    'evidence_conformance',
    'false_positive_control',
    'reproducibility',
)

DEFAULT_WEIGHTS = {
    'routing_precision': 1.0,
    'routing_recall': 1.0,
    'pack_precision': 0.5,
    'pack_recall': 0.5,
    'prerequisite_integrity': 1.5,
    'domain_isolation': 1.5,
    'evidence_conformance': 2.0,
    'false_positive_control': 2.0,
    'reproducibility': 1.0,
}

HARD_GATES = {
    'authorization',
    'evidence-promotion',
    'domain-isolation',
    'prerequisite-integrity',
    'determinism',
}


def _round(value: float) -> float:
    return round(float(value) + 0.0, 2)


def _score_fraction(hit: int, total: int) -> float:
    if total <= 0:
        return 100.0
    return _round(100.0 * hit / total)


def _closure(names: set[str], by_name: dict[str, dict[str, Any]]) -> set[str]:
    out: set[str] = set()

    def visit(name: str) -> None:
        if name in out or name not in by_name:
            return
        for dep in by_name[name].get('prerequisites', []):
            visit(dep)
        out.add(name)

    for name in sorted(names):
        visit(name)
    return out


def _prerequisite_issues(route: list[str], by_name: dict[str, dict[str, Any]]) -> list[str]:
    positions = {name: i for i, name in enumerate(route)}
    issues: list[str] = []
    for name in route:
        for dep in by_name.get(name, {}).get('prerequisites', []):
            if dep not in positions:
                issues.append(f'missing prerequisite {dep} for {name}')
            elif positions[dep] > positions[name]:
                issues.append(f'prerequisite ordered after dependent: {dep} -> {name}')
    return sorted(set(issues))


def _domain_isolation_issues(case: dict[str, Any], route: list[str]) -> list[str]:
    domains = {str(x).lower() for x in case.get('domains', [])}
    issues: list[str] = []
    if 'android' in domains:
        issues.extend(f'android route leaked iOS skill {name}' for name in route if name.startswith('ios-'))
    if 'ios' in domains:
        issues.extend(f'iOS route leaked Android skill {name}' for name in route if name.startswith('android-'))
    return sorted(issues)


def _evaluate_once(root: Path, fixture: dict[str, Any]) -> dict[str, Any]:
    expect = fixture.get('expect', {})
    expected_valid = expect.get('case_valid') is True
    case = fixture.get('case', {})
    issues = [x for x in validate_case(case) if x.level == 'error']
    issue_paths = sorted({x.path for x in issues})
    actual_valid = not issues
    route: dict[str, Any] | None = None
    if actual_valid:
        route = route_case(root, case, limit=int(expect.get('route_limit', 12)))

    required_skills = set(expect.get('required_skills', []))
    optional_skills = set(expect.get('optional_skills', []))
    forbidden_skills = set(expect.get('forbidden_skills', []))
    required_packs = set(expect.get('required_packs', []))
    optional_packs = set(expect.get('optional_packs', []))
    forbidden_packs = set(expect.get('forbidden_packs', []))
    required_issue_paths = set(expect.get('required_issue_paths', []))
    enabled_gates = set(expect.get('hard_gates', []))

    actual_skills = list(route.get('skills', [])) if route else []
    actual_packs = list(route.get('packs', [])) if route else []
    actual_skill_set = set(actual_skills)
    actual_pack_set = set(actual_packs)

    entries = load_graph_entries(root)
    by_name = {x['name']: x for x in entries}
    mandatory_anchors = {'security-scope-and-authorization'}
    mandatory_anchors.update(GOAL_ANCHORS.get(case.get('goal'), []))
    mandatory_anchors.update(STATE_ANCHORS.get(case.get('state'), []))
    mandatory_anchors = {name for name in mandatory_anchors if name in by_name}
    allowed_skills = _closure(required_skills | optional_skills | mandatory_anchors, by_name)
    allowed_packs = required_packs | optional_packs

    metrics: dict[str, float] = {}
    diagnostics: list[str] = []

    validity_matches = actual_valid == expected_valid
    issue_matches = required_issue_paths.issubset(issue_paths)
    metrics['evidence_conformance'] = 100.0 if validity_matches and issue_matches else 0.0
    if not validity_matches:
        diagnostics.append(f"case validity mismatch: expected {str(expected_valid).lower()} got {str(actual_valid).lower()}")
    for path in sorted(required_issue_paths - set(issue_paths)):
        diagnostics.append(f'missing expected issue path: {path}')

    if route is not None:
        if required_skills:
            metrics['routing_recall'] = _score_fraction(len(required_skills & actual_skill_set), len(required_skills))
        expected_route_space = allowed_skills | forbidden_skills
        if expected_route_space:
            allowed_hits = sum(1 for name in actual_skills if name in allowed_skills)
            metrics['routing_precision'] = _score_fraction(allowed_hits, len(actual_skills))
        if required_packs:
            metrics['pack_recall'] = _score_fraction(len(required_packs & actual_pack_set), len(required_packs))
        expected_pack_space = allowed_packs | forbidden_packs
        if expected_pack_space:
            allowed_pack_hits = sum(1 for name in actual_packs if name in allowed_packs)
            metrics['pack_precision'] = _score_fraction(allowed_pack_hits, len(actual_packs))

        prereq_issues = _prerequisite_issues(actual_skills, by_name)
        metrics['prerequisite_integrity'] = 100.0 if not prereq_issues else 0.0
        diagnostics.extend(prereq_issues)

        domain_issues = _domain_isolation_issues(case, actual_skills)
        metrics['domain_isolation'] = 100.0 if not domain_issues else 0.0
        diagnostics.extend(domain_issues)

        for name in sorted(required_skills - actual_skill_set):
            diagnostics.append(f'missing required skill: {name}')
        for name in sorted(forbidden_skills & actual_skill_set):
            diagnostics.append(f'forbidden skill routed: {name}')
        for name in sorted(required_packs - actual_pack_set):
            diagnostics.append(f'missing required pack: {name}')
        for name in sorted(forbidden_packs & actual_pack_set):
            diagnostics.append(f'forbidden pack recommended: {name}')

        positions = {name: i for i, name in enumerate(actual_skills)}
        for pair in expect.get('ordered_before', []):
            if not isinstance(pair, list) or len(pair) != 2:
                continue
            before, after = pair
            if before in positions and after in positions and positions[before] >= positions[after]:
                diagnostics.append(f'ordering constraint violated: {before} before {after}')

    forbidden_total = len(forbidden_skills) + len(forbidden_packs)
    forbidden_hits = len(forbidden_skills & actual_skill_set) + len(forbidden_packs & actual_pack_set)
    if forbidden_total or not expected_valid:
        metrics['false_positive_control'] = _score_fraction(forbidden_total - forbidden_hits, forbidden_total) if forbidden_total else (100.0 if not actual_valid else 0.0)

    hard_gate_failures: list[str] = []
    if 'authorization' in enabled_gates:
        unauthorized = not isinstance(case.get('scope'), dict) or case.get('scope', {}).get('authorized') is not True
        if unauthorized and (actual_valid or 'scope.authorized' not in issue_paths):
            hard_gate_failures.append('authorization')
    if 'evidence-promotion' in enabled_gates and not expected_valid and actual_valid:
        hard_gate_failures.append('evidence-promotion')
    if 'domain-isolation' in enabled_gates and route is not None and metrics.get('domain_isolation') != 100.0:
        hard_gate_failures.append('domain-isolation')
    if 'prerequisite-integrity' in enabled_gates and route is not None and metrics.get('prerequisite_integrity') != 100.0:
        hard_gate_failures.append('prerequisite-integrity')

    constraint_failures = []
    if not validity_matches or not issue_matches:
        constraint_failures.append('evidence')
    if route is not None:
        if required_skills - actual_skill_set:
            constraint_failures.append('required-skills')
        if forbidden_skills & actual_skill_set:
            constraint_failures.append('forbidden-skills')
        if required_packs - actual_pack_set:
            constraint_failures.append('required-packs')
        if forbidden_packs & actual_pack_set:
            constraint_failures.append('forbidden-packs')
        if any(x.startswith('ordering constraint violated:') for x in diagnostics):
            constraint_failures.append('ordering')

    return {
        'benchmark_id': fixture.get('benchmark_id', ''),
        'category': fixture.get('category', ''),
        'case_valid': actual_valid,
        'issue_paths': issue_paths,
        'route': route,
        'metrics': {k: _round(v) for k, v in sorted(metrics.items())},
        'hard_gate_failures': sorted(set(hard_gate_failures)),
        'diagnostics': sorted(set(diagnostics)),
        'constraint_failures': sorted(set(constraint_failures)),
    }


def evaluate_fixture(root: Path, fixture: dict[str, Any]) -> dict[str, Any]:
    root = Path(root).resolve()
    first = _evaluate_once(root, fixture)
    second = _evaluate_once(root, fixture)
    reproducible = normalize_result(first) == normalize_result(second)
    result = first
    result['metrics']['reproducibility'] = 100.0 if reproducible else 0.0
    enabled_gates = set(fixture.get('expect', {}).get('hard_gates', []))
    if 'determinism' in enabled_gates and not reproducible:
        result['hard_gate_failures'] = sorted(set(result['hard_gate_failures']) | {'determinism'})
    fixture_weights = {**DEFAULT_WEIGHTS, **fixture.get('weights', {})}
    result['score'] = _weighted_mean(result['metrics'], fixture_weights)
    result['passed'] = not result['constraint_failures'] and not result['hard_gate_failures']
    result.pop('constraint_failures', None)
    return result


def _weighted_mean(metrics: dict[str, float], weights: dict[str, float]) -> float:
    applicable = [(metrics[name], float(weights.get(name, DEFAULT_WEIGHTS.get(name, 1.0)))) for name in sorted(metrics) if float(weights.get(name, DEFAULT_WEIGHTS.get(name, 1.0))) > 0]
    if not applicable:
        return 0.0
    numerator = sum(score * weight for score, weight in applicable)
    denominator = sum(weight for _, weight in applicable)
    return _round(numerator / denominator)


def evaluate_suite(root: Path, suite: dict[str, Any], fixtures: list[dict[str, Any]]) -> dict[str, Any]:
    ordered = sorted(fixtures, key=lambda x: x.get('benchmark_id', ''))
    suite_gates = set(suite.get('hard_gates', []))
    prepared: list[dict[str, Any]] = []
    for fixture in ordered:
        item = copy.deepcopy(fixture)
        expect = item.setdefault('expect', {})
        expect['hard_gates'] = sorted(set(expect.get('hard_gates', [])) | suite_gates)
        prepared.append(item)
    results = [evaluate_fixture(root, fixture) for fixture in prepared]
    aggregate: dict[str, float] = {}
    for metric in METRIC_NAMES:
        values = [r['metrics'][metric] for r in results if metric in r['metrics']]
        if values:
            aggregate[metric] = _round(sum(values) / len(values))
    weights = {**DEFAULT_WEIGHTS, **suite.get('weights', {})}
    overall = _weighted_mean(aggregate, weights)
    hard_count = sum(len(r['hard_gate_failures']) for r in results)
    passed_count = sum(1 for r in results if r['passed'])
    minimum = _round(float(suite.get('minimum_score', 0.0)))
    passed = hard_count == 0 and passed_count == len(results) and overall >= minimum
    return {
        'schema_version': 1,
        'suite': suite.get('name', ''),
        'fixture_count': len(results),
        'passed_fixture_count': passed_count,
        'failed_fixture_count': len(results) - passed_count,
        'overall_score': overall,
        'minimum_score': minimum,
        'hard_gate_failures': hard_count,
        'metrics': {k: aggregate[k] for k in sorted(aggregate)},
        'fixtures': results,
        'passed': passed,
    }


def normalize_result(result: dict[str, Any]) -> str:
    return json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(',', ':')) + '\n'
