---
name: security-research-reporting
description: "Produce a reproducible evidence-bounded security research report from the case ledger: scope, tested revisions, claim state, root cause, controls, consequences, limitations, remediation, regression evidence, and artifacts. Use without overstating unproven impact."
metadata:
  nolane-security-category: orchestration
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Security Research Reporting

Perform dynamic or intrusive validation only in an authorized, owned lab or equivalent explicitly scoped test environment.

## When to use

Use for internal findings, responsible disclosure drafts, engineering handoff, audit notes, or case closure at any evidence state.

## Preconditions

1. Use only authorized evidence and redact secrets/personal data.
2. Preserve the exact case evidence state in the report.
3. Do not convert hypotheses into declarative vulnerabilities for narrative clarity.

## Workflow

1. Lead with tested target/revision/configuration, scope and evidence state.
2. State the claim in the narrowest language supported by current evidence.
3. Describe the root cause only if validated; otherwise label the causal hypothesis and alternatives.
4. Document reproducer prerequisites/fixture digest and benign expected evidence without embedding destructive payloads.
5. List positive/negative controls and explain what alternative explanations they eliminate.
6. Separate demonstrated security consequence from plausible higher impact and record mitigations/limitations.
7. Describe remediation direction and regression results if available; identify static consumers/variants or operational dependencies explicitly.
8. Provide artifact references/hashes and a concise reproduction checklist that another authorized researcher can follow.

## Evidence contract

A report is evidence-bounded when every material factual claim traces to case observations/controls/artifacts and uncertainty is visible. Formatting quality never upgrades the evidence state.

## Stop conditions

Stop publication/disclosure if sensitive data is unredacted, the target/version is uncertain, key claims lack provenance, or coordinated-disclosure requirements are unresolved.

## Output

```text
scope/target/revisions:
evidence state:
summary claim:
root cause or hypothesis:
reproduction/evidence:
controls:
bounded impact:
limitations/mitigations:
remediation/regression:
artifacts/provenance:
```
