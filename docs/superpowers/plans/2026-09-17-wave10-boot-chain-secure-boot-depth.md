# Wave 10 Profile #20 — Boot Chain And Secure Boot Depth Implementation Plan

> Execute strictly test-first. The dedicated test is authority after a valid RED and must not be weakened to fit implementation.

**Goal:** deepen `boot-chain-and-secure-boot-analysis` into a deterministic operator-depth profile that proves root/policy authority, component selection, selected-vs-loaded identity, rollback generation, handoff inheritance, and alternate-path equivalence using only benign synthetic/owned fixtures.

**Base:** `main@6b8e0f36fee255a985d39aa8178598d58e1e21ad`

**Expected final scope:** exactly nine paths listed in the design spec. No metadata/graph/pack/routing/benchmark/eval/workflow changes.

## Task 1 — Freeze the semantic contract with a dedicated test

Create `tests/test_boot_chain_secure_boot_depth.py` only.

The test must contain exactly four high-level test methods:

1. canonical `SKILL.md` depth: required headings, full causal-chain anchor, key distinctions, BC0–BC5, counterfactuals, evidence ceiling;
2. operator runbook depth: common sections plus root/policy, boot path, selection, signer authority, rollback generation, selected-vs-loaded, handoff, recovery, receipt/attestation, lifecycle traces;
3. review-case matrix: version 1, >=3 scenarios, required IDs, all common/domain fields, substantive strings, safe oracle/stop condition, BC-level syntax;
4. registry: version 2, >=20 profiles, exactly one new skill entry, expected paths, `lab_only: true`, common section list unchanged.

Before writing production artifacts, commit the test and open a Draft PR at that exact SHA. Observe RED in CI. Accept RED only when failures are dedicated contract failures caused by missing implementation; pre-existing validators, graph/index checks, benchmark validation, portability checks, and existing profile validation must remain green, with zero unexpected unittest errors.

## Task 2 — Implement canonical causal depth

Update `skills/boot-chain-and-secure-boot-analysis/SKILL.md` without changing frontmatter identity or metadata semantics.

Required new semantic sections:

- `## Causal boot-chain model`
- `## Root, policy, and signer authority`
- `## Component selection and identity`
- `## Selected-versus-loaded binding`
- `## Rollback and freshness generation`
- `## Handoff and next-stage inheritance`
- `## Recovery and alternate-path reasoning`
- `## Boot-chain evidence ladder`
- `## Counterfactual proof`
- `## Alternative explanations`
- `## Evidence ceiling`

Include the exact normalized causal-chain anchor frozen by the test and explicit distinctions from the design. Keep all validation bounded to emulators, synthetic artifacts/keys, owned lab devices, inert next stages, read-only traces, and reversible effects.

## Task 3 — Add the transition-level operator runbook

Create `skills/boot-chain-and-secure-boot-analysis/references/operator-runbook.md`.

Required headings:

- Attack surface
- Hypothesis matrix
- Root-of-trust and policy-generation trace
- Boot-mode and path trace
- Component selection and identity trace
- Signature and signer-authority trace
- Rollback and freshness-generation trace
- Selected-versus-loaded binding trace
- Handoff and next-stage inheritance trace
- Recovery and alternate-path equivalence trace
- Receipt, measurement, and attestation trace
- Lifecycle/revocation generation trace
- Controlled validation
- False-positive controls
- Counterfactual controls
- Alternative explanations
- Evidence capture
- Evidence promotion and ceiling
- Remediation checks

The runbook must operationalize transition-level evidence capture instead of repeating the canonical skill prose. It must explicitly separate measurement from enforcement, signature validity from signer authorization, selected identity from loaded identity, and normal-path proof from recovery-path equivalence.

## Task 4 — Add deterministic benign review cases

Create `skills/boot-chain-and-secure-boot-analysis/references/operator-review-cases.json`, schema version 1.

Required scenarios:

- `root-policy-component-binding`
- `rollback-slot-loaded-identity-binding`
- `recovery-handoff-generation-binding`

Every scenario must contain all fields frozen by the dedicated test, each substantive enough to encode a causal transition. Use synthetic keys, components, manifests, slots, mock loaders, emulator receipts, or inert next stages. Stop conditions must prohibit irreversible fuse/key changes, production signing material, destructive flashing, or unauthorized devices.

## Task 5 — Register exactly one twentieth profile

Update `operator-depth/profiles.json` only after the RED authority exists.

Add exactly one object:

```json
{
  "skill": "boot-chain-and-secure-boot-analysis",
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

Keep registry `version` at 2. Do not touch any other registration except ordering if the file convention requires it.

## Task 6 — Behavioral verification

Push Tasks 2–5 without changing the dedicated test. Monitor the PR workflow on the exact behavioral SHA.

Behavioral GREEN requires:

- all six OS/Python matrix jobs SUCCESS;
- `benchmark-core` SUCCESS;
- `agent-eval-core` SUCCESS;
- `superiority-court-core` SUCCESS;
- deterministic byte-identical checks SUCCESS;
- cautious/faulty controls SUCCESS.

If any dedicated assertion fails, diagnose the implementation/root cause and fix production artifacts only unless the test itself is demonstrably wrong. Any new commit requires the full relevant CI rerun.

## Task 7 — Docs-only public finalization

Only after behavioral FULL GREEN, update:

- `README.md`
- `docs/operator-depth-contract.md`

Publish 20 CI-enforced profiles, identify `boot-chain-and-secure-boot-analysis` as profile #20, summarize the causal model and BC0–BC5 evidence ceiling, and preserve the external-superiority caveat.

Prove the delta from behavioral GREEN to final candidate is exactly these two documentation paths.

## Task 8 — Exact-head and integration verification

On final candidate SHA:

1. prove total PR changed paths are exactly the nine expected paths;
2. run/observe full exact-head CI and require every required job GREEN;
3. do not create another commit after exact-head GREEN;
4. freshly verify PR head, base, mergeability, changed paths, and current `main` SHA;
5. require `main` still equals the original base before merge;
6. mark the PR Ready;
7. merge using `expected_head_sha=<exact-final-head>`.

## Task 9 — Post-merge closure

On the exact merge SHA:

1. verify `main` points to the merge commit;
2. verify parent 1 equals pre-merge main and parent 2 equals final PR head;
3. require the post-merge push workflow to complete fully GREEN;
4. read `operator-depth/profiles.json`, `README.md`, and `docs/operator-depth-contract.md` directly from the merge SHA;
5. verify version 2, exactly one boot-chain registration, total profile count 20, correct runbook/case paths, `lab_only: true`, public docs count 20 and BC0–BC5 publication;
6. write a closure provenance comment with test-first SHA, RED run, behavioral authority, exact-head run, guarded merge SHA, parents, post-merge run, final scope, safety boundary, and no unsupported external-superiority claim.

Only then declare Wave 10 profile #20 complete.