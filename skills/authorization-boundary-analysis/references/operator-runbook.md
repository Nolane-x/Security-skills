# Authorization Boundary Operator Runbook

Use this runbook only with local, owned, sandboxed, benchmark/CTF, or explicitly authorized systems. Prefer synthetic accounts, tenants, objects, roles, and inert marker operations. Do not use real third-party identities or data as authorization probes.

The operator goal is to prove or disprove a specific principal–operation–resource–context policy relation and identify the enforcement point that produced the result.

## Attack surface

Model authorization as a graph of identities, resources, operations, policy inputs, enforcement points, and state transitions.

### Principal dimensions

Inventory every identity form that can reach the target operation:

- human account and session;
- tenant or organization membership;
- role/group membership;
- OAuth/API-token scopes;
- service, workload, or machine identity;
- delegated/on-behalf-of identity;
- background worker identity;
- internal service credential;
- administrative or support impersonation mode;
- anonymous/partially authenticated state.

Record where identities are created, translated, cached, delegated, refreshed, and attached to internal calls.

### Resource dimensions

For each resource class record:

- stable identifier and alternate aliases;
- owner and tenant;
- parent/child hierarchy;
- visibility and lifecycle state;
- sharing/delegation state;
- soft-delete/archive state;
- cache/index representation;
- export/download/report representation;
- indirect references through jobs, attachments, comments, or child objects.

Authorization bugs often appear when an alternate representation is checked less strictly than the canonical resource.

### Operation and execution dimensions

Enumerate read, list, search, create, update, delete, restore, share, export, approve, admin, bulk, and background operations. Include alternate verbs/content types, batch endpoints, GraphQL/resolver paths, asynchronous jobs, helpers, internal RPC, and legacy routes.

Locate every enforcement point: gateway, route middleware, controller, service method, policy engine, database row filter, storage layer, cache, message consumer, and privileged helper.

### Context dimensions

Record policy inputs that can change the decision:

- tenant and organization;
- project/workspace;
- object ownership;
- session age or authentication strength;
- network/origin/channel;
- feature flags;
- resource lifecycle state;
- delegation purpose;
- approval workflow state;
- time or region constraints.

## Hypothesis matrix

Construct explicit hypotheses before testing.

| Hypothesis class | Policy question | Controlled proof |
| --- | --- | --- |
| object-level mismatch | can principal A act on object B by changing an identifier? | B is a synthetic neighboring object and the inert operation succeeds unexpectedly |
| tenant-boundary mismatch | is tenant identity bound at every lookup/write? | tenant A principal reaches tenant B synthetic marker |
| collection/item inconsistency | do list/search/export paths apply the same object policy as item fetch? | a denied synthetic item appears through an aggregate path |
| batch partial-check gap | is every member of a batch authorized independently? | mixed authorized/denied synthetic objects are processed incorrectly |
| async identity drift | does a queued job preserve/re-evaluate initiating authority? | worker performs inert action after initiating identity loses the required synthetic permission |
| delegated-identity confusion | is caller identity distinguished from service/delegate identity? | delegated service acts outside the initiator's allowed synthetic scope |
| stale-cache decision | can cached authorization survive revocation/context change? | revoked synthetic access remains usable through cache/index path |
| policy/data binding gap | is the resource checked the same resource later mutated? | checked synthetic id differs from the inert sink actually changed |
| alternate-route gap | do legacy/internal/helper routes enforce the same invariant? | only an alternate test route accepts the prohibited tuple |
| state-transition gap | does authorization change correctly across share/archive/ownership transitions? | synthetic resource retains access after a transition that should remove it |
| scope composition gap | are global, object, method, and token scopes combined correctly? | one permissive scope unintentionally overrides a required restrictive dimension |
| confused deputy | can a low-authority caller induce a privileged component to use its own authority? | privileged mock helper performs an inert operation without caller-bound authorization |

For each row write the expected decision and source of authority: product requirement, policy configuration, ownership rule, test oracle, or explicitly approved security invariant.

## Controlled validation

1. **Freeze the policy snapshot.** Record application revision, policy-engine revision, route/service versions, test feature flags, identity configuration, and cache state.
2. **Create a synthetic identity lattice.** At minimum use an owner, same-tenant non-owner, different-tenant user, lower-role user, and service/delegated identity where relevant.
3. **Create paired synthetic resources.** Give each identity/tenant unique markers so accidental cross-access is unambiguous.
4. **Establish positive controls.** Confirm each intended principal-operation-resource tuple succeeds through the canonical path.
5. **Establish negative controls.** Confirm clearly prohibited neighboring tuples fail before exploring alternate paths.
6. **Vary one dimension at a time.** Change object id, tenant, role, scope, operation, route, content type, worker path, or lifecycle state independently.
7. **Trace policy input to sink.** Capture the identity/resource/context used at the decision and compare it to the identity/resource/context used at the final read/write/action.
8. **Exercise aggregate paths.** Test list/search/export/batch behavior using only synthetic resources because aggregate authorization is often implemented separately.
9. **Exercise asynchronous paths.** Queue benign marker operations and test whether authorization is bound to enqueue-time authority, execution-time authority, or an explicitly designed service identity.
10. **Exercise state transitions.** Change synthetic sharing, role, ownership, revocation, archive, or approval state and test whether all representations update consistently.
11. **Bound the consequence.** Use marker reads, no-op/benign updates, or dedicated test objects rather than destructive operations.
12. **Stop at the first proven invariant break.** Do not broaden from a synthetic proof to real data or unrelated accounts.

When the policy is intentionally delegated, shared, inherited, or eventually consistent, encode that expectation in the test oracle before deciding that a difference is unauthorized.

## False-positive controls

Use paired controls to rule out policy misunderstanding and test-harness artifacts:

- owner versus same-tenant non-owner;
- same-tenant versus different-tenant;
- allowed role versus lower role;
- full scope versus reduced scope;
- canonical item endpoint versus list/search/export representation;
- single-object operation versus batch with only allowed objects;
- immediate request versus asynchronous worker;
- before and after explicit synthetic revocation;
- direct caller versus explicitly delegated caller;
- object id versus an unrelated nonexistent id to distinguish authorization from generic lookup behavior;
- warmed cache versus cleared cache;
- policy engine decision log versus final data-store/action log.

Do not call a case validated if the observed difference can be explained by intended resource sharing, test fixture ownership, stale test setup, eventual consistency inside the documented window, an implicit administrator role, or a generic existence/error-message difference without unauthorized access/effect.

For enumeration-style behavior, distinguish information leakage about object existence from actual ability to read or modify the object; they may be separate findings with different evidence.

## Evidence capture

Capture authorization evidence as the complete decision tuple:

```text
case_id:
application_revision:
policy_revision:
principal_id_and_type:
principal_tenant_role_scopes:
delegated_identity_if_any:
operation:
requested_resource_id:
requested_resource_owner_tenant:
context_and_state:
policy_enforcement_point:
policy_inputs:
policy_decision:
resource_id_at_final_sink:
identity_at_final_sink:
benign_effect_or_marker:
positive_control:
negative_control:
cache_or_worker_state:
expected_policy_source:
evidence_state:
```

A `validated` finding requires proof that a specifically prohibited tuple is accepted or reaches a protected synthetic effect because a policy decision is absent, incomplete, stale, or bound to the wrong principal/resource/context. Preserve an allowed control and a denied neighboring control whenever possible.

If only policy source code appears weak but no reachable path has been established, keep the claim as a hypothesis. If a request is accepted but the protected sink is not reached, record that intermediate boundary rather than overstating impact.

## Remediation checks

Remediation should encode the authorization invariant at the narrowest authoritative layer that all relevant paths must traverse.

Check these dimensions:

1. **Canonical policy function:** centralize principal-operation-resource-context evaluation instead of duplicating route-specific checks.
2. **Object/tenant binding:** derive protected resource identity from authoritative data and bind tenant/owner constraints to the actual query or mutation.
3. **Defense in depth at data access:** where appropriate, use tenant-aware queries, row-level controls, scoped repositories, or equivalent safeguards so missing middleware is not sufficient for cross-boundary access.
4. **Delegation semantics:** carry both initiator and service identity; constrain privileged service actions by caller-authorized purpose and resource.
5. **Batch/aggregate parity:** authorize each protected member and prevent list/search/export paths from bypassing item-level policy.
6. **Async authority:** define whether jobs capture an immutable authorization grant, re-check current authorization, or use a narrowly scoped service role; avoid ambiguous inheritance.
7. **Cache correctness:** include every policy-relevant identity/resource/context dimension in cache keys or avoid caching decisions that cannot be invalidated safely.
8. **Revocation behavior:** invalidate sessions/tokens/cache entries according to the documented security requirement.
9. **State transitions:** re-evaluate permissions when ownership, tenant, sharing, role, archive, or approval state changes.
10. **Audit correlation:** record principal, delegated actor, resource, operation, policy result, and final sink without leaking sensitive content.

Regression verification must replay the original failing synthetic tuple and a matrix of neighboring intended-allow/intended-deny cases. A remediation that blocks the exploit path by disabling the feature, breaking all access, or special-casing one test identifier is not sufficient.
