# Protocol State Machine Operator Runbook

Use this runbook only for local, owned, sandboxed, benchmark/CTF, simulated, or explicitly authorized endpoints. Keep traffic bounded and state resettable. Use synthetic peers, loopback/mock transports, fake ledgers, inert consumers, and reversible owner-controlled effects.

## Attack surface

Map:

- peer identity and authenticated principal;
- role and role generation;
- connection identity/generation;
- session identity/generation;
- stream/channel/transaction identity and generation;
- protocol version and feature-negotiation generation;
- message/event families and message identity/generation;
- transition guards;
- replay/retry/idempotency state;
- timeout/cancellation/reset/reconnect transitions;
- commit points and terminal states;
- background completions and downstream consumers/actions.

## Hypothesis matrix

| Hypothesis | Safe oracle | Control |
| --- | --- | --- |
| stale session message survives reconnect | mock endpoint emits an inert synthetic receipt when generation N is accepted by N+1 | bind request to current session generation and require stale rejection |
| retry duplicates semantic commit | fake transaction ledger counts bounded synthetic commits | generation-bound idempotency makes repeated attempt produce one commit |
| old role authority survives role transition | read-only consumer records which role generation authorized synthetic action | current-role guard rejects stale role generation |
| late completion crosses timeout/reset generation | mock completion router emits structured inert result | old operation generation is fenced after cancellation |

## Peer/session/role-generation trace

Record:

- peer identity;
- authenticated principal;
- role and role generation;
- connection identity/generation;
- session identity/generation;
- stream/transaction identity/generation;
- protocol version/feature generation;
- message identity/generation;
- retry/cancellation/reset/reconnect generations.

Reused textual IDs do not prove continuity. Explicitly record which generations are authoritative at each transition.

## Transition-guard and authenticated-context trace

For every relevant message/event capture:

1. current state;
2. transition identity;
3. message/event identity and generation;
4. transition guard;
5. authenticated context;
6. authorization context;
7. negotiated protocol/feature generation;
8. next state;
9. side effect;
10. downstream consumer/action.

The test must identify the first illegal or stale transition, not only the final response.

## Replay/retry/idempotency trace

Capture:

- logical operation identity;
- request/message ID;
- retry attempt/generation;
- replay token or idempotency key;
- duplicate suppression state;
- response cache generation;
- pre-commit state;
- commit generation;
- final effect count;
- receipt/result.

A duplicate request is not automatically a duplicate effect, and a retry is not automatically idempotent.

## Timeout/cancellation/reset/reconnect trace

Capture:

- timeout generation;
- cancellation generation;
- targeted operation;
- local state transition;
- remote state assumptions;
- reset/reconnect generation;
- replacement session/stream/transaction generation;
- cleanup/revocation completion;
- background completion generation;
- late completion routing.

Timeout does not imply rollback. Reset does not imply revocation. Reconnect does not imply session continuity.

## Commit/terminal-state/downstream-action trace

Separate:

- message acceptance;
- transition acceptance;
- acknowledgment;
- semantic commit;
- downstream action;
- terminal protocol state;
- cleanup/revocation completion.

Record the exact final consumer/action, effective protocol capability, bounded result, and receipt/result.

## Controlled validation

Use deterministic benign fixtures:

- synthetic peers and principals;
- loopback or mock endpoints;
- fixed state-machine scripts;
- fake transaction ledgers;
- generation-tagged sessions and operations;
- inert/read-only downstream consumers;
- bounded reversible markers.

Recommended sequence:

1. establish valid current-generation positive control;
2. establish stale/forbidden negative control;
3. change one state or generation variable;
4. capture first illegal transition;
5. bind the resulting state to final consumer or commit;
6. apply minimal generation/guard/idempotency fix;
7. replay the exact sequence;
8. capture deterministic before/after receipts.

## False-positive controls

Eliminate:

- protocol specification explicitly permits the sequence;
- test harness reused IDs incorrectly;
- positive control created the effect;
- response correlation is ambiguous;
- client/server state divergence is intentional;
- reconnect continuity is documented;
- at-least-once retry semantics are intended;
- role transition is advisory only;
- timeout is explicitly non-cancelling;
- completion belongs to a different logical operation;
- concurrency scheduling, rather than protocol-state legality, explains the result;
- receipt belongs to another peer/session generation.

## Counterfactual protocol controls

Hold all other fields constant and change one variable:

- current versus stale session generation;
- generation-bound versus generation-blind idempotency;
- old versus current role generation;
- old versus replacement transaction generation;
- feature generation before versus after renegotiation;
- acknowledgment before versus after semantic commit.

Generic timing or reordering is insufficient unless it controls the hypothesized transition.

## Alternative explanations

Before PST4/PST5 explicitly reject:

- allowed protocol behavior;
- identifier reuse by the harness;
- positive-control duplication;
- ambiguous request/response matching;
- documented reconnect continuity;
- intentional at-least-once semantics;
- non-authoritative role changes;
- non-cancelling timeout semantics;
- different-operation late completion;
- concurrency-race root cause;
- wrong endpoint/session receipt.

Any unresolved material alternative caps evidence at PST2.

## Evidence capture

Capture one reconstructable tuple:

`peer identity + role generation + connection generation + session generation + stream/transaction generation + protocol/feature generation + message identity/generation + transition identity/guard + authenticated/authorization context + replay/retry/cancellation generation + commit/terminal state + downstream consumer/action + effective protocol capability + bounded result + receipt/result`

Useful artifacts include state traces, generation-tagged message logs, fake-ledger entries, idempotency receipts, cancellation fences, late-completion routing records, and pre/post remediation replay.

## Evidence promotion and ceiling

### PST0 — Surface mapped

Peers, sessions, connections, streams, transactions, states, transitions, guards, negotiation, retries, lifecycle events, commits, and consumers are known.

### PST1 — State/generation divergence observed

A repeatable session, role, transition, replay, lifecycle, ownership, or negotiation divergence exists without wrong-context downstream acceptance.

### PST2 — Controlled transition-policy mismatch

A deterministic lab sequence proves a documented guard, precondition, idempotency, replay, ownership, or lifecycle invariant can be violated.

### PST3 — Inert wrong-context protocol acceptance

A mock/read-only consumer accepts a message, action, or completion under the wrong session, role, stream, transaction, retry, negotiation, or lifecycle generation.

### PST4 — Bounded reversible protocol effect

A synthetic action, inert transition, duplicate marker, read-only result, or reversible commit is causally bound to the exact protocol tuple.

### PST5 — Regression-verified causal protocol proof

PST4 plus complete generation provenance, first-illegal-transition trace, replay/retry/lifecycle state, commit/terminal semantics, meaningful counterfactuals, eliminated alternatives, receipt/result binding, and remediation replay.

Evidence ceiling rules:

- odd response/reachable handler only: PST0 maximum;
- generation divergence only: PST1 maximum;
- deterministic guard/lifecycle mismatch without final consumer: PST2 maximum;
- inert wrong-context acceptance: PST3 maximum;
- bounded causal protocol effect: PST4 maximum;
- complete causal proof plus regression only: PST5.

## Remediation checks

Replay the exact sequence and verify:

1. stale session/role/stream/transaction generations are rejected;
2. transition guards use current authenticated context;
3. retries bind idempotency to logical operation and current protocol generation;
4. duplicate suppression and commit are aligned;
5. timeout/cancellation fences late completions;
6. reset/reconnect invalidates or deliberately transfers authority;
7. terminal state is paired with required cleanup/revocation;
8. intended positive sequences continue to work;
9. deterministic receipts prove the change.

Prefer the smallest generation, guard, idempotency, lifecycle-fence, or cleanup fix that restores the protocol invariant.

## Safety boundary

Use only local/owned/sandboxed/explicitly authorized endpoints. Stop if the experiment requires uncontrolled external traffic, destructive actions, credential use, persistence, denial-of-service, malware, evasion, or unauthorized systems.
