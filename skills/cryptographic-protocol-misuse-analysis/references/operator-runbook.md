# Cryptographic Protocol Misuse Operator Runbook

Use this runbook only for local, owned, sandboxed, benchmark, CTF, or explicitly authorized protocol implementations. Prefer a synthetic key hierarchy, deterministic vectors, a mock peer or loopback peer, inert consumers, read-only traces, and bounded reversible owner-controlled state. Do not use real production credentials, brute-force real secrets, intercept unrelated traffic, or turn a bounded protocol-composition result into a broad cryptanalytic claim.

## Attack surface

Map the protocol as a state machine whose security depends on authenticated relationships, not merely primitive strength. Record:

- security goals and protocol operations;
- initiator/responder or client/server roles;
- session and peer identity;
- version/feature/suite negotiation;
- transcript construction and authentication;
- key schedule roots, derivation context, labels, role/direction/epoch;
- nonce, sequence, record, and message identities;
- protocol phase and authenticated context/AAD;
- decrypt/verify/authentication order;
- replay/freshness state and retry semantics;
- early-data, rekey, resumption, restart, and policy generations;
- final application decision, authenticated protocol/session state, privileged consumer, and receipt/result.

Separate protocol-composition questions from RNG generation quality and certificate/hostname path validation. Consume those neighboring facts when relevant without duplicating their operator contracts.

## Hypothesis matrix

Turn broad crypto concerns into transition-level falsifiable hypotheses.

| Hypothesis | Controlled variable | Benign oracle | Minimum causal requirement |
| --- | --- | --- | --- |
| Negotiation is not authenticated | selected version/suite/feature tuple | mock peer decision + inert session marker | same peers/keys, one transcript-binding difference |
| Key roles are confusable | role/direction/purpose/epoch label | synthetic message accept/reject receipt | same root key, one derivation-context difference |
| Data is used before final authentication | valid vs corrupted tag/signature | inert consumer marker before/after rejection | same ciphertext/message, one authentication outcome |
| Replay context is incomplete | session/epoch/phase/resumption generation | read-only replay receipt/counter | same valid message, one context/generation change |

Do not promote “old algorithm,” “same key bytes,” “tag verifies,” “handshake works,” or “cache misses” into a vulnerability without the causal protocol transition and controls.

## Protocol intent and role/session trace

Define the security goal before interpreting crypto behavior: confidentiality, integrity, peer/entity authenticity, action authorization, freshness, channel binding, forward secrecy, replay resistance, or another explicit property.

Record initiator/responder roles, peer identities, session identifier, requested operation, expected receiver, protocol phase, and intended privileged consumer.

Bind every observation to one exact session. If two parallel mock peer sessions exist, give them different correlation IDs so logs, callbacks, and receipts cannot be mixed.

## Negotiation and downgrade trace

Capture offered versions, features and suites; retry/fallback state; selected version/suite; downgrade sentinels; and any server/client preference that changes the result.

Record both the implementation-visible selected state and the state actually included in authenticated data.

A downgrade hypothesis is not validated because a weaker suite can be selected. It requires showing that intended policy says the state should be rejected or authenticated differently and that the final application decision diverges under a controlled counterfactual.

## Transcript and authenticated-negotiation trace

Assign a deterministic transcript identity to the exact ordered handshake/message sequence. Record canonical bytes or stable fixture identities used by the authenticator, including whether the selected negotiation tuple, role markers, peer/session identifiers, retry state, and relevant extensions are covered.

Preserve the distinction between a local log of selected parameters and authenticated negotiation. A transcript identity must follow the data the verifier actually authenticates.

For paired controls, hold synthetic keys, mock peer identities, message payloads, and consumer constant while changing only the negotiation field or transcript inclusion being tested.

## Key schedule, role, direction, epoch, and domain-separation trace

Record:

- synthetic key-schedule root or fixture identity;
- KDF identity and derivation context;
- protocol/version/suite labels;
- sender/receiver role;
- client/server or initiator/responder direction;
- encryption/MAC/signature/exporter/purpose role;
- handshake/application/early-data phase;
- current epoch or rekey generation.

A strong KDF does not repair missing context. Prove whether two logically distinct authorities can derive confusable keys because role, direction, phase, purpose, protocol, or epoch is omitted.

Treat domain separation as an explicit security binding: document which protocol, role, direction, purpose, phase, and epoch each label separates, and prove paired controls cannot cross those domains.

Use only synthetic key material. Never require real-key recovery.

## Nonce, sequence, and record identity trace

Record the exact nonce/IV/sequence/record identifier consumed by the tested construction and the key/role/epoch with which it is paired.

This runbook does not evaluate RNG statistical quality or seed compromise. When reuse or collision is relevant, import the deterministic fact from `nonce-and-randomness-lifecycle-analysis` and ask whether that identity is acceptable for this protocol/key/context tuple.

A unique nonce is not sufficient when the wrong key, role, epoch, or authenticated context is bound to the record.

## Protocol phase and authenticated-context trace

Capture message type, protocol phase, sender role, receiver, action/purpose, audience or tenant/session where material, suite, sequence identity, and all AAD or signed context.

Record any canonicalization or parsing that happens before authentication and the representation later consumed.

A valid MAC/tag or signature does not establish that the message is valid for the current phase or action. Require explicit authenticated-context binding when the protocol security goal depends on that context.

## Verification and authentication-order trace

Trace the exact order:

`receive -> frame/parse -> decrypt or reconstruct candidate plaintext -> verify tag/signature/MAC -> final accept/reject -> promote protocol state -> privileged consumer -> receipt/result`

If an API exposes candidate plaintext before reporting failure, instrument an inert consumer to prove whether any semantic use occurs before final authentication.

The relevant invariant is auth-before-use. A transient buffer existing in memory is not enough; evidence requires a privileged or security-relevant consumer transition before final reject.

## Replay and freshness trace

Record replay-key identity, sequence/window semantics, freshness source, update timing, session/epoch binding, retry/idempotency rules, and the final application decision.

Determine whether replay state advances before or after authentication, whether failed messages consume sequence state, whether the key includes the authoritative session/epoch/role, and whether cache resets or concurrency create false observations.

Distinguish an intended retry from an unauthorized replay using positive and negative controls with the same message identity.

## Rekey, resumption, and early-data lifecycle trace

Record protocol-policy generation, key-schedule epoch, replay-window generation, session-ticket identity and generation, resumption state, early-data authority, and any current peer/account authorization generation.

Treat rekey and resumption as explicit transitions. Record what state is inherited, what is re-authenticated, and which generation controls the resumed session.

For early-data trials, keep the application action inert and ask whether replay is safe for that exact action. The phrase `0-RTT accepted != replay-safe application action` is a protocol invariant, not a demand to disable all early data.

## Privileged-consumer and result trace

Name the exact consumer that observes authenticated protocol state or semantic data. Prefer an inert in-memory state machine, read-only query, or bounded test-only counter.

Every receipt/result must bind:

- fixture and test-run ID;
- peer/role/session;
- negotiation and transcript identity;
- key role/direction/epoch;
- record/message identity and protocol phase;
- replay/freshness/lifecycle generation;
- final application decision.

A successful action or result without this correlation cannot establish which protocol tuple caused it.

## Controlled validation

Use deterministic paired experiments.

1. Pin one implementation build and one synthetic protocol configuration.
2. Use synthetic keys and mock peer fixtures with stable IDs.
3. Keep one positive control that represents intended protocol behavior.
4. Keep one negative control that should be rejected.
5. Change only one material causal variable for each counterfactual.
6. Use inert/read-only consumers and bounded reversible state.
7. Preserve complete receipts for both controls and the tested case.
8. Repeat remediation with the same fixture identities.

Do not fuzz arbitrary crypto payloads here unless a separate authorized fuzzing workflow is the actual investigation. The purpose of this profile is controlled causal validation.

## False-positive controls

Require controls for the likely alternative explanation:

- same transcript, different authenticated negotiation field;
- same root key, different role/direction/domain label;
- same ciphertext/message, valid vs corrupted tag;
- same valid message, current vs neighboring session/epoch;
- same resumption ticket before vs after authoritative generation change;
- same early-data bytes for a read-only/idempotent vs deliberately stateful inert action;
- same consumer with a fresh correlation ID to exclude stale markers.

Also rule out debug-only configuration, fixture mismatch, stale caches, unrelated parsing errors, and receipts from another run.

## Counterfactual controls

A meaningful counterfactual changes one causal transition while all other authoritative identities remain fixed.

For transcript hypotheses, add or remove exactly the selected negotiation binding.

For key-role hypotheses, change only role/direction/purpose/epoch derivation context while preserving the synthetic root key.

For auth-before-use, corrupt only the authenticator while preserving candidate plaintext and consumer instrumentation.

For replay/lifecycle, replay the same authenticated message while changing only session, epoch, phase, rekey generation, or resumption generation.

If more than one authoritative variable changes, split the experiment before evidence promotion.

## Alternative explanations

Before a validated claim, explicitly eliminate:

- stale or mixed transcript logs;
- wrong peer/session correlation;
- alternate selected-suite reporting;
- stale key/replay/session-ticket cache;
- debug/test-only permissive branches;
- benign retry or idempotent replay;
- consumer initialization mistaken for pre-authentication use;
- representation/canonicalization differences unrelated to authentication;
- synthetic key fixture mismatch;
- an RNG/nonce-generation problem owned by the randomness-lifecycle skill;
- a certificate/hostname problem owned by the PKI profile;
- receipt/result correlation to another run.

Document the alternative explanation that remains most plausible if evidence cannot exceed CP1 or CP2.

## Evidence capture

For each case preserve a compact evidence bundle containing:

- security goal and protocol intent;
- peer/role/session identities;
- version/suite negotiation state;
- transcript identity and authenticated binding;
- synthetic key-schedule root/context;
- key role/direction/epoch and domain labels;
- nonce/sequence/record identity;
- protocol phase and authenticated context;
- verification/authentication order;
- replay/freshness state;
- final application decision;
- authenticated protocol/session state;
- lifecycle/rekey/resumption generation;
- privileged-consumer identity;
- bounded result and receipt/result binding;
- positive, negative, and counterfactual control receipts;
- alternative explanations and remediation result.

Use stable fixture IDs, not secret values, where raw material is unnecessary.

## Evidence promotion and ceiling

CP0 maps the surface.

CP1 observes a binding, ordering, identity, or generation divergence.

CP2 demonstrates a deterministic protocol-policy mismatch.

CP3 requires inert wrong-context acceptance by the final application verifier.

CP4 requires a bounded reversible state transition or read-only/inert result correlated to the exact protocol tuple.

CP5 requires CP4 plus the complete causal protocol chain, key-role/domain proof, replay/lifecycle generations, privileged consumer, receipt/result binding, meaningful counterfactuals, eliminated alternative explanations, and remediation regression.

Primitive approval, signature/tag validity, decrypt success, handshake success, selected-suite logs, unique-looking nonces, replay-cache telemetry, or a crash cannot skip the evidence ceiling.

## Remediation checks

Prefer fixes that repair the causal binding:

- authenticate the final negotiation tuple;
- strengthen KDF labels/context or role/direction/epoch separation;
- bind protocol phase, action, audience/session, and algorithm state into authenticated context;
- move privileged use behind the final authenticity decision;
- bind replay state to authoritative session/epoch and advance it atomically with acceptance;
- invalidate or re-authorize stale rekey/resumption/early-data state after generation changes.

Regression verification must prove the failing synthetic path no longer reaches the bounded oracle while the neighboring valid protocol path still succeeds.

Do not “fix” by inventing new cryptography. Prefer established protocol/library semantics and the smallest change that restores the intended invariant.
