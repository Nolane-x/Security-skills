# Instructions for AI agents working on Security Skills

This repository is a portable security-research skill library. Treat `skills/` as the canonical source of reusable capability.

## Before changing a skill

1. Read the target `SKILL.md` and any directly referenced files.
2. Preserve compatibility with the open Agent Skills format.
3. Keep `name` equal to the containing directory name.
4. Do not add vendor-only frontmatter to canonical skills unless it is safely ignorable by other consumers.
5. Prefer focused references over making `SKILL.md` large.

## Security research quality bar

- Distinguish hypothesis from confirmed behavior.
- Require an explicit scope/authorization check before intrusive testing.
- Prefer local, owned, sandboxed, CTF, benchmark, or explicitly authorized targets.
- Prefer benign proof signals: assertions, sanitizer output, controlled crashes, marker files, test fixtures, and regression tests.
- Do not turn a methodology skill into credential theft, persistence, destructive action, evasion, malware deployment, or indiscriminate exploitation guidance.
- Record uncertainty and environment dependence instead of overstating exploitability.
- A finding is not confirmed solely because an LLM or static tool says it exists.

## Completion gate

Run all of:

```bash
python scripts/validate_skills.py
python scripts/build_catalog.py --check
python -m unittest discover -s tests -v
```

If the catalog changed, regenerate it with `python scripts/build_catalog.py` before the check.
