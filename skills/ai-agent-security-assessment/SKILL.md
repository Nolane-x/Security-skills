---
name: ai-agent-security-assessment
description: "Threat-model and test an AI agent or LLM application for prompt injection, tool abuse, data-flow boundary failures, excessive permissions, unsafe retrieval, cross-tenant leakage, and action confirmation gaps. Use for agents with tools, browsers, plugins, MCP/connectors, RAG, memory, or autonomous actions."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# AI Agent Security Assessment

Assess the agent as a system of trust boundaries, tools, data sources, and action policies rather than treating the model prompt as the only control.

See [the agent threat model](references/threat-model.md) for a reusable boundary checklist.

## When to use

Use for LLM applications that can read untrusted content, retrieve private data, call tools/APIs, browse, execute code, use plugins/MCP servers, remember state, or take actions.

## Preconditions

- Assessment environment is owned, local, sandboxed, benchmark/CTF, or explicitly authorized.
- Use synthetic accounts/data for adversarial testing when possible.
- Define which actions require confirmation and which resources should be unreachable.

## Workflow

1. Inventory principals: user, model, agent orchestrator, tools, connectors, remote content authors, memory, retrieval indexes, external services.
2. Map trust transitions for every data source and tool call.
3. Separate **instructions** from **untrusted content** in the model's effective context.
4. Review tool schemas and permissions for least privilege.
5. Test control classes with benign synthetic probes:
   - indirect prompt injection resistance;
   - tool-argument integrity;
   - data exfiltration boundaries using fake secrets/canaries;
   - cross-user/tenant separation using test identities;
   - confirmation before high-impact actions;
   - retrieval provenance and content trust;
   - memory poisoning boundaries;
   - plugin/MCP trust and permission changes.
6. Observe whether policy is enforced deterministically outside the model where high assurance is needed.
7. Add negative controls that should be allowed so the defense is not simply disabling functionality.
8. Route concrete boundary failures to evidence validation.
9. Recommend architectural controls before prompt-only mitigations.

Tool/benchmark families may include purpose-built agent security evaluations, prompt-injection test suites, and model red-team frameworks, but the assessment remains vendor-neutral.

## Evidence contract

A validated agent-security finding needs:

- exact trust boundary;
- untrusted input source;
- prohibited resource/action;
- deterministic or characterized reproduction;
- synthetic/non-sensitive proof data;
- control case;
- model/tool/orchestrator versions and policy configuration.

One surprising model response is not sufficient by itself.

## Stop conditions

Stop tests that would touch real secrets, send unintended external messages, create persistence, make purchases, damage data, or exceed the authorized test environment. Replace them with synthetic canaries or mocked tools.

## Output

Return a threat-boundary map and findings with source, crossed boundary, tool/action, proof signal, control, status, and architectural remediation.
