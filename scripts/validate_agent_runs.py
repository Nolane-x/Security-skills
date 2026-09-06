from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from agent_run import validate_agent_run


ROOT = Path(__file__).resolve().parents[1]


def _paths(target: Path) -> list[Path]:
    if target.is_file():
        return [target]
    if target.is_dir():
        return sorted(target.rglob('*.json'))
    raise FileNotFoundError(target)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description='Validate normalized agent-run artifacts.')
    parser.add_argument('target')
    args = parser.parse_args(argv)
    try:
        paths = _paths(Path(args.target))
        if not paths:
            raise ValueError('no JSON run artifacts found')
        failures = 0
        for path in paths:
            data = json.loads(path.read_text(encoding='utf-8'))
            if not isinstance(data, dict):
                raise ValueError(f'{path}: run must be a JSON object')
            errors = validate_agent_run(ROOT, data)
            if errors:
                failures += 1
                for error in errors:
                    print(f'{path}: {error}', file=sys.stderr)
        if failures:
            return 2
    except (OSError, json.JSONDecodeError, ValueError, TypeError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2
    print(f'Validated {len(paths)} agent run(s).')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
