---
name: cryptographic-protocol-misuse-analysis
description: "Analyze application-level cryptographic protocol use: primitive choice, mode/domain separation, transcript binding, key roles, authentication order, replay context, downgrade negotiation, and error handling. Use for misuse analysis, not cryptanalytic key breaking."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Cryptographic Protocol Misuse Analysis

Perform dynamic validation only in a local/owned/sandboxed lab, benchmark, CTF, or other explicitly authorized environment. Use synthetic keys, synthetic peers, published or deterministic vectors, mock or loopback transports, inert consumers, read-only traces, and bounded reversible owner-controlled effects. Do not brute-force real keys or passwords, intercept unrelated live traffic, use production credentials, or turn a bounded protocol-composition finding into a claim of cryptanalytic breakage.

## When to use

Use when code implements or composes encryption, AEAD, MACs, signatures, KDFs, password hashing, key agreement, token/envelope formats, authenticated channels, negotiated security protocols, resumption, rekeying, or early data.

Use this skill to reason about protocol composition and state binding. Delegate RNG-source, seeding, fork/restart, and statistical reuse questions to `nonce-and-randomness-lifecycle-analysis`; delegate X.509 path, hostname, pin, and peer-certificate authorization to `certificate-and-hostname-validation-analysis`.

## Preconditions

1. Define the exact security goal and protocol operation before testing.
2. Pin implementation/library versions, protocol version space, algorithm/suite choices, role model, message phases, and lifecycle state.
3. Use only synthetic keys, peers, sessions, messages, and deterministic fixtures.
4. Define the intended consumer and a benign receipt/result oracle before attempting dynamic validation.
5. Stop before any test requires real-key recovery, credential abuse, unrelated live-traffic interception, destructive effects, persistence, or unauthorized systems.

## Causal protocol-composition model

Treat a cryptographic protocol as an authenticated state-transition system, not a list of primitives:

`security goal/protocol intent -> peer/role/session identities -> protocol version and feature negotiation -> selected algorithm/suite -> transcript identity -> authenticated negotiation binding -> key-schedule root/context -> derived key role/direction/epoch -> domain-separation labels -> nonce/sequence/record identity -> protocol phase/state -> authenticated context/AAD -> verification/decryption/authentication order -> replay/freshness state -> final verifier/application accept-or-reject decision -> authenticated protocol/session state -> privileged consumer/use -> bounded result/receipt -> protocol/key/replay/resumption/rekey lifecycle generation`

A claim can rise only as high as the weakest material transition that is captured. Library success, primitive approval, a valid tag/signature, a handshake success code, or a replay-cache observation cannot replace missing role, transcript, key-context, protocol-phase, consumer, or lifecycle evidence.

Preserve these distinctions:

- `approved primitive != safe protocol composition`;
- `signature valid != intended role/context authorized`;
- `decrypt success != authenticated acceptance`;
- `handshake success != authenticated negotiation transcript`;
- `selected suite != authenticated selected suite`;
- `unique nonce != correct key/nonce/context binding`;
- `same key material != same role/direction/epoch authorization`;
- `MAC/tag valid != message phase/action/context authorized`;
- `replay-cache miss != message fresh`;
- `resumed session != current protocol/key/policy generation`;
- `0-RTT accepted != replay-safe application action`;
- `bounded synthetic wrong-context acceptance != key recovery or broad cryptanalytic compromise`;
- `action/result success != receipt binding`.

## Negotiation and transcript binding

Record every negotiation input that can change protocol security: supported versions, selected version, algorithms/suites, optional features, compression or extension state, downgrade sentinels, role markers, and retry/fallback transitions.

Capture a stable transcript identity for the authenticated handshake or message sequence and prove whether the final selected state is bound into that transcript or an equivalent authenticated structure.

A local variable saying “TLS 1.3 selected,” a UI label, or a server log is not enough. The question is whether the final verifier and both intended roles authenticate the same selected state before privileged protocol use.

When testing a downgrade or feature-binding hypothesis, change one negotiated element at a time while holding peer identities, synthetic keys, transcript framing, and consumer constant.

## Key schedule, role, epoch, and domain separation

Map the key-schedule root, derivation context, labels, role, direction, purpose, protocol phase, and epoch for every derived key that participates in the hypothesis.

Require explicit separation where the design depends on it. Reusing equal bytes is not automatically a vulnerability, but equal or confusable derived authority across roles, directions, phases, algorithms, or epochs is a causal variable that must be traced.

Record whether labels/context bind the protocol name, version/suite, peer role, client/server direction, message purpose, transcript state, tenant/session where relevant, and rekey generation.

Do not infer safety from KDF strength alone. A strong KDF with incomplete context can deterministically derive the wrong authority.

## Protocol phase and authenticated-context binding

For each protected message, record the protocol phase/state, message type, sender role, intended receiver, action/purpose, session/tenant context where relevant, algorithm/suite, sequence or record identity, and authenticated context/AAD.

Authentication must cover the semantic context required by the protocol, not merely the payload bytes. A valid tag or signature over an under-specified message can still authorize the wrong role, phase, audience, action, or session.

Treat parsing and canonicalization that occurs before authentication as part of the causal trace. If the verifier authenticates one representation while the consumer uses another, preserve both identities and the transformation order.

## Authenticate-before-use ordering

Record the exact point where ciphertext becomes plaintext, signatures/tags are checked, protocol state is promoted, callbacks fire, and privileged consumers receive semantic data.

The default invariant is auth-before-use: attacker-controlled or unauthenticated semantics must not produce privileged state, callbacks, routing decisions, account transitions, or durable side effects before the final authenticity/integrity decision required by the protocol.

A decrypt API returning plaintext before reporting tag failure is not itself a vulnerability; evidence requires showing that a privileged consumer can observe or act on that plaintext before the final rejection.

Use inert markers, read-only consumers, or bounded in-memory state to demonstrate ordering. Never require harmful effects.

## Replay, freshness, and early-data reasoning

Map nonce/sequence/record identity, replay window, freshness source, session and epoch binding, retry semantics, idempotency expectations, and protocol phase.

A replay-cache miss is an observation, not proof of freshness. Prove what identity keys the replay state, when the state advances relative to authentication and application acceptance, how retries are distinguished from replays, and whether cross-session or cross-epoch reuse is possible.

For early data, preserve the distinction `0-RTT accepted != replay-safe application action`. Acceptance of early data can be correct only when the application action and anti-replay design support the resulting semantics.

Detailed RNG quality, seeding, collision probability, fork/restart behavior, or nonce-generation statistics belong to `nonce-and-randomness-lifecycle-analysis`; this profile consumes the resulting identity/reuse facts and binds them to the protocol consequence.

## Rekey, resumption, and lifecycle generations

Track generations for protocol policy, negotiated features, key schedule, derived keys, replay windows, session tickets, resumptions, early-data authority, peer/account mapping where applicable, and application authorization.

Rekey and resumption are new causal transitions, not invisible continuation. Capture which prior transcript, peer identity, policy, and key context are inherited; what is re-authenticated; which generation governs the resumed session; and which stale records, tickets, or cached decisions become invalid.

Preserve `resumed session != current protocol/key/policy generation`. A valid old ticket or cached session cannot establish current authorization by assumption after an authoritative generation changes.

## Workflow

1. Define security goal, protocol intent, peer roles, session identity, and bounded consumer.
2. Capture version/feature negotiation and the final selected algorithm/suite.
3. Build a stable transcript identity and record what negotiation state is authenticated.
4. Map key-schedule root/context, derived key roles, directions, epochs, and domain-separation labels.
5. Record nonce/sequence/record identity and the protocol phase of each tested message.
6. Record authenticated context/AAD and the exact verification/decryption/authentication order.
7. Trace replay/freshness state, retries, early data, rekey, and resumption generations.
8. Capture the final application accept-or-reject decision and authenticated protocol/session state.
9. Bind any inert or bounded result/receipt to the exact protocol tuple.
10. Run positive, negative, and counterfactual controls that change one causal transition at a time.
11. Eliminate alternative explanations before evidence promotion.
12. Re-run remediation while preserving neighboring intended protocol behavior.

## Cryptographic protocol evidence ladder

### CP0 — surface mapped

Security goals, roles, negotiation, transcript, key schedule, message phases, authenticated context, replay state, consumer, and lifecycle surfaces are mapped. No incorrect protocol decision is established.

### CP1 — binding or generation divergence observed

A concrete version/suite/transcript/key-role/context/authentication-order/replay/lifecycle divergence is observed, but incorrect acceptance is not yet demonstrated.

### CP2 — controlled protocol-policy mismatch demonstrated

A deterministic synthetic fixture proves that authenticated negotiation, key-role/domain separation, message-context binding, authentication order, replay/freshness logic, or lifecycle semantics diverge from intended protocol policy. No unauthorized protocol effect is required.

### CP3 — inert wrong-context acceptance

The final application verifier accepts a synthetic message/session under a role, phase, negotiation, replay, or context state that intended policy requires rejecting. The downstream consumer remains inert or read-only.

### CP4 — bounded protocol effect

The CP3 mismatch produces a bounded reversible owner-controlled state change or a read-only/inert consumer result through the intended protocol path. The result is bound to the exact role/session/negotiation/transcript/key-context/message/replay tuple. This is `bounded synthetic wrong-context acceptance != key recovery or broad cryptanalytic compromise`.

### CP5 — causal protocol-composition proof

Requires CP4 plus exact security goal/protocol intent, peer/role/session identities, negotiation and selected suite, authenticated transcript state, key-schedule root/context, role/direction/epoch and domain-separation proof, nonce/sequence/record identity, protocol phase, authenticated context, verification/authentication order, replay/freshness state, final application decision, authenticated protocol/session state, lifecycle/rekey/resumption generation, privileged consumer, receipt/result binding, meaningful counterfactuals, eliminated alternative explanations, and remediation regression preserving neighboring intended behavior.

## Counterfactual proof

Change one material transition while holding the rest constant. Strong controls include:

- bind vs omit the selected negotiation tuple from the authenticated transcript;
- vary only client/server role or direction while keeping the synthetic root key and message bytes constant;
- vary only domain-separation label or epoch while keeping the protocol phase constant;
- corrupt only a synthetic tag while observing whether an inert consumer receives data before final rejection;
- replay the same authenticated message into a neighboring session/epoch/phase while keeping payload and key material fixed;
- advance policy/rekey/resumption generation while replaying an otherwise identical stale ticket or record.

A counterfactual is useful only when fixture identity, transcript, key context, consumer, and receipt correlation prove what changed.

## Alternative explanations

Before promotion, rule out at least the relevant alternatives:

- fixture or vector mismatch;
- wrong peer role or session correlation;
- logging a selected suite that differs from the authenticated suite;
- stale transcript, key cache, replay cache, or session ticket;
- a debug/test-only fallback path not present in the claimed configuration;
- benign retry or intended idempotent replay;
- consumer initialization mistaken for pre-authentication use;
- message canonicalization differences unrelated to cryptographic acceptance;
- receipt/result from a neighboring run;
- an RNG/nonce-generation defect that belongs to the dedicated randomness-lifecycle skill;
- certificate/hostname acceptance that belongs to the dedicated PKI profile.

## Evidence ceiling

Primitive names, static warnings, approved algorithms, signature/tag success, decrypt success, handshake success, selected-suite logs, unique-looking nonces, replay-cache state, or protocol crashes cannot by themselves exceed CP1.

A deterministic protocol-policy mismatch can reach CP2. Inert wrong-context acceptance can reach CP3. A bounded correlated protocol effect can reach CP4.

Only the full causal chain plus controls, lifecycle evidence, counterfactuals, eliminated alternatives, privileged-consumer and receipt/result binding, and remediation regression can support CP5.

## Stop conditions

Stop when validation would require brute-force or recovery of real keys/passwords, unrelated live-traffic interception or decryption, production credentials, unauthorized third-party interaction, persistence, malware, destructive action, evasion, out-of-scope side-channel probing, or a claim beyond the demonstrated protocol property.

## Output

```text
security goal / protocol intent:
peer / role / session identities:
negotiation and selected suite:
transcript identity / authenticated binding:
key schedule / roles / epochs / domain separation:
nonce / sequence / record identity:
protocol phase / authenticated context:
verification / authentication order:
replay / freshness / early-data state:
rekey / resumption / lifecycle generation:
final application decision:
authenticated protocol / session state:
privileged consumer:
bounded result / receipt binding:
counterfactual controls:
alternative explanations:
evidence level / ceiling:
```
