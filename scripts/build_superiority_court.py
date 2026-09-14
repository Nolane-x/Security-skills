from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from prepare_superiority_tasks import ROOT, load_suite_fixtures, stable_json_text
from superiority_court import build_court


def load_score_artifact(path: Path) -> dict:
    data = json.loads(Path(path).read_text(encoding='utf-8'))
    if data.get('schema_version') != 1:
        raise ValueError(f'unsupported score artifact schema: {path}')
    if not isinstance(data.get('contestant_id'), str) or not data['contestant_id'].strip():
        raise ValueError(f'invalid contestant_id: {path}')
    if not isinstance(data.get('results'), list):
        raise ValueError(f'invalid results list: {path}')
    if data.get('result_count') != len(data['results']):
        raise ValueError(f'result_count mismatch: {path}')
    return data


def build_court_artifact(root: Path, suite_path: Path, score_paths: list[Path]) -> dict:
    suite, fixtures = load_suite_fixtures(root, suite_path)
    if len(score_paths) < 2:
        raise ValueError('at least two contestant score artifacts are required')

    expected_ids = sorted(fixture['fixture_id'] for fixture in fixtures)
    seen_contestants: set[str] = set()
    all_results: list[dict] = []

    for path in score_paths:
        artifact = load_score_artifact(path)
        if artifact.get('suite_id') != suite['suite_id']:
            raise ValueError(f'suite mismatch: {path}')
        contestant_id = artifact['contestant_id']
        if contestant_id in seen_contestants:
            raise ValueError(f'duplicate contestant score artifact: {contestant_id}')
        seen_contestants.add(contestant_id)
        if artifact['result_count'] != len(expected_ids):
            raise ValueError(f'incomplete score artifact: {contestant_id}')
        for result in artifact['results']:
            if result.get('contestant_id') != contestant_id:
                raise ValueError(f'contestant identity mismatch inside score artifact: {path}')
        all_results.extend(artifact['results'])

    return build_court(suite['suite_id'], expected_ids, all_results)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description='Build a deterministic framework-neutral superiority court artifact.'
    )
    parser.add_argument('suite')
    parser.add_argument('scores', nargs='+')
    parser.add_argument('--json', required=True)
    args = parser.parse_args(argv)
    try:
        result = build_court_artifact(
            ROOT, Path(args.suite), [Path(path) for path in args.scores]
        )
        Path(args.json).write_text(stable_json_text(result), encoding='utf-8')
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2
    print(
        f"Built superiority court for {len(result['contestants'])} contestant(s); "
        f"absolute winner: {result['absolute_winner'] or 'none'}."
    )
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
