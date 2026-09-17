# Wave 10 Browser Process Boundary Depth Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add operator-depth profile #19 for `browser-process-boundary-analysis`, converting the existing browser multi-process checklist into a deterministic causal identity/authority model with B0–B5 evidence ceilings and safe machine-readable review cases.

**Architecture:** Preserve the canonical skill and metadata graph. Add depth through the existing operator-depth architecture: deepen `SKILL.md`, add one browser-specific runbook, add one deterministic three-case review matrix, register the profile in `operator-depth/profiles.json`, freeze semantics in a dedicated regression test, then publish the profile count/description in two public docs only after behavioral GREEN.

**Tech Stack:** Markdown, JSON, Python standard-library `unittest`, zero third-party dependencies, GitHub Actions matrix validation on Ubuntu/macOS/Windows × Python 3.11/3.13.

**Spec:** `docs/superpowers/specs/2026-09-17-wave10-browser-process-boundary-depth-design.md`

## Global Constraints

- Base authority is `main@82dab4efefcecc3bea86a2bdf523a3359dfb275c`.
- Exact feature branch: `wave10-browser-process-boundary-depth`.
- Exact PR scope is nine paths defined in the spec.
- Do not change `skills/browser-process-boundary-analysis/skill.meta.json`, graph edges, packs, routing domains, benchmark fixtures/thresholds, agent-eval authority, superiority-court authority, or workflow semantics.
- Registry schema remains version 2.
- All browser validation remains local/owned/sandboxed/benchmark/explicitly authorized and uses synthetic origins, mock brokers, inert sinks, read-only resources, or bounded reversible owner-controlled state.
- Do not provide sandbox-escape recipes, privilege-escalation procedures, arbitrary-code-execution proof, persistence, evasion, malware, destructive actions, or testing of third-party websites/users.
- Test-first commit must be observed RED before production behavior is added.
- Dedicated test is frozen after the test-first commit unless a genuine test defect is demonstrated.
- `README.md` and `docs/operator-depth-contract.md` may change only after behavioral full GREEN.
- Merge requires exact-head full GREEN, fresh scope/base/head/main checks, and `expected_head_sha` guard.
- Completion requires post-merge push CI full GREEN on the exact merge SHA plus registry/docs verification at that merge SHA.

---

### Task 1: Freeze browser-process depth semantics in a failing dedicated test

**Files:**
- Create: `tests/test_browser_process_boundary_depth.py`
- Read only: `skills/browser-process-boundary-analysis/SKILL.md`
- Read only: `operator-depth/profiles.json`

**Interfaces:**
- Consumes: design terms and exact paths from the spec.
- Produces: one `unittest` module containing four test methods/groups that become the immutable behavioral contract for the rest of the profile.

- [ ] **Step 1: Write the canonical-skill contract test**

Create assertions that require the causal chain and the following exact semantic anchors to be present in `SKILL.md`: process role vs process identity; origin/site/frame identity; route/interface vs routed object identity; parsing vs authorization; object generation; brokered capability; ambient vs delegated authority; receipt/result binding; B0 through B5; counterfactual controls; and an explicit evidence-ceiling statement that reachability/parsing/crash/configuration alone cannot establish B4/B5.

Use standard-library path handling only:

```python
from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "browser-process-boundary-analysis" / "SKILL.md"
RUNBOOK = ROOT / "skills" / "browser-process-boundary-analysis" / "references" / "operator-runbook.md"
CASES = ROOT / "skills" / "browser-process-boundary-analysis" / "references" / "operator-review-cases.json"
REGISTRY = ROOT / "operator-depth" / "profiles.json"
```

- [ ] **Step 2: Write the runbook contract test**

Require all common operator-depth sections and these browser-specific second-level headings:

```text
## Process graph and sandbox-profile trace
## Origin/site/frame context trace
## Process identity and generation trace
## IPC schema and normalized-message trace
## Routed object and lifecycle trace
## Ownership and authorization decision trace
## Brokered capability and resource trace
## Ambient-versus-delegated authority trace
## Privileged-consumer and result trace
## Lifecycle/revocation generation trace
## Counterfactual controls
## Evidence promotion and ceiling
```

Also assert local/owned/synthetic authorization language, generation-aware reasoning, and prohibition on debug/unsandboxed configurations as release-boundary proof.

- [ ] **Step 3: Write the review-case contract test**

Require `version == 1`, at least three cases, and exact IDs:

```python
REQUIRED_IDS = {
    "origin-process-object-binding",
    "ipc-capability-broker-binding",
    "process-generation-lifecycle-binding",
}
```

Require every case to contain all fields specified in the design spec. For every textual field except `id`, require a stripped string length of at least 40 characters. Require `safe_oracle` to mention at least one safe mechanism (`synthetic`, `mock`, `inert`, `read-only`, `controlled`, or `canary`), `stop_condition` to include `stop`, `abort`, or `do not proceed`, and `evidence_level`/`evidence_ceiling` to match `B[0-5]`.

- [ ] **Step 4: Write the additive registry contract test**

Load `operator-depth/profiles.json` and assert:

```python
assert data["version"] == 2
profiles = [p for p in data["profiles"] if p["skill"] == "browser-process-boundary-analysis"]
assert len(profiles) == 1
assert len(data["profiles"]) >= 19
assert profiles[0]["runbook"] == "references/operator-runbook.md"
assert profiles[0]["scenario_matrix"] == "references/operator-review-cases.json"
assert profiles[0]["lab_only"] is True
```

- [ ] **Step 5: Commit test-first state**

Commit only the new dedicated test on top of spec+plan. Do not edit production artifacts.

- [ ] **Step 6: Open Draft PR on the exact test-first SHA and verify RED**

Expected RED shape: the new dedicated module contributes exactly four intended assertion failures; there are zero unittest errors; existing canonical-skill validation, current 18-profile operator-depth validation, graph/index validation, benchmark validation, portability benchmark, and agent-eval smoke pass before the dedicated failures.

If failure count or cause differs, stop and debug the test rather than implementing around it.

---

### Task 2: Deepen the canonical browser-process reasoning model

**Files:**
- Modify: `skills/browser-process-boundary-analysis/SKILL.md`
- Test: `tests/test_browser_process_boundary_depth.py`

**Interfaces:**
- Consumes: causal chain, invariants, distinctions, lifecycle model, and B0–B5 ladder from the spec.
- Produces: canonical portable reasoning entry point; no vendor-specific terminology or metadata change.

- [ ] **Step 1: Replace checklist-only workflow with the causal chain**

Include the exact conceptual progression:

```text
request origin
-> browser principal
-> origin/site/frame context
-> process assignment
-> process identity/generation
-> routed object/interface identity
-> normalized IPC state
-> ownership/lifecycle validation
-> broker/service identity
-> requested capability/resource
-> policy decision
-> effective brokered authority
-> privileged consumer
-> bounded result
-> receipt/result binding
-> lifecycle/revocation generation
```

- [ ] **Step 2: Add required distinctions and generation semantics**

State explicitly that process role ≠ process identity, process identity ≠ origin/site/frame identity, parsing ≠ authorization, route identifier ≠ current routed object identity, object reference ≠ ownership, and ambient privileged authority ≠ delegated caller authority.

- [ ] **Step 3: Add B0–B5 evidence ladder and ceilings**

Define all six levels exactly as the spec. B5 must require provenance, object-generation binding, policy trace, broker/consumer identity, capability binding, lifecycle control, counterfactual, alternative-explanation elimination, and remediation regression.

- [ ] **Step 4: Add safe counterfactual and stop discipline**

Use synthetic origins/process IDs/object generations/resources only. Explicitly reject public-site testing, real profiles/credentials, sandbox disabling as proof, host compromise, and destructive proof.

- [ ] **Step 5: Commit canonical-skill behavioral change**

Do not change `skill.meta.json`.

---

### Task 3: Add the deep operator runbook

**Files:**
- Create: `skills/browser-process-boundary-analysis/references/operator-runbook.md`
- Test: `tests/test_browser_process_boundary_depth.py`

**Interfaces:**
- Consumes: canonical causal model from Task 2.
- Produces: transition-level methodology used by human/agent reviewers and referenced by the registry.

- [ ] **Step 1: Add common required sections**

Use exact headings required by the operator-depth validator:

```text
## Attack surface
## Hypothesis matrix
## Controlled validation
## False-positive controls
## Evidence capture
## Remediation checks
```

- [ ] **Step 2: Add all browser-specific trace sections**

Use the exact headings frozen in Task 1. Each section must explain what identity/state is authoritative, what can be attacker/sender-controlled, what evidence is required, and what cannot promote evidence.

- [ ] **Step 3: Add alternative-explanation and counterfactual methodology**

Cover wrong-process attachment, route reuse, expected process/site reuse, telemetry lag, broker cache propagation, benign retry, shared-memory synchronization, fixture collision, extension/native-host reconnect, and unrelated concurrent result correlation.

- [ ] **Step 4: Add evidence promotion rules**

Explain B0–B5 and require independent evidence for every claimed cross-process hop. Explicitly cap reachability/parser/configuration-only observations below B4/B5.

- [ ] **Step 5: Commit runbook**

Keep content defensive and bounded; no exploit chain or payload recipe.

---

### Task 4: Add deterministic browser-process review cases

**Files:**
- Create: `skills/browser-process-boundary-analysis/references/operator-review-cases.json`
- Test: `tests/test_browser_process_boundary_depth.py`

**Interfaces:**
- Consumes: machine-readable field contract from the spec.
- Produces: version-1 deterministic audit-only matrix with exactly the required three case IDs (additional cases are unnecessary for this wave).

- [ ] **Step 1: Create `origin-process-object-binding`**

Use a synthetic origin, synthetic frame/site instance, synthetic process IDs and generations, inert routed object, and read-only or inert sink. The negative control changes only one security-relevant identity and must be denied. The remediation oracle preserves the intended neighboring synthetic flow.

- [ ] **Step 2: Create `ipc-capability-broker-binding`**

Use a mock broker and inert capability/resource. Demonstrate requested vs policy-approved capability, ambient-vs-delegated authority separation, and receipt binding without any real privileged action.

- [ ] **Step 3: Create `process-generation-lifecycle-binding`**

Use deterministic old/current process and object generations. The stale generation must be rejected while current generation remains valid. Include a service/broker restart or revocation-generation dimension without real persistence or host modification.

- [ ] **Step 4: Validate field quality manually against the test contract**

Every textual field other than `id` must be at least 40 characters and explain a concrete deterministic fixture rather than filler prose.

- [ ] **Step 5: Commit review matrix**

---

### Task 5: Register profile #19 and obtain behavioral GREEN

**Files:**
- Modify: `operator-depth/profiles.json`
- Test: `tests/test_browser_process_boundary_depth.py`

**Interfaces:**
- Consumes: runbook and review matrix paths from Tasks 3–4.
- Produces: exactly one CI-enforced profile registration.

- [ ] **Step 1: Add exactly one registry object**

Use:

```json
{
  "skill": "browser-process-boundary-analysis",
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

Preserve registry version 2 and deterministic ordering convention.

- [ ] **Step 2: Commit registry change**

- [ ] **Step 3: Run/observe full behavioral CI on the exact behavioral head**

Require SUCCESS for all six matrix jobs, `benchmark-core`, `agent-eval-core`, and `superiority-court-core`, including byte-identical checks and cautious/faulty controls.

- [ ] **Step 4: Lock behavioral authority SHA**

Record the exact SHA and workflow run. After this point, only the two public documentation files may change.

---

### Task 6: Publish profile #19 in public docs only

**Files:**
- Modify: `README.md`
- Modify: `docs/operator-depth-contract.md`

**Interfaces:**
- Consumes: behavioral GREEN profile count and B0–B5 semantics.
- Produces: public snapshot at 19 profiles and a concise profile #19 description.

- [ ] **Step 1: Update README snapshot and profile list**

Change operator-depth count from 18 to 19 everywhere it represents the current registry. Add `browser-process-boundary-analysis` as the nineteenth profile and summarize process/origin/object generation, IPC routing, brokered capability, lifecycle, counterfactual, and B0–B5 evidence ceilings.

- [ ] **Step 2: Update operator-depth contract**

Add profile #19 to Wave 10 expansion and change current registry count from eighteen to nineteen. Preserve Wave 8 historical counts.

- [ ] **Step 3: Commit docs-only changes**

- [ ] **Step 4: Prove post-GREEN delta is docs-only**

Compare behavioral authority SHA to final candidate; require exactly:

```text
README.md
docs/operator-depth-contract.md
```

- [ ] **Step 5: Prove total PR scope is exactly nine paths**

Require the exact nine paths listed in the design spec and no others.

---

### Task 7: Exact-head verification, guarded merge, and closure

**Files:**
- No new file changes permitted.

**Interfaces:**
- Consumes: final candidate SHA with exact nine-file scope.
- Produces: merged `main` commit with complete CI/provenance closure.

- [ ] **Step 1: Run/observe full exact-head CI**

Require all six matrix jobs and all three core jobs SUCCESS on the exact final candidate SHA.

- [ ] **Step 2: Update PR provenance without changing branch SHA**

Record spec SHA, plan SHA, test-first SHA, RED run, behavioral GREEN SHA/run, final candidate SHA, docs-only compare, exact nine-file scope, and exact-head GREEN run.

- [ ] **Step 3: Perform fresh pre-merge checks**

Verify immediately before merge:

```text
PR head == final candidate SHA
PR base == main
PR mergeable == true
main == 82dab4efefcecc3bea86a2bdf523a3359dfb275c
changed paths == exact nine-path set
```

If `main` has drifted, stop and re-evaluate rather than merging stale evidence.

- [ ] **Step 4: Mark Ready and guarded merge**

Merge with method `merge` and `expected_head_sha=<final candidate SHA>`.

- [ ] **Step 5: Verify merge commit lineage**

Require parent 1 to be the verified pre-merge `main` SHA and parent 2 to be the exact final candidate SHA.

- [ ] **Step 6: Observe post-merge push CI on exact merge SHA**

Require the `push` event run on `main` to finish with all six matrix jobs and all three core jobs SUCCESS.

- [ ] **Step 7: Verify closure state at merge SHA**

Confirm `operator-depth/profiles.json` has version 2, exactly one `browser-process-boundary-analysis`, and total profile count 19. Confirm README and operator-depth contract both publish 19 and identify browser-process boundary as profile #19.

- [ ] **Step 8: Write final closure provenance comment**

Include merge SHA, both parents, post-merge run ID/number, 9-gate success, registry count 19, docs state, and explicit statement that this is contract conformance only and not empirical superiority over an external system.
