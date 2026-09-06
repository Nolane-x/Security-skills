---
name: tool-capability-and-confirmation-analysis
description: "Analyze AI-agent tool capabilities, argument scoping, confirmation gates, read/write separation, least privilege, transaction boundaries, and post-action verification. Use harmless mock/sandbox tools to test authority enforcement."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Tool Capability And Confirmation Analysis

## When to use

Use when agents can call filesystem, shell, browser, email, cloud, code-hosting, database, financial, or other external-action tools.

## Preconditions

1. Use mock/sandbox accounts and reversible test resources.
2. Document tool schemas, credential scopes, allowlists, confirmation rules, and high-impact action classes.
3. Do not test destructive actions on real services or bypass actual user consent.

## Workflow

1. Inventory tools and split capabilities into read, propose/draft, create, modify, delete, execute, external-send, and privilege-changing operations.
2. Map identity/credential context for each tool and whether arguments can broaden scope beyond the user-visible request.
3. Identify actions requiring confirmation and define exactly what must be shown: target, effect, amount/resource, recipients, irreversibility.
4. Test benign mock actions for missing, stale, or ambiguous confirmation and for confused-deputy argument substitution.
5. Verify read-only requests cannot silently escalate to write tools through chained planning.
6. Check post-action receipts/state and rollback/idempotency where applicable.

## Evidence contract

Record tool, credential scope, requested intent, proposed arguments, confirmation artifact, executed benign result, and negative control. Tool availability alone is not unsafe; show a policy/capability mismatch.

## Stop conditions

Stop before sending real messages, changing production resources, deleting data, spending funds, or bypassing real account confirmations.

## Output

```text
agent/tool:
credential scope:
capability class:
requested intent:
proposed arguments:
confirmation gate:
benign result/control:
evidence status:
```
