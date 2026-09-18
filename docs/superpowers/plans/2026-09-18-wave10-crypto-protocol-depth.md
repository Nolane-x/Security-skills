# Wave 10 Cryptographic Protocol Depth Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Promote `cryptographic-protocol-misuse-analysis` to Wave 10 operator-depth profile #23 with deterministic causal protocol-composition reasoning and a CP0–CP5 evidence ceiling.

**Architecture:** Keep the existing canonical skill identity and registry schema. Add causal depth to the portable SKILL, a domain runbook, deterministic benign review cases, and a dedicated test-first contract. Preserve all benchmark/evaluation/workflow authorities. One existing profile #22 test receives a one-line extensibility maintenance change so future registry growth does not invalidate #22 semantics.

**Tech Stack:** Markdown Agent Skill, JSON operator-depth registry/review cases, Python `unittest`, zero third-party Python dependencies, GitHub Actions CI.

**Spec:** `docs/superpowers/specs/2026-09-18-wave10-crypto-protocol-depth-design.md`

## Global Constraints

- Exact base authority: `main@9318953f530ea7d88b07a8b19413e7ee77d74c00`.
- Target existing canonical skill: `cryptographic-protocol-misuse-analysis`.
- Registry remains schema/version `2`.
- Profile remains `lab_only: true`.
- All dynamic proof is local/owned/sandboxed/benchmark/CTF/explicitly authorized and uses synthetic keys/peers/vectors, mock/loopback transports, inert sinks, read-only traces, or bounded reversible owner-controlled effects.
- No brute-force of real keys/passwords, unrelated live-traffic interception/decryption, production credentials, persistence, malware, destruction, evasion, or unauthorized targeting.
- Dedicated #23 test is committed before production depth artifacts and is not weakened after RED.
- No `skill.meta.json`, graph-edge, pack, routing-domain, benchmark authority, agent-eval authority, superiority-court authority, or workflow-semantic change.
- After final behavioral GREEN, only `README.md` and `docs/operator-depth-contract.md` may change.
- Expected final scope is exactly ten paths, including the one-line #22 test extensibility maintenance.

---

### Task 1: Commit the dedicated profile #23 RED contract

**Files:**
- Create: `tests/test_cryptographic_protocol_misuse_depth.py`

**Interfaces:**
- Consumes: existing canonical skill, common operator-depth registry schema, Wave 10 test style.
- Produces: four failing assertion groups that freeze #23 semantics before implementation.

- [ ] **Step 1: Create the dedicated test**

The test must define:

```python
ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "cryptographic-protocol-misuse-analysis" / "SKILL.md"
RUNBOOK = ROOT / "skills" / "cryptographic-protocol-misuse-analysis" / "references" / "operator-runbook.md"
CASES = ROOT / "skills" / "cryptographic-protocol-misuse-analysis" / "references" / "operator-review-cases.json"
PROFILES = ROOT / "operator-depth" / "profiles.json"
```

It must contain exactly four test methods:

1. `test_skill_exposes_causal_protocol_composition_model`
2. `test_runbook_requires_transition_level_crypto_protocol_reasoning`
3. `test_review_cases_encode_crypto_protocol_reasoning`
4. `test_skill_is_registered_as_twenty_third_operator_depth_profile`

The first test must freeze the required SKILL sections and the exact causal transition string from the design, required distinctions, `CP0` through `CP5`, counterfactuals, alternatives, evidence ceiling, and local/owned/sandboxed safety language.

The runbook test must require at least these second-level sections in addition to the common sections:

```text
## Protocol intent and role/session trace
## Negotiation and downgrade trace
## Transcript and authenticated-negotiation trace
## Key schedule, role, direction, epoch, and domain-separation trace
## Nonce, sequence, and record identity trace
## Protocol phase and authenticated-context trace
## Verification and authentication-order trace
## Replay and freshness trace
## Rekey, resumption, and early-data lifecycle trace
## Privileged-consumer and result trace
## Counterfactual controls
## Alternative explanations
## Evidence promotion and ceiling
```

The review-case test must require four IDs:

```text
negotiation-transcript-binding
key-role-domain-separation
authenticate-before-use
replay-context-lifecycle-binding
```

and require all machine fields named in the spec, with substantive string values, benign safe-oracle terminology, explicit stop language, and `CP[0-5]` evidence values.

The registry test must require version 2, exactly 23 profiles, exactly one `cryptographic-protocol-misuse-analysis` entry, expected artifact paths, `lab_only: true`, and the unchanged common required-runbook-section list.

- [ ] **Step 2: Commit the test-first state**

Commit message:

```text
test: freeze Wave 10 crypto protocol depth
```

- [ ] **Step 3: Open Draft PR on the exact test-first SHA**

PR title:

```text
Wave 10: deepen cryptographic protocol misuse reasoning
```

The PR body records exact base, design SHA, plan SHA, test-first SHA, intended four RED failures, intended ten-path scope, causal contract, and safety boundary.

- [ ] **Step 4: Verify RED**

Use the pull-request-triggered `validate-security-skills` run on the exact test-first SHA.

Valid RED requires:

- the four dedicated #23 test methods fail for missing depth/artifacts/registry promotion;
- zero unittest errors;
- old canonical-skill/operator-depth/graph/index/benchmark/portability/agent-eval gates remain healthy before the intended dedicated failures;
- the #23 test file is not edited after this authority unless the test itself is proven wrong.

### Task 2: Implement the behavioral profile

**Files:**
- Modify: `skills/cryptographic-protocol-misuse-analysis/SKILL.md`
- Create: `skills/cryptographic-protocol-misuse-analysis/references/operator-runbook.md`
- Create: `skills/cryptographic-protocol-misuse-analysis/references/operator-review-cases.json`
- Modify: `operator-depth/profiles.json`
- Modify: `tests/test_certificate_hostname_depth.py`

**Interfaces:**
- Consumes: exact dedicated RED contract.
- Produces: profile #23 behavioral authority candidate.

- [ ] **Step 1: Deepen the canonical SKILL**

Retain frontmatter identity and authorization metadata. Expand the body to include:

- `## Causal protocol-composition model`
- `## Negotiation and transcript binding`
- `## Key schedule, role, epoch, and domain separation`
- `## Protocol phase and authenticated-context binding`
- `## Authenticate-before-use ordering`
- `## Replay, freshness, and early-data reasoning`
- `## Rekey, resumption, and lifecycle generations`
- `## Workflow`
- `## Cryptographic protocol evidence ladder`
- `## Counterfactual proof`
- `## Alternative explanations`
- `## Evidence ceiling`

The SKILL must use the exact causal chain and distinctions frozen by Task 1.

- [ ] **Step 2: Add the runbook**

Create all common required sections plus the domain-specific trace sections from Task 1.

The hypothesis matrix must cover at least:

- unauthenticated/downgraded negotiation state;
- incomplete key-role/domain separation;
- privileged use before authenticity decision;
- replay/context acceptance across session/epoch/resumption/early-data generations.

Controlled validation uses synthetic keys, synthetic peers, deterministic vectors, mock transports, and inert/read-only consumers.

- [ ] **Step 3: Add four deterministic review cases**

Create JSON:

```json
{
  "version": 1,
  "scenarios": [
    {"id": "negotiation-transcript-binding"},
    {"id": "key-role-domain-separation"},
    {"id": "authenticate-before-use"},
    {"id": "replay-context-lifecycle-binding"}
  ]
}
```

Each object must include all common and domain-specific fields required by the dedicated test. Every field must describe a deterministic benign experiment rather than an exploit recipe.

- [ ] **Step 4: Register profile #23**

Append exactly one registry entry:

```json
{
  "skill": "cryptographic-protocol-misuse-analysis",
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

Maintain deterministic ordering consistent with the existing registry.

- [ ] **Step 5: Apply known #22 extensibility maintenance**

In `tests/test_certificate_hostname_depth.py`, change only:

```python
self.assertEqual(len(profiles), 22)
```

to:

```python
self.assertGreaterEqual(len(profiles), 22)
```

Do not change any certificate/hostname-specific assertion.

- [ ] **Step 6: Commit behavioral implementation**

Commit message:

```text
feat: add cryptographic protocol operator depth
```

- [ ] **Step 7: Verify full behavioral CI**

Require all nine jobs GREEN on the exact behavioral candidate:

- Linux/macOS/Windows × Python 3.11/3.13;
- `benchmark-core`;
- `agent-eval-core`;
- `superiority-court-core`.

Require byte-identical checks and cautious/faulty controls to pass.

If any failure occurs, diagnose root cause before modification. Do not weaken the dedicated #23 test.

### Task 3: Publish public documentation only after behavioral GREEN

**Files:**
- Modify: `README.md`
- Modify: `docs/operator-depth-contract.md`

**Interfaces:**
- Consumes: exact behavioral 9/9 GREEN SHA.
- Produces: final reviewed candidate whose post-behavioral delta is exactly two paths.

- [ ] **Step 1: Update README**

Change published profile counts from 22 to 23 and identify `cryptographic-protocol-misuse-analysis` as the twenty-third profile.

Summarize protocol intent/role binding, negotiation/transcript authentication, key-role/domain separation, auth-before-use, replay/freshness, rekey/resumption lifecycle, and CP0–CP5.

- [ ] **Step 2: Update operator-depth contract**

Add profile #23 to the Wave 10 list and add a causal CP0–CP5 paragraph. Explicitly state that primitive approval, valid signatures/tags, handshake success, selected suites, unique nonces, or replay-cache observations cannot skip missing causal bindings.

- [ ] **Step 3: Commit publication**

Commit message:

```text
docs: publish cryptographic protocol depth after behavioral green
```

- [ ] **Step 4: Prove the post-behavioral delta**

Compare behavioral authority to final candidate. The changed files must be exactly:

```text
README.md
docs/operator-depth-contract.md
```

Any third path invalidates the final candidate and requires lineage repair/revalidation.

- [ ] **Step 5: Verify exact-head CI**

Require full 9/9 GREEN on the exact final head. No commits after this run succeeds.

### Task 4: Guarded integration and closure

**Files:**
- No source mutation after exact-head GREEN.
- PR body/comment metadata only.

**Interfaces:**
- Consumes: exact-head GREEN SHA.
- Produces: merged and post-merge-verified profile #23.

- [ ] **Step 1: Fresh integration check**

Immediately before merge verify:

- PR head equals exact GREEN SHA;
- PR base is `main`;
- current `main` still equals the branch base;
- PR is mergeable;
- changed files are exactly the ten intended paths;
- no forbidden authority files changed.

- [ ] **Step 2: Mark PR ready and guarded merge**

Use `expected_head_sha=<exact final head>`.

- [ ] **Step 3: Verify merge parents**

Merge commit parents must be exactly:

1. prior current-main SHA;
2. exact reviewed head SHA.

- [ ] **Step 4: Verify post-merge CI**

Require push-triggered full 9/9 GREEN on the exact merge SHA.

- [ ] **Step 5: Read merge-tree authority**

Verify directly from the merge commit:

- registry v2 with exactly 23 profiles and exactly one crypto-protocol profile with expected paths and `lab_only: true`;
- README publishes 23 profiles and profile #23;
- operator-depth contract publishes profile #23 and CP0–CP5.

- [ ] **Step 6: Write closure provenance comment**

Record design, plan, test-first SHA, RED run, behavioral SHA/run, exact final head/run, guarded merge SHA/parents, post-merge run, exact ten-path scope, #22 compatibility maintenance, safety boundary, and the explicit non-claim that repository conformance is not empirical superiority over external security systems.

Profile #23 is complete only after this comment is read back from the merged PR.
