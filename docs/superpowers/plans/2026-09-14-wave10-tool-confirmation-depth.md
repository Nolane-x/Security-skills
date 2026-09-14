# Wave 10 Tool Capability And Confirmation Depth Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Promote `tool-capability-and-confirmation-analysis` into the twelfth CI-enforced operator-depth profile with transition-level intent, authority, confirmation, execution, transaction, and post-action evidence semantics.

**Architecture:** Keep the existing canonical skill as the portable entry point and add profile-specific depth through a reviewed operator runbook plus deterministic audit-only review cases. Freeze the semantics with a dedicated TDD contract test, bind the artifacts through the existing version-2 operator-depth registry, then synchronize public docs only after behavioral GREEN.

**Tech Stack:** Markdown Agent Skills, JSON registry/review cases, Python `unittest`, repository validators, GitHub Actions across Ubuntu/macOS/Windows and Python 3.11/3.13.

**Spec:** `docs/superpowers/specs/2026-09-14-wave10-tool-confirmation-depth-design.md`

## Global Constraints

- All validation is defensive, authorized-only, and uses mock tools, synthetic identities/resources, inert actions, reversible fixtures, or read-only observations.
- Do not teach or test bypass of real user consent or production confirmation systems.
- Do not change `skills/tool-capability-and-confirmation-analysis/skill.meta.json`.
- Do not change graph edges, packs, routing domains, benchmark fixtures/thresholds, agent-eval authority, or superiority-court authority.
- Preserve `operator-depth/profiles.json` schema version `2` and its stable `scenario_matrix` field.
- Register the new profile additively; profile-local tests must never assert an exact global registry length.
- Public docs change only after behavioral GREEN.

---

### Task 1: Freeze the twelfth-profile contract with a clean RED test

**Files:**
- Create: `tests/test_tool_capability_confirmation_depth.py`
- Read: `skills/tool-capability-and-confirmation-analysis/SKILL.md`
- Read: `operator-depth/profiles.json`

**Interfaces:**
- Consumes: current canonical skill and version-2 operator-depth registry.
- Produces: a dedicated semantic contract for canonical sections, runbook sections, review-case fields, and additive profile registration.

- [ ] **Step 1: Write four focused unittest methods**

The test must assert these canonical headings exist:

```python
for section in (
    "## Action-binding causal model",
    "## Intent and capability model",
    "## Argument normalization and binding",
    "## Effective authority model",
    "## Confirmation tuple",
    "## Execution binding and state drift",
    "## Transaction, retry, and idempotency model",
    "## Post-action verification",
    "## Tool evidence ladder",
    "## Counterfactual proof",
    "## Alternative explanations",
    "## Evidence ceiling",
):
    self.assertIn(section, text)
```

It must also require the causal chain and evidence levels `T0` through `T5`.

The runbook test must check file existence before reading and require these headings:

```python
for section in (
    "## Attack surface",
    "## Hypothesis matrix",
    "## Intent and capability binding",
    "## Argument normalization trace",
    "## Effective authority trace",
    "## Confirmation tuple trace",
    "## Execution binding and state drift",
    "## Transaction, retry, and idempotency",
    "## Post-action verification",
    "## Controlled validation",
    "## False-positive controls",
    "## Counterfactual controls",
    "## Evidence capture",
    "## Evidence promotion and ceiling",
    "## Remediation checks",
):
    self.assertIn(section, text)
```

The review-case test must require version `1`, at least three entries under `scenarios`, and non-empty strings for common operator-depth fields plus:

```python
(
    "request_intent",
    "capability_trace",
    "argument_trace",
    "effective_authority",
    "confirmation_tuple",
    "execution_binding",
    "transaction_state",
    "post_action_verification",
    "counterfactual_control",
    "alternative_explanation",
    "evidence_level",
    "evidence_ceiling",
)
```

The registration test must use:

```python
self.assertGreaterEqual(len(profiles), 12)
matching = [p for p in profiles if p["skill"] == "tool-capability-and-confirmation-analysis"]
self.assertEqual(len(matching), 1)
self.assertEqual(matching[0]["runbook"], "references/operator-runbook.md")
self.assertEqual(matching[0]["scenario_matrix"], "references/operator-review-cases.json")
self.assertTrue(matching[0]["lab_only"])
```

- [ ] **Step 2: Commit only the dedicated test**

Commit message:

```text
Wave 10: add RED tool confirmation depth contract
```

- [ ] **Step 3: Open a Draft PR before implementation**

PR title:

```text
Wave 10: deepen tool capability and confirmation reasoning
```

Record base `main@74f40c88ae55be863ad00280e673e5c5c4961642`, test-first commit SHA, and expected RED state.

- [ ] **Step 4: Verify clean RED in GitHub Actions**

Expected dedicated unittest outcome: exactly four new assertion failures and zero Python/JSON errors. Earlier validators should remain green until the full test phase reaches the four intended failures.

### Task 2: Deepen the canonical skill

**Files:**
- Modify: `skills/tool-capability-and-confirmation-analysis/SKILL.md`
- Test: `tests/test_tool_capability_confirmation_depth.py`

**Interfaces:**
- Consumes: design causal chain and T0-T5 evidence model.
- Produces: portable action-level reasoning semantics and link to the operator runbook.

- [ ] **Step 1: Replace checklist-only depth with explicit causal sections**

Add the headings frozen in Task 1 and include the exact chain:

```text
request intent -> capability proposal -> normalized arguments -> effective authority -> policy decision -> confirmation snapshot -> execution binding -> observable bounded effect -> receipt/state -> retry/rollback state
```

- [ ] **Step 2: Define confirmation as a bound tuple**

Document principal/session, tool/capability, target/resource, effect class, material arguments, policy/credential generation, confirmation generation, and expiry/mutation boundary.

- [ ] **Step 3: Define action-state inequalities**

Include:

```text
proposal != accepted execution != receipt != durable final state
```

and state that tool/schema availability alone is not evidence of effect authority.

- [ ] **Step 4: Add T0-T5 evidence ladder, counterfactual proof, alternative explanations, and evidence ceiling**

Keep all examples synthetic/inert and prohibit inference above directly demonstrated evidence.

- [ ] **Step 5: Add operator-depth link**

Link to `references/operator-runbook.md` for full authorized methodology.

### Task 3: Add reviewed operator methodology

**Files:**
- Create: `skills/tool-capability-and-confirmation-analysis/references/operator-runbook.md`

**Interfaces:**
- Consumes: canonical action-binding model.
- Produces: detailed reviewed methodology satisfying common operator-depth sections plus tool-specific traces.

- [ ] **Step 1: Create common operator-depth sections**

Include `Attack surface`, `Hypothesis matrix`, `Controlled validation`, `False-positive controls`, `Evidence capture`, and `Remediation checks`.

- [ ] **Step 2: Add tool-specific traces**

Include the headings frozen by Task 1 for intent/capability binding, argument normalization, effective authority, confirmation tuple, execution binding/state drift, transaction/retry/idempotency, post-action verification, counterfactual controls, and evidence promotion/ceiling.

- [ ] **Step 3: Encode false-positive discipline**

Explicitly distinguish stale UI, harmless normalization, asynchronous receipts, duplicate proposals, idempotent replays, mock-service artifacts, and rollback convergence from validated defects.

- [ ] **Step 4: Keep all validation bounded**

Use only mock services, synthetic principals/resources, inert action sinks, reversible state, and read-only receipts. Stop before real external sends, production writes, irreversible changes, spending, destructive operations, or consent bypass.

### Task 4: Add deterministic audit-only review cases

**Files:**
- Create: `skills/tool-capability-and-confirmation-analysis/references/operator-review-cases.json`
- Test: `tests/test_tool_capability_confirmation_depth.py`

**Interfaces:**
- Consumes: common operator-depth matrix contract.
- Produces: deterministic review cases compatible with the existing `scenario_matrix` registry field.

- [ ] **Step 1: Create version-1 matrix with three cases**

Use IDs:

```text
request-confirmation-argument-binding
read-write-chain-boundary
retry-receipt-final-state
```

- [ ] **Step 2: Fill common operator-depth fields**

Each case must contain `hypothesis`, `safe_oracle`, `positive_control`, `negative_control`, `stop_condition`, and `remediation_oracle` with explicit synthetic/mock/read-only mechanisms.

- [ ] **Step 3: Fill tool-specific fields**

Each case must contain all Task-1 fields: request intent, capability trace, argument trace, effective authority, confirmation tuple, execution binding, transaction state, post-action verification, counterfactual control, alternative explanation, evidence level, and evidence ceiling.

### Task 5: Register profile #12 and achieve behavioral GREEN

**Files:**
- Modify: `operator-depth/profiles.json`
- Test: `tests/test_tool_capability_confirmation_depth.py`

**Interfaces:**
- Consumes: canonical skill, runbook, review-case matrix.
- Produces: twelfth CI-enforced profile under registry schema version 2.

- [ ] **Step 1: Add one registry entry**

```json
{
  "skill": "tool-capability-and-confirmation-analysis",
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

- [ ] **Step 2: Run behavioral CI**

Do not touch README/docs yet. Require six matrix jobs to pass the canonical validator, 12-profile operator-depth validator, graph/index checks, benchmark validation, portability, agent smoke, and full tests.

- [ ] **Step 3: Diagnose any regression before changing contracts**

If an older profile-local test asserts an exact global profile count, repair that ownership bug without weakening the central validator. Do not relax safety, evidence, determinism, or oracle requirements merely to get green.

### Task 6: Synchronize public operator-depth documentation

**Files:**
- Modify: `docs/operator-depth-contract.md`
- Modify: `README.md`

**Interfaces:**
- Consumes: behavioral GREEN at exact implementation head before docs.
- Produces: public status showing 12 profiles and the fourth Wave-10 second-depth promotion.

- [ ] **Step 1: Update operator-depth contract history**

Preserve Wave 8 = eight profiles and document prompt injection = 9, RAG/memory = 10, connector/plugin trust = 11, tool capability/confirmation = 12.

- [ ] **Step 2: Update README count/list and Wave-10 description**

Change current operator-depth profile count from 11 to 12, add `tool-capability-and-confirmation-analysis`, and summarize action binding, confirmation tuple, transaction/idempotency, post-action verification, and T0-T5 evidence ceilings.

- [ ] **Step 3: Review docs patch for unrelated drift**

Ensure no capability claims or historical counts outside the intended profile-status text are accidentally removed.

### Task 7: Exact-head verification and integration

**Files:**
- Review only: all PR changed files

**Interfaces:**
- Consumes: complete branch tree.
- Produces: provenance-complete PR and merged `main` only after exact-head evidence.

- [ ] **Step 1: Freeze exact PR head**

No more commits after starting final verification.

- [ ] **Step 2: Require full exact-head CI**

Require SUCCESS for all six OS/Python matrix jobs, `benchmark-core`, `agent-eval-core`, and `superiority-court-core`, including every double-run/byte-identical determinism check and cautious/faulty replay control.

- [ ] **Step 3: Review changed-file scope**

Expected changes are limited to spec, plan, dedicated test, canonical skill, runbook, review cases, registry, operator-depth contract, and README. Confirm no `skill.meta.json`, graph, packs, routing, benchmark authority, evaluator authority, or superiority-court authority drift.

- [ ] **Step 4: Update PR provenance**

Record RED commit/run, behavioral GREEN commit/run, final exact head/run, changed-file scope, and any narrowly repaired test-ownership regression.

- [ ] **Step 5: Mark Ready and merge with expected-head guard**

Merge only if the PR head still matches the fully verified SHA.

- [ ] **Step 6: Verify post-merge main**

Confirm `main` points to the merge commit and the push-triggered workflow passes the same six matrix jobs plus all three core determinism gates.
