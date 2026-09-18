# Concurrency Race Operator Runbook

Use this runbook only for local, owned, sandboxed, benchmark/CTF, simulated, or explicitly authorized targets. The objective is causal ordering evidence with deterministic, bounded, benign effects—not uncontrolled stress or impact escalation.

## Attack surface

Map the complete concurrency surface before testing:

- logical shared-state identities and their generations;
- actors: threads, tasks, processes, callbacks, workers, interrupts, external changers;
- scheduler/executor/queue identities;
- locks, atomics, fences, channels, barriers, transactions, epochs, generation checks, joins;
- check/use pairs and authorization/state observations;
- publication and initialization boundaries;
- retries, duplicate completions, timeout paths, cancellation, teardown, shutdown;
- final consumers that commit state or produce externally visible bounded results.

Pin build/runtime configuration, scheduler mode, fixture identity, and all test-controlled generation values.

## Hypothesis matrix

Turn each suspected race into a falsifiable ordering claim.

| Hypothesis | Safe proof signal | Control |
| --- | --- | --- |
| check result can be consumed after its generation changes | inert synthetic consumer records old check generation and new use generation | same schedule with mandatory revalidation rejects |
| two completions can commit one logical effect twice | controlled fake ledger records two commits for one operation generation | single-effect fence permits exactly one commit |
| cancelled work can commit after lifecycle epoch advances | read-only synthetic sink records stale work generation | acknowledged cancellation epoch blocks commit |
| reader can consume partially initialized publication | synthetic structured marker exposes missing initialized field | publish-after-initialize order returns complete marker |

Do not write “race exists” from flakiness alone. Name the shared invariant, actors, exact interleaving, required ordering edge, final consumer, and bounded result.

## Shared invariant and state-generation trace

For every scenario, record:

- logical shared-state identity;
- state generation before and after each actor step;
- fields jointly forming the invariant;
- authoritative mutation/commit operation;
- invalidation/retirement generation if relevant;
- whether each actor observed current or stale generation.

The same numeric address, request ID, queue slot, or object handle does not by itself prove the same logical state generation.

## Actor and operation-generation trace

Assign each participant:

- actor identity;
- thread/task/process/callback/worker class;
- operation/request generation;
- retry/attempt generation;
- scheduler/executor/queue identity;
- callback/completion identity;
- lifecycle generation.

Two invocations of the same function are distinct actor-operation generations unless the target contract explicitly treats them as the same operation.

## Synchronization and happens-before trace

Record all relevant synchronization primitives and the exact edge each is supposed to provide:

- lock acquire/release;
- atomic operations and memory ordering;
- fences;
- channels/events;
- condition variables;
- barriers;
- queue handoffs;
- transaction boundaries;
- epoch/generation fences;
- joins and cancellation acknowledgements.

Write the required happens-before relation and observed relation separately. A lock that does not cover both sides of the invariant is not sufficient evidence of serialization.

## Check/use and commit-point trace

For check/use or decision/commit races, record:

1. actor and operation generation performing the check;
2. shared-state generation observed;
3. interfering actor transition;
4. generation after interference;
5. revalidation, if any;
6. use or commit point;
7. final consumer;
8. bounded result and receipt/result.

A TOCTOU-shaped code pattern is only a hypothesis until the old decision is proven to be consumed after the authoritative state changes.

## Queue, executor, and publication trace

For queued or published work, record:

- queue/executor identity;
- enqueue generation;
- dequeue/dispatch generation;
- ordering guarantees actually provided by the runtime;
- object initialization state;
- publication event;
- reader acquisition;
- final consumption.

Do not infer execution order from enqueue order unless the executor contract guarantees it. For publication races, distinguish “visible reference” from “fully initialized consumable state.”

## Cancellation, retry, and teardown trace

Trace every lifecycle transition that can race with in-flight work:

- cancellation request;
- cancellation acknowledgement;
- timeout;
- retry creation;
- prior-attempt completion;
- teardown/shutdown;
- resource invalidation;
- callback completion;
- final commit.

Record the lifecycle epoch each path carries and exactly where stale work is rejected—or where rejection is absent.

## Final consumer and single-effect trace

Identify the final consumer that can convert a scheduling mismatch into a meaningful result.

Record:

- final consumer identity;
- required current state/operation generation;
- effective concurrent capability;
- whether action is idempotent by contract;
- single-effect or uniqueness invariant;
- bounded result;
- receipt/result correlation.

Use a fake ledger, inert counter, read-only object, synthetic marker, or bounded reversible owner-controlled transition. Never require destructive corruption or arbitrary code execution.

## Deterministic schedule control

Prefer deterministic control over probability amplification:

- explicit barriers;
- test-only scheduler hooks;
- event/latch synchronization;
- controlled executor suspension;
- deterministic fake clocks;
- mock queue release points;
- generation-tagged state transitions.

A useful experiment fixes all semantic inputs and changes only one scheduling edge. Repeated sleeps or high-load loops can support CR1 observation but are weak causal proof.

## Controlled validation

Use local and bounded fixtures such as:

- synthetic two-actor check/use harnesses;
- controlled fake ledgers for single-effect invariants;
- mock queues and executors;
- deterministic cancellation/completion barriers;
- synthetic publication objects with generation-tagged fields;
- read-only consumers that return only structured markers.

Recommended sequence:

1. establish positive current-order behavior;
2. establish negative denied/stale behavior;
3. force one exact interleaving;
4. observe the final inert/read-only consumer;
5. add the minimal ordering/revalidation fix;
6. replay the exact same schedule;
7. capture deterministic receipts.

## False-positive controls

Always eliminate:

- stale logs from another test run;
- actors operating on different logical state generations;
- instrumentation-created ordering not present in the target;
- scheduler perturbation from race detectors or tracing;
- intended idempotent duplicate completion;
- documented late completion after cancellation;
- queue ordering assumptions not guaranteed by the runtime;
- a lifetime bug whose consequence is independent of the race;
- independent authorization/configuration changes;
- marker emission before the hypothesized interference;
- benign overlap with no invariant violation.

## Counterfactual schedules

Change exactly one causal schedule variable while holding semantic state constant.

Examples:

- same actors/state, required barrier present versus removed;
- same check/use, generation unchanged versus advanced between operations;
- same duplicate completion pair, single-effect commit guard enabled versus disabled;
- same cancellation/completion, completion before versus after cancellation acknowledgement;
- same publisher/reader, initialize-before-publish versus publish-before-final-initialize;
- same retry overlap, current attempt generation checked versus ignored.

A generic timing delay is not a sufficient counterfactual unless it directly controls the hypothesized ordering edge.

## Alternative explanations

Before CR4 or CR5, explicitly test and reject:

- the positive-control path generated the receipt;
- actors touched different state generations;
- a race detector or debugger created the bad schedule;
- queue semantics were mischaracterized;
- duplicate results were contractually idempotent;
- cancellation intentionally permits late completion;
- stale lifetime authority, not ordering, caused the result;
- authorization changed independently;
- another actor emitted the bounded marker;
- the marker was emitted before the interfering transition;
- nondeterministic fixture initialization caused the observation.

Any material unresolved alternative caps evidence at CR2.

## Evidence capture

Capture one reconstructable causal tuple:

`shared invariant + shared state identity/generation + actor identities + operation generations + scheduler/executor + synchronization epoch + check observation + interfering transition + use/commit + happens-before relation + cancellation/retry/teardown generation + final consumer + effective concurrent capability + bounded result + receipt/result`

Useful artifacts include:

- generation-tagged deterministic logs;
- barrier state;
- lock/atomic/fence/transaction event traces;
- queue dispatch receipts;
- cancellation acknowledgement receipts;
- fake-ledger entries;
- read-only structured consumer output;
- before/after remediation replay on the same controlled schedule.

## Evidence promotion and ceiling

Use the CR ladder exactly:

### CR0 — Surface mapped

Actors, shared state, synchronization, scheduler/executor, lifecycle transitions, and invariants are known. No race proven.

### CR1 — Ordering divergence observed

A repeatable scheduling, visibility, generation, or lifecycle divergence exists, but final wrong-order acceptance is not shown.

### CR2 — Controlled synchronization-policy mismatch

A deterministic schedule proves the documented ordering, atomicity, serialization, or revalidation contract can be violated.

### CR3 — Inert wrong-order acceptance

The final inert/read-only consumer accepts state under the wrong ordering or generation.

### CR4 — Bounded reversible concurrent effect

A bounded reversible owner-controlled marker, duplicate inert action, synthetic transition, or read-only result is tied to the exact actor/state/interleaving/synchronization tuple.

### CR5 — Regression-verified causal concurrency proof

CR4 plus complete actor/state/generation provenance, scheduler/executor identity, synchronization and happens-before trace, check/use or publication/commit ordering, cancellation/retry/teardown state, final consumer identity, counterfactual schedules, eliminated alternatives, receipt/result binding, and remediation replay.

Evidence ceiling rules:

- flaky timing correlation: CR1 maximum;
- race-detector report alone: CR1 maximum;
- deterministic bad schedule without final consumer: CR2 maximum;
- inert final acceptance: CR3 maximum;
- bounded causally bound effect: CR4 maximum;
- only complete proof plus regression reaches CR5.

## Remediation checks

Verify the causal fix, not merely symptom disappearance.

For each case:

1. replay the exact pre-fix deterministic schedule;
2. require the bad bounded result to disappear;
3. require intended positive behavior to remain;
4. record the new happens-before/revalidation/single-effect invariant;
5. verify cancellation/retry/teardown generations converge;
6. confirm no neighboring deadlock/livelock or starvation regression;
7. preserve deterministic receipt/result evidence.

Minimal fixes may include a narrower lock scope, generation revalidation, atomic state machine transition, single-effect commit primitive, publication barrier, cancellation acknowledgement fence, or operation-generation check. Choose the smallest fix that restores the stated invariant.

## Safety boundary

Only use local/owned/sandboxed/explicitly authorized environments and synthetic/mock/inert/read-only fixtures. Stop if validation would require uncontrolled production stress, denial-of-service, destructive state corruption, arbitrary code execution, privilege escalation, persistence, credential access, malware, evasion, or an unauthorized target.

## Quick operator template

```text
shared invariant:
shared state identity/generation:
actors + operation generations:
scheduler/executor:
required happens-before:
observed happens-before:
minimal controlled interleaving:
check/use or publication/commit trace:
cancellation/retry/teardown generation:
final consumer:
single-effect invariant:
effective concurrent capability:
bounded result:
receipt/result:
counterfactual schedule:
alternative explanations rejected:
evidence level:
evidence ceiling:
minimal remediation ordering:
regression replay:
```
