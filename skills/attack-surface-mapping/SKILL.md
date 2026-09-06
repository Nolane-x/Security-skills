---
name: attack-surface-mapping
description: "Map security-relevant inputs, parsers, trust boundaries, privilege transitions, state machines, and dangerous sinks before deeper analysis. Use when beginning review of an unfamiliar application, library, service, binary, protocol, agent, or subsystem."
metadata:
  nolane-security-category: discovery
  nolane-security-version: "1"
  nolane-security-authorization: conditional
---
# Attack Surface Mapping

Build a compact model of where untrusted influence enters the system and where it can cross a security boundary.

## When to use

Use at the beginning of an unfamiliar target, especially when “where should I look?” is the main question.

## Preconditions

- Prefer source, architecture docs, interfaces, or a local/authorized binary.
- For live discovery, confirm authorization with `security-scope-and-authorization`.
- Record exact target version/build when available.

## Workflow

1. **Enumerate entry points.** Files, network protocols, IPC, environment, command-line arguments, plugins, extensions, package metadata, URLs, serialization formats, database rows, message queues, model/tool inputs.
2. **Identify decoders and parsers.** Mark format transitions and normalization steps.
3. **Trace identity and authorization decisions.** Note authentication source, principal changes, signature/trust checks, ACLs, tokens, and confused-deputy opportunities.
4. **Mark stateful components.** Caches, retries, background jobs, connection state, session state, object lifetime, queues, and cleanup.
5. **Mark high-consequence sinks.** Memory copies, dynamic loading, command/process creation, filesystem writes, template interpretation, SQL/query construction, privileged APIs, deserialization, tool execution, network egress.
6. **Record invariants.** Length relationships, ownership/lifetime, canonical identity, permission assumptions, state transitions, isolation guarantees.
7. Rank surfaces by:
   - untrusted influence;
   - boundary crossed;
   - parser/normalization complexity;
   - statefulness;
   - historical bug density;
   - observability/testability.
8. Route top-ranked surfaces into `vulnerability-hypothesis-generation`.

## Evidence contract

The map should cite concrete code symbols, interfaces, files, binary functions, protocol fields, or configuration entries. “This component looks risky” is not enough.

A useful map explains an influence path:

```text
untrusted source -> transformation/state -> security decision -> sensitive sink
```

## Stop conditions

Stop broad mapping and move to a focused technique when:

- the top surfaces and invariants are clear;
- additional enumeration is producing duplicates rather than new boundary information;
- the available artifact cannot support stronger mapping.

For unauthorized live targets, do not expand mapping through active probing.

## Output

Produce a ranked table with:

- surface;
- untrusted source;
- trust/privilege boundary;
- key parser/state;
- sensitive sink;
- invariant to test;
- recommended next skill.
