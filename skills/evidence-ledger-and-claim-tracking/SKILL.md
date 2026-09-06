---
name: evidence-ledger-and-claim-tracking
description: "Keep an append-oriented ledger that separates observations, interpretations, claim revisions, controls, contradictions, provenance, and uncertainty. Use to make long security investigations auditable across agents and tools."
metadata:
  nolane-security-category: orchestration
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Evidence Ledger And Claim Tracking

Perform dynamic or intrusive validation only in an authorized, owned lab or equivalent explicitly scoped test environment.

## When to use

Use when a case spans multiple files/tools/runs/agents, when evidence can conflict, or when a conclusion may later need to be defended or reproduced.

## Preconditions

1. A stable research case ID exists.
2. Evidence artifacts use non-sensitive references/digests where possible.
3. Do not paste real credentials/secrets into a shared ledger.

## Workflow

1. Append each observation with timestamp/run identity, target revision, environment, tool/harness version, and artifact reference.
2. Store interpretation separately from raw observation so later reasoning can change without rewriting history.
3. Track claim revisions with why they changed and which evidence invalidated the previous formulation.
4. Link every control and reproducer to the exact claim/evidence stage it supports.
5. Record contradictions and failed experiments as first-class entries; they constrain future hypotheses.
6. Maintain uncertainty items with owner/next discriminating experiment rather than deleting caveats when confidence rises.
7. At handoff/report time, derive a current claim summary from the ledger instead of relying on conversation memory.

## Evidence contract

A ledger is sufficient when another authorized researcher can reconstruct the claim evolution and locate each supporting/contradicting artifact without relying on unstated chat context.

## Stop conditions

Stop and repair provenance if an important claim depends on an artifact with unknown target revision, unknown environment, or untraceable transformation.

## Output

```text
case ID:
observation entries:
artifact/digest references:
interpretations:
claim revisions:
controls:
contradictions:
uncertainties:
current summary:
```
