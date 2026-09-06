---
name: crash-triage-and-minimization
description: "Triage an authorized crash or sanitizer finding into reproducibility, root-cause class, minimized input, duplicate family, and security-relevant primitive. Use after fuzzing, testing, sanitizer failures, debugger faults, or flaky native crashes."
metadata:
  nolane-security-category: verification
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Crash Triage and Minimization

A crash is evidence of a failure, not proof of exploitability or even a unique bug.

## When to use

Use when a local/authorized target produces a crash, sanitizer report, assertion, hang, or abnormal termination.

## Preconditions

- Keep the original artifact immutable.
- Record target version/build and environment.
- Reproduction is performed only on a local, owned, sandboxed, CTF, benchmark, or explicitly authorized target.
- Have debugger/sanitizer output when available.

## Workflow

1. Reproduce the failure multiple times from a clean process.
2. Separate deterministic failures from flaky/environment-sensitive ones.
3. Capture the first meaningful fault, sanitizer origin, and relevant stack rather than only the final abort.
4. Minimize the input while preserving the same root-cause signature.
5. Deduplicate by root cause, not merely instruction pointer.
6. Identify the violated property:
   - bounds;
   - lifetime/ownership;
   - integer size/offset;
   - initialization;
   - concurrency/state;
   - assertion/invariant;
   - resource exhaustion.
7. Determine attacker influence over corrupted/read state without assuming control.
8. Build a benign control that exercises the same path without violating the invariant.
9. Route a concrete causal claim to `evidence-driven-vulnerability-validation`.

## Evidence contract

Preserve:

- minimized input;
- exact command/harness invocation in the lab;
- sanitizer/debugger signature;
- deterministic reproduction rate;
- root-cause location;
- relevant attacker-controlled fields;
- negative/control input;
- duplicate-family key.

Use **observed** until root cause and security consequence are established.

## Stop conditions

Stop escalation when:

- the crash disappears after minimization because it was a harness artifact;
- only availability impact is demonstrated and no stronger property is evidenced;
- control over the relevant state cannot be shown;
- further proof would require harmful payload behavior rather than a benign marker/assertion.

## Output

Return a triage record with status, minimized reproducer, root-cause hypothesis, primitive (if any), control, confidence, and next verification step.
