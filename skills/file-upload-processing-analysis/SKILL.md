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
