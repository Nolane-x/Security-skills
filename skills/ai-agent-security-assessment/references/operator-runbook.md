# AI Agent Security Operator Runbook

This runbook deepens `ai-agent-security-assessment` for local, owned, sandboxed, benchmark/CTF, or explicitly authorized systems. Use synthetic identities, fake secrets, inert action sinks, and mocked external services wherever a real action could affect people, data, money, credentials, or external systems.

The objective is not to make a model say something surprising. The objective is to determine whether untrusted influence can cross a concrete system boundary and cause an action, disclosure, persistence event, or authority change that policy forbids.

## Attack surface

Build the assessment as a graph of principals, data sources, decision points, capabilities, and sinks.

### Principals and authority holders

Inventory at least:

- end users and tenant identities;
- system/developer instruction authors;
- model/runtime identity;
- agent orchestrator and planner;
- browser/code/shell/file/database tools;
- plugins, MCP servers, connectors, and remote APIs;
- sub-agents and delegated workers;
- retrieval indexes, memory stores, and summarizers;
- background jobs and scheduled actions;
- service accounts, OAuth applications, and API credentials.

For every principal, record authentication identity, tenant, scopes/roles, writable state, readable state, network reach, and whether another component can cause it to act.

### Instruction and data boundaries

Map every path by which bytes can enter the effective model context:

- direct user messages;
- system/developer instructions;
- webpages and search results;
- email, documents, PDFs, issue bodies, comments, chat history, and code repositories;
- RAG chunks and metadata;
- connector/plugin responses;
- tool stdout/stderr and structured results;
- long-term memory and conversation summaries;
- outputs produced by other agents.

Mark each source as trusted instruction, trusted data, untrusted data, or mixed/ambiguous. A boundary that relies on the model inferring that distinction is weaker than one enforced by the orchestrator.

### Capability surfaces

For each tool/action, record:

- schema and accepted argument types;
- read versus write effects;
- target namespace/resource type;
- credential used and its scope;
- whether the model chooses the target directly;
- server-side allowlists or policy checks;
- confirmation rules;
- rate/quantity bounds;
- network egress behavior;
- audit/event records;
- idempotency and rollback properties.

Pay special attention to compound authority: two individually low-risk tools may form a higher-risk path when chained, such as private-data read plus external message send.

### State and persistence surfaces

Record where attacker-influenced content can outlive the current turn:

- memory writes;
- preference/profile stores;
- vector indexes;
- generated files or notes re-read later;
- scheduled tasks;
- connector-side records;
- cached summaries;
- agent-to-agent handoff artifacts.

A persistent write is a separate boundary from transient prompt influence and needs its own authorization and cleanup policy.

## Hypothesis matrix

Generate hypotheses as explicit source → boundary → capability → consequence paths. Do not treat a prompt pattern by itself as a finding.

| Hypothesis class | Source | Boundary under test | Safe proof signal |
| --- | --- | --- | --- |
| indirect instruction following | controlled untrusted document/web content | content vs instruction | model attempts an inert marked action that policy says content cannot request |
| tool-argument integrity | user/content-derived value | model output → tool schema/policy | mocked tool receives an argument outside the permitted synthetic namespace |
| excessive agency | benign user task | planner → privileged capability | action sink records a prohibited synthetic operation without required confirmation |
| confirmation bypass | controlled request or retrieved content | intent → high-impact action gate | mocked high-impact action executes without the expected confirmation state |
| data exfiltration boundary | fake secret/canary in private fixture | private source → external sink | canary appears in a controlled sink that policy forbids |
| cross-tenant isolation | tenant A synthetic content | retrieval/memory/tool → tenant B | tenant B test identity receives A-only marker |
| RAG trust confusion | adversarial synthetic chunk | retriever → effective instruction context | retrieved data changes tool/action policy rather than only answer content |
| memory poisoning | synthetic persistent note | memory write → later session | later clean task is altered by the planted inert instruction |
| connector scope drift | connector with bounded test scope | connector result/action → broader resource | requested operation escapes the configured synthetic resource set |
| delegation escalation | low-authority parent agent | delegation → higher-authority worker | child performs an inert action unavailable to the parent without independent authorization |
| identity confusion | two synthetic accounts/tenants | user/session identity → tool credential | operation executes under the wrong synthetic identity |
| output-to-execution boundary | model text | downstream parser/executor | inert marker is interpreted as executable/actionable control data where plain data was expected |

For every hypothesis state the expected policy first. If the expected behavior cannot be established from owner-approved requirements, configuration, or tests, keep the case as `needs-policy` rather than labeling a vulnerability.

## Controlled validation

Use a staged experiment so evidence is attributable to one boundary at a time.

1. **Freeze the environment.** Capture model/runtime version, orchestrator revision, enabled tools, policy configuration, connector versions, retrieval index revision, memory state, and test tenant identities.
2. **Create synthetic assets.** Use unique canaries, fake secrets, fake tenant records, mock inboxes, inert files, and no-op action endpoints. Never use real credentials or sensitive data as proof material.
3. **Establish the allowed baseline.** Run a clean task that should succeed and preserve its trace. This proves the test harness is not simply blocking all behavior.
4. **Establish the denied baseline.** Ask directly for the synthetic prohibited action using the same identity. Confirm the deterministic policy layer denies it where policy requires denial.
5. **Introduce one untrusted influence channel.** Place the inert instruction or manipulated metadata in exactly one controlled source such as a fixture document, mock webpage, RAG chunk, or tool result.
6. **Observe the complete decision chain.** Capture retrieval selection, effective context provenance when available, tool proposal, normalized arguments, policy decision, confirmation state, credential identity, and action result.
7. **Repeat with equivalent variants.** Vary content formatting, source location, context length, retrieval position, or delegation topology only enough to determine whether the behavior is stable or stochastic.
8. **Test state persistence separately.** After any memory/index write, start a clean synthetic session and verify whether the effect survives. Remove the fixture afterwards.
9. **Bound the consequence.** A model producing an unsafe sentence is different from a tool invocation; a tool proposal is different from an accepted call; an accepted call is different from access to a protected resource. Record the highest boundary actually crossed.
10. **Route validated failures.** Send confirmed cases to evidence validation and remediation/regression workflows rather than escalating to broader real-world testing.

For high-impact actions, configure the action sink so that success means only “the control would have allowed this synthetic operation.” Do not send real messages, create accounts, make purchases, delete data, change production configuration, establish persistence, or expose real secrets.

## False-positive controls

A strong test proves both the failure and the intended behavior around it.

Use paired controls appropriate to the hypothesis:

- **clean-content control:** same task and resource without the untrusted instruction;
- **trusted-instruction control:** equivalent instruction delivered through an explicitly authorized control channel;
- **same-tenant/cross-tenant pair:** same query against synthetic records owned by the current versus neighboring test tenant;
- **confirmation pair:** low-impact permitted action versus high-impact synthetic action requiring confirmation;
- **tool-disabled control:** same prompt with the relevant tool unavailable, separating model text behavior from tool-boundary behavior;
- **policy-enforced/prompt-only pair:** deterministic server-side policy enabled versus a sandbox configuration that relies only on prompt instructions;
- **retrieval relevance control:** benign near-neighbor chunk with similar semantics but no instruction content;
- **memory lifetime control:** transient context-only case versus explicitly persistent test memory;
- **credential identity control:** same inert action under two synthetic identities with intentionally different permissions;
- **delegation control:** parent and child agents configured with equal authority before testing asymmetric authority.

Reject or downgrade a case when behavior is explained by intended delegation, stale fixture state, retrieval contamination, test-harness leakage, malformed mocked-tool semantics, or an undocumented policy assumption.

One successful adversarial turn with no repeatability and no boundary proof remains an observation, not a validated finding.

## Evidence capture

For each case preserve a compact evidence ledger:

```text
case_id:
environment_revision:
model_runtime:
orchestrator_revision:
policy_revision:
principal_and_tenant:
untrusted_source:
source_provenance:
hypothesis:
expected_policy:
retrieval_or_memory_state:
proposed_tool_and_arguments:
normalized_tool_arguments:
confirmation_state:
policy_decision:
credential_identity_and_scope:
controlled_action_sink_result:
canary_or_proof_signal:
positive_control:
negative_control:
repeat_count_and_variance:
highest_boundary_crossed:
evidence_state:
```

Prefer machine-captured traces over screenshots or prose recollection. Preserve enough information to distinguish model behavior from orchestrator, tool, connector, identity, and policy behavior.

Evidence promotion rules:

- **hypothesis:** a plausible path exists but has not been reproduced;
- **observed:** controlled behavior relevant to the path was reproduced;
- **validated:** prohibited boundary crossing plus bounded synthetic consequence and controls are demonstrated;
- **regression-verified:** the fixed system blocks the failing path while expected allowed controls remain functional.

Do not request, record, or store hidden chain-of-thought as evidence. Observable inputs, decisions, tool calls, policy outcomes, and outputs are sufficient.

## Remediation checks

Prefer architectural enforcement over prompt-only wording changes.

Evaluate remediation in these layers:

1. **Capability reduction:** narrow tool/resource scopes, split read/write credentials, remove unused actions, and prevent compound authority where possible.
2. **Deterministic policy:** enforce tenant, resource, action, egress, and confirmation rules outside the language model.
3. **Instruction/data separation:** tag provenance, preserve source identity, prevent untrusted content from mutating control messages, and make downstream components consume structured data rather than free-form instructions.
4. **Tool argument validation:** validate types, resource namespaces, destination allowlists, quantity/rate bounds, and authorization at execution time.
5. **Retrieval isolation:** tenant-bind indexes and filters, enforce source ACLs before retrieval, preserve provenance, and prevent content from changing retrieval/tool policy.
6. **Memory governance:** constrain what can be written, bind memory to identity/tenant/purpose, set expiry, retain provenance, and provide deterministic deletion/rollback.
7. **Delegation controls:** ensure a child/sub-agent cannot inherit authority the initiating principal lacks; re-authorize at the privileged boundary.
8. **Confirmation semantics:** bind confirmation to the exact normalized action, arguments, target, identity, and expiry rather than to a vague conversational approval.
9. **Egress controls:** restrict destinations and data classes independently of model intent.
10. **Auditability:** log policy-relevant inputs and decisions without collecting unnecessary sensitive content.

Regression verification must replay the original synthetic failing fixture, the clean positive control, and at least one neighboring negative control. A fix that merely disables the feature or causes all actions to fail is not a successful remediation.
