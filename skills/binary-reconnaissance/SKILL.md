---
name: binary-reconnaissance
description: "Map an authorized binary's functions, imports, parsers, IPC/network surfaces, privilege boundaries, dynamic loading, and security-relevant behavior before deeper reverse engineering. Use when source is missing, incomplete, or does not match the shipped artifact."
metadata:
  nolane-security-category: discovery
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Binary Reconnaissance

Build a security-oriented binary map without prematurely attempting exploitation.

## When to use

Use when the available artifact is a binary, firmware component, library, plugin, or executable whose source is missing or uncertain.

## Preconditions

- Binary is local, owned, sandboxed, benchmark/CTF, or explicitly authorized for analysis.
- Record hashes, architecture, platform, version metadata, and signing status.
- Preserve an original copy.

## Workflow

1. Identify format, architecture, imports/exports, sections, symbols, signatures, and obvious packers/obfuscation.
2. Locate input surfaces through imports, strings, entry points, protocol/file handlers, IPC APIs, plugin loading, and command-line parsing.
3. Locate security boundaries: privilege changes, sandbox interfaces, trust/signature checks, service/helper IPC, dynamic loading.
4. Build a call/function map around the top surfaces.
5. Recover data structures only as deeply as the current hypothesis requires.
6. Correlate static findings with safe local runtime observation when useful.
7. Name key invariants and suspicious transformations.
8. Route:
   - repeated input surface -> fuzzing;
   - bounded path question -> symbolic execution;
   - runtime fault -> crash triage;
   - source equivalent found -> static/dataflow.

Tool families may include Ghidra-style decompilation, debugger tracing, emulation, and runtime instrumentation.

## Evidence contract

Record:

- binary hash and metadata;
- concrete functions/imports/strings supporting each surface;
- observed runtime events separately from decompiler inference;
- confidence for recovered types/control flow;
- unresolved assumptions.

Do not treat decompiler output as exact source semantics.

## Stop conditions

Stop deeper dynamic work when authorization is unclear, when anti-analysis behavior risks affecting systems outside the lab, or when the current question can be answered more reliably from source/vendor symbols.

## Output

Produce a ranked binary surface map with artifact identity, functions/interfaces, trust boundaries, invariants, confidence, and next recommended skill.
