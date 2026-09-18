# Wave 10 Profile #27 — Sandbox Boundary Depth Implementation Plan

> **For agentic workers:** execute this plan task-by-task and preserve the test-first lineage.

**Goal:** Promote `sandbox-boundary-analysis` into the twenty-seventh CI-enforced operator-depth profile with causal SB0–SB5 semantics and deterministic benign review cases.

**Architecture:** Preserve the portable canonical skill and existing graph identity. Add one deep runbook and one machine-readable review-case matrix, register both under operator-depth schema v2, freeze all new semantics in a dedicated test before production changes, and publish public docs only after behavioral GREEN.

**Base authority:** `main@b2b6e163ae9690925bbe7db497922ebb6b748f40`

**Design:** `docs/superpowers/specs/2026-09-18-wave10-sandbox-boundary-depth-design.md`

## Global constraints

- Preserve 83 canonical skills and 20 packs.
- Preserve all existing 26 operator-depth profiles.
- Keep `operator-depth/profiles.json` schema version 2.
- Do not change `skill.meta.json`, graph edges, packs, routing domains, benchmark authority, agent-eval authority, superiority-court authority, or workflow semantics.
- Commit the #27 dedicated test before SKILL deepening, runbook, review cases, or registry promotion.
- Do not weaken the #27 test after intentional RED.
- Use only local/owned/sandboxed/explicitly authorized synthetic/mock/inert/read-only/bounded-reversible validation.
- After behavioral GREEN, only `README.md` and `docs/operator-depth-contract.md` may change before exact-head verification.

---

## Task 1 — Freeze #27 semantics with a dedicated RED test

**Create:** `tests/test_sandbox_boundary_depth.py`

The canonical SKILL test must require:

- `## Causal sandbox-boundary model`
- `## Sandboxed principal, policy, and lifecycle generations`
- `## Broker request and caller-session binding`
- `## Resource, namespace, and canonical identity binding`
- `## Inherited and delegated capability provenance`
- `## Shared state and privileged-service consumer binding`
- `## Final capability and bounded effect binding`
- `## Sandbox-boundary evidence ladder`
- `## Counterfactual boundary controls`
- `## Alternative explanations`
- `## Evidence ceiling`

Freeze these distinctions:

- broker reachability != broker authority;
- inherited handle/fd != ambient host authority;
- mapped shared memory != authorized privileged use;
- namespace alias != policy bypass;
- sandbox policy present != policy applied to decisive operation;
- restricted token/seccomp profile != proof of complete confinement;
- sandboxed-process crash != sandbox escape;
- privileged-service crash != sandbox escape;
- privileged-service code execution != arbitrary host compromise;
- broadened broker capability != arbitrary code execution;
- process outside sandbox != privileged process;
- policy mismatch != complete escape;
- stale session/request identity != current authority.

The runbook test must require the six common headings plus:

- Principal and policy-generation trace
- Broker request and caller-session trace
- Resource and namespace-resolution trace
- Inherited/delegated capability trace
- Shared-state and privileged-consumer trace
- Lifecycle revocation and restart trace
- Final capability and bounded-effect trace
- Counterfactual boundary controls
- Alternative explanations
- Evidence promotion and ceiling

The review matrix must contain at least:

- `stale-session-broker-authorization`
- `namespace-alias-resolved-object-mismatch`
- `inherited-capability-rights-drift`
- `shared-object-generation-confusion`

Every scenario must provide substantive strings for:

`hypothesis`, `safe_oracle`, `positive_control`, `negative_control`, `stop_condition`, `remediation_oracle`, `sandbox_principal_policy_generation`, `broker_request_caller_binding`, `resource_namespace_resolution`, `inherited_delegated_capability`, `shared_state_privileged_consumer`, `lifecycle_revocation_state`, `final_consumer_identity`, `effective_crossed_capability`, `bounded_result`, `receipt_result_binding`, `counterfactual_control`, `alternative_explanation`, `evidence_level`, and `evidence_ceiling`.

Registry assertions: schema version 2, exactly 27 profiles, exactly one sandbox-boundary entry, standard runbook/matrix paths, `lab_only: true`, and the six common required sections.

Open a Draft PR at the exact test-first SHA. Require intentional RED before any production depth implementation.

---

## Task 2 — Deepen the canonical skill

**Modify:** `skills/sandbox-boundary-analysis/SKILL.md`

Preserve frontmatter and existing portable workflow. Add the causal tuple:

`sandbox principal + principal/session generation + sandbox policy identity/generation + request/operation generation + broker/service identity + caller-to-request binding + requested resource identity + canonical/resolved resource identity + inherited/delegated capability provenance + namespace/object generation + shared-state generation + privileged consumer + policy decision + effective crossed capability + bounded result + receipt/result`

Add SB0–SB5, counterfactual boundary controls, alternative explanations, lifecycle/revocation reasoning, and explicit evidence ceilings.

Do not absorb neighboring canonicalization, confused-deputy, memory-lifetime, browser-process, or exploitability ownership.

---

## Task 3 — Add the operator runbook

**Create:** `skills/sandbox-boundary-analysis/references/operator-runbook.md`

Include exactly the six common headings:

- Attack surface
- Hypothesis matrix
- Controlled validation
- False-positive controls
- Evidence capture
- Remediation checks

Also include every domain-specific heading frozen in Task 1.

Use synthetic principals/resources, mock or loopback brokers, fake object tables, inert/read-only privileged consumers, controlled namespace views, generation-tagged sessions, and bounded reversible owner-controlled markers.

---

## Task 4 — Add deterministic benign review cases

**Create:** `skills/sandbox-boundary-analysis/references/operator-review-cases.json`

Use version 1 with at least the four required IDs. Every required field must contain at least 40 non-whitespace characters.

Each `safe_oracle` must explicitly contain a safe mechanism such as `synthetic`, `mock`, `inert`, `read-only`, or `controlled`.

Each `stop_condition` must explicitly say `stop`, `abort`, or `do not proceed`.

Evidence fields must use SB0–SB5.

---

## Task 5 — Register profile #27

**Modify:** `operator-depth/profiles.json`

Add exactly one sorted entry for `sandbox-boundary-analysis` with:

- runbook: `references/operator-runbook.md`
- scenario_matrix: `references/operator-review-cases.json`
- lab_only: `true`
- the standard six required runbook sections.

Target registry count: 27.

---

## Task 6 — Repair only a proven stale #26 global count assertion

**Potentially modify:** `tests/test_concurrency_race_depth.py`

Do not preemptively edit #26. If behavioral CI shows that the valid 27-profile registry fails only because #26 asserts exactly 26 global entries, change only that assertion to `>= 26`. Preserve all #26 profile-specific assertions.

---

## Task 7 — Require behavioral 9/9 GREEN

Behavioral authority is the first head where SKILL, runbook, cases, registry, and any strictly necessary previous-profile extensibility repair are complete.

Require six OS/Python validation jobs plus `benchmark-core`, `agent-eval-core`, and `superiority-court-core` all GREEN before public documentation.

---

## Task 8 — Publish public docs

**Modify only after behavioral GREEN:**

- `README.md`
- `docs/operator-depth-contract.md`

Update current profile count from 26 to 27, identify `sandbox-boundary-analysis` as the twenty-seventh profile, summarize its causal bindings, and publish SB0–SB5.

---

## Task 9 — Exact-head verification, guarded merge, and closure

1. Require exact-head 9/9 GREEN.
2. Confirm `main` still equals the expected base.
3. Confirm final reviewed head and changed-path scope.
4. Require mergeable state.
5. Guarded merge using exact expected head SHA.
6. Verify parent 1 equals pre-merge `main` and parent 2 equals final reviewed head.
7. Require post-merge 9/9 GREEN on exact merge SHA.
8. Read merge-tree registry, README, and operator-depth contract.
9. Record closure provenance on the PR.

## Success criterion

Profile #27 is complete only when the merge tree contains exactly 27 profiles, exactly one valid `sandbox-boundary-analysis` entry, SB0–SB5 is published, exact-head and post-merge CI are fully GREEN, and no unauthorized scope expansion occurred.