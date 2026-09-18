# Wave 10 Profile #29 — Protocol State Machine Causal Depth Design

**Date:** 2026-09-18  
**Base authority:** `main@d2d9275b4bcc2ebb2f1a7db7730f4c576ebdf540`  
**Canonical skill:** `protocol-state-machine-analysis`

## Purpose

Promote `protocol-state-machine-analysis` into the twenty-ninth CI-enforced operator-depth profile without changing routing, graph, packs, benchmark authority, agent-eval authority, superiority-court authority, or workflow semantics.

The current skill already models state variables, message/event families, transitions, duplicate/replay semantics, retries, cross-connection leakage, and negative controls. The missing contract is causal identity across protocol generations: which peer/session/connection/stream/transaction/message generation is active, which transition guard was applied, which authenticated context authorized the transition, which retry/reconnect/reset generation survived, and which downstream action or commit consumed the state.

## Causal model

Every promoted finding must bind one reconstructable tuple:

`peer identity + peer role generation + connection identity/generation + session identity/generation + stream/transaction identity/generation + protocol version/feature generation + message family + message identity/generation + request/response correlation + current state + transition identity + transition guard + authenticated context + authorization context + replay/retry/cancellation generation + commit/terminal state + downstream consumer/action + effective protocol capability + bounded result + receipt/result`

The proof must identify the first illegal or stale transition and show why the resulting state survives into a downstream consumer, commit point, or terminal action.

## Required distinctions

Freeze these non-equivalences:

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

## Identity and generation model

Track independently:

- peer identity and authenticated principal;
- peer role and role generation;
- connection identity and generation;
- session identity and generation;
- stream/channel/request scope;
- transaction identity and generation;
- protocol version/negotiation generation;
- feature/capability negotiation generation;
- message/request identity and generation;
- retry attempt and idempotency generation;
- cancellation/timeout generation;
- reconnect/reset generation;
- commit generation;
- terminal/cleanup generation;
- background completion generation.

A reconnect, role change, renegotiation, retry, timeout, reset, stream recycle, transaction restart, or connection-pool reassignment can invalidate prior authority even when textual IDs or payloads repeat.

## Transition and guard binding

For each suspicious path record:

1. current protocol state;
2. peer/session/stream/transaction generation;
3. incoming event or message identity;
4. transition identity;
5. transition guard;
6. authenticated/authorized context consulted;
7. next protocol state;
8. side effect or object mutation;
9. commit/terminal state;
10. downstream action and receipt/result.

A handler being reachable does not prove a transition is legal. A response bearing a matching ID does not prove it belongs to the current operation generation.

## Authentication, role, and negotiated-context binding

Authentication and negotiation are stateful. Bind every privileged transition to the current:

- authenticated peer/principal;
- session generation;
- role generation;
- negotiated protocol version;
- feature/capability generation;
- stream/transaction ownership;
- policy or authorization context.

An identity or feature established in generation N must not silently authorize generation N+1 unless the protocol contract explicitly allows continuity.

## Replay, retry, idempotency, and duplicate-effect binding

For repeated messages or retries, record:

- logical operation identity;
- message/request ID;
- retry attempt/generation;
- idempotency key or replay token;
- commit state;
- duplicate suppression state;
- response cache generation;
- final effect count;
- receipt/result.

Duplicate request != duplicate side effect. Retry != idempotent replay. A repeated response or message ID is not enough; evidence must show whether the same logical operation is replayed, duplicated, or newly authorized.

## Timeout, cancellation, reset, reconnect, and late completion

Model each lifecycle event as a generation boundary. Record:

- timeout/cancellation generation;
- which in-flight operation it targets;
- local state transition;
- remote state assumptions;
- revocation/cleanup semantics;
- reconnect/reset generation;
- whether stale acknowledgments or completions remain routable;
- whether a late completion reaches a new session/transaction/stream.

Timeout != rollback. Reset != state revocation. Terminal state != cleanup complete.

## Commit, terminal state, and downstream action

Separate:

- message acceptance;
- transition acceptance;
- acknowledgment;
- semantic commit;
- durable or externally visible action;
- terminal protocol state;
- cleanup/revocation completion.

An acknowledgment != commit unless the protocol explicitly defines it so. The profile must bind the strongest demonstrated effect only.

## Evidence ladder

- **PST0 — Surface mapped:** peers, sessions, connections, streams, transactions, states, transitions, guards, negotiation, retries, lifecycle events, commits, and consumers are identified.
- **PST1 — State/generation divergence observed:** a repeatable session, role, transition, replay, lifecycle, or ownership divergence exists, but wrong-context downstream acceptance is not shown.
- **PST2 — Controlled transition-policy mismatch:** a deterministic lab sequence proves a documented guard, state precondition, idempotency rule, replay rule, ownership rule, or lifecycle invariant can be violated.
- **PST3 — Inert wrong-context protocol acceptance:** a mock/read-only downstream consumer accepts a message, semantic action, or completion under the wrong session, role, stream, transaction, retry, or lifecycle generation.
- **PST4 — Bounded reversible protocol effect:** an owner-controlled synthetic action, inert state transition, duplicate marker, read-only result, or reversible commit is causally bound to the exact peer/session/state/message/transition/consumer tuple.
- **PST5 — Regression-verified causal protocol proof:** PST4 plus complete peer/session/role/negotiation provenance, first-illegal-transition trace, replay/retry/lifecycle state, commit/terminal semantics, meaningful counterfactuals, eliminated alternatives, receipt/result binding, and remediation replay.

Weird responses, crashes, message reordering, duplicate IDs, timeouts, or synthetic markers cannot skip missing causal bindings.

## Deterministic benign review cases

At minimum freeze four cases:

1. `stale-session-replay-after-reconnect` — a message or response from session generation N is accepted after reconnect creates N+1.
2. `retry-duplicate-commit` — a retried synthetic operation crosses commit twice because duplicate suppression is keyed to the wrong generation.
3. `role-change-stale-authority` — an operation authorized under role generation N remains consumable after the peer role changes to generation N+1.
4. `timeout-late-completion-cross-generation` — a timed-out/cancelled synthetic operation completes late and is routed into a replacement stream/transaction/session generation.

Each case must use synthetic peers, loopback/mock protocol endpoints, inert/read-only consumers, fake transaction ledgers, or bounded reversible owner-controlled markers.

## Counterfactual requirements

Each case changes exactly one causal variable while holding the rest constant, such as:

- same message under current versus stale session generation;
- same retry with valid idempotency binding versus generation-blind binding;
- same operation under old versus current role generation;
- same late completion with old versus replacement transaction generation;
- same negotiated feature before versus after renegotiation.

## Alternative explanations

Before PST4/PST5 eliminate:

- the protocol specification explicitly permits the sequence;
- test harness reused identifiers incorrectly;
- duplicate effect came from the positive control;
- message correlation was ambiguous;
- server and client state models intentionally differ;
- reconnect continuity is specified;
- retry semantics are at-least-once by design;
- role change is advisory rather than authoritative;
- timeout is explicitly non-cancelling;
- late completion belongs to a different operation;
- concurrency/race behavior fully explains the observation without a protocol-state invariant violation;
- receipt belongs to another endpoint/session generation.

Any unresolved material alternative caps evidence at PST2.

## Expected repository scope

1. `README.md`
2. `docs/operator-depth-contract.md`
3. `docs/superpowers/plans/2026-09-18-wave10-protocol-state-machine-depth.md`
4. `docs/superpowers/specs/2026-09-18-wave10-protocol-state-machine-depth-design.md`
5. `operator-depth/profiles.json`
6. `skills/protocol-state-machine-analysis/SKILL.md`
7. `skills/protocol-state-machine-analysis/references/operator-review-cases.json`
8. `skills/protocol-state-machine-analysis/references/operator-runbook.md`
9. `tests/test_protocol_state_machine_depth.py`
10. `tests/test_parser_state_machine_depth.py` only if behavioral CI proves its exact global-count assertion is the sole extensibility defect.

Do not change `skill.meta.json`, graph edges, packs, routing domains, benchmark authority, agent-eval authority, superiority-court authority, or workflow semantics.

## Success criterion

Profile #29 is complete only when the merge tree contains exactly 29 profiles, exactly one valid `protocol-state-machine-analysis` entry, PST0–PST5 is published, exact-head and post-merge CI are fully GREEN, and the final scope remains bounded to the intended paths.
