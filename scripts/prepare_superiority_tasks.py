from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from superiority_court import build_authority_commitment, build_task

ROOT = SCRIPT_DIR.parent
CORPUS_PATH = ROOT / 'superiority' / 'corpus.json'


def stable_json_text(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + '\n'


def load_suite_fixtures(root: Path, suite_path: Path) -> tuple[dict, list[dict]]:
    suite = json.loads(Path(suite_path).read_text(encoding='utf-8'))
    corpus = json.loads((root / 'superiority' / 'corpus.json').read_text(encoding='utf-8'))
    fixtures = {item['fixture_id']: item for item in corpus['fixtures']}
    fixture_ids = suite['fixture_ids']
    if len(fixture_ids) != len(set(fixture_ids)):
        raise ValueError('suite contains duplicate fixture ids')
    unknown = sorted(set(fixture_ids) - set(fixtures))
    if unknown:
        raise ValueError(f"suite references unknown fixture(s): {', '.join(unknown)}")
    return suite, [fixtures[fixture_id] for fixture_id in sorted(fixture_ids)]


def _ensure_empty_destination(out_dir: Path) -> None:
    if out_dir.exists():
        if not out_dir.is_dir():
            raise ValueError(f'task destination is not a directory: {out_dir}')
        if any(out_dir.iterdir()):
            raise ValueError(f'task destination must be empty: {out_dir}')
    else:
        out_dir.mkdir(parents=True)


def prepare_suite_tasks(root: Path, suite_path: Path, out_dir: Path) -> list[dict]:
    suite, fixtures = load_suite_fixtures(root, suite_path)
    out_dir = Path(out_dir)
    _ensure_empty_destination(out_dir)
    tasks = [build_task(fixture) for fixture in fixtures]
    tasks.sort(key=lambda item: item['fixture_id'])
    for task in tasks:
        (out_dir / f"{task['fixture_id']}.json").write_text(
            stable_json_text(task), encoding='utf-8'
        )

    manifest = {
        'schema_version': 1,
        'kind': 'superiority-public-suite-manifest',
        'suite_id': suite['suite_id'],
        'task_count': len(tasks),
        'tasks': [
            {'fixture_id': task['fixture_id'], 'task_digest': task['task_digest']}
            for task in tasks
        ],
        'authority_commitment': build_authority_commitment(suite['suite_id'], fixtures),
    }
    (out_dir / 'SUITE_MANIFEST.json').write_text(
        stable_json_text(manifest), encoding='utf-8'
    )
    return tasks


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description='Prepare oracle-free framework-neutral superiority court tasks.'
    )
    parser.add_argument('suite')
    parser.add_argument('--out', required=True)
    args = parser.parse_args(argv)
    try:
        tasks = prepare_suite_tasks(ROOT, Path(args.suite), Path(args.out))
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2
    print(f'Prepared {len(tasks)} superiority task(s).')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
