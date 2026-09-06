# Security Skills repository instructions

Treat `skills/` as the canonical source of Agent Skills.

Before proposing or editing a skill:

- read `AGENTS.md`;
- preserve open `SKILL.md` portability;
- do not duplicate canonical skill bodies into Copilot-only files;
- maintain authorization-aware, evidence-first security research behavior;
- distinguish hypothesis, observed, validated, and regression-verified;
- prefer benign proof signals and defensive/authorized research boundaries.

Before completion run:

```bash
python scripts/validate_skills.py
python scripts/build_catalog.py --check
python -m unittest discover -s tests -v
```
