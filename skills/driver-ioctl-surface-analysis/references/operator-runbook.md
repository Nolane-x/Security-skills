# Driver Interface Operator Runbook

Use this runbook only on owned test systems, disposable virtual machines, simulators, or explicitly authorized hardware. Prefer schema review, synthetic requests, diagnostics, and read-only device state. The objective is to verify request contracts and caller boundaries without causing device or host side effects.

## Attack surface

Model each device-control command as a versioned request contract. Record caller class, handle/open policy, request selector, input/output schema, transfer method, length and version fields, object identifiers, state prerequisites, asynchronous lifetime, and the privileged subsystem or device state ultimately affected.

Group commands that share parsers, object tables, state machines, completion logic, or access policy so that one validated invariant can be checked across sibling interfaces.

## Hypothesis matrix

Create bounded hypotheses for schema/version disagreement, incomplete length validation, object-identity mismatch, caller-policy inconsistency, per-handle versus global-state confusion, and asynchronous lifetime mismatch.

Every hypothesis must define an expected contract and a benign signal such as a verifier diagnostic, controlled rejection result, synthetic object marker, or simulator state transition.

## Controlled validation

1. Pin driver/service build, OS/runtime revision, device or simulator model, and relevant configuration.
2. Establish the documented or source-derived request schema before generating a test.
3. Use synthetic buffers, identifiers, and state in a disposable lab fixture.
4. Exercise one contract dimension at a time and preserve the exact request metadata.
5. Compare accepted and rejected neighboring requests to prove the harness distinguishes valid from invalid input.
6. Capture diagnostics and state transitions without modifying unrelated device or host state.
7. Repeat asynchronous or lifecycle cases under the same pinned schedule controls when timing matters.
8. Compare sibling commands that use the same helper or object table only after the seed invariant is established.
9. Stop at the first direct evidence of a contract violation; no broader effect is required.
10. Route the causal invariant to remediation and regression tests.

## False-positive controls

Use valid versus one-field-invalid request pairs, correct versus neighboring object identity, expected caller class versus explicitly denied test caller, per-handle versus fresh-handle state, and synchronous versus controlled asynchronous test cases where applicable.

Reject findings caused by an undocumented schema guess, mismatched symbols/build, simulator behavior that differs from the real reviewed contract, or a diagnostic that appears equally for the valid control request.

## Evidence capture

```text
driver_service_revision:
device_or_simulator:
caller_test_class:
request_selector:
request_schema_version:
input_output_lengths:
object_identity:
state_preconditions:
async_lifetime:
expected_contract:
controlled_signal:
positive_control:
negative_control:
related_sibling_commands:
evidence_state:
```

A reachable command or broad caller class is not sufficient evidence. Preserve the exact contract violation and the control that distinguishes it from expected behavior.

## Remediation checks

Centralize schema/version validation, caller policy, object lookup rules, ownership/lifetime checks, and state-transition invariants where shared commands depend on them. Prefer fixes that make invalid states unrepresentable rather than special-casing one test input.

Regression verification must replay the original synthetic request plus a valid neighboring request and at least one sibling command or state path when the root cause is shared.
