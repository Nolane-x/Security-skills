# Operator Depth Contract

Wave 7 adds a deterministic contract for deep operator guidance without changing the canonical skill graph or turning Security Skills into a payload collection.

## Purpose

Canonical `SKILL.md` files remain portable, concise entry points. Selected high-value skills may expose a deeper `references/operator-runbook.md` for authorized investigations that need a larger hypothesis space, stronger experimental controls, richer evidence capture, and explicit remediation regression.

The repository intentionally does **not** use line count, byte count, payload count, or tool-name count as a quality metric. Operator depth is defined by reviewable structure and evidence discipline.

## Canonical registry

`operator-depth/profiles.json` is the source of truth for operator-depth profiles.

Each profile contains:

```json
{
  "skill": "canonical-skill-name",
  "runbook": "references/operator-runbook.md",
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

`runbook` is relative to `skills/<skill>/`. Absolute paths and paths that escape the canonical skill directory are rejected.

## Required runbook structure

Every registered runbook must contain these exact second-level sections:

1. `Attack surface` — enumerate the concrete principals, resources, trust transitions, policy layers, parsers, or capability boundaries relevant to the domain.
2. `Hypothesis matrix` — turn broad vulnerability classes into falsifiable boundary hypotheses with safe proof signals.
3. `Controlled validation` — define a bounded, reproducible experiment using owned/sandboxed/synthetic resources.
4. `False-positive controls` — require paired allowed/denied or equivalent controls that distinguish a real boundary failure from harness, policy, or configuration artifacts.
5. `Evidence capture` — specify the observable evidence needed to promote a claim through the repository evidence state machine.
6. `Remediation checks` — test the architectural fix and neighboring intended behavior, not only the original trigger.

Every runbook must also contain explicit authorization/lab language plus evidence and control discipline.

## Validation

Run:

```bash
python scripts/validate_operator_depth.py
```

The validator uses only the Python standard library. It fails closed for malformed registries, duplicate profiles, missing canonical skills, unsafe paths, missing runbooks, missing canonical links, missing required sections, disabled lab-only policy, or missing evidence/control/authorization language.

Diagnostics are deduplicated and sorted to remain deterministic across supported CI environments.

## Security boundary

Operator-depth runbooks are for local, owned, sandboxed, benchmark/CTF, or explicitly authorized targets. They use synthetic canaries, test identities, mock services, policy simulators, inert action sinks, and bounded test resources rather than real secrets, third-party data, uncontrolled scanning, destructive operations, or production-impacting actions.

A deeper methodology does not weaken the evidence standard. Scanner output, a model assertion, a policy statement containing `allow`, a single surprising response, or theoretical reachability is not sufficient by itself for a validated finding.

## Evidence states

Operator-depth profiles inherit the repository evidence model:

```text
hypothesis
    ↓
observed
    ↓
validated
    ↓
regression-verified
```

A `validated` case must demonstrate a concrete prohibited boundary crossing and bounded consequence with suitable controls. `regression-verified` additionally proves that the remediation blocks the failing path while expected neighboring behavior still succeeds.

## Wave 7 profiles

Wave 7 registers four profiles:

- `ai-agent-security-assessment`
- `authorization-boundary-analysis`
- `cloud-iam-path-analysis`
- `server-side-request-boundary-analysis`

These were chosen because each benefits significantly from deeper system-level reasoning while remaining compatible with safe synthetic validation.

## Adding a future profile

1. Deepen an existing canonical skill rather than creating a near-duplicate skill.
2. Add `references/operator-runbook.md` under that skill.
3. Link the runbook once from `SKILL.md` under an `## Operator depth` section.
4. Register the profile in `operator-depth/profiles.json` with `lab_only: true`.
5. Include all required runbook sections and domain-specific paired controls.
6. Run the operator-depth validator and full repository test/benchmark stack.
7. Review the diff for copied payload corpora, vendor lock-in, duplicated canonical prose, and weakened authorization/evidence language.

Operator depth is intentionally selective. A skill should receive a profile only when extended methodology materially improves research quality and can be kept deterministic, evidence-first, and safely bounded.
