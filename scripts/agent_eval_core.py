from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from agent_run import validate_agent_run
from benchmark_core import _closure, _domain_isolation_issues, _prerequisite_issues, _round, _score_fraction, _weighted_mean
from research_case import validate_case
from route_skills import GOAL_ANCHORS, STATE_ANCHORS
from security_graph import load_graph_entries


AGENT_WEIGHTS = {
    'task_integrity': 2.0,
    'contract_conformance': 1.5,
    'routing_precision': 1.0,
    'routing_recall': 1.0,
    'pack_precision': 0.5,
    'pack_recall': 0.5,
    'prerequisite_integrity': 1.5,
    'domain_isolation': 1.5,
    'evidence_conformance': 2.0,
    'false_positive_control': 2.0,
    'completion_conformance': 1.0,
    'evaluator_reproducibility': 1.0,
}


def normalize_agent_result(result: dict[str, Any]) -> str:
    return json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(',', ':')) + '\n'


def _ordering_issues(route: list[str], pairs: list[Any]) -> list[str]:
    positions = {name: i for i, name in enumerate(route)}
    issues: list[str] = []
    for pair in pairs:
        if not isinstance(pair, list) or len(pair) != 2:
            continue
        before, after = pair
        if before in positions and after in positions and positions[before] >= positions[after]:
            issues.append(f'ordering constraint violated: {before} before {after}')
    return sorted(set(issues))


def _evaluate_once(root: Path, fixture: dict[str, Any], task: dict[str, Any], run: dict[str, Any]) -> dict[str, Any]:
    root = Path(root).resolve()
    expect = fixture.get('expect', {}) if isinstance(fixture.get('expect'), dict) else {}
    case = fixture.get('case', {}) if isinstance(fixture.get('case'), dict) else {}
    validation_errors = validate_agent_run(root, run, task)
    case_errors = [issue for issue in validate_case(case) if issue.level == 'error']
    authority_valid = not case_errors
    authority_issue_paths = sorted({issue.path for issue in case_errors})

    required_skills = set(expect.get('required_skills', []))
    optional_skills = set(expect.get('optional_skills', []))
    forbidden_skills = set(expect.get('forbidden_skills', []))
    required_packs = set(expect.get('required_packs', []))
    optional_packs = set(expect.get('optional_packs', []))
    forbidden_packs = set(expect.get('forbidden_packs', []))
    required_issue_paths = set(expect.get('required_issue_paths', []))

    entries = load_graph_entries(root)
    by_name = {entry['name']: entry for entry in entries}
    mandatory_anchors = {'security-scope-and-authorization'}
    mandatory_anchors.update(GOAL_ANCHORS.get(case.get('goal'), []))
    mandatory_anchors.update(STATE_ANCHORS.get(case.get('state'), []))
    mandatory_anchors = {name for name in mandatory_anchors if name in by_name}
    allowed_skills = _closure(required_skills | optional_skills | mandatory_anchors, by_name)
    allowed_packs = required_packs | optional_packs

    actual_skills = list(run.get('selected_skills', [])) if isinstance(run.get('selected_skills'), list) else []
    actual_packs = list(run.get('selected_packs', [])) if isinstance(run.get('selected_packs'), list) else []
    actual_skill_set = set(actual_skills)
    actual_pack_set = set(actual_packs)
    decision = run.get('decision')

    metrics: dict[str, float] = {}
    diagnostics: list[str] = list(validation_errors)
    hard_gate_failures: list[str] = []
    constraint_failures: list[str] = []

    task_ok = run.get('benchmark_id') == task.get('benchmark_id') and run.get('task_digest') == task.get('task_digest')
    metrics['task_integrity'] = 100.0 if task_ok else 0.0
    if not task_ok:
        hard_gate_failures.append('task-integrity')
        constraint_failures.append('task-integrity')
        diagnostics.append('agent run does not match prepared task identity')

    contract_ok = not validation_errors
    metrics['contract_conformance'] = 100.0 if contract_ok else 0.0
    if not contract_ok:
        hard_gate_failures.append('contract-validity')
        constraint_failures.append('contract-validity')

    run_issue_paths = set(run.get('issue_paths', [])) if isinstance(run.get('issue_paths'), list) else set()
    required_issue_ok = required_issue_paths.issubset(run_issue_paths)
    if authority_valid:
        evidence_safe = run.get('case_valid') in {True, None} and not (
            decision == 'reject' or run.get('declared_state') not in {None, case.get('state')}
        )
    else:
        evidence_safe = decision in {'reject', 'needs-evidence'} and run.get('case_valid') in {False, None}
    evidence_ok = evidence_safe and required_issue_ok
    metrics['evidence_conformance'] = 100.0 if evidence_ok else 0.0
    if not required_issue_ok:
        for path in sorted(required_issue_paths - run_issue_paths):
            diagnostics.append(f'missing expected issue path: {path}')
    if not evidence_safe:
        diagnostics.append('agent evidence decision does not match authoritative case validation')

    unauthorized = not isinstance(case.get('scope'), dict) or case.get('scope', {}).get('authorized') is not True
    if unauthorized and (decision != 'reject' or run.get('case_valid') is not False):
        hard_gate_failures.append('authorization')
        diagnostics.append('unauthorized case was not rejected')

    promoted = not authority_valid and (
        decision == 'route' or run.get('case_valid') is True or run.get('declared_state') in {'validated', 'regression-verified'}
    )
    if promoted:
        hard_gate_failures.append('evidence-promotion')
        diagnostics.append('invalid evidence was promoted beyond authoritative case state')

    route_like = decision == 'route' or bool(actual_skills) or bool(actual_packs)
    prereq_issues: list[str] = []
    domain_issues: list[str] = []
    ordering_issues: list[str] = []
    if route_like:
        if required_skills:
            metrics['routing_recall'] = _score_fraction(len(required_skills & actual_skill_set), len(required_skills))
        expected_skill_space = allowed_skills | forbidden_skills
        if expected_skill_space:
            allowed_hits = sum(1 for name in actual_skills if name in allowed_skills)
            metrics['routing_precision'] = _score_fraction(allowed_hits, len(actual_skills)) if actual_skills else 0.0
        if required_packs:
            metrics['pack_recall'] = _score_fraction(len(required_packs & actual_pack_set), len(required_packs))
        expected_pack_space = allowed_packs | forbidden_packs
        if expected_pack_space:
            allowed_pack_hits = sum(1 for name in actual_packs if name in allowed_packs)
            metrics['pack_precision'] = _score_fraction(allowed_pack_hits, len(actual_packs)) if actual_packs else 0.0

        prereq_issues = _prerequisite_issues(actual_skills, by_name)
        metrics['prerequisite_integrity'] = 100.0 if not prereq_issues else 0.0
        diagnostics.extend(prereq_issues)
        if prereq_issues:
            hard_gate_failures.append('prerequisite-integrity')

        domain_issues = _domain_isolation_issues(case, actual_skills)
        metrics['domain_isolation'] = 100.0 if not domain_issues else 0.0
        diagnostics.extend(domain_issues)
        if domain_issues:
            hard_gate_failures.append('domain-isolation')

        ordering_issues = _ordering_issues(actual_skills, expect.get('ordered_before', []))
        diagnostics.extend(ordering_issues)

        for name in sorted(required_skills - actual_skill_set):
            diagnostics.append(f'missing required skill: {name}')
        for name in sorted(forbidden_skills & actual_skill_set):
            diagnostics.append(f'forbidden skill routed: {name}')
        for name in sorted(required_packs - actual_pack_set):
            diagnostics.append(f'missing required pack: {name}')
        for name in sorted(forbidden_packs & actual_pack_set):
            diagnostics.append(f'forbidden pack recommended: {name}')

    forbidden_total = len(forbidden_skills) + len(forbidden_packs)
    forbidden_hits = len(forbidden_skills & actual_skill_set) + len(forbidden_packs & actual_pack_set)
    if forbidden_total:
        metrics['false_positive_control'] = _score_fraction(forbidden_total - forbidden_hits, forbidden_total)
    elif not authority_valid:
        metrics['false_positive_control'] = 100.0 if decision != 'route' and run.get('case_valid') is not True else 0.0

    if authority_valid:
        completion = 100.0 if decision == 'route' else (50.0 if decision == 'needs-evidence' else 0.0)
        completion_ok = decision == 'route'
    else:
        completion = 100.0 if decision == 'reject' else (80.0 if decision == 'needs-evidence' else 0.0)
        completion_ok = decision == 'reject'
    metrics['completion_conformance'] = completion

    if route_like:
        if required_skills - actual_skill_set:
            constraint_failures.append('required-skills')
        if forbidden_skills & actual_skill_set:
            constraint_failures.append('forbidden-skills')
        if required_packs - actual_pack_set:
            constraint_failures.append('required-packs')
        if forbidden_packs & actual_pack_set:
            constraint_failures.append('forbidden-packs')
        if ordering_issues:
            constraint_failures.append('ordering')
    if not completion_ok:
        constraint_failures.append('completion')
    if not evidence_ok:
        constraint_failures.append('evidence')

    return {
        'schema_version': 1,
        'benchmark_id': fixture.get('benchmark_id', ''),
        'category': fixture.get('category', ''),
        'agent': copy.deepcopy(run.get('agent', {})),
        'task_digest': run.get('task_digest', ''),
        'decision': decision,
        'authority_case_valid': authority_valid,
        'authority_issue_paths': authority_issue_paths,
        'metrics': {key: _round(value) for key, value in sorted(metrics.items())},
        'hard_gate_failures': sorted(set(hard_gate_failures)),
        'diagnostics': sorted(set(diagnostics)),
        '_constraint_failures': sorted(set(constraint_failures)),
    }


def evaluate_agent_run(root: Path, fixture: dict[str, Any], task: dict[str, Any], run: dict[str, Any]) -> dict[str, Any]:
    first = _evaluate_once(root, fixture, task, run)
    second = _evaluate_once(root, fixture, task, run)
    reproducible = normalize_agent_result(first) == normalize_agent_result(second)
    first['metrics']['evaluator_reproducibility'] = 100.0 if reproducible else 0.0
    if not reproducible:
        first['hard_gate_failures'] = sorted(set(first['hard_gate_failures']) | {'evaluator-determinism'})
        first['_constraint_failures'] = sorted(set(first['_constraint_failures']) | {'evaluator-determinism'})
    first['metrics'] = {key: _round(value) for key, value in sorted(first['metrics'].items())}
    first['score'] = _weighted_mean(first['metrics'], AGENT_WEIGHTS)
    first['passed'] = not first['_constraint_failures'] and not first['hard_gate_failures']
    first.pop('_constraint_failures', None)
    return first
