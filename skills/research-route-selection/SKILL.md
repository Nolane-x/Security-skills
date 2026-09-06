---
name: research-route-selection
description: "Select the smallest next Security Skills route from case domains, evidence state, research goal, prerequisites, failed hypotheses, and available observability. Use to avoid firing every tool or domain skill at every target."
metadata:
  nolane-security-category: orchestration
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Research Route Selection

Perform dynamic or intrusive validation only in an authorized, owned lab or equivalent explicitly scoped test environment.

## When to use

Use when starting a case, after a hypothesis is rejected, after evidence state advances, or when deciding between fuzzing/static/symbolic/binary/domain-specific validation paths.

## Preconditions

1. The case has explicit domains, goal and current evidence state.
2. Authorization scope is already established.
3. Treat router output as advisory; human/agent evidence can justify deviating.

## Workflow

1. Start with authorization/scope and retain all true prerequisites for any selected skill.
2. Match target-specific domains before generic primitives; avoid selecting a platform/domain skill merely because it shares “parser”, “memory-safety”, or “routing”.
3. Prefer skills designed for the current or next evidence stage rather than jumping directly to regression/impact.
4. Use the research goal to add anchors: discovery, root-cause, validation, remediation, or reporting.
5. Close prerequisite dependencies transitively and order by prerequisite DAG plus evidence stage.
6. Use failed experiments/negative evidence to remove hypotheses rather than adding ever more unrelated skills.
7. Re-route whenever the primary claim, domain, or evidence state changes materially.

## Evidence contract

A route is justified when every selected non-prerequisite skill has an explicit domain/goal/state reason and prerequisites appear before dependents. Routing itself is not security evidence.

## Stop conditions

Stop and request more case context when all high-scoring routes depend on unknown target type, missing source/binary access, or unestablished authorization.

## Output

```text
case state/goal/domains:
selected packs:
ordered skills:
prerequisite closure:
selection reasons:
excluded/conflicting domains:
next re-route trigger:
```
