---
name: controlled-security-experiment-design
description: "Design small falsifiable security experiments with one changed variable, explicit hypothesis, positive/negative controls, bounded resources, deterministic observations, and safe rollback. Use before dynamic validation to separate causes from coincidence."
metadata:
  nolane-security-category: orchestration
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Controlled Security Experiment Design

Perform dynamic or intrusive validation only in an authorized, owned lab or equivalent explicitly scoped test environment.

## When to use

Use when several explanations could account for a crash, policy difference, route, authorization result, parser behavior, race, or security boundary observation.

## Preconditions

1. The research case and authorization scope are explicit.
2. Identify the exact hypothesis the experiment is intended to falsify.
3. Prefer a local/owned lab and synthetic data/resources.

## Workflow

1. Write the hypothesis and its strongest plausible alternative explanation before running anything.
2. Choose one independent variable to change; freeze target revision, harness, environment and observation method where possible.
3. Define a positive control that proves the path/harness is functioning and a negative control that removes the suspected cause.
4. Define a deterministic observable: sanitizer site, return code, state diff, audit event, synthetic marker, assertion, or bounded timing distribution.
5. Set resource/time/retry bounds and rollback/reset steps before execution.
6. Run controls and experiment in an order that reduces state contamination; reset between trials when stateful.
7. Interpret the result against both the hypothesis and alternative explanation, recording inconclusive outcomes rather than forcing a binary answer.

## Evidence contract

The experiment record must name the independent variable, frozen variables, controls, oracle, trial/reset model, observed outcome, and which explanations were strengthened or weakened.

## Stop conditions

Stop if the experiment cannot isolate a variable, lacks a safe oracle/rollback, risks non-lab resources, or repeated trials show uncontrolled environment drift.

## Output

```text
hypothesis:
alternative explanation:
independent variable:
frozen variables:
positive control:
negative control:
oracle:
bounds/reset:
result:
interpretation:
```
