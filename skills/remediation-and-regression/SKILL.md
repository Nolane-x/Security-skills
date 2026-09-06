---
name: remediation-and-regression
description: "Design a minimal security fix that restores the violated invariant, then prove it with regression tests and controls. Use after a vulnerability root cause is validated or when reviewing a proposed security patch."
metadata:
  nolane-security-category: remediation
  nolane-security-version: "1"
  nolane-security-authorization: conditional
---
# Remediation and Regression

Fix the invariant at the correct trust boundary rather than merely blocking one reproducer.

## When to use

Use after root cause is understood, or when evaluating a candidate patch for a security bug.

## Preconditions

- Have a concrete violated invariant and affected path.
- Preserve the original reproducer and negative/control cases.
- Run dynamic regression only in local/owned/sandboxed/authorized environments.

## Workflow

1. State the invariant the fix must enforce.
2. Find the earliest reliable boundary where the invariant can be checked or represented correctly.
3. Prefer structural fixes:
   - correct ownership/lifetime;
   - checked arithmetic/ranges;
   - canonical identity;
   - explicit authorization;
   - state-machine validation;
   - safe API/type.
4. Avoid payload-specific string blocks or one-input special cases.
5. Write a regression test from the minimized reproducer.
6. Add neighboring boundary/control cases.
7. Verify:
   - reproducer fails safely or no longer violates the property;
   - legitimate control behavior still works;
   - sanitizer/assertion evidence is clean where applicable.
8. Search sibling paths for the same invariant before declaring complete.
9. Record compatibility/performance/security tradeoffs.

## Evidence contract

A fix is **regression-verified** only when the same evidence that demonstrates the vulnerable behavior no longer demonstrates it on the fixed build, while controls prove the relevant functionality remains exercised.

## Stop conditions

Do not declare fixed when:

- only the original literal payload is blocked;
- the regression no longer reaches the vulnerable path;
- tests pass because the feature is disabled;
- the root cause remains reachable through a sibling path.

## Output

Return the repaired invariant, patch strategy, regression cases, control cases, before/after evidence, residual risk, and variant-search result.
