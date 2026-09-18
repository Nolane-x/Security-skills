# Wave 10 Profile #36 — File Upload Processing Causal Depth Design

**Date:** 2026-09-18  
**Base authority:** `main@78d3a60712479fbdfd8a87070a80f9829b5c1d09`  
**Canonical skill:** `file-upload-processing-analysis`

## Purpose

Promote `file-upload-processing-analysis` into the thirty-sixth CI-enforced operator-depth profile without changing routing, graph, packs, benchmark authority, agent-eval authority, superiority-court authority, or workflow semantics.

The current skill maps multipart parsing, names/metadata, temporary storage, validation/sniffing, transforms/extraction, permanent storage, serving, and cleanup. The missing operator contract is end-to-end artifact identity: exactly which byte/content generation, metadata/name representation, classification verdict, quarantine/temp object, scanner/parser/delegate result, derived artifact, storage object/version, serving policy, tenant/authorization state, and cleanup generation belong to the same upload transaction.

## Causal model

Every promoted finding must bind one reconstructable tuple:

`uploader principal/tenant identity + upload request/transaction identity/generation + fixture/content hash + raw artifact identity/generation + client filename representation + declared content-type/extension metadata + normalized name/storage-key result + temporary/quarantine object identity/generation + classification/sniff identity/generation + validator/scanner identity/version + validator/scanner verdict generation + parser/delegate identity/version + transform/extraction identity/generation + derived artifact/child identity/generation + promotion decision identity/generation + permanent storage object/key/version + metadata-to-bytes binding + serving/download policy identity/generation + serving origin/content-type/disposition identity + authorization/tenant binding + cleanup/tombstone lifecycle generation + downstream consumer identity + effective upload-pipeline capability + bounded result + receipt/result`

The proof must identify the first pipeline stage where identity, metadata, validation state, quarantine state, derived-object provenance, storage promotion, serving policy, or cleanup lifecycle becomes bound to the wrong artifact generation.

## Required distinctions

Preserve explicitly:

- upload request accepted != artifact validated;
- artifact validated != artifact promoted;
- artifact promoted != artifact served;
- served artifact != executable active content by assumption;
- client filename != canonical storage identity;
- normalized path != authorized storage namespace by assumption;
- generated object key != tenant authorization;
- same filename != same artifact generation;
- same content hash != same metadata/serving policy generation;
- declared MIME != observed content type;
- extension match != content validation;
- magic-byte match != complete format safety;
- content sniffing != parser validation;
- validator success != downstream delegate safety;
- scanner clean verdict != unchanged bytes;
- clean original != clean transformed derivative;
- clean parent archive != clean extracted child;
- parser success != safe serving policy;
- parser crash != code execution;
- converter invocation != unsafe delegate effect;
- harmless malformed fixture != active payload;
- temporary storage != quarantine guarantee;
- quarantine flag != immutable quarantined bytes;
- validation receipt != current artifact generation;
- transformed artifact != validated original by inheritance;
- derived preview != source artifact identity;
- archive child path != final canonical storage identity;
- object-store write success != intended object/version selected;
- permanent storage != public accessibility;
- public URL != authorization bypass by itself;
- inline serving != active-content execution by assumption;
- attachment disposition != safe content type by itself;
- cache hit != current serving-policy generation;
- cleanup requested != object inaccessible;
- tombstone written != all replicas/derivatives removed;
- duplicate upload != duplicate object effect by assumption;
- oversized metadata != resource-exhaustion proof;
- local benign policy difference != production exploitability.

## Upload transaction, principal, and artifact generations

Track independently:

- uploader principal/tenant identity;
- request identity/generation;
- upload transaction identity/generation;
- raw artifact identity and content hash;
- raw artifact generation;
- metadata/name generation;
- temporary/quarantine object generation;
- validation/scanning generation;
- transformation/derivative generation;
- permanent storage object/version generation;
- serving-policy generation;
- cleanup/tombstone generation.

A stable object key or filename does not collapse these generations.

## Representation and classification binding

For every stage capture:

- client filename;
- declared MIME/content type;
- extension;
- magic/sniffed type;
- normalized name/canonical storage result;
- archive member/path representation where relevant;
- generated object key;
- classification decision and generation;
- stage that consumes each representation.

`canonicalization-and-namespace-analysis` owns representation-to-identity normalization correctness. This profile owns whether the correct normalized identity/classification result is bound to the correct upload artifact generation and stage.

## Validation, scanning, and quarantine binding

Record:

- temp/quarantine object identity/generation;
- exact bytes/hash validated;
- validator/scanner identity/version;
- verdict generation;
- policy configuration generation;
- whether bytes/metadata can change after verdict;
- promotion preconditions;
- promotion decision generation;
- final artifact generation receiving the verdict.

A valid verdict for generation N cannot silently authorize generation N+1.

## Parser, delegate, transformation, and derived-artifact provenance

For each parser/delegate/transform record:

- input artifact identity/generation;
- parser/delegate identity/version;
- operation identity;
- output/derived artifact identity/generation;
- parent-child provenance;
- metadata transformations;
- classification/scanner inheritance policy;
- whether revalidation is required;
- bounded local result.

`parser-state-machine-analysis` owns parser-local automaton/state correctness. This profile owns cross-stage artifact and verdict provenance around the parser/delegate boundary.

## Storage promotion, object-version, and serving binding

For promotion and serving record:

- promoted artifact identity/generation;
- permanent storage bucket/namespace identity;
- object key;
- object version/generation;
- metadata-to-bytes binding;
- tenant/authorization binding;
- serving/download policy generation;
- serving origin;
- response content type;
- content disposition;
- cache/CDN policy generation where relevant;
- final object/version served to downstream consumer.

`cache-key-identity-analysis` owns semantic cache-key completeness. This profile binds the selected upload object/version and serving policy to the validated/promoted artifact.

## Cleanup, derivative, and lifecycle binding

Track:

- source object cleanup request generation;
- derivative/preview/extracted-child identities;
- tombstone/delete generation;
- object-store version visibility;
- cleanup completion receipt;
- serving-policy revocation generation;
- retained references/derived assets;
- final reachability state.

Cleanup requested != object inaccessible. A source deletion does not prove derivatives or older object versions are no longer served.

## Consumer and bounded-effect binding

For each promoted finding record:

- downstream consumer identity;
- exact object/version/derived artifact consumed;
- serving policy generation;
- tenant/authorization state;
- content type/disposition/origin state;
- effective upload-pipeline capability;
- bounded result;
- receipt/result.

Prefer read-only downloads, inert text/image fixtures, fake object stores, local preview renderers, mock delegates, shadow serving policies, and reversible owner-controlled markers.

## Evidence ladder

Use UPL0–UPL5 exactly:

- **UPL0 — Upload pipeline mapped.** Request, artifact, representations, temp/quarantine, validation/scanning, parser/delegate, transformation, storage, serving, and cleanup stages are identified.
- **UPL1 — Artifact/policy generation divergence observed.** A repeatable artifact, metadata, verdict, derived-object, storage-version, serving-policy, tenant, or cleanup generation mismatch exists without final wrong-context consumer acceptance.
- **UPL2 — Controlled upload-policy mismatch.** A deterministic local fixture proves a documented classification, validation, quarantine, revalidation, promotion, serving, tenant, or cleanup invariant can be violated.
- **UPL3 — Inert wrong-context artifact acceptance.** A mock/read-only consumer receives an artifact/derivative under the wrong validation, classification, storage-version, serving-policy, tenant, or lifecycle generation.
- **UPL4 — Bounded reversible upload effect.** A fake-object-store write, inert preview/serve marker, read-only download result, synthetic derivative, or reversible owner-controlled state transition is causally bound to the exact upload/artifact/verdict/storage/serving tuple.
- **UPL5 — Regression-verified causal upload proof.** UPL4 plus complete principal/request/artifact provenance, representation/classification trace, validation/quarantine/transform lineage, storage-version/serving-policy binding, cleanup lifecycle where relevant, meaningful counterfactuals, eliminated alternatives, receipt/result binding, and remediation replay.

Filename mismatches, MIME mismatches, parser crashes, scanner labels, public URLs, storage writes, or synthetic markers cannot skip missing causal bindings.

## Deterministic benign review cases

Freeze at least:

1. `scanner-verdict-reused-after-artifact-generation-change` — a clean verdict for temporary artifact generation N is reused after bytes/metadata advance to N+1 before promotion.
2. `derived-preview-inherits-source-verdict-without-revalidation` — a transformed preview/derivative receives the source artifact verdict despite being a distinct generation requiring revalidation.
3. `declared-mime-sniffed-type-serving-policy-mismatch` — validation consumes one benign classification while serving policy is selected from a conflicting representation, producing a bounded read-only policy mismatch.
4. `cleanup-removes-source-but-leaves-served-derivative-generation` — source cleanup succeeds while a derived preview/object version remains reachable under an older serving-policy generation.

Use inert text/image/document fixtures, fake archives without active content, mock scanners, local converters, fake object stores, read-only download/preview consumers, and bounded reversible markers only.

## Counterfactual requirements

Change exactly one causal variable while holding fixture content and final consumer constant, for example:

- current versus stale scanner verdict generation;
- source versus derived artifact identity;
- declared versus sniffed classification used for serving;
- current versus stale storage object version;
- source cleanup only versus source+derivative lifecycle revocation;
- intended versus wrong tenant/serving-policy generation.

## Alternative explanations

Before UPL4/UPL5 eliminate:

- bytes/hash are actually unchanged and verdict reuse is allowed;
- derivative is specification-equivalent and policy explicitly permits verdict inheritance;
- serving policy intentionally uses declared rather than sniffed type;
- content disposition/origin prevents the hypothesized active interpretation;
- object version selection is intentional;
- authorization/tenant policy independently explains the result;
- canonicalization defect is the independent root cause;
- parser-local state bug independently explains the observation;
- cache-key mismatch independently selects stale policy/content;
- cleanup is explicitly asynchronous and receipt is not a completion signal;
- fixture accidentally contains active content;
- receipt belongs to another upload/object/version/consumer generation.

Any unresolved material alternative caps evidence at UPL2.

## Ownership boundaries

- This profile owns end-to-end upload artifact/verdict/derived-object/storage/serving/cleanup lineage.
- `canonicalization-and-namespace-analysis` owns path/name/key normalization and resolved namespace identity.
- `parser-state-machine-analysis` owns parser-local state/phase/transition mechanics.
- `cache-key-identity-analysis` owns cache-key semantic dependency completeness.
- `authorization-boundary-analysis` and tenant-isolation profiles own authorization/tenant policy semantics; this profile binds those decisions to the selected upload object/version.
- `concurrency-race-analysis` owns scheduler/happens-before races; this profile may record generation skew without claiming a race root cause.
- Active malware development, destructive archives, resource exhaustion, credential-bearing fixtures, and external delegates outside the lab are out of scope.

## Expected repository scope

1. `README.md`
2. `docs/operator-depth-contract.md`
3. `docs/superpowers/plans/2026-09-18-wave10-file-upload-processing-depth.md`
4. `docs/superpowers/specs/2026-09-18-wave10-file-upload-processing-depth-design.md`
5. `operator-depth/profiles.json`
6. `skills/file-upload-processing-analysis/SKILL.md`
7. `skills/file-upload-processing-analysis/references/operator-review-cases.json`
8. `skills/file-upload-processing-analysis/references/operator-runbook.md`
9. `tests/test_file_upload_processing_depth.py`
10. `tests/test_oracle_external_data_trust_depth.py` only if behavioral CI proves its exact global-count assertion is the sole extensibility defect.

Do not change `skill.meta.json`, graph edges, packs, routing domains, benchmark authority, agent-eval authority, superiority-court authority, or workflow semantics.

## Success criterion

Profile #36 is complete only when the merge tree contains exactly 36 profiles, exactly one valid `file-upload-processing-analysis` entry, UPL0–UPL5 is published, exact-head and post-merge CI are fully GREEN, merge parents are verified, and final scope remains bounded to the intended paths.
