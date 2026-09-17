---
name: boot-chain-and-secure-boot-analysis
description: "Analyze embedded/firmware boot trust chains from immutable root through loaders, configuration, measured/verified boot, handoff state, recovery, and runtime policy. Use to reason about verification gaps without weaponizing boot bypasses."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Boot Chain And Secure Boot Analysis

## When to use

Use when reviewing ROM/first-stage boot, UEFI-like flows, secure boot, measured boot, verified partitions, recovery loaders, anti-rollback, boot slots, or handoff configuration. The goal is to establish causal trust bindings, not to infer compromise from configuration or verification output alone.

## Preconditions

1. Use owned lab hardware with documented recovery, emulation, or deterministic synthetic fixtures.
2. Pin root/key state, active policy generation, firmware versions, boot mode, slot state, rollback domains, and relevant configuration.
3. Use synthetic keys, benign images, mock loaders, inert next stages, and read-only traces wherever possible.
4. Do not alter irreversible fuses/keys, disable platform security persistently, or introduce production signing material.

## Causal boot-chain model

Reason about the complete chain rather than isolated verifier calls:

```text
immutable or policy root-of-trust identity -> active verification-policy/key generation -> boot mode and path identity -> boot target/slot/component selection -> candidate component identity and digest -> signature/measurement result -> signer or verification authority decision -> version/rollback generation decision -> accepted component identity -> loaded/executed component identity -> verified-to-loaded binding -> handoff state and next-stage security context -> next-stage trust inheritance -> bounded synthetic boot outcome -> receipt/log/attestation binding -> lifecycle, revocation, rollback, and recovery generation
```

Every promoted claim must preserve the material identity, authority, freshness, selection, load, and handoff links that the claim depends on. A missing link lowers the evidence ceiling.

Important invariants:

- measured boot != verified boot or enforcement;
- signature validity != authorized boot signer or active verification authority;
- root-key presence != proof that the active path chains to that root;
- candidate artifact identity != selected artifact identity;
- selected artifact identity != loaded/executed artifact identity;
- digest match != approved version or rollback generation;
- rollback metadata presence != monotonic rollback enforcement;
- verified update/install != boot selection or execution;
- verification of one stage != authenticated handoff to the next stage;
- recovery/alternate slot path != equivalent verification policy by assumption;
- valid key/certificate != active authorized key generation;
- a measurement or attestation receipt != local enforcement unless identity and freshness bindings are independently established.

## Root, policy, and signer authority

Identify the actual root or policy object consulted by the active boot path. Record root identity, policy generation, active/revoked signer state, key-transition rules, and the authoritative component that makes the signer-authorization decision.

Cryptographic validity proves that bytes verify under a key. It does not prove that the key is authorized for this stage, boot mode, component class, hardware identity, rollback generation, or current policy epoch. A development/manufacturing key that is intentionally accepted in a lab mode must not be used to prove release-mode impact.

## Component selection and identity

Trace the selector inputs that choose a candidate: boot mode, A/B slot metadata, partition identifiers, recovery flags, fallback counters, component class, and any mutable configuration. Bind the candidate identity to immutable or authenticated metadata where the design requires it.

Do not collapse these identities:

```text
candidate component
!= verified/accepted component by assumption
!= selected component by assumption
!= loaded/executed component by assumption
```

A useful controlled fixture gives neighboring synthetic components distinguishable identities so selection and load can be observed without executing untrusted functionality.

## Selected-versus-loaded binding

A verifier may authenticate one object while a later loader reads another source, offset, slot, partition, cached buffer, decompressed output, or transformed representation. Record the verification output and the exact bytes/identity delivered to the next stage.

Require a verified-to-loaded binding before promoting a claim about execution. Safe proof can use synthetic markers, mock loader receipts, digest traces, or an inert next-stage consumer. Do not require arbitrary code execution.

## Rollback and freshness generation

For every protected component, record the rollback domain, authoritative counter or version state, comparison semantics, update ordering, and generation at both acceptance and boot time. Distinguish existence of rollback metadata from monotonic enforcement.

Model restart, staged update, failed-boot fallback, A/B slot switch, partial update, power-loss recovery, counter commit, key rotation, and policy revocation as generation transitions. A stale artifact accepted after the authoritative generation advances is a separate hypothesis requiring a generation-aware control.

## Handoff and next-stage inheritance

Verification of stage N does not automatically authenticate every value handed to stage N+1. Record which handoff fields are measured, authenticated, recomputed, or trusted; which stage owns them; and how the next-stage consumer validates them.

Security-sensitive mutable handoff state can include memory maps, boot arguments, selected policy identifiers, device-tree/configuration data, recovery state, component locations, or synthetic equivalents. Prove that the next stage consumes the same authenticated identity/policy context rather than a mutable neighbor.

## Recovery and alternate-path reasoning

Enumerate recovery, fallback, alternate slot, removable/local boot, manufacturing, debug, rescue, and failed-boot paths that are in scope. For each path, compare root/policy generation, signer authority, component binding, rollback enforcement, and handoff semantics with the normal path.

An intentional recovery exception is not automatically a vulnerability. Conversely, proof on the normal path does not establish equivalent enforcement on an alternate path. Use synthetic path markers and owner-controlled emulator states to compare behavior safely.

## Workflow

1. Map every boot stage, transition, selector, verification/measurement point, root/policy source, rollback domain, and alternate path.
2. Form a transition-level hypothesis naming the expected root/policy generation, candidate, selected component, loaded component, handoff consumer, and freshness state.
3. Capture the authoritative identity/decision at each edge before mutating a fixture.
4. Run a positive control proving the intended current synthetic artifact succeeds.
5. Change one security-relevant binding at a time for a negative/counterfactual control.
6. Observe acceptance/rejection using inert markers, mock loaders, read-only traces, or reversible emulator effects.
7. Eliminate fallback, stale logging, debug/manufacturing policy, selector retry, and previous-generation artifacts as alternative explanations.
8. After remediation, rerun both the blocked failing fixture and neighboring legitimate boot flow.

## Boot-chain evidence ladder

### BC0 — surface mapped

Stages, roots, modes, selectors, verification points, rollback state, and alternate paths are identified. No trust failure is established.

### BC1 — identity or generation divergence observed

A candidate/selected/loaded component, signer/policy generation, boot path, slot, handoff state, or rollback identity differs from expectation without proving wrongful acceptance.

### BC2 — verification/selection policy mismatch demonstrated

A deterministic fixture shows that signer resolution, policy generation, version decision, selected component, or transition binding differs from the intended rule. No boot effect is required.

### BC3 — inert unauthorized acceptance

A benign synthetic marker, component, or handoff value is accepted under an identity/authority/generation tuple that should be rejected.

### BC4 — bounded synthetic boot effect

BC3 reaches a reversible owner-controlled emulator/lab outcome through the exact path under review: for example a harmless marker component is selected/loaded, an inert mock next stage receives the wrong handoff identity, or a read-only synthetic receipt is produced.

### BC5 — causal boot-chain proof

BC4 plus exact root/policy provenance, signer authorization, rollback/freshness generation, selected-to-loaded identity binding, transition/handoff trace, relevant alternate-path control, meaningful counterfactuals, eliminated alternative explanations, and remediation regression preserving legitimate neighboring behavior.

## Counterfactual proof

Prefer controls that change one binding while holding the rest constant:

- same bytes signed by an authorized-current vs revoked/stale synthetic signer;
- same signature-valid object under a different active policy generation;
- same component under current vs stale rollback generation;
- same verified candidate with a neighboring synthetic slot selected;
- same verification receipt while the mock loader exposes a distinguishable loaded identity;
- same image with authenticated vs unauthenticated handoff state;
- normal path vs recovery/alternate path under equivalent synthetic policy;
- same receipt shape with a different boot-generation correlation identity.

A counterfactual is evidence only when the changed dimension is authoritative for the transition being claimed.

## Alternative explanations

Actively test explanations such as expected fallback after failed boot, stale logs or measurements, harness attachment to a previous boot generation, retry/slot semantics, policy propagation delay, intentional development keys, debug/manufacturing mode, emulator-only behavior, selector cache, expected recovery exception, or verification of a file different from the bytes later loaded.

Do not promote evidence until plausible alternatives relevant to the observed behavior are eliminated or explicitly bound into the evidence ceiling.

## Evidence capture

For each material transition, record:

```text
boot generation:
boot mode/path:
root-of-trust identity:
verification-policy/key generation:
selector state:
candidate component identity/digest/version:
signer identity and authorization decision:
rollback domain/generation:
selected component identity:
loaded/executed component identity:
verified-to-loaded binding:
handoff state and next-stage consumer:
recovery/alternate-path state:
bounded result/receipt identity:
counterfactual result:
alternative explanations excluded:
evidence level and ceiling:
```

## Evidence ceiling

A secure-boot-enabled flag, a signature-valid result, measurement entry, attestation quote, configuration string, successful update, boot-success log, parser rejection, or crash cannot by itself exceed the identity/authority transitions it directly proves.

BC4/BC5 require bounded causal acceptance through the exact root/policy/selection/load/handoff chain. If selected-versus-loaded identity, signer authorization, rollback generation, or result correlation is missing, cap the claim below causal boot-chain proof.

## Evidence contract

Preserve boot generation, boot mode/path, root-of-trust identity, active verification-policy/key generation, candidate component identity/digest/version, signer identity and signer-authorization decision, rollback domain/generation, selector state, selected component identity, loaded/executed component identity, verified-to-loaded binding, handoff state and next-stage consumer, recovery/alternate-path state, bounded result/receipt correlation, positive/negative controls, counterfactuals, eliminated alternative explanations, remediation regression, and the final BC evidence level/ceiling. Evidence may not claim a later transition that these bindings do not directly establish.

## Stop conditions

Stop if validation would require irreversible fuse/key changes, production signing-key compromise, destructive flashing, persistent security disablement, unrecoverable device state, boot-bypass weaponization, arbitrary code execution, or any unauthorized/third-party target.

## Output

```text
boot stages and transitions:
root/policy generations:
component selection identities:
signer authorization:
rollback/freshness state:
selected-versus-loaded binding:
handoff inheritance:
recovery/alternate paths:
controls and counterfactuals:
bounded result:
evidence level/ceiling:
remediation regression:
```
