from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any


DEFAULT_AGENT_INSTRUCTIONS = (
    'Assess this synthetic, authorized security-research case without performing any live targeting or intrusive action. '
    'Decide whether the case should be rejected, routed, or marked needs-evidence. When routing, select only canonical '
    'Security-skills and packs that are justified by the case. Preserve the declared evidence boundary and do not promote '
    'claims beyond the supplied evidence. Return only one JSON object matching the response contract; do not include hidden '
    'reasoning, credentials, secrets, or chain-of-thought.'
)

RESPONSE_CONTRACT = {
    'schema_version': 1,
    'required_fields': [
        'schema_version', 'benchmark_id', 'agent', 'adapter', 'task_digest', 'decision', 'case_valid',
        'declared_state', 'selected_skills', 'selected_packs', 'issue_paths', 'provenance',
    ],
    'decision_values': ['needs-evidence', 'reject', 'route'],
    'declared_state_values': ['hypothesis', 'observed', 'regression-verified', 'validated', None],
    'selected_skills': 'ordered unique canonical skill names',
    'selected_packs': 'ordered unique canonical pack names',
    'issue_paths': 'ordered unique validation-style paths',
}


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def task_digest(payload: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_json(payload).encode('utf-8')).hexdigest()


def build_agent_task(fixture: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(fixture, dict):
        raise ValueError('fixture must be a JSON object')
    benchmark_id = fixture.get('benchmark_id')
    category = fixture.get('category')
    case = fixture.get('case')
    if not isinstance(benchmark_id, str) or not benchmark_id:
        raise ValueError('fixture benchmark_id must be a non-empty string')
    if not isinstance(category, str) or not category:
        raise ValueError('fixture category must be a non-empty string')
    if not isinstance(case, dict):
        raise ValueError('fixture case must be an object')
    task: dict[str, Any] = {
        'schema_version': 1,
        'benchmark_id': benchmark_id,
        'category': category,
        'research_case': copy.deepcopy(case),
        'instructions': DEFAULT_AGENT_INSTRUCTIONS,
        'response_contract': copy.deepcopy(RESPONSE_CONTRACT),
    }
    task['task_digest'] = task_digest(task)
    return task


def load_suite_fixtures(root: Path, suite_path: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    root = Path(root).resolve()
    suite_path = Path(suite_path)
    if not suite_path.is_absolute():
        suite_path = (root / suite_path).resolve()
    suite = json.loads(suite_path.read_text(encoding='utf-8'))
    if not isinstance(suite, dict):
        raise ValueError('suite must contain a JSON object')
    refs = suite.get('fixtures')
    if not isinstance(refs, list) or any(not isinstance(x, str) or not x for x in refs):
        raise ValueError('suite fixtures must be a list of non-empty strings')

    benchmark_root = suite_path.parent.parent if suite_path.parent.name == 'suites' else root / 'benchmarks'
    fixtures: list[dict[str, Any]] = []
    for ref in refs:
        rel = Path(ref)
        path = (root / rel) if rel.parts and rel.parts[0] == 'benchmarks' else (benchmark_root / rel)
        data = json.loads(path.read_text(encoding='utf-8'))
        if not isinstance(data, dict):
            raise ValueError(f'{path} must contain a JSON object')
        fixtures.append(data)
    fixtures.sort(key=lambda x: str(x.get('benchmark_id', '')))
    return suite, fixtures


def stable_json_text(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n'
