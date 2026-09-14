# AI Agent Security Operator Runbook

Use this runbook only for local, owned, sandboxed, benchmark/CTF, or explicitly authorized systems. Prefer synthetic identities, fake secrets, inert action sinks, mocked external services, controlled retrieval indexes, and disposable memory stores. Do not use real secrets, real purchases, production writes, persistence deployment, or destructive actions as proof material.

The objective is not to make a model say something surprising. The objective is to prove or falsify a bounded causal claim about how untrusted influence crosses a concrete policy, identity, authority, data, action, persistence, or delegation boundary.

## Attack surface

Build the system as a graph of principals, sources, transformations, decision points, capabilities, credentials, stores, and sinks.

### Principals and authority holders

Inventory at least:

- end users and tenant identities;
- system/developer instruction authors;
- model/runtime identity;
- orchestrator and planner;
- browser, code, shell, file, database, messaging, and workflow tools;
- plugins, MCP servers, connectors, and remote APIs;
- sub-agents and delegated workers;
- retrieval indexes, memory stores, and summarizers;
- background jobs and scheduled actions;
- service accounts, OAuth applications, API credentials, and delegated identities.

For each principal, record authentication identity, tenant, scopes/roles, readable and writable state, network reach, and whether another component can cause it to act.

### Instruction and data boundaries

Map every source that can enter the effective context: direct user messages, system/developer instructions, webpages, search results, email, documents, PDFs, issue bodies, comments, code repositories, RAG chunks, connector responses, tool outputs, long-term memory, summaries, and delegated-agent artifacts.

Classify each source as trusted instruction, trusted data, untrusted data, or mixed/ambiguous. Record source provenance, tenant/ACL context, transformation history, and whether the policy layer can still see those attributes after processing.

### Capability and state surfaces

For each tool or action, record its schema, normalized arguments, read/write effects, target namespace, credential authority, confirmation requirements, rate/quantity bounds, egress behavior, audit events, rollback semantics, and effective authority at execution time.

Pay special attention to compound authority. Two individually low-risk capabilities can become high-impact when chained, such as private-data read plus external-send, or persistent-memory write plus later privileged automation.

Record persistence surfaces separately: memory writes, profile/preference stores, vector indexes, generated files re-read later, scheduled tasks, connector-side records, cached summaries, and agent-to-agent handoff artifacts.

## Hypothesis matrix

Express every hypothesis as a falsifiable path with an expected policy and evidence ceiling.

| Hypothesis class | Source | Boundary | Required causal proof | Safe oracle |
| --- | --- | --- | --- | --- |
| indirect instruction following | controlled untrusted document/web content | data vs instruction | source provenance survives to the decision point and the untrusted influence changes a prohibited proposal/decision | inert marked action proposal or sink event |
| tool-argument integrity | user/content-derived value | proposal -> execution | normalized arguments cross a policy boundary under the pinned identity | mocked tool records bounded synthetic arguments |
| excessive agency | benign user task | principal authority -> effective authority | execution uses authority outside the initiating principal's allowed policy | inert high-impact action sink |
| confirmation bypass | controlled request/content | confirmation -> execution | executed normalized tuple differs from the confirmed tuple or confirmation is absent where required | controlled tuple-comparison sink |
| data isolation | tenant A synthetic data | tenant binding -> tenant B observation | wrong identity/ACL state reaches the protected read boundary | synthetic canary visible only to test identities |
| RAG trust confusion | adversarial synthetic chunk | retrieval provenance -> policy | untrusted data is reclassified or loses provenance before a prohibited decision | controlled retrieval and policy trace |
| memory poisoning | synthetic persistent note | write -> later retrieval -> later effect | a persistent write is stored, later retrieval occurs, and the later effect tracks that stored state | disposable memory store and inert sink |
| connector scope drift | bounded connector fixture | credential/resource scope -> execution | normalized target escapes the configured synthetic scope and is accepted | mock connector resource set |
| delegation escalation | lower-authority parent | delegation -> child effective authority | child effective authority exceeds parent-authorized policy without valid re-authorization | inert delegated action sink |
| output-to-execution confusion | model text | data -> executable control | downstream parser/executor interprets data as actionable control | no-op executor fixture |

If expected behavior cannot be established from owner-approved requirements, configuration, or tests, classify the case as `needs-policy` rather than a vulnerability.

## Causal decision trace

For every candidate finding, preserve an observable transition trace:

```text
source
  -> source provenance
  -> interpretation role
  -> proposal
  -> normalized arguments
  -> initiating-principal authority
  -> credential/delegated/effective authority
  -> policy decision
  -> confirmation state
  -> execution acceptance/result
  -> bounded effect
  -> persistence or delegation consequence
```

A later node cannot be inferred from an earlier one. Model text is not tool execution. A tool proposal is not acceptance. Acceptance is not a prohibited effect. A transient effect is not persistence.

For every transition record the observable artifact that proves it, the component that produced it, the pinned revision/configuration, and the strongest conclusion that still remains justified if the next transition is unknown.

## Authority-capability matrix

Build one matrix per high-impact path.

| Component | Identity/principal | Capability | Credential/scope | Policy boundary | Confirmation | Effective authority |
| --- | --- | --- | --- | --- | --- | --- |
| initiating user/workflow | pinned synthetic identity | requested task | user/tenant policy | request admission | task-specific if required | authority allowed to initiate |
| model/orchestrator | runtime + orchestrator revision | propose/sequence actions | normally no direct credential | planning/action policy | proposal may require confirmation | proposal capability only |
| tool/connector | exact tool identity/version | read/write/action surface | service/OAuth/API scope | execution-time authorization | bound to normalized tuple where required | authority actually exercisable |
| delegated worker | child identity/runtime | delegated task subset | child credential/delegation token | delegation and re-authorization | independent confirmation where required | post-delegation authority |

Separate nominal capability from effective authority. A powerful tool does not prove excessive agency. A child with broader nominal capability does not prove escalation unless the initiating principal can causally exercise that broader authority without legitimate re-authorization.

Record compound authority explicitly when two or more paths compose into a stronger consequence. Then test whether policy is applied to the composition rather than only to each isolated tool.

## Provenance continuity

Track source provenance through every transformation that can affect security meaning:

- retrieval ranking, filtering, and cross-index joins;
- parsing, OCR, transcription, metadata extraction, and chunking;
- summarization and context compression;
- memory write, roll-up, expiry, and later retrieval;
- tool stdout/stderr and structured output normalization;
- connector/plugin/MCP result wrapping;
- sub-agent task packaging and returned artifacts.

At each hop, record source identity, trust label, tenant/ACL binding, transformation history, and whether the downstream policy layer receives that metadata. If provenance is lost, mark the exact hop and lower the evidence ceiling until a causal link from that loss to a prohibited decision/effect is demonstrated.

Do not treat a model's apparent awareness of source trust as equivalent to deterministic provenance enforcement.

## Controlled validation

Use staged experiments so one boundary changes at a time.

1. **Freeze the environment.** Capture model/runtime, orchestrator revision, enabled tools, policy revision, connector/tool versions, credential identities/scopes, retrieval index revision, memory state, tenant identities, and delegated-agent configuration.
2. **Create synthetic assets.** Use unique canaries, fake tenant records, mock inboxes, inert files, disposable memory/index entries, and no-op action sinks.
3. **Establish a neighboring allowed control.** Run an intended task that should succeed and preserve its trace. This proves the harness is not simply blocking all functionality.
4. **Establish the denied baseline.** Directly request the synthetic prohibited operation using the same identity and confirm the expected deterministic denial where policy requires it.
5. **Introduce one untrusted influence channel.** Use exactly one controlled source: fixture document, mock webpage, RAG chunk, memory entry, tool result, connector response, or delegated-agent output.
6. **Capture the causal decision trace.** Preserve source provenance, interpretation role, proposal, normalized arguments, authority-capability state, policy decision, confirmation state, credential identity, execution result, and bounded effect.
7. **Repeat only to characterize variance.** Vary formatting, source location, retrieval position, context length, memory state, or delegation topology one factor at a time.
8. **Test persistence separately.** Demonstrate persistent write, then start a clean synthetic session, demonstrate later retrieval, and only then test a later inert effect. Remove the fixture afterward.
9. **Test delegation separately.** Record parent authority, delegated task, child authority before/after, credential used, and re-authorization point before claiming delegation escalation.
10. **Bound the consequence.** Stop at the highest directly observed transition and state the evidence ceiling.

For high-impact actions, success must mean only that the controlled sink would have allowed the synthetic operation. Never send real messages, make purchases, delete real data, create real persistence, or expose real secrets.

## Persistence and delegation

Treat persistence and delegation as separate causal dimensions, not as extensions automatically implied by prompt influence.

### Persistence trace

Require the sequence:

```text
transient influence -> proposed persistent write -> accepted persistent write -> stored state identity/provenance -> later retrieval -> later interpretation -> later policy/action decision -> bounded later effect
```

A persistent write alone does not prove later retrieval. Later retrieval does not prove later policy influence. A later unsafe-looking model response does not prove a prohibited effect. Record expiry, tenant binding, cleanup behavior, and provenance retention at each state transition.

### Delegation trace

For every delegation edge record:

- initiating principal;
- parent agent authority and capability;
- exact delegated task;
- child identity/runtime;
- child authority before and after delegation;
- credential or delegation token used;
- policy and re-authorization point;
- normalized delegated arguments/target;
- controlled execution result and bounded effect.

A delegation flaw is demonstrated only when authority or policy outcome differs in a way the initiating principal was not authorized to cause, and the difference disappears when the suspect delegation variable is removed.

## False-positive controls

Use paired controls that discriminate the causal explanation from harness or configuration artifacts:

- clean-content control: same task/resource with the untrusted instruction removed;
- trusted-instruction control: equivalent instruction delivered through an approved control channel;
- same-tenant/cross-tenant pair using synthetic records;
- exact-confirmation versus one-field-changed normalized tuple;
- tool-disabled control separating model text from tool-boundary behavior;
- policy-enforced versus prompt-only sandbox configuration;
- retrieval near-neighbor with equivalent relevance but no adversarial instruction;
- transient-context versus accepted persistent write;
- credential identity pair with intentionally different synthetic permissions;
- equal-authority delegation versus asymmetric-authority delegation.

Reject or downgrade cases explained by stale fixture state, retrieval contamination, mismatched revisions, malformed mocked-tool semantics, wrong credential/tenant binding, hidden test state, intended delegation, or an undocumented policy assumption.

## Counterfactual boundary proof

A validated causal claim requires at least one counterfactual that removes or neutralizes the suspected cause while preserving neighboring state.

Examples include removing the untrusted instruction but preserving document content; retaining the retrieved chunk while correcting its provenance label; keeping the proposed action while changing to the authorized credential; binding confirmation to the exact normalized tuple; disabling only the memory write while preserving transient context; or removing only the privileged delegation edge.

The prohibited synthetic effect must disappear, while a neighboring allowed control still succeeds. If the effect survives, investigate an alternative explanation and lower the claim instead of changing the counterfactual until it produces the expected result.

## Evidence capture

Preserve a compact machine-readable or machine-derived ledger:

```text
case_id:
environment_revision:
model_runtime:
orchestrator_revision:
policy_revision:
principal_and_tenant:
source:
source_provenance:
interpretation_role:
hypothesis:
expected_policy:
proposal:
normalized_arguments:
authority_capability_profile:
credential_identity_and_scope:
delegated_authority:
effective_authority:
compound_authority:
policy_decision:
confirmation_state:
execution_result:
bounded_effect:
persistent_write:
later_retrieval:
delegation_trace:
counterfactual_control:
neighboring_allowed_control:
alternative_explanations_tested:
repeat_count_and_variance:
evidence_level:
evidence_ceiling:
```

Prefer machine-captured traces over screenshots or prose recollection. Do not request or store hidden chain-of-thought. Observable inputs, provenance, decisions, tool calls, policy outcomes, identities, state transitions, and outputs are sufficient evidence.

## Evidence ceiling

Use the A0-A5 ladder from the canonical skill and stop at the strongest completed causal stage.

- A0: suspicious/policy-relevant model output only.
- A1: policy-relevant proposal, normalized argument change, retrieval decision, or memory-write proposal observed.
- A2: policy or confirmation decision divergence demonstrated.
- A3: prohibited synthetic capability accepted at the controlled execution boundary.
- A4: prohibited bounded effect observed at the inert sink/protected fixture.
- A5: persistent or delegated consequence demonstrated across a later state/delegation transition.

Do not promote from model text to execution, from acceptance to prohibited effect, from current-turn effect to persistence, or from nominal child capability to delegation escalation without direct evidence for the missing transitions.

## Remediation checks

Prefer architectural enforcement over prompt-only wording changes.

Evaluate remediation across capability reduction, deterministic policy, instruction/data separation, tool argument validation, tenant-bound retrieval, memory governance, delegation controls, confirmation tuple binding, egress controls, and auditability.

A fix is incomplete if it merely causes the model to refuse while the execution boundary still accepts the prohibited synthetic operation, or if it disables intended neighboring behavior.

## Remediation proof

Replay the exact original synthetic failing fixture on the fixed revision and require the causal break at the intended invariant. Then replay:

1. the neighboring allowed control, which must still succeed;
2. the neighboring denied control, which must still be denied;
3. the relevant persistence or delegation control when those dimensions were part of the claim;
4. the same pinned identity, credential, policy, tool schema, retrieval/memory state shape, and normalized action semantics unless the remediation intentionally changes one of them.

Record the post-remediation causal trace and the new evidence ceiling. A remediation is `regression-verified` only when the failing path no longer reaches the prohibited effect and intended neighboring behavior remains functional.
