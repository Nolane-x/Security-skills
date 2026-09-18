---
name: protocol-state-machine-analysis
description: "Analyze protocol, IPC, RPC, and session implementations as explicit state machines with message guards, retries, role changes, timeouts, duplicate handling, and cross-connection state. Use for logic flaws that require a sequence rather than one malformed packet."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Protocol State Machine Analysis

Protocol security depends on allowed transitions as much as message syntax. Find states that can be skipped, replayed, reached under the wrong identity, or cleaned up inconsistently.

## When to use

Use for authentication handshakes, upgrades, transactions, multiplexed streams, connection pools, retry logic, async RPC, IPC helpers, or peer role negotiation.

## Preconditions

Exercise only local lab/owned/sandboxed or explicitly authorized endpoints with bounded traffic and resettable state.

## Workflow

1. **Define state variables.** Connection, session, identity, transaction, stream, feature negotiation, retry/error state.
2. **Enumerate message/event families.** Input packet, timeout, close/reset, retry, cancellation, reconnect, background completion.
3. **Build transition table.** Current state + event + guard → next state + side effects.
4. **Mark security invariants per state.** Which operations require authentication, ownership, transaction membership, or negotiated feature?
5. **Look for skipped transitions.** Direct access to a later-state handler or state initialized optimistically.
6. **Look for duplicate/replay semantics.** Idempotence assumptions, repeated response ids, retransmission, stale acknowledgments.
7. **Look for error/retry asymmetry.** State may be partially reset while objects/permissions survive.
8. **Look for cross-connection leakage.** Global/shared state keyed incorrectly by connection, stream, peer, or request id.
9. **Use stateful-protocol-fuzzing** to explore uncertain transitions and minimize sequences.
10. **Validate with a transition-level negative control** showing the forbidden sequence is blocked after invariant restoration.

## Evidence contract

Provide a transition table subset, minimal event/message sequence, expected versus actual state, security invariant violated, side effect, reset assumptions, and control. A weird protocol response without invariant violation is not enough.

## Causal protocol-state model

Treat every promoted protocol-state finding as one causal tuple:

`peer identity + peer role generation + connection identity/generation + session identity/generation + stream/transaction identity/generation + protocol version/feature generation + message family + message identity/generation + request/response correlation + current state + transition identity + transition guard + authenticated context + authorization context + replay/retry/cancellation generation + commit/terminal state + downstream consumer/action + effective protocol capability + bounded result + receipt/result`.

The proof must identify the first illegal, stale, or wrong-context transition and then bind that transition to the downstream state mutation, commit, or action. A reachable handler, matching message ID, odd response, or reordered packet is only an observation until the current protocol generation and guard context are reconstructed.

Preserve these distinctions explicitly:

- syntactically valid message != legal state transition;
- authenticated once != authenticated current session;
- connection identity != session identity;
- message id != operation identity;
- response correlation != causal authorization;
- duplicate request != duplicate side effect;
- retry != idempotent replay;
- acknowledgment != commit;
- timeout != rollback;
- reset != state revocation;
- reconnect != same session;
- negotiated feature != authorized feature use;
- role label != current authority;
- stream id != ownership;
- out-of-order message != forbidden transition without protocol evidence;
- weird response != invariant violation;
- terminal state != cleanup complete;
- stale background completion != current operation;
- protocol crash != protocol-state exploitability.

## Peer, connection, session, and role generations

Track independently:

- peer identity and authenticated principal;
- peer role generation;
- connection identity/generation;
- session identity/generation;
- stream/transaction identity/generation;
- protocol version/feature generation;
- message identity/generation;
- retry attempt and idempotency generation;
- timeout/cancellation generation;
- reset/reconnect generation;
- commit generation;
- terminal/cleanup generation;
- background-completion generation.

A reconnect, connection-pool reassignment, role change, stream recycle, transaction restart, renegotiation, retry, timeout, cancellation, or reset may advance one generation without advancing another. Reused textual IDs do not imply continuity of authority.

All dynamic validation stays local/owned/sandboxed or explicitly authorized, with bounded traffic, deterministic resets, synthetic peers, and inert or read-only effects.

## Transition guard and authenticated-context binding

For each suspicious transition, record:

1. current protocol state;
2. peer/session/stream/transaction generation;
3. message or event identity/generation;
4. transition identity;
5. transition guard;
6. authenticated context;
7. authorization context;
8. negotiated protocol/feature generation;
9. resulting state and side effect;
10. commit/terminal state and downstream consumer/action.

A syntactically valid message can still be illegal in the current state. Authentication from an earlier session generation cannot be treated as the authenticated context for a later session unless the protocol contract explicitly binds that continuity.

Keep authorization policy ownership with `authorization-boundary-analysis`; this skill binds the current protocol generation to the policy context that is actually consulted.

## Replay, retry, idempotency, and duplicate-effect binding

For each repeated request, replay, or retry, capture:

- logical operation identity;
- message/request ID;
- message identity/generation;
- retry attempt/generation;
- replay token or idempotency key;
- duplicate-suppression generation;
- response-cache generation;
- pre-commit state;
- semantic commit generation;
- final effect count;
- receipt/result.

Message id != operation identity. Duplicate request != duplicate side effect. Retry != idempotent replay.

The key question is whether the same logical operation is recognized across generations and whether duplicate suppression is bound to the same peer/session/transaction context as the final commit. A repeated cached response can hide a duplicate commit just as a repeated request can be safely suppressed.

## Timeout, cancellation, reset, reconnect, and late-completion binding

Treat lifecycle events as explicit generation boundaries.

Record:

- targeted operation identity;
- timeout generation;
- cancellation generation;
- local protocol state before and after cancellation;
- remote-state assumptions;
- reset/reconnect generation;
- stream/transaction replacement generation;
- revocation/cleanup completion;
- background completion generation;
- routing decision for late acknowledgments or completions.

Timeout != rollback. Reset != state revocation. Reconnect != same session. Stale background completion != current operation.

A late completion becomes protocol-state evidence only if it is bound to the old operation generation and then demonstrably accepted by a new session, stream, transaction, or role context.

## Commit, terminal-state, and downstream-action binding

Separate each stage:

`message acceptance -> transition acceptance -> acknowledgment -> semantic commit -> downstream action -> terminal state -> cleanup/revocation completion`.

Acknowledgment != commit unless the protocol contract explicitly defines the acknowledgment as the commit point. Terminal state != cleanup complete.

For each promoted finding record the downstream consumer/action, effective protocol capability actually demonstrated, bounded result, and receipt/result. Prefer synthetic actions, fake transaction ledgers, inert state markers, read-only results, or reversible owner-controlled commits.

Do not infer arbitrary authorization, broad compromise, persistence, or external impact from a narrower protocol-state capability.

## Protocol-state evidence ladder

Use PST0–PST5 exactly:

- **PST0 — Surface mapped.** Peers, sessions, connections, streams, transactions, states, transitions, guards, negotiations, retries, lifecycle events, commits, and downstream consumers are identified.
- **PST1 — State/generation divergence observed.** A repeatable session, role, transition, replay, lifecycle, ownership, or negotiation divergence exists, but wrong-context downstream acceptance is not shown.
- **PST2 — Controlled transition-policy mismatch.** A deterministic lab sequence proves a documented guard, state precondition, idempotency rule, replay rule, ownership rule, or lifecycle invariant can be violated.
- **PST3 — Inert wrong-context protocol acceptance.** A mock/read-only downstream consumer accepts a message, action, or completion under the wrong session, role, stream, transaction, retry, negotiation, or lifecycle generation.
- **PST4 — Bounded reversible protocol effect.** An owner-controlled synthetic action, inert state transition, duplicate marker, read-only result, or reversible commit is causally bound to the exact peer/session/state/message/transition/consumer tuple.
- **PST5 — Regression-verified causal protocol proof.** PST4 plus complete peer/session/role/negotiation provenance, first-illegal-transition trace, replay/retry/lifecycle state, commit/terminal semantics, meaningful counterfactuals, eliminated alternative explanations, receipt/result binding, and remediation replay.

Weird responses, protocol crashes, out-of-order messages, duplicate IDs, timeouts, reconnects, or synthetic markers cannot skip missing causal bindings.

## Counterfactual protocol controls

Hold all semantic inputs constant and change one causal variable:

- same message under current versus stale session generation;
- same retry with generation-bound versus generation-blind idempotency;
- same operation under old versus current role generation;
- same completion routed to old versus replacement transaction generation;
- same feature before versus after renegotiation;
- same acknowledgment before versus after the semantic commit point.

A generic delay or message reorder is not a sufficient counterfactual unless it changes the exact lifecycle or transition edge under test.

## Alternative explanations

Before PST4 or PST5, test and reject:

- the protocol specification explicitly permits the sequence;
- the harness reused message or stream identifiers incorrectly;
- the positive control created the duplicate effect;
- request/response correlation is ambiguous;
- client and server state models intentionally differ;
- reconnect continuity is specified behavior;
- retry delivery is intentionally at-least-once;
- role changes are advisory rather than authoritative;
- timeout is explicitly non-cancelling;
- the late completion belongs to a different logical operation;
- a concurrency race fully explains the result without a protocol-state invariant violation;
- the receipt belongs to another endpoint/session generation.

Any unresolved material alternative caps evidence at PST2.

## Evidence ceiling

Apply the narrowest supported level:

- mapped protocol surface or odd response only: PST0 maximum;
- state/generation divergence without downstream acceptance: PST1 maximum;
- deterministic guard/lifecycle/idempotency mismatch without final consumer: PST2 maximum;
- inert/read-only wrong-context acceptance: PST3 maximum;
- bounded causally bound protocol effect: PST4 maximum;
- only complete generation provenance, first-illegal-transition proof, lifecycle trace, counterfactuals, receipts, and remediation replay reaches PST5.

Do not promote protocol crashes, retransmissions, duplicate IDs, handler reachability, timeouts, or successful handshakes into stronger protocol-state claims without the missing causal bindings.

## Stop conditions

Stop when the sequence is explicitly permitted by protocol specification and safe in context, reset cannot be made deterministic, or testing risks external/shared systems.

## Output

```text
protocol/session:
state variables:
relevant transitions:
security invariant:
minimal violating sequence:
actual state/effect:
reset assumptions:
negative control:
related fuzzing strategy:
```
