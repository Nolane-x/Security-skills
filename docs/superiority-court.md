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

## Evaluation firewall

A blind comparison is invalid if a contestant can read the private judge authority.

`superiority/corpus.json`, the superiority scorer, court builders, benchmark authority, tests, and CI files belong to the **judge side**. They must not be exposed to the contestant process.

For the Security Skills arm, build a deterministic contestant-only surface outside the source repository:

```bash
python scripts/build_contestant_view.py --out /tmp/security-skills-contestant
```

The builder uses an explicit allowlist and emits `CONTESTANT_VIEW.json` with per-file hashes plus a deterministic `surface_digest`. It excludes the superiority authority, benchmark/evaluation roots, tests, CI configuration, and court/scoring scripts. The destination must be outside the source repository and empty, so stale or judge-side files cannot be inherited accidentally.

A real comparison must preserve that manifest and record its `surface_digest` in every run artifact. The contestant runtime must not have another path, mount, connector, network route, or tool that can retrieve the judge repository or private authority. If such access exists, the blind run is invalid and must be discarded rather than scored.

Other frameworks should be packaged under the same principle: expose only the framework surface intended to help the model, record an immutable digest of that surface, and keep judge material inaccessible.

## Public task / private authority split

`superiority/corpus.json` is the private scoring authority. Each fixture contains a public task plus private expected decisions, hard rules, and a minimum score.

```bash
python scripts/prepare_superiority_tasks.py superiority/suites/core.json --out tasks
```

produces 12 oracle-free task artifacts plus `SUITE_MANIFEST.json`. Each public task contains only:

- schema version;
- fixture ID;
- category;
- task content;
- SHA-256 task digest.

The suite manifest contains the exact ordered fixture/task-digest set and a SHA-256 `authority_commitment`. That commitment binds the semantic private expected answers, hard rules, thresholds, categories, and suite identity without revealing them.

Private expected answers, hard rules, and thresholds are never copied into contestant tasks or the public manifest.

The task output directory must be empty. Reusing a directory that contains stale artifacts fails closed.

## Contestant run contract

A contestant returns one JSON artifact per fixture:

```json
{
  "schema_version": 1,
  "fixture_id": "evidence-single-signal",
  "contestant_id": "opaque-a",
  "contestant_surface_digest": "<64 lowercase hex characters>",
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

All runs for one contestant must carry the same contestant-surface digest. Contestant IDs should remain opaque until the court artifact is frozen. Hidden reasoning or chain-of-thought is neither requested nor stored.

## Deterministic scoring

Scoring requires the same frozen public manifest that was published before contestant execution:

```bash
python scripts/score_superiority_runs.py \
  superiority/suites/core.json \
  <runs-dir> \
  --manifest tasks/SUITE_MANIFEST.json \
  --json scores.json
```

The scorer recomputes each task from the private corpus and verifies:

- suite identity;
- the exact public fixture/task-digest set;
- the exact semantic private `authority_commitment`;
- fixture identity and task digest on every run;
- one non-empty contestant ID;
- one valid contestant-surface digest across the entire contestant run set;
- complete, non-duplicate fixture coverage.

If the judge answers, hard rules, thresholds, categories, or task definitions drift after the public manifest was frozen, scoring fails closed instead of silently accepting the new authority.

List-valued answers are normalized for order so equivalent check sets do not receive an arbitrary ordering penalty. A hard-rule mismatch makes that fixture fail even when the arithmetic score would otherwise exceed the fixture threshold.

The score artifact preserves both `authority_commitment` and `contestant_surface_digest` for downstream audit.

## Court construction

```bash
python scripts/build_superiority_court.py \
  superiority/suites/core.json \
  scores-a.json scores-b.json \
  --json court.json
```

requires at least two unique contestants evaluated on the same suite.

The court refuses score artifacts whose authority commitment is malformed, differs across contestants, or differs from the current recomputed private authority. It also validates contestant-surface provenance and task identity before aggregation.

The final court artifact preserves the single frozen `authority_commitment` and each contestant's `contestant_surface_digest`, then computes:

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

CI builds the Security Skills contestant view twice outside the repository and requires byte-identical snapshots. It prepares public tasks/manifests twice, requires byte-identical task artifacts, scores replay profiles against the corresponding frozen manifests, builds the court twice, and requires byte-identical score/court artifacts. The final court check also verifies authority commitment and contestant-surface provenance.

The synthetic replay profiles use an explicit fixed self-test surface digest. They are not representations of a real external framework run.

This proves that the court implementation, firewall builder, authority commitment, scorer binding, provenance propagation, and dominance rule are deterministic under controlled fixtures. It does **not** prove that Security Skills is empirically superior to any external framework.

## Protocol for a real external comparison

For a defensible comparison between Security Skills and another framework:

1. preregister the suite/corpus revision, model family, exact model version, system policy, context budget, tool budget, temperature/sampling settings, timeout, retry policy, and repeated-run/seed plan;
2. build and freeze each contestant-visible framework surface; preserve its manifest/digest and ensure the judge authority is inaccessible from the contestant runtime;
3. generate the public task set exactly once; freeze `SUITE_MANIFEST.json` before any contestant sees a task;
4. assign opaque contestant IDs and keep the identity mapping sealed until scoring is complete;
5. give every contestant the identical public task digest and equivalent runtime/tool budget; only the framework surface being evaluated may differ;
6. require the structured run contract above and reject task-digest or contestant-surface drift;
7. score every contestant with the same private corpus/scorer revision and the frozen public manifest; any authority-commitment mismatch invalidates the scoring attempt;
8. build and freeze score artifacts and the final court artifact before unblinding contestant identities;
9. preserve the court authority commitment, task digests, contestant-surface digests, model/runtime configuration, and raw structured runs as the audit record;
10. for stochastic models, repeat the full paired protocol across all preregistered seeds/runs and report every result rather than selecting a favorable run.

For a direct Security Skills versus Claude-Red experiment, the model itself must remain identical across both arms. Otherwise a model-quality difference is confounded with a framework-quality difference.

## Interpretation boundary

A court result means only that one evaluated framework produced better conformance on the reviewed Wave 9 decision corpus under the pinned experimental protocol.

It does not establish universal superiority in exploit knowledge, general intelligence, every security domain, every model, or every real-world environment. Broader claims require broader preregistered corpora, independent repetitions, and additional domain-specific courts.
