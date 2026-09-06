---
name: symbolic-execution-workflow
description: "Use symbolic or concolic execution to answer bounded reachability and path-constraint questions in an authorized program or binary. Use when a suspicious state is known but concrete inputs are hard to derive, branches block exploration, or path conditions need formal inspection."
metadata:
  nolane-security-category: discovery
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Symbolic Execution Workflow

Use symbolic execution as a scalpel for a bounded question, not as an attempt to symbolically execute an entire complex application.

## When to use

Use when:

- a target state/function is known;
- path constraints are the main blocker;
- a concrete input is hard to derive manually;
- static reasoning needs feasibility confirmation.

## Preconditions

- Target is local, owned, sandboxed, benchmark/CTF, or explicitly authorized.
- Identify entry state, target state, and avoidance states.
- Model environment interactions narrowly enough to avoid unconstrained explosion.

## Workflow

1. Define one reachability question.
2. Select the smallest entry point that still includes the relevant checks.
3. Mark only necessary attacker-controlled values symbolic.
4. Concretize environment details that are not part of the hypothesis.
5. Define target/avoid conditions using semantic events where possible.
6. Bound loops, recursion, input sizes, and time.
7. Inspect constraints when exploration stalls; do not blindly add compute.
8. If a path is found, export a concrete benign test input and reproduce it normally.
9. If no path is found, distinguish “proved infeasible under model” from “search/model incomplete.”
10. Route reproduced anomalies to evidence validation.

Tool families may include angr-, Triton-, Manticore-, or custom SMT/concolic workflows.

## Evidence contract

A useful symbolic result includes:

- modeled entry state;
- symbolic variables and ranges;
- environmental assumptions;
- target and avoid predicates;
- solver/path constraints;
- concrete witness if found;
- independent concrete reproduction.

A solver-generated witness without native reproduction is not a validated vulnerability.

## Stop conditions

Stop or simplify when:

- path explosion prevents meaningful state progress;
- external environment is modeled with unrealistic unconstrained values;
- the witness cannot be reproduced concretely;
- the next step would exceed authorized scope.

## Output

Return the bounded question, model assumptions, explored/blocked state summary, witness or infeasibility result, reproduction status, and next action.
