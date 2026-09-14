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

Use when agents can call filesystem, shell, browser, email, cloud, code-hosting, database, financial, or other external-action tools and you need to determine whether an action stayed bound to the user's intent, effective authority, confirmation, and final observed state.

## Preconditions

1. Use mock/sandbox accounts, synthetic identities/resources, inert action sinks, reversible state, or read-only observations.
2. Document tool schemas, credential scopes, allowlists, confirmation rules, transaction behavior, and high-impact action classes.
3. Do not test destructive actions on real services, send real external messages, spend funds, alter production resources, or bypass actual user consent.
4. Define the highest evidence level the fixture can safely support before validation starts.

## Action-binding causal model

Trace every candidate finding through:

`request intent -> capability proposal -> normalized arguments -> effective authority -> policy decision -> confirmation snapshot -> execution binding -> observable bounded effect -> receipt/state -> retry/rollback state`

Tool availability, broad schema text, model prose, or a confirmation UI alone does not prove an action-level defect. Identify the exact transition where the intended contract and the observed effective contract diverge.

## Intent and capability model

Record the initiating principal, requested task, allowed side-effect class, proposed tool/capability, and whether the proposal is read-only, draft/propose, create, modify, execute, external-send, delete, or privilege-changing.

Keep these distinctions explicit:

- request intent is not the same as a model/tool capability proposal;
- declared capability is not the same as effective authority after policy and credential limits;
- read-only authority is not write/effect authority;
- one-step authority is not authority created by a chained plan.

A broad tool being installed is not itself a finding. Evidence requires a mismatch between intended authority and the effective action path.

## Argument normalization and binding

Track arguments through user-visible request state, model proposal, host normalization, policy filtering, confirmation-bound state, execution-time state, and receipt-observed target/effect.

Use synthetic targets and inert effects to determine whether the same material tuple remains bound across those stages. Harmless normalization is not a defect unless it changes a protected target, scope, effect class, or other policy-relevant field.

## Effective authority model

Effective authority is the bounded action capability that remains after principal identity, credential scope, host policy, allowlists, capability class, argument constraints, confirmation state, transaction policy, and service-side restrictions are applied.

Record nominal tool capability separately from effective authority at the decision point. Do not infer effect authority from schema exposure alone, and do not infer durable effect authority from a proposal or accepted mock call.

## Confirmation tuple

Model confirmation as a snapshot over the materially relevant tuple rather than a boolean `confirmed` flag. At minimum record:

- principal/session;
- tool/capability;
- target/resource;
- effect class;
- material arguments such as recipient, path, resource identifier, quantity, or irreversible flag when applicable;
- policy generation and credential generation;
- confirmation generation or equivalent binding identifier when available;
- expiry or mutation boundary.

If a material field changes after confirmation, the old confirmation must not be treated as evidence of consent for the changed tuple.

## Execution binding and state drift

Compare the confirmation snapshot with the execution-time tuple and the final read-back/receipt. Review only controlled fixtures for stale state, policy generation changes, confirmation generation changes, target substitutions, normalized-argument changes, or chained-plan transitions.

Use a time-of-check/time-of-use lens defensively: identify whether principal, policy, target, capability, or arguments changed between confirmation and the inert execution boundary. Do not provide instructions for bypassing real confirmation systems.

## Transaction, retry, and idempotency model

Record transaction identity, action generation, retry attempt, idempotency key or equivalent, observable receipt, rollback or compensation state, and final state.

A timeout, duplicate plan, or duplicate proposal is not proof of duplicate effect. Promote only when the fixture can distinguish proposal, accepted execution, receipt, durable final state, and any rollback state.

## Post-action verification

Require observable receipts or read-back state for effect claims. Preserve this inequality:

`proposal != accepted execution != receipt != durable final state`

A success string from the model or tool wrapper is insufficient when the backing state can be checked safely. For a read-only or inert fixture, the post-action oracle should be explicit and deterministic.

## Tool evidence ladder

Use evidence levels `T0` through `T5`:

- `T0`: tool/capability/schema is present or broadly described; no protected decision divergence.
- `T1`: proposal, normalization, or confirmation tuple differs from the request, but policy rejects it or no bounded effect is accepted.
- `T2`: deterministic policy or confirmation decision diverges from the intended action contract in a synthetic harness.
- `T3`: an inert mock action is accepted outside the intended effective authority or confirmation tuple.
- `T4`: a bounded synthetic effect or state change is observed and bound to the wrong action tuple.
- `T5`: the causal defect is repeatable across controls and includes durable post-action, retry/idempotency, or rollback-state proof plus regression evidence.

Never report above the highest directly demonstrated level.

## Counterfactual proof

Keep the harness and intended task fixed while changing one causal variable at a time: principal, capability class, argument tuple, policy generation, confirmation generation, target, retry identity, or final-state read-back. If the effect persists after the suspected variable is restored, downgrade or reject that explanation.

## Alternative explanations

Explicitly consider benign causes such as stale UI text with correct execution binding, harmless argument normalization, asynchronous receipt delay, duplicate proposal without duplicate effect, expected idempotent replay, mock-service artifacts, intentionally broad but policy-constrained schema, or bounded convergence after rollback.

## Evidence ceiling

State the maximum defensible evidence level and why it cannot be promoted further. A text/proposal mismatch cannot be reported as executed effect. An accepted mock call cannot be reported as durable state without a receipt or read-back oracle. A read/write policy mismatch without an accepted inert effect remains below effect-level evidence.

## Workflow

1. Inventory tool capabilities and classify read-only, propose/draft, create, modify, execute, external-send, delete, and privilege-changing operations.
2. Pin request intent, initiating principal, credential scope, and the protected side-effect boundary.
3. Trace proposed and normalized arguments through policy and confirmation state.
4. Record effective authority and the confirmation tuple at the decision point.
5. Use mock/sandbox tools to compare confirmation-bound state with execution-time state and bounded receipts.
6. Exercise positive, negative, and one-variable counterfactual controls.
7. For retries, verify transaction identity, idempotency behavior, receipt, final state, and rollback/compensation semantics.
8. Promote evidence only to the highest directly observed level and record alternative explanations that were rejected or remain plausible.
9. Verify remediation by rerunning the same deterministic controls without broadening the original authority.

## Operator depth

For a full authorized assessment, load the [operator runbook](references/operator-runbook.md). It expands this skill into transition-level action binding, confirmation-tuple reasoning, transaction/idempotency analysis, post-action verification, false-positive controls, evidence ceilings, and deterministic remediation checks.

## Evidence contract

Record principal/session, requested intent, capability proposal, normalized arguments, effective authority, policy decision, confirmation tuple, execution binding, bounded result/receipt, transaction/retry state, final read-back, controls, alternative explanations, evidence level, and evidence ceiling.

Tool availability alone is not unsafe; show a policy/capability/confirmation mismatch at a specific transition. Do not claim durable effect from proposal, confirmation display, or wrapper success text without the corresponding bounded receipt/state evidence.

## Stop conditions

Stop before sending real messages, changing production resources, deleting data, spending funds, altering real privileges, performing irreversible actions, or bypassing real account confirmations. Stop when a fixture would exceed its predeclared evidence ceiling or require production credentials/effects.

## Output

```text
agent/tool:
principal/session:
request intent:
capability proposal:
normalized arguments:
effective authority:
policy decision:
confirmation tuple:
execution binding:
transaction/retry state:
receipt/final state:
counterfactual controls:
alternative explanations:
evidence level:
evidence ceiling:
remediation regression:
```
