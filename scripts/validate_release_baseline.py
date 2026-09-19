#!/usr/bin/env python3
"""Validate the frozen public release baseline against repository reality."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BASELINE = Path("release-baseline.json")
COUNT_FIELDS = (
    "canonical_skills",
    "packs",
    "operator_depth_profiles",
    "benchmark_core_fixtures",
    "benchmark_portability_fixtures",
)


def _read_json(path: Path, label: str, errors: list[str]) -> object | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"missing {label}: {path}")
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        errors.append(f"cannot read {label}: {exc}")
    return None


def _nonempty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _validate_string_list(
    value: object, *, label: str, errors: list[str], allow_empty: bool = False
) -> list[str]:
    if not isinstance(value, list) or (not value and not allow_empty):
        errors.append(f"{label} must be a {'possibly empty ' if allow_empty else 'non-empty '}list")
        return []
    result: list[str] = []
    seen: set[str] = set()
    for index, item in enumerate(value):
        if not _nonempty_string(item):
            errors.append(f"{label}[{index}] must be a non-empty string")
            continue
        text = item.strip()
        if text in seen:
            errors.append(f"{label} contains duplicate entry '{text}'")
        seen.add(text)
        result.append(text)
    return result


def validate(root: Path, baseline_path: Path | None = None) -> list[str]:
    root = root.resolve()
    path = baseline_path or DEFAULT_BASELINE
    if not path.is_absolute():
        path = root / path

    errors: list[str] = []
    baseline = _read_json(path, "release baseline", errors)
    if not isinstance(baseline, dict):
        if baseline is not None:
            errors.append("release baseline root must be an object")
        return sorted(set(errors))

    if baseline.get("schema_version") != 1:
        errors.append("release baseline schema_version must be 1")
    if not _nonempty_string(baseline.get("release")):
        errors.append("release baseline release must be a non-empty string")
    if baseline.get("status") != "closed":
        errors.append("release baseline status must be 'closed'")
    if baseline.get("license") != "Apache-2.0":
        errors.append("release baseline license must be Apache-2.0")

    counts = baseline.get("counts")
    if not isinstance(counts, dict):
        errors.append("release baseline counts must be an object")
        counts = {}

    for field in COUNT_FIELDS:
        value = counts.get(field)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            errors.append(f"release baseline counts.{field} must be a non-negative integer")

    registry_version = baseline.get("operator_depth_registry_version")
    if not isinstance(registry_version, int) or isinstance(registry_version, bool):
        errors.append("operator_depth_registry_version must be an integer")

    published_documents = _validate_string_list(
        baseline.get("published_release_documents"),
        label="published_release_documents",
        errors=errors,
    )
    required_tokens = _validate_string_list(
        baseline.get("required_readme_tokens"),
        label="required_readme_tokens",
        errors=errors,
    )
    required_paths = _validate_string_list(
        baseline.get("required_paths"), label="required_paths", errors=errors
    )

    for relative in required_paths:
        target = root / relative
        if not target.exists():
            errors.append(f"required path is missing: {relative}")

    skills = sorted((root / "skills").glob("*/SKILL.md"))
    packs = sorted((root / "packs").glob("*.json"))

    expected_skills = counts.get("canonical_skills")
    if isinstance(expected_skills, int) and len(skills) != expected_skills:
        errors.append(
            f"canonical skill count drifted: expected {expected_skills}, found {len(skills)}"
        )

    expected_packs = counts.get("packs")
    if isinstance(expected_packs, int) and len(packs) != expected_packs:
        errors.append(f"pack count drifted: expected {expected_packs}, found {len(packs)}")

    registry = _read_json(
        root / "operator-depth" / "profiles.json", "operator-depth registry", errors
    )
    if isinstance(registry, dict):
        if registry.get("version") != registry_version:
            errors.append(
                "operator-depth registry version drifted: "
                f"expected {registry_version}, found {registry.get('version')}"
            )
        profiles = registry.get("profiles")
        if not isinstance(profiles, list):
            errors.append("operator-depth registry profiles must be a list")
        else:
            expected_profiles = counts.get("operator_depth_profiles")
            if isinstance(expected_profiles, int) and len(profiles) != expected_profiles:
                errors.append(
                    "operator-depth profile count drifted: "
                    f"expected {expected_profiles}, found {len(profiles)}"
                )
            names = [
                item.get("skill")
                for item in profiles
                if isinstance(item, dict) and _nonempty_string(item.get("skill"))
            ]
            if len(names) != len(profiles):
                errors.append("every operator-depth profile must name a skill")
            if len(names) != len(set(names)):
                errors.append("operator-depth profile skills must be unique")
            skill_names = {item.parent.name for item in skills}
            unknown = sorted(set(names) - skill_names)
            if unknown:
                errors.append(
                    "operator-depth profile references unknown canonical skill(s): "
                    + ", ".join(unknown)
                )
            for index, item in enumerate(profiles):
                if isinstance(item, dict) and item.get("lab_only") is not True:
                    errors.append(f"operator-depth profile[{index}] lab_only must remain true")

    suites = (
        ("core", "benchmark_core_fixtures"),
        ("portability", "benchmark_portability_fixtures"),
    )
    for suite_name, count_field in suites:
        suite = _read_json(
            root / "benchmarks" / "suites" / f"{suite_name}.json",
            f"{suite_name} benchmark suite",
            errors,
        )
        if not isinstance(suite, dict):
            continue
        fixtures = suite.get("fixtures")
        if not isinstance(fixtures, list):
            errors.append(f"{suite_name} benchmark fixtures must be a list")
            continue
        if len(fixtures) != len(set(fixtures)):
            errors.append(f"{suite_name} benchmark fixtures must be unique")
        expected = counts.get(count_field)
        if isinstance(expected, int) and len(fixtures) != expected:
            errors.append(
                f"{suite_name} benchmark fixture count drifted: "
                f"expected {expected}, found {len(fixtures)}"
            )
        for fixture in fixtures:
            if not _nonempty_string(fixture):
                errors.append(f"{suite_name} benchmark fixture path must be a non-empty string")
                continue
            if not (root / "benchmarks" / fixture).is_file():
                errors.append(f"{suite_name} benchmark fixture is missing: {fixture}")

    for document in published_documents:
        document_path = root / document
        try:
            text = document_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            errors.append(f"published release document is missing: {document}")
            continue
        except (OSError, UnicodeError) as exc:
            errors.append(f"cannot read published release document {document}: {exc}")
            continue
        for token in required_tokens:
            if token not in text:
                errors.append(
                    f"{document} is missing release-baseline token '{token}'"
                )

    license_path = root / "LICENSE"
    try:
        license_text = license_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        errors.append("root LICENSE is missing")
    except (OSError, UnicodeError) as exc:
        errors.append(f"cannot read root LICENSE: {exc}")
    else:
        required_license_markers = (
            "Apache License",
            "Version 2.0, January 2004",
            "TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION",
            "END OF TERMS AND CONDITIONS",
        )
        for marker in required_license_markers:
            if marker not in license_text:
                errors.append(f"root LICENSE is missing Apache-2.0 marker '{marker}'")

    return sorted(set(errors))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the frozen release baseline")
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--baseline", type=Path, default=DEFAULT_BASELINE)
    args = parser.parse_args(argv)

    errors = validate(args.root, args.baseline)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    baseline_path = args.baseline
    if not baseline_path.is_absolute():
        baseline_path = args.root.resolve() / baseline_path
    baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
    counts = baseline["counts"]
    print(
        "Release baseline validation passed: "
        f"{counts['canonical_skills']} skills, "
        f"{counts['packs']} packs, "
        f"{counts['operator_depth_profiles']} operator-depth profiles, "
        f"{counts['benchmark_core_fixtures']} core fixtures, "
        f"{counts['benchmark_portability_fixtures']} portability fixtures."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
