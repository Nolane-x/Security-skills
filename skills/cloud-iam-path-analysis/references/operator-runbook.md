# Cloud IAM Path Operator Runbook

Use this runbook for read-only IAM inventory review, policy-model review, provider policy simulation/explain tooling, local tests, synthetic cloud fixtures, and explicitly authorized sandbox environments. Prefer normalized policy data, test identities, synthetic resources, mock workload claims, and inert assertions. Do not use production secrets, unrelated tenants, destructive administrative actions, or guardrail removal as evidence.

The objective is to distinguish three things that are often conflated:

1. a policy statement that appears permissive;
2. an **effective edge** whose complete authorization preconditions are satisfied;
3. a **causal path** in which every required edge can coexist in one compatible policy/session state and reaches a precisely defined target capability.

A deep IAM review explains why each edge exists, why restrictive controls do not eliminate it, what session or trust state it depends on, what would make it disappear, and how a remediation breaks the path without breaking intended neighbors.

## Effective permission semantics

Do not treat a cloud IAM graph as a graph of raw `Allow` statements. Build it from provider-aware effective authorization decisions.

For each candidate edge normalize:

```text
source principal
semantic transition/capability
target principal/resource/scope
policy sources
edge preconditions
trust conditions
session context
explicit deny controls
maximum-permission controls
resource conditions
provider precedence semantics
-> effective decision
```

The exact composition algorithm is provider-specific. The model below is conceptual; when AWS, Azure, GCP, Kubernetes federation, or another system differs, the provider's documented semantics are authoritative.

### Policy-source roles

Classify policy sources by what they do, not only by their file/API type:

- **positive grant:** can contribute authority when applicable;
- **resource grant:** grants through the protected resource or resource owner;
- **trust rule:** determines whether an identity/session transition is accepted;
- **explicit deny:** prevents a capability when applicable according to provider precedence;
- **maximum-permission control:** caps what can become effective but does not itself grant the capability;
- **session restriction:** narrows or conditions derived authority;
- **organization/tenant guardrail:** constrains authority at a broader administrative scope;
- **condition:** activates or deactivates a rule based on tags, claims, source, resource, region, time, audience, or another context field;
- **service-specific rule:** adds semantics not captured by generic identity/resource policy composition.

A review should be able to answer: *which source grants this edge, which sources constrain it, and which provider rule determines the final effective decision?*

### Explicit deny

An applicable **explicit deny** must be represented as a first-class decision input. Do not hide it in notes after drawing the edge.

For every candidate path, record:

- where the deny originates;
- the principal/resource/action/context universe to which it applies;
- whether the current edge falls inside that universe;
- how the provider resolves conflict between this deny and positive grants.

If deny applicability is unresolved, the edge is unresolved.

### Maximum-permission controls

A **maximum-permission** control defines a ceiling. Typical examples include permission boundaries, organization guardrails, maximum role scopes, session limits, or analogous provider mechanisms.

Ask two separate questions:

1. Does some policy source positively grant the semantic capability?
2. Does every applicable ceiling permit that grant to become effective?

Do not create an edge merely because the ceiling includes an action. A ceiling that says "at most X" is not evidence that X was granted.

### Resource and scope semantics

Normalize both action and resource/scope. Wildcards, inheritance, hierarchy, parent scopes, resource aliases, tags, condition keys, and provider-specific resource matching can make two syntactically similar policies semantically different.

Record the authoritative target resource or administrative scope for the edge. Avoid path labels such as "can administer cloud" when the evidence supports only a particular resource class or scope.

### Trust conditions

Identity transitions require more than source-side permission in many systems. Normalize the complete **trust condition**:

- trusted source principal or source scope;
- issuer or identity provider;
- subject/workload selector;
- audience/recipient;
- external/context identifier;
- source-resource or source-account binding;
- required tags/claims/attributes;
- provider-specific chain/session constraints.

A source-side grant and a target-side trust rule are distinct evidence. Both may be required for one edge.

### Session context

The **session context** is security state attached to the effective principal at a particular edge. Capture only fields that influence authority:

- session policy or role/session scope;
- tags/claims/attributes;
- source identity or delegated initiator;
- authentication context;
- session issue time and expiry;
- revocation semantics;
- role-chain/session-chain constraints;
- policy revision relationship;
- provider-specific transient identity fields.

A static principal may have one policy set while a derived session carries a narrower effective set. Conversely, a policy edit may not retroactively alter an already issued session. State the provider rule rather than assuming either behavior.

## Attack surface

For this runbook, the attack surface is the set of authority-bearing relationships visible through owned policy/configuration/state—not a request to exercise those relationships against production.

### Principal inventory

Include, when relevant:

- human identities and groups;
- roles, service accounts, service principals, managed identities;
- workload identities from compute, containers, Kubernetes, CI/CD, and serverless runtimes;
- federated OIDC/SAML/external subjects;
- managed cloud services acting for a customer;
- automation/deployment identities;
- support/admin or break-glass identities if explicitly in scope.

For each principal record:

- authoritative scope/tenant/account/project/subscription;
- authentication/federation mechanism;
- direct and inherited attachments;
- trust/federation constraints;
- session lifetime model;
- tags/attributes/claims relevant to policy;
- whether another owned actor can change the principal's effective policy or runtime configuration.

### Policy inventory

Inventory all layers that materially participate in the provider's effective decision, including resource and key policies, organization controls, boundaries/ceilings, trust, federation mappings, conditional access, and service-specific delegation rules.

Annotate each policy source with:

- revision/snapshot;
- semantic role (grant/deny/ceiling/trust/condition);
- applicable principal/action/resource/context domain;
- precedence/composition rule;
- whether the chosen simulator/model covers it.

### Authority-changing surfaces

An actor may affect future authority without currently holding the target data-plane capability. Model these as graph-state transitions rather than direct target edges.

Examples include the ability, in an authorized test model, to change:

- policy attachments or role assignments;
- trust/federation mappings;
- workload identity bindings;
- code/configuration consumed by a stronger workload;
- resource/key policy;
- deployment identity association;
- session issuance configuration.

The review must state the resulting synthetic policy state before evaluating any later edge that depends on the change.

## Hypothesis matrix

| Hypothesis class | Causal question | Required local/model evidence | Main disambiguation |
| --- | --- | --- | --- |
| direct effective grant | does the complete policy composition allow P/A/R/C? | authoritative simulator/model decision plus policy-source trace | same tuple with one required condition changed |
| identity transition | can source become/use target identity under both source permission and target trust? | source decision + complete trust tuple + derived session context | neighboring source/claim that target trust rejects |
| maximum-scope oversight | does a positive grant survive boundary/org/session ceilings? | explicit evaluation of each ceiling under provider semantics | equivalent model with restrictive ceiling present |
| resource-policy alternate grant | does resource policy contribute authority not visible in identity policy? | composed identity/resource effective decision | identity-only interpretation compared with complete decision |
| authority-changing state transition | can owned actor change policy/trust/workload state such that a new edge becomes effective? | before/after synthetic model and new effective decision | state-change permission absent or target change outside editable scope |
| federation selector breadth | does trust mapping accept more subjects/claims than intended? | simulated neighboring subject and trust-condition evaluation | intended subject with identical non-selector context |
| workload identity mismatch | does workload tuple map to a cloud principal outside intended selector? | local/simulated claim tuple -> principal mapping | one-at-a-time claim mismatch |
| managed-service delegation | is service authority correctly bound to source/customer/resource/purpose? | normalized delegation decision with initiator/context retained | same service with neighboring denied source context |
| session-lifetime mismatch | does current session authority differ from expected post-change policy state? | issue/expiry/revocation semantics plus session decision | fresh session under current policy snapshot |
| temporal incompatibility | do path edges require states that cannot coexist? | explicit edge timestamps/policy revisions/session windows | compatible-state reconstruction shows path cannot exist |

Every hypothesis must name the exact **edge precondition** that could falsify it. "Policy looks broad" is not a complete hypothesis.

## Edge proof model

An IAM path should be assembled from edge proof records, not free-form arrows.

Use a conceptual record like:

```text
edge_id:
source_principal:
semantic_transition_or_capability:
target_principal_or_resource:
resource_scope:
policy_sources:
positive_grants:
explicit_denies:
maximum_permission_controls:
trust_condition:
session_context:
edge_precondition:
provider_composition_rule:
effective_decision:
decision_evidence:
model_or_simulator_limitations:
temporal_validity:
remaining_assumptions:
```

### Edge precondition

The **edge precondition** is the smallest set of facts that must be true for the edge to exist. Make it explicit enough that a reviewer can construct a counterfactual by changing one fact.

Examples of precondition classes—not provider-specific recipes—include:

- source principal has an applicable positive grant;
- authoritative resource is inside policy scope;
- target trust accepts source/issuer/subject/audience;
- required context/tag/claim matches;
- no applicable explicit deny overrides the grant;
- all maximum-permission ceilings permit the capability;
- session is valid and carries required context;
- an earlier synthetic state transition has actually produced the policy state assumed by this edge.

### Effective decision

Record an **effective decision** for the edge: allowed, denied, unresolved, or provider-specific equivalent. A raw policy match is not enough.

If the simulator cannot model a relevant layer, the effective decision may remain unresolved even if all modeled layers say allow.

### Edge evidence state

Keep edge evidence distinct from whole-path evidence. One edge can be observed while the path remains a hypothesis.

Useful edge notes include:

- statically modeled only;
- authoritative simulator/explain result;
- local synthetic fixture result;
- blocked by deny/ceiling/condition;
- unresolved due to provider/service semantics;
- temporally incompatible with another edge.

## Path causality

A path is causal only when the ordered edges form one realizable authority chain.

### Edge conjunction

For path `E1 -> E2 -> ... -> En`, every required edge must be effective under compatible assumptions. One unresolved or denied edge breaks validation of the whole chain.

Do not average edge confidence. Nine strong edges plus one speculative edge still produce a speculative path.

### State compatibility

Check that the output state of one edge satisfies the input requirements of the next:

- principal/session identity;
- policy/session restrictions;
- tags/claims/source identity;
- resource/scope binding;
- workload/delegation context;
- time and policy revision.

If an edge requires a session issued before a policy change and a later edge requires a condition only present after that change, write the incompatibility explicitly.

### Authority-changing edges

When one edge changes policy/trust/workload configuration, separate:

```text
state S0
-> authorized synthetic configuration change
-> state S1
-> recomputed effective authorization under S1
```

Do not skip directly from "can edit configuration" to the final target capability. The resulting state must actually contain the policy/trust relationship that the next modeled edge uses.

### Non-transitivity

Do not assume A→B and B→C imply A→C. Derived sessions and delegated identities can carry constraints that differ from B's long-lived identity. Record the actual identity/session represented at each edge.

### Target capability

Define the terminal capability precisely. Prefer a semantic target such as "read synthetic object class R in scope X" or "cause synthetic workload W to execute under principal P" rather than labels such as "admin" or "privilege escalation" unless that exact administrative state is what the policy model proves.

## Controlled validation

Prefer policy models and provider simulators. Use sandbox/runtime confirmation only where it adds evidence not available statically and only with inert synthetic resources.

1. Freeze provider/scope/policy/session snapshot.
2. Normalize policy-source roles and provider precedence.
3. Build candidate edge records with explicit preconditions.
4. Mark edges denied or unresolved before composing paths.
5. Run authoritative policy simulator/explain tooling where available and record unsupported layers.
6. Construct local/synthetic fixtures for trust, workload claims, session context, resource matching, or policy composition when appropriate.
7. Change one decision-relevant dimension at a time for controls.
8. Represent policy/configuration edits as before/after model states, not as direct target authority.
9. Confirm temporal compatibility among session and policy facts.
10. Stop once the smallest causal path or blocking edge is established.

Do not turn a defensive path analysis into production privilege exercise. Reading real secrets, changing production IAM, disabling controls, or touching unrelated accounts is unnecessary for this evidence model.

## Counterfactual controls

A counterfactual tests causality by changing a single policy-relevant fact and predicting which edge changes.

### Neighboring path

A **neighboring path** should share as much structure as possible with the case under review while differing in one material precondition.

Examples include:

- same source/target/resource, one trust claim differs;
- same grant, an applicable maximum-permission ceiling differs;
- same identity/resource, explicit deny applicability differs;
- same workload tuple, one bound claim differs;
- same path, fresh session replaces an older session;
- same authority-changing policy, editable scope excludes the target policy object.

### Deny counterfactual

If the causal claim depends on an allow surviving policy composition, a model with an applicable authoritative explicit deny should remove the edge according to provider semantics. If it does not, either the deny is outside the policy universe or the model is incomplete.

### Ceiling counterfactual

If a grant exceeds a maximum-permission control, the edge should be denied/limited even though the positive grant remains. This distinguishes "grant exists" from "grant is effective."

### Trust counterfactual

Change only a trust-relevant source/issuer/subject/audience/context field. The intended trust tuple should remain accepted while the neighboring tuple should not create the identity-transition edge.

### Session counterfactual

When session age/revision matters, compare a session state whose documented semantics should retain old authority with a fresh/recomputed session under the current policy snapshot. Record provider behavior rather than assuming immediate revocation.

### Alternative explanation

For every promoted path, identify at least one plausible **alternative explanation** and the evidence that weakens it. Common alternatives include:

- stale or incomplete inventory;
- inherited group/role not modeled;
- resource policy omitted from the model;
- organization deny or boundary omitted;
- simulator blind spot;
- provider/service implicit behavior;
- session issued under a different policy revision;
- documented eventual consistency;
- resource alias/hierarchy interpreted incorrectly;
- intended managed-service autonomy rather than caller-bound delegation.

## False-positive controls

Cloud IAM path analysis is unusually sensitive to incomplete composition. Use controls that exercise the whole decision model:

- complete policy set versus grant-only interpretation;
- applicable deny versus equivalent fixture without deny;
- positive grant inside versus outside maximum-permission ceiling;
- intended trust tuple versus one changed claim/source condition;
- fresh session versus policy-revision-sensitive older session when relevant;
- intended workload selector versus one changed workload attribute;
- same resource class inside versus outside authoritative scope;
- intended managed-service source context versus neighboring denied source context;
- state S0 versus resulting state S1 for authority-changing edges;
- complete path versus the same path with one required edge removed.

Downgrade findings when a path can be explained by missing policy layers, simulator coverage limits, stale snapshot, inherited identity state, documented propagation/session behavior, or an intended trust/delegation model.

An edge is not validated because a policy statement syntactically includes an action. An effective decision is the unit of evidence.

## Evidence ladder

### Hypothesis

Use when policy/configuration review suggests a candidate edge/path but one or more edge preconditions, restrictive layers, provider semantics, or compatible session states are unresolved.

Required record:

- candidate ordered path;
- unresolved edge(s);
- missing decision evidence;
- policy/session snapshot.

### Observed

Use when at least one material edge is established by authoritative simulator/explain evidence or a controlled local/synthetic fixture, while the complete path remains incomplete.

Record which edges are observed and which remain modeled only.

### Validated

Use only when:

- each required edge has an authoritative or otherwise defensible effective decision;
- edge preconditions are explicitly satisfied;
- explicit deny and maximum-permission controls have been evaluated;
- trust and session context are captured where relevant;
- edge states are temporally compatible;
- the exact terminal capability is bounded and supported;
- neighboring counterfactuals isolate material path conditions;
- alternative explanations are addressed for the scope claimed.

### Regression verified

Use after remediation only when the original path is recomputed against the fixed policy/configuration state, the selected **path-breaking control** removes the dangerous edge/path for the intended reason, and at least one intended **neighboring path** remains effective.

If an equivalent alternate edge reconstructs the target capability inside the reviewed scope, the original remediation is incomplete even if the edited policy looks narrower.

## Evidence capture

Preserve a reconstructable path record:

```text
case_id:
provider_and_scope:
inventory_timestamp:
policy_snapshot:
source_principal:
target_capability:
ordered_edge_ids:
edge_preconditions:
per_edge_policy_sources:
per_edge_positive_grants:
per_edge_explicit_denies:
per_edge_maximum_permission_controls:
per_edge_trust_conditions:
per_edge_session_context:
per_edge_effective_decision:
provider_composition_rule:
temporal_compatibility:
policy_simulator_evidence:
simulator_limitations:
bounded_synthetic_evidence:
positive_control:
neighboring_path:
counterfactual:
alternative_explanation:
alternative_explanation_control:
evidence_state:
causal_path_summary:
```

Write conclusions in causal form. For example:

> Under snapshot S, edge E2 is effective because positive grant G applies to resource R, target trust T accepts the normalized source tuple, no applicable explicit deny is present, and maximum-permission control M contains the capability. Changing only trust subject Q removes E2 while the intended subject retains it. All downstream edges use the derived session context and remain compatible in the same snapshot.

This is stronger than "the role can be assumed" because it preserves why the transition is effective and what would falsify it.

## Remediation checks

Choose the narrowest control that breaks the causal path while preserving required workflows.

Review candidate fixes across these categories:

1. **Grant scope:** narrow semantic action/resource scope rather than relying on a broad grant plus informal convention.
2. **Trust binding:** constrain issuer/source/subject/audience/context to the intended identity tuple.
3. **Maximum-permission control:** use an independent ceiling where architecture requires containment even if a positive policy later broadens.
4. **Explicit deny/organization guardrail:** apply only where provider semantics and governance model make this the reliable containment layer.
5. **Authority-changing separation:** restrict who can alter policy/trust/workload bindings that materially change future effective authority.
6. **Delegation binding:** preserve the initiating subject/source/resource/purpose when the managed service or privileged component is meant to act on behalf of that subject.
7. **Workload identity precision:** bind the complete intended workload selector/claims rather than a broader class of subjects.
8. **Resource-policy alignment:** ensure resource grants do not silently recreate a capability removed from identity policy.
9. **Session lifecycle:** define issue/expiry/revocation behavior and ensure the control is evaluated at the time semantics require.
10. **Audit correlation:** retain enough source principal, target identity/resource, session context, policy decision, and policy-change provenance to reconstruct authority transitions.

## Remediation proof

A remediation is proven by recomputing the causal path, not by visually inspecting the edited policy.

### 1. Rebuild the original edge records

Use the fixed snapshot and preserve the same semantic target capability. Determine which edge changed and why.

### 2. Identify the path-breaking control

Name the **path-breaking control** introduced or corrected by the remediation: narrowed trust condition, lower maximum-permission ceiling, removed grant, restored deny applicability, narrower resource scope, corrected workload selector, or another explicit invariant.

The proof should show that the original edge precondition is no longer satisfied or the effective decision is now denied/limited for the intended reason.

### 3. Preserve a neighboring path

An intended **neighboring path** should remain effective. This prevents a broad outage from being mistaken for least-privilege remediation.

### 4. Re-evaluate alternate policy sources

Check whether resource policy, inherited role, alternate trust mapping, workload binding, managed-service rule, or another reviewed policy layer reconstructs an equivalent edge to the same target capability.

### 5. Re-evaluate session context

If existing sessions can retain authority after policy change, record the provider's documented lifetime/revocation rule and verify the fixed-state expectation at the correct time/session boundary.

### 6. Reject overfit fixes

Do not accept proof that depends on one synthetic principal ID, one resource name, disabled functionality, hidden UI, changed error text, or a route-specific check that leaves the authoritative IAM relation unchanged.

### 7. State residual scope

Record what path families were recomputed and what remained outside the review. Precise residual scope is better evidence than an unsupported claim that "IAM is now secure."
