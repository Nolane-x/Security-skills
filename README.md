# Security Skills

A portable, verification-first security research skill library for AI agents.

The repository is built around the open **Agent Skills** format: each capability is a self-contained directory under `skills/` with a `SKILL.md` file and optional references, scripts, or assets. The goal is to teach an agent *how to reason through security research and verify claims*, not merely how to invoke a tool.

## What makes this different

- **Portable:** canonical skills use the open `SKILL.md` format instead of a vendor-specific prompt format.
- **Composable:** a router selects focused skills instead of injecting a giant security prompt into every session.
- **Evidence-first:** hypotheses, reproductions, root-cause evidence, impact evidence, and regression evidence are separate states.
- **Authorization-aware:** intrusive workflows are scoped to local, owned, sandboxed, or explicitly authorized targets.
- **Benign-by-default proofs:** marker files, assertions, sanitizer reports, controlled crashes, and regression tests are preferred over destructive or persistent payloads.
- **Tool-independent:** workflows teach decisions and evidence contracts first; tool families are optional implementations.
- **Validated:** dependency-free Python checks enforce the repository's skill contract and deterministic catalog.

## Foundation skill graph

The first release deliberately starts with a compact set of high-leverage skills:

- `security-research-router`
- `security-scope-and-authorization`
- `attack-surface-mapping`
- `vulnerability-hypothesis-generation`
- `fuzzing-workflow`
- `crash-triage-and-minimization`
- `static-dataflow-analysis`
- `symbolic-execution-workflow`
- `binary-reconnaissance`
- `evidence-driven-vulnerability-validation`
- `patch-diff-variant-analysis`
- `remediation-and-regression`
- `secure-code-review`
- `ai-agent-security-assessment`

See [CATALOG.md](CATALOG.md) for descriptions and categories.

## Install / use

The canonical source is `skills/`. Current agents increasingly support this format directly.

A broadly interoperable project layout is:

```text
<your-project>/
└── .agents/
    └── skills/
        └── <skill-name>/
            └── SKILL.md
```

Copy or install the desired skill directories into your agent's supported skills location. See [docs/compatibility.md](docs/compatibility.md) for current native paths and fallbacks for Gemini CLI, Cursor, GitHub Copilot, OpenCode, Kiro, Claude Code/Codex-style consumers, and generic agents.

## Validate

No third-party Python package is required:

```bash
python scripts/validate_skills.py
python scripts/build_catalog.py --check
python -m unittest discover -s tests -v
```

Generate the catalog after adding or changing a skill:

```bash
python scripts/build_catalog.py
```

## Adding skills

Read [CONTRIBUTING.md](CONTRIBUTING.md). New skills should encode a reusable research decision process, not a thin command wrapper. They must state when they apply, their preconditions, evidence contract, stop conditions, and output.

## Research lineage

The project is inspired by reproducible vulnerability-research archives and autonomous cyber-reasoning systems, but the skills are original distilled workflows rather than copied prompts or exploit code. See [docs/sources.md](docs/sources.md).

## Security boundary

This repository supports defensive security, secure development, education, and good-faith research. It is not a payload pack. See [SECURITY.md](SECURITY.md).
