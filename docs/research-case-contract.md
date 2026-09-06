# Research Case Contract

A research case is the machine-readable state shared by the Security Skills router, validators, and any AI agent using the library. It records **what is claimed, what has actually been observed, what controls exist, and what remains uncertain**.

Canonical schema: [`schemas/research-case.schema.json`](../schemas/research-case.schema.json)

Example: [`examples/research-case.example.json`](../examples/research-case.example.json)

## Evidence states

| State | Minimum meaning |
| --- | --- |
| `hypothesis` | Authorized scoped claim worth investigating. No reproduction implied. |
| `observed` | Behavior reproduced in a pinned environment. Cause/impact may still be unknown. |
| `validated` | Reproducer + causal root cause + bounded security consequence + positive and negative controls. |
| `regression-verified` | Validated evidence no longer reproduces on a pinned fixed revision while controls still pass. |

States may advance one step at a time. The validator rejects silent downgrades and skipped stages because both hide missing evidence.

## Scope gate

Every case carries:

```json
"scope": {
  "authorized": true,
  "kind": "sandbox",
  "target": "local fixture"
}
```

The advisory router refuses an unauthorized case. Routing cannot grant authorization and does not execute security tools.

## Controls

A `validated` claim needs both:

- a **positive control** showing the environment/harness still exercises expected behavior;
- a **negative control** that removes or changes the hypothesized cause and discriminates it from harness noise or an unrelated failure.

## Reproducer identity

Validated cases record human-readable steps and a fixture digest. This makes later fix validation compare the same evidence rather than a loosely similar test.

## Commands

```bash
python scripts/validate_case.py examples/research-case.example.json
python scripts/route_skills.py examples/research-case.example.json --limit 12
```

The example intentionally remains `observed`; it does not contain enough evidence to be called validated.
