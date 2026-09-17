# Wave 10 Profile #22 — Certificate And Hostname Trust Depth Implementation Plan

Base authority: `main@0638eb26c8d66226afc3e856e58327f470a2b537`.

Target skill: `certificate-and-hostname-validation-analysis`.

Design authority: `docs/superpowers/specs/2026-09-17-wave10-certificate-hostname-depth-design.md`.

## Objective

Promote `certificate-and-hostname-validation-analysis` into the twenty-second CI-enforced operator-depth profile without creating duplicate canonical capabilities or changing routing, benchmark, agent-eval, superiority-court, or workflow authority.

The implementation must freeze causal peer-identity reasoning across endpoint/reference identity, certification path, trust anchor, certificate constraints, pin/revocation/callback policy, final authenticated peer/session identity, lifecycle generations, downstream consumer, result/receipt binding, counterfactuals, and a PKI0–PKI5 evidence ceiling.

## Exact final scope

Exactly nine paths are allowed:

1. `README.md`
2. `docs/operator-depth-contract.md`
3. `docs/superpowers/specs/2026-09-17-wave10-certificate-hostname-depth-design.md`
4. `docs/superpowers/plans/2026-09-17-wave10-certificate-hostname-depth.md`
5. `operator-depth/profiles.json`
6. `skills/certificate-and-hostname-validation-analysis/SKILL.md`
7. `skills/certificate-and-hostname-validation-analysis/references/operator-review-cases.json`
8. `skills/certificate-and-hostname-validation-analysis/references/operator-runbook.md`
9. `tests/test_certificate_hostname_depth.py`

No `skill.meta.json`, graph, pack, routing, benchmark authority, agent-eval authority, superiority-court authority, or workflow-semantic changes.

## Phase 1 — TDD RED

Create `tests/test_certificate_hostname_depth.py` before production artifacts.

The dedicated test must freeze four groups and make each group fail independently while the profile is missing:

1. canonical skill depth;
2. operator runbook depth;
3. deterministic review-case depth;
4. registry integration/count.

The canonical-skill group must require:

- the full request/service-intent → endpoint/redirect/transport/SNI → canonical reference identity → verifier/trust-store generation → presented chain → selected path/anchor → certificate constraints → hostname/service identity → pin/revocation → callback/final decision → authenticated peer/session → consumer/result → lifecycle chain;
- distinctions including chain-valid ≠ hostname-valid, root trust ≠ peer authorization, SNI ≠ reference identity, pin match ≠ complete validation, callback invocation ≠ final acceptance, certificate acceptance ≠ mTLS account authorization, and session resumption ≠ current policy generation;
- PKI0–PKI5 evidence ladder and ceiling;
- counterfactual and alternative-explanation methodology;
- explicit benign/local authorization boundary.

The runbook group must require common operator-depth sections plus peer/endpoint identity, path/anchor, certificate constraints, pin/revocation/callback, session/lifecycle, result binding, counterfactual, alternatives, and PKI evidence sections.

The review-case group must require at least three cases and common fields:

- `id`
- `hypothesis`
- `safe_oracle`
- `positive_control`
- `negative_control`
- `stop_condition`
- `remediation_oracle`

It must additionally require substantive PKI fields covering intended peer identity, endpoint/SNI/reference identity, verifier, trust-store generation, chain/path/anchor, certificate constraints, SAN/name match, pin/revocation/callback state, final decision, authenticated peer/session, consumer/result/receipt, lifecycle generation, counterfactual, alternatives, evidence level, and evidence ceiling.

The registry group must require schema version 2, exactly 22 profiles, exactly one certificate/hostname entry, the new review-case path, and `lab_only: true`.

Open a Draft PR at the exact test-first SHA before any production implementation. Capture the RED workflow run. RED is valid only if the four intended groups fail with zero unittest errors and pre-existing authorities pass before the dedicated failures.

## Phase 2 — Minimal behavioral implementation

Do not modify the dedicated test after valid RED unless the test itself is objectively wrong.

Update `skills/certificate-and-hostname-validation-analysis/SKILL.md` to encode the causal model, distinctions/invariants, PKI0–PKI5 ladder, counterfactuals, alternative explanations, evidence ceiling, lifecycle/session semantics, and safe validation boundary.

Create `references/operator-runbook.md` with required common sections and transition-oriented validation. Emphasize exact identity and generation traces rather than certificate payload volume.

Create `references/operator-review-cases.json` with at least these deterministic benign cases:

- `peer-reference-identity-binding`;
- `callback-pin-effective-decision-binding`;
- `trust-policy-session-generation-binding`.

Update `operator-depth/profiles.json` with exactly one new profile entry pointing to `references/operator-runbook.md` and `references/operator-review-cases.json`, `lab_only: true`, retaining schema version 2.

No public README/operator contract change in this phase.

## Phase 3 — Behavioral verification

Require a full PR workflow on the behavioral candidate:

- Linux Python 3.11 and 3.13;
- macOS Python 3.11 and 3.13;
- Windows Python 3.11 and 3.13;
- `benchmark-core`;
- `agent-eval-core`;
- `superiority-court-core`.

All nine jobs must pass. Benchmark/agent/court deterministic outputs must remain byte-identical; cautious/faulty replay controls must still behave as expected.

If a test fails, identify root cause and make the narrowest production fix. Do not weaken the test to accommodate incomplete semantics.

## Phase 4 — Public documentation only after behavioral GREEN

Only after the behavioral candidate is full GREEN:

- update README counts from 21 to 22;
- identify `certificate-and-hostname-validation-analysis` as the twenty-second Wave 10 profile;
- summarize peer-identity/path/anchor/policy/callback/session/lifecycle depth and PKI0–PKI5;
- update `docs/operator-depth-contract.md` with the same profile and causal evidence ladder.

Prove the delta from behavioral authority to final candidate is exactly those two documentation files.

## Phase 5 — Exact-head verification and guarded integration

Require full 9/9 CI on the exact final head. Do not create commits after exact-head GREEN.

Fresh-check immediately before merge:

- PR head equals exact-green SHA;
- PR base equals the current `main` SHA used by the branch;
- current `main` has not drifted;
- PR is mergeable;
- changed files are exactly the nine expected paths;
- no forbidden authority files changed.

Mark ready and merge using `expected_head_sha` equal to the exact final head.

## Phase 6 — Post-merge verification and closure

Verify merge commit parents are exactly:

1. expected base/main SHA;
2. exact reviewed PR head SHA.

Require the push-triggered full 9/9 workflow to complete successfully on the exact merge SHA.

Read directly from the merge tree:

- `operator-depth/profiles.json` — schema v2, 22 entries, exactly one certificate/hostname profile, correct paths, `lab_only: true`;
- `README.md` — 22 profiles and profile #22 published;
- `docs/operator-depth-contract.md` — profile #22 and PKI0–PKI5 published.

Only then add the closure provenance comment containing design, plan, test-first SHA, RED run, behavioral authority/run, exact final head/run, merge SHA/parents, post-merge run, exact scope, safety boundary, and non-claim.

## Safety

Use only local/owned/sandbox/benchmark/explicitly authorized TLS endpoints, synthetic CAs/certificates, fake host/service identities, mock trust stores, inert consumers, read-only traces, and bounded reversible owner-controlled session effects.

Do not require real third-party impersonation, unrelated traffic interception, real production client certificates, credential theft, persistence, malware, destruction, evasion, or unauthorized testing.

## Completion definition

Profile #22 is complete only after the closure comment is written following successful post-merge verification. A green PR alone, a successful merge alone, or a successful subset of CI is not completion.