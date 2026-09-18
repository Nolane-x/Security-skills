# Oracle And External Data Trust Operator Runbook

Use this runbook only for local, owned, sandboxed, benchmark/CTF, simulated, or explicitly authorized systems. Keep every experiment deterministic and bounded. Use synthetic feeds, fake reports/signatures, mock aggregators, local test contracts, read-only consumers, fake accounting ledgers, and reversible threshold markers. Do not manipulate live markets, production feeds, or third-party funds.

## Attack surface

Map:

- datum classes and required trust properties;
- source/provider identities and source generation;
- source-set/quorum identities;
- feed/configuration generation;
- round/observation identity and generation;
- publication, retrieval, and consumption timestamps;
- heartbeat/freshness policy;
- unit/decimal/scale configuration;
- normalization transform;
- aggregation/source diversity/quorum;
- fallback and emergency paths;
- sequencer/liveness state;
- authenticity/verifier state;
- replay/order and origin-domain binding;
- consumer snapshot/state generation;
- consuming invariant reference.

## Hypothesis matrix

| Hypothesis | Safe oracle | Control |
| --- | --- | --- |
| old heartbeat policy accepts stale round | synthetic feed and read-only consumer emit a generation-tagged receipt | current freshness generation rejects the same stale round |
| stale decimals config changes semantic quantity | fake feed value is normalized into a shadow read-only quantity | current decimal generation yields intended normalized value |
| fallback weakens source diversity | mock aggregator reports only source-set membership and selected aggregate | fallback policy preserving minimum independence is accepted |
| valid report is misbound to wrong origin | fake signed report reaches inert local consumer under wrong domain generation | intended chain/domain/contract/function binding succeeds |

## Datum/source/configuration-generation trace

Record:

- datum class;
- required trust property;
- source/provider identity and source generation;
- source-set/quorum identity/generation;
- feed identity;
- configuration generation;
- direct/aggregated/cached/bridged/signed/fallback delivery mode;
- consumer identities.

Do not equate a stable address or adapter with a stable source/configuration generation.

## Round/freshness/heartbeat trace

Capture:

- observation/round identity;
- observation generation;
- publication timestamp;
- retrieval timestamp;
- consumption timestamp;
- heartbeat/freshness policy identity and generation;
- maximum age;
- grace period;
- ordering rule;
- missing/skipped round semantics.

A recent timestamp alone is not proof of current external state.

## Unit/decimal/normalization trace

Capture:

- source-native unit;
- decimal/scale identity and configuration generation;
- normalization transform identity;
- intermediate representation when relevant;
- target unit/scale;
- normalized value;
- consumer expectation.

Keep numeric width/overflow/truncation proof in `bounds-and-integer-analysis`; here prove semantic quantity/configuration binding.

## Aggregation/source-diversity/quorum trace

Capture:

- member source identities/generations;
- underlying origin identities;
- independence assumptions;
- source-set/quorum generation;
- aggregation algorithm/configuration generation;
- weights;
- threshold/source-count requirements;
- deviation/outlier rules;
- missing-source behavior;
- selected aggregate.

Quorum count without independence evidence does not establish source diversity.

## Fallback/liveness-state trace

Capture:

- transition trigger;
- primary source/configuration generation;
- fallback source/path generation;
- fallback hierarchy;
- changes in freshness/diversity/authentication assumptions;
- sequencer/liveness state and generation;
- minimum-up/grace period;
- recovery/re-entry rule;
- final consumer snapshot.

Treat fallback as a trust-policy transition, not only an availability switch.

## Authenticity/replay/origin-domain trace

For signed, relayed, or cross-domain data record:

- report/message identity;
- source/signer identity;
- verifier identity/generation;
- origin chain/domain identity;
- origin contract/function identity;
- destination/consumer identity;
- round/epoch;
- freshness state;
- replay/order identity;
- final trust decision.

A valid signature is insufficient without intended origin, freshness, replay, and consumer binding.

## Consumer-snapshot/invariant-reference trace

Record:

- downstream consumer identity;
- consumer snapshot/state generation;
- exact normalized datum;
- source/round/configuration generations;
- checks actually performed;
- consuming invariant reference or decision threshold;
- local state transition/result;
- effective external-data-trust capability;
- bounded result;
- receipt/result.

Do not infer the downstream economic invariant violation here; keep that root ownership with `smart-contract-invariant-analysis`.

## Controlled validation

Use:

- deterministic synthetic feed rounds;
- fake timestamps and heartbeat policy generations;
- fake decimals/configuration versions;
- mock independent and aliased source sets;
- mock aggregators;
- fake signed reports and local verifier keys;
- local chain/domain identifiers;
- read-only consumer snapshots;
- fake accounting ledgers or inert threshold markers.

Recommended sequence:

1. establish the current valid datum positive control;
2. establish a clearly invalid negative control;
3. change exactly one source/round/freshness/unit/aggregation/fallback/origin variable;
4. capture the first trust-policy mismatch;
5. bind it to the final consumer snapshot;
6. apply the minimal trust-policy/configuration fix;
7. replay the exact same synthetic fixture;
8. capture deterministic before/after receipts.

## False-positive controls

Eliminate:

- source contract permits the round behavior;
- configured staleness is intentionally accepted;
- source timestamps and consumer clocks use different but correctly converted domains;
- decimal conversion is equivalent by specification;
- source disagreement remains inside designed tolerance;
- source correlation is documented and accepted;
- fallback deliberately has weaker but approved guarantees;
- signed report is intentionally domain-agnostic;
- replay state belongs to another consumer generation;
- independent bounds/integer arithmetic explains the result;
- downstream invariant logic is the root defect;
- fixture configuration does not match the modeled production path;
- receipt belongs to another feed/round/configuration/consumer generation.

## Counterfactual external-data controls

Hold the normalized datum semantics and consumer constant while changing one causal trust variable:

- old versus current freshness policy generation;
- stale versus current decimal configuration;
- independent versus aliased source membership;
- primary versus fallback path;
- intended versus wrong origin domain;
- old versus current consumer snapshot;
- replayed versus current round generation.

Arbitrary price perturbation alone is not a causal counterfactual.

## Alternative explanations

Before OED4/OED5 explicitly reject:

- specification-permitted staleness;
- policy-approved fallback downgrade;
- equivalent normalization;
- expected source correlation;
- downstream arithmetic defect;
- downstream invariant defect;
- fixture drift;
- unrelated report/round receipt;
- consumer-generation mismatch caused by the harness.

Any unresolved material alternative caps evidence at OED2.

## Evidence capture

Capture one reconstructable tuple:

`datum class + required trust property + source/provider identity + source/provider generation + source-set/quorum identity/generation + feed/configuration identity/generation + observation/round identity + observation generation + publication timestamp + retrieval/consumption timestamp + heartbeat/freshness policy identity/generation + unit/decimal/scale identity/generation + normalization transform identity + aggregation algorithm/configuration generation + fallback/emergency-path identity/generation + sequencer/liveness state generation + origin chain/domain/contract/function identity + authenticity/verifier identity/generation + replay/order identity + normalized external datum + consumer snapshot/state generation + downstream consumer identity + consuming invariant reference + effective external-data-trust capability + bounded result + receipt/result`

Useful artifacts include synthetic round logs, source-set membership snapshots, normalization receipts, fallback transition traces, fake-signature verification records, consumer snapshot IDs, and remediation replay.

## Evidence promotion and ceiling

### OED0 — External-data surface mapped

Datum classes, providers, source sets, rounds, freshness rules, units, aggregation, fallback, origin/authentication, and consumers are known.

### OED1 — Trust-context divergence observed

A repeatable source, round, freshness, unit, aggregation, fallback, origin, replay, or consumer-snapshot divergence exists without final wrong-context acceptance.

### OED2 — Controlled external-data policy mismatch

A deterministic local fixture proves a freshness, unit, source-diversity, aggregation, fallback, origin-domain, replay, or liveness policy mismatch.

### OED3 — Inert wrong-context datum acceptance

A mock/read-only consumer accepts a deterministic datum under the wrong source, round, freshness, unit/configuration, fallback, origin, or snapshot generation.

### OED4 — Bounded reversible external-data effect

A synthetic threshold marker, fake accounting state, inert transition, read-only result, or reversible owner-controlled marker is causally bound to the exact external-data tuple.

### OED5 — Regression-verified causal external-data proof

OED4 plus complete source/source-set/configuration provenance, round/freshness/unit/aggregation/fallback/origin binding, consumer snapshot, meaningful counterfactuals, eliminated alternatives, receipt/result binding, and remediation replay.

Evidence ceiling rules:

- surface/configuration only: OED0 maximum;
- trust-context divergence only: OED1 maximum;
- deterministic policy mismatch without final consumer: OED2 maximum;
- inert wrong-context acceptance: OED3 maximum;
- bounded causal external-data effect: OED4 maximum;
- complete causal proof plus regression: OED5.

## Remediation checks

Replay the exact fixture and verify:

1. current source/configuration generation is selected;
2. heartbeat/freshness policy uses current generation;
3. round/timestamp ordering is enforced;
4. decimal/unit normalization binds to current config;
5. aggregation uses intended independent source set and quorum;
6. fallback transitions preserve or explicitly enforce the intended trust policy;
7. sequencer/liveness grace periods are enforced;
8. signed/cross-domain reports bind to intended origin and replay state;
9. consumer snapshot receives only the current trusted datum;
10. deterministic receipts prove the change.

Prefer the smallest source/configuration, freshness, normalization, aggregation, fallback, domain-binding, or consumer-snapshot fix that restores the intended trust contract.
