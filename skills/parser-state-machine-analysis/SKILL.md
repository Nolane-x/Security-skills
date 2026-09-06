---
name: parser-state-machine-analysis
description: "Analyze multi-phase parsers, nested formats, length/count bookkeeping, error recovery, deferred validation, container/child relationships, and parser state transitions in authorized code. Use when a parser bug depends on phase order, malformed structure, partial success, duplicate records, or post-parse semantic processing."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Parser State Machine Analysis

Treat a parser as a state machine that transforms untrusted bytes into increasingly trusted objects. Security bugs often appear where one phase assumes another phase established an invariant that was only partially checked.

## When to use

Use for file formats, archive/container readers, protocol decoders, image/media parsers, configuration languages, bytecode/loaders, or custom binary/text grammars.

## Preconditions

Run malformed-input testing only against authorized local/owned/sandboxed targets. Obtain format documentation or infer a phase model from source/traces.

## Workflow

1. **Draw phases.** Framing/header → index/table → body → nested parse → resolution/linking → validation → execution/render/use.
2. **List trust promotion points.** Where raw lengths become allocations, ids become pointers/references, tags select types, or parsed values become executable/configuration behavior.
3. **Track redundant metadata.** Outer/inner lengths, count vs actual entries, offsets vs buffer size, checksums, compressed/uncompressed size.
4. **Inspect duplicate and ordering behavior.** First-wins/last-wins, repeated metadata, forward references, out-of-order definitions.
5. **Inspect error recovery.** Partial objects, skipped bytes, resynchronization, rollback, cleanup, and whether “warning” states continue with weakened invariants.
6. **Inspect nested ownership.** Parent buffers versus child views/slices and lifetime after decompression/remapping.
7. **Model cross-record references.** Cycles, dangling ids, integer domains, aliasing, overlapping regions.
8. **Target phase-boundary mutations.** Inputs valid enough to cross one gate but inconsistent with the next phase’s assumptions.
9. **Minimize while preserving phase reach.** A smaller file that fails earlier may not represent the same bug.
10. **Validate root cause** with phase trace, first invalid state, and controls.

## Evidence contract

Preserve the minimized structure, parse-phase trace, invariant expected at each boundary, first phase where state becomes inconsistent, and downstream consumer. A malformed file being rejected or crashing only in harness glue is not a parser vulnerability.

## Stop conditions

Stop when the failure is an intentional hard rejection with no security-relevant side effect, the format model is too wrong to preserve phase reach, or testing would leave authorized scope.

## Output

```text
format/parser:
phase model:
trust-promotion points:
redundant/cross-record metadata:
first inconsistent state:
downstream assumption:
minimized structure:
controls:
variant phases:
```
