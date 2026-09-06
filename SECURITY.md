# Security and responsible-use policy

Security Skills is intended for secure development, defensive review, education, vulnerability research, benchmarks, CTF/lab work, and explicitly authorized testing.

## Scope rule

A skill that can interact with a live target must first establish that the target is one of:

- owned by the user;
- a local or isolated research environment;
- a benchmark/CTF intentionally provided for testing; or
- covered by explicit authorization that includes the contemplated activity.

When scope is ambiguous, the skill should remain in non-intrusive analysis mode.

## Proof rule

Prefer the least harmful evidence that proves the research claim. Good examples include:

- sanitizer or debugger evidence;
- a deterministic test failure;
- a minimized crashing input;
- a marker file in a local harness;
- a safe callback or assertion proving control flow;
- a regression test that fails before a fix and passes after it.

Avoid escalating a proof into persistence, credential access, destructive changes, covert collection, security-control disabling, or uncontrolled propagation.

## Reporting security issues in this repository

If a repository script, workflow, or bundled asset creates an unexpected security risk, open a GitHub security report where available rather than publishing sensitive details in a public issue.
