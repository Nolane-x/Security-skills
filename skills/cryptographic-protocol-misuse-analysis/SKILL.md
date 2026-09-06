---
name: cryptographic-protocol-misuse-analysis
description: "Analyze application-level cryptographic protocol use: primitive choice, mode/domain separation, transcript binding, key roles, authentication order, replay context, downgrade negotiation, and error handling. Use for misuse analysis, not cryptanalytic key breaking."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Cryptographic Protocol Misuse Analysis

Perform any dynamic validation only in an authorized, owned lab or equivalent explicitly scoped test environment.

## When to use

Use when code implements or composes encryption, MACs, signatures, KDFs, password hashing, key agreement, token formats, custom envelopes, or negotiated security protocols.

## Preconditions

1. Work from source/specification and synthetic test vectors.
2. Pin library/version, protocol version, algorithms, and threat model.
3. Do not attempt brute-force recovery of real keys/passwords.

## Workflow

1. Define security goals: confidentiality, integrity, authenticity, freshness, channel/identity binding, forward secrecy, or password resistance.
2. Map keys and domains: generation, derivation labels/context, roles, storage, rotation, and which messages/transcripts they authenticate.
3. Check primitive/mode parameters, nonce/IV requirements, tag/signature verification order, and whether errors expose distinct security states.
4. Review downgrade/version/algorithm negotiation and whether the final choice is bound into authenticated context.
5. Review replay/freshness and whether tokens/messages bind to audience, action, tenant/session, and protocol phase.
6. Use published/synthetic vectors and mutation controls to verify expected rejection/acceptance; do not invent “novel crypto” as a fix.

## Evidence contract

Record stated security goal, primitive/protocol construction, key role, bound/unbound context, synthetic vector/mutation, and acceptance result. Nonstandard code is a hypothesis, not proof of breakage.

## Stop conditions

Stop if assessment requires attacking real keys, brute force, side-channel probing outside scope, or claims beyond the demonstrated protocol property.

## Output

```text
protocol/use case:
security goals:
algorithms/parameters:
key roles/lifecycle:
bound context:
replay/downgrade model:
test vectors/controls:
evidence status:
```
