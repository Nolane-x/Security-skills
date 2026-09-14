# Tool Capability And Confirmation Operator Runbook

Use this runbook only for owned, local, sandboxed, benchmark/CTF, or explicitly authorized systems. Prefer mock tools, synthetic identities/resources, inert action sinks, reversible state, and read-only verification. Stop before any real external send, production write, spending, destructive change, privilege change, or consent bypass.

## Attack surface

Map action-producing tools by capability class and trust boundary rather than by product name. Record request source, initiating principal/session, credential context, policy layer, tool schema, normalized arguments, confirmation surface, execution boundary, receipt source, and final-state oracle.

Separate read-only, propose/draft, create, modify, execute, external-send, delete, and privilege-changing capabilities. A single integration may expose several classes with different effective authority.

## Hypothesis matrix

For each candidate issue, write a falsifiable hypothesis that names the exact state transition expected to diverge. Useful hypothesis families include request-intent drift, read-to-write authority drift, argument-binding drift, stale confirmation state, execution-time state drift, retry/idempotency ambiguity, and receipt/final-state mismatch.

For every hypothesis, define one positive control, one negative control, a safe oracle, a stop condition, an alternative explanation, and an evidence ceiling before validation begins.

## Intent and capability binding

Capture the request intent and initiating principal before tool selection. Then record the capability proposal, its side-effect class, and whether the proposed capability is necessary for the stated task.

Keep request intent distinct from capability proposal. Keep nominal tool capability distinct from effective authority. Keep read-only authority distinct from write/effect authority, including authority that appears only after a chained plan.

## Argument normalization trace

Trace the material argument tuple across:

1. user-visible request arguments;
2. model-proposed arguments;
3. host-normalized arguments;
4. policy-filtered arguments;
5. confirmation-bound arguments;
6. execution-time arguments;
7. receipt-observed target/effect.

Mark only policy-relevant changes. Formatting, canonical ordering, or other harmless normalization is not a defect unless it changes target, scope, effect class, recipient/resource identity, or another protected field.

## Effective authority trace

Record principal/session, credential scope, host policy, allowlists, capability class, argument constraints, confirmation state, transaction policy, and service-side restrictions. The effective authority is the bounded action capability remaining after all of those constraints are applied.

Do not infer effective authority from schema exposure. Do not infer durable authority from an accepted proposal or wrapper success string.

## Confirmation tuple trace

Treat confirmation as a bound snapshot, not a boolean. Record at least:

- principal/session;
- tool/capability;
- target/resource;
- effect class;
- material arguments;
- policy generation and credential generation;
- confirmation generation or equivalent binding identifier;
- expiry or mutation boundary.

Compare the confirmation tuple with both the policy-decision tuple and the execution-time tuple. If a material field changes, record the change explicitly and do not reuse the earlier confirmation as evidence for the changed action.

## Execution binding and state drift

Use a defensive time-of-check/time-of-use lens. Compare confirmation-bound state to execution-bound state and ask whether principal, target, policy generation, confirmation generation, capability, or material arguments changed.

Validate only with mock or inert actions. The goal is to prove or reject binding drift, not to bypass a real confirmation mechanism.

## Transaction, retry, and idempotency

Record transaction identity, action generation, retry attempt, idempotency key or equivalent, accepted execution state, observable receipt, rollback/compensation state, and final read-back.

A retry request, timeout, duplicate plan, or duplicate proposal does not prove duplicate effect. An idempotent replay that yields one final state is a false-positive control, not a defect.

## Post-action verification

Preserve this distinction:

`proposal != accepted execution != receipt != durable final state`

Use a deterministic read-back oracle when the backing state can be inspected safely. For an inert sink, the receipt may be a synthetic marker or append-only mock ledger entry. For a read-only action, verify no effect state changed.

Do not promote wrapper text or model narration to durable-effect evidence without a bounded receipt/final-state observation.

## Controlled validation

Use a fixed harness with synthetic principals, synthetic targets, mock credentials, deterministic policy generations, inert action sinks, and reversible state. Change one causal variable at a time and preserve all other inputs.

Safe validation mechanisms include policy simulation, local mock services, in-memory or temporary-file state, synthetic receipts, deterministic counters, and read-only state comparisons.

## False-positive controls

Explicitly test and document benign alternatives, including:

- stale confirmation/UI text while execution binding remains correct;
- harmless argument normalization;
- asynchronous receipt delay without wrong final state;
- duplicate proposal without duplicate effect;
- expected idempotent replay;
- mock-service artifacts;
- intentionally broad schema constrained by policy;
- rollback or compensation still within a documented convergence window.

A candidate that is explained by one of these controls must be downgraded or rejected.

## Counterfactual controls

Keep the intended task and harness fixed while changing one variable: principal, capability class, argument tuple, policy generation, confirmation generation, target, retry identity, or final-state read-back.

A causal explanation is strengthened only when the suspect variable changes the bounded observation while the negative control does not. If the observation persists after restoring the intended variable, reject or downgrade that explanation.

## Evidence capture

Capture a compact trace containing:

- request intent and principal/session;
- capability proposal and class;
- argument normalization states;
- effective authority inputs;
- policy decision;
- confirmation tuple;
- execution binding;
- transaction identity and retry state;
- receipt and durable final state;
- positive, negative, and counterfactual controls;
- alternative explanations;
- remediation result.

Prefer structured synthetic identifiers and deterministic timestamps/generations from the fixture rather than real account identifiers or secrets.

## Evidence promotion and ceiling

Use the canonical `T0` through `T5` ladder. Promotion requires direct evidence for every lower transition needed by the claim.

- `T0` stays at metadata/schema presence.
- `T1` reaches proposal/normalization/confirmation mismatch without accepted bounded effect.
- `T2` requires deterministic policy/confirmation decision divergence.
- `T3` requires an accepted inert mock action outside intended effective authority or confirmation tuple.
- `T4` requires an observed bounded synthetic effect bound to the wrong action tuple.
- `T5` requires repeatable causal proof with durable post-action, retry/idempotency or rollback-state evidence, controls, and regression verification.

Always state the evidence ceiling. If the fixture cannot observe durable final state, it cannot support a durable-effect claim.

## Remediation checks

Rerun the exact failing fixture and all controls after remediation. Confirm that:

1. request intent still maps to the allowed capability class;
2. normalization preserves protected arguments;
3. effective authority does not exceed policy;
4. confirmation remains bound to the material tuple;
5. execution-time state matches the confirmed action;
6. retries preserve idempotency or explicit transaction semantics;
7. receipts/final state match the bounded action;
8. negative controls still demonstrate legitimate allowed behavior;
9. no broader confirmation or permission was introduced as a shortcut.
