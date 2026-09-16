# Wave 10 Secrets and Token Flow Depth Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add Wave 10 operator-depth profile #16 by turning `secrets-and-token-flow-analysis` into a causal credential-authority method with deterministic synthetic review artifacts, S0-S5 evidence ceilings, verifier-context reasoning, delegation attenuation, and revocation-generation controls.

**Architecture:** Keep the existing canonical skill identity and routing metadata unchanged. Add a credential-authority causal model, operator runbook, deterministic synthetic review cases, one additive operator-depth registry entry, and one dedicated contract test; synchronize public docs only after behavioral GREEN. Preserve graph, packs, routing, benchmark, agent-eval, and superiority-court authority unchanged.

**Tech Stack:** Markdown Agent Skills, JSON registry/review fixtures, Python `unittest`, GitHub Actions matrix validation.

**Spec:** `docs/superpowers/specs/2026-09-16-wave10-secrets-token-flow-depth-design.md`

## Global Constraints

- Base is `main@7077edaa96853309530f39002467d1df1348dc8e`.
- Only the nine paths enumerated in the spec may change.
- Do not modify `skill.meta.json`, graph edges, packs, routing domains, benchmark fixtures/thresholds, agent-eval authority, or superiority-court authority.
- Dynamic validation is restricted to synthetic/test credentials, synthetic principals/tenants, deterministic mock issuers/verifiers, inert capability markers, read-only services, policy simulators, or reversible owner-controlled state.
- No real credentials, production sessions, third-party tokens, credential replay against external systems, credential dumping, phishing, token theft, destructive actions, persistence, evasion, malware, or unauthorized targets.
- Registry schema remains version `2`.
- Dedicated profile test uses additive `>= 16`, never an exact global profile count.
- README and `docs/operator-depth-contract.md` are changed only after behavioral GREEN.
- Do not claim empirical superiority over Claude-Red or any external system without an actual contestant run through the repository superiority court.

---

### Task 1: Lock the dedicated RED contract

**Files:**
- Create: `tests/test_secrets_token_flow_depth.py`

**Interfaces:**
- Consumes: current canonical `skills/secrets-and-token-flow-analysis/SKILL.md` and `operator-depth/profiles.json`.
- Produces: four dedicated assertions that fail until causal credential-authority skill depth, runbook, review cases, and profile #16 registration exist.

- [ ] **Step 1: Create the dedicated test first**

Use this exact structure:

```python
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "secrets-and-token-flow-analysis" / "SKILL.md"
RUNBOOK = ROOT / "skills" / "secrets-and-token-flow-analysis" / "references" / "operator-runbook.md"
CASES = ROOT / "skills" / "secrets-and-token-flow-analysis" / "references" / "operator-review-cases.json"
PROFILES = ROOT / "operator-depth" / "profiles.json"


class SecretsTokenFlowDepthTests(unittest.TestCase):
    def test_skill_exposes_causal_credential_authority_model(self):
        text = SKILL.read_text(encoding="utf-8")
        for section in (
            "## Causal credential-authority model",
            "## Credential-class model",
            "## Issuance provenance and binding",
            "## Possession, storage, and propagation",
            "## Verifier-decision trace",
            "## Token-class integrity",
            "## Authority representation and attenuation",
            "## Lifecycle, rotation, and revocation generation",
            "## Credential-authority evidence ladder",
            "## Counterfactual proof",
            "## Alternative explanations",
            "## Evidence ceiling",
        ):
            self.assertIn(section, text)

        lower = text.lower()
        for concept in (
            "credential origin -> issuer identity -> subject identity -> credential class -> issuance constraints -> possession channel -> storage representation -> propagation hop -> verifier identity -> verification decision -> audience/resource binding -> represented authority -> downstream exchange/delegation -> attenuated effective authority -> bounded action/result -> lifecycle/revocation generation",
            "secret bytes != authority semantics",
            "issuer identity != subject identity",
            "possession != permission",
            "valid signature/mac != valid authorization context",
            "identity token != access token",
            "delegated authority != deputy/downstream ambient authority",
            "audience validity != resource authorization",
            "expiry time != revocation generation",
            "s0",
            "s1",
            "s2",
            "s3",
            "s4",
            "s5",
            "counterfactual",
            "evidence ceiling",
        ):
            self.assertIn(concept, lower)

    def test_runbook_requires_transition_level_credential_reasoning(self):
        self.assertTrue(RUNBOOK.is_file(), "secrets/token operator runbook must exist before depth can pass")
        text = RUNBOOK.read_text(encoding="utf-8")
        for section in (
            "## Attack surface",
            "## Hypothesis matrix",
            "## Credential-class trace",
            "## Issuance provenance trace",
            "## Possession and storage trace",
            "## Propagation-boundary trace",
            "## Verifier-decision trace",
            "## Audience and resource binding",
            "## Authority representation trace",
            "## Delegation and attenuation trace",
            "## Lifecycle and revocation-generation trace",
            "## Result and receipt binding",
            "## Controlled validation",
            "## False-positive controls",
            "## Counterfactual controls",
            "## Evidence capture",
            "## Evidence promotion and ceiling",
            "## Remediation checks",
        ):
            self.assertIn(section, text)

        lower = text.lower()
        for phrase in (
            "credential class",
            "issuer identity",
            "subject identity",
            "audience/resource",
            "verifier identity",
            "represented authority",
            "attenuated effective authority",
            "revocation generation",
            "token class",
            "counterfactual",
            "alternative explanation",
            "evidence ceiling",
        ):
            self.assertIn(phrase, lower)

    def test_review_cases_encode_credential_authority_reasoning(self):
        self.assertTrue(CASES.is_file(), "secrets/token review-case matrix must exist before depth can pass")
        payload = json.loads(CASES.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 1)
        self.assertGreaterEqual(len(payload["scenarios"]), 3)
        required = (
            "hypothesis",
            "safe_oracle",
            "positive_control",
            "negative_control",
            "stop_condition",
            "remediation_oracle",
            "credential_origin",
            "issuer_identity",
            "subject_identity",
            "credential_class",
            "issuance_constraints",
            "possession_channel",
            "storage_representation",
            "propagation_hop",
            "verifier_identity",
            "verification_decision",
            "audience_resource_binding",
            "represented_authority",
            "downstream_exchange",
            "attenuated_effective_authority",
            "bounded_result",
            "lifecycle_generation",
            "revocation_generation",
            "token_class_control",
            "counterfactual_control",
            "alternative_explanation",
            "evidence_level",
            "evidence_ceiling",
        )
        for scenario in payload["scenarios"]:
            for field in required:
                self.assertIn(field, scenario)
                self.assertIsInstance(scenario[field], str)
                self.assertGreaterEqual(len(scenario[field].strip()), 40)

    def test_skill_is_registered_as_sixteenth_operator_depth_profile(self):
        payload = json.loads(PROFILES.read_text(encoding="utf-8"))
        profiles = payload["profiles"]
        self.assertGreaterEqual(len(profiles), 16)
        matching = [p for p in profiles if p["skill"] == "secrets-and-token-flow-analysis"]
        self.assertEqual(len(matching), 1)
        profile = matching[0]
        self.assertEqual(profile["runbook"], "references/operator-runbook.md")
        self.assertEqual(profile["scenario_matrix"], "references/operator-review-cases.json")
        self.assertTrue(profile["lab_only"])
        self.assertEqual(
            profile["required_runbook_sections"],
            [
                "Attack surface",
                "Hypothesis matrix",
                "Controlled validation",
                "False-positive controls",
                "Evidence capture",
                "Remediation checks",
            ],
        )


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Commit the test without implementation artifacts**

Commit message:

```text
test: lock secrets and token flow depth contract
```

- [ ] **Step 3: Run the full repository workflow and record clean RED**

Expected dedicated failures:

- missing causal credential-authority sections/concepts in the current skill;
- missing `references/operator-runbook.md`;
- missing `references/operator-review-cases.json`;
- no `secrets-and-token-flow-analysis` entry and fewer than 16 profiles.

The RED run is valid only if canonical-skill validation, current 15-profile operator-depth validation, graph/index checks, benchmark validation, portability benchmark, and agent-eval portability smoke remain healthy before the dedicated test fails. Unexpected unittest errors or unrelated failures must be debugged rather than accepted.

---

### Task 2: Implement the causal credential-authority depth artifacts

**Files:**
- Modify: `skills/secrets-and-token-flow-analysis/SKILL.md`
- Create: `skills/secrets-and-token-flow-analysis/references/operator-runbook.md`
- Create: `skills/secrets-and-token-flow-analysis/references/operator-review-cases.json`
- Modify: `operator-depth/profiles.json`
- Test: `tests/test_secrets_token_flow_depth.py`

**Interfaces:**
- Consumes: the exact RED contract from Task 1 and the causal model in the design spec.
- Produces: canonical skill depth, operator runbook, deterministic review cases, and additive profile registration #16.

- [ ] **Step 1: Replace the short checklist-oriented skill body with the causal model while preserving frontmatter identity**

The resulting `SKILL.md` must contain these exact headings:

```text
## When to use
## Preconditions
## Causal credential-authority model
## Credential-class model
## Issuance provenance and binding
## Possession, storage, and propagation
## Verifier-decision trace
## Token-class integrity
## Authority representation and attenuation
## Lifecycle, rotation, and revocation generation
## Workflow
## Credential-authority evidence ladder
## Counterfactual proof
## Alternative explanations
## Evidence contract
## Evidence ceiling
## Stop conditions
## Output
```

It must include the exact causal chain and distinctions frozen by the test, define S0-S5 as in the spec, distinguish cryptographic validity from semantic verification and authorization, model credential exchange/delegation attenuation, and keep all dynamic validation synthetic/owned/read-only/reversible.

- [ ] **Step 2: Create the operator runbook**

`operator-runbook.md` must include every section required by the test. For each trace, require both observed value and proof source. Controlled validation must prescribe one-dimension synthetic controls for issuer, subject, audience/resource, token class, verifier identity, revocation generation, reduced ambient privilege, narrower downstream exchange, and remediation regression. It must explicitly prohibit real-token replay and secret-value capture.

- [ ] **Step 3: Create deterministic review cases**

Create JSON version `1` with exactly three initial scenarios named:

```text
issuance-verification-binding
propagation-and-token-class-integrity
delegation-attenuation-and-revocation
```

Every required field in Task 1 must be a substantive string of at least 40 characters. Use synthetic opaque credentials, deterministic mock issuers/verifiers, inert markers, fake tenants/principals, bounded policy decisions, and reversible owner-controlled effects. Each scenario must contain a safe oracle, positive/negative controls, stop condition, remediation oracle, token-class control, counterfactual, alternative explanation, evidence level, and evidence ceiling.

- [ ] **Step 4: Register profile #16 additively**

Add exactly one entry to `operator-depth/profiles.json`:

```json
{
  "skill": "secrets-and-token-flow-analysis",
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

Preserve schema version `2` and every existing profile unchanged.

- [ ] **Step 5: Run the dedicated test and operator-depth validator**

Expected:

```text
python -m unittest tests.test_secrets_token_flow_depth -v
# 4 tests, all PASS

python scripts/validate_operator_depth.py
# PASS with >= 16 profiles and no schema/path errors
```

- [ ] **Step 6: Commit the behavioral implementation**

Commit message:

```text
feat: deepen secrets and token flow reasoning
```

- [ ] **Step 7: Run full GitHub Actions and require behavioral GREEN**

All six Ubuntu/macOS/Windows x Python 3.11/3.13 matrix jobs plus `benchmark-core`, `agent-eval-core`, and `superiority-court-core` must succeed. Public docs remain untouched until this full GREEN run is recorded on the behavioral SHA.

---

### Task 3: Synchronize public documentation after behavioral GREEN

**Files:**
- Modify: `README.md`
- Modify: `docs/operator-depth-contract.md`

**Interfaces:**
- Consumes: verified profile #16 behavioral implementation from Task 2.
- Produces: public snapshot and operator-depth history synchronized to 16 profiles without changing behavior.

- [ ] **Step 1: Update README counts and Wave 10 narrative**

Change every current operator-depth total from 15 to 16 where it describes the current baseline. Add `secrets-and-token-flow-analysis` as the sixteenth profile and summarize its causal contribution as credential-class semantics, issuance provenance, possession/storage/propagation boundaries, verifier-decision traces, audience/resource binding, represented-authority reasoning, delegation attenuation, revocation generations, counterfactual controls, deterministic audit-only review cases, and S0-S5 evidence ceilings.

- [ ] **Step 2: Update `docs/operator-depth-contract.md`**

Append `secrets-and-token-flow-analysis` as the sixteenth Wave 10 profile and update the current registry count to 16. Preserve Wave 8 history and all descriptions for profiles #9-#15 unchanged.

- [ ] **Step 3: Verify the docs-only delta**

Compare behavioral GREEN SHA to docs head and require exactly:

```text
README.md
docs/operator-depth-contract.md
```

No skill, test, registry, workflow, benchmark, agent-eval, or superiority-court artifact may change after behavioral GREEN.

- [ ] **Step 4: Commit docs**

Commit message:

```text
docs: publish secrets and token flow depth
```

---

### Task 4: Exact-head verification and PR closure

**Files:**
- No new behavioral files.
- PR metadata/provenance only after the final candidate SHA is fixed.

**Interfaces:**
- Consumes: final candidate containing Tasks 1-3 only.
- Produces: exact-head CI evidence, reviewable PR provenance, and guarded merge.

- [ ] **Step 1: Open a Draft PR from `wave10-secrets-token-flow-depth` to `main`**

PR body must record base SHA, design/plan commits, RED run, behavioral GREEN SHA/run, final candidate SHA, exact nine-file scope, unchanged authority surfaces, and safety boundary. Explicitly state that no empirical superiority over external systems is claimed.

- [ ] **Step 2: Verify exact changed-file scope**

Require exactly the nine paths in the spec and no others.

- [ ] **Step 3: Require exact-head full CI GREEN**

On the final candidate SHA, require all six matrix jobs plus `benchmark-core`, `agent-eval-core`, and `superiority-court-core` to complete successfully. If any job fails, inspect steps/logs and debug the root cause before changing the branch.

- [ ] **Step 4: Mark Ready only after exact-head GREEN**

Re-read PR head/base immediately before transition. Head must equal the exact verified candidate and base must remain intended `main` lineage.

- [ ] **Step 5: Merge with expected-head SHA guard**

Use the final candidate SHA as `expected_head_sha`. Abort rather than merge if GitHub reports drift.

---

### Task 5: Post-merge verification

**Files:**
- No source changes.

**Interfaces:**
- Consumes: actual merge commit returned by GitHub.
- Produces: final closure evidence for operator-depth profile #16.

- [ ] **Step 1: Verify `main` points to the merge commit**

Confirm merge parents are previous `main` and final candidate.

- [ ] **Step 2: Locate the push-triggered workflow on the merge SHA**

Require event `push`, branch `main`, and exact merge `head_sha`.

- [ ] **Step 3: Require post-merge full GREEN**

All six matrix jobs plus `benchmark-core`, `agent-eval-core`, and `superiority-court-core` must succeed on the merge commit.

- [ ] **Step 4: Verify registry and public docs on the merge SHA**

`operator-depth/profiles.json` must contain at least 16 profiles and exactly one `secrets-and-token-flow-analysis` registration. README and operator-depth contract must both publish the 16-profile current baseline.

- [ ] **Step 5: Record final provenance on the PR**

Record merge SHA and post-merge run ID. Only after this fresh evidence may profile #16 be called closed.
