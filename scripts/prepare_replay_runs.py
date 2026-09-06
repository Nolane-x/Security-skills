from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from agent_run import semantic_output_digest
from agent_task import build_agent_task, load_suite_fixtures, stable_json_text
from research_case import validate_case
from route_skills import route_case


ROOT = Path(__file__).resolve().parents[1]
PROFILES = {'reference', 'cautious', 'faulty'}


def _finish(run: dict[str, Any]) -> dict[str, Any]:
    run['provenance']['output_digest'] = semantic_output_digest(run)
    return run


def build_replay_run(root: Path, fixture: dict[str, Any], task: dict[str, Any], profile: str) -> dict[str, Any]:
    if profile not in PROFILES:
        raise ValueError(f'unknown replay profile: {profile}')
    case = fixture['case']
    errors = [issue for issue in validate_case(case) if issue.level == 'error']
    valid = not errors
    issue_paths = sorted({issue.path for issue in errors})
    base = {
        'schema_version': 1,
        'benchmark_id': task['benchmark_id'],
        'agent': {'id': f'replay-{profile}'},
        'adapter': {'id': 'deterministic-replay', 'version': '1'},
        'task_digest': task['task_digest'],
        'decision': 'reject',
        'case_valid': False,
        'declared_state': None,
        'selected_skills': [],
        'selected_packs': [],
        'issue_paths': issue_paths,
        'notes': f'deterministic {profile} replay profile',
        'provenance': {'source': 'replay', 'output_digest': ''},
    }

    if valid:
        route = route_case(root, case, limit=int(fixture.get('expect', {}).get('route_limit', 12)))
        base.update({
            'decision': 'route',
            'case_valid': True,
            'declared_state': case.get('state'),
            'selected_skills': list(route.get('skills', [])),
            'selected_packs': list(route.get('packs', [])),
            'issue_paths': [],
        })

    if profile == 'cautious' and valid and fixture.get('category') in {'evidence', 'false-positive'}:
        base.update({
            'decision': 'needs-evidence',
            'case_valid': True,
            'declared_state': case.get('state'),
            'selected_skills': [],
            'selected_packs': [],
            'issue_paths': [],
        })

    if profile == 'faulty':
        if not valid:
            base.update({
                'decision': 'route',
                'case_valid': True,
                'declared_state': case.get('state'),
                'selected_skills': ['security-scope-and-authorization'],
                'selected_packs': [],
                'issue_paths': [],
            })
        else:
            domains = {str(x).lower() for x in case.get('domains', [])}
            forbidden = list(fixture.get('expect', {}).get('forbidden_skills', []))
            if 'android' in domains and 'ios-entitlement-and-sandbox-analysis' not in base['selected_skills']:
                base['selected_skills'].append('ios-entitlement-and-sandbox-analysis')
            elif forbidden:
                name = forbidden[0]
                if name not in base['selected_skills']:
                    base['selected_skills'].append(name)
            else:
                base['selected_skills'] = ['security-scope-and-authorization']
                base['selected_packs'] = []

    return _finish(base)


def prepare_replay_runs(root: Path, suite_path: Path, out_dir: Path, profile: str) -> list[dict[str, Any]]:
    _, fixtures = load_suite_fixtures(root, suite_path)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    runs: list[dict[str, Any]] = []
    for fixture in fixtures:
        task = build_agent_task(fixture)
        run = build_replay_run(root, fixture, task, profile)
        runs.append(run)
        (out_dir / f"{run['benchmark_id']}.json").write_text(stable_json_text(run), encoding='utf-8')
    runs.sort(key=lambda x: x['benchmark_id'])
    return runs


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description='Generate deterministic offline replay agent-run artifacts.')
    parser.add_argument('suite')
    parser.add_argument('--profile', choices=sorted(PROFILES), required=True)
    parser.add_argument('--out', required=True)
    args = parser.parse_args(argv)
    try:
        runs = prepare_replay_runs(ROOT, Path(args.suite), Path(args.out), args.profile)
    except (OSError, json.JSONDecodeError, ValueError, KeyError, TypeError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2
    print(f'Prepared {len(runs)} {args.profile} replay run(s).')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
