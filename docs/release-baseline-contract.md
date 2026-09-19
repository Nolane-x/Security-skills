# Release Baseline Contract

The root `release-baseline.json` is the machine-readable authority for the frozen public architecture after Wave 10.

It exists to prevent release facts from drifting independently across README files, tests, benchmark suites, the operator-depth registry, and licensing metadata.

## Authority

The current closed baseline declares:

- 83 canonical skills;
- 20 packs;
- 40 CI-enforced operator-depth profiles;
- operator-depth registry schema version 2;
- 36 fixtures in the core deterministic benchmark suite;
- 12 fixtures in the portability suite;
- Apache-2.0 licensing;
- three synchronized public README landing pages.

These are release invariants, not quality scores. The contract does not claim that larger counts are better, that every skill needs operator depth, or that an internal benchmark proves external superiority.

## Validator

Run:

```bash
python scripts/validate_release_baseline.py
```

The validator compares the declared baseline with repository reality. It fails when:

- the canonical skill or pack count drifts;
- the operator-depth registry version or profile count drifts;
- a registered depth profile no longer maps to a canonical skill;
- a profile drops the `lab_only` safety boundary;
- core or portability benchmark fixture counts drift;
- benchmark suites contain duplicate or missing fixture paths;
- a required release path disappears;
- a public README stops publishing the frozen Wave 10 baseline;
- the root Apache-2.0 license is missing or incomplete.

The validator is zero-dependency and is executed in every CI matrix environment.

## Change policy

Changing `release-baseline.json` is an architecture change.

A pull request must not edit the baseline merely to make a failing validator pass. The repository reality and the declared release contract must be reconciled deliberately. Increasing skill, pack, profile, or fixture counts requires a concrete design reason and review of the corresponding architecture authority.

Routine maintenance should normally preserve the baseline and improve correctness, evidence quality, tests, documentation, safety, portability, or implementation reliability.

## Relationship to Wave 10 closure

`docs/wave10-closure-audit.md` explains why the Wave 10 program closed at the current architecture. This contract turns that closure into a reusable machine-readable gate.

`tests/test_wave10_closure.py` consumes the same baseline file so tests and public release metadata do not maintain separate copies of the architecture numbers.
