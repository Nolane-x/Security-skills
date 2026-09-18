# File Upload Processing Operator Runbook

Use this runbook only for local, owned, sandboxed, staging, benchmark/CTF, simulated, or explicitly authorized systems. Fixtures must be inert and non-destructive. Do not use active malware, credential-bearing files, destructive archives, uncontrolled resource exhaustion, or external delegates outside the lab.

## Attack surface

Map:

- uploader principal/tenant;
- upload request generation and upload transaction generation;
- raw artifact identity, hash, and metadata;
- client filename, extension, declared MIME, and sniffed type;
- normalized storage identity;
- temporary/quarantine objects;
- scanner/validator identities and verdict generations;
- parser/delegate/transform stages;
- derived artifact/child generations;
- promotion decisions;
- permanent storage object/key/version;
- serving origin/type/disposition and policy generation;
- authorization/tenant binding;
- cleanup/tombstone lifecycle;
- final downstream consumers.

## Hypothesis matrix

| Hypothesis | Safe oracle | Control |
| --- | --- | --- |
| stale scanner verdict authorizes new artifact generation | fake scanner and object store expose only inert hashes/verdict generations | current-generation verdict is required before promotion |
| derivative inherits source verdict incorrectly | local converter creates inert text/image preview and read-only policy receipt | revalidation of derivative permits intended preview |
| validation and serving use conflicting classifications | synthetic benign bytes expose declared/sniffed type decision | serving policy uses the same authoritative classification |
| cleanup leaves derivative reachable | fake object store/read-only downloader exposes only derivative reachability | lifecycle revocation removes source and derivatives |

## Upload/principal/artifact-generation trace

Record:

- uploader principal/tenant identity;
- upload request/transaction identity and generation;
- fixture/content hash;
- raw artifact identity and artifact generation;
- filename/metadata generation;
- temp/quarantine generation;
- validation generation;
- derivative generation;
- permanent object/version generation;
- serving-policy generation;
- cleanup/tombstone generation.

Do not equate stable filename, hash, or object key with stable artifact lifecycle generation.

## Representation/classification trace

Capture:

- client filename;
- extension;
- declared content type;
- magic/sniffed type;
- classification identity/generation;
- normalized name/storage-key result;
- archive-member representation if relevant;
- generated object key;
- stage consuming each representation.

Use only benign mismatches such as inert text/image/document fixtures.

## Validation/scanning/quarantine trace

Capture:

- temp/quarantine object identity/generation;
- exact bytes/hash checked;
- scanner/validator identity/version;
- scanner verdict generation;
- policy/configuration generation;
- quarantine state;
- whether bytes/metadata changed after verdict;
- promotion decision generation;
- final artifact generation receiving the verdict.

A scanner verdict is evidence about the exact checked generation, not future derivatives or replacements.

## Parser/delegate/derived-artifact trace

Record:

- input artifact generation;
- parser/delegate identity/version;
- transform/extraction operation;
- derived artifact/child identity/generation;
- parent-child provenance;
- metadata changes;
- verdict/classification inheritance policy;
- revalidation requirement;
- bounded local result.

Keep parser-state-machine mechanics in the parser profile; this trace is about cross-stage artifact provenance.

## Storage/object-version/serving trace

Capture:

- promoted artifact identity/generation;
- permanent storage namespace;
- object key;
- object version/generation;
- metadata-to-bytes binding;
- authorization/tenant binding;
- serving policy generation;
- serving origin;
- response content type;
- content disposition;
- cache policy generation where relevant;
- exact object/version selected for the consumer.

## Cleanup/derivative lifecycle trace

Capture:

- source cleanup request generation;
- source delete/tombstone generation;
- derivative identities;
- older object versions;
- serving-policy revocation generation;
- cleanup completion receipt;
- final source and derivative reachability.

Distinguish cleanup requested from cleanup completed.

## Consumer/bounded-effect trace

Record:

- downstream consumer identity;
- exact source/derivative object/version;
- serving policy generation;
- tenant/authorization state;
- content type/disposition/origin;
- effective upload-pipeline capability;
- bounded result;
- receipt/result.

Prefer read-only downloads, inert previews, fake-object-store receipts, and shadow policy decisions.

## Controlled validation

Use:

- inert synthetic text/image/document fixtures;
- fake archives containing only harmless files;
- mock scanners;
- local converters;
- fake object stores;
- read-only serving/download endpoints;
- deterministic generation tags;
- bounded reversible markers.

Recommended sequence:

1. establish valid current-generation positive control;
2. establish invalid negative control;
3. alter exactly one artifact/verdict/derived/storage/serving/lifecycle variable;
4. identify the first cross-stage binding mismatch;
5. bind it to the final read-only consumer;
6. apply the minimal generation/provenance/policy fix;
7. replay the identical inert fixture;
8. capture deterministic before/after receipts.

## False-positive controls

Eliminate:

- unchanged bytes legitimately reuse a verdict;
- policy explicitly permits derivative verdict inheritance;
- declared type is intentionally authoritative;
- content disposition/origin prevents the hypothesized interpretation;
- selected object version is intentional;
- independent authorization/tenant policy explains result;
- independent canonicalization defect explains result;
- independent parser-state defect explains result;
- independent cache-key defect explains stale content/policy;
- cleanup is asynchronous and receipt is not final completion;
- fixture accidentally contains active content;
- receipt belongs to another upload generation.

## Counterfactual upload controls

Hold fixture bytes and final consumer constant while changing one variable:

- stale versus current scanner verdict;
- source versus derivative identity;
- declared versus sniffed classification selected for serving;
- stale versus current object version;
- source-only versus source-plus-derivative cleanup;
- intended versus wrong tenant/serving-policy generation.

Generic random filename or MIME changes are not sufficient causal controls.

## Alternative explanations

Before UPL4/UPL5 reject:

- explicitly valid verdict reuse;
- explicitly valid derivative inheritance;
- intentionally declared-type-based serving;
- non-active serving context;
- intended object-version selection;
- authorization or tenant policy as independent root cause;
- canonicalization as independent root cause;
- parser-state bug as independent root cause;
- cache selection as independent root cause;
- asynchronous cleanup contract;
- active fixture contamination;
- unrelated upload/object/consumer receipt.

Any unresolved material alternative caps evidence at UPL2.

## Evidence capture

Capture one tuple:

`uploader principal/tenant identity + upload request/transaction identity/generation + fixture/content hash + raw artifact identity/generation + client filename representation + declared content-type/extension metadata + normalized name/storage-key result + temporary/quarantine object identity/generation + classification/sniff identity/generation + validator/scanner identity/version + validator/scanner verdict generation + parser/delegate identity/version + transform/extraction identity/generation + derived artifact/child identity/generation + promotion decision identity/generation + permanent storage object/key/version + metadata-to-bytes binding + serving/download policy identity/generation + serving origin/content-type/disposition identity + authorization/tenant binding + cleanup/tombstone lifecycle generation + downstream consumer identity + effective upload-pipeline capability + bounded result + receipt/result`

Useful artifacts include fixture hashes, generation-tagged scanner receipts, transform parent-child maps, fake-object-store version receipts, serving-policy snapshots, and cleanup reachability records.

## Evidence promotion and ceiling

### UPL0 — Upload pipeline mapped

Request, artifact, representation, temp/quarantine, validation/scanning, parser/delegate, transform, storage, serving, and cleanup stages are known.

### UPL1 — Artifact/policy generation divergence observed

A repeatable artifact, metadata, verdict, derivative, storage-version, serving-policy, tenant, or cleanup mismatch exists without final wrong-context acceptance.

### UPL2 — Controlled upload-policy mismatch

A deterministic local fixture proves a classification, validation, quarantine, revalidation, promotion, serving, tenant, or cleanup invariant mismatch.

### UPL3 — Inert wrong-context artifact acceptance

A mock/read-only consumer receives an artifact or derivative under the wrong validation, classification, storage-version, serving-policy, tenant, or lifecycle generation.

### UPL4 — Bounded reversible upload effect

A fake-object-store write, inert preview/serve marker, read-only download result, synthetic derivative, or reversible owner-controlled transition is bound to the exact pipeline tuple.

### UPL5 — Regression-verified causal upload proof

UPL4 plus complete principal/request/artifact provenance, representation/classification trace, validation/quarantine/transform lineage, storage-version/serving-policy binding, cleanup lifecycle where relevant, meaningful counterfactuals, eliminated alternatives, receipt/result binding, and remediation replay.

Evidence ceiling rules:

- surface map only: UPL0 maximum;
- generation divergence only: UPL1 maximum;
- deterministic policy mismatch without final consumer: UPL2 maximum;
- inert wrong-context acceptance: UPL3 maximum;
- bounded causal upload effect: UPL4 maximum;
- complete causal proof plus regression: UPL5.

## Remediation checks

Replay the exact inert fixture and verify:

1. validation/scanner verdict binds to current artifact generation;
2. quarantine state cannot silently transfer to changed bytes;
3. derivatives receive required independent classification/revalidation;
4. promotion selects the intended object generation;
5. permanent storage version binds to validated bytes/metadata;
6. serving policy uses the intended current classification and object version;
7. tenant/authorization decision binds to selected object;
8. cleanup revokes required source and derivative generations;
9. positive controls still process and serve correctly;
10. deterministic receipts prove the fix.

Prefer the smallest artifact-generation, verdict, revalidation, promotion, serving, or lifecycle fix that restores the pipeline invariant.
