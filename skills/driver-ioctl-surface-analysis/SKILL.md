---
name: driver-ioctl-surface-analysis
description: "Analyze device-control and IOCTL-style interfaces in authorized kernel/driver labs, including request schemas, buffer methods, length validation, object handles, privilege checks, asynchronous completion, and user/kernel trust transitions. Use for Windows/Linux/embedded drivers and device services."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Driver IOCTL Surface Analysis

Treat an IOCTL or device-control interface as a privileged RPC boundary. A command number by itself is not the security unit; the security unit is the full request contract from caller authority through transport, parsing, object/state binding, asynchronous ownership, and bounded privileged effect.

## When to use

Use for ioctl/device-control dispatchers, char devices, Windows IRP/IOCTL handlers, firmware control paths, vendor kernel modules, privileged device brokers, or other interfaces where less-privileged callers submit structured requests to privileged code.

## Preconditions

1. Use only owned/sandboxed test machines, disposable VMs, simulators, verifier-enabled labs, or explicitly authorized hardware.
2. Pin driver/service build, OS/runtime revision, architecture, symbols, device/simulator model, and relevant configuration.
3. Establish the documented or source-derived request contract before interpreting diagnostics.
4. Prefer source review, synthetic requests, inert object markers, verifier/sanitizer diagnostics, and read-only or simulator state.
5. Do not exercise operations that can damage hardware, alter unrelated host/device state, expose real secrets, or require weaponized exploitation to prove impact.

## Privileged request-contract model

Represent each command as an ordered state transition:

```text
caller principal
  -> namespace / device exposure
  -> open/handle gate
  -> command selector
  -> transport provenance
  -> schema version + structure interpretation
  -> normalized length / count / offset state
  -> object identity + ownership binding
  -> state prerequisite
  -> validation decision
  -> privileged handling
  -> asynchronous ownership / cancellation state
  -> completion authority
  -> bounded privileged effect
```

Every arrow is a contract boundary. Record which component owns the state, which representation it consumes, and which invariant must still hold before the next transition.

A reachable command is not a finding. A crash is not automatically a boundary failure. A validated finding requires evidence that a specific request-contract invariant is violated and that the violation changes a security-relevant state or effect beyond what the documented caller authority permits.

## Contract interpretation discipline

### Caller and open authority

Record the **caller principal** independently from the handle or file descriptor. The **open/handle gate** may restrict who can obtain an object, while individual commands may impose additional policy. Do not infer command authorization from device reachability alone, and do not call broad reachability a vulnerability when the documented policy intentionally permits it.

### Command and transport provenance

Bind the **command selector** to the exact transport model. Preserve **transport provenance** for buffered/direct/neither-style I/O, copied buffers, shared mappings, nested references, or brokered request envelopes. Record when data is copied, pinned, re-read, translated, or normalized. Two stages referring to “the same buffer” are not necessarily consuming the same bytes or ownership state.

### Schema and normalized arithmetic

Model the **schema version** and every length, count, offset, stride, element-size, discriminator, and union branch that affects interpretation. Record the **normalized length** after conversions and arithmetic, not only the caller-provided raw field.

Keep validation and later consumption conceptually separate. A request can pass a check correctly yet be consumed under different width, signedness, version, branch, or object-state assumptions. Conversely, a diagnostic during malformed input is not enough unless the valid neighboring contract is understood.

### Object identity and ownership

Track **object identity** as a tuple appropriate to the design: handle/id, type, creator/owner, namespace, generation or lifetime epoch, and any per-handle state. Require explicit **ownership binding** where the contract says the caller may operate only on objects it owns or has been granted.

Do not treat an identifier mismatch as security-relevant until the selected object, caller authority, and expected ownership rule are all established in the pinned lab.

### State and lifecycle

Record each **state prerequisite** that authorizes a command: initialization phase, device mode, per-handle negotiation, session state, queue state, feature flag, or transaction epoch. A state checked before queuing may no longer hold at completion.

For pending work, model **asynchronous ownership** explicitly: which object owns the request, buffer, referenced object, cancellation token, and completion context at each stage. Record **completion authority** separately from submission authority. A request authorized at submission is not automatically authorized to complete after handle close, device reset, ownership transfer, or state revocation.

### Bounded privileged effect

State the highest **privileged effect** directly demonstrated in the safe harness: controlled rejection difference, verifier diagnostic, bounded synthetic state mutation, cross-object marker selection, stale-lifecycle observation, or another non-destructive signal. Do not convert a parser bug class into claims of code execution, persistence, credential access, or hardware control without direct benign evidence.

### Counterfactual reasoning

For each suspected violation, construct a **counterfactual** that restores one contract invariant while holding neighboring state fixed. If the diagnostic or bounded effect persists unchanged, the suspected invariant is not yet causal.

Use neighboring valid/invalid requests to distinguish a real contract violation from stale symbols, wrong schema assumptions, simulator divergence, generic verifier noise, or intentionally permissive policy.

## Workflow

1. Freeze build, symbols, runtime, device/simulator model, and caller test class.
2. Define the command's expected request contract before generating any malformed variant.
3. Map caller principal, namespace exposure, open/handle gate, command selector, and transport provenance.
4. Build the schema/version model including normalized lengths, counts, offsets, discriminators, and object identifiers.
5. Record the validation snapshot: exact state proven before privileged handling.
6. Record the consumption snapshot: exact state later used by the parser, lookup, state machine, worker, or completion path.
7. Compare validation and consumption; identify the first contract invariant that stops matching.
8. Bind object identity, ownership binding, and state prerequisite to the caller and handle/session that authorized the operation.
9. For asynchronous paths, trace asynchronous ownership and completion authority through queue, cancellation, close/reset, and completion states using only controlled fixtures.
10. Use a counterfactual plus a valid neighboring request and one intentionally invalid neighboring request to test causality and false-positive explanations.
11. Stop at the first bounded privileged effect sufficient to demonstrate the invariant failure; broader real-world impact is unnecessary.
12. Check sibling commands only when they share the causal parser, object table, state machine, policy helper, or completion logic.

## Evidence ladder

Use evidence states conservatively:

- **Hypothesis** — source/configuration suggests a request-contract mismatch, but no controlled observation demonstrates it.
- **Observed** — a pinned lab shows a parser, object, state, or lifecycle difference, but causal linkage to the expected contract is incomplete.
- **Validated** — the expected invariant is established; validation and consumption or lifecycle states are captured; the first causal divergence is identified; a bounded privileged effect is observed; and positive, negative, counterfactual, and neighboring controls reject plausible alternatives.
- **Regression verified** — the causal invariant is restored on the fixed revision, the original synthetic failure no longer reproduces, and neighboring valid behavior plus relevant sibling/state controls remain correct.

Do not promote a finding solely because a command is exposed, a malformed request crashes, a verifier fires, or an invalid request is accepted. The evidence must identify what contract was broken and why the observed effect depends on that break.

## Evidence contract

For each candidate preserve:

- pinned build/runtime/device or simulator identity;
- caller principal and documented authority;
- namespace exposure and open/handle gate;
- command selector and transport provenance;
- schema version plus normalized length/count/offset state;
- validation snapshot and consumption snapshot;
- object identity, ownership binding, and state prerequisite;
- asynchronous ownership and completion authority when applicable;
- first causal contract divergence;
- bounded privileged effect;
- positive, negative, counterfactual, and neighboring controls;
- alternative explanations rejected;
- evidence state and remediation regression result.

An exposed IOCTL, a broad caller class, a parser diagnostic, or a crash is not sufficient evidence by itself.

## Stop conditions

Stop if validation would require real production targeting, destructive device operations, uncontrolled host state, real secrets, bypass construction, persistence, or weaponized payloads. Stop if the request schema cannot be established reliably, if the caller already has the documented authority for the observed effect, or if the claimed causal contract cannot be separated from build/symbol/simulator mismatch.

## Output

```text
driver/service revision:
device/simulator:
caller principal:
open/handle gate:
command selector:
transport provenance:
schema version:
normalized lengths/counts/offsets:
validation snapshot:
consumption snapshot:
object identity / ownership binding:
state prerequisite:
asynchronous ownership:
completion authority:
first causal contract divergence:
bounded privileged effect:
counterfactual:
positive / negative / neighboring controls:
alternative explanations rejected:
evidence state:
remediation regression:
```
