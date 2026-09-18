# Wave 10 Profile #23 — Cryptographic Protocol Misuse Depth Design

## Status

Design authority for Wave 10 operator-depth profile #23, based on exact `main@9318953f530ea7d88b07a8b19413e7ee77d74c00`.

Target canonical skill: `cryptographic-protocol-misuse-analysis`.

## Why this profile

The canonical skill already covers primitive choice, transcript binding, key roles, authentication order, replay context, downgrade negotiation, and error handling, but it remains a compact reasoning entry point. The current operator-depth registry has no profile that deterministically freezes causal protocol-composition semantics across negotiation, transcripts, key schedule roles, authenticated context, replay state, and rekey/resumption generations.

This gap is materially distinct from:

- `certificate-and-hostname-validation-analysis`: peer identity, X.509 path/trust-anchor, hostname, pin/revocation, and session-to-peer binding;
- `nonce-and-randomness-lifecycle-analysis`: RNG source/state, uniqueness, unpredictability, fork/restart/concurrency, and reuse/collision conditions;
- `secrets-and-token-flow-analysis`: issuance, possession, verifier audience/resource binding, and represented authority;
- `canonicalization-and-namespace-analysis`: representation-to-identity transformation and namespace binding.

Profile #23 focuses on whether a cryptographic protocol composes otherwise-valid primitives into the intended authenticated state transition.

## Safety boundary

Dynamic validation is limited to local, owned, sandboxed, benchmark, CTF, or explicitly authorized systems using synthetic keys, synthetic protocol peers, published or deterministic test vectors, mock/loopback transports, inert consumers, read-only traces, or bounded reversible owner-controlled effects.

The profile must not require:

- brute-force or recovery of real keys/passwords;
- interception/decryption of unrelated live traffic;
- real production credentials or tokens;
- unauthorized third-party protocol interaction;
- persistence, malware, destructive action, evasion, or stealth;
- side-channel probing outside explicit authorization.

## Causal protocol model

The canonical skill must explicitly reason through this transition chain:

`security goal/protocol intent -> peer/role/session identities -> protocol version and feature negotiation -> selected algorithm/suite -> transcript identity -> authenticated negotiation binding -> key-schedule root/context -> derived key role/direction/epoch -> domain-separation labels -> nonce/sequence/record identity -> protocol phase/state -> authenticated context/AAD -> verification/decryption/authentication order -> replay/freshness state -> final verifier/application accept-or-reject decision -> authenticated protocol/session state -> privileged consumer/use -> bounded result/receipt -> protocol/key/replay/resumption/rekey lifecycle generation`

Evidence may rise only as high as the weakest material transition that is actually captured.

## Required distinctions

The skill and runbook must preserve at least these distinctions:

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

## Required invariants

1. **Goal-to-construction binding** — every claimed property is tied to the exact protocol operation, role, phase, and consumer.
2. **Authenticated negotiation binding** — final version/suite/features/downgrade state are authenticated by the transcript or an equivalent binding before privileged use.
3. **Key-role/domain separation** — derived keys and labels are bound to protocol, role, direction, phase, purpose, and epoch where required.
4. **Authenticated-context binding** — message acceptance covers required role, audience/action, tenant/session, phase, algorithm, and transcript context.
5. **Authenticate-before-use** — plaintext or reconstructed semantics do not reach privileged consumers before the final authenticity/integrity decision.
6. **Replay/freshness state** — sequence/window/nonce/freshness state is bound to the intended session/epoch and advanced consistently with acceptance.
7. **Lifecycle continuity** — rekey, rotation, resumption, retry, restart, and early-data transitions do not silently inherit stale authorization.
8. **Result/receipt correlation** — any bounded effect or read-only result is correlated to the exact protocol/session tuple that produced it.

## Evidence ladder

### CP0 — surface mapped

Protocol goals, roles, negotiation, transcript, key schedule, message phases, replay state, and lifecycle surfaces are identified. No incorrect protocol decision is established.

### CP1 — binding or generation divergence observed

A concrete version/suite/transcript/key-role/context/auth-order/replay/lifecycle divergence is observed, but incorrect acceptance is not yet demonstrated.

### CP2 — controlled protocol-policy mismatch demonstrated

A deterministic synthetic fixture proves that negotiation binding, key-role separation, authenticated context, authentication order, replay/freshness logic, or lifecycle semantics diverge from intended protocol policy. No unauthorized protocol effect is required.

### CP3 — inert wrong-context acceptance

The final application verifier accepts a synthetic message/session under a role, phase, negotiation, replay, or context state that intended policy requires rejecting. The downstream consumer remains inert or read-only.

### CP4 — bounded protocol effect

The CP3 mismatch causes a bounded reversible owner-controlled state change or read-only/inert consumer result through the intended protocol path. The result is bound to the exact role/session/negotiation/transcript/key-context/message/replay tuple. CP4 is not key recovery, arbitrary traffic decryption, or a broad cryptanalytic break.

### CP5 — causal protocol-composition proof

Requires CP4 plus exact security goal and protocol intent; peer/role/session identity; negotiation and selected suite; authenticated transcript state; key-schedule root/context and role/direction/epoch; domain-separation labels; nonce/sequence/record identity; protocol phase; authenticated context; verification/authentication order; replay/freshness state; final application decision; lifecycle/rekey/resumption generation; privileged consumer; receipt/result binding; meaningful counterfactuals; eliminated alternative explanations; and remediation regression preserving neighboring intended behavior.

## Deterministic review cases

At least four benign scenarios will be encoded.

### 1. Negotiation/transcript binding

A synthetic handshake chooses a weaker/different version or feature state that is not bound into the authenticated transcript. Positive and negative controls change only the authenticated negotiation tuple. The oracle is a mock verifier decision and inert session marker.

### 2. Key-role/domain separation

Synthetic derived keys intentionally collide across role/direction/purpose/epoch because labels/context are incomplete. Controls preserve the same root key while varying only the role/domain tuple. The oracle is deterministic accept/reject of inert messages.

### 3. Authenticate-before-use

A synthetic encrypted/authenticated record reaches an inert semantic consumer before final tag/signature verification. A corrupted tag must prove whether any consumer result is emitted before rejection. Remediation moves privileged consumption behind final authentication while preserving valid-record behavior.

### 4. Replay/context/lifecycle binding

A valid synthetic message is replayed across session, epoch, protocol phase, resumption, or early-data context. Controls distinguish legitimate retransmission/idempotent behavior from stale cross-generation acceptance. The oracle is an inert counter/read-only receipt.

## Review-case machine fields

Every scenario must include the common operator-depth fields plus:

- `security_goal_protocol_intent`
- `peer_role_session_identity`
- `protocol_version_suite_negotiation_state`
- `transcript_identity_binding`
- `key_schedule_root_context`
- `key_role_direction_epoch`
- `domain_separation_labels`
- `nonce_sequence_record_identity`
- `protocol_phase_state`
- `authenticated_context_binding`
- `verification_authentication_order`
- `replay_freshness_state`
- `final_application_decision`
- `authenticated_protocol_session_state`
- `privileged_consumer`
- `bounded_result`
- `receipt_result_binding`
- `lifecycle_generation`
- `counterfactual_control`
- `alternative_explanation`
- `evidence_level`
- `evidence_ceiling`

All substantive string fields must be non-trivial and deterministic. Evidence levels and ceilings use `CP0` through `CP5`.

## Runbook structure

The runbook must contain the common required sections plus domain sections for:

- protocol intent and role/session trace;
- negotiation and downgrade trace;
- transcript/authenticated-negotiation trace;
- key schedule, role, direction, epoch, and domain-separation trace;
- nonce/sequence/record identity trace;
- protocol phase and authenticated-context trace;
- verification/authentication-order trace;
- replay/freshness trace;
- rekey/resumption/early-data lifecycle trace;
- privileged-consumer and receipt/result trace;
- counterfactual controls;
- alternative explanations;
- evidence promotion and ceiling.

## Test-first contract

A dedicated `tests/test_cryptographic_protocol_misuse_depth.py` will be committed before production depth artifacts.

It freezes four assertion groups:

1. canonical SKILL causal semantics, distinctions, CP0–CP5, counterfactuals, alternatives, evidence ceiling, and safety boundary;
2. runbook section and transition-level methodology;
3. deterministic review-case IDs, required fields, safe oracles, stops, remediation, and CP evidence values;
4. registry v2 with exactly 23 profiles and exactly one `cryptographic-protocol-misuse-analysis` profile pointing to the expected runbook/review-case paths with `lab_only: true`.

The dedicated #23 test must not be weakened after RED.

## Known extensibility maintenance

The current profile #22 dedicated test contains a stale global snapshot assertion `len(profiles) == 22`. That assertion blocks every valid future profile while adding no profile-#22 semantic protection.

Profile #23 therefore includes one exact maintenance change:

`tests/test_certificate_hostname_depth.py`: change only the global profile-count assertion from `== 22` to `>= 22`.

All certificate/hostname-specific assertions remain exact and unchanged.

## Intended scope

Exactly ten paths are expected:

1. `README.md`
2. `docs/operator-depth-contract.md`
3. `docs/superpowers/specs/2026-09-18-wave10-crypto-protocol-depth-design.md`
4. `docs/superpowers/plans/2026-09-18-wave10-crypto-protocol-depth.md`
5. `operator-depth/profiles.json`
6. `skills/cryptographic-protocol-misuse-analysis/SKILL.md`
7. `skills/cryptographic-protocol-misuse-analysis/references/operator-runbook.md`
8. `skills/cryptographic-protocol-misuse-analysis/references/operator-review-cases.json`
9. `tests/test_cryptographic_protocol_misuse_depth.py`
10. `tests/test_certificate_hostname_depth.py`

No `skill.meta.json`, graph edge, pack, routing domain, benchmark authority, agent-eval authority, superiority-court authority, or workflow-semantic change is intended.

## CI lineage

1. exact base branch;
2. design commit;
3. plan commit;
4. dedicated test-first commit;
5. Draft PR on the exact test-first SHA;
6. RED CI, valid only when the four intended #23 assertion groups fail while pre-existing gates remain healthy;
7. implementation + registry + the one-line #22 extensibility maintenance;
8. full behavioral 9/9 GREEN;
9. only after behavioral GREEN, public README and operator-depth contract publication;
10. prove the post-behavioral delta is exactly those two public docs;
11. exact-head full 9/9 GREEN;
12. fresh base/head/scope/mergeability check;
13. guarded merge with `expected_head_sha`;
14. exact merge-parent verification;
15. post-merge push CI 9/9 GREEN on the merge SHA;
16. merge-tree registry/README/contract verification;
17. closure provenance comment.

## Completion definition

Profile #23 is complete only after post-merge 9/9 GREEN and closure provenance are verified on the merged PR.
