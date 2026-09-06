---
name: static-dynamic-correlation
description: "Correlate source/binary dataflow and state reasoning with runtime traces, sanitizer stacks, coverage, logs, and minimized triggers to establish a causal path without treating either static or dynamic evidence as sufficient alone."
metadata:
  nolane-security-category: orchestration
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Static Dynamic Correlation

Perform dynamic or intrusive validation only in an authorized, owned lab or equivalent explicitly scoped test environment.

## When to use

Use when static review identifies a plausible source→sink path or dynamic evidence identifies a failure but the causal path/root state remains uncertain.

## Preconditions

1. Use pinned source/binary revision matching the runtime target.
2. Have at least one static hypothesis or dynamic observation.
3. Perform dynamic work only in an authorized/owned lab.

## Workflow

1. Normalize symbol/build identity so source, binary, stack traces and coverage refer to the same revision/configuration.
2. From dynamic evidence, identify the earliest trustworthy target frame/state and trace backwards to attacker/user-controlled input or lifecycle event.
3. From static evidence, enumerate required predicates/aliases/state transitions and mark which were actually observed at runtime.
4. Instrument/log only the smallest ambiguous edges needed to discriminate paths; avoid broad noisy tracing.
5. Use a minimized trigger and negative control to test whether removing the suspected edge/predicate removes the same runtime symptom.
6. Record static-only edges, dynamic-only surprises, and the final correlated path separately.
7. Route the correlated invariant violation to the appropriate semantic root-cause skill and evidence validation.

## Evidence contract

Evidence must map the same build’s static path/invariant to concrete runtime frames/state/input, including any unobserved assumptions. Correlation increases causal confidence but does not by itself establish impact.

## Stop conditions

Stop if build/symbol identity is mismatched, instrumentation materially changes behavior without a control, or required runtime tracing would exceed authorization/safety bounds.

## Output

```text
build identity:
static hypothesis/path:
runtime trace/coverage:
matched edges:
unobserved assumptions:
discriminating instrumentation:
correlated invariant:
next root-cause skill:
```
