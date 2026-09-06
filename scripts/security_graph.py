from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
from typing import Any

from skilllib import discover_skills

MATURITY_VALUES = {'experimental', 'beta', 'stable'}
EVIDENCE_STAGE_VALUES = {'hypothesis', 'observed', 'validated', 'regression-verified'}


@dataclass(frozen=True)
class GraphIssue:
    level: str
    path: Path
    message: str


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(data, dict):
        raise ValueError(f'{path} must contain a JSON object')
    return data


def _validate_string_list(data: dict[str, Any], key: str, path: Path, *, allow_empty: bool = True) -> list[GraphIssue]:
    issues: list[GraphIssue] = []
    value = data.get(key)
    if not isinstance(value, list) or any(not isinstance(x, str) or not x for x in value):
        issues.append(GraphIssue('error', path, f'{key} must be a list of non-empty strings'))
        return issues
    if not allow_empty and not value:
        issues.append(GraphIssue('error', path, f'{key} must not be empty'))
    if len(value) != len(set(value)):
        issues.append(GraphIssue('error', path, f'{key} must not contain duplicates'))
    return issues


def _find_cycle(prereqs: dict[str, list[str]]) -> list[str] | None:
    state: dict[str, int] = {}
    stack: list[str] = []

    def visit(node: str) -> list[str] | None:
        state[node] = 1
        stack.append(node)
        for dep in prereqs.get(node, []):
            if dep not in prereqs:
                continue
            if state.get(dep, 0) == 0:
                cycle = visit(dep)
                if cycle:
                    return cycle
            elif state.get(dep) == 1:
                i = stack.index(dep)
                return stack[i:] + [dep]
        stack.pop()
        state[node] = 2
        return None

    for node in sorted(prereqs):
        if state.get(node, 0) == 0:
            cycle = visit(node)
            if cycle:
                return cycle
    return None


def validate_graph(root: Path) -> list[GraphIssue]:
    root = root.resolve()
    issues: list[GraphIssue] = []
    skills = discover_skills(root)
    names = {s.name for s in skills}
    prereqs: dict[str, list[str]] = {}

    for skill in skills:
        path = skill.path.parent / 'skill.meta.json'
        if not path.exists():
            issues.append(GraphIssue('error', skill.path, 'missing required graph sidecar: skill.meta.json'))
            continue
        try:
            data = load_json(path)
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            issues.append(GraphIssue('error', path, f'invalid graph metadata: {exc}'))
            continue

        if data.get('schema_version') != 1:
            issues.append(GraphIssue('error', path, 'schema_version must be integer 1'))
        if data.get('maturity') not in MATURITY_VALUES:
            issues.append(GraphIssue('error', path, f'maturity must be one of {sorted(MATURITY_VALUES)}'))
        if data.get('evidence_stage') not in EVIDENCE_STAGE_VALUES:
            issues.append(GraphIssue('error', path, f'evidence_stage must be one of {sorted(EVIDENCE_STAGE_VALUES)}'))

        for key in ('domains', 'prerequisites', 'composes_with'):
            issues.extend(_validate_string_list(data, key, path, allow_empty=(key != 'domains')))

        skill_prereqs = data.get('prerequisites') if isinstance(data.get('prerequisites'), list) else []
        skill_composes = data.get('composes_with') if isinstance(data.get('composes_with'), list) else []
        prereqs[skill.name] = [x for x in skill_prereqs if isinstance(x, str)]

        if skill.name in skill_prereqs:
            issues.append(GraphIssue('error', path, 'a skill cannot require itself'))
        if skill.name in skill_composes:
            issues.append(GraphIssue('error', path, 'a skill cannot compose with itself'))

        for dep in skill_prereqs:
            if isinstance(dep, str) and dep not in names:
                issues.append(GraphIssue('error', path, f'unknown prerequisite: {dep}'))
        for other in skill_composes:
            if isinstance(other, str) and other not in names:
                issues.append(GraphIssue('error', path, f'unknown composes_with skill: {other}'))

    cycle = _find_cycle(prereqs)
    if cycle:
        issues.append(GraphIssue('error', root / 'skills', 'prerequisite cycle detected: ' + ' -> '.join(cycle)))

    pack_root = root / 'packs'
    if pack_root.exists():
        for path in sorted(pack_root.glob('*.json')):
            try:
                data = load_json(path)
            except (OSError, json.JSONDecodeError, ValueError) as exc:
                issues.append(GraphIssue('error', path, f'invalid pack manifest: {exc}'))
                continue
            if data.get('schema_version') != 1:
                issues.append(GraphIssue('error', path, 'pack schema_version must be integer 1'))
            if data.get('name') != path.stem:
                issues.append(GraphIssue('error', path, f"pack name must match filename stem '{path.stem}'"))
            if not isinstance(data.get('description'), str) or not data.get('description'):
                issues.append(GraphIssue('error', path, 'pack description must be a non-empty string'))
            for key in ('skills', 'default_flow'):
                issues.extend(_validate_string_list(data, key, path, allow_empty=False))
            pack_skills = data.get('skills') if isinstance(data.get('skills'), list) else []
            flow = data.get('default_flow') if isinstance(data.get('default_flow'), list) else []
            entrypoint = data.get('entrypoint')
            if not isinstance(entrypoint, str) or entrypoint not in names:
                issues.append(GraphIssue('error', path, f'pack entrypoint must reference a known skill: {entrypoint}'))
            for name in pack_skills:
                if isinstance(name, str) and name not in names:
                    issues.append(GraphIssue('error', path, f'pack references unknown skill: {name}'))
            for name in flow:
                if isinstance(name, str) and name not in pack_skills:
                    issues.append(GraphIssue('error', path, f'default_flow skill is not listed in pack skills: {name}'))

    return issues


def load_graph_entries(root: Path) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for skill in discover_skills(root):
        meta_path = skill.path.parent / 'skill.meta.json'
        if not meta_path.exists():
            continue
        meta = load_json(meta_path)
        entries.append({
            'name': skill.name,
            'description': skill.description,
            'category': skill.metadata.get('nolane-security-category', ''),
            'authorization': skill.metadata.get('nolane-security-authorization', ''),
            'maturity': meta.get('maturity', ''),
            'domains': meta.get('domains', []),
            'prerequisites': meta.get('prerequisites', []),
            'composes_with': meta.get('composes_with', []),
            'evidence_stage': meta.get('evidence_stage', ''),
            'path': skill.path.relative_to(root).as_posix(),
        })
    entries.sort(key=lambda x: x['name'])
    return entries


def load_packs(root: Path) -> list[dict[str, Any]]:
    packs: list[dict[str, Any]] = []
    for path in sorted((root / 'packs').glob('*.json')) if (root / 'packs').exists() else []:
        data = load_json(path)
        packs.append({**data, 'path': path.relative_to(root).as_posix()})
    return packs
