---
name: oracle-and-external-data-trust-analysis
description: "Analyze smart-contract oracle and external-data trust: source diversity, freshness, decimals/units, heartbeat, aggregation, fallback, sequencer status, cross-chain messages, and economic dependency. Use synthetic/local feed perturbations only."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Oracle And External Data Trust Analysis

Perform any dynamic validation only in an authorized, owned lab or equivalent explicitly scoped test environment.

## When to use

Use when contract state/actions depend on price feeds, randomness beacons, bridge messages, off-chain signatures, keepers, sequencer status, time, or external protocol state.

## Preconditions

1. Use local/forked test feeds and synthetic data.
2. Document source identities, update cadence, decimals/units, fallback hierarchy, and trust assumptions.
3. Do not manipulate live markets or production oracle feeds.

## Workflow

1. Map each external datum to source, authentication, freshness, unit/decimal conversion, aggregation, and consuming invariant.
2. Check stale/zero/negative/extreme values, source disagreement, missing rounds, sequencer downtime, timestamp/round ordering, and fallback transitions.
3. Trace cross-chain or signed data through domain/chain/contract/function binding and replay controls.
4. Use bounded synthetic feed perturbations to test liquidation/accounting/state-transition thresholds locally.
5. Check whether fallback or emergency paths weaken source diversity or freshness guarantees.
6. Separate oracle-input acceptance from economic exploitability; quantify only within synthetic/local model.

## Evidence contract

Record source/config, synthetic value/round/timestamp, validation performed, consuming invariant, and observed local state consequence. Price manipulability claims require evidence beyond code-level trust assumptions.

## Causal external-data trust model

Treat every promoted external-data finding as one causal tuple:

`datum class + required trust property + source/provider identity + source/provider generation + source-set/quorum identity/generation + feed/configuration identity/generation + observation/round identity + observation generation + publication timestamp + retrieval/consumption timestamp + heartbeat/freshness policy identity/generation + unit/decimal/scale identity/generation + normalization transform identity + aggregation algorithm/configuration generation + fallback/emergency-path identity/generation + sequencer/liveness state generation + origin chain/domain/contract/function identity + authenticity/verifier identity/generation + replay/order identity + normalized external datum + consumer snapshot/state generation + downstream consumer identity + consuming invariant reference + effective external-data-trust capability + bounded result + receipt/result`.

The proof must identify the first external-data trust transition that becomes stale, misbound, under-authenticated, incorrectly normalized, improperly aggregated, or downgraded and bind that transition to the exact consumer snapshot/state generation.

Preserve these distinctions explicitly:

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

All dynamic validation stays local/owned/sandboxed or explicitly authorized and uses synthetic feeds, fake reports/signatures, mock aggregators, local test contracts, read-only consumers, fake accounting ledgers, and bounded reversible threshold markers.

## Datum class, trust property, and source generations

For each external datum identify:

- datum class;
- required trust property;
- source/provider identity;
- source/provider generation;
- source-set/quorum identity/generation;
- feed/configuration identity/generation;
- consumer identities;
- whether the datum is direct, aggregated, cached, bridged, signed, or delivered through a fallback.

Useful trust properties include authenticity, freshness, availability, source diversity, unit correctness, ordering, replay resistance, origin-domain binding, and liveness.

Randomness generation/entropy lifecycle stays with `nonce-and-randomness-lifecycle-analysis`; this profile begins at the externally supplied beacon/report datum.

## Round, timestamp, heartbeat, and freshness binding

Track independently:

- observation/round identity;
- observation generation or epoch;
- publication timestamp;
- retrieval/consumption timestamp;
- heartbeat/freshness policy identity/generation;
- maximum age;
- grace period;
- ordering constraints;
- previous/current round relationship;
- missing/skipped-round semantics;
- source-specific update cadence.

A recent timestamp does not prove the represented external state is current. Freshness must be evaluated under the source contract and current policy generation.

## Unit, decimal, scale, and normalization binding

For each consumer path record:

- source-native unit;
- unit/decimal/scale identity/generation;
- feed configuration generation;
- normalization transform identity;
- intermediate representation where relevant;
- target unit/scale;
- normalized external datum;
- consumer expectation.

Delegate width, overflow, truncation, and arithmetic range equations to `bounds-and-integer-analysis`. This profile owns the semantic binding between source quantity, configuration generation, normalization, and intended consumer quantity.

## Aggregation, source diversity, and quorum binding

Track:

- member source identities/generations;
- independence assumptions;
- source-set/quorum identity/generation;
- aggregation algorithm/configuration generation;
- weights;
- minimum source count;
- disagreement/deviation thresholds;
- outlier handling;
- missing-source behavior;
- selected aggregate identity/result.

Quorum met != independent source diversity. Multiple adapters may share one underlying data origin and therefore one correlated trust failure.

## Fallback, emergency, and liveness-state binding

For every fallback or emergency transition capture:

- trigger identity;
- primary source/configuration generation;
- fallback/emergency-path identity/generation;
- fallback hierarchy;
- selected source/source-set identity;
- changed freshness, diversity, authentication, and availability assumptions;
- sequencer/liveness state generation;
- minimum-up/grace periods;
- recovery/re-entry conditions;
- consumer snapshot receiving the fallback datum.

Fallback is a trust-policy transition, not only an availability mechanism.

## Authenticity, replay, and origin-domain binding

For signed, relayed, or cross-domain data record:

- report/message identity;
- source/signer identity;
- authenticity/verifier identity/generation;
- origin chain/domain/contract/function identity;
- destination/consumer identity;
- observation/round/epoch identity;
- timestamp/freshness state;
- replay/order identity;
- final authenticity/domain/freshness decision.

Signature validity alone cannot prove that the report belongs to the intended chain, domain, contract, function, round, freshness window, or consumer generation.

Keep cryptographic composition/key-schedule proof with `cryptographic-protocol-misuse-analysis`.

## Consumer snapshot and invariant-reference binding

For each promoted finding capture:

- downstream consumer identity;
- consumer snapshot/state generation;
- normalized external datum;
- source/round/configuration generation;
- freshness, unit, aggregation, fallback, and origin checks performed;
- consuming invariant reference or decision threshold;
- local state transition/result;
- effective external-data-trust capability;
- bounded result;
- receipt/result.

`smart-contract-invariant-analysis` owns the downstream accounting/solvency/ownership/liveness invariant itself. This profile proves whether the wrong external trust context reached that invariant.

## External-data evidence ladder

Use OED0–OED5 exactly:

- **OED0 — External-data surface mapped.** Datum classes, providers, source sets, rounds, freshness rules, units, aggregation, fallback, origin/authentication, and consumers are identified.
- **OED1 — Trust-context divergence observed.** A repeatable source, round, freshness, unit, aggregation, fallback, origin, replay, or consumer-snapshot divergence exists without final wrong-context consumer acceptance.
- **OED2 — Controlled external-data policy mismatch.** A deterministic local fixture proves a documented freshness, unit, source-diversity, aggregation, fallback, origin-domain, replay, or liveness policy can be violated.
- **OED3 — Inert wrong-context datum acceptance.** A mock/read-only consumer accepts a deterministic external datum under the wrong source, round, freshness, unit/configuration, fallback, origin, or snapshot generation.
- **OED4 — Bounded reversible external-data effect.** A synthetic threshold marker, fake accounting state, inert state transition, read-only result, or reversible owner-controlled marker is causally bound to the exact source/round/policy/datum/consumer tuple.
- **OED5 — Regression-verified causal external-data proof.** OED4 plus complete source/source-set/configuration provenance, round/freshness/unit/aggregation/fallback/origin binding, consumer snapshot, meaningful counterfactuals, eliminated alternative explanations, receipt/result binding, and remediation replay.

Stale-looking values, source disagreement, valid signatures, threshold crossings, local reverts, price movements, or synthetic markers cannot skip missing causal bindings.

## Counterfactual external-data controls

Hold datum semantics and final consumer constant while changing one trust variable:

- old versus current freshness-policy generation;
- stale versus current decimal/scale configuration;
- independent versus aliased source-set membership;
- primary versus fallback source generation;
- intended versus wrong origin domain;
- stale versus current consumer snapshot generation;
- replayed versus current observation/round generation.

Generic arbitrary price/value changes are not sufficient counterfactuals unless they isolate the hypothesized trust binding.

## Alternative explanations

Before OED4 or OED5 reject:

- source contract explicitly permits the round/timestamp behavior;
- consumer intentionally accepts the configured staleness window;
- unit conversion is specification-equivalent;
- disagreement remains within aggregation tolerance;
- source members are intentionally correlated and the trust model documents it;
- fallback guarantees are explicitly weaker and the consumer is designed for them;
- signed report is domain-agnostic by specification;
- replay/order state belongs to another consumer generation;
- an independent bounds/integer defect explains the normalized value;
- downstream smart-contract invariant logic is the independent root cause;
- local fixture configuration differs from the production logic being modeled;
- receipt belongs to another round/feed/configuration/consumer generation.

Any unresolved material alternative caps evidence at OED2.

## Evidence ceiling

Apply the narrowest supported level:

- mapped source/configuration only: OED0 maximum;
- trust-context divergence without final consumer acceptance: OED1 maximum;
- deterministic external-data policy mismatch without final consumer: OED2 maximum;
- inert/read-only wrong-context consumer acceptance: OED3 maximum;
- bounded causally bound external-data effect: OED4 maximum;
- only complete source/round/freshness/unit/aggregation/fallback/origin/consumer provenance, counterfactuals, receipts, and remediation replay reaches OED5.

Do not promote stale-looking values, signatures, source disagreement, threshold crossings, reverts, or price movements into stronger claims without the missing causal bindings.

## Stop conditions

Stop before live price manipulation, real cross-chain message injection, or transactions that could affect third-party funds.

## Output

```text
oracle/source model:
auth/freshness/units:
fallback hierarchy:
synthetic perturbation:
consuming invariant:
local consequence:
evidence status:
```
