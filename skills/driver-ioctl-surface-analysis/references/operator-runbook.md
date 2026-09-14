# Driver Interface Operator Runbook

Use this runbook only on owned test systems, disposable virtual machines, simulators, verifier-enabled labs, or explicitly authorized hardware. Prefer source/schema review, synthetic requests, diagnostics, inert object markers, and read-only or simulator state. The objective is to verify privileged request contracts without causing device or host side effects.

## Privileged request-contract semantics

Treat each device-control command as a contract joining authority, interpretation, identity, state, and lifetime.

The contract is valid only when all relevant layers agree on the same security meaning:

```text
caller authority
  + open/handle authority
  + command meaning
  + transport ownership
  + schema/version meaning
  + normalized arithmetic
  + object identity and ownership
  + state prerequisite
  + completion authority
  -> permitted bounded privileged effect
```

Write the expected invariant before testing. A command being callable, an invalid request being accepted, or a diagnostic appearing does not by itself establish a security failure. The review must identify which contract term diverged and why that divergence matters under the documented caller policy.

## Request interpretation model

Build a hopwise state trace for every candidate command:

```text
caller principal
  -> namespace/device exposure
  -> open/handle gate
  -> command selector
  -> transport provenance
  -> schema/version decode
  -> normalized length/count/offset state
  -> validation snapshot
  -> object lookup and ownership binding
  -> state prerequisite
  -> consumption snapshot
  -> asynchronous ownership / cancellation
  -> completion authority
  -> bounded privileged effect
```

Record both raw and normalized fields where interpretation changes. Preserve the component that produced each state and the component that consumes it next.

### Open and command authority

Separate the **open/handle gate** from per-command authorization. A caller may legitimately obtain a device handle yet still be denied particular operations, or the documented design may intentionally grant all commands to that caller class. Establish the policy from source, configuration, or owner-approved requirements before assigning security meaning.

### Transport provenance

Record **transport provenance** for every request representation: copied buffer, direct/pinned region, shared mapping, user reference, nested structure, broker envelope, or other design-specific transport. Record when ownership or mutability changes. Do not assume validation and later handling observe the same bytes merely because they originate from one logical request.

### Schema/version and arithmetic

Record the complete **schema/version** contract: structure version, discriminator, union branch, minimum/maximum size, element count, offset, stride, alignment, and related flags. Record the **normalized length** after width conversion and arithmetic rather than relying only on the raw caller field.

Arithmetic should be reviewed as interpretation state. The important question is whether validation and later consumption use compatible normalized meanings, not whether one isolated comparison appears present in source.

## Validation-to-consumption binding

Capture a **validation snapshot** and a **consumption snapshot** for each suspected invariant.

The validation snapshot records the exact state that has been proven safe or authorized before privileged handling: caller/handle context, command selector, schema version, normalized lengths/counts/offsets, object reference form, and relevant state prerequisite.

The consumption snapshot records the exact state later used by parsing, copying, object lookup, state-machine logic, worker execution, or completion. It must include any re-read, re-decoded, transformed, or asynchronously retained values.

A validated mismatch requires more than different values. Show that the two snapshots are intended to represent the same contract term, that the difference is not an intentional transformation, and that the divergence causally changes a bounded security-relevant result.

Examples of safe review questions include:

- Does validation prove the same schema branch that later handling consumes?
- Are length/count/offset values normalized once or independently interpreted later?
- Can object lookup replace a validated identifier with a different ownership context?
- Does asynchronous work retain the state that authorized submission, or must authority be re-established at completion?

Keep these as source/configuration and synthetic-harness questions; do not broaden them into real-world exploitation.

## Object identity and lifecycle binding

Model **object identity** as the tuple required by the design: identifier/handle, type, namespace, creator or owner, generation/lifetime epoch, and per-handle/session context when applicable.

Record **ownership binding** explicitly. If policy says a caller may operate only on owned or granted objects, identify where that relationship is established, where it is checked, and whether later lookup or asynchronous handling preserves it.

Record each **state prerequisite** separately from object identity. Initialization state, negotiated mode, queue membership, transaction epoch, device mode, or per-handle setup can authorize behavior without changing the object identifier.

For queued/pending operations, record **asynchronous ownership**: which object owns the request, referenced object, buffer or mapped region, cancellation state, and completion context at each transition.

Record **completion authority** as its own contract term. A request accepted at submission time is not automatically entitled to complete after close, reset, ownership transfer, cancellation, or state revocation. Conversely, a completion after a lifecycle change is not automatically wrong if the documented contract intentionally permits it.

## Attack surface

Map commands by shared security machinery rather than only by numeric selector. Group commands that share parsers, schema helpers, object tables, ownership rules, state machines, queues, completion logic, or caller policy.

For every command capture:

- caller principal and expected authority;
- namespace exposure and open/handle gate;
- command selector and command family;
- transport provenance and mutability/ownership transitions;
- schema/version and normalized arithmetic;
- validation snapshot;
- object identity, ownership binding, and state prerequisite;
- consumption snapshot;
- asynchronous ownership and completion authority;
- bounded privileged effect or rejection result.

A sibling command is relevant only when it shares the causal machinery under review.

## Hypothesis matrix

Write falsifiable hypotheses around contract invariants, for example:

- validation and consumption disagree on schema/version or normalized length;
- an object identifier resolves without the ownership binding required by policy;
- a per-handle state prerequisite is replaced by global/shared state;
- asynchronous ownership no longer matches the object/session that authorized submission;
- completion authority survives a lifecycle transition that policy says should revoke it;
- caller/open policy and per-command policy disagree on the same documented operation.

Every hypothesis must define an expected invariant, a benign proof signal, and at least one alternative explanation that would invalidate the claim.

## Controlled validation

1. Pin driver/service build, symbols, OS/runtime, architecture, device/simulator model, and configuration.
2. Establish the source-derived or documented contract before creating a synthetic case.
3. Use synthetic buffers, identifiers, caller classes, state markers, and simulator/verifier fixtures only.
4. Capture the canonical valid request as a positive control.
5. Capture one intentionally invalid neighboring request as a negative control.
6. Record transport provenance plus schema/version and normalized arithmetic for both controls.
7. Capture the validation snapshot and consumption snapshot at the smallest observable boundary supported by the lab.
8. Bind object identity, ownership binding, and state prerequisite to the caller/session that authorizes the request.
9. For lifecycle cases, record asynchronous ownership and completion authority using deterministic simulator or test-harness state transitions where possible.
10. Identify the first contract divergence; do not reason backward only from a final diagnostic.
11. Run a counterfactual that restores that single invariant while keeping neighboring synthetic state fixed.
12. Stop once a bounded privileged effect or direct contract violation is demonstrated; broader impact is unnecessary.

## Counterfactual controls

A counterfactual must test the suspected cause, not merely use a different request.

Useful controlled comparisons include:

- same valid request with one reviewed contract field changed to its canonical value;
- same synthetic object identity with correct versus intentionally distinct ownership metadata;
- same schema/version with validation and consumption forced through the same source-derived interpretation in a unit/integration fixture;
- same lifecycle case with the state prerequisite preserved versus intentionally revoked in a simulator;
- same asynchronous request with completion authority preserved versus explicitly absent according to the test contract.

Reject or downgrade the finding if the signal persists when the suspected invariant is restored.

Use a **neighboring control** that should remain valid after remediation. This prevents a fix from “passing” simply by rejecting every request or disabling the command family.

## False-positive controls

Actively test plausible **alternative explanation** classes:

- stale or mismatched symbols/build;
- incorrect schema/version assumption;
- simulator behavior not matching the reviewed contract;
- generic verifier noise that also appears for valid controls;
- intentionally permissive caller policy;
- documented transformation between validation and consumption;
- expected object aliasing or shared ownership;
- timing noise not tied to lifecycle state;
- instrumentation that changes the state being observed.

A diagnostic is stronger when the valid neighboring control remains clean and the counterfactual removes the signal.

## Evidence ladder

Use conservative evidence states:

- **Hypothesis** — source/configuration suggests a contract mismatch but there is no controlled observation yet.
- **Observed** — a pinned lab shows a schema, object, state, or lifecycle difference, but causality or policy meaning is incomplete.
- **Validated** — the expected invariant is established; validation snapshot and consumption snapshot or lifecycle states are captured; the first divergence is identified; a bounded privileged effect is observed; and positive, negative, counterfactual, and neighboring controls reject plausible alternatives.
- **Regression verified** — the fixed revision restores the causal invariant while the original synthetic failure disappears and valid neighboring behavior plus relevant sibling/state controls remain correct.

Do not promote from observed to validated based on reachability, a crash, one verifier diagnostic, or a common vulnerability class alone.

## Evidence capture

```text
driver_service_revision:
os_runtime_architecture:
device_or_simulator:
caller_principal:
open_handle_gate:
command_selector:
transport_provenance:
schema_version:
normalized_lengths_counts_offsets:
validation_snapshot:
object_identity:
ownership_binding:
state_prerequisite:
consumption_snapshot:
asynchronous_ownership:
completion_authority:
expected_invariant:
first_contract_divergence:
bounded_privileged_effect:
counterfactual_result:
positive_control:
negative_control:
neighboring_control:
alternative_explanations_rejected:
related_sibling_commands:
evidence_state:
```

Preserve observable traces and state. Hidden reasoning is not evidence.

## Remediation proof

Repair the causal invariant, not the synthetic proof artifact. Appropriate design-level remediations can include centralizing schema/version interpretation, computing normalized arithmetic once, preserving object/ownership tuples across lookup, making state prerequisites explicit, or re-establishing completion authority where lifecycle transitions require it.

A remediation is proven only when all of the following hold:

1. the original synthetic failing case no longer violates the contract;
2. the validation snapshot and consumption snapshot agree on the repaired invariant;
3. the canonical valid neighboring control still succeeds;
4. the intentionally invalid control remains rejected;
5. relevant sibling commands or lifecycle paths sharing the root cause are checked;
6. the previous bounded privileged effect or diagnostic disappears for the causal reason, not because instrumentation or the feature was removed.

Do not accept a fix that merely hides a crash, disables the interface, rejects all requests, or makes the lab unable to observe the contract.

## Remediation checks

Prefer shared invariants over one-input special cases. Centralize request decoding, ownership checks, state transitions, and lifecycle rules only where the command family truly shares those semantics.

Regression verification must replay the original synthetic request, a valid neighboring request, an intentionally invalid request, and any sibling/state path justified by the shared root cause.
