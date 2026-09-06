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
