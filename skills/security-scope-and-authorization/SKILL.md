---
name: security-scope-and-authorization
description: "Establish authorization, target boundaries, permitted actions, and proof limits before security testing. Use before fuzzing, dynamic analysis, scanning, exploit reproduction, live-target testing, or any workflow that can change or stress a system."
metadata:
  nolane-security-category: foundation
  nolane-security-version: "1"
  nolane-security-authorization: not-applicable
---
# Security Scope and Authorization

Convert vague permission into an explicit research boundary before intrusive work.

## When to use

Use before any activity that may:

- send generated traffic or malformed input to a live service;
- execute a proof of concept;
- fuzz or stress a target;
- attach instrumentation/debuggers to a process not clearly local;
- modify cloud, device, account, or application state;
- test privilege or isolation boundaries.

## Preconditions

Collect the minimum available context:

- target identity and owner;
- environment (local lab, CTF, staging, production, public third party);
- allowed dates/windows if relevant;
- allowed techniques and prohibited actions;
- data handling constraints;
- expected proof level.

If the target is the user's local code, test fixture, sandbox, benchmark, or owned lab, state that directly.

## Workflow

1. **Name the target boundary.** Prefer exact repository, application, host group, lab image, or benchmark rather than “the network.”
2. **Classify the environment.**
   - local/offline;
   - isolated lab/CTF;
   - owned development/staging;
   - owned production;
   - third party with explicit authorization;
   - unknown.
3. **Classify the proposed action.**
   - read-only/static;
   - passive observation;
   - active but low-impact;
   - stress/fuzzing;
   - privilege/isolation validation;
   - state-changing proof.
4. **Match action to permission.** Unknown scope defaults to read-only/non-intrusive analysis.
5. **Define proof ceiling.** Prefer the least harmful signal that can prove the claim.
6. **Record exclusions.** Examples: no credential access, no persistence, no destructive changes, no lateral movement, no uncontrolled availability impact.
7. Hand the resulting scope record to downstream skills.

## Evidence contract

The scope record is sufficient when another researcher could answer:

- what may be tested;
- where;
- using which class of technique;
- what must not be done;
- what evidence is acceptable.

Do not infer authorization from public accessibility alone.

## Stop conditions

Stop intrusive work when:

- ownership/authorization is unknown;
- the requested technique is outside the stated scope;
- the target changed from lab/staging to production without renewed scope;
- proof requires materially more impact than the approved ceiling.

Non-intrusive source review, threat modeling, and defensive guidance may continue.

## Output

Return:

```text
target:
environment:
authorization basis:
allowed actions:
excluded actions:
proof ceiling:
data constraints:
scope confidence: confirmed | partial | unknown
```
