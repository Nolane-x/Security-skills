#!/usr/bin/env python3
"""Validate CI-enforced operator-depth profiles.

The operator-depth layer extends selected canonical skills with deeper, lab-bounded
research runbooks. This validator intentionally checks structural and evidence
contracts rather than prose length or payload counts.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = Path("operator-depth") / "profiles.json"


def _nonempty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _inside(child: Path, parent: Path) -> bool:
    try:
        child.relative_to(parent)
    except ValueError:
        return False
    return True


def validate(root: Path) -> list[str]:
    root = root.resolve()
    manifest_path = root / MANIFEST_PATH
    errors: list[str] = []

    if not manifest_path.is_file():
        return [f"missing operator-depth manifest: {MANIFEST_PATH.as_posix()}"]

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return [f"cannot read operator-depth manifest: {exc}"]

    if not isinstance(manifest, dict):
        return ["operator-depth manifest root must be an object"]

    if manifest.get("version") != 1:
        errors.append("operator-depth manifest version must be 1")

    profiles = manifest.get("profiles")
    if not isinstance(profiles, list) or not profiles:
        errors.append("operator-depth manifest profiles must be a non-empty list")
        return sorted(set(errors))

    seen_skills: set[str] = set()

    for index, profile in enumerate(profiles):
        prefix = f"profile[{index}]"
        if not isinstance(profile, dict):
            errors.append(f"{prefix}: profile must be an object")
            continue

        skill_value = profile.get("skill")
        if not _nonempty_string(skill_value):
            errors.append(f"{prefix}: skill must be a non-empty string")
            continue
        skill = skill_value.strip()
        prefix = f"profile[{index}] {skill}"

        if skill in seen_skills:
            errors.append(f"{prefix}: duplicate skill profile")
        seen_skills.add(skill)

        if profile.get("lab_only") is not True:
            errors.append(f"{prefix}: lab_only must be true")

        runbook_value = profile.get("runbook")
        if not _nonempty_string(runbook_value):
            errors.append(f"{prefix}: runbook must be a non-empty relative path")
            runbook_value = None
        else:
            runbook_value = runbook_value.strip()
            if Path(runbook_value).is_absolute():
                errors.append(f"{prefix}: runbook path escapes skill directory")
                runbook_value = None

        sections_value = profile.get("required_runbook_sections")
        sections: list[str] = []
        if not isinstance(sections_value, list) or not sections_value:
            errors.append(f"{prefix}: required_runbook_sections must be a non-empty list")
        else:
            seen_sections: set[str] = set()
            for section_index, section in enumerate(sections_value):
                if not _nonempty_string(section):
                    errors.append(
                        f"{prefix}: required_runbook_sections[{section_index}] "
                        "must be a non-empty string"
                    )
                    continue
                normalized = section.strip()
                if normalized in seen_sections:
                    errors.append(f"{prefix}: duplicate required section '{normalized}'")
                seen_sections.add(normalized)
                sections.append(normalized)

        skill_dir = (root / "skills" / skill).resolve()
        skill_file = skill_dir / "SKILL.md"
        if not skill_dir.is_dir():
            errors.append(f"{prefix}: missing canonical skill directory")
            continue
        if not skill_file.is_file():
            errors.append(f"{prefix}: missing canonical SKILL.md")
            continue

        try:
            skill_text = skill_file.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"{prefix}: cannot read canonical SKILL.md: {exc}")
            continue

        if runbook_value is None:
            continue

        runbook_path = (skill_dir / runbook_value).resolve()
        if not _inside(runbook_path, skill_dir):
            errors.append(f"{prefix}: runbook path escapes skill directory")
            continue

        if runbook_value not in skill_text:
            errors.append(
                f"{prefix}: canonical SKILL.md does not link declared runbook "
                f"'{runbook_value}'"
            )

        if not runbook_path.is_file():
            errors.append(f"{prefix}: missing runbook '{runbook_value}'")
            continue

        try:
            runbook_text = runbook_path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"{prefix}: cannot read runbook '{runbook_value}': {exc}")
            continue

        headings = {line.strip() for line in runbook_text.splitlines() if line.startswith("## ")}
        for section in sections:
            heading = f"## {section}"
            if heading not in headings:
                errors.append(f"{prefix}: missing required section '{section}'")

        lower = runbook_text.lower()
        if not any(term in lower for term in ("authorized", "owned", "sandbox", "lab")):
            errors.append(f"{prefix}: runbook lacks an authorization/lab boundary")
        if "evidence" not in lower:
            errors.append(f"{prefix}: runbook lacks evidence discipline")
        if "control" not in lower:
            errors.append(f"{prefix}: runbook lacks control/false-positive discipline")

    return sorted(set(errors))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate operator-depth profiles")
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    args = parser.parse_args(argv)

    errors = validate(args.root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    manifest = json.loads((args.root.resolve() / MANIFEST_PATH).read_text(encoding="utf-8"))
    print(f"Operator depth validation passed: {len(manifest['profiles'])} profile(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
