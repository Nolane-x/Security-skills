# Web Routing And Middleware Operator Runbook

Use this runbook only with source plus a local, staging, sandboxed, or explicitly authorized deployment. Use synthetic principals, inert handlers, and test-only state. The goal is to verify that equivalent request representations receive the same reviewed policy treatment.

## Attack surface

Map the request interpretation chain from the test edge to the selected handler. Record normalization, rewrite, route selection, middleware sequence, identity context, tenant context, content handling, fallback behavior, and downstream dispatch.

For every layer, record the representation actually consumed instead of assuming that all components see the same path, method, host, or identity.

## Hypothesis matrix

Create falsifiable hypotheses for policy consistency across equivalent representations, middleware coverage, method handling, host/proxy context, fallback routes, and tenant-context attachment.

Each hypothesis must state the expected invariant first and use only an inert local handler or synthetic response marker as its proof signal.

## Controlled validation

1. Pin framework, proxy, and application revisions and configuration.
2. Create synthetic identities, test tenants, and inert handlers.
3. Capture one request that should be accepted and one neighboring request that should be denied.
4. Record representation, policy state, and selected handler at every observable layer.
5. Change one representation dimension at a time while preserving the intended semantic request.
6. Compare only topology paths that are part of the authorized test deployment.
7. Keep validation independent of business side effects by using inert handlers.
8. Minimize the representation difference that changes the observed policy result.
9. Repeat with equivalent controls to distinguish documented aliases from policy inconsistency.
10. Preserve the complete evidence chain for remediation and regression testing.

## False-positive controls

Use exact versus equivalent representation pairs, reviewed protected versus reviewed public inert handlers, expected versus neighboring methods, and normalized versus pre-normalized representations.

Reject cases explained by stale test state, intentionally different policy classes, documented aliases, or a test handler whose middleware differs from the reviewed route class.

## Evidence capture

```text
stack_revision:
raw_test_request:
normalized_representation:
route_match:
middleware_sequence:
principal_tenant_context:
selected_inert_handler:
expected_policy:
observed_policy:
synthetic_marker:
positive_control:
negative_control:
evidence_state:
```

A different handler is not sufficient evidence. The recorded policy invariant must also differ for representations intended to be equivalent.

## Remediation checks

Prefer one canonical interpretation before policy enforcement, explicit route-group policy, centralized identity binding, and regression tests that exercise the deployed test topology.

Replay the original synthetic case plus neighboring allowed and denied controls. A remediation is incomplete if it only hides one representation while leaving an equivalent policy inconsistency.
