from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import ast
import re
from typing import Dict, List


NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REQUIRED_SECTIONS = (
    "When to use",
    "Preconditions",
    "Workflow",
    "Evidence contract",
    "Stop conditions",
    "Output",
)
AUTH_VALUES = {"required", "conditional", "not-applicable"}
CATEGORY_VALUES = {
    "foundation",
    "orchestration",
    "discovery",
    "verification",
    "remediation",
    "domain",
}
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


@dataclass(frozen=True)
class Skill:
    path: Path
    frontmatter: Dict[str, object]
    body: str

    @property
    def name(self) -> str:
        return str(self.frontmatter.get("name", ""))

    @property
    def description(self) -> str:
        return str(self.frontmatter.get("description", ""))

    @property
    def metadata(self) -> Dict[str, str]:
        raw = self.frontmatter.get("metadata", {})
        return dict(raw) if isinstance(raw, dict) else {}


@dataclass(frozen=True)
class Issue:
    level: str
    path: Path
    message: str


class SkillParseError(ValueError):
    pass


def _parse_scalar(raw: str) -> str:
    value = raw.strip()
    if not value:
        return ""
    if value[0:1] in {"'", '"'}:
        try:
            parsed = ast.literal_eval(value)
        except (ValueError, SyntaxError) as exc:
            raise SkillParseError(f"invalid quoted scalar: {value}") from exc
        if not isinstance(parsed, str):
            raise SkillParseError("frontmatter scalar must be a string")
        return parsed
    return value


def parse_frontmatter(text: str) -> tuple[Dict[str, object], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise SkillParseError("SKILL.md must start with YAML frontmatter delimiter '---'")

    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration as exc:
        raise SkillParseError("SKILL.md frontmatter is missing closing '---'") from exc

    fm_lines = lines[1:end]
    data: Dict[str, object] = {}
    active_map: Dict[str, str] | None = None

    for line_no, line in enumerate(fm_lines, start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue

        if line.startswith((" ", "\t")):
            if active_map is None:
                raise SkillParseError(
                    f"unsupported indentation in frontmatter at line {line_no}"
                )
            stripped = line.strip()
            if ":" not in stripped:
                raise SkillParseError(f"invalid metadata entry at line {line_no}")
            key, raw_value = stripped.split(":", 1)
            key = key.strip()
            if not key:
                raise SkillParseError(f"empty metadata key at line {line_no}")
            active_map[key] = _parse_scalar(raw_value)
            continue

        active_map = None
        if ":" not in line:
            raise SkillParseError(f"invalid frontmatter entry at line {line_no}")
        key, raw_value = line.split(":", 1)
        key = key.strip()
        if not key:
            raise SkillParseError(f"empty frontmatter key at line {line_no}")

        if raw_value.strip() == "":
            if key != "metadata":
                raise SkillParseError(
                    f"only metadata mappings are supported by the dependency-free parser (line {line_no})"
                )
            mapping: Dict[str, str] = {}
            data[key] = mapping
            active_map = mapping
        else:
            data[key] = _parse_scalar(raw_value)

    body = "\n".join(lines[end + 1 :]).lstrip("\n")
    return data, body


def parse_skill(path: Path) -> Skill:
    text = path.read_text(encoding="utf-8")
    frontmatter, body = parse_frontmatter(text)
    return Skill(path=path, frontmatter=frontmatter, body=body)


def discover_skills(root: Path) -> List[Skill]:
    skill_root = root / "skills"
    if not skill_root.exists():
        return []
    skills: List[Skill] = []
    for path in sorted(skill_root.rglob("SKILL.md")):
        skills.append(parse_skill(path))
    return skills


def _section_present(body: str, section: str) -> bool:
    return re.search(
        rf"^##\s+{re.escape(section)}\s*$",
        body,
        flags=re.IGNORECASE | re.MULTILINE,
    ) is not None


def _validate_links(skill: Skill) -> List[Issue]:
    issues: List[Issue] = []
    base = skill.path.parent.resolve()
    for target in LINK_RE.findall(skill.body):
        clean = target.split("#", 1)[0].strip()
        if (
            not clean
            or clean.startswith(("#", "http://", "https://", "mailto:"))
            or "://" in clean
        ):
            continue
        candidate = (base / clean).resolve()
        try:
            candidate.relative_to(base)
        except ValueError:
            issues.append(
                Issue("error", skill.path, f"relative link escapes the skill directory: {target}")
            )
            continue
        if not candidate.exists():
            issues.append(
                Issue("error", skill.path, f"relative link target does not exist: {target}")
            )
    return issues


def validate_skill(skill: Skill, root: Path) -> List[Issue]:
    issues: List[Issue] = []
    fm = skill.frontmatter

    if not skill.name:
        issues.append(Issue("error", skill.path, "missing required frontmatter field: name"))
    elif len(skill.name) > 64 or not NAME_RE.fullmatch(skill.name):
        issues.append(
            Issue(
                "error",
                skill.path,
                "name must be 1-64 lowercase alphanumeric characters with single hyphen separators",
            )
        )

    if skill.path.parent.name != skill.name:
        issues.append(
            Issue(
                "error",
                skill.path,
                f"skill directory '{skill.path.parent.name}' must match frontmatter name '{skill.name}'",
            )
        )

    if not skill.description:
        issues.append(
            Issue("error", skill.path, "missing required frontmatter field: description")
        )
    elif len(skill.description) > 1024:
        issues.append(
            Issue("error", skill.path, "description exceeds the 1024 character Agent Skills limit")
        )

    if "allowed-tools" in fm:
        issues.append(
            Issue(
                "error",
                skill.path,
                "allowed-tools is intentionally disallowed in canonical foundation skills because support is experimental and non-uniform",
            )
        )

    metadata = skill.metadata
    category = metadata.get("nolane-security-category")
    version = metadata.get("nolane-security-version")
    authorization = metadata.get("nolane-security-authorization")

    if category not in CATEGORY_VALUES:
        issues.append(
            Issue(
                "error",
                skill.path,
                f"metadata nolane-security-category must be one of {sorted(CATEGORY_VALUES)}",
            )
        )
    if version != "1":
        issues.append(
            Issue(
                "error",
                skill.path,
                "metadata nolane-security-version must be string value \"1\" for the foundation contract",
            )
        )
    if authorization not in AUTH_VALUES:
        issues.append(
            Issue(
                "error",
                skill.path,
                f"metadata nolane-security-authorization must be one of {sorted(AUTH_VALUES)}",
            )
        )

    for section in REQUIRED_SECTIONS:
        if not _section_present(skill.body, section):
            issues.append(
                Issue("error", skill.path, f"missing required section: ## {section}")
            )

    body_lines = skill.body.splitlines()
    if len(body_lines) > 500:
        issues.append(
            Issue(
                "error",
                skill.path,
                f"SKILL.md body has {len(body_lines)} lines; keep it at or below 500 and move detail into references/",
            )
        )

    if re.search(r"\b(TBD|TODO|FIXME)\b", skill.body):
        issues.append(
            Issue("error", skill.path, "skill body contains a placeholder token (TBD/TODO/FIXME)")
        )

    if authorization in {"required", "conditional"}:
        lower = skill.body.lower()
        if not any(word in lower for word in ("authorized", "owned", "sandbox", "local lab", "ctf")):
            issues.append(
                Issue(
                    "error",
                    skill.path,
                    "authorization-sensitive skill must explicitly constrain intrusive work to authorized/owned/lab scope",
                )
            )

    issues.extend(_validate_links(skill))
    return issues
