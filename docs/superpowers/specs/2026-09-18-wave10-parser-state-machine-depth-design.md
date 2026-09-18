# Wave 10 Profile #28 — Parser State Machine Causal Depth Design

**Date:** 2026-09-18  
**Base authority:** `main@7b283ad5a2315918e82f763e4aa23d0e8e9a5594`  
**Canonical skill:** `parser-state-machine-analysis`

## Purpose

Promote the existing parser state-machine skill into the twenty-eighth CI-enforced operator-depth profile while preserving its canonical identity and all existing graph/routing/benchmark authority.

The existing skill already maps phases, trust-promotion points, redundant metadata, duplicate ordering, error recovery, nested ownership, cross-record references, and phase-boundary mutations. The missing contract is causal: which parser instance and input generation produced which state transition, which invariant was expected at that transition, which semantic object was emitted, and which downstream consumer accepted the inconsistent state.

## Causal model

Every promoted parser-state finding must bind one reconstructable tuple:

`input artifact identity + input generation + parser instance identity + parser configuration/version + phase identity + state generation + transition identity + token/record identity + framing/length/count/offset metadata + semantic object identity + semantic object generation + invariant expected + invariant observed + recovery/deferred-validation state + downstream consumer identity + effective semantic capability + bounded result + receipt/result`

The profile must identify the **first invalid state transition** and distinguish it from later crashes, assertion failures, or downstream symptoms.

## Required distinctions

Freeze these non-equivalences:

- malformed input != parser vulnerability;
- parse acceptance != semantic acceptance;
- parser crash != exploitability;
- harness crash != parser crash;
- phase reach != invariant violation;
- duplicate record != duplicate semantic effect;
- warning/recovery != successful validation;
- deferred validation != omitted validation;
- outer length mismatch != out-of-bounds access;
- integer wrap != security consequence;
- overlapping regions != harmful aliasing;
- forward reference != dangling reference;
- partial object != privileged semantic object;
- state divergence != downstream dangerous consumption;
- grammar mismatch != parser-state bug;
- minimized crash != same causal phase path.

## Parser identity and generations

Track independently:

- input artifact identity/hash and mutation generation;
- parser binary/build/version/configuration identity;
- parser instance/session generation;
- phase identity and phase generation;
- state-machine node/state generation;
- token/record/section identity and generation;
- nested child parser identity;
- semantic object identity and generation;
- recovery/resynchronization generation;
- deferred-validation generation;
- downstream consumer generation.

A parser restart, nested parser instantiation, rewind/resynchronization, reparsing pass, lazy/deferred validation pass, or object reconstruction may create a new causal generation even when it consumes the same bytes.

## Transition and invariant binding

For each suspicious path, record:

1. source parser state;
2. input token/record/section consumed;
3. transition condition;
4. expected invariant before transition;
5. resulting parser state;
6. actual invariant after transition;
7. whether recovery or deferred validation modified the state;
8. semantic object emitted or mutated;
9. downstream consumer;
10. bounded result.

A later crash does not prove the transition was security relevant. Evidence must bind the first invalid transition to the downstream semantic consumer.

## Structural metadata and object binding

Lengths, counts, offsets, indexes, parent/child relationships, cross-record IDs, compression sizes, checksums, and duplicate ordering decisions are only metadata until their interpretation is bound to an exact parser state and semantic object.

The profile must distinguish:

- raw field value;
- normalized/decoded value;
- arithmetic result;
- allocation/view size;
- region/object identity;
- semantic object generated;
- consumer that trusts it.

Bounds/integer mechanics remain owned by the neighboring canonical skill; this profile owns the **state-machine and phase-order reasoning** around those values.

## Error recovery and deferred validation

Recovery paths must be modeled as explicit transitions, not generic “parser continued” observations. Record:

- error class and state;
- bytes/tokens skipped or retained;
- resynchronization target;
- partial object lifetime;
- flags marking untrusted/incomplete state;
- later pass expected to validate or finalize;
- whether downstream consumers honor those flags/generations.

A warning path is not a vulnerability unless incomplete or inconsistent state survives into a consumer that assumes stronger validation.

## Nested parser and cross-record provenance

For nested formats or child parsers, bind child input slices/views to the parent artifact and generation. Record who owns the bytes, whether remapping/decompression/reallocation changed identity, and how child semantic objects are linked back to parent records.

For cross-record references, record source record identity, destination record identity, resolution generation, duplicate/overwrite policy, cycle state, and final linked semantic object.

## Evidence ladder

- **PS0 — Surface mapped:** parser phases, state nodes, trust-promotion points, metadata relationships, recovery paths, nested parsers, and consumers are identified.
- **PS1 — State divergence observed:** a repeatable phase/state/invariant/recovery divergence exists, but the final semantic consumer has not accepted the inconsistent state.
- **PS2 — Controlled transition-policy mismatch:** a deterministic fixture proves a documented transition, validation-order, recovery, or phase invariant can be violated.
- **PS3 — Inert inconsistent semantic acceptance:** a read-only/inert downstream consumer accepts a semantic object created from the wrong parser state, generation, phase, or deferred-validation status.
- **PS4 — Bounded reversible semantic effect:** a synthetic marker, read-only result, or reversible owner-controlled semantic transition is causally bound to the exact input/parser/state/transition/object/consumer tuple.
- **PS5 — Regression-verified causal parser proof:** PS4 plus complete input and parser provenance, first-invalid-transition trace, recovery/deferred-validation state, semantic object lineage, meaningful counterfactuals, eliminated alternatives, receipt/result binding, and remediation replay.

Malformed files, parser crashes, sanitizer findings, warnings, duplicate records, phase reach, or synthetic markers cannot skip missing causal bindings.

## Deterministic benign review cases

At minimum freeze these four cases:

1. `recovery-state-trust-promotion` — recovery/resynchronization leaves a partial synthetic object marked inconsistently before a later consumer.
2. `duplicate-record-semantic-selection` — duplicate synthetic records cause a deterministic first/last-wins divergence between parser state and downstream selection.
3. `nested-length-phase-drift` — parent and child synthetic lengths remain individually parseable but disagree across phase generations, producing an inconsistent child semantic view.
4. `deferred-reference-resolution-generation` — a forward/cross-record synthetic reference is resolved under a later generation without validating the originating parser-state assumptions.

Use synthetic in-memory files/records, mock consumers, read-only semantic objects, deterministic parser fixtures, and bounded reversible markers only.

## Counterfactual requirements

Each review case changes exactly one causal variable while holding the rest constant, such as:

- recovery disabled vs enabled;
- duplicate ordering first-wins vs last-wins;
- parent length generation A vs B;
- deferred validation before vs after semantic consumption;
- reference resolution generation current vs stale.

Generic fuzzing volume or timing is not a sufficient counterfactual.

## Alternative explanations

Before PS4/PS5 eliminate:

- harness glue failed before parser state changed;
- minimized fixture follows a different phase path;
- sanitizer instrumentation created the observation;
- format model is wrong;
- duplicate behavior is documented;
- recovery is intentionally permissive and downstream respects incomplete flags;
- semantic object was rebuilt safely in a later pass;
- child parser consumes a copy with independent valid bounds;
- neighboring bounds/integer/lifetime issue fully explains the result;
- receipt belongs to a different parser instance or input generation.

Any unresolved material alternative caps evidence at PS2.

## Expected repository scope

1. `README.md`
2. `docs/operator-depth-contract.md`
3. `docs/superpowers/plans/2026-09-18-wave10-parser-state-machine-depth.md`
4. `docs/superpowers/specs/2026-09-18-wave10-parser-state-machine-depth-design.md`
5. `operator-depth/profiles.json`
6. `skills/parser-state-machine-analysis/SKILL.md`
7. `skills/parser-state-machine-analysis/references/operator-review-cases.json`
8. `skills/parser-state-machine-analysis/references/operator-runbook.md`
9. `tests/test_parser_state_machine_depth.py`
10. `tests/test_sandbox_boundary_depth.py` only if behavioral CI proves its exact global-count assertion is the sole extensibility defect.

Do not change `skill.meta.json`, graph edges, packs, routing domains, benchmark authority, agent-eval authority, superiority-court authority, or workflow semantics.

## Success criterion

Profile #28 is complete only when the merge tree contains exactly 28 profiles, exactly one valid `parser-state-machine-analysis` entry, PS0–PS5 is published, exact-head and post-merge CI are fully green, and final scope remains bounded to the intended paths.
