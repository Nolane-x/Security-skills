# Instructions for AI agents working on Security Skills

This repository is a portable, verification-first security-research skill graph. Treat `skills/` as canonical capability content, `skill.meta.json` as graph metadata, and `packs/` as routing manifests.

## Before changing a skill

1. Read the target `SKILL.md`, its `skill.meta.json`, and any local referenced files.
2. Preserve compatibility with the open Agent Skills format.
3. Keep `name` equal to the containing directory name.
4. Do not put vendor-only routing/tool metadata in canonical frontmatter.
5. Keep the skill self-contained; local Markdown links may not escape its directory.
6. Update graph relationships only when the dependency is semantically required; do not create dependency cycles.
7. If a pack flow changes, ensure every flow node is explicitly listed in that pack and its prerequisites appear earlier when both are in the flow.
8. Treat pack `domains` as routing constraints; do not broaden them merely to increase matches.

## Security research quality bar

- Distinguish hypothesis, observed, validated, and regression-verified evidence.
- Require explicit scope/authorization before intrusive work.
- Prefer local, owned, sandboxed, CTF, benchmark, or explicitly authorized targets.
- Prefer benign proof signals: assertions, sanitizer output, controlled crashes, synthetic resources, marker files, policy simulation, and regression tests.
- Do not turn methodology into credential theft, persistence, destructive action, evasion, malware deployment, or indiscriminate exploitation guidance.
- Record uncertainty, mitigations, and environment dependence instead of overstating exploitability.
- Tool output or LLM judgment alone never confirms a vulnerability.
- Keep chain claims hop-by-hop: renderer bug ≠ sandbox escape; memory corruption ≠ code execution; exposed interface ≠ authorization bypass.
- For multi-step investigations, preserve state in the research-case contract rather than inferring evidence level from chat history.
- The skill router is advisory-only. It may suggest a path but cannot grant authorization, confirm a claim, or skip evidence gates.
- Benchmark fixtures are conformance tests, not exploit tasks. Keep them synthetic/controlled, deterministic, and free of live external targets or deployable attack payloads.
- Do not weaken benchmark thresholds or forbidden-route expectations merely to make CI green; change them only when a reviewed contract change justifies the new behavior.

## Completion gate

Run all of:

```bash
python scripts/validate_skills.py
python scripts/validate_graph.py
python scripts/build_catalog.py
python scripts/build_graph.py
python scripts/build_catalog.py --check
python scripts/build_graph.py --check
python scripts/validate_case.py examples/research-case.example.json
python scripts/route_skills.py examples/research-case.example.json --limit 12
python scripts/validate_benchmarks.py
python scripts/run_benchmarks.py benchmarks/suites/portability.json
python scripts/run_benchmarks.py benchmarks/suites/core.json
python -m unittest discover -s tests -v
```

Regenerate stale outputs before the checks:

```bash
python scripts/build_catalog.py
python scripts/build_graph.py
```
