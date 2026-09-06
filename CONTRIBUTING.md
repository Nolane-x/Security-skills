# Contributing

## What belongs here

A good skill captures a reusable security-research decision process: when to use a technique, what assumptions must hold, how to collect evidence, how to recognize false positives, when to stop, and what output to produce.

A weak contribution is a thin wrapper around a single shell command with no reasoning or evidence model.

## Required skill structure

Each `skills/<name>/SKILL.md` must use valid Agent Skills frontmatter and contain these headings:

- `## When to use`
- `## Preconditions`
- `## Workflow`
- `## Evidence contract`
- `## Stop conditions`
- `## Output`

Use lowercase kebab-case names. Keep the main file focused; put deep technical notes in `references/`.

Recommended metadata:

```yaml
metadata:
  nolane-security-category: discovery
  nolane-security-version: "1"
  nolane-security-authorization: required
```

`nolane-security-authorization` must be `required`, `conditional`, or `not-applicable`.

## Evidence language

Use these statuses consistently:

- **hypothesis** — plausible from code/design reasoning but not reproduced;
- **observed** — behavior reproduced, but root cause or security impact is not yet established;
- **validated** — the claimed vulnerability behavior and root cause have evidence under stated conditions;
- **regression-verified** — the same evidence fails on the fixed build while controls still behave correctly.

## Validation

Run:

```bash
python scripts/validate_skills.py
python scripts/build_catalog.py
python scripts/build_catalog.py --check
python -m unittest discover -s tests -v
```

CI repeats the checks on Linux, macOS, and Windows.
