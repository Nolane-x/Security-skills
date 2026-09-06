# AI agent compatibility

**Verified/documented against public product documentation on 2026-09-06.** Product paths evolve; the canonical `SKILL.md` content is intentionally vendor-neutral.

## Canonical format

The repository follows the Agent Skills open specification: one directory per skill, a required `SKILL.md` with YAML frontmatter, and optional `scripts/`, `references/`, and `assets/`.

## Major native consumers

| Agent / product | Project-level location or import path | Notes |
| --- | --- | --- |
| Gemini CLI | `.agents/skills/<name>/` or `.gemini/skills/<name>/` | Gemini documents `.agents/skills/` as an interoperable alias and can install from a Git repository with a `--path`. |
| Cursor | `.agents/skills/<name>/` or `.cursor/skills/<name>/` | Cursor supports Agent Skills directly and also reads Claude/Codex compatibility directories. |
| GitHub Copilot | `.agents/skills/<name>/`, `.github/skills/<name>/`, or `.claude/skills/<name>/` | Copilot cloud agent, code review, CLI, app, and supported IDE agent modes use Agent Skills. |
| OpenCode | `.agents/skills/<name>/`, `.opencode/skills/<name>/`, or `.claude/skills/<name>/` | Native on-demand skill tool. |
| Kiro | `.kiro/skills/<name>/` | Kiro can also import an individual skill folder or `SKILL.md` from a public GitHub repository. |
| Claude Code-style consumers | `.claude/skills/<name>/` | The open-format skill directory is the portable unit; verify the current host's discovery path. |
| Codex-style consumers | `.agents/skills/<name>/` or host-documented skills directory | Prefer `.agents/skills/` when supported because multiple current agents recognize it. |

## Lowest-common-denominator fallback

For an agent that cannot discover `SKILL.md` natively:

1. keep the canonical skill untouched under `skills/<name>/`;
2. put short standing instructions in that product's equivalent of `AGENTS.md` / rules;
3. tell the agent to read the selected canonical `skills/<name>/SKILL.md` when the task matches its description;
4. avoid copy-pasting full skill bodies into multiple product-specific files.

This preserves one source of truth even when the host lacks native progressive disclosure.

## Installation strategy

For a project that supports `.agents/skills/`, copy selected canonical skill directories:

```text
skills/security-research-router/
    -> .agents/skills/security-research-router/
```

For a host with a dedicated directory, copy the same directory without modifying `SKILL.md`.

A community `skills` CLI can install open-format skills into many agent products. When using any third-party installer, review what it writes before granting script/tool permissions.

## Why canonical frontmatter is conservative

Some products accept extra fields such as path globs, icons, automatic-invocation controls, or tool allowlists. Those fields are intentionally omitted from the foundation because they are not uniformly portable. Product-specific adapters may add them later without modifying canonical content.
