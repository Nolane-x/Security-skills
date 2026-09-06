from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

from research_case import STATES, validate_case
from security_graph import load_graph_entries, load_packs, validate_graph

GOAL_ANCHORS = {
    'discover': ['attack-surface-mapping', 'vulnerability-hypothesis-generation'],
    'root-cause': ['vulnerability-hypothesis-generation', 'static-dataflow-analysis'],
    'validate': ['evidence-driven-vulnerability-validation'],
    'remediate': ['remediation-and-regression', 'regression-matrix-testing'],
    'report': ['evidence-driven-vulnerability-validation'],
}

STATE_ANCHORS = {
    'hypothesis': ['attack-surface-mapping'],
    'observed': ['evidence-driven-vulnerability-validation'],
    'validated': ['remediation-and-regression', 'regression-matrix-testing'],
    'regression-verified': [],
}

MATURITY_WEIGHT = {'stable': 3, 'beta': 2, 'experimental': 1}
STAGE_WEIGHT = {name: i for i, name in enumerate(STATES)}
EXCLUSIVE_DOMAIN_GROUPS = ({'android', 'ios'},)
CONTEXT_DOMAINS = {
    'android', 'ios', 'mobile', 'firmware', 'embedded', 'virtualization', 'hypervisor',
    'web', 'smart-contracts', 'ai-security', 'agent-security', 'cloud', 'kernel',
    'browser', 'container', 'containers', 'driver', 'jit',
}
GOAL_PACKS = {
    'discover': {'research-foundation'},
    'root-cause': {'program-analysis'},
    'validate': {'verification-engineering'},
    'remediate': {'remediation', 'verification-engineering'},
    'report': {'verification-engineering'},
}


def _score(entry: dict[str, Any], domains: set[str], goal: str, state: str) -> tuple[int, int, int, str]:
    entry_domains = {str(x).lower() for x in entry.get('domains', [])}
    for group in EXCLUSIVE_DOMAIN_GROUPS:
        requested = domains & group
        offered = entry_domains & group
        if requested and offered and not (requested & offered):
            return (-1, 0, 0, entry['name'])
    context = entry_domains & CONTEXT_DOMAINS
    if context and not (context & domains):
        return (-1, 0, 0, entry['name'])
    overlap = len(domains & entry_domains)
    goal_bonus = 0
    if entry['name'] in GOAL_ANCHORS.get(goal, []):
        goal_bonus += 4
    if entry['name'] in STATE_ANCHORS.get(state, []):
        goal_bonus += 3
    # At hypothesis/observed stages, prefer skills whose designed evidence stage is at most
    # one step ahead. At validated/remediation stages, allow regression skills to surface.
    stage = STAGE_WEIGHT.get(entry.get('evidence_stage'), 0)
    current = STAGE_WEIGHT.get(state, 0)
    stage_fit = 2 if stage <= min(current + 1, 3) else 0
    return (overlap * 10 + goal_bonus, stage_fit, MATURITY_WEIGHT.get(entry.get('maturity'), 0), entry['name'])


def _closure(name: str, by_name: dict[str, dict[str, Any]], out: set[str]) -> None:
    if name not in by_name or name in out:
        return
    for dep in by_name[name].get('prerequisites', []):
        _closure(dep, by_name, out)
    out.add(name)


def _topological(selected: set[str], by_name: dict[str, dict[str, Any]], preference: list[str]) -> list[str]:
    order: list[str] = []
    visiting: set[str] = set()
    visited: set[str] = set()

    rank = {name: i for i, name in enumerate(preference)}

    def visit(name: str) -> None:
        if name in visited or name not in selected:
            return
        if name in visiting:
            raise ValueError(f'prerequisite cycle while routing at {name}')
        visiting.add(name)
        deps = [d for d in by_name[name].get('prerequisites', []) if d in selected]
        deps.sort(key=lambda x: (rank.get(x, 10**9), x))
        for dep in deps:
            visit(dep)
        visiting.remove(name)
        visited.add(name)
        order.append(name)

    def route_key(name: str) -> tuple[int, int, str]:
        stage = STAGE_WEIGHT.get(by_name[name].get('evidence_stage'), 0)
        return (stage, rank.get(name, 10**9), name)

    for name in sorted(selected, key=route_key):
        visit(name)
    if 'security-scope-and-authorization' in order:
        order.remove('security-scope-and-authorization')
        order.insert(0, 'security-scope-and-authorization')
    return order


def route_case(root: Path, case: dict[str, Any], *, limit: int = 12) -> dict[str, Any]:
    root = Path(root).resolve()
    case_issues = [x for x in validate_case(case) if x.level == 'error']
    if case_issues:
        raise ValueError('invalid research case: ' + '; '.join(f'{x.path}: {x.message}' for x in case_issues))
    graph_issues = [x for x in validate_graph(root) if x.level == 'error']
    if graph_issues:
        raise ValueError('invalid skill graph: ' + '; '.join(x.message for x in graph_issues[:5]))
    if limit < 1:
        raise ValueError('limit must be at least 1')

    entries = load_graph_entries(root)
    by_name = {x['name']: x for x in entries}
    domains = {str(x).lower() for x in case.get('domains', [])}
    goal = case['goal']
    state = case['state']

    anchors = ['security-scope-and-authorization']
    anchors += GOAL_ANCHORS.get(goal, [])
    anchors += STATE_ANCHORS.get(state, [])
    anchors = list(dict.fromkeys(x for x in anchors if x in by_name))

    scored = []
    for entry in entries:
        score = _score(entry, domains, goal, state)
        if score[0] > 0:
            scored.append((score, entry['name']))
    # Reverse numerical scores, deterministic alphabetical tie break.
    scored.sort(key=lambda item: (-item[0][0], -item[0][1], -item[0][2], item[1]))
    preference = anchors + [name for _, name in scored]

    selected: set[str] = set()
    # Anchors are mandatory even if closure makes the route exceed a tiny caller limit.
    for name in anchors:
        _closure(name, by_name, selected)

    for _, name in scored:
        trial = set(selected)
        _closure(name, by_name, trial)
        if len(trial) <= limit or len(selected) < len(anchors):
            selected = trial
        if len(selected) >= limit:
            break

    ordered = _topological(selected, by_name, preference)
    packs = load_packs(root)
    pack_scores = []
    selected_set = set(ordered)
    for pack in packs:
        pack_domains = {str(x).lower() for x in pack.get('domains', [])}
        goal_pack = pack.get('name') in GOAL_PACKS.get(goal, set())
        if not (pack_domains & domains) and not goal_pack:
            continue
        members = set(pack.get('skills', []))
        overlap = len(selected_set & members)
        entry_hit = 1 if pack.get('entrypoint') in selected_set else 0
        if overlap >= 2 or entry_hit or goal_pack:
            pack_scores.append((overlap, entry_hit, pack['name']))
    pack_scores.sort(key=lambda x: (-x[0], -x[1], x[2]))
    recommended_packs = [name for _, _, name in pack_scores[:5]]

    reasons = {}
    for name in ordered:
        entry = by_name[name]
        overlap = sorted(domains & {str(x).lower() for x in entry.get('domains', [])})
        why = []
        if name == 'security-scope-and-authorization':
            why.append('authorization gate')
        if name in GOAL_ANCHORS.get(goal, []):
            why.append(f'goal:{goal}')
        if name in STATE_ANCHORS.get(state, []):
            why.append(f'state:{state}')
        if overlap:
            why.append('domain:' + ','.join(overlap))
        if not why:
            why.append('prerequisite')
        reasons[name] = why

    return {
        'schema_version': 1,
        'case_id': case['case_id'],
        'state': state,
        'goal': goal,
        'domains': sorted(domains),
        'skills': ordered,
        'packs': recommended_packs,
        'reasons': reasons,
        'advisory_only': True,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description='Recommend an advisory Security Skills route for a validated research case.')
    parser.add_argument('case', type=Path, help='research case JSON file')
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--limit', type=int, default=12)
    args = parser.parse_args()
    try:
        data = json.loads(args.case.read_text(encoding='utf-8'))
        result = route_case(args.root, data, limit=args.limit)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
