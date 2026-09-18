---
name: concurrency-race-analysis
description: "Analyze interleavings, shared-state invariants, atomicity, lock coverage, cancellation, publication, teardown, and time-of-check/time-of-use behavior in authorized code. Use for race conditions, double actions, stale state, UAF races, authorization TOCTOU, or non-deterministic corruption."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Concurrency and Race Analysis

A race is security-relevant when an unsafe interleaving violates an invariant that sequential executions preserve. Describe the smallest happens-before relationship needed to prevent it.

## When to use

Use when a failure is timing-sensitive, thread/task dependent, cancellation-related, or involves separately checked and used shared state.

## Preconditions

Only stress authorized local/owned/sandboxed systems. Record thread/task model, scheduler/runtime, synchronization primitives, and whether instrumentation changes timing substantially.

## Workflow

1. **Name shared state and invariant.** Object lifetime, authorization state, uniqueness, queue membership, refcount, transaction phase, file/path identity.
2. **List actors.** Threads, processes, callbacks, signals, async tasks, interrupts, workers, external state changers.
3. **Map synchronization.** Locks, atomics/orderings, fences, channels, event loops, transactions, refcounts, epochs.
4. **Write candidate interleaving.** A1 → B1 → A2 with the exact gap that breaks the invariant.
5. **Distinguish data race from higher-level race.** Atomic memory accesses can still form an unsafe check/use sequence.
6. **Inspect cancellation/error teardown.** Concurrent abort and completion paths often duplicate release or action.
7. **Check publication.** Is a partially initialized or already-retired object visible to another actor?
8. **Amplify deterministically where possible.** Test hooks, barriers, controlled delays, repeated lab runs, or schedule tracing rather than uncontrolled production load.
9. **Run near-neighbor controls.** Add the missing ordering or disable one actor and confirm the failure disappears.
10. **State the minimal synchronization/invariant fix**, not merely “add a lock.”

## Evidence contract

Provide the shared invariant, actors, candidate interleaving, synchronization gap, reproducibility strategy, observed violation, and control. ThreadSanitizer output helps but does not replace higher-level invariant reasoning.

## Causal concurrency model

Treat every promoted concurrency finding as one causal tuple:

`shared invariant + shared state identity + state generation + actor identity set + operation generation set + scheduler/executor identity + synchronization epoch + check observation + interfering transition + use/commit transition + happens-before relation + cancellation generation + teardown generation + final consumer + effective concurrent capability + bounded result + receipt/result`.

A schedule is evidence only when the same logical shared state and the same relevant generations are bound across the observations. A timestamp ordering, log ordering, or “happened around the same time” description is not a happens-before proof.

The model must identify the minimal missing or ineffective ordering edge. “Add a lock” is not a causal explanation unless the protected state, actor operations, entry/exit epochs, and final consumer are named.

## Shared invariant and state generations

Write the invariant as a statement that can be true or false for one logical shared-state generation.

Record:

- shared state identity;
- state generation before each actor operation;
- mutation/commit generation;
- invalidation or retirement generation if relevant;
- which fields jointly form the invariant;
- which actor may legitimately advance the generation;
- which observations become stale after a generation change.

For a check/use race, bind the check observation to the exact state generation it observed and bind the later use or commit to the generation actually consumed.

## Actor, scheduler, and operation generations

Assign stable synthetic identities to every participating actor:

- thread/task/process/callback/worker identity;
- operation generation or request generation;
- scheduler/executor/queue identity;
- retry/attempt identity;
- callback/completion identity;
- cancellation generation;
- teardown/shutdown generation.

Do not collapse “same function” into “same actor.” Two invocations of the same code path can have different operation generations and different authority to commit.

## Synchronization and happens-before binding

Map every relevant synchronization edge:

- lock acquire/release;
- atomic read/modify/write and memory ordering;
- fences;
- channels/events;
- barriers;
- queue handoff;
- transaction boundaries;
- epochs/generation fences;
- cancellation acknowledgements;
- completion joins.

State the required happens-before relation and the observed relation separately. Lock present != protected operation. Atomic access != atomic invariant.

A data race report can reveal unsynchronized memory access, but data race != higher-level race: a program may have no low-level data race and still violate a multi-step invariant.

## Check/use, publication, and commit binding

For check/use sequences, record:

1. the check observation and state generation;
2. the actor that can invalidate that observation;
3. the interfering transition;
4. whether revalidation occurs;
5. the use/commit point;
6. the final consumer and bounded result.

TOCTOU window != demonstrated stale decision use. The final consumer must prove that a decision derived from an older generation was actually accepted after the interfering transition.

For publication, separate object initialization, publication, visibility, reader acquisition, and final consumption. Thread/task overlap != harmful interleaving. Queue order != execution order unless the runtime contract guarantees that ordering.

## Cancellation, retry, and teardown binding

Cancellation requested != work revoked. Record:

- cancellation request generation;
- acknowledgement/commit barrier;
- work-item generation;
- retry/attempt generation;
- teardown generation;
- whether the final consumer checks the current lifecycle epoch;
- whether a duplicate completion is idempotent by contract.

Retry overlap != duplicate effect. A duplicated final effect must be demonstrated at the bounded final consumer or inert ledger, not inferred from overlapping attempts.

## Final consumer and bounded effect binding

Identify the exact final consumer that can make the race security-relevant.

Record:

- final consumer identity;
- required current state/operation generation;
- actor operation presented;
- synchronization/revalidation decision;
- effective concurrent capability;
- bounded result;
- correlated receipt/result.

Prefer inert ledgers, read-only synthetic consumers, marker-only transitions, mock queues, and reversible owner-controlled state. Arbitrary code execution or destructive corruption is not required.

## Concurrency evidence ladder

### CR0 — Concurrency surface mapped

Actors, shared state, synchronization primitives, schedulers/executors, lifecycle transitions, and candidate invariants are mapped. No race is claimed.

### CR1 — Ordering divergence observed

A repeatable ordering, visibility, generation, cancellation, or revalidation divergence is observed, but no forbidden final transition is established.

### CR2 — Controlled synchronization-policy mismatch

A deterministic barrier or scheduler-hook experiment demonstrates that the required ordering, atomicity, serialization, or revalidation contract can be violated by one named interleaving.

### CR3 — Inert wrong-order acceptance

The final synthetic or read-only consumer accepts stale, duplicated, partially initialized, or otherwise wrong-order state under the controlled interleaving.

### CR4 — Bounded reversible concurrent effect

A bounded reversible owner-controlled marker, synthetic state transition, duplicate inert action, or read-only result is causally bound to the exact actors, state generation, interleaving, synchronization epoch, and final consumer.

### CR5 — Regression-verified causal concurrency proof

CR4 plus complete actor/state/generation provenance, scheduler/executor identity, synchronization and happens-before trace, check/use or publication/commit ordering, cancellation/retry/teardown state, final consumer identity, meaningful counterfactual schedules, eliminated alternative explanations, receipt/result binding, and remediation regression.

Sanitizer race report != complete causal concurrency proof. Crash != exploitability. Neither can skip missing causal bindings.

## Counterfactual schedules

Change one scheduling or synchronization variable while holding the logical state and test fixture constant.

Useful counterfactuals include:

- same actors and state, barrier present versus absent;
- same check and use, generation unchanged versus deliberately advanced;
- same competing completions, single-effect guard present versus absent;
- same cancellation and completion, completion before versus after cancellation acknowledgement;
- same publisher/reader, initialized-before-publication versus publication-before-final-initialization;
- same retry pair, idempotency/commit epoch enforced versus omitted.

Timing correlation != causal schedule. If a result disappears only because a generic sleep changes timing, keep the claim below CR2 until the exact causal edge is controlled.

## Alternative explanations

Before CR4 or CR5, explicitly test and reject plausible alternatives:

- the receipt came from the positive-control path;
- actors touched different logical state generations;
- instrumentation changed the scheduler enough to create an artificial path;
- queue ordering was assumed but not guaranteed;
- retry completion was idempotent and therefore not a duplicate effect;
- the cancellation contract intentionally allows late completion;
- a lifetime violation, not ordering, explains the result;
- authorization changed independently of the interleaving;
- a stale log from another run created false ordering;
- the marker was emitted before the hypothesized interference.

Unresolved alternatives cap evidence at CR2.

## Evidence ceiling

Evidence never rises above the strongest directly demonstrated causal binding.

- thread/task overlap alone stays at CR0 or CR1;
- a sanitizer or race-detector report stays at CR1 unless higher-level invariant causality is proven;
- a controlled bad interleaving without final-consumer acceptance stays at CR2;
- an inert wrong-order acceptance can reach CR3;
- a bounded reversible effect with exact actor/state/interleaving binding can reach CR4;
- CR5 additionally requires full provenance, counterfactual schedules, alternative-explanation elimination, receipt/result binding, and remediation regression.

The profile is local/owned/sandboxed and explicitly authorized. Do not use uncontrolled production stress, destructive corruption, denial-of-service, arbitrary code execution, privilege escalation, persistence, malware, evasion, or unauthorized targets as proof requirements.

## Stop conditions

Stop if the interleaving is impossible under the documented memory/order model, the only reproducer relies on instrumentation-only timing, stress would affect systems outside scope, or the suspected state is not actually shared.

## Output

```text
shared invariant:
shared state identity/generation:
actors and operation generations:
scheduler/executor:
existing synchronization:
required happens-before:
minimal bad interleaving:
check/use or publication/commit trace:
cancellation/retry/teardown state:
final consumer:
effective concurrent capability:
bounded result:
receipt/result:
counterfactual schedule:
alternative explanations:
minimal ordering needed:
related lifetime/auth implications:
```
