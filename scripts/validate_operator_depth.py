#!/usr/bin/env python3
"""Validate CI-enforced operator-depth profiles and safe scenario matrices."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = Path("operator-depth") / "profiles.json"
SCENARIO_FIELDS = (
    "hypothesis",
    "safe_oracle",
    "positive_control",
    "negative_control",
    "stop_condition",
    "remediation_oracle",
)
SAFE_ORACLE_TERMS = (
    "synthetic",
    "mock",
    "inert",
    "read-only",
    "simulated",
    "controlled",
    "test",
    "canary",
)
STOP_TERMS = ("stop", "abort", "do not")
SCENARIO_ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")


def _nonempty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _inside(child: Path, parent: Path) -> bool:
    try:
        child.relative_to(parent)
    except ValueError:
        return False
    return True


def _safe_skill_name(value: str) -> bool:
    return (
        value not in {".", ".."}
        and "/" not in value
        and "\\" not in value
        and not Path(value).is_absolute()
    )


def _profile_path(
    *,
    prefix: str,
    skill_dir: Path,
    value: object,
    field: str,
    errors: list[str],
) -> tuple[str | None, Path | None]:
    if not _nonempty_string(value):
        errors.append(f"{prefix}: {field} must be a non-empty relative path")
        return None, None

    text = value.strip()
    if Path(text).is_absolute():
        errors.append(f"{prefix}: {field.replace('_', ' ')} path escapes skill directory")
        return None, None

    path = (skill_dir / text).resolve()
    if not _inside(path, skill_dir):
        errors.append(f"{prefix}: {field.replace('_', ' ')} path escapes skill directory")
        return None, None
    return text, path


def _validate_scenario_matrix(
    *,
    prefix: str,
    path: Path,
    errors: list[str],
) -> None:
    if not path.is_file():
        errors.append(f"{prefix}: missing scenario matrix '{path.name}'")
        return

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        errors.append(f"{prefix}: cannot read scenario matrix: {exc}")
        return

    if not isinstance(payload, dict):
        errors.append(f"{prefix}: scenario matrix root must be an object")
        return
    if payload.get("version") != 1:
        errors.append(f"{prefix}: scenario matrix version must be 1")

    scenarios = payload.get("scenarios")
    if not isinstance(scenarios, list) or len(scenarios) < 3:
        errors.append(f"{prefix}: scenario matrix must contain at least 3 scenarios")
        return

    seen_ids: set[str] = set()
    for index, item in enumerate(scenarios):
        scenario_prefix = f"{prefix}: scenario[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{scenario_prefix}: scenario must be an object")
            continue

        scenario_id = item.get("id")
        if not _nonempty_string(scenario_id):
            errors.append(f"{scenario_prefix}: id must be a non-empty string")
        else:
            scenario_id = scenario_id.strip()
            if not SCENARIO_ID_RE.fullmatch(scenario_id):
                errors.append(f"{scenario_prefix}: invalid scenario id '{scenario_id}'")
            if scenario_id in seen_ids:
                errors.append(f"{scenario_prefix}: duplicate scenario id '{scenario_id}'")
            seen_ids.add(scenario_id)
            scenario_prefix = f"{prefix}: scenario[{index}] {scenario_id}"

        for field in SCENARIO_FIELDS:
            if not _nonempty_string(item.get(field)):
                errors.append(f"{scenario_prefix}: {field} must be a non-empty string")

        safe_oracle = item.get("safe_oracle")
        if _nonempty_string(safe_oracle):
            lower = safe_oracle.lower()
            if not any(term in lower for term in SAFE_ORACLE_TERMS):
                errors.append(
                    f"{scenario_prefix}: safe_oracle must name a benign synthetic/mock/controlled signal"
                )

        stop_condition = item.get("stop_condition")
        if _nonempty_string(stop_condition):
            lower = stop_condition.lower()
            if not any(term in lower for term in STOP_TERMS):
                errors.append(f"{scenario_prefix}: stop_condition must explicitly stop or abort")


def validate(root: Path) -> list[str]:
    root = root.resolve()
    skills_root = (root / "skills").resolve()
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

    if manifest.get("version") != 2:
        errors.append("operator-depth manifest version must be 2")

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

        if not _safe_skill_name(skill):
            errors.append(f"{prefix}: skill path escapes skills directory")
            continue

        if skill in seen_skills:
            errors.append(f"{prefix}: duplicate skill profile")
        seen_skills.add(skill)

        if profile.get("lab_only") is not True:
            errors.append(f"{prefix}: lab_only must be true")

        sections_value = profile.get("required_runbook_sections")
        sections: list[str] = []
        if not isinstance(sections_value, list) or not sections_value:
            errors.append(f"{prefix}: required_runbook_sections must be a non-empty list")
        else:
            seen_sections: set[str] = set()
            for section_index, section in enumerate(sections_value):
                if not _nonempty_string(section):
                    errors.append(
                        f"{prefix}: required_runbook_sections[{section_index}] must be a non-empty string"
                    )
                    continue
                normalized = section.strip()
                if normalized in seen_sections:
                    errors.append(f"{prefix}: duplicate required section '{normalized}'")
                seen_sections.add(normalized)
                sections.append(normalized)

        skill_dir = (skills_root / skill).resolve()
        if not _inside(skill_dir, skills_root) or skill_dir == skills_root:
            errors.append(f"{prefix}: skill path escapes skills directory")
            continue

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

        runbook_value, runbook_path = _profile_path(
            prefix=prefix,
            skill_dir=skill_dir,
            value=profile.get("runbook"),
            field="runbook",
            errors=errors,
        )
        scenario_value, scenario_path = _profile_path(
            prefix=prefix,
            skill_dir=skill_dir,
            value=profile.get("scenario_matrix"),
            field="scenario_matrix",
            errors=errors,
        )

        if runbook_value is not None and runbook_value not in skill_text:
            errors.append(
                f"{prefix}: canonical SKILL.md does not link declared runbook '{runbook_value}'"
            )

        runbook_text: str | None = None
        if runbook_path is not None:
            if not runbook_path.is_file():
                errors.append(f"{prefix}: missing runbook '{runbook_value}'")
            else:
                try:
                    runbook_text = runbook_path.read_text(encoding="utf-8")
                except (OSError, UnicodeError) as exc:
                    errors.append(f"{prefix}: cannot read runbook '{runbook_value}': {exc}")

        if runbook_text is not None:
            headings = {
                line.strip() for line in runbook_text.splitlines() if line.startswith("## ")
            }
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
            if scenario_value is not None and scenario_value not in runbook_text:
                errors.append(
                    f"{prefix}: runbook does not link declared scenario matrix '{scenario_value}'"
                )

        if scenario_path is not None:
            _validate_scenario_matrix(prefix=prefix, path=scenario_path, errors=errors)

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
