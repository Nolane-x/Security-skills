# Boot Chain And Secure Boot — Operator Runbook

Use this runbook only for local emulators, owned recoverable lab devices, deterministic benchmark fixtures, synthetic keys/components, mock loaders, inert next stages, read-only traces, or bounded reversible effects. It is a causal review protocol, not a boot-bypass procedure.

## Attack surface

Map immutable roots, policy stores, signer/key generations, ROM/first-stage loaders, selectors, A/B slots, recovery/fallback paths, verification and measurement calls, rollback domains, mutable boot configuration, loader sources, handoff state, next-stage consumers, logs/measurements/attestation, and all mode transitions in scope.

For every surface, name the authoritative identity and the generation that should govern it. Treat debug/manufacturing modes as separate policy domains from release mode.

## Hypothesis matrix

Write hypotheses as explicit transition failures rather than vague statements such as “secure boot may be bypassable.” Example columns are expected root/policy generation, boot mode/path, candidate identity, signer authorization, rollback generation, selected component, loaded component, handoff consumer, expected decision, controlled mutation, safe oracle, and evidence ceiling.

A useful hypothesis predicts both the positive control and a neighboring counterfactual.

## Root-of-trust and policy-generation trace

Record the synthetic/owned root identity actually consulted by the path, the active verification-policy generation, accepted/revoked signer set, key-transition state, and the component that makes the authorization decision. Distinguish key validity from signer authorization for the specific stage and generation.

Trace root/policy lookup to the decision point. Do not infer active authority merely because a key or certificate exists in storage.

## Boot-mode and path trace

Record release/recovery/fallback/debug/manufacturing mode, path-selection inputs, retry/failure counters, slot state, and mode-generation transitions. Confirm the harness is observing the intended current boot generation rather than a previous run.

Normal-path evidence does not automatically cover a recovery path or alternate path.

## Component selection and identity trace

Trace selector inputs to the exact candidate and selected component identities. Record slot/partition/component class, authenticated selector metadata, digest/version identity, and any mutable state that can redirect selection.

Use distinguishable synthetic markers when possible so candidate identity and selected component identity cannot be confused.

## Signature and signer-authority trace

Capture authenticated bytes/metadata, signature result, signer identity, root/policy resolution, and the stage-specific signer authorization decision. A valid signature under a non-authorized or stale signer generation is not equivalent to authorization.

When measurement is present, keep the invariant explicit: measurement != enforcement. A measurement record can support provenance only for the object and generation it actually binds.

## Rollback and freshness-generation trace

Record rollback domain, authoritative counter/version, comparison rule, current generation, candidate generation, when state is committed, and behavior across slot switches, failed boots, staged updates, power interruption, policy/key rotation, and revocation.

Rollback generation must be proved at the acceptance and boot transition that matters. Metadata presence is not monotonic enforcement.

## Selected-versus-loaded binding trace

Record the selected component identity and the loaded component identity independently. Trace source/slot/offset/cache/transformation from the verified object to bytes delivered to the next stage.

Require a verified-to-loaded binding before claiming that verification governed execution. A safe oracle can be a mock-loader digest receipt or an inert next-stage marker; arbitrary code execution is unnecessary and out of scope.

## Handoff and next-stage inheritance trace

List security-sensitive handoff state, its owner, authentication/measurement status, generation, and the next-stage consumer. Record which values the consumer recomputes or independently validates.

A verified stage does not make mutable handoff state authoritative by inheritance. Prove the next-stage security context is bound to the same accepted component/policy generation.

## Recovery and alternate-path equivalence trace

For every relevant recovery path and alternate path, compare root/policy generation, signer authorization, rollback rules, selected-versus-loaded behavior, handoff validation, and resulting bounded oracle with the normal path.

Intentional recovery exceptions must be documented as policy, not silently promoted to vulnerabilities. Conversely, equivalence cannot be assumed solely because the same verifier library is called.

## Receipt, measurement, and attestation trace

Bind boot logs, measurement records, synthetic receipts, and attestation evidence to boot generation, component identity, policy generation, and result correlation. Attestation is evidence about the claims actually covered by the signed/measured data; it is not proof of local enforcement outside those bindings.

Reject stale telemetry, previous-generation receipts, or correlation ambiguity as causal proof.

## Lifecycle/revocation generation trace

Trace key rotation/revocation, policy update, rollback counter changes, bootloader update, slot activation, recovery transition, fallback, retry, restart, and handoff-state regeneration. Record which stale identities are invalidated at each generation advance.

A stale component, selector result, signer, cached decision, or handoff state accepted after the authoritative generation changes needs its own counterfactual.

## Controlled validation

1. Establish a positive control with a current authorized synthetic component.
2. Capture root/policy, selector, signature, rollback, selected, loaded, handoff, and receipt identities.
3. Change one security-relevant binding only.
4. Observe reject/accept using an emulator, mock loader, inert next stage, read-only trace, or reversible owner-controlled effect.
5. Restore the baseline and repeat to exclude fixture drift.
6. Promote evidence only to the highest transition actually proven.

Never modify irreversible fuses, use production signing keys, destructively flash a device, or disable platform security persistently.

## False-positive controls

Check for expected fallback, stale logging/measurement, wrong harness boot generation, normal A/B retry behavior, policy propagation delay, intentional development keys, debug/manufacturing mode, documented recovery exceptions, emulator-only shortcuts, selector caching, and mismatch between the artifact inspected and the one actually loaded.

A surprising acceptance is not enough until these explanations are excluded where relevant.

## Counterfactual controls

Useful controls include same bytes under current vs stale signer generation, same valid signature after signer revocation, current vs stale rollback generation, same candidate with a neighboring synthetic slot, same verification result with distinguishable loaded bytes in a mock loader, authenticated vs mutable handoff state, and normal vs recovery path with equivalent synthetic policy.

Keep all non-tested dimensions stable and record the authoritative variable that changed.

## Alternative explanations

For each promoted claim, write at least one plausible alternative explanation and the observation that rules it out. Examples include fallback after an intentionally failed positive control, a receipt from the prior boot, delayed policy state, expected recovery behavior, debug-only acceptance, or the verifier and loader referring to different fixture paths.

If an alternative explanation remains live, lower the evidence ceiling rather than filling the gap by inference.

## Evidence capture

Capture compact transition evidence: boot generation; mode/path; root identity; policy/key generation; candidate/digest/version; signer and authorization decision; rollback domain/generation; selector state; selected component; loaded component; verified-to-loaded receipt; handoff state and next-stage consumer; alternate/recovery state; bounded result; counterfactual; and eliminated alternatives.

Prefer synthetic IDs and hashes. Do not collect production secrets or require real signing material.

## Evidence promotion and ceiling

Use BC0–BC5 from the canonical skill. Surface mapping is BC0; divergence without wrongful acceptance is BC1; deterministic policy/selection mismatch is BC2; inert unauthorized acceptance is BC3; a bounded reversible synthetic effect is BC4; BC5 additionally requires the complete identity/authority/generation/handoff chain, counterfactuals, alternative-explanation elimination, and remediation regression.

Secure-boot flags, signature success, measurements, attestation, update success, logs, crashes, or static configuration cannot leap over missing causal bindings. Missing signer authorization, rollback generation, selected-versus-loaded proof, handoff identity, or receipt correlation lowers the evidence ceiling.

## Remediation checks

After a fix, rerun the exact failing synthetic fixture and require rejection at the intended transition. Then prove the current authorized neighboring component still follows the intended selector, verifier, rollback, loader, handoff, recovery, and receipt path.

Verify stale signer/policy/component/handoff generations do not regain authority after restart, slot switch, recovery transition, or cache reuse. Record the final BC level without claiming exploitability or external-system superiority beyond the evidence.