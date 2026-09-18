# Operator Depth Contract

Wave 8 makes operator depth a deterministic two-artifact contract: reviewed methodology in Markdown plus machine-readable scenario matrices enforced by CI.

## Purpose

Canonical `SKILL.md` files remain the portable reasoning entry points. Selected high-value skills may additionally expose:

- `references/operator-runbook.md` — deeper domain methodology for authorized investigations;
- a machine-readable JSON matrix — deterministic safe cases that freeze evidence, control, stop, and remediation requirements.

The repository intentionally does **not** use line count, byte count, payload count, or tool-name count as a quality metric. Depth is defined by reviewable methodology plus falsifiable machine-readable contracts.

## Registry authority

`operator-depth/profiles.json` is the binding source of truth for operator-depth artifacts. The manifest remains at version `2`; Wave 10 expands the set of registered profiles without changing the registry schema.

Each profile declares:

```json
{
  "skill": "canonical-skill-name",
  "runbook": "references/operator-runbook.md",
  "scenario_matrix": "references/operator-scenarios.json",
  "lab_only": true,
  "required_runbook_sections": [
    "Attack surface",
    "Hypothesis matrix",
    "Controlled validation",
    "False-positive controls",
    "Evidence capture",
    "Remediation checks"
  ]
}
```

The `scenario_matrix` field is the stable registry interface; a profile may bind another deterministic JSON filename when its reviewed semantics are audit cases rather than action-oriented scenarios. Both artifact paths are relative to `skills/<skill>/`. Absolute paths, path traversal, missing canonical skills, duplicate profiles, and missing artifacts fail validation.

The registry is the authoritative binding so a canonical skill does not need duplicated vendor-specific or profile-specific metadata in its portable frontmatter.

## Runbook contract

Every registered runbook must contain these exact second-level sections:

1. `Attack surface` — identify the principals, resources, states, policy layers, parsers, or capability boundaries relevant to the domain.
2. `Hypothesis matrix` — turn broad concerns into falsifiable hypotheses with safe proof signals.
3. `Controlled validation` — define bounded, reproducible experiments using owned, sandboxed, synthetic, simulated, or read-only resources.
4. `False-positive controls` — require paired controls that distinguish a real boundary failure from harness, policy, configuration, or environment artifacts.
5. `Evidence capture` — define observable evidence sufficient to advance the repository evidence state machine.
6. `Remediation checks` — verify the causal fix while preserving neighboring intended behavior.

Every runbook also needs explicit authorization/lab language and evidence/control discipline.

## Scenario-matrix contract

Each registered machine-readable matrix has version `1` and at least three scenarios. Scenario IDs are unique lowercase slugs.

Every scenario must contain non-empty values for:

```json
{
  "id": "stable-scenario-id",
  "hypothesis": "falsifiable policy or boundary claim",
  "safe_oracle": "benign synthetic/mock/controlled/read-only observable",
  "positive_control": "expected neighboring behavior that must still work",
  "negative_control": "expected denied or absent behavior",
  "stop_condition": "explicit stop or abort boundary",
  "remediation_oracle": "post-fix invariant plus preserved intended behavior"
}
```

The validator requires the safe oracle to explicitly name a benign test mechanism such as a synthetic marker, mock, inert sink, simulation, read-only observation, controlled fixture, or canary. The stop condition must explicitly say to stop, abort, or not proceed beyond the stated boundary.

Machine-readable matrices are intentionally not exploit recipes. They encode what must be demonstrated, what controls must exist, where testing must stop, and what a successful remediation must preserve.

## Validation

Run:

```bash
python scripts/validate_operator_depth.py
```

The zero-dependency validator fails closed for malformed registries or matrices, unsafe paths, duplicate profiles/scenario IDs, missing canonical skills or artifacts, missing runbook sections, disabled lab-only policy, incomplete scenarios, unsafe-or-unspecified proof signals, and missing explicit stop conditions.

Diagnostics are deduplicated and sorted to remain deterministic across supported CI environments.

## Security boundary

Operator-depth artifacts are for local, owned, sandboxed, benchmark/CTF, simulated, or explicitly authorized targets. Prefer synthetic identities, mock services, policy simulators, inert action sinks, test canaries, disposable resources, and read-only evidence.

A deeper methodology never weakens the repository evidence standard. Tool output, a model assertion, a permissive-looking configuration, a single surprising response, or theoretical reachability is not sufficient by itself for a validated finding.

## Evidence states

Operator-depth profiles inherit the repository evidence model:

```text
hypothesis
    ↓
observed
    ↓
validated
    ↓
regression-verified
```

A `validated` case requires direct bounded evidence plus suitable controls. `regression-verified` additionally proves the fix blocks the failing synthetic path while expected neighboring behavior still succeeds.

## Wave 8 profiles

Wave 8 established eight CI-enforced profiles:

- `ai-agent-security-assessment`
- `authorization-boundary-analysis`
- `cloud-iam-path-analysis`
- `container-isolation-review`
- `driver-ioctl-surface-analysis`
- `exploitability-triage`
- `server-side-request-boundary-analysis`
- `web-routing-and-middleware-analysis`

The first four-profile Wave 7 baseline is preserved and migrated to scenario matrices; Wave 8 deepens four additional high-value domains without duplicating canonical skills.

## Wave 10 depth expansion

Wave 10 extends operator depth without adding duplicate canonical capabilities. The second-depth ring currently promotes:

- `prompt-injection-boundary-analysis` — the ninth profile, adding instruction-lineage, transformation-provenance, authority-conflict, decision/effect, counterfactual, and evidence-ceiling reasoning;
- `rag-memory-data-isolation-analysis` — the tenth profile, adding end-to-end principal binding, derived-state lineage, retrieval-policy traces, cache/memory coherence, lifecycle/revocation generations, bounded convergence, and R0–R5 evidence ceilings;
- `connector-plugin-trust-analysis` — the eleventh profile, adding integration provenance, effective-permission traces, schema/argument state, response binding, composition boundaries, lifecycle generations, C0–C5 evidence ceilings, and deterministic audit-only review cases;
- `tool-capability-and-confirmation-analysis` — the twelfth profile, adding request-to-action binding, argument-normalization traces, effective-authority reasoning, confirmation tuples, execution-state drift, transaction/retry/idempotency semantics, post-action receipt/final-state verification, and T0–T5 evidence ceilings;
- `canonicalization-and-namespace-analysis` — the thirteenth profile, adding typed representation/identity traces, transformation ordering and non-commutativity, normalization idempotence, policy-key-to-resolved-identity binding, namespace-root and name-to-object state, namespace generations, N0–N5 evidence ceilings, counterfactual controls, and deterministic audit-only review cases;
- `confused-deputy-analysis` — the fourteenth profile, adding causal authority-transfer traces, delegated-versus-ambient authority distinctions, monotonic attenuation, operation/resource and resolved-target binding, delegation generation/lifecycle reasoning, result/receipt binding, counterfactual controls, deterministic audit-only review cases, and D0–D5 evidence ceilings;
- `cache-key-identity-analysis` — the fifteenth profile, adding semantic dependency-to-key completeness, canonical key/namespace/entry identity traces, writer/reader provenance, first-writer and reverse-order controls, lifecycle/invalidation generations, deterministic audit-only review cases, counterfactual controls, and K0–K5 evidence ceilings;
- `secrets-and-token-flow-analysis` — the sixteenth profile, adding credential-class semantics, issuance provenance, possession/storage/propagation boundary traces, verifier-decision reasoning, audience/resource binding, represented-authority and delegation-attenuation traces, lifecycle/revocation generations, deterministic audit-only review cases, counterfactual controls, and S0–S5 evidence ceilings;
- `multi-tenant-data-isolation-analysis` — the seventeenth profile, adding canonical tenant identity and membership/role binding, tenant-context generations, representation/propagation traces, policy/filter and namespace decisions, resolved object/result identity, async/job context, lifecycle/migration generations, ambient-authority controls, deterministic audit-only review cases, counterfactual controls, and M0–M5 evidence ceilings;
- `supply-chain-dependency-review` — the eighteenth profile, adding source/namespace resolution, immutable artifact identity, integrity/signature/provenance-verifier reasoning, build-hook and toolchain identity, CI trust and cache/reuse binding, produced-to-released-to-distributed-to-deployed artifact identity, release/signing/publishing authority, lifecycle/revocation/update generations, deterministic audit-only review cases, counterfactual controls, and SC0–SC5 evidence ceilings;
- `browser-process-boundary-analysis` — the nineteenth profile, adding origin/site/frame-to-process binding, exact process and routed-object generation identity, normalized IPC routing and ownership checks, brokered capability attenuation, ambient-versus-delegated authority separation, privileged-consumer and receipt/result binding, lifecycle/revocation controls, deterministic audit-only review cases, counterfactual controls, and B0–B5 evidence ceilings;
- `boot-chain-and-secure-boot-analysis` — the twentieth profile, adding immutable/policy root identity and active policy/key-generation provenance, boot-mode and selector-state traces, candidate/selected/loaded component identity separation, signer authorization, rollback/freshness generations, verified-to-loaded binding, authenticated handoff and next-stage inheritance, recovery/alternate-path equivalence controls, receipt/measurement/attestation correlation, lifecycle/revocation controls, deterministic benign review cases, counterfactuals, and BC0–BC5 evidence ceilings;
- `deserialization-trust-analysis` — the twenty-first profile, adding serialized-artifact origin and authenticity/purpose provenance, parser/canonical-field traces, schema identity/version, discriminator-to-canonical-runtime-type resolution, resolver/registry identity and generations, object-construction and graph placement, hooks/callbacks and secondary interpretation, requested-to-effective reconstructed authority, privileged-consumer and receipt/result binding, lifecycle invalidation, deterministic benign review cases, counterfactual controls, alternative-explanation elimination, and DT0–DT5 evidence ceilings;
- `certificate-and-hostname-validation-analysis` — the twenty-second profile, adding intended peer/service identity, original/redirect/transport/SNI/reference-identity separation, verifier and trust-store generations, presented-chain identity, selected certification path and trust anchor, certificate constraints and SAN/hostname binding, pin/revocation/callback final-decision traces, authenticated peer/session and mTLS mapping, lifecycle invalidation, deterministic benign review cases, counterfactual controls, alternative-explanation elimination, and PKI0–PKI5 evidence ceilings;
- `cryptographic-protocol-misuse-analysis` — the twenty-third profile, adding security-goal/protocol intent, peer/role/session and negotiated-version/suite identity, transcript/authenticated-negotiation binding, key-schedule root/context plus role/direction/epoch and domain separation, nonce/sequence/record identity, protocol-phase authenticated context, authenticate-before-use ordering, replay/freshness state, rekey/resumption/early-data lifecycle generations, privileged-consumer receipt/result binding, deterministic benign review cases, counterfactual controls, alternative-explanation elimination, and CP0–CP5 evidence ceilings.
- `guest-host-boundary-analysis` — the twenty-fourth profile, adding guest-principal/security-domain provenance, interface/device/channel plus device/queue generation identity, guest-controlled descriptor/register/message/address binding, guest-physical/shared-object and translation/IOMMU/memory-slot generations, backend/emulation-thread consumer identity, host-object ownership/lifetime, validation/pinning/copy/TOCTOU decisions, effective host capability, reset/hot-unplug/migration/snapshot lifecycle revocation, bounded result/receipt binding, deterministic benign review cases, counterfactual controls, alternative-explanation elimination, and GH0–GH5 evidence ceilings.
- `memory-lifetime-analysis` — the twenty-fifth profile, adding logical object/resource identity, allocation/acquisition generations, owner/alias and retain/borrow/refcount provenance, invalidation/retirement and destruction/release generations, address/handle reuse identity, asynchronous callback/work-item lifecycle, final-consumer and effective stale/double-use capability binding, bounded receipt/result semantics, deterministic benign review cases, counterfactual controls, alternative-explanation elimination, and ML0–ML5 evidence ceilings.
- `concurrency-race-analysis` — the twenty-sixth profile, adding shared-invariant and state-generation identity, actor/operation generations, scheduler/executor identity, synchronization epochs and explicit happens-before edges, check/use and interfering-transition binding, publication/commit ordering, cancellation/retry/teardown generations, single-effect semantics, final-consumer and effective concurrent-capability binding, bounded receipt/result semantics, deterministic schedule controls, benign review cases, counterfactual schedules, alternative-explanation elimination, and CR0–CR5 evidence ceilings.
- `sandbox-boundary-analysis` — the twenty-seventh profile, adding sandbox-principal/security-domain and session generations, policy identity/generation, broker/service and caller-request binding, requested-to-canonical/resolved resource identity, inherited/delegated capability provenance and attenuation, namespace/object and shared-state generations, lifecycle/revocation state, privileged-consumer identity, effective crossed-capability and bounded receipt/result binding, deterministic benign review cases, counterfactual boundary controls, alternative-explanation elimination, and SB0–SB5 evidence ceilings.
- `parser-state-machine-analysis` — the twenty-eighth profile, adding input-artifact and parser-instance provenance, phase/state generations, transition identity and first-invalid-transition reasoning, structural-metadata-to-semantic-object binding, explicit recovery/deferred-validation state, nested-parser and cross-record provenance, downstream-consumer identity, effective semantic-capability and bounded receipt/result binding, deterministic benign review cases, counterfactual parser controls, alternative-explanation elimination, and PS0–PS5 evidence ceilings.
- `protocol-state-machine-analysis` — the twenty-ninth profile, adding peer/authenticated-principal provenance, connection/session/role/stream/transaction generations, protocol-version and feature generations, message and transition identity, transition-guard and authenticated-context binding, replay/retry/idempotency state, timeout/cancellation/reset/reconnect and late-completion generations, commit/terminal/cleanup separation, downstream-action and effective protocol-capability binding, deterministic benign review cases, counterfactual protocol controls, alternative-explanation elimination, and PST0–PST5 evidence ceilings.
- `bounds-and-integer-analysis` — the thirtieth profile, adding source-value and object-generation provenance, semantic units, mathematical-versus-machine value binding, width/signedness and cast/promotion/truncation traces, arithmetic-expression identity/generation, check-domain versus allocation/use-domain binding, allocation/object/usable-size separation, index/offset/stride/access-width range equations, aggregate/alignment/nested-size reasoning, downstream invalid-range capability and bounded receipt/result binding, deterministic benign review cases, counterfactual arithmetic controls, alternative-explanation elimination, and BND0–BND5 evidence ceilings.

The boot-chain evidence ladder is deliberately causal: BC0 maps the surface; BC1 observes identity/generation divergence; BC2 demonstrates a deterministic verification or selection-policy mismatch; BC3 requires inert unauthorized acceptance; BC4 requires a bounded reversible synthetic boot effect; and BC5 additionally requires exact root/policy provenance, signer authorization, rollback/freshness generation, selected-to-loaded identity binding, transition/handoff trace, relevant alternate-path controls, meaningful counterfactuals, eliminated alternative explanations, and remediation regression. Secure-boot flags, signature success, measurement entries, attestation, update success, or boot logs cannot skip missing causal bindings.

The deserialization evidence ladder is likewise causal: DT0 maps parser/schema/type/hook/lifecycle surfaces; DT1 observes identity, interpretation, or generation divergence; DT2 demonstrates a controlled reconstruction or policy mismatch; DT3 requires inert wrong-context acceptance; DT4 requires a bounded synthetic authority effect causally bound to the initiating artifact/schema/type/authority tuple; and DT5 additionally requires exact artifact/authenticity context, parser/canonical-field provenance, schema/version, discriminator-to-runtime-type and registry-generation proof, construction/hook/secondary-interpretation trace, requested-to-effective authority binding, privileged-consumer identity, lifecycle controls, receipt/result binding, meaningful counterfactuals, eliminated alternative explanations, and remediation regression. Parser success, suspicious class names, signature validity, hook reachability, crashes, or debug-only permissiveness cannot skip missing causal bindings.

The certificate/hostname evidence ladder is also causal: PKI0 maps endpoint/reference-identity/path/policy/session surfaces; PKI1 observes identity, policy, anchor, callback, or generation divergence; PKI2 demonstrates a controlled verification-policy mismatch; PKI3 requires inert synthetic wrong-peer acceptance by the final application verifier; PKI4 requires a bounded reversible authenticated-session effect or read-only/inert consumer result bound to the exact handshake tuple; and PKI5 additionally requires exact intended peer identity, endpoint/redirect/SNI state, canonical reference identity, verifier configuration, trust-store identity/generation, presented-chain identity, selected path/anchor, certificate-constraint decisions, SAN/hostname binding, pin/revocation/callback final decisions, authenticated peer/session identity, applicable mTLS mapping, lifecycle controls, privileged-consumer identity, receipt/result binding, meaningful counterfactuals, eliminated alternative explanations, and remediation regression. Chain success, signature validity, a certificate fingerprint, pin match, callback reachability, connection success, or a lock icon cannot skip missing causal bindings.

The cryptographic-protocol evidence ladder is likewise causal: CP0 maps protocol-intent, role/session, negotiation, transcript, key-schedule, record, phase, replay, and lifecycle surfaces; CP1 observes a binding, ordering, identity, or generation divergence; CP2 demonstrates a deterministic protocol-policy mismatch; CP3 requires inert synthetic wrong-context acceptance by the final application verifier; CP4 requires a bounded reversible state transition or read-only/inert result correlated to the exact protocol tuple; and CP5 additionally requires the complete causal protocol chain, authenticated-negotiation proof, key-role/direction/epoch and domain-separation proof, nonce/sequence/record identity, protocol-phase authenticated context, auth-before-use ordering, replay/freshness and rekey/resumption generations, privileged-consumer identity, receipt/result binding, meaningful counterfactuals, eliminated alternative explanations, and remediation regression. Primitive approval, signature/tag validity, decrypt success, handshake success, selected-suite logs, unique-looking nonces, replay-cache telemetry, or a crash cannot skip missing causal bindings.

The guest-host evidence ladder is likewise causal: GH0 maps guest principals, interfaces, host consumers, shared objects, translation layers, and lifecycle transitions; GH1 observes identity, generation, ownership, translation, ordering, or lifecycle divergence; GH2 demonstrates a controlled boundary-policy mismatch; GH3 requires inert or read-only wrong-context acceptance by the final host consumer; GH4 requires a bounded reversible owner-controlled host-side marker, synthetic object transition, or read-only result bound to the exact guest/interface/object/generation tuple; and GH5 additionally requires complete guest-principal/interface provenance, device/queue/channel generation, translation/shared-object identity, host-consumer and ownership/lifetime traces, effective host capability, lifecycle/revocation evidence, meaningful counterfactuals, eliminated alternative explanations, receipt/result binding, and remediation regression. A guest crash, host crash, sanitizer finding, mapped page, malformed descriptor, backend callback, emulation-thread execution, or synthetic marker cannot skip missing causal bindings.

The memory-lifetime evidence ladder is likewise causal: ML0 maps logical object identities, acquisition/allocation generations, owners, aliases, release paths, asynchronous work, final consumers, and lifecycle transitions; ML1 observes identity, ownership, refcount, invalidation, reuse, or generation divergence; ML2 demonstrates a controlled lifetime-policy mismatch; ML3 requires inert or read-only wrong-lifetime acceptance by the final synthetic consumer; ML4 requires a bounded reversible owner-controlled marker, synthetic object transition, or read-only result bound to the exact object/alias/release/reuse/consumer generation tuple; and ML5 additionally requires complete object identity, allocation/acquisition generation, ownership/alias and retain/borrow/refcount provenance, invalidation/destruction trace, reuse generation where relevant, callback/work-item and cancellation/teardown identity, final-consumer capability, lifecycle evidence, meaningful counterfactuals, eliminated alternative explanations, receipt/result binding, and remediation regression. Sanitizer output, free/access stacks, crashes, reused addresses/handles, refcount anomalies, queued callbacks, or stale-looking pointers cannot skip missing causal bindings.

The concurrency-race evidence ladder is likewise causal: CR0 maps shared invariants, state identities/generations, actors, scheduler/executor, synchronization, lifecycle transitions, and final consumers; CR1 observes a repeatable scheduling, visibility, generation, or lifecycle divergence; CR2 demonstrates a deterministic ordering, atomicity, serialization, or revalidation-policy mismatch; CR3 requires inert or read-only wrong-order acceptance by the final synthetic consumer; CR4 requires a bounded reversible owner-controlled marker, duplicate inert action, synthetic transition, or read-only result bound to the exact actor/state/interleaving/synchronization tuple; and CR5 additionally requires complete actor/state/generation provenance, scheduler/executor identity, synchronization and happens-before trace, check/use or publication/commit ordering, cancellation/retry/teardown state, final-consumer identity, meaningful counterfactual schedules, eliminated alternative explanations, receipt/result binding, and remediation replay. Flaky timing, race-detector output, thread overlap, timestamps, queue order without a runtime guarantee, or a crash cannot skip missing causal bindings.

The sandbox-boundary evidence ladder is likewise causal: SB0 maps sandbox principals, policies, brokers, inherited/delegated capabilities, namespaces, shared state, privileged consumers, and lifecycle transitions; SB1 observes caller/session, policy, namespace, ownership, generation, or lifecycle divergence; SB2 demonstrates a controlled sandbox-policy, attenuation, identity-binding, namespace-binding, or revocation mismatch; SB3 requires inert or read-only wrong-context acceptance by the final privileged consumer; SB4 requires a bounded reversible synthetic asset, inert privileged marker, read-only result, or owner-controlled state transition bound to the exact principal/policy/request/resource/consumer tuple; and SB5 additionally requires complete principal/policy/request/resource/capability provenance, lifecycle/revocation trace, effective crossed capability, meaningful counterfactual controls, eliminated alternative explanations, receipt/result binding, and remediation replay. Broker reachability, policy configuration, inherited handles, mapped shared memory, sandbox or privileged-service crashes, service code execution, or a synthetic marker cannot skip missing causal bindings.

The parser-state-machine evidence ladder is likewise causal: PS0 maps parser phases, state nodes, trust-promotion points, structural metadata, recovery paths, nested parsers, cross-record references, and downstream consumers; PS1 observes a repeatable phase/state/invariant/recovery divergence; PS2 demonstrates a controlled transition, validation-order, recovery, phase, or deferred-validation mismatch; PS3 requires inert or read-only downstream acceptance of a semantic object produced under the wrong parser state, phase, generation, or validation status; PS4 requires a bounded reversible synthetic marker, read-only result, or owner-controlled semantic transition bound to the exact input/parser/state/transition/object/consumer tuple; and PS5 additionally requires complete input/parser provenance, the first-invalid-transition trace, recovery/deferred-validation state, semantic-object lineage, meaningful counterfactual parser controls, eliminated alternative explanations, receipt/result binding, and remediation replay. Malformed inputs, parser crashes, sanitizer findings, warnings, duplicate records, phase reach, or synthetic markers cannot skip missing causal bindings.

The protocol-state-machine evidence ladder is likewise causal: PST0 maps peers, sessions, connections, streams, transactions, states, transitions, guards, negotiation, retries, lifecycle events, commits, and downstream consumers; PST1 observes a repeatable session, role, transition, replay, lifecycle, ownership, or negotiation divergence; PST2 demonstrates a controlled guard, state-precondition, idempotency, replay, ownership, or lifecycle mismatch; PST3 requires inert or read-only downstream acceptance under the wrong session, role, stream, transaction, retry, negotiation, or lifecycle generation; PST4 requires a bounded reversible synthetic action, inert transition, duplicate marker, read-only result, or owner-controlled commit bound to the exact peer/session/state/message/transition/consumer tuple; and PST5 additionally requires complete peer/session/role/negotiation provenance, the first-illegal-transition trace, replay/retry/lifecycle state, commit/terminal semantics, meaningful counterfactual protocol controls, eliminated alternative explanations, receipt/result binding, and remediation replay. Weird responses, protocol crashes, reordered messages, duplicate IDs, timeouts, reconnects, acknowledgments, or synthetic markers cannot skip missing causal bindings.

The bounds-and-integer evidence ladder is likewise causal: BND0 maps source values, units, representation widths/signedness, arithmetic expressions, checks, objects, and consumers; BND1 observes a repeatable wrap, truncation, signedness, unit, alignment, or endpoint divergence; BND2 demonstrates a controlled check/use mismatch where validation and downstream allocation/access consume different numeric domains, units, widths, endpoints, object sizes, or generations; BND3 requires inert or read-only invalid-range acceptance by a mock range consumer, shadow-memory oracle, bounded assertion, or local sanitizer harness; BND4 requires a bounded reversible synthetic canary, read-only shadow region, fake object, or owner-controlled marker bound to the exact value/arithmetic/check/object/access tuple; and BND5 additionally requires complete value/type/unit/arithmetic provenance, the first representational divergence, exact object/access binding, meaningful counterfactual arithmetic controls, eliminated alternative explanations, receipt/result binding, and remediation replay. Suspicious casts, overflows, crashes, sanitizer findings, allocation failures, or synthetic markers cannot skip missing causal bindings.

This raises the current registry from eight Wave 8 profiles to **thirty CI-enforced profiles** while keeping the Wave 8 history intact. Wave 10 profiles apply the same common operator-depth contract and add domain-specific causal reasoning rather than payload volume or checklist length.

Future Wave 10 promotions must follow the same rule: depth is added only when a dedicated test can freeze meaningful reasoning semantics and the machine-readable matrix remains deterministic, benign, evidence-first, and portable.

## Adding a future profile

1. Deepen an existing canonical skill rather than creating a near-duplicate capability.
2. Add a domain-specific `references/operator-runbook.md`.
3. Add at least three distinct deterministic JSON review cases under the skill's `references/` directory.
4. Register both artifacts in `operator-depth/profiles.json` with `lab_only: true`.
5. Include all required runbook sections and scenario fields.
6. Run the operator-depth validator and the complete repository test/benchmark stack.
7. Review the diff for copied payload corpora, vendor lock-in, duplicated canonical prose, unsafe proof mechanisms, and weakened authorization/evidence language.

Operator depth remains deliberately selective. A profile belongs here only when deeper methodology materially improves research quality and can be kept deterministic, evidence-first, portable, and safely bounded.