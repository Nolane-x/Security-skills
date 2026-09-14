# Empirical Superiority Court

Wave 9 adds a framework-neutral, deterministic comparison court for evaluating two or more security-skill systems on the same reviewed tasks.

The court exists to replace subjective claims such as “framework A is stronger than framework B” with reproducible evidence. It does **not** make a universal intelligence claim, and the committed synthetic replay profiles are only self-tests of the court machinery.

## What the court measures

The core corpus contains 12 synthetic fixtures balanced across four categories:

- `scope` — authorization and boundary decisions;
- `evidence` — evidence-state and claim-promotion discipline;
- `checks` — positive/negative controls and false-positive resistance;
- `resolution` — remediation and regression-verification decisions.

The tasks are intentionally framework-neutral. They do not ask for Security Skills skill names, pack names, router outputs, Claude-specific concepts, or vendor-specific behavior.

## Public task / private authority split

`superiority/corpus.json` is the private scoring authority. Each fixture contains a public task plus private expected decisions, hard rules, and a minimum score.

`python scripts/prepare_superiority_tasks.py superiority/suites/core.json --out tasks`

produces oracle-free task artifacts. Each public task contains only:

- schema version;
- fixture ID;
- category;
- task content;
- SHA-256 task digest.

Private expected answers, hard rules, and thresholds are never copied into contestant tasks.

## Contestant run contract

A contestant returns one JSON artifact per fixture:

```json
{
  "schema_version": 1,
  "fixture_id": "evidence-single-signal",
  "contestant_id": "opaque-a",
  "task_digest": "<64 lowercase hex characters>",
  "answers": {
    "scope_choice": "allow",
    "evidence_level": "observed",
    "next_step": "collect",
    "claim_level": "provisional",
    "checks": ["negative-check", "positive-check"]
  }
}
```

Contestant IDs should remain opaque until the court artifact is frozen. Hidden reasoning or chain-of-thought is neither requested nor stored.

## Deterministic scoring

`python scripts/score_superiority_runs.py superiority/suites/core.json <runs-dir> --json scores.json`

recomputes each task from the private corpus, verifies fixture identity and task digest, then scores the structured decisions. List-valued answers are normalized for order so equivalent check sets do not receive an arbitrary ordering penalty.

A hard-rule mismatch makes that fixture fail even when the arithmetic score would otherwise exceed the fixture threshold.

Malformed input, mixed contestant identities, missing fixtures, duplicate fixtures, unknown fixtures, and task-digest drift fail closed as structural errors.

## Court construction

`python scripts/build_superiority_court.py superiority/suites/core.json scores-a.json scores-b.json --json court.json`

requires at least two unique contestants evaluated on the same suite.

The court computes:

- overall score per contestant;
- category score per contestant;
- rule-failure count;
- paired fixture wins, losses, and ties;
- category-regression status;
- pairwise verdicts;
- an optional global `absolute_winner`.

## Absolute-superiority rule

A higher average is **not** enough.

Contestant A can receive `left-absolute-superiority` over contestant B only when all of the following hold:

1. both contestants completed the entire suite and every fixture passed its own threshold/hard rules;
2. A has a strictly higher overall score;
3. A wins more paired fixtures than B;
4. A is not worse than B in any category;
5. A is strictly better in at least one category.

The rule is symmetric for contestant B.

If A has a higher average but regresses in one category, the verdict can only be `left-score-lead`, never `left-absolute-superiority`.

With more than two contestants, a global `absolute_winner` is emitted only when one contestant satisfies the absolute rule against every other contestant.

## CI self-test

The `superiority-court-core` job uses two deterministic synthetic replay profiles:

- `reference` — exactly follows the private authority;
- `degraded` — changes four non-hard-rule decisions while remaining structurally valid and above each fixture threshold.

CI prepares public tasks twice, scores replay profiles twice, builds the court twice, and requires byte-identical artifacts. It also verifies that the synthetic reference profile is the strict winner over the degraded profile.

This proves that the court implementation is deterministic and that its dominance rule detects a controlled difference. It does **not** prove that Security Skills is empirically superior to any external framework.

## Protocol for a real external comparison

For a defensible comparison between Security Skills and another framework:

1. pin the same model family, exact model version, system policy, context budget, tool budget, temperature/sampling settings, timeout, and retry policy;
2. generate the public task set exactly once and preserve its task digests;
3. assign opaque contestant IDs and keep the identity mapping sealed until scoring is complete;
4. give every contestant the same public task and runtime budget; only the framework context being evaluated may differ;
5. require the structured run contract above and reject task-digest drift;
6. score every contestant with the same private corpus and scorer revision;
7. freeze the score artifacts and court artifact before unblinding contestant identities;
8. for stochastic models, repeat the full paired protocol across predeclared seeds/runs and report every result rather than selecting a favorable run.

For a direct Security Skills versus Claude-Red experiment, the model itself must remain identical across both arms. Otherwise a model-quality difference is confounded with a framework-quality difference.

## Interpretation boundary

A court result means only that one evaluated framework produced better conformance on the reviewed Wave 9 decision corpus under the pinned experimental protocol.

It does not establish universal superiority in exploit knowledge, general intelligence, every security domain, every model, or every real-world environment. Broader claims require broader preregistered corpora and independent repetitions.
