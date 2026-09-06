from __future__ import annotations

import argparse
from pathlib import Path
import sys

from skilllib import SkillParseError, discover_skills, validate_skill


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate canonical Security Skills.")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repository root (default: parent of scripts/)",
    )
    args = parser.parse_args()
    root = args.root.resolve()

    try:
        skills = discover_skills(root)
    except (SkillParseError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if not skills:
        print(f"ERROR: No skills found under {root / 'skills'}")
        return 1

    issues = []
    for skill in skills:
        issues.extend(validate_skill(skill, root))

    for issue in issues:
        try:
            rel = issue.path.resolve().relative_to(root)
        except ValueError:
            rel = issue.path
        print(f"{issue.level.upper()}: {rel}: {issue.message}")

    errors = [i for i in issues if i.level == "error"]
    if errors:
        print(f"Validation failed: {len(errors)} error(s) across {len(skills)} skill(s).")
        return 1

    print(f"Validated {len(skills)} skill(s): 0 errors.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
