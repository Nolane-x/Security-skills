from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from security_graph import load_graph_entries, load_packs, validate_graph


def build_graph_data(root: Path) -> dict:
    issues = validate_graph(root)
    errors = [x for x in issues if x.level == 'error']
    if errors:
        rendered = '; '.join(f'{x.path}: {x.message}' for x in errors[:5])
        raise ValueError(f'graph validation failed before build: {rendered}')
    skills = load_graph_entries(root)
    packs = load_packs(root)
    return {'schema_version': 1, 'skill_count': len(skills), 'pack_count': len(packs), 'skills': skills, 'packs': packs}


def render_json(data: dict) -> str:
    compact = {
        'schema_version': data['schema_version'],
        'skill_count': data['skill_count'],
        'pack_count': data['pack_count'],
        'skills': [
            {
                'name': skill['name'],
                'maturity': skill['maturity'],
                'domains': skill['domains'],
                'prerequisites': skill['prerequisites'],
                'composes_with': skill['composes_with'],
                'evidence_stage': skill['evidence_stage'],
                'path': skill['path'],
            }
            for skill in data['skills']
        ],
        'packs': [
            {
                'name': pack['name'],
                'entrypoint': pack['entrypoint'],
                'skills': pack['skills'],
                'default_flow': pack['default_flow'],
                'path': pack['path'],
            }
            for pack in data['packs']
        ],
    }
    return json.dumps(compact, ensure_ascii=False, separators=(',', ':')) + '\n'


def render_markdown(data: dict) -> str:
    lines = [
        '# Security Skill Graph',
        '',
        f"Generated from `skills/*/skill.meta.json` and `packs/*.json`. **{data['skill_count']} skills across {data['pack_count']} packs.**",
        '',
        '## Packs',
        '',
        '| Pack | Entrypoint | Skills | Default flow |',
        '| --- | --- | ---: | --- |',
    ]
    for pack in data['packs']:
        flow = ' → '.join(f'`{x}`' for x in pack['default_flow'])
        lines.append(f"| `{pack['name']}` | `{pack['entrypoint']}` | {len(pack['skills'])} | {flow} |")
    lines += ['', '## Skills', '', '| Skill | Maturity | Domains | Evidence stage | Prerequisites |', '| --- | --- | --- | --- | --- |']
    for skill in data['skills']:
        domains = ', '.join(skill['domains'])
        prereqs = ', '.join(f'`{x}`' for x in skill['prerequisites']) or '—'
        lines.append(f"| [`{skill['name']}`]({skill['path']}) | {skill['maturity']} | {domains} | {skill['evidence_stage']} | {prereqs} |")
    lines.append('')
    return '\n'.join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description='Build deterministic Security Skills graph outputs.')
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    root = args.root.resolve()

    try:
        data = build_graph_data(root)
    except Exception as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 1

    outputs = {root / 'graph.json': render_json(data), root / 'GRAPH.md': render_markdown(data)}
    if args.check:
        stale = [path.name for path, expected in outputs.items() if not path.exists() or path.read_text(encoding='utf-8') != expected]
        if stale:
            print('ERROR: graph outputs are stale or missing: ' + ', '.join(stale), file=sys.stderr)
            return 1
        print(f"Graph check passed for {data['skill_count']} skill(s) and {data['pack_count']} pack(s).")
        return 0

    for path, content in outputs.items():
        path.write_text(content, encoding='utf-8')
    print(f"Wrote graph for {data['skill_count']} skill(s) and {data['pack_count']} pack(s).")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
