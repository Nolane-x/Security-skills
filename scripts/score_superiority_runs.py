from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from prepare_superiority_tasks import ROOT, load_suite_fixtures, stable_json_text
from superiority_court import build_task, score_run


def load_runs(runs_dir: Path) -> list[dict]:
    runs_dir = Path(runs_dir)
    if not runs_dir.is_dir():
        raise ValueError(f'runs directory does not exist: {runs_dir}')
    paths = sorted(runs_dir.glob('*.json'))
    if not paths:
        raise ValueError('runs directory contains no JSON files')
    return [json.loads(path.read_text(encoding='utf-8')) for path in paths]


def score_suite_runs(root: Path, suite_path: Path, runs_dir: Path) -> dict:
    suite, fixtures = load_suite_fixtures(root, suite_path)
    fixture_map = {fixture['fixture_id']: fixture for fixture in fixtures}
    expected_ids = sorted(fixture_map)
    runs = load_runs(runs_dir)

    contestant_ids = {run.get('contestant_id') for run in runs}
    if None in contestant_ids or '' in contestant_ids or len(contestant_ids) != 1:
        raise ValueError('runs directory must contain exactly one non-empty contestant_id')
    contestant_id = next(iter(contestant_ids))

    by_fixture: dict[str, dict] = {}
    for run in runs:
        fixture_id = run.get('fixture_id')
        if fixture_id not in fixture_map:
            raise ValueError(f'unknown fixture id: {fixture_id}')
        if fixture_id in by_fixture:
            raise ValueError(f'duplicate run for fixture: {fixture_id}')
        by_fixture[fixture_id] = run

    missing = sorted(set(expected_ids) - set(by_fixture))
    if missing:
        raise ValueError(f"missing fixture run(s): {', '.join(missing)}")
    extras = sorted(set(by_fixture) - set(expected_ids))
    if extras:
        raise ValueError(f"unexpected fixture run(s): {', '.join(extras)}")

    results = []
    for fixture_id in expected_ids:
        fixture = fixture_map[fixture_id]
        task = build_task(fixture)
        results.append(score_run(fixture, task, by_fixture[fixture_id]))

    return {
        'schema_version': 1,
        'suite_id': suite['suite_id'],
        'contestant_id': contestant_id,
        'result_count': len(results),
        'results': results,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description='Score one opaque contestant against a superiority court suite.'
    )
    parser.add_argument('suite')
    parser.add_argument('runs')
    parser.add_argument('--json', required=True)
    args = parser.parse_args(argv)
    try:
        result = score_suite_runs(ROOT, Path(args.suite), Path(args.runs))
        Path(args.json).write_text(stable_json_text(result), encoding='utf-8')
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2
    print(
        f"Scored {result['result_count']} run(s) for contestant {result['contestant_id']}."
    )
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
