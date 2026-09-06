---
name: stateful-protocol-fuzzing
description: "Design authorized fuzzing for network or IPC protocols whose behavior depends on message sequences, connection/session state, retries, negotiation, or role transitions. Use when single-message fuzzing cannot reach deep states or bugs require temporal ordering."
metadata:
  nolane-security-category: discovery
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Stateful Protocol Fuzzing

Model protocol fuzzing as exploration of a state machine with observable transitions. A syntactically valid packet is not enough when the vulnerability requires history.

## When to use

Use for request/response protocols, IPC/RPC, authentication flows, handshakes, multiplexed streams, retry logic, upgrade paths, or asynchronous state machines.

## Preconditions

1. The service is local/lab/owned or explicitly authorized; isolate network effects.
2. Define reset semantics so each test starts from a known state.
3. Instrument coverage or expose a state oracle when possible.
4. Bound concurrency, connection count, message rate, and resource consumption.

## Workflow

1. **Enumerate observable states.** Connection phase, negotiated mode, authentication role, transaction stage, stream state, retry counter, object lifecycle.
2. **Model message families and guards.** Which messages are legal, ignored, deferred, retried, or destructive in each state?
3. **Capture valid traces.** Record minimal successful conversations as seed sequences.
4. **Design sequence mutations.** Delete, duplicate, reorder, splice, delay, replay, cross-session mix, alter role, or mutate message content at selected positions.
5. **Define reset strategy.** Process restart, connection reset, transaction rollback, VM snapshot, fixture recreation, or explicit protocol reset.
6. **Track state coverage separately from code coverage.** A campaign can hit the same code edges in meaningfully different protocol states.
7. **Target transition boundaries.** Error-to-retry, unauthenticated-to-authenticated, open-to-closing, upgrade/downgrade, timeout/reconnect, and partial-message transitions.
8. **Minimize sequences, not just packets.** Remove messages while preserving the required state and failure.
9. **Test cross-connection assumptions.** Check whether state incorrectly leaks between clients, sessions, identities, or streams.
10. Validate any security-relevant state violation with deterministic controls.

## Evidence contract

Preserve protocol/version, target build, seed trace, minimized triggering sequence with timing assumptions, reset method, state/coverage observations, failure oracle, and negative sequence control. A crash without sequence reproducibility is not validated.

## Stop conditions

Stop when reset is unreliable, fuzzing changes shared production state, hidden nondeterminism prevents sequence replay, or the state model is too coarse to explain observed behavior.

## Output

```text
protocol + target:
state model:
seed traces:
sequence mutations:
reset method:
state/code coverage:
minimized failing sequence:
timing/concurrency assumptions:
controls:
```
