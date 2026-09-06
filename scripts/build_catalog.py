from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from skilllib import SkillParseError, discover_skills


def build_data(root: Path) -> dict:
    skills = discover_skills(root)
    entries = []
    for skill in skills:
        metadata = skill.metadata
        entries.append(
            {
                "name": skill.name,
                "description": skill.description,
                "category": metadata.get("nolane-security-category", ""),
                "authorization": metadata.get("nolane-security-authorization", ""),
                "version": metadata.get("nolane-security-version", ""),
                "path": skill.path.relative_to(root).as_posix(),
            }
        )
    entries.sort(key=lambda item: (item["category"], item["name"]))
    return {"schema_version": 1, "skill_count": len(entries), "skills": entries}


def render_json(data: dict) -> str:
    compact = {
        "schema_version": data["schema_version"],
        "skill_count": data["skill_count"],
        "skills": [
            {
                "name": item["name"],
                "category": item["category"],
                "authorization": item["authorization"],
                "version": item["version"],
                "path": item["path"],
            }
            for item in data["skills"]
        ],
    }
    return json.dumps(compact, ensure_ascii=False, separators=(",", ":")) + "\n"


def render_markdown(data: dict) -> str:
    lines = [
        "# Skill Catalog",
        "",
        f"Generated from canonical `skills/*/SKILL.md` files. **{data['skill_count']} skills.**",
        "",
        "| Skill | Category | Authorization | Description |",
        "| --- | --- | --- | --- |",
    ]
    for item in data["skills"]:
        desc = item["description"].replace("|", r"\|").replace("\n", " ")
        lines.append(
            f"| [`{item['name']}`]({item['path']}) | {item['category']} | "
            f"{item['authorization']} | {desc} |"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build deterministic Security Skills catalog.")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repository root",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail if catalog outputs are missing or stale",
    )
    args = parser.parse_args()
    root = args.root.resolve()

    try:
        data = build_data(root)
    except (SkillParseError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if not data["skills"]:
        print(f"ERROR: No skills found under {root / 'skills'}", file=sys.stderr)
        return 1

    outputs = {
        root / "catalog.json": render_json(data),
        root / "CATALOG.md": render_markdown(data),
    }

    if args.check:
        stale = []
        for path, expected in outputs.items():
            if not path.exists() or path.read_text(encoding="utf-8") != expected:
                stale.append(path.name)
        if stale:
            print("ERROR: catalog is stale or missing: " + ", ".join(stale), file=sys.stderr)
            return 1
        print(f"Catalog check passed for {data['skill_count']} skill(s).")
        return 0

    for path, content in outputs.items():
        path.write_text(content, encoding="utf-8")
    print(f"Wrote catalog for {data['skill_count']} skill(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
