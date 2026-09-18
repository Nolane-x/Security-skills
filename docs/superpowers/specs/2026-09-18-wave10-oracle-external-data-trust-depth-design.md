# Wave 10 Profile #35 — Oracle And External Data Trust Causal Depth Design

**Date:** 2026-09-18  
**Base authority:** `main@50fadf2729baf2f8bc65e9c70f847358fda27b64`  
**Canonical skill:** `oracle-and-external-data-trust-analysis`

## Purpose

Promote `oracle-and-external-data-trust-analysis` into the thirty-fifth CI-enforced operator-depth profile without changing routing, graph, packs, benchmark authority, agent-eval authority, superiority-court authority, or workflow semantics.

The current skill already maps source, authentication, freshness, units/decimals, aggregation, fallback, sequencer state, cross-chain binding, and consuming invariants. The missing operator contract is causal identity across external-data generations: which source/source-set, feed configuration, round/observation, timestamp/freshness policy, unit/scale transform, aggregation generation, fallback state, authenticity/domain binding, and consumer snapshot were authoritative when the final contract/application decision consumed the datum.

## Causal model

Every promoted finding must bind one reconstructable tuple:

`datum class + required trust property + source/provider identity + source/provider generation + source-set/quorum identity/generation + feed/configuration identity/generation + observation/round identity + observation generation + publication timestamp + retrieval/consumption timestamp + heartbeat/freshness policy identity/generation + unit/decimal/scale identity/generation + normalization transform identity + aggregation algorithm/configuration generation + fallback/emergency-path identity/generation + sequencer/liveness state generation + origin chain/domain/contract/function identity + authenticity/verifier identity/generation + replay/order identity + normalized external datum + consumer snapshot/state generation + downstream consumer identity + consuming invariant reference + effective external-data-trust capability + bounded result + receipt/result`

The proof must identify the first external-data trust transition that becomes stale, misbound, under-authenticated, incorrectly normalized, improperly aggregated, or downgraded before binding that condition to the exact consumer snapshot.

## Required distinctions

Preserve explicitly:

- external datum accepted != external datum trusted for every consumer;
- source configured != source observed at the consuming generation;
- source identity != source-set/quorum identity;
- authenticated source != fresh source;
- fresh timestamp != fresh economic state by assumption;
- heartbeat configured != heartbeat enforced;
- round advanced != value current for the consuming snapshot;
- timestamp monotonicity != round semantic validity;
- nonzero value != valid value;
- positive value != valid domain value;
- source disagreement != aggregation failure by itself;
- quorum met != independent source diversity;
- multiple adapters != multiple independent data origins;
- fallback available != fallback equivalent in trust guarantees;
- fallback activation != safe downgrade;
- primary failure != authorization to weaken freshness/source diversity;
- unit label != unit binding;
- decimal metadata != normalized-value correctness;
- scale conversion != economic correctness;
- normalized numeric mismatch != bounds/integer root cause by assumption;
- stale oracle input != invariant violation until a consumer decision is bound;
- threshold crossing != economic exploitability;
- local synthetic consequence != real-market manipulability;
- signed datum != intended domain/chain/contract/function binding;
- signature valid != current round/freshness authorized;
- cross-chain message valid != source-domain state current;
- bridge relay success != final external-data trust decision;
- sequencer up != sequencer state sufficiently aged for use;
- sequencer down != all external data invalid by assumption;
- randomness beacon output != randomness-lifecycle proof;
- replayed datum != duplicate downstream effect by assumption;
- cached datum != stale datum unless cache generation and policy are bound;
- consumer read != immutable consumer snapshot;
- same feed address != same configuration generation;
- emergency override != production trust equivalence;
- code-level trust assumption != price manipulability;
- suspicious price != oracle compromise;
- crash/revert != external-data trust failure.

## Datum class, trust property, and source generations

For each external datum identify:

- datum class: price, rate, index, timestamp, randomness beacon output, signed report, bridge message, keeper input, sequencer status, or other external state;
- required trust properties: authenticity, freshness, availability, source diversity, unit correctness, ordering, replay resistance, domain binding, or liveness;
- source/provider identity and generation;
- source-set/quorum identity and generation;
- feed/configuration identity and generation;
- consumer(s) that depend on the datum.

Randomness generation/entropy state itself remains owned by `nonce-and-randomness-lifecycle-analysis`; this profile begins at the externally supplied beacon/report datum and its trust binding.

## Round, timestamp, heartbeat, and freshness binding

Record independently:

- observation/round identity;
- round generation or epoch;
- publication timestamp;
- retrieval timestamp;
- consumption timestamp;
- heartbeat/freshness policy identity/generation;
- maximum age and grace period;
- ordering constraints;
- previous/current round relationship;
- missing/skipped round semantics.

A numeric timestamp being recent does not prove the observation represents current external state. Freshness proof must follow the actual source contract.

## Unit, decimal, scale, and normalization binding

For each consumer path record:

- source-native unit;
- source-native decimals/scale;
- configuration generation;
- normalization transform identity;
- intermediate representation if relevant;
- target unit/scale;
- normalized value delivered to the consumer;
- consumer expectation.

Delegate arithmetic overflow/truncation/range equations to `bounds-and-integer-analysis`; this profile owns whether the external datum and its unit/scale configuration are bound to the intended semantic quantity.

## Aggregation, source diversity, and quorum binding

Track:

- member source identities/generations;
- independence assumptions;
- source-set/quorum generation;
- aggregation algorithm;
- weights;
- minimum/maximum source count;
- disagreement/deviation thresholds;
- outlier handling;
- missing-source behavior;
- selected aggregate identity/result.

Quorum met != independent source diversity. Multiple adapters pointing to one underlying origin are not independent merely because interfaces differ.

## Fallback, emergency, and liveness-state binding

For fallback or emergency paths capture:

- trigger identity;
- source/configuration generation before transition;
- fallback hierarchy;
- fallback source identity;
- changed freshness/diversity/authentication assumptions;
- sequencer/liveness state and generation;
- grace periods;
- recovery/re-entry conditions;
- consumer snapshot receiving the fallback datum.

A fallback is a trust-policy transition, not just an availability mechanism.

## Authenticity, replay, and origin-domain binding

For signed or cross-domain data capture:

- report/message identity;
- signer/source identity;
- verifier identity/generation;
- origin chain/domain identity;
- origin contract/function identity;
- destination/consumer identity;
- round/epoch identity;
- timestamp/freshness state;
- replay/order identity;
- final authenticity/domain/freshness decision.

Signature validity alone cannot establish intended domain, freshness, or current consumer authorization.

## Consumer snapshot and invariant-reference binding

For every promoted finding bind:

- consumer identity;
- consumer snapshot/state generation;
- exact normalized datum consumed;
- round/source/configuration generation;
- policy checks performed;
- consuming invariant reference or decision threshold;
- local state transition/result;
- effective external-data-trust capability;
- bounded result;
- receipt/result.

`smart-contract-invariant-analysis` owns whether the downstream state transition violates protocol accounting/solvency/ownership/liveness invariants. This profile proves the external datum that reached that invariant under the wrong trust context.

## Evidence ladder

Use OED0–OED5 exactly:

- **OED0 — External-data surface mapped.** Datum classes, providers, source sets, rounds, freshness rules, units, aggregation, fallback, origin/authentication, and consumers are identified.
- **OED1 — Trust-context divergence observed.** A repeatable source, round, freshness, unit, aggregation, fallback, origin, replay, or consumer-snapshot divergence exists without final wrong-context consumer acceptance.
- **OED2 — Controlled external-data policy mismatch.** A deterministic local fixture proves a documented freshness, unit, source-diversity, aggregation, fallback, origin-domain, replay, or liveness policy can be violated.
- **OED3 — Inert wrong-context datum acceptance.** A mock/read-only consumer accepts a deterministic external datum under the wrong source, round, freshness, unit/configuration, fallback, origin, or snapshot generation.
- **OED4 — Bounded reversible external-data effect.** A synthetic threshold marker, fake accounting state, inert state transition, read-only result, or reversible owner-controlled marker is causally bound to the exact source/round/policy/datum/consumer tuple.
- **OED5 — Regression-verified causal external-data proof.** OED4 plus complete source/source-set/configuration provenance, round/freshness/unit/aggregation/fallback/origin binding, consumer snapshot, meaningful counterfactuals, eliminated alternatives, receipt/result binding, and remediation replay.

Stale-looking values, source disagreement, valid signatures, threshold crossings, local reverts, price movements, or synthetic markers cannot skip missing causal bindings.

## Deterministic benign review cases

Freeze at least:

1. `stale-round-after-heartbeat-generation-change` — consumer accepts a round that is fresh under old policy generation but stale under the current heartbeat/freshness generation.
2. `decimal-configuration-generation-drift` — the same signed/source value is normalized using stale decimals/scale configuration and a read-only consumer observes the wrong semantic quantity.
3. `fallback-source-diversity-downgrade` — primary failure activates a fallback source set with weaker diversity/freshness guarantees without the required policy transition.
4. `cross-domain-report-binding-mismatch` — a valid synthetic signed report is accepted under the wrong origin chain/domain/contract/function or consumer-snapshot generation.

Use synthetic feeds, fake reports/signatures, mock aggregators, local fork/test contracts, read-only consumers, fake accounting ledgers, and bounded reversible threshold markers only.

## Counterfactual requirements

Change exactly one causal trust variable while holding datum semantics and consumer constant, for example:

- old versus current freshness-policy generation;
- stale versus current decimals configuration;
- independent versus aliased source-set membership;
- primary versus fallback source generation;
- intended versus wrong origin domain;
- stale versus current consumer snapshot;
- replayed versus current round generation.

## Alternative explanations

Before OED4/OED5 eliminate:

- source contract explicitly permits the round/timestamp behavior;
- consumer intentionally accepts the configured staleness window;
- unit conversion is specification-equivalent;
- source disagreement is within expected aggregation tolerance;
- source members are intentionally correlated and the trust model documents this;
- fallback guarantees are explicitly weaker and the consumer is designed for them;
- signed report is domain-agnostic by specification;
- replay/order state belongs to a different consumer generation;
- independent arithmetic/bounds error explains the result;
- downstream smart-contract invariant logic, not external-data trust, is the root cause;
- local fixture altered configuration differently from production logic;
- receipt belongs to another round/feed/configuration/consumer generation.

Any unresolved material alternative caps evidence at OED2.

## Ownership boundaries

- This profile owns provenance, freshness, units, aggregation, fallback, authenticity/domain, replay/order, and consumer-snapshot binding for external data.
- `smart-contract-invariant-analysis` owns downstream protocol/accounting invariant correctness.
- `bounds-and-integer-analysis` owns arithmetic width/signedness/overflow/range mechanics.
- `nonce-and-randomness-lifecycle-analysis` owns RNG state, seed, uniqueness, unpredictability, fork/restart, and counter lifecycle.
- `cryptographic-protocol-misuse-analysis` owns cryptographic protocol composition; this profile consumes authenticity results only as one external-data trust dimension.
- Future smart-contract reentrancy/upgradeability profiles own their respective state/control-flow mechanics.

## Expected repository scope

1. `README.md`
2. `docs/operator-depth-contract.md`
3. `docs/superpowers/plans/2026-09-18-wave10-oracle-external-data-trust-depth.md`
4. `docs/superpowers/specs/2026-09-18-wave10-oracle-external-data-trust-depth-design.md`
5. `operator-depth/profiles.json`
6. `skills/oracle-and-external-data-trust-analysis/SKILL.md`
7. `skills/oracle-and-external-data-trust-analysis/references/operator-review-cases.json`
8. `skills/oracle-and-external-data-trust-analysis/references/operator-runbook.md`
9. `tests/test_oracle_external_data_trust_depth.py`
10. `tests/test_nonce_randomness_lifecycle_depth.py` only if behavioral CI proves its exact global-count assertion is the sole extensibility defect.

Do not change `skill.meta.json`, graph edges, packs, routing domains, benchmark authority, agent-eval authority, superiority-court authority, or workflow semantics.

## Success criterion

Profile #35 is complete only when the merge tree contains exactly 35 profiles, exactly one valid `oracle-and-external-data-trust-analysis` entry, OED0–OED5 is published, exact-head and post-merge CI are fully GREEN, merge parents are verified, and the final scope remains bounded to the intended paths.
