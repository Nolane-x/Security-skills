# Wave 10 Prompt Injection Boundary Depth Design

## Goal

Promote `prompt-injection-boundary-analysis` from a concise checklist into a CI-enforced operator-depth profile that proves instruction-boundary failures through observable authority, transformation, decision, and effect transitions rather than by payload novelty or surprising model text.

## Scope

This phase changes only the prompt-injection skill, its new local references, the operator-depth profile registry, dedicated depth tests, and documentation that enumerates registered depth profiles. It does not change routing domains, graph edges, packs, benchmark thresholds, benchmark fixtures, or agent-evaluation oracles.

## Security model

Treat prompt injection as a provenance-and-authority failure across a transformation pipeline:

`source -> provenance label -> transform -> effective context -> interpreted authority -> decision -> policy gate -> proposed capability -> accepted capability -> bounded effect`

A finding must identify the first transition where untrusted content gains influence beyond its intended authority. The model must distinguish content interpretation from capability authorization and must never promote a claim beyond the highest observable boundary actually crossed.

## Required reasoning contracts

### Instruction authority model

Record the source class, intended authority, receiving component, protected invariant, and the authority actually granted after each transform. Equivalent text can be safe or unsafe depending on its source and authority label; payload wording alone is not the unit of analysis.

### Transformation provenance model

Track provenance across retrieval, parsing, OCR/transcription, summarization, templating, memory writes, tool-result formatting, context compaction, and delegation. A transform is security-relevant when it drops, merges, rewrites, or reinterprets source identity or authority.

### Decision/effect separation

Use an observable ladder:

- `P0` content is present or repeated;
- `P1` model preference/answer changes;
- `P2` protected policy decision changes;
- `P3` a capability proposal is produced;
- `P4` a deterministic gate accepts the synthetic proposal;
- `P5` a bounded inert effect occurs in the controlled sink.

No case may claim a level above its evidence.

### Counterfactual proof

For every validated case, vary one causal variable while holding the harness fixed: remove the untrusted source, preserve source but restore provenance, change the authority label, disable one transform, restore deterministic policy, or substitute an equivalent trusted instruction. The effect must track the hypothesized causal variable.

### Alternative explanations

Explicitly test for intended user authority, malformed harness behavior, retrieval relevance changes, stale memory, parser differences, confirmation state, identity/tenant mismatch, and tool-schema differences before promoting a boundary-failure claim.

## Operator runbook requirements

The runbook must retain the common operator-depth sections:

- Attack surface
- Hypothesis matrix
- Controlled validation
- False-positive controls
- Evidence capture
- Remediation checks

It must additionally contain:

- Instruction lineage trace
- Authority conflict analysis
- Transformation boundary analysis
- Decision and effect trace
- Counterfactual controls
- Evidence promotion and ceiling

All validation uses synthetic instructions, fake identities, inert markers, mocked tools, controlled RAG fixtures, and no-op sinks. No real secrets, destructive actions, persistence outside the sandbox, or third-party targets are permitted.

## Scenario contract

Each prompt-injection scenario must retain the common operator-depth fields and add:

- `source_class`
- `intended_authority`
- `transformation_trace`
- `authority_conflict`
- `protected_invariant`
- `decision_trace`
- `effect_ceiling`
- `counterfactual_control`
- `alternative_explanation`
- `evidence_ceiling`

Scenarios remain deterministic and benign. They test authority preservation, provenance continuity, and claim-bounding, not bypass creativity.

## Documentation contract

`operator-depth/profiles.json` becomes nine profiles with `prompt-injection-boundary-analysis` registered using the same local runbook/scenario paths and common required runbook sections. `docs/operator-depth-contract.md` and the README must describe the Wave 10 second-depth-ring expansion without rewriting Wave 8 history.

## Acceptance criteria

1. Dedicated depth tests are written first and fail on the pre-change skill.
2. The skill exposes the authority/provenance/decision/effect model and evidence ceiling.
3. The runbook satisfies common and prompt-specific reasoning sections.
4. The scenario matrix contains at least three distinct benign scenarios with all required reasoning fields.
5. The operator-depth validator reports nine profiles.
6. Existing skill, graph, benchmark, agent-eval, and superiority contracts remain unchanged and green.
7. Exact-head CI passes on Linux, macOS, and Windows for supported Python versions plus deterministic core jobs.