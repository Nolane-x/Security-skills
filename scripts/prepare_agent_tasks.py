from __future__ import annotations

import argparse
import sys
from pathlib import Path

from agent_task import build_agent_task, load_suite_fixtures, stable_json_text


ROOT = Path(__file__).resolve().parents[1]


def prepare_suite_tasks(root: Path, suite_path: Path, out_dir: Path) -> list[dict]:
    _, fixtures = load_suite_fixtures(root, suite_path)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    tasks = [build_agent_task(fixture) for fixture in fixtures]
    tasks.sort(key=lambda x: x['benchmark_id'])
    for task in tasks:
        (out_dir / f"{task['benchmark_id']}.json").write_text(stable_json_text(task), encoding='utf-8')
    return tasks


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description='Prepare oracle-free agent evaluation tasks.')
    parser.add_argument('suite')
    parser.add_argument('--out', required=True)
    args = parser.parse_args(argv)
    try:
        tasks = prepare_suite_tasks(ROOT, Path(args.suite), Path(args.out))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2
    print(f'Prepared {len(tasks)} agent task(s).')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
