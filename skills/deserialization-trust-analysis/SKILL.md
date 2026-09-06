---
name: deserialization-trust-analysis
description: "Analyze how serialized or structured untrusted data becomes typed objects, callbacks, paths, classes, templates, commands, policies, or privileged actions. Use for unsafe polymorphism, object reconstruction, schema confusion, gadget-like side effects, or trust promotion during decoding."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Deserialization Trust Analysis

Deserialization analysis follows trust promotion: bytes become fields, fields become types/objects, and objects may acquire behavior or authority. Focus on the exact semantic boundary where data becomes executable or privileged state.

## When to use

Use for object serializers, RPC codecs, YAML/XML/JSON frameworks with polymorphism, binary object formats, session/token payloads, saved models/configs, template/config loaders.

## Preconditions

Use only authorized local/owned/sandboxed fixtures. Keep proofs benign: type selection, marker callback in a test harness, or rejected/accepted state—not harmful command execution.

## Workflow

1. **Identify format and trust origin.** Network, file upload, cache, database, signed token, inter-service message, local config.
2. **Trace decode layers.** Framing → syntax → schema → type selection → object construction → hooks/callbacks → application use.
3. **Map polymorphism/type controls.** Explicit class name, tag, discriminator, registry, reflection, plugin lookup.
4. **Map side-effecting construction.** Constructors, setters, post-load hooks, finalizers, validators, resource openers.
5. **Check allowlist semantics.** Exact type, base class, namespace prefix, package/module wildcard, aliases.
6. **Check integrity/authentication boundary.** Signed/encrypted data can still be attacker-controlled if the attacker legitimately obtains signing capability for a narrower purpose.
7. **Check schema/runtime mismatch.** Fields validated as data may later be interpreted as paths, expressions, templates, queries, or policy names.
8. **Test with synthetic harmless types/markers** to prove unexpected trust promotion.
9. **Compare safe data-only mode** or explicit schema mapping as a control.
10. **Recommend data/behavior separation** and least-capability reconstruction.

## Evidence contract

Show attacker-influenced serialized fields, the decode/type-selection path, unexpected behavior/authority acquired during or after reconstruction, and a benign control demonstrating the unsafe promotion disappears under restricted mapping.

## Stop conditions

Stop if data authenticity and authorization guarantee the sender is fully trusted for the reconstructed capability, runtime type selection is closed and side-effect free, or proof would require harmful payload behavior.

## Output

```text
format/origin:
decode layers:
type-selection mechanism:
side-effect boundary:
attacker-controlled fields:
benign unexpected behavior:
restricted-mode control:
trust assumption violated:
fix direction:
```
