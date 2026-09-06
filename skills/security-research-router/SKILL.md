---
name: security-research-router
description: "Route an authorized security research task to the smallest useful combination of discovery, verification, remediation, or domain skills. Use when the target is complex, the right technique is unclear, or multiple security methods may be needed."
metadata:
  nolane-security-category: orchestration
  nolane-security-version: "1"
  nolane-security-authorization: conditional
---
# Security Research Router

Use this skill as the entry point for multi-step security research. It selects focused skills and keeps the investigation evidence-driven.

See [the routing map](references/routing-map.md) when several techniques appear applicable.

## When to use

Use when:

- the user asks for a security review/research plan rather than one narrow technique;
- the target spans source, binaries, protocols, runtimes, or trust boundaries;
- an initial technique has stalled and a method switch may be useful;
- findings need to move from hypothesis through validation and remediation.

Do not use it as an excuse to activate every skill.

## Preconditions

1. Establish scope with `security-scope-and-authorization` before intrusive or live-target work; proceed only on local, owned, sandboxed, CTF/benchmark, or explicitly authorized targets.
2. Identify the artifact available: source, binary, trace, crash, patch, protocol description, configuration, or running lab.
3. Record constraints such as platform, version, build flags, sanitizers, and whether reproduction is permitted.
4. Keep public/third-party targets in non-intrusive analysis unless authorization is explicit.

## Workflow

1. **Classify the question.**
   - architecture/trust boundary -> `attack-surface-mapping`;
   - plausible bug patterns -> `vulnerability-hypothesis-generation`;
   - input-driven native target -> `fuzzing-workflow`;
   - cross-function source/sink reasoning -> `static-dataflow-analysis`;
   - path-constraint question -> `symbolic-execution-workflow`;
   - binary-only target -> `binary-reconnaissance`;
   - crash/anomaly -> `crash-triage-and-minimization`;
   - claimed vulnerability -> `evidence-driven-vulnerability-validation`;
   - security fix/known patch -> `patch-diff-variant-analysis`;
   - fix construction -> `remediation-and-regression`;
   - code change/review -> `secure-code-review`;
   - tool-using LLM/agent -> `ai-agent-security-assessment`.
2. **Choose one primary method** and at most two supporting skills for the first pass.
3. **Define the evidence checkpoint** that would justify continuing, switching methods, or rejecting the hypothesis.
4. **Run the cheapest discriminating analysis first.** Prefer source inspection or deterministic tests before expensive broad exploration.
5. **Escalate only when the prior method creates a concrete question.** Example: static dataflow finds a suspicious state; symbolic execution then tests reachability.
6. **Route anomalies to verification.** No discovery skill may promote its own result directly to “validated.”
7. **Route a validated root cause to remediation** and require a regression test or equivalent fix evidence.
8. Summarize the chain as `question -> method -> evidence -> next decision`.

## Evidence contract

A good routing decision includes:

- why the selected skill matches the artifact and question;
- the evidence expected from that method;
- the condition for switching methods;
- the current finding status: hypothesis, observed, validated, or regression-verified.

Routing success is not measured by the number of tools used.

## Stop conditions

Stop or reduce scope when:

- authorization does not cover intrusive work;
- required artifacts or versions are missing;
- the next method cannot produce stronger evidence than the current one;
- results depend on an uncontrolled environment and cannot be reproduced;
- the task shifts toward destructive payloads, persistence, credential access, or indiscriminate exploitation.

## Output

Produce a compact research route:

```text
scope:
target/artifact:
primary skill:
supporting skills:
first evidence checkpoint:
switch condition:
current status:
```
