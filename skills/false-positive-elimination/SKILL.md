---
name: false-positive-elimination
description: "Systematically eliminate harness artifacts, configuration effects, stale state, benign parser rejection, duplicate crashes, instrumentation issues, and unrelated failures before promoting a security finding. Use whenever automated discovery produces a candidate."
metadata:
  nolane-security-category: orchestration
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# False Positive Elimination

Perform dynamic or intrusive validation only in an authorized, owned lab or equivalent explicitly scoped test environment.

## When to use

Use for scanner findings, LLM hypotheses, fuzz crashes, sanitizer reports, differential mismatches, auth anomalies, or any candidate that could have a non-security explanation.

## Preconditions

1. The candidate is reproduced only in an authorized/owned lab.
2. Preserve the original observation and environment before modifying the harness.
3. List at least one benign alternative explanation.

## Workflow

1. Re-run from a clean state and distinguish deterministic, probabilistic and one-off behavior.
2. Minimize the trigger while preserving the same oracle/root symptom; reject candidates that disappear only because unrelated setup was removed.
3. Run a known-good positive control to prove the harness/instrumentation still exercises the target.
4. Run a negative control that removes the suspected cause while keeping the path otherwise similar.
5. Compare uninstrumented/debug/release or nearby versions where safe to detect sanitizer/debug-only artifacts without dismissing genuine UB.
6. Check logs/stack/state for duplicate known issues and for failures originating in harness/test scaffolding rather than target code.
7. Classify outcome as rejected, inconclusive, observed candidate, or ready for causal validation with explicit reasons.

## Evidence contract

Promotion requires reproducibility plus controls that discriminate the candidate from at least the leading benign alternative. Tool confidence scores and LLM agreement are not controls.

## Stop conditions

Stop promotion when the oracle changes under minimization, controls fail, environment cannot be reset, or evidence points to the harness rather than target behavior.

## Output

```text
candidate:
reproduction rate:
minimized trigger:
positive control:
negative control:
alternative explanations:
duplicate/harness check:
classification:
remaining uncertainty:
```
