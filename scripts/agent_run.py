from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from security_graph import load_graph_entries, load_packs


DECISIONS = {'reject', 'route', 'needs-evidence'}
STATES = {'hypothesis', 'observed', 'validated', 'regression-verified'}
PROVENANCE_SOURCES = {'replay', 'subprocess', 'imported'}


def _canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def _is_hex_digest(value: Any) -> bool:
    return isinstance(value, str) and len(value) == 64 and all(ch in '0123456789abcdef' for ch in value.lower())


def semantic_output_digest(run: dict[str, Any]) -> str:
    agent = run.get('agent') if isinstance(run.get('agent'), dict) else {}
    adapter = run.get('adapter') if isinstance(run.get('adapter'), dict) else {}
    provenance = run.get('provenance') if isinstance(run.get('provenance'), dict) else {}
    semantic = {
        'schema_version': run.get('schema_version'),
        'benchmark_id': run.get('benchmark_id'),
        'agent_id': agent.get('id'),
        'adapter_id': adapter.get('id'),
        'task_digest': run.get('task_digest'),
        'decision': run.get('decision'),
        'case_valid': run.get('case_valid'),
        'declared_state': run.get('declared_state'),
        'selected_skills': run.get('selected_skills'),
        'selected_packs': run.get('selected_packs'),
        'issue_paths': run.get('issue_paths'),
        'provenance_source': provenance.get('source'),
    }
    return hashlib.sha256(_canonical(semantic).encode('utf-8')).hexdigest()


def _validate_unique_string_list(run: dict[str, Any], key: str, errors: list[str]) -> list[str]:
    value = run.get(key)
    if not isinstance(value, list) or any(not isinstance(x, str) or not x for x in value):
        errors.append(f'{key} must be a list of non-empty strings')
        return []
    if len(value) != len(set(value)):
        errors.append(f'{key} must not contain duplicate values')
    return [x for x in value if isinstance(x, str) and x]


def validate_agent_run(root: Path, run: dict[str, Any], task: dict[str, Any] | None = None) -> list[str]:
    errors: list[str] = []
    if not isinstance(run, dict):
        return ['run must be a JSON object']
    if run.get('schema_version') != 1:
        errors.append('schema_version must be integer 1')
    benchmark_id = run.get('benchmark_id')
    if not isinstance(benchmark_id, str) or not benchmark_id:
        errors.append('benchmark_id must be a non-empty string')

    agent = run.get('agent')
    if not isinstance(agent, dict) or not isinstance(agent.get('id'), str) or not agent.get('id'):
        errors.append('agent.id must be a non-empty string')
    adapter = run.get('adapter')
    if not isinstance(adapter, dict) or not isinstance(adapter.get('id'), str) or not adapter.get('id'):
        errors.append('adapter.id must be a non-empty string')

    digest = run.get('task_digest')
    if not _is_hex_digest(digest):
        errors.append('task_digest must be a lowercase 64-character SHA-256 hex string')

    decision = run.get('decision')
    if decision not in DECISIONS:
        errors.append(f'decision must be one of {sorted(DECISIONS)}')
    case_valid = run.get('case_valid')
    if case_valid is not None and not isinstance(case_valid, bool):
        errors.append('case_valid must be true, false, or null')
    declared_state = run.get('declared_state')
    if declared_state is not None and declared_state not in STATES:
        errors.append(f'declared_state must be null or one of {sorted(STATES)}')

    skills = _validate_unique_string_list(run, 'selected_skills', errors)
    packs = _validate_unique_string_list(run, 'selected_packs', errors)
    _validate_unique_string_list(run, 'issue_paths', errors)

    known_skills = {entry['name'] for entry in load_graph_entries(Path(root))}
    known_packs = {pack.get('name') for pack in load_packs(Path(root)) if isinstance(pack.get('name'), str)}
    for name in sorted(set(skills) - known_skills):
        errors.append(f'unknown skill: {name}')
    for name in sorted(set(packs) - known_packs):
        errors.append(f'unknown pack: {name}')

    provenance = run.get('provenance')
    if not isinstance(provenance, dict):
        errors.append('provenance must be an object')
    else:
        if provenance.get('source') not in PROVENANCE_SOURCES:
            errors.append(f"provenance.source must be one of {sorted(PROVENANCE_SOURCES)}")
        output_digest = provenance.get('output_digest')
        if not _is_hex_digest(output_digest):
            errors.append('provenance.output_digest must be a lowercase 64-character SHA-256 hex string')
        elif output_digest != semantic_output_digest(run):
            errors.append('provenance.output_digest does not match semantic agent output')

    if decision == 'route':
        if case_valid is not True:
            errors.append('route decision requires case_valid true')
        if not skills:
            errors.append('route decision requires at least one selected skill')
    elif decision == 'reject':
        if case_valid is not False:
            errors.append('reject decision requires case_valid false')
        if skills or packs:
            errors.append('reject decision cannot select skills or packs')
    elif decision == 'needs-evidence' and case_valid is False:
        errors.append('needs-evidence decision requires case_valid true or null')

    if case_valid is False and declared_state in {'validated', 'regression-verified'}:
        errors.append('invalid case cannot declare validated or regression-verified state')

    if task is not None:
        if run.get('benchmark_id') != task.get('benchmark_id'):
            errors.append('benchmark_id does not match prepared task')
        if run.get('task_digest') != task.get('task_digest'):
            errors.append('task_digest does not match prepared task')

    return sorted(set(errors))
