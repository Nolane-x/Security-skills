---
name: parser-state-machine-analysis
description: "Analyze multi-phase parsers, nested formats, length/count bookkeeping, error recovery, deferred validation, container/child relationships, and parser state transitions in authorized code. Use when a parser bug depends on phase order, malformed structure, partial success, duplicate records, or post-parse semantic processing."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Parser State Machine Analysis

Treat a parser as a state machine that transforms untrusted bytes into increasingly trusted objects. Security bugs often appear where one phase assumes another phase established an invariant that was only partially checked.

## When to use

Use for file formats, archive/container readers, protocol decoders, image/media parsers, configuration languages, bytecode/loaders, or custom binary/text grammars.

## Preconditions

Run malformed-input testing only against authorized local/owned/sandboxed targets. Obtain format documentation or infer a phase model from source/traces.

## Workflow

1. **Draw phases.** Framing/header → index/table → body → nested parse → resolution/linking → validation → execution/render/use.
2. **List trust promotion points.** Where raw lengths become allocations, ids become pointers/references, tags select types, or parsed values become executable/configuration behavior.
3. **Track redundant metadata.** Outer/inner lengths, count vs actual entries, offsets vs buffer size, checksums, compressed/uncompressed size.
4. **Inspect duplicate and ordering behavior.** First-wins/last-wins, repeated metadata, forward references, out-of-order definitions.
5. **Inspect error recovery.** Partial objects, skipped bytes, resynchronization, rollback, cleanup, and whether “warning” states continue with weakened invariants.
6. **Inspect nested ownership.** Parent buffers versus child views/slices and lifetime after decompression/remapping.
7. **Model cross-record references.** Cycles, dangling ids, integer domains, aliasing, overlapping regions.
8. **Target phase-boundary mutations.** Inputs valid enough to cross one gate but inconsistent with the next phase’s assumptions.
9. **Minimize while preserving phase reach.** A smaller file that fails earlier may not represent the same bug.
10. **Validate root cause** with phase trace, first invalid state, and controls.

## Evidence contract

Preserve the minimized structure, parse-phase trace, invariant expected at each boundary, first phase where state becomes inconsistent, and downstream consumer. A malformed file being rejected or crashing only in harness glue is not a parser vulnerability.

## Causal parser-state model

Treat every promoted parser finding as one causal tuple:

`input artifact identity + input generation + parser instance identity + parser configuration/version + phase identity + state generation + transition identity + token/record identity + structural metadata + semantic object identity + semantic object generation + invariant expected + invariant observed + recovery/deferred-validation state + downstream consumer identity + effective semantic capability + bounded result + receipt/result`.

The proof must identify the **first invalid state transition**, not merely the final crash or warning. Each later symptom must be bound back to that transition and to the semantic object consumed downstream.

Preserve these distinctions explicitly:

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

## Parser, input, phase, and state generations

Record independently:

- input artifact identity and input generation;
- parser instance identity;
- parser configuration/version and build identity;
- phase identity and phase generation;
- state-machine node and state generation;
- token/record/section identity and generation;
- nested child-parser identity;
- semantic object identity and semantic object generation;
- recovery/resynchronization generation;
- deferred-validation generation;
- downstream consumer generation.

A parser restart, reparsing pass, rewind/resynchronization, lazy validation, nested parser creation, decompression/remapping, or semantic-object rebuild can create a new causal generation even when the same source bytes are involved.

## Transition and invariant binding

For each suspicious path, record:

1. source parser state;
2. transition identity;
3. token/record/section consumed;
4. transition condition;
5. invariant expected before the transition;
6. resulting phase/state generation;
7. invariant observed after the transition;
8. recovery/deferred-validation state;
9. semantic object emitted or mutated;
10. downstream consumer identity and bounded result.

A later crash or assertion is only a symptom unless the first invalid transition is causally tied to a semantic object that survives into a downstream consumer.

## Structural metadata and semantic-object binding

Lengths, counts, offsets, indexes, checksums, compressed/uncompressed sizes, parent/child relationships, duplicate-order decisions, and cross-record IDs must be interpreted through an exact parser state.

Track:

`raw field -> decoded/normalized value -> arithmetic or selection result -> allocation/view/region identity -> parser transition -> semantic object identity/generation -> downstream consumer`.

Bounds/integer mechanics remain owned by the neighboring canonical skill. This profile owns the parser-state, phase-order, and semantic-object reasoning that explains when such metadata changes trust or object meaning.

Outer length mismatch != out-of-bounds access. Overlapping regions != harmful aliasing. Integer wrap != security consequence. Promotion requires the downstream state/consumer binding.

## Error recovery and deferred-validation binding

Model recovery and deferred validation as explicit state transitions.

Record:

- originating error class and parser state;
- bytes/tokens skipped, retained, or resynchronized;
- recovery target phase/state;
- partial object identity and generation;
- incomplete/untrusted flags;
- deferred-validation pass identity and generation;
- later consumer expectations;
- whether incomplete flags or stale generations are honored.

Warning/recovery != successful validation. Deferred validation != omitted validation. A permissive recovery path becomes security relevant only if incomplete or inconsistent state survives into a consumer that assumes a stronger invariant.

## Nested parser and cross-record provenance

For nested formats, bind child input views/slices to the parent artifact identity and generation. Record parent parser instance, child parser instance, byte/view identity, ownership, decompression/remapping generation, and the semantic object returned to the parent.

For cross-record references, bind source record, destination record, resolution generation, duplicate/overwrite policy, cycle state, and final linked semantic object. Forward reference != dangling reference unless the final resolution produces a stale, invalid, or semantically inconsistent object that is consumed.

## Downstream consumer and bounded semantic effect

Name the exact downstream consumer that converts inconsistent parser state into a meaningful semantic result.

Record:

- semantic object identity and generation;
- parser state/phase generation that produced it;
- invariant expected and invariant observed;
- downstream consumer identity;
- effective semantic capability actually demonstrated;
- bounded result;
- receipt/result correlation.

Prefer read-only semantic objects, inert markers, synthetic records, mock renderers/interpreters, or reversible owner-controlled state. Partial object != privileged semantic object, and state divergence != downstream dangerous consumption without this final binding.

## Parser-state evidence ladder

Use PS0–PS5 exactly:

- **PS0 — Surface mapped.** Phases, state nodes, trust-promotion points, metadata relationships, recovery paths, nested parsers, cross-record links, and downstream consumers are identified.
- **PS1 — State divergence observed.** A repeatable phase/state/invariant/recovery divergence exists, but final semantic acceptance is not shown.
- **PS2 — Controlled transition-policy mismatch.** A deterministic fixture proves a documented transition, validation-order, recovery, phase, or deferred-validation invariant can be violated.
- **PS3 — Inert inconsistent semantic acceptance.** A read-only/inert downstream consumer accepts a semantic object created under the wrong parser state, generation, phase, or deferred-validation status.
- **PS4 — Bounded reversible semantic effect.** A synthetic marker, read-only result, or reversible owner-controlled semantic transition is causally bound to the exact input/parser/state/transition/object/consumer tuple.
- **PS5 — Regression-verified causal parser proof.** PS4 plus complete input/parser provenance, first-invalid-transition trace, recovery/deferred-validation state, semantic-object lineage, meaningful counterfactual controls, eliminated alternative explanations, receipt/result binding, and remediation replay.

Malformed files, parser crashes, sanitizer findings, warnings, duplicate records, phase reach, or synthetic markers cannot skip missing causal bindings.

## Counterfactual parser controls

Hold semantic inputs constant and change one causal parser variable:

- recovery disabled versus enabled;
- duplicate selection first-wins versus last-wins;
- parent metadata generation A versus B;
- deferred validation before versus after semantic consumption;
- current versus stale reference-resolution generation;
- same semantic object rebuilt under a valid versus invalid phase transition.

A generic timing delay or fuzzing volume is not a sufficient counterfactual.

## Alternative explanations

Before PS4 or PS5, test and reject:

- harness glue failed before parser state changed;
- minimized fixture follows a different phase path;
- sanitizer/debug instrumentation created the observation;
- the inferred format model is wrong;
- duplicate selection behavior is documented;
- recovery is intentionally permissive and downstream respects incomplete flags;
- a later validation pass safely rebuilds the object;
- child parser consumes an independent safe copy;
- a neighboring bounds/integer/lifetime issue fully explains the result;
- the receipt belongs to another parser instance or input generation.

Any unresolved material alternative caps evidence at PS2.

## Evidence ceiling

Apply the narrowest supported level:

- mapped parser/phase surface only: PS0 maximum;
- state or invariant divergence without final semantic acceptance: PS1 maximum;
- deterministic transition mismatch without final consumer: PS2 maximum;
- inert/read-only inconsistent semantic acceptance: PS3 maximum;
- bounded causally bound semantic effect: PS4 maximum;
- only complete first-invalid-transition provenance, counterfactuals, receipts, and remediation regression reaches PS5.

Never promote malformed input, a crash, a warning, phase reach, or a sanitizer finding into a stronger parser-security claim without the missing causal bindings.

## Stop conditions

Stop when the failure is an intentional hard rejection with no security-relevant side effect, the format model is too wrong to preserve phase reach, or testing would leave authorized scope.

## Output

```text
format/parser:
phase model:
trust-promotion points:
redundant/cross-record metadata:
first inconsistent state:
downstream assumption:
minimized structure:
controls:
variant phases:
```
