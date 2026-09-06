# Architecture

## 1. Canonical portable layer

`skills/<name>/SKILL.md` is the portable source of truth. Skills follow the Agent Skills structure and keep vendor-specific controls out of canonical frontmatter.

A skill contains the smallest complete reasoning workflow an agent can activate independently. Deep implementation notes may live inside that skill's own `references/`, `scripts/`, or `assets/` directory so the package remains self-contained when copied.

## 2. Graph sidecar layer

Each canonical skill also has `skill.meta.json`. The sidecar is intentionally outside `SKILL.md` frontmatter so hosts that implement only the open Agent Skills contract can ignore Nolane-specific routing metadata.

Schema version 1 records:

- maturity: `experimental`, `beta`, or `stable`;
- domains;
- directed `prerequisites`;
- non-ordering `composes_with` recommendations;
- minimum intended evidence stage.

`prerequisites` must form a DAG. Unknown nodes, self-dependencies, malformed metadata, and cycles are hard validation errors.

## 3. Pack layer

`packs/*.json` groups existing canonical skills into reusable domain routes. Packs do not copy skill text. Each pack declares:

- an entrypoint;
- the permitted member skill set;
- an opinionated `default_flow`.

The default flow is advisory. Evidence may require routing to another member or cross-domain skill.

## 4. Conceptual security graph

The graph has six reasoning layers:

1. **Foundations:** authorization, scope, research state, trust boundaries.
2. **Discovery:** attack surface, hypotheses, fuzzing, static/dataflow, differential, symbolic and binary analysis.
3. **Semantic root cause:** lifetime, bounds/integer, type, concurrency, parser/protocol state, identity/canonicalization, authorization/delegation.
4. **Verification:** minimization, sanitizers, controls, causal validation, conservative impact triage, version matrices.
5. **Remediation:** patch analysis, variant hunting, invariant-level fixes, regression closure.
6. **Meta-reasoner:** routing through packs/skills based on target evidence and failed hypotheses.

## 5. Evidence state machine

```text
hypothesis
   |
   v
observed behavior
   |
   +--> alternative explanation / harness artifact -> reject or revise
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

A graph edge never upgrades evidence by itself. The destination skill's evidence contract must actually be satisfied.

## 6. Generated artifacts

- `catalog.json` / `CATALOG.md`: build-on-demand portable skill inventory.
- `graph.json` / `GRAPH.md`: build-on-demand routing graph, pack membership, prerequisites, maturity, domains and evidence stage.

Generated indexes are intentionally ignored by Git. `SKILL.md`, `skill.meta.json`, and `packs/*.json` are the canonical source; CI generates the indexes and immediately runs `--check` to verify deterministic output.

## 7. Why not one giant security prompt?

A giant always-on prompt wastes context, creates ambiguous routing, and encourages agents to skip verification. Progressive disclosure lets an agent first inspect metadata, activate a focused pack/skill, then read only locally relevant detail.
