# Wave 10 AI Agent Causal Depth Design

## Status

Approved continuation of Wave 10 for `Nolane-x/Security-skills` on September 14, 2026.

## Problem

`ai-agent-security-assessment` already has strong system-level coverage, an operator runbook, and scenario enforcement, but its core reasoning contract still reflects the Wave 8 shape: inventory boundaries, generate hypotheses, run controlled validation, and capture evidence. Wave 10 requires a stricter causal model that prevents an agent from promoting a surprising model response, unsafe-looking tool proposal, or prompt-injection success into a stronger claim without proving the system transitions that actually crossed policy or authority boundaries.

## Goal

Deepen the existing skill without increasing the canonical skill count or changing routing semantics. The upgraded skill must force evidence-bounded reasoning across provenance, authority, policy, confirmation, execution, effect, persistence, and delegation, with explicit evidence ceilings and counterfactual controls.

## Non-goals

- Do not add offensive payload corpora, credential theft, persistence, destructive actions, malware, evasion, or live-target exploitation guidance.
- Do not copy Claude-Red prose or vendor-specific attack recipes.
- Do not change `skill.meta.json`, pack membership, routing domains, benchmark thresholds, or graph edges unless an independently justified contract change becomes necessary.
- Do not use line count or token count as a depth metric.

## Causal state model

Every high-confidence claim should be expressible as an observable chain:

`source -> provenance -> interpretation -> proposal -> authority -> policy -> confirmation -> execution -> effect -> persistence`

Each transition must be supported by observable artifacts or explicitly marked unknown. A model response is not a tool call; a tool proposal is not an accepted call; an accepted call is not proof of execution; execution is not proof of a prohibited effect; a transient effect is not proof of persistence.

## Authority-capability model

The skill must distinguish:

- initiating principal authority;
- model/orchestrator capability;
- tool capability;
- credential authority and scope;
- delegated authority;
- effective authority at the execution boundary;
- compound authority created by combining otherwise low-impact capabilities.

Claims such as privilege escalation or excessive agency require evidence that effective authority increased, or that an existing authority was exercised outside the initiating principal's allowed policy.

## Provenance continuity

Track trust labels and source identity through retrieval, summarization, memory writes, memory reads, tool results, connector responses, sub-agent handoffs, and context compression. Loss of provenance is a causal transition to analyze, not an automatic vulnerability conclusion.

## Decision/effect separation

Record distinct stages for model output, tool proposal, normalized arguments, policy decision, confirmation state, credential identity, execution acceptance, controlled sink result, and final boundary consequence. The evidence ceiling is set by the strongest stage actually demonstrated.

## Persistence and delegation

Persistent-state findings must separate transient influence, write acceptance, storage identity, provenance retention, later retrieval, expiry/cleanup, and later consequence. Delegation findings must record the initiating principal, delegated task, authority before/after, credential used, re-authorization point, and bounded consequence.

## Evidence ladder

- `A0` — suspicious or policy-relevant model output only.
- `A1` — policy-relevant proposal or transformed argument observed.
- `A2` — policy/confirmation decision divergence demonstrated under pinned configuration.
- `A3` — prohibited synthetic capability accepted by a controlled execution boundary.
- `A4` — prohibited bounded effect demonstrated in an inert/synthetic sink.
- `A5` — persistent or delegated consequence causally demonstrated across a later state transition.

A case may stop at any level. Missing causal links lower the evidence ceiling.

## Counterfactual discipline

For validated claims, remove or neutralize one causal variable while preserving neighboring state: untrusted content, provenance label, tenant identity, authority, confirmation tuple, tool availability, memory write, or delegation edge. The prohibited synthetic effect must disappear. Preserve a neighboring allowed control to prove the harness still functions.

## Scenario contract extension

Keep the existing Wave 8 scenario fields and deepen each AI-agent scenario with string fields:

- `provenance_trace`
- `authority_capability_profile`
- `decision_effect_trace`
- `persistence_trace`
- `delegation_trace`
- `counterfactual_control`
- `alternative_explanation`
- `evidence_ceiling`
- `neighbor_regression`

Fields that are not applicable must say why they are not applicable and what boundary would make them relevant; they may not be empty.

## TDD contract

Add `tests/test_ai_agent_security_depth.py` before modifying production skill artifacts. The RED state must fail because the Wave 10 sections/phrases/scenario fields are absent. GREEN requires the canonical skill, operator runbook, and all three scenario records to satisfy the new reasoning contract while preserving the existing operator-depth validator and repository-wide completion gate.

## Completion criteria

1. Dedicated depth test is GREEN.
2. Existing operator-depth validation remains GREEN.
3. Full unit-test discovery is GREEN.
4. All repository validation/build/benchmark/evaluation commands in `AGENTS.md` remain GREEN.
5. No canonical skill count, pack count, graph edge, routing domain, benchmark threshold, or oracle is weakened.
6. PR CI is green before merge; post-merge `main` is rechecked separately.
