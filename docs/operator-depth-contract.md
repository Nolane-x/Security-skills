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
- `supply-chain-dependency-review` — the eighteenth profile, adding source/namespace resolution, immutable artifact identity, integrity/signature/provenance-verifier reasoning, build-hook and toolchain identity, CI trust and cache/reuse binding, produced-to-released-to-distributed-to-deployed artifact identity, release/signing/publishing authority, lifecycle/revocation/update generations, deterministic audit-only review cases, counterfactual controls, and SC0–SC5 evidence ceilings.

This raises the current registry from eight Wave 8 profiles to **eighteen CI-enforced profiles** while keeping the Wave 8 history intact. Wave 10 profiles apply the same common operator-depth contract and add domain-specific causal reasoning rather than payload volume or checklist length.

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
