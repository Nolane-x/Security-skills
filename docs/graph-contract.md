# Security Skill Graph Contract

`SKILL.md` remains the portable Agent Skills artifact. `skill.meta.json` is a Nolane-sidecar used only for graph routing, validation, maturity tracking, and pack composition.

Each skill sidecar uses schema version 1:

```json
{
  "schema_version": 1,
  "maturity": "stable",
  "domains": ["fuzzing"],
  "prerequisites": ["security-scope-and-authorization"],
  "composes_with": ["crash-triage-and-minimization"],
  "evidence_stage": "observed"
}
```

`prerequisites` is a directed acyclic dependency relation. `composes_with` is a non-ordering recommendation relation and may be reciprocal. `evidence_stage` means the minimum research-state that the workflow is designed to produce when successfully completed; it does not automatically upgrade a finding without the skill's evidence contract.

Pack manifests under `packs/*.json` group reusable skills without copying their content. A pack has one entrypoint, a set of member skills, and an opinionated default flow. Agents may deviate from the default flow when target evidence justifies a different route.

## Pack ordering invariants

A pack is valid only when:

1. its `entrypoint` is both a known canonical skill and a member of the pack;
2. every `default_flow` node is a member of the pack;
3. if a prerequisite and its dependent skill both appear in `default_flow`, the prerequisite appears first;
4. `default_flow` is an advisory evidence route, not permission to skip a prerequisite that is relevant but omitted from the compact route.

This ordering rule prevents a generated agent route from presenting a dependent research step before the context/evidence it assumes.
