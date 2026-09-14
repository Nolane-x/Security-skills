# Wave 10 Connector Trust Depth Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Promote `connector-plugin-trust-analysis` into the eleventh CI-enforced operator-depth profile with causal authority/provenance reasoning and deterministic benign scenarios.

**Architecture:** Keep the canonical skill as the portable entry point, add a local domain runbook and scenario matrix, bind both in the unchanged operator-depth registry, and freeze the new semantics with one dedicated unittest module. Documentation changes happen only after behavioral GREEN so methodology failures remain isolated from copy changes.

**Tech Stack:** Markdown, JSON, Python 3.11/3.13 `unittest`, existing zero-dependency repository validators and GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-09-14-wave10-connector-trust-depth-design.md`

## Global Constraints

- Dynamic validation is authorized/sandbox-only and uses synthetic identities, fake credentials, mock services, inert actions, or read-only observations.
- Do not add payload corpora or real-account proof procedures.
- Do not modify `skill.meta.json`, graph edges, packs, routing domains, benchmark fixtures/thresholds, evaluator authority, or superiority-court authority.
- Keep operator-depth registry schema/version unchanged.
- Profile-specific tests must be additive and must not assert a permanent global registry size.
- Documentation updates occur after behavioral GREEN.

---

### Task 1: Freeze connector-depth semantics with a RED contract

**Files:**
- Create: `tests/test_connector_plugin_trust_depth.py`

**Interfaces:**
- Consumes: existing `SKILL.md` and `operator-depth/profiles.json`.
- Produces: semantic requirements that later skill/runbook/scenario/registry changes must satisfy.

- [ ] **Step 1: Write the failing test**

Create a `unittest.TestCase` with four tests:

```python
def test_skill_exposes_connector_authority_and_provenance_model():
    # require sections for lifecycle/provenance, effective authority,
    # schema/argument contract, credential/callback binding,
    # cross-connector composition, evidence ladder, counterfactual proof,
    # and evidence ceiling; require C0..C5 and the full causal chain.


def test_runbook_requires_transition_level_connector_reasoning():
    # first assert the runbook file exists so missing artifact is FAIL not ERROR;
    # require common operator-depth sections plus domain-specific transition sections.


def test_scenarios_encode_connector_lifecycle_reasoning():
    # first assert scenario JSON exists; require >=3 scenarios and meaningful
    # strings for common controls plus provenance/authority/schema/callback/
    # composition/revocation/counterfactual/evidence fields.


def test_skill_is_registered_as_eleventh_operator_depth_profile():
    # assert len(profiles) >= 11, exactly one matching profile, expected paths,
    # lab_only true, and unchanged common required_runbook_sections.
```

- [ ] **Step 2: Run RED in CI**

Commit only the test after the spec/plan docs and open a draft PR. Expected result: exactly four new assertion failures, zero errors; existing skill/graph/benchmark/operator-depth checks remain green.

- [ ] **Step 3: Reject bad RED states**

If a failure is caused by syntax, JSON decoding, missing test imports, or harness errors, fix the test only and rerun until RED reflects missing feature semantics.

---

### Task 2: Implement the causal connector methodology

**Files:**
- Modify: `skills/connector-plugin-trust-analysis/SKILL.md`
- Create: `skills/connector-plugin-trust-analysis/references/operator-runbook.md`
- Create: `skills/connector-plugin-trust-analysis/references/operator-scenarios.json`
- Modify: `operator-depth/profiles.json`

**Interfaces:**
- Consumes: Task 1 semantic assertions and the common operator-depth contract.
- Produces: canonical methodology, local deep methodology, deterministic fixtures, and profile 11 registration.

- [ ] **Step 1: Deepen the canonical skill**

Add the exact causal model:

```text
integration identity -> provenance -> permission grant -> delegated scope -> tool/schema contract -> invocation principal -> argument authority -> policy/confirmation -> bounded remote effect -> callback/result provenance -> cross-connector propagation -> revocation/update state
```

Add explicit sections and terminology for effective authority decomposition, provenance continuity, schema/argument separation, delegated scope/audience, callback identity, compound cross-connector authority, grant/update/revocation generations, C0-C5 evidence ladder, counterfactual proof, alternative explanations, and evidence ceiling.

- [ ] **Step 2: Add the operator runbook**

Include the common required sections:

```text
## Attack surface
## Hypothesis matrix
## Controlled validation
## False-positive controls
## Evidence capture
## Remediation checks
```

Also include domain sections for integration lifecycle/provenance, effective authority trace, schema/argument contract, credential/callback binding, cross-connector composition, lifecycle/revocation trace, counterfactual controls, and evidence promotion/ceiling. Keep every dynamic oracle benign and sandboxed.

- [ ] **Step 3: Add three deterministic scenario fixtures**

Create version-1 JSON with at least:

```text
schema-permission-drift
credential-callback-binding
cross-connector-revocation
```

Each scenario includes common fields (`hypothesis`, `safe_oracle`, `positive_control`, `negative_control`, `stop_condition`, `remediation_oracle`) and meaningful domain fields such as `integration_provenance`, `authority_profile`, `schema_argument_trace`, `credential_callback_binding`, `composition_trace`, `lifecycle_state`, `counterfactual_control`, `alternative_explanation`, `evidence_level`, and `evidence_ceiling`.

- [ ] **Step 4: Register profile 11**

Append one `connector-plugin-trust-analysis` entry to `operator-depth/profiles.json` with the unchanged version-2 schema, standard relative paths, `lab_only: true`, and the six common required runbook sections.

- [ ] **Step 5: Run behavioral GREEN**

Expected: dedicated connector tests pass; central operator-depth validator reports 11 profiles; full unittest suite passes; existing benchmark/graph/agent smoke stays green.

---

### Task 3: Synchronize documentation without rewriting history

**Files:**
- Modify: `docs/operator-depth-contract.md`
- Modify: `README.md`

**Interfaces:**
- Consumes: verified profile-11 behavior from Task 2.
- Produces: current repo status without changing historical Wave 8/Wave 10 lineage.

- [ ] **Step 1: Update operator-depth contract**

Preserve `Wave 8 established eight profiles`, then list Wave 10 promotions in order: prompt injection ninth, RAG/memory tenth, connector/plugin trust eleventh. Summarize connector-specific authority/provenance/schema/callback/composition/revocation reasoning.

- [ ] **Step 2: Update README current-state counts and list**

Change current operator-depth count from 10 to 11 in snapshot/diagram/current text and add `connector-plugin-trust-analysis` to the current profile list. Do not change 83 skills, 20 packs, 36 fixtures, 12 portability fixtures, or historical counts.

- [ ] **Step 3: Inspect patches**

Verify README/doc patches contain only intended count/list/description changes.

---

### Task 4: Exact-head verification and merge

**Files:**
- Review only; no intended production changes.

**Interfaces:**
- Consumes: final branch head.
- Produces: mergeable Wave 10 checkpoint with reproducible CI provenance.

- [ ] **Step 1: Review changed filenames**

Expected scope: spec, plan, connector skill, connector runbook, connector scenarios, dedicated connector test, registry, operator-depth docs, README. Any additional file requires explicit causal justification.

- [ ] **Step 2: Verify six matrix jobs**

Require success on Ubuntu/macOS/Windows with Python 3.11 and 3.13, including canonical skills, 11-profile validator, graph/index checks, benchmark validation, portability, agent smoke, and full unittests.

- [ ] **Step 3: Verify deterministic core gates**

Require `benchmark-core`, `agent-eval-core`, and `superiority-court-core` success, including byte-identical double-run checks and negative replay profiles.

- [ ] **Step 4: Record RED -> GREEN provenance in PR**

Document RED commit/run, exact GREEN head/run, changed-file review, and statement that graph/packs/routing/benchmark/evaluator authority did not change.

- [ ] **Step 5: Mark Ready and merge with expected head**

Use the exact verified head SHA so a branch race blocks merge rather than silently merging an unverified tree.

## Self-review

- Spec coverage: all causal, authority, provenance, schema, callback, composition, lifecycle, evidence, counterfactual, safety, registry, docs, and verification requirements are mapped to Tasks 1-4.
- Placeholder scan: no TBD/TODO/"implement later" steps.
- Interface consistency: profile name and artifact paths are identical across spec, tests, registry, docs, and plan; profile checks use additive `>= 11` semantics.
