from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from research_case import validate_case


def main() -> int:
    parser = argparse.ArgumentParser(description='Validate a Security Skills research-case JSON file.')
    parser.add_argument('case', type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.case.read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 1
    issues = validate_case(data)
    errors = [x for x in issues if x.level == 'error']
    if errors:
        for issue in errors:
            print(f'ERROR: {issue.path}: {issue.message}', file=sys.stderr)
        return 1
    print(f"Case validation passed: {data['case_id']} ({data['state']}).")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
