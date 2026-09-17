# Wave 10 profile #22 — certificate and hostname validation depth implementation plan

## Objective

Promote `certificate-and-hostname-validation-analysis` from its existing shallow canonical form into the twenty-second CI-enforced operator-depth profile while preserving repository authorities, deterministic evaluation behavior, and strict safety boundaries.

Base commit: `0638eb26c8d66226afc3e856e58327f470a2b537`.

Branch: `wave10-profile22-certificate-hostname-validation-depth`.

## Task 1 — freeze behavior with a dedicated RED test

Create `tests/test_certificate_hostname_validation_depth.py` before any production artifact changes.

The test must assert four independent contract groups:

1. canonical `SKILL.md` contains the causal peer-identity/path/name/override/lifecycle model, required distinctions, PKI0–PKI5, counterfactuals, alternative explanations, and evidence ceiling;
2. `references/operator-runbook.md` exists and exposes transition-level sections for reference identity, path/trust anchor, SAN/name matching, callback/pin/revocation state, authenticated session/result binding, lifecycle generations, controls, evidence promotion, and remediation;
3. `references/operator-review-cases.json` exists, has at least three substantive deterministic benign cases with required machine fields and the three frozen IDs;
4. `operator-depth/profiles.json` has exactly 22 profiles and exactly one `certificate-and-hostname-validation-analysis` registration pointing at the runbook/review-cases with `lab_only: true`.

Commit only the test after the design/plan commits. Open a Draft PR on this exact test-first head. Observe CI RED caused by the new dedicated test, not syntax/import errors or pre-existing regressions.

## Task 2 — implement the canonical causal contract

Update `skills/certificate-and-hostname-validation-analysis/SKILL.md` without touching `skill.meta.json`.

Required sections:

- `## Causal peer-authentication model`
- `## Reference identity and endpoint binding`
- `## Certificate path and trust-anchor binding`
- `## SAN and hostname/reference-identity reasoning`
- `## Callback, pin, and revocation composition`
- `## Authenticated session and consumer binding`
- `## Lifecycle and generation reasoning`
- `## Certificate evidence ladder`
- `## Counterfactual proof`
- `## Alternative explanations`
- `## Evidence ceiling`

Freeze the approved end-to-end causal chain and non-equivalences exactly enough for deterministic tests while keeping the text vendor-neutral and defensive.

## Task 3 — add the operator runbook

Create `skills/certificate-and-hostname-validation-analysis/references/operator-runbook.md`.

It must include the common required sections:

- Attack surface
- Hypothesis matrix
- Controlled validation
- False-positive controls
- Evidence capture
- Remediation checks

It must additionally include domain-specific sections:

- Reference identity, endpoint, redirect, and SNI trace
- Trust store, path building, and trust-anchor trace
- Certificate constraints and validity trace
- SAN/canonical reference-identity and name-match trace
- Callback/override, pin, and revocation trace
- Authenticated peer/session and privileged-consumer trace
- Lifecycle/trust/pin/revocation/session generation trace
- Counterfactual controls
- Alternative explanations
- Evidence promotion and ceiling

Validation must remain local/owned/sandboxed and synthetic.

## Task 4 — add deterministic benign review cases

Create `skills/certificate-and-hostname-validation-analysis/references/operator-review-cases.json` with `version: 1` and at least these three scenario IDs:

- `chain-vs-reference-identity-binding`
- `callback-pin-effective-decision-binding`
- `trust-policy-session-generation-binding`

Every scenario must contain non-trivial strings for:

- `hypothesis`
- `safe_oracle`
- `positive_control`
- `negative_control`
- `stop_condition`
- `remediation_oracle`
- `intended_peer_identity`
- `endpoint_redirect_sni_state`
- `verification_reference_identity`
- `verifier_configuration`
- `trust_store_identity`
- `trust_store_generation`
- `presented_chain_identity`
- `path_building_state`
- `selected_trust_anchor`
- `certificate_constraints_state`
- `san_reference_identity_state`
- `canonical_reference_identity`
- `hostname_identity_match_decision`
- `pin_policy_state`
- `revocation_policy_state`
- `callback_override_state`
- `effective_accept_reject_decision`
- `authenticated_peer_session_identity`
- `privileged_consumer`
- `bounded_result`
- `receipt_result_binding`
- `lifecycle_generation`
- `counterfactual_control`
- `alternative_explanation`
- `evidence_level`
- `evidence_ceiling`

The evidence fields must use `PKI0` through `PKI5`.

## Task 5 — register exactly one new profile

Update `operator-depth/profiles.json` only by adding one alphabetically appropriate entry for `certificate-and-hostname-validation-analysis`:

- runbook: `references/operator-runbook.md`
- scenario matrix: `references/operator-review-cases.json`
- `lab_only: true`
- unchanged six common required runbook sections.

Profile count becomes exactly 22.

## Task 6 — behavioral CI authority

Do not alter the dedicated test after valid RED.

Push the implementation artifacts and require the full repository workflow to complete with all nine jobs green:

- Linux Python 3.11
- Linux Python 3.13
- macOS Python 3.11
- macOS Python 3.13
- Windows Python 3.11
- Windows Python 3.13
- benchmark-core
- agent-eval-core
- superiority-court-core

Deterministic byte-identical checks and cautious/faulty replay controls must remain green.

If a failure occurs, diagnose the exact failing semantic assertion and change production artifacts only unless the test itself is demonstrably incorrect.

## Task 7 — docs-only publication after behavioral GREEN

Only after Task 6 is fully green:

- update `README.md` from 21 to 22 operator-depth profiles and publish `certificate-and-hostname-validation-analysis` as the twenty-second profile;
- update `docs/operator-depth-contract.md` with the profile summary and PKI0–PKI5 causal ladder.

The delta from behavioral authority to final candidate must be exactly those two public documentation files.

## Task 8 — exact-head verification and guarded merge

Require a new full CI run on the exact final candidate SHA and all nine jobs green.

Then verify freshly:

- `main` has not drifted from the PR base;
- PR head equals the exact green candidate;
- PR is mergeable;
- changed paths are exactly the expected nine;
- no new commit exists after exact-head green.

Mark the Draft PR ready and merge using `expected_head_sha` equal to the exact reviewed final head.

## Task 9 — post-merge verification and closure

Verify the merge commit has exactly two expected parents: pre-merge `main` and final reviewed PR head.

Require post-merge push CI on the exact merge SHA with all nine jobs green.

Read from the merge tree:

- `operator-depth/profiles.json` — version 2, exactly 22 profiles, exactly one certificate/hostname entry, correct paths, `lab_only: true`;
- `README.md` — 22 profiles and certificate/hostname identified as #22;
- `docs/operator-depth-contract.md` — #22 and PKI0–PKI5 causal semantics.

Finally add a closure provenance comment recording RED, behavioral GREEN, exact-head GREEN, guarded merge SHA/parents, post-merge GREEN, exact scope, safety boundary, and no external-superiority claim.