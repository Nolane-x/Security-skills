---
name: canonicalization-and-namespace-analysis
description: "Analyze mismatches between validation names and runtime-resolved identities across paths, URLs, encodings, case rules, alternate streams, aliases, symlinks, archive members, hostnames, Unicode, and object namespaces. Use when two syntactically different names may resolve to the same resource or one name changes meaning across layers."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Canonicalization and Namespace Analysis

Security checks must authorize the same identity that the sink later resolves. Canonicalization bugs happen when validation and use operate in different namespaces or apply normalization in a different order.

## When to use

Use for path traversal defenses, archive extraction, filesystem streams, URL/host validation, case-insensitive stores, Unicode identifiers, cloud resource names, IPC object namespaces, or parser-to-OS name translation.

## Preconditions

Any dynamic checks must use owned/local/sandboxed or explicitly authorized resources. Record platform/filesystem/runtime normalization rules.

## Workflow

1. **Name every representation.** Raw input, decoded text, normalized path/URL, platform API string, filesystem/object-manager identity.
2. **List transformations in order.** Percent decode, Unicode normalize, slash conversion, case fold, dot-segment removal, device/stream suffix handling, symlink resolution.
3. **Identify authorization point and sink point.** What exact representation does each compare or resolve?
4. **Build equivalence classes.** Different strings that the sink treats as one identity; one string that different layers interpret differently.
5. **Check normalization order.** Validate-before-decode, decode-twice, extension before casefold, basename before stream/type suffix, host validation before IDNA.
6. **Check prefix/boundary semantics.** String prefix is not path containment; hostname suffix is not label containment.
7. **Check mutable namespaces.** Symlink/reparse/rename races can change identity between check and use.
8. **Use benign fixture resources** to show aliasing or boundary escape without touching sensitive locations.
9. **Add a canonical identity assertion** at the final resolution layer when possible.
10. **Search sibling validators** that feed the same sink through different transformations.

## Evidence contract

Show the raw value, validation representation, sink representation, exact transformation/equivalence causing disagreement, and benign resource identity actually reached. Merely unusual encoding is not a vulnerability if all layers reject or preserve the same authorization decision.

## Stop conditions

Stop when the sink operates on an immutable already-open handle rather than a re-resolved name, all equivalent forms are canonicalized before policy, or environment behavior cannot be reproduced safely.

## Output

```text
namespace/platform:
raw representation:
transform sequence:
policy representation:
sink representation:
equivalent/ambiguous forms:
benign resolved identity:
control:
fix boundary:
```
