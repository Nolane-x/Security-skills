---
name: root-cause-impact-separation
description: "Separate the proven causal defect from reachability, primitive/control level, security boundary crossed, mitigations, and real-world impact. Use to prevent crash→RCE, renderer→escape, or exposed-interface→authorization-bypass overclaims."
metadata:
  nolane-security-category: orchestration
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Root Cause Impact Separation

Perform dynamic or intrusive validation only in an authorized, owned lab or equivalent explicitly scoped test environment.

## When to use

Use after an observed bug candidate has a plausible cause and before assigning severity, exploitability, privilege-boundary or product-impact claims.

## Preconditions

1. The target and observation are authorized and pinned.
2. Keep the root-cause claim independently testable from the impact claim.
3. Use benign markers/controls; no weaponized payload is required.

## Workflow

1. State the narrow causal defect as an invariant violation independent of attacker story.
2. State the demonstrated reachability: which principal/input reaches the defect under which configuration.
3. Classify the demonstrated primitive conservatively: rejection mismatch, data exposure, state corruption, crash, memory read/write, authorization action, controlled indirect call, etc.
4. List additional hops required for higher impact: sandbox/privilege boundary, code-control, secret value, cross-tenant identity, persistence, or network reachability.
5. For each hop, mark demonstrated, plausible-but-unproven, blocked by mitigation, or outside scope.
6. Run a benign boundary proof where needed (synthetic marker/resource) rather than substituting an offensive payload.
7. Write severity/impact language limited to demonstrated hops and preserve unresolved mitigations/assumptions.

## Evidence contract

The report must support root cause and each claimed impact hop with separate evidence. Missing higher-hop evidence lowers the claim; it does not invalidate the underlying bug.

## Stop conditions

Stop impact escalation when the next hop would require weaponization, production intrusion, bypassing an unrelated boundary, or assumptions not demonstrated in the authorized environment.

## Output

```text
causal defect:
reachable principal/input:
demonstrated primitive:
boundary hops:
mitigations/assumptions:
benign proof:
bounded impact statement:
unproven higher impacts:
```
