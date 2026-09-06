from __future__ import annotations

from dataclasses import dataclass
from typing import Any

STATES = ('hypothesis', 'observed', 'validated', 'regression-verified')
GOALS = ('discover', 'root-cause', 'validate', 'remediate', 'report')
SCOPE_KINDS = ('local', 'owned', 'sandbox', 'ctf', 'explicit')


@dataclass(frozen=True)
class CaseIssue:
    level: str
    path: str
    message: str


def _nonempty_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _nonempty_list(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(_nonempty_text(x) for x in value)


def validate_case(case: dict[str, Any]) -> list[CaseIssue]:
    issues: list[CaseIssue] = []
    if not isinstance(case, dict):
        return [CaseIssue('error', '$', 'research case must be a JSON object')]

    if case.get('schema_version') != 1:
        issues.append(CaseIssue('error', 'schema_version', 'schema_version must be 1'))
    for key in ('case_id', 'title', 'claim'):
        if not _nonempty_text(case.get(key)):
            issues.append(CaseIssue('error', key, f'{key} must be non-empty text'))

    state = case.get('state')
    if state not in STATES:
        issues.append(CaseIssue('error', 'state', f'state must be one of: {", ".join(STATES)}'))
        return issues

    goal = case.get('goal')
    if goal not in GOALS:
        issues.append(CaseIssue('error', 'goal', f'goal must be one of: {", ".join(GOALS)}'))

    domains = case.get('domains')
    if not _nonempty_list(domains):
        issues.append(CaseIssue('error', 'domains', 'domains must contain at least one non-empty domain'))

    scope = case.get('scope')
    if not isinstance(scope, dict) or scope.get('authorized') is not True:
        issues.append(CaseIssue('error', 'scope.authorized', 'research case requires authorized scope'))
    else:
        if scope.get('kind') not in SCOPE_KINDS:
            issues.append(CaseIssue('error', 'scope.kind', f'scope kind must be one of: {", ".join(SCOPE_KINDS)}'))
        if not _nonempty_text(scope.get('target')):
            issues.append(CaseIssue('error', 'scope.target', 'authorized scope must identify the target'))

    state_index = STATES.index(state)
    if state_index >= STATES.index('observed'):
        env = case.get('environment')
        if not isinstance(env, dict) or not _nonempty_text(env.get('target_revision')) or not _nonempty_text(env.get('platform')):
            issues.append(CaseIssue('error', 'environment', 'observed evidence requires environment target_revision and platform'))
        if not _nonempty_list(case.get('observations')):
            issues.append(CaseIssue('error', 'observations', 'observed evidence requires at least one observation'))

    if state_index >= STATES.index('validated'):
        if not _nonempty_text(case.get('root_cause')):
            issues.append(CaseIssue('error', 'root_cause', 'validated evidence requires a causal root cause'))
        if not _nonempty_text(case.get('security_consequence')):
            issues.append(CaseIssue('error', 'security_consequence', 'validated evidence requires a bounded security consequence'))

        controls = case.get('controls')
        if not isinstance(controls, dict) or not _nonempty_list(controls.get('positive')):
            issues.append(CaseIssue('error', 'controls.positive', 'validated evidence requires at least one positive control'))
        if not isinstance(controls, dict) or not _nonempty_list(controls.get('negative')):
            issues.append(CaseIssue('error', 'controls.negative', 'validated evidence requires at least one negative control'))

        reproducer = case.get('reproducer')
        valid_reproducer = (
            isinstance(reproducer, dict)
            and _nonempty_list(reproducer.get('steps'))
            and _nonempty_text(reproducer.get('fixture_digest'))
        )
        if not valid_reproducer:
            issues.append(CaseIssue('error', 'reproducer', 'validated evidence requires a reproducer with steps and a fixture digest'))

    if state == 'regression-verified':
        fix = case.get('fix_validation')
        valid_fix = (
            isinstance(fix, dict)
            and _nonempty_text(fix.get('fixed_revision'))
            and fix.get('vulnerability_no_longer_reproduces') is True
            and fix.get('controls_still_pass') is True
        )
        if not valid_fix:
            issues.append(CaseIssue('error', 'fix_validation', 'regression-verified evidence requires fix validation with fixed revision, non-reproduction, and passing controls'))

    uncertainties = case.get('uncertainties')
    if uncertainties is not None and not isinstance(uncertainties, list):
        issues.append(CaseIssue('error', 'uncertainties', 'uncertainties must be a list'))

    return issues


def validate_transition(old: dict[str, Any], new: dict[str, Any]) -> list[CaseIssue]:
    issues = validate_case(new)
    old_state = old.get('state')
    new_state = new.get('state')
    if old_state not in STATES or new_state not in STATES:
        return issues
    old_i = STATES.index(old_state)
    new_i = STATES.index(new_state)
    if new_i > old_i + 1:
        issues.append(CaseIssue('error', 'state', f'evidence transition cannot skip stages: {old_state} -> {new_state}'))
    elif new_i < old_i:
        issues.append(CaseIssue('error', 'state', f'evidence transition cannot silently downgrade state: {old_state} -> {new_state}'))
    return issues
