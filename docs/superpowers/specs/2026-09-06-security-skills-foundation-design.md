# Security Skills Foundation Design

**Date:** 2026-09-06  
**Status:** Approved foundation design  
**Repository:** `Nolane-x/Security-skills`

## Goal

Build a portable, verification-first security skill graph that can be consumed by current AI coding agents without maintaining divergent prompt copies for each product.

## Design principles

1. **One canonical skill source.** Every reusable capability lives under `skills/<name>/SKILL.md`.
2. **Open-standard first.** Canonical skills conform to the Agent Skills specification: YAML frontmatter plus Markdown, with optional `scripts/`, `references/`, and `assets/`.
3. **Progressive disclosure.** `SKILL.md` stays focused; deeper material lives in references so agents do not load the entire knowledge base into context.
4. **Portable by adapters, not forks.** Native skill consumers read or install the canonical directories. Agents without native skill support use `AGENTS.md`, rules, or generated/imported instruction adapters that point back to the same canonical skill.
5. **Evidence before claims.** A vulnerability is not "confirmed" merely because static reasoning or an LLM says so. The skill graph distinguishes hypothesis, reproduced behavior, root-cause evidence, impact evidence, and fix verification.
6. **Authorization-aware security work.** Intrusive workflows require an owned, local, sandboxed, or explicitly authorized target. Skills stop rather than silently crossing an authorization boundary.
7. **Benign proof defaults.** Demonstrations favor markers, assertions, sanitizer reports, controlled crashes, or local proof signals rather than persistence, credential access, destructive effects, or covert payloads.
8. **Tool-independent reasoning.** Skills teach research decisions and evidence contracts first, then mention compatible tool families as optional adapters.
9. **Deterministic validation.** Repository scripts validate skill structure, metadata, required workflow sections, catalog generation, and cross-platform path assumptions.
10. **Composable graph.** A meta-router selects foundational skills and later domain/tool packs rather than placing all knowledge in one monolithic prompt.

## Architecture

```text
Security Research Router
        |
        +-- Scope & Authorization
        +-- Attack Surface Mapping
        +-- Hypothesis Generation
        |
        +-- Discovery
        |    +-- Fuzzing Workflow
        |    +-- Static/Dataflow Analysis
        |    +-- Symbolic Execution
        |    +-- Binary Reconnaissance
        |
        +-- Verification
        |    +-- Crash Triage & Minimization
        |    +-- Evidence-Driven Validation
        |    +-- Patch-Diff Variant Analysis
        |
        +-- Remediation
        |    +-- Remediation & Regression
        |    +-- Secure Code Review
        |
        +-- Domain Packs
             +-- AI/Agent Security Assessment
             +-- future: kernel/browser/cloud/mobile/firmware/web/...
```

## Canonical skill contract

Every skill must contain:

- valid Agent Skills frontmatter (`name`, `description`);
- Nolane metadata with category, version, and authorization sensitivity;
- `When to use`;
- `Preconditions`;
- `Workflow`;
- `Evidence contract`;
- `Stop conditions`;
- `Output`.

Skills that need substantial technical material put it in `references/` and link to it using relative paths.

## Portability model

The repository stores canonical skills only once. Installation documentation covers native paths and import mechanisms for major agents. `.agents/skills/` is treated as the strongest shared project-level convention where supported. `AGENTS.md` remains a lowest-common-denominator standing-instruction fallback.

Product-specific metadata that is not part of the open specification is not placed in canonical frontmatter unless it can be safely ignored by other consumers. Experimental `allowed-tools` is deliberately avoided in the foundation because support varies.

## Validation

`python scripts/validate_skills.py` performs dependency-free structural validation.  
`python scripts/build_catalog.py --check` verifies that `CATALOG.md` and `catalog.json` are deterministic and current.  
`python -m unittest discover -s tests -v` tests parser, validation, and catalog behavior.

CI runs these checks on Linux, macOS, and Windows.

## Foundation scope

The first release contains reusable reasoning/workflow skills rather than hundreds of thin wrappers. Later releases may add domain packs, tool adapters, benchmark packs, and source-derived research patterns, but only after they meet the same evidence and portability contracts.
