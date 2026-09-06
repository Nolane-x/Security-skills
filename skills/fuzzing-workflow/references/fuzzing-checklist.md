# Fuzzing checklist

## Harness quality

A strong harness:

- reaches the intended parser/logic directly;
- avoids expensive unrelated initialization;
- resets state between iterations;
- does not depend on internet services or production resources;
- has a deterministic failure oracle;
- makes malformed input cheap to reject;
- preserves meaningful state if the target is intentionally stateful.

## Corpus quality

Prefer a small corpus that covers distinct syntax/state features over thousands of near-duplicates. Preserve minimized inputs that add coverage or exercise distinct transitions.

## Useful campaign observations

Record:

- executions per second or iterations per unit time;
- stable edge/state coverage;
- coverage growth over time;
- corpus size/growth;
- unique minimized failures;
- failure reproduction rate;
- fraction of time spent in the intended target.

## Stalls

Before buying more compute, inspect:

- checksums/length fields blocking depth;
- parser requiring grammar-aware mutations;
- global caches/state not reset;
- nondeterministic scheduling;
- blocking I/O;
- environment dependencies;
- a harness entry point that is too high-level or too narrow.

A campaign that cannot explain its coverage and oracle is not ready to support strong security claims.
