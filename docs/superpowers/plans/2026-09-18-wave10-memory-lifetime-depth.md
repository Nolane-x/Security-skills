# Wave 10 Profile #25 — Memory Lifetime Depth Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Promote `memory-lifetime-analysis` into the twenty-fifth CI-enforced operator-depth profile with causal ML0–ML5 semantics and deterministic benign review cases.

**Architecture:** Keep the existing canonical skill as the portable entry point, add one deep operator runbook plus one machine-readable benign review-case matrix, then bind both through registry schema v2. Freeze the profile semantics in a dedicated test before any production artifacts, preserve existing graph/pack/evaluation authorities, and publish public docs only after behavioral GREEN.

**Tech Stack:** Markdown, JSON, Python 3.11/3.13 `unittest`, zero third-party Python dependencies, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-09-18-wave10-memory-lifetime-depth-design.md`

## Global Constraints

- Base authority: `main@52796d72dd1a4d2094b433e14f2b51302a7c40b6`.
- Preserve 83 canonical skills and 20 packs.
- Keep `operator-depth/profiles.json` schema version 2.
- Do not modify `skill.meta.json`, graph edges, packs, routing domains, benchmark authority, agent-eval authority, superiority-court authority, or workflow semantics.
- Dedicated #25 test must be committed before production changes and must not be weakened after valid RED.
- Dynamic methodology remains local/owned/sandboxed/explicitly authorized and bounded; no arbitrary code execution, privilege escalation, weaponized heap shaping, persistence, destructive corruption, malware, evasion, or unauthorized target is a proof requirement.
- After behavioral GREEN, only `README.md` and `docs/operator-depth-contract.md` may change before exact-head verification.

---

### Task 1: Freeze profile #25 semantics with a dedicated RED test

**Files:**
- Create: `tests/test_memory_lifetime_depth.py`

**Interfaces:**
- Consumes: current canonical `skills/memory-lifetime-analysis/SKILL.md`, current 24-profile registry.
- Produces: four assertion groups for canonical SKILL depth, runbook methodology, review-case semantics, and exactly-one registry promotion from 24 to 25.

- [ ] **Step 1: Write the failing test**

The test must require these SKILL sections:

- `## Causal memory-lifetime model`
- `## Object identity, owner, and alias generations`
- `## Invalidation, destruction, and reuse binding`
- `## Callback, asynchronous work, and refcount lifecycle`
- `## Final consumer and bounded effect binding`
- `## Memory-lifetime evidence ladder`
- `## Counterfactual proof`
- `## Alternative explanations`
- `## Evidence ceiling`

It must freeze the causal chain from logical object identity through acquisition/owner/alias/refcount/invalidation/destruction/reuse/async work/final consumer/effective capability/result/lifecycle, the required distinctions, and ML0–ML5.

The runbook test must require the six common sections plus:

- Object identity and allocation-generation trace
- Ownership and alias trace
- Retain, borrow, and refcount trace
- Invalidation and destruction trace
- Address and handle reuse trace
- Callback and asynchronous-work trace
- Cancellation, teardown, and error-path trace
- Final consumer and effective capability trace
- Counterfactual controls
- Alternative explanations
- Evidence promotion and ceiling

The review-case test must require at least these IDs:

- `stale-callback-after-retirement`
- `address-reuse-object-identity-confusion`
- `duplicate-release-refcount-generation`
- `cancellation-completion-teardown-race`

Each case must contain substantive strings for:

`hypothesis`, `safe_oracle`, `positive_control`, `negative_control`, `stop_condition`, `remediation_oracle`, `object_identity_generation`, `owner_alias_state`, `acquisition_release_trace`, `invalidation_event`, `destruction_generation`, `reuse_generation`, `retain_borrow_refcount_state`, `async_work_identity`, `cancellation_teardown_state`, `final_consumer_identity`, `effective_lifetime_capability`, `bounded_result`, `receipt_result_binding`, `counterfactual_control`, `alternative_explanation`, `evidence_level`, and `evidence_ceiling`.

The registry test must require version 2, exactly 25 profiles, exactly one `memory-lifetime-analysis`, the standard runbook/matrix paths, `lab_only: true`, and the common six required sections.

- [ ] **Step 2: Commit only the dedicated test after design + plan**

The test-first SHA must contain no memory-lifetime runbook, review-case matrix, registry promotion, SKILL deepening, or public-doc publication.

- [ ] **Step 3: Open Draft PR on the exact test-first SHA**

Record base, design SHA, plan SHA, test-first SHA, intended ten-path final scope, causal model, and safety boundary.

- [ ] **Step 4: Verify RED**

Expected full test authority: existing validators and 24-profile semantics remain green while the four dedicated #25 assertion groups fail because the new depth artifacts and promotion do not yet exist. No import/read/syntax error may substitute for the intended RED.

---

### Task 2: Deepen the canonical memory-lifetime skill

**Files:**
- Modify: `skills/memory-lifetime-analysis/SKILL.md`

**Interfaces:**
- Consumes: the design's causal model and dedicated #25 test.
- Produces: portable causal lifetime reasoning without absorbing sanitizer, concurrency, type-confusion, or exploitability responsibilities.

- [ ] **Step 1: Preserve canonical frontmatter and existing portable sections**

Keep `When to use`, `Preconditions`, `Workflow`, `Evidence contract`, `Stop conditions`, and `Output`.

- [ ] **Step 2: Add the exact causal model and identity/generation semantics**

Include logical object identity, allocation/acquisition generation, owner/alias set, retain/borrow/refcount state, invalidation/retirement, destruction/release generation, reuse generation, async work identity, final consumer, effective stale/double-use capability, result/receipt, and lifecycle generation.

- [ ] **Step 3: Add ML0–ML5, counterfactuals, alternatives, and evidence ceiling**

Explicitly state that sanitizer output, crash, address reuse, refcount anomaly, or queued callbacks cannot skip missing causal bindings.

---

### Task 3: Add the operator runbook

**Files:**
- Create: `skills/memory-lifetime-analysis/references/operator-runbook.md`

**Interfaces:**
- Consumes: design invariants ML-I1 through ML-I6.
- Produces: falsifiable lifetime investigation methodology usable in local/owned/sandboxed review.

- [ ] **Step 1: Add all common contract sections**

Include exact headings:
`Attack surface`, `Hypothesis matrix`, `Controlled validation`, `False-positive controls`, `Evidence capture`, `Remediation checks`.

- [ ] **Step 2: Add domain-specific trace sections**

Include all eleven required lifetime-specific trace/control headings from Task 1.

- [ ] **Step 3: Encode safe experimental methodology**

Use synthetic object pools, deterministic handles/slots, fake refcount ledgers, inert callbacks/consumers, controlled barriers, bounded markers/read-only results, and explicit abort boundaries.

---

### Task 4: Add deterministic benign review cases

**Files:**
- Create: `skills/memory-lifetime-analysis/references/operator-review-cases.json`

**Interfaces:**
- Consumes: ML invariants and runbook.
- Produces: version-1 machine-readable review matrix with at least four cases.

- [ ] **Step 1: Create all four required scenarios**

Each scenario must use a distinct lifetime mechanism and deterministic safe oracle.

- [ ] **Step 2: Fill every required field substantively**

Every required string must be at least 40 characters, safe oracle must name `synthetic`, `mock`, `inert`, `read-only`, or `controlled`, stop condition must explicitly say stop/abort/do not proceed, and evidence fields must contain ML0–ML5.

- [ ] **Step 3: Keep consequences bounded**

No real credentials, production objects, arbitrary code execution, heap grooming, persistence, or destructive corruption.

---

### Task 5: Register profile #25

**Files:**
- Modify: `operator-depth/profiles.json`

**Interfaces:**
- Consumes: created runbook and matrix.
- Produces: exactly one sorted `memory-lifetime-analysis` entry.

- [ ] **Step 1: Add one registry entry**

Use:
- `runbook: references/operator-runbook.md`
- `scenario_matrix: references/operator-review-cases.json`
- `lab_only: true`
- exact six common required runbook sections.

- [ ] **Step 2: Preserve schema version 2 and all existing entries**

Target registry count after promotion: 25.

---

### Task 6: Repair only the previous profile's stale global count if the behavioral run proves it

**Files:**
- Potentially modify: `tests/test_guest_host_boundary_depth.py`

**Interfaces:**
- Consumes: behavioral failure after profile #25 registration.
- Produces: future-extensible global count assertion while preserving all profile-specific #24 assertions.

- [ ] **Step 1: Run full behavioral CI without preemptively editing #24**

If #24 fails only because it asserts exactly 24 total profiles, treat that as a pre-existing extensibility defect.

- [ ] **Step 2: Apply the minimal compatibility correction**

Change only the global count from exact 24 to at-least 24. Do not weaken the exact-one guest-host entry, artifact paths, `lab_only`, required sections, or any #25 test.

- [ ] **Step 3: Require full 9/9 behavioral GREEN**

All six OS/Python matrix jobs plus `benchmark-core`, `agent-eval-core`, and `superiority-court-core` must complete successfully.

---

### Task 7: Publish public documentation only after behavioral GREEN

**Files:**
- Modify: `README.md`
- Modify: `docs/operator-depth-contract.md`

**Interfaces:**
- Consumes: behavioral authority SHA.
- Produces: public count 25, profile #25 description, and ML0–ML5 evidence ladder.

- [ ] **Step 1: Update README**

Change the operator-depth count from 24 to 25 and add `memory-lifetime-analysis` as the twenty-fifth profile with its causal semantics.

- [ ] **Step 2: Update operator-depth contract**

Add profile #25 and the complete ML0–ML5 ladder.

- [ ] **Step 3: Prove docs-only delta**

Compare behavioral authority to final head. The delta must be exactly two paths: README and operator-depth contract.

---

### Task 8: Exact-head integration and closure

**Files:**
- No new code paths.

**Interfaces:**
- Consumes: exact final head after docs publication.
- Produces: merged, post-merge-verified profile #25 with recorded provenance.

- [ ] **Step 1: Require exact-head 9/9 GREEN**

Do not create any commit after this run completes successfully.

- [ ] **Step 2: Fresh-check integration**

Confirm current main equals the expected base, PR head equals the exact GREEN head, final changed paths are exactly the intended ten, and PR is mergeable.

- [ ] **Step 3: Guarded merge**

Merge with `expected_head_sha=<exact final head>`.

- [ ] **Step 4: Verify merge parents**

Parent 1 must be pre-merge main; parent 2 must be exact reviewed head.

- [ ] **Step 5: Require post-merge 9/9 GREEN on exact merge SHA**

Check aggregate `completed/success` and all nine jobs.

- [ ] **Step 6: Read merge-tree registry/README/contract**

Verify registry version 2, exactly 25 profiles, one valid memory-lifetime entry, README count 25, and ML0–ML5 contract publication.

- [ ] **Step 7: Record closure provenance**

Document design, plan, RED, any compatibility repair, behavioral authority, docs-only delta, exact-head run, guarded merge, merge parents, post-merge run, merge-tree verification, final scope, safety boundary, and no external-superiority claim.
