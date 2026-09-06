from __future__ import annotations

import argparse
from pathlib import Path
import sys

from security_graph import validate_graph


def main() -> int:
    parser = argparse.ArgumentParser(description='Validate Security Skills graph metadata and packs.')
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()

    try:
        issues = validate_graph(root)
    except Exception as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 1

    for issue in issues:
        try:
            rel = issue.path.resolve().relative_to(root)
        except ValueError:
            rel = issue.path
        print(f'{issue.level.upper()}: {rel}: {issue.message}')

    errors = [x for x in issues if x.level == 'error']
    if errors:
        print(f'Graph validation failed: {len(errors)} error(s).')
        return 1
    print('Graph validation passed: 0 errors.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
