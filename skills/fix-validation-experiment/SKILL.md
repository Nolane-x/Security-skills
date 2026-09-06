---
name: fix-validation-experiment
description: "Design and execute a controlled fix-validation experiment that reruns the exact original reproducer and controls on a pinned fixed revision, tests invariant-level closure, and checks nearby variants/regressions before declaring remediation complete."
metadata:
  nolane-security-category: orchestration
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Fix Validation Experiment

Perform dynamic or intrusive validation only in an authorized, owned lab or equivalent explicitly scoped test environment.

## When to use

Use when a candidate patch/fixed release exists for a validated security case and the goal is to prove the original cause is closed without breaking controls.

## Preconditions

1. The original case is validated with fixture digest, controls, root cause and bounded consequence.
2. The fixed revision/build is pinned and produced under authorized conditions.
3. Do not broaden testing into unrelated production systems.

## Workflow

1. Recreate the original environment except for the explicitly changed target revision/build.
2. Run the exact original reproducer/fixture and confirm the vulnerable oracle no longer appears.
3. Run original positive controls to prove the target path/harness still functions and negative controls to ensure the test remains discriminating.
4. Inspect the patch/invariant and test nearby boundary values/state transitions that could bypass a narrow symptom fix.
5. Run relevant regression/variant matrix across vulnerable, fixed, and optionally neighboring versions/configurations.
6. Record any behavioral changes unrelated to the security fix as potential regressions rather than hiding them.
7. Promote to regression-verified only when original non-reproduction and passing controls are both evidenced.

## Evidence contract

Regression verification needs fixed revision identity, exact original fixture identity, non-reproduction of the vulnerability oracle, passing controls, and evidence the intended invariant—not just one symptom—was restored.

## Stop conditions

Stop if the fixed build differs in uncontrolled ways, the original fixture cannot be reproduced, controls fail, or patch validation would require unsafe production testing.

## Output

```text
vulnerable revision:
fixed revision:
original fixture digest:
original oracle result:
fixed oracle result:
control results:
variant/regression matrix:
invariant closure:
final state:
```
