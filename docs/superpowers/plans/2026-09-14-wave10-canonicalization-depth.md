# Wave 10 Canonicalization and Namespace Depth Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Promote `canonicalization-and-namespace-analysis` into operator-depth profile #13 with a representation/identity graph, deterministic audit cases, CI-enforced methodology, and full RED→GREEN→exact-head→post-merge provenance.

**Architecture:** Keep the existing canonical skill as the single portable capability and deepen it with a typed representation-to-object model. Add local operator artifacts under the skill, register them in the existing version-2 operator-depth registry, freeze domain semantics in one dedicated additive test, and leave graph/routing/benchmark/evaluator authority unchanged.

**Tech Stack:** Markdown Agent Skills, JSON operator-depth registry/review cases, Python `unittest`, zero third-party dependencies, GitHub Actions matrix on Ubuntu/macOS/Windows with Python 3.11/3.13.

**Spec:** `docs/superpowers/specs/2026-09-14-wave10-canonicalization-depth-design.md`

## Global Constraints

- Base exactly from `main@a917b24f6408539e388cdf3e17e8bb1db515b4bd`.
- Use only owned/local/sandboxed/synthetic/mock/inert/read-only/explicitly authorized fixtures.
- Do not create operational bypass recipes or touch production/sensitive resources.
- Do not change `skill.meta.json`, graph edges, packs, routing domains, benchmark fixtures/thresholds, agent-eval authority, or superiority-court authority.
- Preserve `operator-depth/profiles.json` schema version `2`.
- Use `references/operator-review-cases.json` for the machine-readable artifact.
- Registry-count assertions must be additive (`>= 13`), never exact global ownership.
- Public docs are updated only after behavioral GREEN.
- Merge only after exact-head CI is fully green and use expected-head SHA protection.

---

### Task 1: Freeze profile #13 semantics with a dedicated failing test

**Files:**
- Create: `tests/test_canonicalization_namespace_depth.py`

**Interfaces:**
- Consumes: existing canonical skill at `skills/canonicalization-and-namespace-analysis/SKILL.md` and registry at `operator-depth/profiles.json`.
- Produces: four deterministic contract tests for canonical prose, runbook, review cases, and additive profile registration.

- [ ] **Step 1: Create the dedicated test before implementation artifacts**

The test must define:

```python
ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "canonicalization-and-namespace-analysis" / "SKILL.md"
RUNBOOK = ROOT / "skills" / "canonicalization-and-namespace-analysis" / "references" / "operator-runbook.md"
CASES = ROOT / "skills" / "canonicalization-and-namespace-analysis" / "references" / "operator-review-cases.json"
PROFILES = ROOT / "operator-depth" / "profiles.json"
```

Freeze these canonical sections:

```text
## Representation and identity graph
## Transformation ordering and non-commutativity
## Normalization idempotence
## Equivalence, collision, ambiguity, and aliasing
## Policy-key to resolved-identity invariant
## Namespace-root and authority binding
## Boundary-preserving normalization
## Name-to-object transition
## Mutable namespace and identity drift
## Namespace evidence ladder
## Counterfactual proof
## Alternative explanations
## Evidence ceiling
```

Freeze the exact causal chain:

```text
raw input -> parsed representation -> decoded representation -> normalized representation -> policy key -> resolver input -> resolved identity -> opened handle/object identity
```

Require the concepts `non-commutativity`, `idempotence`, `resolver equivalence`, `policy equivalence`, `namespace root`, `namespace generation`, `name-to-object`, `N0` through `N5`, `counterfactual`, and `evidence ceiling`.

Freeze these runbook sections:

```text
## Attack surface
## Hypothesis matrix
## Representation and identity trace
## Transformation-order trace
## Equivalence and ambiguity trace
## Policy-key and resolver binding
## Namespace-root binding
## Name-to-object and generation trace
## Controlled validation
## False-positive controls
## Counterfactual controls
## Evidence capture
## Evidence promotion and ceiling
## Remediation checks
```

Require at least three review cases. For every case, require the common fields plus:

```text
representation_chain
transform_order
normalization_idempotence
equivalence_class
policy_key
resolver_input
resolved_identity
namespace_root
object_binding
namespace_generation
counterfactual_control
alternative_explanation
evidence_level
evidence_ceiling
```

Require each domain field to be a string with at least 40 non-whitespace characters.

For registry registration, require exactly one matching skill entry, the two relative artifact paths, `lab_only: true`, the existing six required runbook sections, and `len(profiles) >= 13`.

- [ ] **Step 2: Commit the test without implementation artifacts**

Commit message:

```text
test: define canonicalization depth contract
```

- [ ] **Step 3: Open a Draft PR and let CI prove clean RED**

The expected full unittest result is four assertion failures and zero unittest errors:

1. canonical depth sections/concepts absent;
2. runbook absent;
3. review-case matrix absent;
4. profile count/registration absent.

Existing canonical validation, 12-profile operator-depth validation, graph/index checks, benchmark validation, portability, and agent portability smoke must remain green before the dedicated test failures.

- [ ] **Step 4: Record the RED run ID and exact failing-test count in the PR body**

Do not proceed to implementation if RED contains import errors, JSON errors, unrelated regression failures, or more/fewer than the four intended contract failures.

---

### Task 2: Deepen the canonical skill

**Files:**
- Modify: `skills/canonicalization-and-namespace-analysis/SKILL.md`

**Interfaces:**
- Consumes: the design's representation/identity model and Task 1 test contract.
- Produces: portable canonical methodology independent of operator-depth registry details.

- [ ] **Step 1: Replace checklist-only depth with the typed representation/identity graph**

Add the exact causal chain and explain representation equality, normalized equality, resolver equivalence, policy equivalence, and object identity as distinct relations.

- [ ] **Step 2: Add transform-order and idempotence methodology**

State that transform order is observable and potentially non-commutative. Define idempotence as a stability property and explicitly state that idempotence failure alone does not prove a security consequence.

- [ ] **Step 3: Add equivalence/collision/ambiguity/aliasing distinctions**

Prevent syntactic oddity from being promoted without sink-identity evidence.

- [ ] **Step 4: Add policy-key↔resolved-identity, namespace-root, boundary, and name-to-object invariants**

Require the checked policy key to denote the same intended identity that the sink resolves under the same root/authority context. Record whether execution uses a bound object or re-resolves a name.

- [ ] **Step 5: Add mutable-namespace generation reasoning and N0–N5 evidence ceiling**

Keep generic race mechanics out of scope; record only name-to-object identity drift and state/generation evidence relevant to resolution.

- [ ] **Step 6: Add counterfactual and alternative-explanation sections**

Require one-variable synthetic counterfactuals and explicit benign explanations before evidence promotion.

- [ ] **Step 7: Commit canonical methodology**

Commit message:

```text
feat: deepen canonicalization identity reasoning
```

---

### Task 3: Add the operator runbook

**Files:**
- Create: `skills/canonicalization-and-namespace-analysis/references/operator-runbook.md`

**Interfaces:**
- Consumes: canonical methodology from Task 2.
- Produces: operator-level trace discipline satisfying both the central validator and dedicated test.

- [ ] **Step 1: Add required common sections exactly**

Include `Attack surface`, `Hypothesis matrix`, `Controlled validation`, `False-positive controls`, `Evidence capture`, and `Remediation checks` as exact `##` headings.

- [ ] **Step 2: Add domain-specific trace sections exactly**

Include the domain headings frozen by Task 1 and describe a trace record containing the raw/parsed/decoded/normalized representations, policy key, resolver input, resolved identity, root/authority, object binding, and namespace generation/state.

- [ ] **Step 3: Add authorization and lab boundary**

State that all dynamic observations use owned, sandboxed, synthetic, mock, inert, read-only, test-only, or explicitly authorized resources and stop before production/sensitive effects.

- [ ] **Step 4: Add false-positive and counterfactual discipline**

Require neighboring valid controls, alternative explanations, and one-variable counterfactuals before promoting evidence.

- [ ] **Step 5: Add N0–N5 evidence promotion/ceiling and remediation regression**

A remediation check must preserve intended equivalent names/neighboring identities while removing the causal divergence.

- [ ] **Step 6: Commit the runbook**

Commit message:

```text
docs: add canonicalization operator runbook
```

---

### Task 4: Add deterministic audit-only review cases

**Files:**
- Create: `skills/canonicalization-and-namespace-analysis/references/operator-review-cases.json`

**Interfaces:**
- Consumes: Task 1 JSON contract and central `validate_operator_depth.py` common field requirements.
- Produces: version-1 deterministic matrix with at least three safe cases.

- [ ] **Step 1: Create `transform-order-consistency`**

Use a synthetic/read-only fixture. Record the full representation chain, actual transform sequence, idempotence observation, policy key, resolver input, resolved identity, controls, alternative explanations, and a conservative evidence ceiling.

- [ ] **Step 2: Create `namespace-root-binding`**

Use a controlled synthetic namespace with two benign roots/authorities. The oracle compares recorded policy and resolver roots without accessing sensitive resources.

- [ ] **Step 3: Create `name-to-object-generation-binding`**

Use a synthetic object/handle record and read-only generation/state labels. Demonstrate how evidence is capped when the name-to-object state is stale or not bound.

- [ ] **Step 4: Validate every common oracle/stop condition**

Every `safe_oracle` must explicitly name a safe mechanism such as `synthetic`, `read-only`, `controlled`, `mock`, `inert`, or `test`. Every `stop_condition` must explicitly say `stop`, `abort`, or `do not` proceed beyond the authorized boundary.

- [ ] **Step 5: Commit the review cases**

Commit message:

```text
testdata: add canonicalization review cases
```

---

### Task 5: Register profile #13 and obtain behavioral GREEN

**Files:**
- Modify: `operator-depth/profiles.json`

**Interfaces:**
- Consumes: runbook/review cases from Tasks 3–4.
- Produces: one alphabetically positioned CI-enforced profile registration.

- [ ] **Step 1: Add the registry entry**

Insert:

```json
{
  "skill": "canonicalization-and-namespace-analysis",
  "runbook": "references/operator-runbook.md",
  "scenario_matrix": "references/operator-review-cases.json",
  "lab_only": true,
  "required_runbook_sections": ["Attack surface", "Hypothesis matrix", "Controlled validation", "False-positive controls", "Evidence capture", "Remediation checks"]
}
```

Preserve schema version `2` and existing profiles unchanged.

- [ ] **Step 2: Commit the registry change**

Commit message:

```text
feat: register canonicalization depth profile
```

- [ ] **Step 3: Run/observe CI on the behavioral head**

Require all six matrix jobs to pass:

```text
ubuntu-latest 3.11
ubuntu-latest 3.13
macos-latest 3.11
macos-latest 3.13
windows-latest 3.11
windows-latest 3.13
```

Each must pass canonical skills, 13-profile operator depth, graph, generated-index checks, benchmark validation, portability, agent-eval contracts/smoke, and full unittest discovery.

- [ ] **Step 4: Require all core determinism jobs**

Require `benchmark-core`, `agent-eval-core`, and `superiority-court-core` to pass their double-run byte-identical checks and existing negative-control exercises.

Do not update README/docs until this behavioral checkpoint is fully green.

---

### Task 6: Synchronize public documentation

**Files:**
- Modify: `README.md`
- Modify: `docs/operator-depth-contract.md`

**Interfaces:**
- Consumes: behavioral GREEN proof from Task 5.
- Produces: public 13-profile snapshot without altering unrelated counts or historical claims.

- [ ] **Step 1: Update README profile counts 12→13**

Update only operator-depth count text/table/diagram and the Wave 10 profile list.

- [ ] **Step 2: Add profile #13 description**

Describe representation/identity graph, transform ordering/non-commutativity, policy-key↔resolved-identity binding, namespace roots, name-to-object/generation state, N0–N5 ceiling, and deterministic audit cases.

- [ ] **Step 3: Update `docs/operator-depth-contract.md`**

Add `canonicalization-and-namespace-analysis` as the thirteenth profile and change the current registry count from 12 to 13 while preserving Wave 8 history.

- [ ] **Step 4: Commit docs synchronization**

Commit message:

```text
docs: publish canonicalization depth profile
```

---

### Task 7: Freeze final head, verify scope, and merge

**Files:**
- No new files; inspect the final nine-path diff.

**Interfaces:**
- Consumes: final docs-synced branch head.
- Produces: exact-head verification, merge provenance, and post-merge verification on main.

- [ ] **Step 1: Review changed filenames**

Require exactly the nine paths listed in the design spec. Verify no change to metadata, graph, packs, routing, benchmarks, evaluator authority, or court authority.

- [ ] **Step 2: Review README and operator-depth contract patches separately**

Confirm they contain only count/list/current-profile wording changes.

- [ ] **Step 3: Freeze final head and run exact-head CI**

No commits after the verification SHA is selected. Require six matrix jobs plus all three core determinism jobs to succeed on that exact SHA.

- [ ] **Step 4: Update PR provenance**

Record base SHA, test-first commit, RED run and failure count, behavioral GREEN SHA/run, exact-head SHA/run, changed-file scope, and safety boundary.

- [ ] **Step 5: Mark PR ready and merge with expected-head guard**

Reject the merge if the head moved.

- [ ] **Step 6: Verify `main` points to the returned merge commit**

Read the branch/commit directly rather than assuming the merge state.

- [ ] **Step 7: Require push-triggered post-merge CI**

On the merge commit, require all six OS/Python matrix jobs, `benchmark-core`, `agent-eval-core`, and `superiority-court-core` to succeed before claiming profile #13 complete.
