# Wave 7 Operator Depth Contract Design

## Status

Approved implementation direction for the September 14, 2026 upgrade of `Nolane-x/Security-skills`.

## Problem

The repository already has a strong verification-first architecture: canonical skills, graph metadata, deterministic routing, evidence states, benchmark fixtures, and cross-agent evaluation. Its main weakness versus deep offensive skill libraries is not skill count; it is tactical/operator depth inside high-value domain skills.

Simply making `SKILL.md` files longer would be the wrong fix. Length is not a quality contract, duplicated payload catalogs are difficult to maintain, and unbounded offensive instructions would conflict with the repository's authorization and evidence-first design.

## Goal

Add a deterministic, testable operator-depth layer that makes selected canonical skills substantially more useful during authorized security research while preserving the existing graph, safety boundaries, evidence discipline, portability, and zero-third-party-dependency baseline.

## Scope

Wave 7 covers four high-value skills:

1. `ai-agent-security-assessment`
2. `server-side-request-boundary-analysis`
3. `authorization-boundary-analysis`
4. `cloud-iam-path-analysis`

The wave does not increase the canonical skill count. It deepens existing skills through reviewed runbooks and an enforceable repository contract.

## Architecture

### Operator-depth manifest

Add `operator-depth/profiles.json` as the canonical registry for operator-depth profiles. Each entry identifies:

- the canonical skill name;
- a runbook path relative to that skill;
- required runbook section headings;
- an explicit `lab_only: true` requirement.

The manifest contains no executable payloads and no vendor-specific agent bindings.

### Deterministic validator

Add `scripts/validate_operator_depth.py` using only the Python standard library. It must fail closed when:

- the manifest is absent or malformed;
- the version is unsupported;
- a profile references a missing/nonexistent canonical skill;
- skill names are duplicated;
- a runbook path is absolute or escapes the skill directory;
- the runbook is absent;
- `lab_only` is not exactly `true`;
- the canonical `SKILL.md` does not link to the runbook;
- the runbook omits a required section;
- the runbook omits explicit authorization/lab boundaries, evidence capture, or false-positive/control discipline.

Diagnostics must be deterministic: collect errors, sort them, print each once, and return a non-zero exit code when any error exists.

### Deep operator runbooks

Each selected skill gets `references/operator-runbook.md`. Runbooks are tactical research guides, not exploit/payload dumps. Every runbook contains six required sections:

- `## Attack surface`
- `## Hypothesis matrix`
- `## Controlled validation`
- `## False-positive controls`
- `## Evidence capture`
- `## Remediation checks`

The depth comes from enumerating concrete trust transitions, failure modes, experimental controls, evidence fields, and remediation regression checks.

### Canonical skill integration

Each selected `SKILL.md` gets a concise `## Operator depth` section linking `references/operator-runbook.md`. The canonical skill remains the portable entry point; the runbook carries extended methodology without duplicating the skill itself.

### CI authority

The existing cross-platform validation matrix invokes `python scripts/validate_operator_depth.py`. The new contract therefore becomes a merge gate alongside skill, graph, benchmark, and agent-evaluation validation.

## Domain depth requirements

### AI agent security

The runbook covers principals, trust transitions, untrusted retrieved/web/document content, RAG provenance, persistent memory, tool schemas, connectors/MCP, delegated/multi-agent actions, confirmation policy, network egress, and tenant identity. Validation uses synthetic canaries, mocked tools, fake tenants, and non-sensitive data.

### Server-side request boundaries

The runbook covers parser/normalization differences, hostname/address resolution, DNS changes, IPv4/IPv6 interpretation, redirect revalidation, scheme/port transitions, proxies, and credential/header forwarding. Dynamic validation uses only controlled mock endpoints; real cloud metadata or internal-network probing is explicitly excluded.

### Authorization boundaries

The runbook models subject/object/action/context combinations, ownership, role/tenant boundaries, batch and collection operations, asynchronous workers, exports, caches, delegated service identities, stale sessions, and state-change races. Validation uses synthetic identities and owned test objects.

### Cloud IAM

The runbook models principals, identity federation, role/service-account assumption, policy sources, explicit denies, permission boundaries/organization policies, conditions, session/token lifetime, resource policies, cross-account/project/subscription trust, KMS/storage access, and audit evidence. Validation is limited to dedicated sandbox cloud environments.

## Evidence discipline

A successful operator-depth profile must make the agent distinguish at least these states:

- hypothesis: a path may exist;
- observed: a relevant boundary behavior was reproduced;
- validated: the boundary crossing and bounded security consequence were demonstrated with positive and negative controls;
- regression-verified: the fix blocks the failing path while intended controls still succeed.

Runbooks must never instruct an agent to promote a finding solely from scanner output, model speculation, a single surprising response, or theoretical policy composition.

## Safety and authorization boundaries

Wave 7 remains designed for local, owned, sandboxed, CTF, benchmark, or explicitly authorized targets. The runbooks do not add credential theft, persistence, destructive actions, uncontrolled network scanning, real metadata-service access, or production-secret handling.

Where a real system would make validation risky, the runbook substitutes synthetic canaries, mock services, fake identities, or policy simulation.

## Testing strategy

Use TDD:

1. Add repository/fixture tests before the validator exists and confirm CI RED for the missing validator/contract.
2. Implement the minimal validator and manifest required to satisfy structural tests.
3. Add runbooks and skill links, keeping the same tests GREEN.
4. Add the validator to the existing CI matrix.
5. Run the complete repository CI and require all existing deterministic benchmark and cross-agent gates to remain GREEN.

Tests include repository success plus negative fixtures for a missing runbook, path escape, and omitted required section.

## Non-goals

Wave 7 does not:

- increase the 83-skill count;
- copy Claude-Red or another repository's prose;
- add exploit payload catalogs;
- add third-party Python packages;
- hard-code Claude, GPT, Gemini, Qwen, DeepSeek, or another model vendor;
- weaken authorization or evidence gates;
- replace existing Wave 5/6 benchmarks.

## Success criteria

Wave 7 is complete when:

- all four profiles have distinct deep runbooks;
- each canonical skill links its runbook;
- `validate_operator_depth.py` rejects malformed/unsafe profiles deterministically;
- the new validator is part of cross-platform CI;
- all existing skill/graph/benchmark/agent-evaluation tests remain GREEN;
- the PR diff contains no duplicated payload corpus or vendor lock-in.
