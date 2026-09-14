# Wave 7 Operator Depth Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deepen four high-value canonical security skills with deterministic, lab-bounded operator runbooks and a CI-enforced operator-depth contract.

**Architecture:** Keep `skills/` as the canonical portable source and add a small `operator-depth/profiles.json` registry plus a zero-dependency validator. Extended methodology lives in per-skill `references/operator-runbook.md` files, linked from canonical `SKILL.md`; CI validates structure, containment, authorization, evidence, and control requirements without using file length as a quality proxy.

**Tech Stack:** Python 3.11/3.13 standard library, JSON, Markdown, `unittest`, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-09-14-wave7-operator-depth-contract-design.md`

## Global Constraints

- Keep the canonical skill count at exactly 83 for this wave.
- Add zero third-party Python dependencies.
- Preserve vendor-neutral Agent Skills portability.
- Dynamic methodology is limited to local, owned, sandboxed, CTF, benchmark, or explicitly authorized environments.
- Do not add exploit/payload catalogs, credential theft, persistence, destructive actions, uncontrolled scanning, real cloud-metadata probing, or production-secret handling.
- Every operator-depth profile must be evidence-first and include positive/negative false-positive controls.
- Existing Wave 5 deterministic benchmark and Wave 6 cross-agent evaluation gates must remain GREEN.

---

### Task 1: Freeze the operator-depth contract with RED tests

**Files:**
- Create: `tests/test_operator_depth.py`

**Interfaces:**
- Consumes: repository root layout and future CLI path `scripts/validate_operator_depth.py`.
- Produces: a subprocess-level contract for repository validation and negative fixture behavior.

- [ ] **Step 1: Write repository-success and negative-fixture tests**

```python
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_operator_depth.py"


def run_validator(root: Path):
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(root)],
        text=True,
        capture_output=True,
    )


def make_fixture(root: Path, *, runbook="references/operator-runbook.md", sections=None):
    sections = sections or [
        "Attack surface",
        "Hypothesis matrix",
        "Controlled validation",
        "False-positive controls",
        "Evidence capture",
        "Remediation checks",
    ]
    skill = root / "skills" / "fixture-skill"
    (skill / "references").mkdir(parents=True)
    (root / "operator-depth").mkdir()
    (skill / "SKILL.md").write_text(
        "---\nname: fixture-skill\ndescription: test\n---\n"
        "# Fixture\n\n## Operator depth\n"
        "See [operator runbook](references/operator-runbook.md).\n",
        encoding="utf-8",
    )
    manifest = {
        "version": 1,
        "profiles": [{
            "skill": "fixture-skill",
            "runbook": runbook,
            "lab_only": True,
            "required_runbook_sections": sections,
        }],
    }
    (root / "operator-depth" / "profiles.json").write_text(
        json.dumps(manifest), encoding="utf-8"
    )
    return skill


class OperatorDepthCliTests(unittest.TestCase):
    def test_repository_contract_passes(self):
        proc = run_validator(ROOT)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_rejects_missing_runbook(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            make_fixture(root)
            proc = run_validator(root)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("missing runbook", (proc.stdout + proc.stderr).lower())

    def test_rejects_runbook_path_escape(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            make_fixture(root, runbook="../outside.md")
            proc = run_validator(root)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("escapes skill directory", (proc.stdout + proc.stderr).lower())

    def test_rejects_missing_required_section(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            skill = make_fixture(root)
            (skill / "references" / "operator-runbook.md").write_text(
                "# Runbook\n\nAuthorized lab only.\n\n"
                "## Attack surface\nA\n"
                "## Hypothesis matrix\nB\n"
                "## Controlled validation\nC\n"
                "## False-positive controls\nD\n"
                "## Evidence capture\nE\n",
                encoding="utf-8",
            )
            proc = run_validator(root)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("remediation checks", (proc.stdout + proc.stderr).lower())
```

- [ ] **Step 2: Open a draft PR and verify RED**

Expected: `python -m unittest tests.test_operator_depth -v` fails because `scripts/validate_operator_depth.py` does not exist. The failure must be due to the missing implementation, not malformed test syntax.

- [ ] **Step 3: Commit the RED contract**

Commit message: `test: freeze Wave 7 operator depth contract`

---

### Task 2: Implement the deterministic validator and manifest

**Files:**
- Create: `scripts/validate_operator_depth.py`
- Create: `operator-depth/profiles.json`

**Interfaces:**
- Consumes: `--root PATH`, `operator-depth/profiles.json`, canonical `skills/<name>/SKILL.md`, runbook files.
- Produces: exit code `0` with a stable success line, or exit code `1` with sorted deterministic diagnostics.

- [ ] **Step 1: Implement argument parsing and manifest loading**

Use `argparse`, `json`, and `pathlib` only. Resolve the repository root, require manifest version `1`, require a non-empty profile list, and report parse/schema-shape errors through the same deterministic error collector.

- [ ] **Step 2: Implement per-profile structural validation**

For every profile:

```text
skill: non-empty string and unique
runbook: non-empty relative path
lab_only: exactly true
required_runbook_sections: non-empty list of unique non-empty strings
skills/<skill>/SKILL.md: must exist
runbook resolved from skill directory: must stay inside that skill directory
runbook: must exist as a file
SKILL.md: must contain the declared relative runbook link
runbook: must contain every required `## <section>` heading
```

- [ ] **Step 3: Implement semantic guard checks**

Require each runbook, case-insensitively, to contain language covering all three concepts:

```text
authorization/lab boundary: one of "authorized", "owned", "sandbox", "lab"
evidence: "evidence"
control discipline: "control"
```

These checks enforce categories, not exact prose templates.

- [ ] **Step 4: Add four manifest profiles**

Register the four selected canonical skills and the shared six required section names. Set every profile to `lab_only: true`.

- [ ] **Step 5: Run focused tests**

Run: `python -m unittest tests.test_operator_depth -v`

Expected at this intermediate point: negative fixtures pass; repository-success remains RED until runbooks and links are created.

- [ ] **Step 6: Commit**

Commit message: `feat: add deterministic operator depth validator`

---

### Task 3: Add four deep, distinct operator runbooks

**Files:**
- Create: `skills/ai-agent-security-assessment/references/operator-runbook.md`
- Create: `skills/server-side-request-boundary-analysis/references/operator-runbook.md`
- Create: `skills/authorization-boundary-analysis/references/operator-runbook.md`
- Create: `skills/cloud-iam-path-analysis/references/operator-runbook.md`
- Modify: `skills/ai-agent-security-assessment/SKILL.md`
- Modify: `skills/server-side-request-boundary-analysis/SKILL.md`
- Modify: `skills/authorization-boundary-analysis/SKILL.md`
- Modify: `skills/cloud-iam-path-analysis/SKILL.md`

**Interfaces:**
- Consumes: manifest section contract from Task 2.
- Produces: four extended methodologies discoverable from canonical skills.

- [ ] **Step 1: Write AI-agent operator runbook**

Cover principals, data/instruction transitions, RAG provenance, memory persistence, tool schemas, connectors/MCP, delegation, confirmation, egress, tenant identity, synthetic canaries, mocked tools, paired controls, evidence lineage, architectural remediation, and regression checks.

- [ ] **Step 2: Write server-side-request operator runbook**

Cover parser/normalization boundaries, resolution, dual-stack interpretation, redirects, scheme/port changes, proxies, credential/header forwarding, controlled DNS behavior, mock internal-style endpoints, paired controls, final socket-target evidence, and regression checks. Explicitly prohibit real metadata/internal-network probing.

- [ ] **Step 3: Write authorization operator runbook**

Cover subject/object/action/context matrices, role/tenant/ownership boundaries, collection and batch paths, async workers, exports, caches, delegated identities, stale sessions, state transitions, paired synthetic identities/objects, policy-vs-enforcement evidence, and regression matrices.

- [ ] **Step 4: Write cloud-IAM operator runbook**

Cover principal inventory, federation, role/service-account delegation, identity/resource policies, explicit deny and boundaries/organization controls, conditional grants, session lifetime, cross-scope trust, KMS/storage edges, policy simulation, audit evidence, synthetic/sandbox controls, and path regression.

- [ ] **Step 5: Link every canonical skill**

Add exactly one concise `## Operator depth` section to each of the four `SKILL.md` files, linking `references/operator-runbook.md` and explaining when to load it.

- [ ] **Step 6: Run focused validation**

Run:

```bash
python scripts/validate_operator_depth.py
python -m unittest tests.test_operator_depth -v
python scripts/validate_skills.py
python scripts/validate_graph.py
```

Expected: all commands succeed.

- [ ] **Step 7: Commit**

Commit message: `feat: deepen high-value operator security workflows`

---

### Task 4: Promote the contract into CI and documentation

**Files:**
- Modify: `.github/workflows/validate.yml`
- Create: `docs/operator-depth-contract.md`
- Modify: `README.md`
- Modify: `README-VN.md`
- Modify: `README-CN.md`

**Interfaces:**
- Consumes: validator and profiles from Tasks 2–3.
- Produces: merge-gated CI enforcement and public documentation of Wave 7 without changing canonical skill count.

- [ ] **Step 1: Add CI validation step**

Immediately after canonical skill validation, run:

```yaml
- name: Validate operator depth profiles
  run: python scripts/validate_operator_depth.py
```

- [ ] **Step 2: Document the contract**

Explain profile purpose, manifest fields, required sections, path containment, semantic guard categories, lab-only boundary, and why file length/payload count are intentionally not quality metrics.

- [ ] **Step 3: Update multilingual README snapshot**

Retain `83 canonical skills` and `20 packs`; add `4 operator-depth profiles` and Wave 7 language. Do not claim empirical superiority over another repository or model without benchmark evidence.

- [ ] **Step 4: Run full local-equivalent command set where available**

```bash
python scripts/validate_skills.py
python scripts/validate_operator_depth.py
python scripts/validate_graph.py
python scripts/validate_benchmarks.py
python scripts/run_benchmarks.py benchmarks/suites/portability.json
python scripts/run_benchmarks.py benchmarks/suites/core.json
python -m unittest discover -s tests -v
```

- [ ] **Step 5: Commit**

Commit message: `ci: enforce Wave 7 operator depth profiles`

---

### Task 5: PR-level verification and completion

**Files:**
- Review only; change files only if verification finds a concrete issue.

**Interfaces:**
- Consumes: complete Wave 7 branch.
- Produces: reviewed, merge-ready PR with evidence from GitHub Actions.

- [ ] **Step 1: Inspect the complete PR diff**

Verify there are no unrelated changes, duplicated payload corpora, vendor-specific forks, path escapes, or weakening of authorization/evidence language.

- [ ] **Step 2: Wait for current-head GitHub Actions results and inspect them**

Required jobs must conclude successfully, including the six-platform validation matrix, deterministic core benchmark, and agent-eval core.

- [ ] **Step 3: Run completion verification discipline**

Use `superpowers:verification-before-completion`; do not claim success from stale runs or earlier commits.

- [ ] **Step 4: Finish the development branch**

Use `superpowers:finishing-a-development-branch`. Merge only after current-head required verification is GREEN and the final diff review finds no blocking issue.
