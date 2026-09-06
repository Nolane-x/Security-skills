---
name: template-expression-boundary-analysis
description: "Analyze template and expression engines for data-vs-code boundaries, context escaping, dynamic evaluation, helper/function exposure, sandbox policy, and tenant-controlled templates. Use to distinguish injection from intended templating capabilities."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Template Expression Boundary Analysis

## When to use

Use when applications render templates, expressions, rules, filters, user-customizable messages, server-side transformations, or sandboxed scripting.

## Preconditions

1. Use a local/staging authorized environment with inert expressions.
2. Pin engine/framework version, enabled extensions/helpers, sandbox mode, and template source trust level.
3. Do not use OS-command or persistence payloads; use arithmetic/string/marker expressions.

## Workflow

1. Classify which inputs are template source, expression source, plain data, variable names, filters/helpers, or context configuration.
2. Trace construction/compilation/evaluation and whether untrusted data can cross from value position into source position.
3. Map available object graph, helpers/functions, filesystem/network/process abstractions, and sandbox restrictions.
4. Use benign expressions to establish whether evaluation exists and negative controls to show intended data escaping.
5. Test sandbox policy with harmless denied capabilities or synthetic objects rather than system effects.
6. Separate “expression evaluated” from “security boundary escaped”; route only proven capability expansion to sandbox analysis.

## Evidence contract

Record engine/version, source-trust model, controlled field, evaluation context, benign expression result, denied/allowed capability controls, and affected policy boundary.

## Stop conditions

Stop before invoking process execution, reading real secrets/files, network pivoting, or testing public multi-tenant templates outside explicit scope.

## Output

```text
engine/version:
template ownership:
controlled source/data field:
evaluation context:
available helpers/capabilities:
benign controls:
boundary consequence:
evidence status:
```
