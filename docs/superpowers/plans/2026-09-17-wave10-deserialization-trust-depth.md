# Wave 10 Profile #21 — Deserialization Trust Depth Implementation Plan

> Execution authority: implement this plan on branch `wave10-profile21-deserialization-trust-depth`, based on exact `main@e4979d27272ea059464b9285b5e452643b8f36f1`. Do not merge if any gate below is incomplete.

**Goal:** deepen the existing `deserialization-trust-analysis` canonical skill into the twenty-first CI-enforced operator-depth profile with deterministic causal reconstruction-trust reasoning and a DT0–DT5 evidence ceiling.

**Architecture:** preserve the repository's existing canonical-skill + operator-runbook + machine-readable review-case pattern. Add one additive registry entry only. Freeze semantics with a dedicated test before production artifacts, then require behavioral full GREEN before public docs, exact-head full GREEN before guarded merge, and post-merge full GREEN before closure.

**Safety:** all proof mechanisms remain local/owned/sandboxed/synthetic/benchmark/explicitly authorized. Use inert callback markers, mock type/plugin registries, read-only synthetic capabilities, or bounded reversible owner-controlled effects. Do not introduce gadget-chain development, command execution, arbitrary file writes, external network effects, credential theft, persistence, malware, destructive actions, evasion, public-registry manipulation, or unauthorized target interaction.

---

## Task 1 — Freeze the dedicated semantic contract first

**Create:** `tests/test_deserialization_trust_depth.py`

The test must fail before production implementation and freeze four semantic groups.

### 1A. Canonical skill contract

Require the canonical `SKILL.md` to contain substantive semantics for:

- full reconstruction causal chain from artifact origin to lifecycle generation;
- parser/schema/runtime-type separation;
- discriminator/alias versus canonical runtime type identity;
- registry/resolver identity and generation;
- payload authenticity versus reconstruction authorization;
- construction versus side-effect authorization;
- hook/secondary-interpretation boundaries;
- requested versus effective reconstructed authority;
- privileged-consumer and receipt/result binding;
- stale schema/registry/policy/object generation controls;
- DT0–DT5 evidence ladder and evidence ceiling;
- transition-specific counterfactuals and alternative explanations;
- explicit benign/synthetic safety boundary.

### 1B. Runbook contract

Require the common second-level sections exactly:

- `Attack surface`
- `Hypothesis matrix`
- `Controlled validation`
- `False-positive controls`
- `Evidence capture`
- `Remediation checks`

Also require domain methodology for artifact/authenticity trace, parser/canonical fields, schema/version, discriminator/registry resolution, runtime type/object construction, hook/secondary interpretation, authority/reconstruction policy, privileged consumer/result, lifecycle generations, counterfactuals, alternatives, and evidence promotion/ceiling.

### 1C. Review-case contract

Require at least three cases and specifically:

- `type-registry-binding`
- `construction-hook-capability-binding`
- `schema-registry-generation-binding`

Each case must include common fields:

- `id`
- `hypothesis`
- `safe_oracle`
- `positive_control`
- `negative_control`
- `stop_condition`
- `remediation_oracle`

And substantive domain fields:

- `artifact_origin`
- `envelope_authentication_context`
- `format_parser_identity`
- `canonical_field_state`
- `schema_identity_version`
- `discriminator_state`
- `registry_resolver_identity`
- `registry_generation`
- `runtime_type_identity`
- `object_construction_path`
- `hook_callback_surface`
- `secondary_interpretation`
- `authority_context`
- `requested_reconstructed_capability`
- `policy_decision`
- `effective_reconstructed_authority`
- `privileged_consumer`
- `bounded_result`
- `receipt_result_binding`
- `lifecycle_generation`
- `counterfactual_control`
- `alternative_explanation`
- `evidence_level`
- `evidence_ceiling`

Require substantive strings rather than placeholders, safe benign proof language, explicit stop/abort wording, and DT-level evidence ceilings.

### 1D. Registry contract

Require:

- registry schema/version remains `2`;
- exact profile count increases from 20 to 21;
- exactly one `deserialization-trust-analysis` entry;
- `runbook = references/operator-runbook.md`;
- `scenario_matrix = references/operator-review-cases.json`;
- `lab_only = true`;
- common required runbook sections unchanged.

**Commit:** test-only semantic contract.

---

## Task 2 — Open Draft PR at exact test-first SHA and validate RED

1. Record exact test-first branch SHA.
2. Open Draft PR to `main` before adding production artifacts.
3. Run CI naturally from the PR.
4. RED is valid only when the new dedicated contract is the cause of failure and no unexpected unittest/runtime error masks it.
5. Confirm pre-existing canonical-skill, 20-profile operator-depth, graph/index, benchmark, portability, agent-eval, and superiority-court authorities remain intact before the dedicated failure where observable.
6. Do not weaken the dedicated test after valid RED merely to fit incomplete implementation.

Record RED run ID and failure shape in the PR body.

---

## Task 3 — Implement the canonical causal model

**Modify:** `skills/deserialization-trust-analysis/SKILL.md`

Deepen the existing portable skill rather than replacing it with a runbook dump.

Required additions:

1. causal reconstruction chain;
2. explicit distinctions/invariants;
3. reconstruction identity tuple;
4. registry/resolver generation semantics;
5. authenticity versus represented authority;
6. construction/hook/secondary-interpretation transitions;
7. effective authority and privileged-consumer binding;
8. lifecycle generation reasoning;
9. DT0–DT5 evidence ladder;
10. counterfactual discipline;
11. alternative-explanation discipline;
12. evidence ceiling;
13. remediation regression requirements;
14. local/owned/synthetic safety boundary.

Avoid duplicating large runbook procedures in `SKILL.md`; keep it portable and reasoning-focused.

---

## Task 4 — Add transition-level operator runbook

**Create:** `skills/deserialization-trust-analysis/references/operator-runbook.md`

The runbook must operationalize the design without unsafe exploitation detail.

Include:

- common mandatory sections;
- artifact origin/authenticity trace;
- parser and canonical-field trace;
- schema identity/version trace;
- discriminator/registry-resolution trace;
- canonical runtime-type and object-construction trace;
- hook/callback/secondary-interpretation trace;
- authority and reconstruction-policy trace;
- privileged-consumer/result trace;
- lifecycle/schema/registry/policy generation trace;
- controlled validation using benign markers/mock registries/read-only capabilities;
- paired false-positive controls;
- transition-level counterfactuals;
- alternative explanations;
- evidence promotion DT0–DT5 and ceiling;
- remediation regression preserving intended data-only/explicit-schema behavior.

No gadget recipes, shell commands for exploitation, arbitrary write/network proofs, persistence, or destructive effects.

---

## Task 5 — Add deterministic benign review cases

**Create:** `skills/deserialization-trust-analysis/references/operator-review-cases.json`

Use JSON version `1` and at least three cases.

### Case A — type-registry binding

Synthetic artifact + schema + alias/discriminator + mock resolver. Hold bytes/schema constant and vary resolver/registry generation or canonical runtime type. Prove pre-resolution text cannot stand in for final type identity.

### Case B — construction-hook capability binding

Authenticated/syntactically valid synthetic object. Use inert post-load/callback marker. Prove represented sender authority and reconstruction policy do or do not authorize behavior acquisition. Include safe data-only neighboring positive control.

### Case C — schema-registry generation binding

Persisted synthetic state crosses schema/registry/policy generation. Prove stale reconstruction authority is invalidated while current explicit-schema/data-only flow still works.

For every case:

- safe oracle must name synthetic/mock/inert/read-only/controlled mechanism;
- stop condition must explicitly stop/abort before harmful effects;
- counterfactual isolates one transition;
- alternative explanation is plausible and independently bounded;
- remediation oracle proves both failure closure and neighboring legitimate behavior preservation.

---

## Task 6 — Add exactly one registry entry

**Modify:** `operator-depth/profiles.json`

Add one alphabetically consistent `deserialization-trust-analysis` profile with:

```json
{
  "skill": "deserialization-trust-analysis",
  "runbook": "references/operator-runbook.md",
  "scenario_matrix": "references/operator-review-cases.json",
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

Do not change schema version or unrelated entries.

---

## Task 7 — Behavioral verification gate

After Tasks 3–6 are implemented, run/observe the full repository CI on the behavioral head.

Required GREEN:

- Ubuntu Python 3.11;
- Ubuntu Python 3.13;
- macOS Python 3.11;
- macOS Python 3.13;
- Windows Python 3.11;
- Windows Python 3.13;
- `benchmark-core`;
- `agent-eval-core`;
- `superiority-court-core`.

Also require deterministic byte-identical checks and cautious/faulty controls where the workflow provides them.

If any gate fails, investigate root cause and correct the production artifact. Do not edit the dedicated test unless the test itself is demonstrably wrong.

Lock the first fully valid behavioral GREEN SHA as authority.

---

## Task 8 — Public docs only after behavioral GREEN

Only after Task 7 full GREEN:

**Modify:** `README.md`

- profile count 20 → 21;
- identify `deserialization-trust-analysis` as twenty-first;
- summarize causal reconstruction/type/authority/generation semantics and DT0–DT5.

**Modify:** `docs/operator-depth-contract.md`

- add profile #21 entry;
- publish DT0–DT5 ceiling and causal requirements;
- registry total 20 → 21.

No behavioral file changes are allowed after the behavioral authority SHA unless a real regression is discovered and the behavioral full stack is rerun.

---

## Task 9 — Prove docs-only delta and exact scope

1. Compare behavioral GREEN SHA to final candidate: exactly `README.md` and `docs/operator-depth-contract.md` may differ.
2. Compare base `e4979d27272ea059464b9285b5e452643b8f36f1` to final candidate: exactly nine expected paths must differ.
3. Confirm no changes to metadata, graph, packs, routing, benchmarks, eval/court authority, or workflows.

---

## Task 10 — Exact-head verification

Run/observe full CI on exact final candidate SHA.

Require the same nine CI jobs GREEN. Do not create another commit after exact-head GREEN.

Record final SHA and run ID in PR provenance.

---

## Task 11 — Fresh guarded integration

Immediately before merge:

1. fetch current `main` SHA;
2. fetch PR head SHA and base;
3. verify changed paths still exactly nine;
4. verify PR mergeable;
5. verify no base drift from the intended integration base or, if `main` moved, stop and re-evaluate/rebase rather than silently merge stale semantics;
6. mark Ready;
7. merge only with `expected_head_sha=<exact-final-head>` and merge-commit method.

---

## Task 12 — Post-merge closure

1. Verify merge commit parent 1 equals pre-merge `main`.
2. Verify parent 2 equals exact final PR head.
3. Require post-merge push CI full GREEN on exact merge SHA.
4. Read `operator-depth/profiles.json` on merge SHA and verify version 2, 21 profiles, one deserialization entry, correct paths, `lab_only: true`.
5. Read `README.md` on merge SHA and verify 21 profiles/profile #21.
6. Read `docs/operator-depth-contract.md` on merge SHA and verify profile #21 and DT0–DT5 publication.
7. Add final closure provenance comment to the PR.
8. Only then report profile #21 complete.

## Acceptance boundary

The finished profile demonstrates deterministic internal conformance and stronger causal reasoning for deserialization/reconstruction trust boundaries. It does not establish external empirical superiority without running an external contestant through the same repository court.