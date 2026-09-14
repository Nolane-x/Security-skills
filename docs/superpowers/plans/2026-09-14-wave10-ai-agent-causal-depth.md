# Wave 10 AI Agent Causal Depth Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deepen `ai-agent-security-assessment` into a falsifiable causal security-reasoning contract covering provenance, authority, policy/confirmation, execution/effect, persistence, delegation, counterfactual controls, and explicit evidence ceilings.

**Architecture:** Preserve the existing 83-skill graph and Wave 8 operator-depth architecture. Add one dedicated TDD contract, then deepen the existing canonical `SKILL.md`, its operator runbook, and its three registered scenarios. No routing, pack, graph, benchmark-oracle, or threshold changes are required.

**Tech Stack:** Markdown Agent Skills, JSON scenario matrices, Python `unittest`, existing zero-dependency repository validators and GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-09-14-wave10-ai-agent-causal-depth-design.md`

## Global Constraints

- Preserve the existing canonical skill name, frontmatter format, `skill.meta.json`, pack membership, routing domains, graph edges, and benchmark thresholds.
- Keep all validation synthetic, inert, mocked, read-only, owned, sandboxed, benchmark/CTF, or explicitly authorized.
- Never request or preserve hidden chain-of-thought; observable states, policy decisions, tool calls, and effects are sufficient evidence.
- No credential theft, persistence deployment, destructive actions, malware, evasion, live-target exploitation, or deployable payload corpus.
- Depth is measured by causal methodology plus falsifiable scenario contracts, not line count.

---

### Task 1: Freeze the Wave 10 AI-agent depth contract in a failing test

**Files:**
- Create: `tests/test_ai_agent_security_depth.py`

**Interfaces:**
- Consumes: existing `skills/ai-agent-security-assessment/SKILL.md`, `references/operator-runbook.md`, and `references/operator-scenarios.json`.
- Produces: a repository-level executable contract for Wave 10 AI-agent depth.

- [ ] **Step 1: Add the failing unit test**

Create `tests/test_ai_agent_security_depth.py` with tests that require these canonical skill sections: `## Causal security state model`, `## Authority-capability model`, `## Provenance continuity`, `## Evidence ladder`, `## Evidence ceiling`, and `## Counterfactual discipline`; these runbook sections: `## Causal decision trace`, `## Authority-capability matrix`, `## Provenance continuity`, `## Persistence and delegation`, `## Counterfactual boundary proof`, `## Evidence ceiling`, and `## Remediation proof`; and these scenario fields on every scenario: `provenance_trace`, `authority_capability_profile`, `decision_effect_trace`, `persistence_trace`, `delegation_trace`, `counterfactual_control`, `alternative_explanation`, `evidence_ceiling`, `neighbor_regression`.

Require each scenario-specific Wave 10 field to be a string of at least 50 non-whitespace characters so empty/formulaic placeholders cannot satisfy the contract.

- [ ] **Step 2: Verify RED**

Run:

```bash
python -m unittest tests.test_ai_agent_security_depth -v
```

Expected: FAIL because the current Wave 8-style artifacts do not contain the required Wave 10 sections or scenario fields. A syntax/import error is not an acceptable RED state.

- [ ] **Step 3: Commit the RED contract**

```bash
git add tests/test_ai_agent_security_depth.py
git commit -m "test: define AI agent causal depth contract"
```

---

### Task 2: Deepen the canonical AI-agent skill

**Files:**
- Modify: `skills/ai-agent-security-assessment/SKILL.md`
- Test: `tests/test_ai_agent_security_depth.py`

**Interfaces:**
- Consumes: the causal model and evidence ladder defined in the approved spec.
- Produces: a portable entry-point skill that forces bounded transition-by-transition reasoning before impact promotion.

- [ ] **Step 1: Add the causal state model**

Add `## Causal security state model` with the observable chain:

```text
source -> provenance -> interpretation -> proposal -> authority -> policy -> confirmation -> execution -> effect -> persistence
```

State explicitly that later stages cannot be inferred from earlier ones.

- [ ] **Step 2: Add authority-capability and provenance contracts**

Add `## Authority-capability model` separating initiating-principal authority, model/orchestrator capability, tool capability, credential authority, delegated authority, effective execution authority, and compound authority. Add `## Provenance continuity` covering retrieval, summarization, memory, tool results, connectors, sub-agent handoff, and context compression.

- [ ] **Step 3: Add evidence ladder and ceiling**

Add `## Evidence ladder` with `A0` through `A5` exactly as defined by the spec, and `## Evidence ceiling` rules that prohibit promotion from model output to tool execution, from execution to prohibited effect, or from transient effect to persistence without direct evidence.

- [ ] **Step 4: Add counterfactual discipline and structured output**

Add `## Counterfactual discipline` and expand the output schema to record source/provenance, authority profile, normalized proposal, policy decision, confirmation tuple, execution result, bounded effect, persistence/delegation trace, alternative explanations, evidence level, evidence ceiling, and remediation invariant.

- [ ] **Step 5: Run focused test**

```bash
python -m unittest tests.test_ai_agent_security_depth -v
```

Expected: scenario/runbook assertions may still fail, but the canonical-skill assertions must pass.

- [ ] **Step 6: Commit**

```bash
git add skills/ai-agent-security-assessment/SKILL.md
git commit -m "docs: deepen AI agent causal security reasoning"
```

---

### Task 3: Deepen operator methodology and scenario evidence

**Files:**
- Modify: `skills/ai-agent-security-assessment/references/operator-runbook.md`
- Modify: `skills/ai-agent-security-assessment/references/operator-scenarios.json`
- Test: `tests/test_ai_agent_security_depth.py`

**Interfaces:**
- Consumes: the canonical causal-state and evidence-ceiling semantics from Task 2.
- Produces: operational methodology and deterministic scenario records that make the semantics falsifiable.

- [ ] **Step 1: Add causal decision trace and authority matrix**

Add `## Causal decision trace` requiring observable records for each transition from source through effect/persistence. Add `## Authority-capability matrix` with principal, capability, credential/scope, policy boundary, confirmation requirement, and effective authority columns.

- [ ] **Step 2: Add provenance continuity**

Add `## Provenance continuity` requiring source/trust-label continuity across retrieval, transformation, summarization, memory, tool results, connectors, delegation, and compression. Require explicit downgrade when provenance is lost or ambiguous.

- [ ] **Step 3: Add persistence/delegation reasoning**

Add `## Persistence and delegation` separating transient influence from persistent write/read/later effect and requiring delegation edges to record initiating principal, delegated task, authority before/after, credential, re-authorization point, and consequence.

- [ ] **Step 4: Add counterfactual boundary proof, evidence ceiling, and remediation proof**

Add `## Counterfactual boundary proof`, `## Evidence ceiling`, and `## Remediation proof`. Require one-variable-at-a-time causal controls and replay of the original failing fixture plus neighboring allowed and denied controls after remediation.

- [ ] **Step 5: Deepen all three scenario records**

For each existing scenario, preserve the Wave 8 fields and add substantive strings for all nine Wave 10 fields. For non-applicable persistence or delegation dimensions, explicitly state why they are not part of the current scenario and what observation would make them relevant.

- [ ] **Step 6: Verify GREEN for the dedicated contract**

```bash
python -m unittest tests.test_ai_agent_security_depth -v
```

Expected: PASS.

- [ ] **Step 7: Verify operator-depth compatibility**

```bash
python scripts/validate_operator_depth.py
python -m unittest tests.test_operator_depth -v
```

Expected: PASS with the existing profile registry unchanged.

- [ ] **Step 8: Commit**

```bash
git add skills/ai-agent-security-assessment/references/operator-runbook.md skills/ai-agent-security-assessment/references/operator-scenarios.json
git commit -m "docs: deepen AI agent operator evidence model"
```

---

### Task 4: Repository-wide verification and PR gate

**Files:**
- No production-file changes unless a verification failure identifies a real compatibility defect.

**Interfaces:**
- Consumes: completed Wave 10 Phase 8 artifacts.
- Produces: exact-head evidence that the change preserves repository contracts.

- [ ] **Step 1: Run skill/graph/build validators**

```bash
python scripts/validate_skills.py
python scripts/validate_graph.py
python scripts/build_catalog.py
python scripts/build_graph.py
python scripts/build_catalog.py --check
python scripts/build_graph.py --check
python scripts/validate_case.py examples/research-case.example.json
python scripts/route_skills.py examples/research-case.example.json --limit 12
python scripts/validate_operator_depth.py
```

- [ ] **Step 2: Run benchmark and agent-eval gates**

```bash
python scripts/validate_benchmarks.py
python scripts/run_benchmarks.py benchmarks/suites/portability.json
python scripts/run_benchmarks.py benchmarks/suites/core.json
python scripts/prepare_agent_tasks.py benchmarks/suites/portability.json --out /tmp/agent-tasks
python scripts/prepare_replay_runs.py benchmarks/suites/portability.json --profile reference --out /tmp/agent-runs
python scripts/validate_agent_runs.py /tmp/agent-runs
python scripts/evaluate_agent_runs.py benchmarks/suites/portability.json /tmp/agent-runs
```

- [ ] **Step 3: Run full tests**

```bash
python -m unittest discover -s tests -v
```

Expected: zero failures.

- [ ] **Step 4: Review diff invariants**

Confirm the diff does not alter `skill.meta.json`, `packs/`, routing domains, benchmark thresholds/oracles, or the canonical skill count, and contains no live target, credential, destructive action, persistence deployment, malware/evasion, or deployable exploit payload.

- [ ] **Step 5: Open a draft PR and require CI green**

PR title: `Wave 10: deepen AI agent causal security reasoning`.

The PR body must state that Wave 10 Phase 8 preserves the 83-skill/20-pack architecture and deepens the last Wave 8 operator-depth profile with a causal evidence model.

- [ ] **Step 6: Merge only after exact-head CI is green**

After merge, independently verify `main` CI before declaring Phase 8 complete.
