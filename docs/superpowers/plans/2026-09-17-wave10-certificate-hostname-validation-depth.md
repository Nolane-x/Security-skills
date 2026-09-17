# Wave 10 Certificate And Hostname Validation Depth Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add Wave 10 operator-depth profile #20 for the existing `certificate-and-hostname-validation-analysis` skill, enforcing deterministic causal TLS/X.509 identity, policy, callback, lifecycle, and evidence reasoning.

**Architecture:** Keep the existing canonical skill identity and routing metadata unchanged. Add a dedicated test-first semantic contract, deepen the canonical skill, add a transition-level operator runbook plus machine-readable benign review cases, register exactly one lab-only profile, then publish the new count/semantics only after behavioral CI is fully green.

**Tech Stack:** Markdown, JSON, Python 3 `unittest`, repository validators, GitHub Actions matrix on Ubuntu/macOS/Windows × Python 3.11/3.13, benchmark-core, agent-eval-core, superiority-court-core.

**Spec:** `docs/superpowers/specs/2026-09-17-wave10-certificate-hostname-validation-depth-design.md`

## Global Constraints

- Base exact current main: `6b8e0f36fee255a985d39aa8178598d58e1e21ad`.
- Target existing canonical skill only: `certificate-and-hostname-validation-analysis`.
- Final operator-depth profile count must be exactly 20 on this lineage.
- `operator-depth/profiles.json` schema/version remains `2`.
- The new registration must have `lab_only: true`, runbook `references/operator-runbook.md`, and matrix `references/operator-review-cases.json`.
- Do not modify `skill.meta.json`, graph edges, packs, routing domains, benchmark fixtures/thresholds, agent-eval authority, superiority-court authority, or CI workflow semantics.
- Dynamic validation remains local/owned/sandbox/synthetic/explicitly authorized only.
- No third-party hostname impersonation, unrelated traffic interception, production certificates/private keys, persistence, evasion, destructive actions, credential theft, or unauthorized access.
- Do not claim external superiority from internal court results.
- Dedicated test is immutable after valid RED unless the test itself is proven incorrect.
- Behavioral artifacts must be full GREEN before `README.md` or `docs/operator-depth-contract.md` changes.
- Final PR scope is exactly nine files listed in the design spec.
- Exact-head GREEN must occur before guarded merge; no commit may follow exact-head GREEN.

---

### Task 1: Freeze the certificate/hostname depth contract with a failing test

**Files:**
- Create: `tests/test_certificate_hostname_validation_depth.py`
- Read: `skills/certificate-and-hostname-validation-analysis/SKILL.md`
- Read: `operator-depth/profiles.json`
- Reference pattern: `tests/test_browser_process_boundary_depth.py`

**Interfaces:**
- Consumes: the design spec and current nineteen-profile registry.
- Produces: four dedicated `unittest` methods that fail only because profile #20 semantics/artifacts do not exist yet.

- [ ] **Step 1: Create the dedicated test with four semantic groups**

Use `Path(__file__).resolve().parents[1]` and define paths for the canonical skill, new runbook, new review cases, and profile registry.

The first test must require these exact canonical sections:

```python
required_sections = (
    "## Causal certificate and peer-identity model",
    "## Peer identity and reference binding",
    "## Path construction and trust-anchor authority",
    "## Certificate policy and application decision",
    "## Pinning and mutual TLS binding",
    "## Session, revocation, and lifecycle reasoning",
    "## Certificate identity evidence ladder",
    "## Counterfactual proof",
    "## Alternative explanations",
    "## Evidence ceiling",
)
```

It must also require the canonical causal-chain text, all domain distinctions from the spec, `PKI0` through `PKI5`, `counterfactual`, and `evidence ceiling`.

The second test must require the common runbook sections plus:

```python
required_runbook_sections = (
    "## Connection intent and reference identity trace",
    "## Endpoint routing and TLS context trace",
    "## Presented chain and constructed path trace",
    "## Trust anchor and trust-store generation trace",
    "## Certificate policy and name-binding trace",
    "## Verifier callback and final-decision trace",
    "## Pin policy and pin-generation trace",
    "## mTLS identity and principal-mapping trace",
    "## Session cache and resumption trace",
    "## Revocation and lifecycle-generation trace",
    "## Counterfactual controls",
    "## Alternative explanations",
    "## Evidence promotion and ceiling",
)
```

The third test must require `version == 1`, at least three scenarios, and these IDs:

```python
{
    "peer-identity-chain-hostname-binding",
    "callback-pin-policy-binding",
    "lifecycle-resumption-mtls-binding",
}
```

Every scenario must contain the common fields plus substantive strings for:

```python
(
    "connection_intent",
    "reference_identifier",
    "endpoint_authority",
    "transport_peer",
    "tls_role_context",
    "presented_chain",
    "constructed_path",
    "trust_anchor_identity",
    "trust_store_generation",
    "chain_validation_result",
    "certificate_time_state",
    "eku_key_usage_policy",
    "name_constraints_state",
    "san_identity_binding",
    "library_verifier_result",
    "application_override",
    "pin_policy_state",
    "pin_generation",
    "client_certificate_identity",
    "principal_mapping",
    "final_accept_reject",
    "bounded_result",
    "session_resumption_state",
    "revocation_state",
    "lifecycle_generation",
    "counterfactual_control",
    "alternative_explanation",
    "evidence_level",
    "evidence_ceiling",
)
```

Require each substantive field to be a string of at least 40 non-whitespace characters. Require safe-oracle language to include at least one of `synthetic`, `mock`, `inert`, `read-only`, `controlled`, `local`, or `canary`; stop conditions must contain `stop`, `abort`, or `do not proceed`; evidence fields must contain `PKI0`–`PKI5`.

The fourth test must require registry version 2, exact profile count 20, exactly one registration for `certificate-and-hostname-validation-analysis`, correct paths, `lab_only: true`, and the six standard required runbook sections.

- [ ] **Step 2: Commit only the dedicated test**

```bash
git add tests/test_certificate_hostname_validation_depth.py
git commit -m "test: define certificate hostname operator-depth contract"
```

Record this exact SHA as the test-first authority.

- [ ] **Step 3: Open a Draft PR at the exact test-first SHA**

The PR body must record base SHA, design SHA, plan SHA, test-first SHA, intended nine-file scope, safety boundary, and explicitly state that RED is expected only from the new dedicated contract.

- [ ] **Step 4: Run/observe RED CI and verify the failure shape**

Expected dedicated failures before implementation:

1. canonical skill missing required causal-depth sections/phrases;
2. operator runbook missing;
3. review-case matrix missing;
4. twentieth registry entry missing / count remains 19.

The run is valid RED only if there are zero unexpected unittest errors and all pre-existing validators/gates pass before these intended assertions fail. If any old gate fails, investigate that failure before production implementation.

---

### Task 2: Deepen the canonical certificate/hostname skill

**Files:**
- Modify: `skills/certificate-and-hostname-validation-analysis/SKILL.md`
- Test: `tests/test_certificate_hostname_validation_depth.py`

**Interfaces:**
- Consumes: the causal model, distinctions, evidence ladder, counterfactuals, safety boundary from the spec.
- Produces: the canonical human-readable security reasoning contract used by the runbook and cases.

- [ ] **Step 1: Replace the shallow workflow with the causal model**

Preserve the YAML front matter name/description/metadata. Add the exact canonical chain from the spec and explain each transition, including endpoint/routing context, presented-vs-constructed chain, trust-anchor identity/generation, policy/name binding, verifier/callback decision, optional pin/mTLS mapping, bounded result, and session/revocation/lifecycle state.

- [ ] **Step 2: Add the required identity/policy distinctions**

Encode each distinction explicitly with the `!=` form frozen by the test. Explain why each prevents a false promotion rather than merely listing it.

- [ ] **Step 3: Add PKI0–PKI5 evidence semantics**

The levels must preserve repository evidence philosophy: observations and tool output stay below validated status until transition-level causal proof, controls, and bounded effect exist; regression verification requires remediation oracle plus legitimate-neighbor preservation.

- [ ] **Step 4: Add counterfactuals, alternatives, evidence ceiling, and safety stop conditions**

Counterfactuals must isolate one transition. Alternatives must include routing/SNI mismatch, intended proxy termination, platform path-building differences, clock skew, stale session/cache, offline revocation policy, development-only trust paths, and retry/fallback confusion where applicable.

Do not include real-host interception instructions, public CA abuse, production credential use, or validation-disablement as proof.

---

### Task 3: Add the transition-level operator runbook

**Files:**
- Create: `skills/certificate-and-hostname-validation-analysis/references/operator-runbook.md`
- Test: `tests/test_certificate_hostname_validation_depth.py`

**Interfaces:**
- Consumes: canonical causal model and PKI evidence ladder.
- Produces: repeatable audit methodology that an operator can execute entirely with synthetic/local fixtures.

- [ ] **Step 1: Add the six common required sections**

Use exact headings:

```text
## Attack surface
## Hypothesis matrix
## Controlled validation
## False-positive controls
## Evidence capture
## Remediation checks
```

- [ ] **Step 2: Add every domain trace section frozen by the dedicated test**

For each transition, specify what identity/state to record, which deterministic control isolates it, what result promotes evidence, and what must remain unresolved if the evidence is absent.

- [ ] **Step 3: Define a safe controlled validation sequence**

The runbook sequence must use only a synthetic CA/certificate hierarchy, synthetic hostnames, local TLS endpoints or mock verifier callbacks, local trust/pin stores, and inert bounded results. It must record exact platform/library/configuration identity so path-building differences are reproducible.

- [ ] **Step 4: Define false-positive and alternative-explanation controls**

At minimum cover hostname-vs-chain separation, selected-vs-present trust anchor, callback override, pin-policy scope, mTLS mapping, stale session/cache behavior, revocation policy, SNI/routing mismatch, proxy termination, and debug-only configuration.

- [ ] **Step 5: Define remediation regression checks**

The fix oracle must reject the original invalid synthetic binding while preserving valid neighboring hostnames/chains/pins/client mappings; stale sessions/caches must converge to the corrected lifecycle generation according to the documented product policy.

---

### Task 4: Add deterministic benign review cases

**Files:**
- Create: `skills/certificate-and-hostname-validation-analysis/references/operator-review-cases.json`
- Test: `tests/test_certificate_hostname_validation_depth.py`

**Interfaces:**
- Consumes: runbook fields and evidence semantics.
- Produces: deterministic machine-readable scenarios accepted by the operator-depth validator.

- [ ] **Step 1: Create version 1 payload with exactly three initial scenarios**

Use the three IDs from Task 1. Every common/domain-specific field must be substantive and case-specific, not copied filler.

- [ ] **Step 2: Encode `peer-identity-chain-hostname-binding`**

Use a synthetic local hostname and synthetic CA hierarchy. The positive control keeps the chain/path valid and matches the intended reference identity. The negative control changes only the name/path transition under test. The safe oracle observes the local final decision and inert connection result.

- [ ] **Step 3: Encode `callback-pin-policy-binding`**

Model a local verifier result, application callback/override, versioned synthetic pin policy, final decision, and bounded result. Controls must distinguish an application override problem from a legitimate pin policy and from normal PKI behavior without pinning.

- [ ] **Step 4: Encode `lifecycle-resumption-mtls-binding`**

Model trust/pin/certificate lifecycle generation, fresh vs resumed/cached verification state, and a synthetic client-certificate-to-principal mapping. Controls must distinguish certificate possession from application-principal authorization and stale session state from current-policy acceptance.

- [ ] **Step 5: Validate JSON determinism and safety wording**

All scenario IDs are unique. All required fields are strings, no secrets or real hostnames are present, stop conditions abort before third-party/production interaction, and evidence levels never exceed the described proof.

---

### Task 5: Register exactly one twentieth profile and reach behavioral GREEN

**Files:**
- Modify: `operator-depth/profiles.json`
- Modify/Create from Tasks 2–4: canonical skill, runbook, cases
- Test: `tests/test_certificate_hostname_validation_depth.py`

**Interfaces:**
- Consumes: completed behavioral artifacts.
- Produces: one new lab-only operator-depth registration and a behavioral candidate with no public-doc changes.

- [ ] **Step 1: Add one alphabetically placed registry object**

The object is exactly:

```json
{
  "skill": "certificate-and-hostname-validation-analysis",
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

Keep registry `version` at 2 and total profiles at exactly 20.

- [ ] **Step 2: Commit behavioral implementation without README/docs-contract changes**

The behavioral commit may include exactly these four files:

```text
operator-depth/profiles.json
skills/certificate-and-hostname-validation-analysis/SKILL.md
skills/certificate-and-hostname-validation-analysis/references/operator-review-cases.json
skills/certificate-and-hostname-validation-analysis/references/operator-runbook.md
```

The dedicated test remains unchanged from the RED authority.

- [ ] **Step 3: Run the dedicated test and repository validators**

Expected local/deterministic results before relying on GitHub Actions:

```bash
python -m unittest tests.test_certificate_hostname_validation_depth -v
python scripts/validate_skills.py
python scripts/validate_operator_depth.py
python scripts/validate_graph.py
python scripts/validate_benchmarks.py
```

All must pass.

- [ ] **Step 4: Observe full behavioral CI on the exact behavioral SHA**

Require all six OS/Python matrix jobs plus `benchmark-core`, `agent-eval-core`, and `superiority-court-core` to succeed. If a dedicated assertion fails, fix production artifacts, not the frozen test, unless the test is factually wrong.

Record the exact behavioral SHA and run ID/number once full GREEN is confirmed.

---

### Task 6: Publish profile #20 only after behavioral GREEN

**Files:**
- Modify: `README.md`
- Modify: `docs/operator-depth-contract.md`

**Interfaces:**
- Consumes: exact behavioral GREEN SHA and established certificate/hostname semantics.
- Produces: public docs reflecting 20 profiles without changing behavior.

- [ ] **Step 1: Update README counts and Wave 10 profile narrative**

Change operator-depth profile count from 19 to 20 wherever the English README publishes the current count. Add `certificate-and-hostname-validation-analysis` as the twentieth profile and summarize its new semantics: intended reference identity, constructed path/trust-anchor identity, trust-store generation, certificate-policy/name binding, verifier/callback/final decision, pin and mTLS mapping, session/resumption/revocation lifecycle, deterministic synthetic review cases, counterfactual controls, and PKI0–PKI5 evidence ceilings.

Do not alter unrelated README sections.

- [ ] **Step 2: Update `docs/operator-depth-contract.md`**

Change the current registry count from 19 to 20, add the twentieth profile to the Wave 10 history/list, and document the certificate/hostname causal-depth additions consistently with the canonical skill and runbook.

- [ ] **Step 3: Commit only the two public docs**

After this commit, compare behavioral GREEN SHA to final candidate and require exactly:

```text
README.md
docs/operator-depth-contract.md
```

No behavioral file may differ in the post-GREEN delta.

---

### Task 7: Exact-head verification, guarded integration, and closure

**Files:**
- No new paths.
- Read final PR metadata, changed paths, registry, README, and operator-depth contract.

**Interfaces:**
- Consumes: docs-only final candidate.
- Produces: guarded merge with complete provenance and post-merge verification.

- [ ] **Step 1: Prove complete PR scope**

List changed filenames and require exactly the nine paths in the design spec. Compare branch base to final candidate and ensure no hidden authority changes exist.

- [ ] **Step 2: Observe full exact-head CI**

On the exact final candidate SHA require all six matrix jobs plus `benchmark-core`, `agent-eval-core`, and `superiority-court-core` GREEN. Record run ID/number and exact SHA. Do not create further commits afterward.

- [ ] **Step 3: Fresh integration check immediately before merge**

Fetch current `main`, PR head/base, mergeable state, and changed paths. Require current `main` still equals the PR's intended base lineage; if it moved, investigate/rebase by a new verified cycle rather than merging stale assumptions.

- [ ] **Step 4: Mark ready and guarded-merge**

Mark the Draft PR ready only after all prior gates pass. Merge with merge method `merge` and `expected_head_sha` equal to the exact final candidate SHA.

- [ ] **Step 5: Verify merge topology**

Fetch the merge commit. Require parent 1 to equal the pre-merge main SHA and parent 2 to equal the exact final PR head. Require `main` to resolve to the merge SHA.

- [ ] **Step 6: Observe post-merge push CI on the exact merge SHA**

Require the same full matrix/core gates to be GREEN. Do not infer post-merge health from the PR run.

- [ ] **Step 7: Read closure authority directly from merge SHA**

Read `operator-depth/profiles.json`, `README.md`, and `docs/operator-depth-contract.md` at the merge SHA. Confirm exactly 20 profiles, exactly one certificate/hostname registration, and public documentation consistent with the registry.

- [ ] **Step 8: Add closure provenance comment**

Record design SHA, plan SHA, test-first SHA, RED CI evidence, behavioral GREEN SHA/run, final candidate SHA/exact-head run, pre-merge main, merge SHA and parents, post-merge run, exact nine-path scope, and the statement that no external superiority claim is made.

Only after this comment and post-merge verification may profile #20 be declared complete.
