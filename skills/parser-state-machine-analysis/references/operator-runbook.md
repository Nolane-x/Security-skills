# Parser State Machine Operator Runbook

Use this runbook only for local, owned, sandboxed, benchmark/CTF, simulated, or explicitly authorized parser targets. The objective is deterministic causal parser evidence with synthetic or read-only effects.

## Attack surface

Map the parser before testing:

- input artifact identity and input generation;
- parser build/configuration and parser instance identity;
- phase graph and state-machine nodes;
- token/record/section boundaries;
- lengths, counts, offsets, indexes, checksums, compressed/uncompressed metadata;
- duplicate-order and first/last-wins rules;
- error recovery, rollback, resynchronization, and deferred-validation paths;
- nested parser creation and parent/child byte-view ownership;
- cross-record references, cycles, forward references, and resolution passes;
- semantic object construction and downstream consumers.

## Hypothesis matrix

| Hypothesis | Safe oracle | Control |
| --- | --- | --- |
| recovery promotes partial object too early | mock read-only consumer records incomplete synthetic object after resynchronization | same fixture with recovery disabled or required validation rejects |
| duplicate records produce semantic selection drift | controlled synthetic first/last records yield different semantic object than parser-state assumption | one-record fixture or pinned duplicate policy converges |
| nested parent/child lengths drift across phase generations | read-only child consumer reports controlled semantic view inconsistent with parent generation | identical lengths and generation binding converge |
| deferred reference resolves under stale generation | mock linker returns inert semantic receipt for stale source assumptions | generation revalidation rejects stale reference |

## Parser/input/phase-generation trace

For every case capture:

- input artifact identity/hash and input generation;
- parser instance and parser configuration/version;
- phase identity and phase generation;
- current state node and state generation;
- token/record/section identity;
- nested parser identity if present;
- semantic object generation;
- downstream consumer generation.

Do not merge multiple parser runs merely because the same bytes were used.

## Transition and invariant trace

Record:

1. source state;
2. transition identity;
3. consumed token/record;
4. transition condition;
5. invariant expected;
6. resulting state/phase generation;
7. invariant observed;
8. recovery or deferred-validation state;
9. semantic object mutation;
10. final consumer.

Identify the first invalid transition explicitly.

## Structural metadata and semantic-object trace

Bind metadata to parser state:

- raw and decoded lengths/counts/offsets;
- arithmetic/selection result;
- allocation/view/region identity;
- parent/child object relationship;
- duplicate-selection rule;
- cross-record ID mapping;
- semantic object identity and generation;
- final consumer.

Metadata mismatch alone is not a security result.

## Error-recovery and deferred-validation trace

Capture:

- originating error;
- recovery state and resynchronization target;
- bytes/tokens skipped or retained;
- partial object identity;
- incomplete/untrusted flags;
- deferred-validation pass;
- validation generation;
- whether the consumer observes the incomplete/stale state.

A warning that remains quarantined is a control, not a vulnerability.

## Nested parser and cross-record trace

For nested parsers record parent artifact, child slice/view identity, decompression/remapping generation, ownership, child parser instance, and returned semantic object.

For references record source record, destination record, resolution generation, duplicate policy, cycle state, and final linked object.

## Downstream consumer and bounded-effect trace

Record:

- semantic object identity/generation;
- parser phase/state generation that produced it;
- downstream consumer identity;
- invariant expected by the consumer;
- effective semantic capability;
- bounded result;
- receipt/result.

Use mock renderers, inert interpreters, read-only object inspectors, or bounded reversible synthetic state only.

## Controlled validation

Use deterministic fixtures:

- synthetic in-memory files/records;
- fixed parser configuration;
- explicit phase/state tracing;
- controlled recovery hooks;
- mock linkers/resolvers;
- generation-tagged parent/child views;
- read-only semantic consumers.

Recommended sequence:

1. establish valid positive control;
2. establish hard-rejection negative control;
3. change one phase/state variable;
4. observe first invalid transition;
5. bind resulting semantic object to final consumer;
6. apply minimal validation/order fix;
7. replay identical fixture and collect receipts.

## False-positive controls

Eliminate:

- harness failures before parser entry;
- a minimized fixture taking a different path;
- instrumentation-created state;
- incorrect format model;
- documented duplicate semantics;
- recovery that remains safely quarantined;
- later safe object reconstruction;
- independent child-parser copies;
- neighboring bounds/integer/lifetime root cause;
- receipts from another parser instance/input generation.

## Counterfactual parser controls

Change exactly one causal variable:

- recovery on/off;
- first-wins versus last-wins;
- parent metadata generation A/B;
- deferred validation before/after consumption;
- current/stale reference generation;
- same object emitted from valid/invalid transition.

Generic mutation volume or timing is not sufficient.

## Alternative explanations

Before PS4/PS5 explicitly reject:

- harness glue caused the symptom;
- minimized input changed phase reach;
- sanitizer/debug mode caused the divergence;
- format inference is wrong;
- duplicate behavior is intended;
- consumer honors incomplete flags;
- later validation rebuilds safely;
- nested parser owns a valid copy;
- bounds/integer/lifetime defect fully explains effect;
- receipt is from another parser instance or input generation.

Any unresolved material alternative caps evidence at PS2.

## Evidence capture

Capture one reconstructable tuple:

`input artifact + input generation + parser instance + configuration/version + phase + state generation + transition identity + token/record identity + structural metadata + semantic object identity/generation + invariant expected/observed + recovery/deferred-validation state + downstream consumer + effective semantic capability + bounded result + receipt/result`

Useful artifacts include phase traces, transition receipts, object-generation tags, recovery logs, read-only consumer output, and pre/post-remediation replay.

## Evidence promotion and ceiling

### PS0 — Surface mapped

Parser phases, states, metadata, recovery paths, nested parsers, references, and consumers are known.

### PS1 — State divergence observed

A repeatable state/invariant/recovery divergence exists without final semantic acceptance.

### PS2 — Controlled transition-policy mismatch

A deterministic fixture proves a transition, validation-order, recovery, phase, or deferred-validation invariant can be violated.

### PS3 — Inert inconsistent semantic acceptance

A read-only/inert downstream consumer accepts a semantic object produced under the wrong parser state, phase, generation, or validation status.

### PS4 — Bounded reversible semantic effect

A synthetic marker, read-only result, or reversible owner-controlled semantic transition is tied to the exact input/parser/state/transition/object/consumer tuple.

### PS5 — Regression-verified causal parser proof

PS4 plus complete provenance, first-invalid-transition trace, recovery/deferred-validation state, semantic-object lineage, meaningful counterfactuals, eliminated alternatives, receipt/result binding, and remediation replay.

Evidence ceiling rules:

- malformed input or phase reach: PS0 maximum;
- divergence without final acceptance: PS1 maximum;
- controlled mismatch without consumer: PS2 maximum;
- inert semantic acceptance: PS3 maximum;
- bounded causal semantic effect: PS4 maximum;
- only full proof plus regression reaches PS5.

## Remediation checks

Verify the causal fix:

1. replay exact pre-fix fixture;
2. require the first invalid transition to be rejected or normalized;
3. preserve intended valid parsing;
4. verify recovery flags remain attached until validation;
5. bind deferred validation before consumer use;
6. revalidate nested/cross-record generations;
7. confirm semantic object lineage after repair;
8. collect deterministic before/after receipts.

Prefer the smallest fix restoring the intended state-machine invariant.

## Safety boundary

Only use local/owned/sandboxed/explicitly authorized fixtures. Stop if validation requires destructive payloads, uncontrolled exploitation, persistence, credential access, malware, evasion, or unauthorized targets.
