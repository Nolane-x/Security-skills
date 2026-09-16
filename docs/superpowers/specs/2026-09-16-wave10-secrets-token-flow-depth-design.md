# Wave 10 Secrets and Token Flow Depth Design

## Status

Approved design for Wave 10 operator-depth profile #16. Base: `main@7077edaa96853309530f39002467d1df1348dc8e`.

## Goal

Deepen the existing canonical `secrets-and-token-flow-analysis` skill from a credential inventory/checklist into a causal credential-authority method that can distinguish benign secret propagation from security-relevant authority confusion, token-class misuse, verifier-context mismatch, delegation broadening, stale lifecycle state, and revocation drift using deterministic, synthetic, evidence-bounded review artifacts.

The profile treats a credential as both sensitive data and a representation of authority. Review therefore follows both confidentiality flow and authority flow, but promotes evidence only from bounded, directly observed causal links.

## Non-goals

- Do not create a new canonical skill.
- Do not change `skill.meta.json`, graph edges, packs, routing domains, benchmark fixtures/thresholds, agent-eval authority, or superiority-court authority.
- Do not collect, replay, expose, or persist real credentials or third-party secrets.
- Do not add credential dumping, phishing, token theft, session hijacking, evasion, malware, persistence, destructive actions, or unauthorized testing guidance.
- Do not claim empirical superiority over Claude-Red or any external system without an actual contestant run through the repository superiority court.

## Scope

Exactly these nine paths are intended:

1. `README.md`
2. `docs/operator-depth-contract.md`
3. `docs/superpowers/specs/2026-09-16-wave10-secrets-token-flow-depth-design.md`
4. `docs/superpowers/plans/2026-09-16-wave10-secrets-token-flow-depth.md`
5. `operator-depth/profiles.json`
6. `skills/secrets-and-token-flow-analysis/SKILL.md`
7. `skills/secrets-and-token-flow-analysis/references/operator-review-cases.json`
8. `skills/secrets-and-token-flow-analysis/references/operator-runbook.md`
9. `tests/test_secrets_token_flow_depth.py`

The registry schema remains version `2`. Public docs are synchronized only after behavioral GREEN.

## Causal credential-authority model

The canonical reasoning chain is:

`credential origin -> issuer identity -> subject identity -> credential class -> issuance constraints -> possession channel -> storage representation -> propagation hop -> verifier identity -> verification decision -> audience/resource binding -> represented authority -> downstream exchange/delegation -> attenuated effective authority -> bounded action/result -> lifecycle/revocation generation`

The method treats each acceptance of a credential as a security claim: not merely that bytes parse or a signature verifies, but that the credential class, issuer, subject, audience, resource, lifecycle generation, possession semantics, and represented authority are valid for the exact verifier decision being made.

## Core distinctions

The skill must make these distinctions explicit:

- secret bytes != authority semantics;
- issuer identity != subject identity;
- possession != permission;
- syntactic validity != verification success;
- valid signature/MAC != valid authorization context;
- identity token != access token;
- access token != refresh token;
- bearer credential != proof-of-possession credential;
- delegated authority != deputy/downstream ambient authority;
- audience validity != resource authorization;
- expiry time != revocation generation;
- storage location != intended propagation boundary;
- credential acceptance != proof that downstream action/result is bound to the same authority context.

## Core invariants

1. Every credential acceptance has traceable provenance to an authorized issuer or credential origin appropriate for the credential class.
2. The verifier validates the credential class expected by the interface; one token class must not silently substitute for another without an explicit conversion/exchange contract.
3. Issuer, subject, audience, resource, tenant/namespace when relevant, scopes/roles/capabilities, lifetime, generation, and sender/channel binding are checked according to the exact credential semantics.
4. Signature or MAC validation is necessary only where the credential class requires it and is never treated as sufficient authorization by itself.
5. Represented authority is no broader than the authority explicitly encoded or independently granted for the exact verifier/resource context.
6. Credential exchange/delegation monotonically attenuates authority unless a distinct, documented authority boundary independently authorizes expansion.
7. Propagation through headers, RPC metadata, redirects, queues/jobs, caches, logs, telemetry, build artifacts, or browser/process storage does not change credential semantics or silently cross an unauthorized trust boundary.
8. Lifecycle generation advances on rotation, refresh-token replacement, logout/session invalidation, subject disablement, issuer-key generation changes, explicit revocation, or other contract-defined invalidation events.
9. A credential from an invalidated generation is not accepted later merely because its timestamp has not expired, except when the system contract explicitly defines bounded delayed revocation and the evidence reflects that limit.
10. Result/receipt/post-state binding correlates the accepted credential, effective authority, exact resource/action, and lifecycle generation to the observed bounded effect.
11. Remediation removes the incorrect acceptance/propagation/authority transfer while preserving legitimate neighboring credential flows.
12. Evidence level never exceeds the strongest directly captured causal link.

## Credential-class model

The operator records the credential class before reasoning about verification. Supported semantic classes include, when applicable:

- bearer access token;
- proof-of-possession token;
- identity token;
- refresh token;
- session identifier;
- signing key or verification-key reference;
- API key/service credential;
- workload/service identity;
- capability URL or signed resource URL;
- one-time reset/verification token;
- delegated/downstream token produced by token exchange.

The review does not infer class from string shape alone. Class comes from the issuing and verifying contract.

## Issuance provenance and binding

For each synthetic credential flow, capture:

- credential origin/issuer;
- issuer generation or key generation when relevant;
- subject identity;
- intended recipient/verifier;
- credential class;
- audience/resource binding;
- tenant/namespace binding when relevant;
- encoded scopes/roles/capabilities;
- issue time and expiry/lifetime;
- nonce/session/sender/channel binding where applicable;
- refresh/rotation lineage when applicable;
- whether further exchange/delegation is permitted.

A token that is well-formed but lacks provenance to the expected issuer or intended semantic class does not satisfy the authority contract.

## Possession, storage, and propagation trace

The method records how a credential becomes available to a component and whether that path is intended. Relevant representations include:

- secure cookie or session store;
- browser storage when applicable;
- process memory or environment;
- secret manager or protected file;
- database/cache representation;
- HTTP headers;
- query/redirect parameters where a documented flow uses them;
- IPC/RPC metadata;
- queues/background jobs;
- CI/build/test artifacts;
- logs, telemetry, crash reports, or diagnostics.

The profile never requires exposing credential values. Synthetic identifiers, redacted fingerprints, issuer-generated canaries, or opaque fixture IDs are sufficient for evidence.

## Verification-decision trace

The operator records the exact verifier and decision boundary:

`received credential -> parser/classification -> cryptographic verification where required -> issuer check -> subject check -> audience/resource check -> tenant/namespace check -> lifetime/generation check -> sender/channel/nonce check where required -> scope/capability interpretation -> policy decision -> effective authority`

Each skipped check must either be proven irrelevant to that credential class or documented as a contract gap. The method distinguishes parser acceptance from cryptographic verification, cryptographic verification from semantic verification, and semantic verification from authorization.

## Token-class integrity

The review tests whether interfaces require the intended credential class. Examples of safe synthetic distinctions include:

- identity token presented where an access token is required;
- refresh token presented to a normal resource verifier;
- access token accepted where a one-time capability/reset token is required;
- bearer semantics substituted for a proof-of-possession contract;
- one audience/resource token replayed to a neighboring synthetic verifier;
- a downstream/exchanged token interpreted as the broader upstream credential.

These are tested only with synthetic credentials and mock/read-only verifier paths.

## Authority representation and attenuation

For every hop, capture:

`incoming authority -> local verification/policy -> local ambient authority -> outgoing/exchanged authority -> next verifier/resource`

The review must distinguish authority represented by the credential from privileges available to the service itself. A service's ambient authority must not silently leak into the downstream credential on behalf of a caller.

When exchange/delegation is permitted, the outgoing token should be no broader than the incoming represented authority plus any explicitly independent service policy required for the exact operation/resource. Any expansion must be attributable to a separate, documented authority boundary rather than accidental inheritance.

## Lifecycle, rotation, and revocation generation

Timestamp validity and revocation are modeled separately. Track:

- issuance generation;
- signing/verification key generation where relevant;
- refresh-token generation/rotation lineage;
- session generation;
- explicit revocation generation;
- subject/account/service disablement generation when relevant;
- logout/session invalidation;
- cache of verifier decisions or introspection responses;
- bounded propagation delay if the contract allows asynchronous revocation.

Controls compare same token bytes or same logical credential identity across lifecycle generations using synthetic fixtures. Evidence must distinguish stale verifier cache from actual credential acceptance logic.

## Counterfactual proof

Use one-dimension-at-a-time synthetic controls:

- same issuer/class, different subject;
- same subject, different audience;
- same audience, neighboring synthetic resource;
- same credential bytes/fixture identity, advanced revocation generation;
- same request, different credential class;
- same represented authority, narrower downstream exchange;
- same credential, different verifier identity;
- same verifier path with reduced local ambient privilege;
- same flow after remediation with intended neighboring credential still accepted.

Counterfactuals must use synthetic identities, mock verifier decisions, inert markers, or reversible owner-controlled state.

## Alternative explanations

Before promoting evidence, rule out or record:

- fixture accidentally using a different issuer or signing key;
- stale verifier/introspection cache;
- clock skew or deterministic test-time mismatch;
- different resolved audience/resource than assumed;
- retry/duplicate delivery;
- intentionally global service identity used by documented design;
- background-worker identity substitution explicitly required by the service contract;
- token exchange occurring at an unobserved upstream hop;
- parser normalization producing a different synthetic credential representation;
- correlation error between credential acceptance and observed result;
- delayed revocation explicitly permitted by a bounded lifecycle contract;
- synthetic fixture contamination or credential reuse across test cases.

## Evidence ladder S0-S5

- **S0 — credential surface:** a credential, token, session, key, capability reference, or issuance/verification path is identified; no security-relevant divergence is established.
- **S1 — binding/flow divergence:** issuance, storage, propagation, verifier expectation, token class, audience/resource, scope, or lifecycle metadata diverges from the documented contract, but incorrect acceptance is not yet observed.
- **S2 — verifier-context mismatch:** controlled synthetic evidence shows that two credentials/contexts that should be distinguished converge at a verifier decision, or that a required semantic binding is absent, without demonstrating an accepted bounded effect.
- **S3 — inert wrong-context acceptance:** a synthetic credential is accepted by a mock/read-only/inert verifier in a token class, audience/resource, subject, verifier, or lifecycle context where the oracle expects rejection.
- **S4 — bounded synthetic authority effect:** the wrong-context acceptance produces a bounded, reversible, owner-controlled security-relevant action/result in the synthetic fixture.
- **S5 — causal lifecycle/authority proof:** S4 plus issuance provenance, verifier-decision trace, credential-class integrity, downstream exchange/attenuation trace where applicable, revocation-generation control, alternative-explanation elimination, remediation, and regression evidence preserving legitimate neighboring credential flows.

The evidence ceiling is the highest level directly supported by captured artifacts. A reviewer must never infer S4/S5 from secret exposure, token parsing, signature validity, or suspicious configuration alone.

## Deterministic review cases

### 1. `issuance-verification-binding`

Tests whether issuer, subject, token class, audience/resource, tenant/namespace where relevant, lifetime/generation, and sender/channel/nonce constraints remain bound at the verifier decision. Controls vary one synthetic binding at a time while keeping unrelated state fixed. The remediation oracle restores exact binding and preserves the correct neighboring credential.

### 2. `propagation-and-token-class-integrity`

Tests whether credential semantics remain stable across controlled propagation hops and whether one credential class is incorrectly accepted as another. The case uses synthetic opaque credentials, inert verifier markers, and safe propagation fixtures rather than real credential values. The remediation oracle rejects wrong-class/wrong-boundary use while preserving intended propagation.

### 3. `delegation-attenuation-and-revocation`

Tests downstream exchange/delegation attenuation, ambient-authority separation, lifecycle generation, refresh/rotation lineage, and revocation behavior. Controls compare narrower downstream authority, reduced local ambient privilege, and advanced synthetic revocation generation. The remediation oracle prevents stale or broadened authority from being accepted while preserving valid same-generation, properly attenuated flows.

Each scenario must provide strings for at least:

- `hypothesis`
- `safe_oracle`
- `positive_control`
- `negative_control`
- `stop_condition`
- `remediation_oracle`
- `credential_origin`
- `issuer_identity`
- `subject_identity`
- `credential_class`
- `issuance_constraints`
- `possession_channel`
- `storage_representation`
- `propagation_hop`
- `verifier_identity`
- `verification_decision`
- `audience_resource_binding`
- `represented_authority`
- `downstream_exchange`
- `attenuated_effective_authority`
- `bounded_result`
- `lifecycle_generation`
- `revocation_generation`
- `token_class_control`
- `counterfactual_control`
- `alternative_explanation`
- `evidence_level`
- `evidence_ceiling`

## Operator runbook

The runbook must contain the common required sections plus credential-specific sections:

- Attack surface
- Hypothesis matrix
- Credential-class trace
- Issuance provenance trace
- Possession and storage trace
- Propagation-boundary trace
- Verifier-decision trace
- Audience and resource binding
- Authority representation trace
- Delegation and attenuation trace
- Lifecycle and revocation-generation trace
- Result and receipt binding
- Controlled validation
- False-positive controls
- Counterfactual controls
- Evidence capture
- Evidence promotion and ceiling
- Remediation checks

## Dedicated test contract

`tests/test_secrets_token_flow_depth.py` will freeze four things:

1. `SKILL.md` exposes the causal credential-authority model, core distinctions/invariants, token-class integrity, authority attenuation, lifecycle/revocation generation, S0-S5 ladder, counterfactual proof, alternative explanations, and evidence ceiling.
2. The operator runbook contains all credential-specific transition-level reasoning sections.
3. The machine-readable review cases contain at least three deterministic scenarios and every required issuance/verification/authority/lifecycle field with substantive content.
4. `operator-depth/profiles.json` contains exactly one additive registration for `secrets-and-token-flow-analysis` using the existing runbook/scenario paths and `lab_only: true`, while the total profile assertion remains additive (`>= 16`).

## TDD and verification sequence

1. Commit this design spec on the isolated branch.
2. Commit the implementation plan.
3. Add only the dedicated test and run CI to obtain a clean RED caused by the missing depth artifacts/profile registration.
4. Implement the skill, runbook, review cases, and additive registry entry.
5. Obtain behavioral GREEN on the full repository workflow.
6. Only after behavioral GREEN, synchronize README and `docs/operator-depth-contract.md` to 16 profiles.
7. Run exact-head full CI on the final candidate.
8. Review changed-file scope and provenance.
9. Mark Ready and merge only with an expected-head SHA guard.
10. Require post-merge push CI on the merge commit: all six matrix jobs plus `benchmark-core`, `agent-eval-core`, and `superiority-court-core` must succeed.

## Safety boundary

All dynamic examples and review cases use synthetic/test credentials, synthetic principals/tenants, deterministic mock issuers/verifiers, inert capability markers, read-only services, policy simulators, or reversible owner-controlled state. Real credentials, production sessions, third-party tokens, credential replay against external systems, destructive actions, persistence mechanisms, evasion, malware, and unauthorized targets are prohibited.
