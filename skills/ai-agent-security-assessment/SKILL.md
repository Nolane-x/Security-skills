---
name: ai-agent-security-assessment
description: "Threat-model and test an AI agent or LLM application for prompt injection, tool abuse, data-flow boundary failures, excessive permissions, unsafe retrieval, cross-tenant leakage, and action confirmation gaps. Use for agents with tools, browsers, plugins, MCP/connectors, RAG, memory, or autonomous actions."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# AI Agent Security Assessment

Assess the agent as a system of trust boundaries, principals, data sources, policy decisions, capabilities, and observable effects rather than treating the model prompt as the only control.

See [the agent threat model](references/threat-model.md) for a reusable boundary checklist.

## When to use

Use for LLM applications that can read untrusted content, retrieve private data, call tools/APIs, browse, execute code, use plugins/MCP servers, remember state, delegate work, or take actions.

## Preconditions

- Assessment environment is owned, local, sandboxed, benchmark/CTF, or explicitly authorized.
- Use synthetic accounts/data for adversarial testing when possible.
- Define which actions require confirmation and which resources should be unreachable.
- Pin the model/runtime, orchestrator revision, tool and connector configuration, policy revision, credential identity, memory/retrieval state, and relevant tenant identities before promoting evidence.
- Define a harmless observable oracle before testing any stronger action, disclosure, persistence, or authority claim.

## Causal security state model

Reason through the complete observable chain before assigning impact:

```text
source -> provenance -> interpretation -> proposal -> authority -> policy -> confirmation -> execution -> effect -> persistence
```

Treat each transition as an independent claim boundary.

1. **Source.** Identify the user, document, webpage, retrieval chunk, tool result, connector response, memory record, or delegated-agent output that supplied the relevant bytes or state.
2. **Provenance.** Record source identity, trust label, tenant, ACL context, and transformation history. Unknown or lost provenance lowers the evidence ceiling.
3. **Interpretation.** Record the observable semantic role assigned by the application: data, instruction, tool result, memory, policy metadata, or ambiguous mixed context. Do not infer hidden reasoning.
4. **Proposal.** Capture the model-visible or orchestrator-visible proposed operation, including normalized arguments where available.
5. **Authority.** Determine which initiating principal, credential authority, delegated authority, tool capability, and effective authority could authorize the proposed operation.
6. **Policy.** Capture the deterministic or configured policy decision that applies to the normalized proposal, target, identity, and resource.
7. **Confirmation.** Record confirmation state and whether confirmation is bound to the exact normalized action tuple rather than a vague conversational approval.
8. **Execution.** Distinguish a proposed call, accepted call, rejected call, simulated call, and actual controlled execution.
9. **Effect.** Measure the bounded synthetic consequence at the controlled sink or protected resource boundary.
10. **Persistence.** Determine whether the effect is only transient or survives through a later write/read, retrieval, summarization, scheduled action, or delegated workflow.

A surprising model response does not prove tool use. A tool proposal does not prove acceptance. Acceptance does not prove execution. Execution does not prove a prohibited effect. A transient effect does not prove persistence.

## Authority-capability model

Separate authority from capability. The existence of a powerful tool is not itself proof that the initiating principal can cause it to exercise that power outside policy.

Record independently:

- **initiating principal authority:** the user, tenant, service, or workflow authority that started the task;
- **model/orchestrator capability:** what the planner can propose or sequence;
- **tool capability:** which read/write/action surface the tool exposes;
- **credential authority:** the credential, service account, OAuth grant, connector token, or delegated identity used at execution time and its scope;
- **delegated authority:** authority assigned to a child/sub-agent or downstream worker and whether the delegation is narrower, equal, or broader;
- **effective authority:** the actual authority available at the execution boundary after policy, credential, target, and delegation constraints are composed;
- **compound authority:** a stronger path created by chaining individually low-impact capabilities, such as a private-data read plus an external-send capability.

Do not label a path privilege escalation merely because a child agent or tool is powerful. Demonstrate either an increase in effective authority relative to the initiating principal or an exercise of existing authority outside the initiating principal's allowed policy.

## Provenance continuity

Preserve source provenance across every transformation that can change security meaning:

- retrieval selection and ranking;
- chunking, parsing, OCR, transcription, and metadata extraction;
- summarization and context compression;
- RAG joins and cross-index composition;
- memory writes, later retrieval, roll-up, and expiry;
- tool stdout/stderr and structured results;
- connector/plugin/MCP responses;
- agent-to-agent handoff and delegated task packaging.

At each transition record whether source identity, trust label, tenant binding, ACL context, and transformation history remain available to the policy layer. Provenance loss is a fact to investigate, not automatic proof of a vulnerability. A validated boundary failure requires evidence that the loss or misclassification contributed causally to a prohibited proposal, decision, execution, or effect.

## Workflow

1. Inventory principals: user, model, agent orchestrator, tools, connectors, remote content authors, memory, retrieval indexes, external services, and delegated workers.
2. Map trust transitions for every data source and tool call using the causal security state model.
3. Separate **instructions** from **untrusted content** in the model's effective context and track source provenance through transformations.
4. Build the authority-capability profile for each high-impact path, including credential authority, delegated authority, effective authority, and compound authority.
5. Review tool schemas and permissions for least privilege and confirm that normalized arguments are policy-checked at execution time.
6. Test control classes with benign synthetic probes:
   - indirect prompt injection resistance;
   - tool-argument integrity;
   - data disclosure boundaries using fake secrets/canaries;
   - cross-user/tenant separation using test identities;
   - confirmation before high-impact actions;
   - retrieval provenance and content trust;
   - memory write/read isolation;
   - plugin/MCP trust and permission changes;
   - delegation and re-authorization boundaries.
7. Capture the complete observable decision trace: source provenance, proposal, normalized arguments, effective authority, policy decision, confirmation state, credential identity, execution result, and bounded effect.
8. Separate transient behavior from persistent write, later retrieval, scheduled execution, or delegated consequence.
9. Run a counterfactual control that neutralizes one causal variable while preserving neighboring state.
10. Test alternative explanations including stale fixture state, target/config mismatch, harness leakage, retrieval contamination, malformed mock semantics, wrong identity binding, or intended delegation.
11. Route concrete boundary failures to evidence validation and remediation/regression workflows.
12. Recommend architectural controls before prompt-only mitigations.

Tool/benchmark families may include purpose-built agent security evaluations, prompt-injection test suites, and model red-team frameworks, but the assessment remains vendor-neutral and evidence-first.

## Operator depth

For a full authorized assessment, load the [operator runbook](references/operator-runbook.md). It expands this skill into transition-level causal reasoning across provenance, authority/capability composition, RAG, memory, tools, connectors/MCP, delegation, confirmation, tenant identity, controlled synthetic validation, false-positive controls, evidence ceilings, and regression checks without relying on real secrets or destructive actions.

## Evidence contract

A validated agent-security finding needs:

- exact trust boundary and expected policy;
- pinned model/runtime, orchestrator, policy, tool/connector, credential, tenant, retrieval, and memory configuration;
- untrusted input source plus source provenance;
- prohibited resource/action or state transition;
- transition-level trace from proposal through normalized arguments, policy decision, confirmation state, execution, and bounded effect;
- initiating-principal, credential, delegated, and effective authority profile;
- deterministic or characterized reproduction;
- synthetic/non-sensitive proof data;
- a causal counterfactual plus neighboring safe control;
- alternative explanations considered and bounded;
- explicit evidence level and evidence ceiling.

One surprising model response, one unsafe-looking completion, one tool proposal, or one permissive-looking configuration is not sufficient by itself.

## Evidence ladder

- **A0 — suspicious output:** a model response or retrieved/generated text is policy-relevant, but no tool or boundary transition is demonstrated.
- **A1 — proposal observed:** a policy-relevant tool/action proposal, normalized argument change, retrieval decision, or memory-write proposal is directly observed.
- **A2 — decision divergence demonstrated:** the pinned policy or confirmation layer makes a decision inconsistent with the stated boundary for the normalized action tuple.
- **A3 — prohibited synthetic capability accepted:** a controlled execution boundary accepts the prohibited synthetic operation under the pinned identity and authority state.
- **A4 — prohibited bounded effect demonstrated:** an inert sink or synthetic protected resource shows the policy-forbidden effect caused by the accepted operation.
- **A5 — persistent or delegated consequence demonstrated:** the bounded effect survives a later persistence transition or crosses a delegation edge with causal evidence and re-authorization state recorded.

Evidence may stop at any level. A precise A1 or A2 result with a clear ceiling is stronger than a speculative A4/A5 claim.

## Evidence ceiling

The evidence ceiling is the strongest conclusion justified by the complete observable chain.

- Model text alone supports at most a model-output claim.
- A tool proposal without policy acceptance supports at most A1.
- A policy or confirmation anomaly without controlled acceptance supports at most A2.
- Accepted execution without an observed prohibited sink/resource effect supports at most A3.
- A bounded effect in the current session does not prove persistence, future retrieval, or delegated propagation.
- A persistent write does not prove later retrieval; later retrieval does not prove a later prohibited effect.
- A child agent with broader nominal capability does not prove delegated privilege escalation unless effective authority and re-authorization behavior are demonstrated.
- Evidence from a different model, policy revision, credential, tenant, tool schema, connector version, retrieval index, or memory state does not transfer automatically.
- Unknown transitions remain unknown. State exactly which observable artifact would be required to raise the ceiling.

## Counterfactual discipline

A positive result is causal only when the prohibited synthetic effect tracks the suspected security transition.

Hold neighboring state constant and remove or neutralize one variable such as the untrusted content, provenance label, tenant identity, credential authority, delegated authority, confirmation state, tool availability, memory write, retrieval selection, or delegation edge. The claimed prohibited effect must disappear while a neighboring allowed control still succeeds.

If the effect survives the counterfactual, downgrade the claim and investigate an alternative explanation rather than promoting impact.

## Stop conditions

Stop tests that would touch real secrets, send unintended external messages, create persistence on real systems, make purchases, damage data, alter production configuration, or exceed the authorized test environment. Replace them with synthetic canaries, mocked tools, inert action sinks, controlled fixtures, or read-only evidence.

Stop impact promotion when the next step depends on hidden reasoning, guessed authority, unverified tenant/credential state, ambiguous provenance, unpinned configuration, or a real-world side effect outside the synthetic boundary.

## Output

```text
case_id:
target_and_configuration:
expected_policy:
initiating_principal:
source_and_source_provenance:
interpretation_boundary:
proposed_action:
normalized_arguments:
authority_capability_profile:
credential_authority:
delegated_authority:
effective_authority:
compound_authority:
policy_decision:
confirmation_state:
execution_result:
bounded_effect:
transient_or_persistent_state:
persistence_trace:
delegation_trace:
counterfactual_control:
neighboring_safe_control:
alternative_explanations_tested:
evidence_level:
evidence_ceiling:
remediation_invariant:
post_remediation_oracle:
```
