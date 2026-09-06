---
name: fuzzing-workflow
description: "Design and evaluate coverage-guided or structured fuzzing for an authorized local target: choose a harness, corpus, oracle, instrumentation, resource budget, and triage loop. Use for parsers, libraries, protocols, state machines, native code, or input-processing components."
metadata:
  nolane-security-category: discovery
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Fuzzing Workflow

Treat fuzzing as an experiment with a measurable harness and oracle, not as “run a fuzzer and wait.”

See [the fuzzing checklist](references/fuzzing-checklist.md) for harness-quality questions and campaign metrics.

## When to use

Use when the target has a controllable input surface and many candidate input/state combinations.

## Preconditions

1. Target is local, owned, sandboxed, benchmark/CTF, or explicitly authorized for fuzzing.
2. Exact build/version and build flags are recorded.
3. A failure oracle exists: sanitizer, assertion, invariant violation, crash, differential mismatch, or protocol-state error.
4. Resource limits prevent accidental impact outside the research environment.

## Workflow

1. **Choose the smallest meaningful harness.** Reach the target parser/logic without unrelated startup, network, UI, or persistence costs.
2. **Define one campaign objective.** Example: maximize parser edge coverage or explore a specific state transition.
3. **Choose instrumentation/oracle.** Sanitizers and explicit invariants are stronger than process exit alone.
4. **Seed intentionally.** Include minimal valid samples plus boundary-oriented structures; avoid a giant redundant corpus.
5. **Measure baseline.** Record executions/sec, stable coverage, startup cost, and known-control behavior.
6. **Run a bounded campaign.** Track coverage growth, unique failures, and corpus growth.
7. **Improve the harness before adding compute** when coverage stalls because checksums, global initialization, blocking I/O, or nondeterminism dominate.
8. **Deduplicate and minimize** every unique failure before analysis.
9. Route minimized failures to `crash-triage-and-minimization`.
10. Preserve corpus inputs that cover distinct states for regression.

## Evidence contract

A fuzzing result is **observed**, not automatically validated. Preserve:

- target commit/version and build flags;
- harness source/config;
- fuzzer/tool version if relevant;
- minimized reproducer;
- oracle output;
- deterministic reproduction rate;
- control result.

Coverage increase alone is not a vulnerability.

## Stop conditions

Stop or redesign when:

- authorization/resource limits are uncertain;
- the harness mostly fuzzes setup code instead of the intended surface;
- failures cannot be reproduced outside the fuzzing process;
- coverage is unstable due to nondeterminism;
- additional runtime yields no new states and no concrete hypothesis suggests a mutation/harness change.

## Output

Report:

```text
target + version:
harness boundary:
oracle:
seed/corpus strategy:
baseline metrics:
campaign budget:
coverage/state result:
unique minimized failures:
next action:
```
