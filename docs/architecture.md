# Architecture

## Canonical layer

`skills/` is the source of truth. A skill is a directory containing `SKILL.md` and optional `references/`, `scripts/`, or `assets/`.

The foundation avoids vendor-specific fields such as product-only glob controls or experimental pre-approved tool declarations in canonical frontmatter. Product adapters may add such behavior outside the canonical skill.

## Skill graph

The graph has six conceptual layers:

1. **Foundations:** authorization, scope, trust boundaries, evidence states.
2. **Discovery:** attack-surface mapping, hypotheses, fuzzing, static/dataflow, symbolic execution, binary reconnaissance.
3. **Verification:** triage, minimization, causal evidence, controls, affected-version checks.
4. **Remediation:** patch analysis, regression construction, secure review.
5. **Domain packs:** AI/agent security first; later web, kernel, browser, cloud, mobile, firmware, hypervisor, smart contract, and protocol packs.
6. **Meta-reasoner:** `security-research-router` composes the other skills and decides when to change methods.

## Why not one giant skill?

Large always-on prompts consume context and make routing ambiguous. The open Agent Skills model supports progressive disclosure: an agent sees metadata first, activates a relevant skill, and reads deeper references only when needed.

## Evidence model

```text
hypothesis
   |
   v
observed behavior
   |
   +--> alternative explanations / harness artifact -> reject or revise
   |
   v
validated root cause + security consequence
   |
   v
fix candidate
   |
   v
regression-verified
```

Every domain pack inherits this evidence model.
