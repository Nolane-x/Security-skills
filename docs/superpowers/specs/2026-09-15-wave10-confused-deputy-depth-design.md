# Wave 10 Confused Deputy Depth Design

## Goal

Deepen `confused-deputy-analysis` from a caller/deputy checklist into a causal authority-transfer analysis that can distinguish authentication, delegation, attenuation, deputy ambient privilege, resolved target identity, bounded effect, and result binding with deterministic evidence ceilings.

## Baseline

This work starts from `main@be7a59bf725949eaceb346894b4c2a6f53093577`, where Wave 10 operator-depth profile #13 (`canonicalization-and-namespace-analysis`) is merged and post-merge verified. The current operator-depth registry contains 13 profiles.

## Scope

The change deepens one existing canonical skill and adds one operator-depth profile. It may change only:

1. `skills/confused-deputy-analysis/SKILL.md`
2. `skills/confused-deputy-analysis/references/operator-runbook.md`
3. `skills/confused-deputy-analysis/references/operator-review-cases.json`
4. `operator-depth/profiles.json`
5. `tests/test_confused_deputy_depth.py`
6. `docs/operator-depth-contract.md`
7. `README.md`
8. this design specification
9. `docs/superpowers/plans/2026-09-15-wave10-confused-deputy-depth.md`

The change MUST NOT modify `skill.meta.json`, graph edges, packs, routing domains, benchmark fixtures or thresholds, agent-eval authority, or superiority-court authority.

## Ownership boundary

`confused-deputy-analysis` owns authority transfer through a privileged intermediary: who initiated the action, what authority was actually delegated, what ambient authority the deputy possesses, how authority is attenuated, what operation/resource is authorized, what target identity is resolved, and whether the bounded result is bound back to the initiating request.

It does not replace:

- `authorization-boundary-analysis`, which owns general subject-action-resource authorization reasoning;
- `connector-plugin-trust-analysis`, which owns integration identity, publisher/install/update provenance, connector permission grants, schema provenance, and connector lifecycle;
- `tool-capability-and-confirmation-analysis`, which owns action proposal, normalized arguments, confirmation snapshots, execution binding, receipt/final-state semantics, retry/idempotency, and rollback;
- `canonicalization-and-namespace-analysis`, which owns representation-to-resolved-object identity consistency;
- `cloud-iam-path-analysis`, which owns cloud-specific IAM path semantics.

The confused-deputy profile composes with these skills when a deputy path crosses those boundaries, but does not duplicate their full methodology.

## Causal authority-transfer model

The canonical chain is:

`request origin -> authenticated principal -> initiating authority -> delegation artifact -> requested operation -> requested resource -> deputy identity -> deputy ambient authority -> policy decision -> attenuated effective authority -> resolved target identity -> bounded effect -> receipt/result binding`

The analysis must record each transition independently. A strong identity assertion at one transition does not prove the authority of a later transition.

### Core distinctions

The skill must distinguish:

- request origin from authenticated principal;
- authenticated principal from initiating authority;
- initiating authority from authority encoded in a delegation artifact;
- delegated authority from deputy ambient authority;
- requested operation from the operation actually authorized;
- requested resource from the resource actually resolved;
- policy acceptance from accepted bounded effect;
- bounded effect from result/receipt binding to the initiating request.

The canonical inequality is:

`authenticated principal != delegated authority != deputy ambient authority != attenuated effective authority`

unless evidence proves those authority sets are intentionally equivalent for the exact operation and resource.

## Authority conservation and attenuation invariants

A deputy path is acceptable only when all applicable invariants hold:

1. Every privileged effect has a traceable initiating principal and request generation.
2. Effective authority is no broader than the union of explicitly delegated authority and independently justified service policy for the exact operation/resource.
3. Deputy ambient authority is not silently inherited by the caller.
4. Delegation binds the operation, resource/target identity, tenant or namespace where relevant, lifetime/generation, and any material constraints required by policy.
5. Multi-hop delegation is monotonically attenuating unless an explicitly documented authority expansion is independently authorized by a different principal/policy boundary.
6. Per-operation authorization is re-evaluated when the requested operation or resolved target changes materially.
7. The resource identity used by policy is equivalent to the identity resolved by the sink, or the handoff is bound to an immutable object/handle.
8. Results, receipts, callbacks, and durable state observations are correlated to the same initiating principal, request generation, operation, and target identity.
9. Revocation, expiry, or delegation-generation changes invalidate later use according to the documented lifecycle contract.
10. A remediation must preserve legitimate neighboring callers and delegated operations while removing the incorrect authority transfer.

## Delegation model

Treat delegation as a structured authority object, not a boolean “trusted caller” flag. Record at minimum:

- issuer or authority source;
- initiating principal;
- deputy identity;
- operation class;
- resource/target scope;
- tenant/namespace scope where relevant;
- material constraints;
- generation/version;
- issue and expiry/revocation state;
- whether further delegation is allowed;
- attenuation rule across the next hop.

The operator should compare declared delegation to effective authority at execution. A credential, connection, signer, process image, or host identity can authenticate a channel without authorizing a particular privileged action.

## Multi-hop authority trace

For brokered or chained systems, record each hop as:

`incoming principal -> incoming delegated authority -> local policy -> local ambient authority -> outgoing delegated authority -> next-hop target`

The analysis must detect authority amplification, context loss, principal substitution, operation/resource drift, and result misbinding without relying on destructive effects.

## Deputy ambient authority

Ambient deputy privilege is evidence about maximum capability, not caller authorization. The review must identify which privileges are always available to the deputy and which subset is intentionally exposed for the current request.

The proof obligation is the attenuation boundary: show how the system derives an effective authority set for the request rather than assuming the deputy’s full identity or role is acceptable.

## Policy and target binding

Authorization must bind at least:

`initiating principal + delegation generation + operation + resolved resource identity + relevant tenant/namespace + material request constraints`

If authorization occurs before target resolution, the analysis must prove policy equivalence to sink resolution or an immutable target binding. This is where `canonicalization-and-namespace-analysis` composes with the deputy profile.

## Result and receipt binding

A successful privileged action is not sufficient evidence by itself. The operator must determine whether the observed result, callback, receipt, or post-action state is attributable to the exact initiating request and effective authority tuple.

Result binding records:

- initiating principal;
- request/delegation generation;
- deputy identity;
- operation;
- resolved target identity;
- accepted bounded effect;
- receipt/result identity;
- post-action state observation where relevant.

## Counterfactual proof

At least one controlled counterfactual must change exactly one security-relevant authority dimension while holding the rest constant. Useful defensive controls include:

- same principal, narrower delegation;
- same delegation, different operation;
- same operation, neighboring synthetic resource;
- same request, different delegation generation;
- same deputy path, no ambient privilege beyond the delegated subset;
- same bounded effect oracle with a properly attenuated policy.

The purpose is to prove which authority transition caused the divergence rather than merely correlating a privileged component with an outcome.

## Alternative explanations

Before promoting evidence, explicitly consider at least:

- independent downstream authorization not visible at the first deputy;
- cached policy or stale delegation generation;
- different resolved target identity;
- test-fixture contamination between synthetic principals;
- result/receipt correlation error;
- retry or duplicate-delivery behavior;
- background worker identity replacing the original principal by design;
- intentionally global service behavior independent of caller authority.

## Deputy evidence ladder

Evidence is capped at the highest directly demonstrated level:

- **D0 — surface only:** a privileged deputy, delegation mechanism, or broad role exists, but no security-relevant authority divergence is demonstrated.
- **D1 — authority-context divergence:** two synthetic requests produce different principal/delegation/operation/resource context, but policy still rejects the unauthorized path or no accepted bounded effect occurs.
- **D2 — policy or attenuation divergence:** deterministic synthetic policy evaluation authorizes a tuple outside the intended delegation/attenuation contract, without relying on a real privileged effect.
- **D3 — inert deputy acceptance:** an owned mock/read-only deputy accepts an operation or resolved target outside the intended effective authority set and exposes a deterministic inert marker/result.
- **D4 — bounded synthetic effect:** a reversible or inert owner-controlled state change/read-back proves that the wrong authority tuple caused the deputy to act on the wrong permitted synthetic target or operation.
- **D5 — causal lifecycle proof:** the defect reproduces across counterfactual controls and includes multi-hop, delegation-generation/revocation, or result-binding evidence plus a remediation regression proving correct attenuation without breaking legitimate neighboring behavior.

Never report above the directly demonstrated level.

## Evidence ceiling

The operator must state both `evidence_level` and `evidence_ceiling`. The ceiling is constrained by missing proof. Examples:

- no accepted bounded effect: ceiling D2;
- inert mock acceptance only: ceiling D3;
- bounded synthetic effect without lifecycle/counterfactual proof: ceiling D4;
- D5 requires repeatable causal controls and remediation regression evidence.

## Deterministic audit review cases

Create exactly defensive/synthetic review artifacts under `references/operator-review-cases.json`. At least three scenarios are required:

1. `principal-authority-binding` — tests whether authenticated principal, initiating authority, delegation, operation, and resource remain bound through the deputy policy decision.
2. `delegation-attenuation-consistency` — tests that deputy ambient authority is narrowed monotonically and that a neighboring operation/resource does not inherit broader authority.
3. `deputy-result-binding` — tests that inert result/receipt/post-action evidence is correlated to the same request/delegation generation and resolved target.

Every scenario must include:

- `hypothesis`
- `safe_oracle`
- `positive_control`
- `negative_control`
- `stop_condition`
- `remediation_oracle`
- `request_origin`
- `authenticated_principal`
- `initiating_authority`
- `delegation_artifact`
- `requested_operation`
- `requested_resource`
- `deputy_identity`
- `deputy_ambient_authority`
- `policy_decision`
- `attenuated_effective_authority`
- `resolved_target_identity`
- `bounded_effect`
- `result_binding`
- `delegation_generation`
- `counterfactual_control`
- `alternative_explanation`
- `evidence_level`
- `evidence_ceiling`

Every field must be a substantive string. Dynamic cases are restricted to synthetic principals, mock/read-only deputies, inert markers, or reversible owner-controlled state. No real credentials, persistence, destructive action, evasion, malware, or third-party effects are permitted.

## Operator runbook

The runbook must include the registry-required sections plus deputy-specific reasoning sections:

- Attack surface
- Hypothesis matrix
- Authority-transfer trace
- Delegation trace
- Ambient-authority and attenuation trace
- Operation/resource binding
- Multi-hop authority trace
- Target identity binding
- Result and receipt binding
- Delegation generation and lifecycle trace
- Controlled validation
- False-positive controls
- Counterfactual controls
- Evidence capture
- Evidence promotion and ceiling
- Remediation checks

## Dedicated TDD contract

Add `tests/test_confused_deputy_depth.py` first. It must fail before implementation for exactly four intended reasons:

1. missing canonical authority-transfer depth;
2. missing operator runbook;
3. missing deterministic review-case matrix;
4. missing profile #14 registry entry.

The test must use `assertGreaterEqual(len(profiles), 14)` and must never own the exact global registry count.

## Registry contract

Register `confused-deputy-analysis` once with:

- `runbook`: `references/operator-runbook.md`
- `scenario_matrix`: `references/operator-review-cases.json`
- `lab_only`: `true`
- the existing six required runbook sections unchanged.

Keep registry schema version `2`.

## Documentation gate

Do not update README or `docs/operator-depth-contract.md` until behavioral implementation and registry have passed the full CI matrix plus all three core determinism jobs. Public documentation is the last code-tree change before exact-head verification.

## Verification gates

The implementation is not complete until all of the following are proven on a fixed SHA:

1. RED dedicated test provenance exists and shows only the four intended assertion failures with zero unittest errors.
2. Behavioral GREEN passes Ubuntu/macOS/Windows × Python 3.11/3.13.
3. `benchmark-core` passes double-run byte-identical checks.
4. `agent-eval-core` passes deterministic tasks/evals/matrix plus cautious/faulty controls.
5. `superiority-court-core` passes deterministic contestant views/tasks/scores/court.
6. Changed-file scope is exactly the nine intended paths.
7. Exact-head CI passes all gates on the final SHA.
8. Merge uses an expected-head guard.
9. Push-triggered post-merge CI passes the same matrix and core gates on merged `main`.

## Claim boundary

This profile strengthens causal authority-transfer reasoning. It does not by itself establish empirical superiority over Claude-Red or another external system. Such a claim requires a real contestant run through the existing superiority court.