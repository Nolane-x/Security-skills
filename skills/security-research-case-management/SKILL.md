---
name: security-research-case-management
description: "Maintain a security research case as an explicit claim/evidence state machine with authorization scope, pinned environment, observations, controls, reproducer identity, uncertainty, and fix-validation status. Use to prevent evidence drift across long agent sessions."
metadata:
  nolane-security-category: orchestration
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Security Research Case Management

Perform dynamic or intrusive validation only in an authorized, owned lab or equivalent explicitly scoped test environment.

## When to use

Use at the beginning of any multi-step security investigation, when handing work between agents, or whenever a finding has accumulated observations from multiple tools/runs.

## Preconditions

1. The target is authorized, owned, local, sandboxed, CTF, or explicitly scoped.
2. Assign a stable case ID and one falsifiable primary claim.
3. Use synthetic/non-sensitive identifiers in shared evidence records.

## Workflow

1. Initialize scope, domains, goal, evidence state, claim, and known uncertainties before choosing tools.
2. Pin target revision/configuration as soon as behavior is observed; do not let “latest” silently replace the tested build.
3. Store observations as facts with provenance rather than rewriting them into stronger conclusions.
4. Keep positive/negative controls separate from the reproducer and preserve fixture identity/digest.
5. Advance evidence state only when the next state’s contract is satisfied; never skip hypothesis → observed → validated → regression-verified.
6. When the claim changes materially, create a related case or explicitly revise the claim instead of mixing hypotheses.
7. Before handoff, record unresolved alternatives, missing controls, and the next discriminating experiment.

## Evidence contract

A well-managed case can answer: what is claimed, what was actually observed, on which exact environment, under what authorization, which controls discriminate alternatives, and what remains uncertain. Case metadata never substitutes for vulnerability evidence.

## Stop conditions

Stop state promotion when required evidence is missing, the tested environment has drifted, the claim changed without being re-scoped, or authorization no longer covers the next experiment.

## Output

```text
case ID/title:
scope:
domains/goal/state:
claim:
environment:
observations:
controls:
reproducer identity:
root cause/consequence:
uncertainties:
next evidence gap:
```
