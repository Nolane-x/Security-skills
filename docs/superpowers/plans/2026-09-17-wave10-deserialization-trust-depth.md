# Wave 10 Deserialization Trust Depth Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add Wave 10 operator-depth profile #20 for `deserialization-trust-analysis` with deterministic causal reconstruction-trust semantics, safe review cases, exact-head verification, and guarded merge.

**Architecture:** Keep the canonical 83-skill graph unchanged and deepen one existing skill in place. Add one dedicated contract test first, then deepen `SKILL.md`, add a domain runbook and deterministic review-case matrix, register exactly one profile, require behavioral full GREEN, and only then update the two public documentation files.

**Tech Stack:** Markdown, JSON, Python 3 standard library `unittest`, existing repository validators, GitHub Actions matrix on Linux/macOS/Windows × Python 3.11/3.13.

**Spec:** `docs/superpowers/specs/2026-09-17-wave10-deserialization-trust-depth-design.md`

## Global Constraints

- Base exactly on `main@6b8e0f36fee255a985d39aa8178598d58e1e21ad`.
- Keep `operator-depth/profiles.json` schema version `2`.
- Add exactly one registration for `deserialization-trust-analysis` with `lab_only: true`.
- Do not modify `skill.meta.json`, graph edges, packs, routing domains, benchmark fixtures/thresholds, agent-eval authority, superiority-court authority, or workflow semantics.
- Dedicated test is written before production behavior and is not changed after a valid RED unless the test itself is proven wrong.
- Safety proof is local/owned/sandboxed and uses synthetic artifacts, inert callbacks, mock registries/services, read-only synthetic capabilities, or bounded reversible owner-controlled effects.
- Do not require gadget-chain development, command execution, arbitrary file writes, external network access, credential theft, production secrets, persistence, malware, destructive effects, public-registry manipulation, or unauthorized targets.
- Complete PR scope is exactly nine paths listed in the design spec.
- External superiority claims remain out of scope.

---

### Task 1: Freeze the deserialization depth contract RED-first

**Files:**
- Create: `tests/test_deserialization_trust_depth.py`

**Interfaces:**
- Consumes: existing canonical skill, future runbook/review-case paths, and `operator-depth/profiles.json`.
- Produces: four deterministic `unittest` contract groups for canonical skill semantics, runbook semantics, review-case schema, and registry registration.

- [ ] **Step 1: Write the failing dedicated test**

Create `tests/test_deserialization_trust_depth.py` with these exact contract families:

```python
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "deserialization-trust-analysis" / "SKILL.md"
RUNBOOK = ROOT / "skills" / "deserialization-trust-analysis" / "references" / "operator-runbook.md"
CASES = ROOT / "skills" / "deserialization-trust-analysis" / "references" / "operator-review-cases.json"
PROFILES = ROOT / "operator-depth" / "profiles.json"


class DeserializationTrustDepthTests(unittest.TestCase):
    def test_skill_exposes_causal_reconstruction_trust_model(self):
        text = SKILL.read_text(encoding="utf-8")
        for section in (
            "## Causal reconstruction-trust model",
            "## Reconstruction identity and type binding",
            "## Construction, hooks, and secondary interpretation",
            "## Authenticity and reconstructed authority",
            "## Lifecycle and generation reasoning",
            "## Deserialization evidence ladder",
            "## Counterfactual proof",
            "## Alternative explanations",
            "## Evidence ceiling",
        ):
            self.assertIn(section, text)

        lower = text.lower()
        for concept in (
            "serialized artifact origin -> transport/storage envelope identity -> authenticity/integrity context -> format/parser identity -> syntax and canonical field state -> schema identity and schema version -> discriminator/variant state -> type registry/resolver identity and registry generation -> resolved runtime type identity -> object construction path and object-graph identity -> constructor/setter/post-load hook state -> secondary interpretation state -> caller/request authority context -> requested reconstructed capability -> policy/allowlist decision -> effective reconstructed authority -> privileged consumer or behavior boundary -> bounded synthetic effect -> receipt/result binding -> schema/registry/object lifecycle generation",
            "parser acceptance != schema authorization",
            "schema validation != runtime type authorization",
            "discriminator/alias string != resolved runtime type identity",
            "payload authenticity != capability authorization",
            "object construction != side-effect authorization",
            "constructor/hook reachability != security impact",
            "data field != later secondary interpretation",
            "current schema/registry/object generation != stale generation",
            "unexpected type selection != exploitability",
            "dt0",
            "dt1",
            "dt2",
            "dt3",
            "dt4",
            "dt5",
            "counterfactual",
            "evidence ceiling",
        ):
            self.assertIn(concept, lower)

    def test_runbook_requires_transition_level_deserialization_reasoning(self):
        self.assertTrue(RUNBOOK.is_file(), "deserialization operator runbook must exist before depth can pass")
        text = RUNBOOK.read_text(encoding="utf-8")
        for section in (
            "## Attack surface",
            "## Hypothesis matrix",
            "## Artifact origin and authenticity trace",
            "## Parser and canonical-field trace",
            "## Schema identity and version trace",
            "## Discriminator and registry-resolution trace",
            "## Runtime type and object-construction trace",
            "## Hook/callback and secondary-interpretation trace",
            "## Authority and reconstruction-policy trace",
            "## Privileged-consumer and result trace",
            "## Lifecycle/schema/registry generation trace",
            "## Controlled validation",
            "## False-positive controls",
            "## Counterfactual controls",
            "## Alternative explanations",
            "## Evidence capture",
            "## Evidence promotion and ceiling",
            "## Remediation checks",
        ):
            self.assertIn(section, text)

        lower = text.lower()
        for phrase in (
            "registry generation",
            "schema version",
            "runtime type identity",
            "secondary interpretation",
            "reconstructed authority",
            "receipt/result",
            "inert callback",
            "data-only",
            "debug-only",
            "alternative explanation",
            "evidence ceiling",
        ):
            self.assertIn(phrase, lower)

    def test_review_cases_encode_reconstruction_trust_reasoning(self):
        self.assertTrue(CASES.is_file(), "deserialization review-case matrix must exist before depth can pass")
        payload = json.loads(CASES.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 1)
        self.assertGreaterEqual(len(payload["scenarios"]), 3)
        required_ids = {
            "type-registry-binding",
            "construction-hook-capability-binding",
            "schema-registry-generation-binding",
        }
        self.assertTrue(required_ids.issubset({scenario["id"] for scenario in payload["scenarios"]}))
        required = (
            "hypothesis",
            "safe_oracle",
            "positive_control",
            "negative_control",
            "stop_condition",
            "remediation_oracle",
            "artifact_origin",
            "envelope_authentication_context",
            "format_parser_identity",
            "canonical_field_state",
            "schema_identity_version",
            "discriminator_state",
            "registry_resolver_identity",
            "registry_generation",
            "runtime_type_identity",
            "object_construction_path",
            "hook_callback_surface",
            "secondary_interpretation",
            "authority_context",
            "requested_reconstructed_capability",
            "policy_decision",
            "effective_reconstructed_authority",
            "privileged_consumer",
            "bounded_result",
            "receipt_result_binding",
            "lifecycle_generation",
            "counterfactual_control",
            "alternative_explanation",
            "evidence_level",
            "evidence_ceiling",
        )
        safe_terms = ("synthetic", "mock", "inert", "read-only", "controlled", "canary")
        for scenario in payload["scenarios"]:
            for field in required:
                self.assertIn(field, scenario)
                self.assertIsInstance(scenario[field], str)
                self.assertGreaterEqual(len(scenario[field].strip()), 40)
            self.assertTrue(any(term in scenario["safe_oracle"].lower() for term in safe_terms))
            self.assertTrue(any(term in scenario["stop_condition"].lower() for term in ("stop", "abort", "do not proceed")))
            self.assertRegex(scenario["evidence_level"], r"\bDT[0-5]\b")
            self.assertRegex(scenario["evidence_ceiling"], r"\bDT[0-5]\b")

    def test_skill_is_registered_as_twentieth_operator_depth_profile(self):
        payload = json.loads(PROFILES.read_text(encoding="utf-8"))
        self.assertEqual(payload["version"], 2)
        profiles = payload["profiles"]
        self.assertGreaterEqual(len(profiles), 20)
        matching = [p for p in profiles if p["skill"] == "deserialization-trust-analysis"]
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
```

- [ ] **Step 2: Commit the dedicated test only**

```bash
git add tests/test_deserialization_trust_depth.py
git commit -m "test: freeze deserialization trust depth contract"
```

- [ ] **Step 3: Open a Draft PR at the exact test-first SHA**

PR title: `Wave 10: deepen deserialization trust reasoning`.

- [ ] **Step 4: Observe RED without changing the test**

Required RED characteristics:

```text
new dedicated file present
4 intended dedicated test-method failures
0 unexpected unittest errors
existing skill validation PASS
existing 19-profile operator-depth validation PASS
existing graph/index/benchmark/agent-eval/superiority-court gates remain green before dedicated assertion failure
```

If RED differs, inspect the failing job/log and repair only a genuinely incorrect test or infrastructure issue.

### Task 2: Implement the causal deserialization profile

**Files:**
- Modify: `skills/deserialization-trust-analysis/SKILL.md`
- Create: `skills/deserialization-trust-analysis/references/operator-runbook.md`
- Create: `skills/deserialization-trust-analysis/references/operator-review-cases.json`
- Modify: `operator-depth/profiles.json`
- Test: `tests/test_deserialization_trust_depth.py`

**Interfaces:**
- Consumes: exact test contract from Task 1 and design semantics from the spec.
- Produces: one additive operator-depth profile with DT0–DT5 evidence semantics and three deterministic safe review cases.

- [ ] **Step 1: Deepen canonical `SKILL.md` without changing frontmatter identity**

Preserve `name`, description category, version, and authorization metadata. Add the exact section headings frozen by Task 1 and the exact causal-chain sentence. Include all frozen distinctions using the `!=` wording required by the test, DT0–DT5 ladder, counterfactual controls, alternative explanations, and explicit evidence ceiling.

- [ ] **Step 2: Add the operator runbook**

Create `references/operator-runbook.md` with every exact heading frozen by the test. Require transition-level traces for artifact origin/authenticity, parser/canonical fields, schema/version, discriminator/registry resolution, runtime type/object construction, hooks/secondary interpretation, authority/policy, privileged consumer/result, and lifecycle generations.

The runbook must state that acceptable proof uses synthetic artifacts, mock registries/services, inert callbacks, read-only synthetic capabilities, or bounded reversible effects, and must stop before command execution, arbitrary writes, external network effects, persistence, malware, destructive actions, or unauthorized systems.

- [ ] **Step 3: Add deterministic review cases**

Create version-1 JSON with at least the exact IDs:

```json
{
  "version": 1,
  "scenarios": [
    {"id": "type-registry-binding"},
    {"id": "construction-hook-capability-binding"},
    {"id": "schema-registry-generation-binding"}
  ]
}
```

Expand every scenario so every required field from Task 1 is a substantive string of at least 40 characters. Use DT levels and ceilings appropriate to the proof. `safe_oracle` must mention a synthetic/mock/inert/read-only/controlled/canary mechanism; `stop_condition` must explicitly say stop/abort/do not proceed.

- [ ] **Step 4: Add exactly one registry entry**

Add one alphabetically placed `deserialization-trust-analysis` object to `operator-depth/profiles.json`:

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

Do not change schema version 2.

- [ ] **Step 5: Commit the behavioral implementation**

```bash
git add operator-depth/profiles.json skills/deserialization-trust-analysis/SKILL.md skills/deserialization-trust-analysis/references/operator-runbook.md skills/deserialization-trust-analysis/references/operator-review-cases.json
git commit -m "feat: deepen deserialization trust reasoning"
```

### Task 3: Establish behavioral GREEN authority

**Files:**
- No intended file changes.

**Interfaces:**
- Consumes: behavioral head from Task 2.
- Produces: one exact SHA that has passed the complete repository CI authority.

- [ ] **Step 1: Require all GitHub Actions jobs on the behavioral SHA to finish**

Expected authority:

```text
6/6 Linux/macOS/Windows × Python 3.11/3.13 matrix jobs SUCCESS
benchmark-core SUCCESS
agent-eval-core SUCCESS
superiority-court-core SUCCESS
deterministic byte-identical checks SUCCESS
cautious/faulty controls SUCCESS
```

- [ ] **Step 2: If any job fails, inspect the exact failed job and make the smallest semantic correction**

Do not edit the dedicated test unless it is demonstrably wrong. Any correction creates a new behavioral SHA and requires the complete authority again.

- [ ] **Step 3: Lock the first full-GREEN behavioral SHA as behavioral authority**

Record the exact SHA and workflow run ID in the PR body/provenance.

### Task 4: Finalize public docs only after behavioral GREEN

**Files:**
- Modify: `README.md`
- Modify: `docs/operator-depth-contract.md`

**Interfaces:**
- Consumes: behavioral GREEN authority.
- Produces: final candidate whose post-GREEN delta is exactly two documentation files.

- [ ] **Step 1: Update profile counts from 19 to 20**

Update the stable-baseline sentence, architecture diagram count, current snapshot table, operator-depth summary, and explicit profile list in `README.md`.

- [ ] **Step 2: Document `deserialization-trust-analysis` as profile #20**

Summarize causal reconstruction semantics: artifact/authenticity context, parser/canonical state, schema/version, discriminator-to-runtime-type registry binding, construction/hooks/secondary interpretation, represented/effective reconstructed authority, lifecycle generations, deterministic review cases, counterfactual controls, and DT0–DT5 ceilings.

- [ ] **Step 3: Update `docs/operator-depth-contract.md` consistently**

Raise the registry/profile count to 20 and add the same profile #20 semantics without changing general validator authority.

- [ ] **Step 4: Commit docs only**

```bash
git add README.md docs/operator-depth-contract.md
git commit -m "docs: publish deserialization trust depth profile"
```

- [ ] **Step 5: Prove docs-only delta from behavioral authority**

Compare behavioral GREEN SHA to final candidate and require exactly:

```text
README.md
docs/operator-depth-contract.md
```

### Task 5: Exact-head verification and guarded integration

**Files:**
- No intended file changes after exact-head GREEN.

**Interfaces:**
- Consumes: final candidate SHA.
- Produces: merged `main` commit with verified parents, post-merge GREEN, and closure provenance.

- [ ] **Step 1: Verify total PR path scope is exactly nine files**

Required set:

```text
README.md
docs/operator-depth-contract.md
docs/superpowers/plans/2026-09-17-wave10-deserialization-trust-depth.md
docs/superpowers/specs/2026-09-17-wave10-deserialization-trust-depth-design.md
operator-depth/profiles.json
skills/deserialization-trust-analysis/SKILL.md
skills/deserialization-trust-analysis/references/operator-review-cases.json
skills/deserialization-trust-analysis/references/operator-runbook.md
tests/test_deserialization_trust_depth.py
```

- [ ] **Step 2: Require full CI GREEN on the exact final candidate SHA**

Do not create any further commit after this succeeds unless a real defect is discovered.

- [ ] **Step 3: Fresh integration check immediately before merge**

Verify:

```text
PR head == exact final candidate SHA
PR base == main
current main == 6b8e0f36fee255a985d39aa8178598d58e1e21ad
changed paths == exact nine-path set
mergeable state allows merge
no base drift
```

If `main` drifted, stop the merge and reconcile/re-run exact-head authority instead of merging stale work.

- [ ] **Step 4: Mark Ready and merge with expected-head guard**

Use merge commit mode with `expected_head_sha=<exact-final-head>`.

- [ ] **Step 5: Verify merge commit parent lineage**

Require:

```text
parent 1 == pre-merge main
parent 2 == exact final PR head
main == merge commit SHA
```

- [ ] **Step 6: Require post-merge push CI GREEN on the exact merge SHA**

All six matrix jobs and the three deterministic core jobs must be successful.

- [ ] **Step 7: Verify merged registry/docs directly on the merge SHA**

Require profile count at least 20, exactly one `deserialization-trust-analysis` registration, and public docs declaring 20 profiles/profile #20.

- [ ] **Step 8: Add closure provenance comment to the PR**

Record design SHA, plan SHA, test-first SHA, RED run, behavioral GREEN SHA/run, final candidate SHA/run, merge SHA, post-merge run, exact nine-path scope, and the bounded safety statement.
