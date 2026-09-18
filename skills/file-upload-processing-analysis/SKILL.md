---
name: file-upload-processing-analysis
description: "Analyze file-upload pipelines across multipart parsing, naming/canonicalization, temporary storage, content sniffing, archive/media/document processing, object storage, serving, and cleanup. Use to map parser and trust transitions safely."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# File Upload Processing Analysis

## When to use

Use for web/API file uploads, import pipelines, media conversion, document preview, archive extraction, antivirus/content scanning, or object-storage ingestion.

## Preconditions

1. Use a local/staging authorized deployment and inert synthetic files.
2. Pin parser/converter/library versions and storage configuration.
3. Do not upload active malware, credential-bearing documents, or destructive archives.

## Workflow

1. Map request parser → filename/content metadata → temporary storage → validation/sniffing → transformation/extraction → permanent storage → serving/download → cleanup.
2. Record which representation each stage trusts: client filename, MIME, magic bytes, extension, archive path, generated key.
3. Trace path/namespace normalization and object-storage key derivation.
4. Identify parser boundaries and subprocess/delegate transitions for images, media, office/PDF/archive formats.
5. Test benign mismatches (extension vs magic, nested names, harmless malformed files, oversized metadata within safe resource caps) with positive/negative controls.
6. Check serving policy separately: content disposition/type, origin, cache, authorization, and tenant isolation.

## Evidence contract

Record fixture hash, pipeline stages, representation changes, storage location/key, parser/tool version, and benign observable policy difference. A parser crash should route to minimization rather than be labeled code execution.

## Causal upload-pipeline model

Treat every promoted upload finding as one causal tuple:

`uploader principal/tenant identity + upload request/transaction identity/generation + fixture/content hash + raw artifact identity/generation + client filename representation + declared content-type/extension metadata + normalized name/storage-key result + temporary/quarantine object identity/generation + classification/sniff identity/generation + validator/scanner identity/version + validator/scanner verdict generation + parser/delegate identity/version + transform/extraction identity/generation + derived artifact/child identity/generation + promotion decision identity/generation + permanent storage object/key/version + metadata-to-bytes binding + serving/download policy identity/generation + serving origin/content-type/disposition identity + authorization/tenant binding + cleanup/tombstone lifecycle generation + downstream consumer identity + effective upload-pipeline capability + bounded result + receipt/result`.

The proof must identify the first stage where representation, artifact generation, validation state, quarantine state, derived-artifact provenance, storage version, serving policy, authorization binding, or cleanup lifecycle is applied to the wrong upload object generation.

Preserve these distinctions explicitly:

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

All dynamic validation remains local/owned/sandboxed or explicitly authorized and uses inert synthetic files, fake archives without active content, mock scanners, local converters, fake object stores, read-only consumers, and bounded reversible markers.

## Upload transaction, principal, and artifact generations

Track independently:

- uploader principal/tenant identity;
- upload request identity/generation;
- upload transaction identity/generation;
- raw artifact identity and fixture/content hash;
- raw artifact generation;
- filename/metadata generation;
- temporary/quarantine object identity/generation;
- validation/scanning generation;
- transform/derived-artifact generation;
- permanent object/version generation;
- serving-policy generation;
- cleanup/tombstone lifecycle generation.

A stable filename, hash, or object key does not collapse distinct artifact or policy generations.

## Representation and classification binding

For every stage capture:

- client filename representation;
- declared content-type/extension metadata;
- extension;
- magic/sniffed type;
- classification/sniff identity/generation;
- normalized name/storage-key result;
- archive member/path representation where relevant;
- generated object key;
- classification decision generation;
- consumer stage that trusts each representation.

Keep normalization correctness and namespace-resolution proof with `canonicalization-and-namespace-analysis`. This profile owns whether the resulting representation/classification is bound to the correct upload generation.

## Validation, scanning, and quarantine binding

Record:

- temporary/quarantine object identity/generation;
- exact fixture/content hash validated;
- validator/scanner identity/version;
- validator/scanner verdict generation;
- validation policy/configuration generation;
- quarantine state;
- whether bytes or metadata can change after verdict;
- promotion decision identity/generation;
- final artifact generation receiving the verdict.

A verdict for generation N cannot silently authorize generation N+1.

## Parser, delegate, transformation, and derived-artifact provenance

For each parser/delegate/transform capture:

- input artifact identity/generation;
- parser/delegate identity/version;
- transform/extraction identity/generation;
- operation identity;
- derived artifact/child identity/generation;
- parent-child provenance;
- metadata transformations;
- classification/scanner inheritance policy;
- required revalidation;
- bounded local result.

Keep parser-local state-machine correctness with `parser-state-machine-analysis`. This profile owns cross-stage artifact/verdict provenance around parser and delegate boundaries.

## Storage promotion, object-version, and serving binding

For promotion and serving record:

- promoted artifact identity/generation;
- permanent storage object/key/version;
- storage namespace identity;
- metadata-to-bytes binding;
- authorization/tenant binding;
- serving/download policy identity/generation;
- serving origin/content-type/disposition identity;
- cache/CDN policy generation if relevant;
- exact object/version served to downstream consumer.

Keep cache-key semantic completeness with `cache-key-identity-analysis`. This profile binds the selected upload object/version and serving policy to the validated/promoted artifact generation.

## Cleanup, derivative, and lifecycle binding

Track:

- source cleanup request generation;
- derived preview/extracted-child identities;
- tombstone/delete generation;
- object-version visibility;
- cleanup completion receipt;
- serving-policy revocation generation;
- retained references or derivatives;
- final reachability state.

Cleanup requested != object inaccessible. Source deletion does not prove derivatives, replicas, cached variants, or older versions are no longer served.

## Consumer and bounded-effect binding

For each promoted finding record:

- downstream consumer identity;
- exact object/version or derived artifact consumed;
- serving policy generation;
- authorization/tenant binding;
- content type/disposition/origin state;
- effective upload-pipeline capability;
- bounded result;
- receipt/result.

Prefer read-only downloads, inert previews, fake object-store receipts, shadow serving-policy decisions, and reversible owner-controlled markers.

## Upload-pipeline evidence ladder

Use UPL0–UPL5 exactly:

- **UPL0 — Upload pipeline mapped.** Request, artifact, representations, temp/quarantine, validation/scanning, parser/delegate, transformation, storage, serving, and cleanup stages are identified.
- **UPL1 — Artifact/policy generation divergence observed.** A repeatable artifact, metadata, verdict, derived-object, storage-version, serving-policy, tenant, or cleanup generation mismatch exists without final wrong-context consumer acceptance.
- **UPL2 — Controlled upload-policy mismatch.** A deterministic local fixture proves a documented classification, validation, quarantine, revalidation, promotion, serving, tenant, or cleanup invariant can be violated.
- **UPL3 — Inert wrong-context artifact acceptance.** A mock/read-only consumer receives an artifact or derivative under the wrong validation, classification, storage-version, serving-policy, tenant, or lifecycle generation.
- **UPL4 — Bounded reversible upload effect.** A fake-object-store write, inert preview/serve marker, read-only download result, synthetic derivative, or reversible owner-controlled transition is causally bound to the exact upload/artifact/verdict/storage/serving tuple.
- **UPL5 — Regression-verified causal upload proof.** UPL4 plus complete principal/request/artifact provenance, representation/classification trace, validation/quarantine/transform lineage, storage-version/serving-policy binding, cleanup lifecycle where relevant, meaningful counterfactuals, eliminated alternative explanations, receipt/result binding, and remediation replay.

Filename mismatches, MIME mismatches, parser crashes, scanner labels, public URLs, storage writes, or synthetic markers cannot skip missing causal bindings.

## Counterfactual upload controls

Hold fixture content and final consumer constant while changing one pipeline variable:

- current versus stale scanner verdict generation;
- source versus derived artifact identity;
- declared versus sniffed classification used for serving;
- current versus stale permanent object version;
- source-only cleanup versus source-plus-derivative lifecycle revocation;
- intended versus wrong tenant/serving-policy generation.

Generic filename or MIME mutation is not sufficient unless it isolates the hypothesized stage binding.

## Alternative explanations

Before UPL4 or UPL5 reject:

- bytes/hash are unchanged and verdict reuse is explicitly allowed;
- derivative is specification-equivalent and policy permits verdict inheritance;
- serving policy intentionally uses declared instead of sniffed type;
- content disposition/origin makes the hypothesized active interpretation impossible;
- object-version selection is intentional;
- authorization/tenant policy independently explains the result;
- canonicalization defect is the independent root cause;
- parser-local state bug independently explains the observation;
- cache-key mismatch independently selects stale content/policy;
- cleanup is explicitly asynchronous and the observed receipt is not a completion signal;
- fixture accidentally contains active content;
- receipt belongs to another upload/object/version/consumer generation.

Any unresolved material alternative caps evidence at UPL2.

## Evidence ceiling

Apply the narrowest supported level:

- mapped upload pipeline only: UPL0 maximum;
- artifact/policy generation divergence without final consumer: UPL1 maximum;
- deterministic upload-policy mismatch without final consumer: UPL2 maximum;
- inert/read-only wrong-context artifact acceptance: UPL3 maximum;
- bounded causally bound upload effect: UPL4 maximum;
- only complete principal/artifact/verdict/derived/storage/serving/lifecycle provenance, counterfactuals, receipts, and remediation replay reaches UPL5.

Do not promote MIME/name mismatches, scanner verdicts, parser crashes, public URLs, object writes, or synthetic markers into stronger claims without the missing causal bindings.

## Stop conditions

Stop if fixtures can execute active content, exhaust shared resources, overwrite real data, or trigger external delegates outside the lab.

## Output

```text
upload endpoint:
fixture/hash:
pipeline stages:
name/content representations:
parser/delegate boundaries:
storage/serving policy:
controls:
evidence status:
```
