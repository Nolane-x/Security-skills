from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from prepare_superiority_tasks import ROOT, load_suite_fixtures, stable_json_text
from superiority_court import build_task

DEGRADED_OVERRIDES = {
    'scope-authorized-sandbox': ('evidence_level', 'observed'),
    'evidence-single-signal': ('next_step', 'check'),
    'checks-contradictory-control': ('next_step', 'check'),
    'resolution-fix-unverified': ('claim_level', 'provisional'),
}
SHA256_RE = re.compile(r'^[0-9a-f]{64}$')


def prepare_replays(
    root: Path,
    suite_path: Path,
    *,
    profile: str,
    contestant_id: str,
    surface_digest: str,
    out_dir: Path,
) -> list[dict]:
    if profile not in {'reference', 'degraded'}:
        raise ValueError(f'unknown replay profile: {profile}')
    if not contestant_id.strip():
        raise ValueError('contestant_id must be non-empty')
    if not isinstance(surface_digest, str) or not SHA256_RE.fullmatch(surface_digest):
        raise ValueError('surface_digest must be a lowercase SHA-256 digest')

    _, fixtures = load_suite_fixtures(root, suite_path)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    runs: list[dict] = []
    for fixture in fixtures:
        task = build_task(fixture)
        answers = copy.deepcopy(fixture['private_expected'])
        if profile == 'degraded' and fixture['fixture_id'] in DEGRADED_OVERRIDES:
            field, value = DEGRADED_OVERRIDES[fixture['fixture_id']]
            if field in fixture.get('rules', []):
                raise ValueError(f'degraded override touches hard rule: {fixture["fixture_id"]}:{field}')
            answers[field] = value
        run = {
            'schema_version': 1,
            'fixture_id': fixture['fixture_id'],
            'contestant_id': contestant_id,
            'contestant_surface_digest': surface_digest,
            'task_digest': task['task_digest'],
            'answers': answers,
        }
        runs.append(run)
        (out_dir / f"{fixture['fixture_id']}.json").write_text(
            stable_json_text(run), encoding='utf-8'
        )
    return runs


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description='Prepare deterministic synthetic replay runs for court self-tests.'
    )
    parser.add_argument('suite')
    parser.add_argument('--profile', choices=('reference', 'degraded'), required=True)
    parser.add_argument('--contestant-id', required=True)
    parser.add_argument('--surface-digest', required=True)
    parser.add_argument('--out', required=True)
    args = parser.parse_args(argv)
    try:
        runs = prepare_replays(
            ROOT,
            Path(args.suite),
            profile=args.profile,
            contestant_id=args.contestant_id,
            surface_digest=args.surface_digest,
            out_dir=Path(args.out),
        )
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2
    print(f'Prepared {len(runs)} {args.profile} superiority replay run(s).')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
