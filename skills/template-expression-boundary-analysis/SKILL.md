---
name: template-expression-boundary-analysis
description: "Analyze template and expression engines for data-vs-code boundaries, context escaping, dynamic evaluation, helper/function exposure, sandbox policy, and tenant-controlled templates. Use to distinguish injection from intended templating capabilities."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Template Expression Boundary Analysis

## When to use

Use when applications render templates, expressions, rules, filters, user-customizable messages, server-side transformations, or sandboxed scripting.

## Preconditions

1. Use a local/staging authorized environment with inert expressions.
2. Pin engine/framework version, enabled extensions/helpers, sandbox mode, and template source trust level.
3. Do not use OS-command or persistence payloads; use arithmetic/string/marker expressions.

## Workflow

1. Classify which inputs are template source, expression source, plain data, variable names, filters/helpers, or context configuration.
2. Trace construction/compilation/evaluation and whether untrusted data can cross from value position into source position.
3. Map available object graph, helpers/functions, filesystem/network/process abstractions, and sandbox restrictions.
4. Use benign expressions to establish whether evaluation exists and negative controls to show intended data escaping.
5. Test sandbox policy with harmless denied capabilities or synthetic objects rather than system effects.
6. Separate “expression evaluated” from “security boundary escaped”; route only proven capability expansion to sandbox analysis.

## Evidence contract

Record engine/version, source-trust model, controlled field, evaluation context, benign expression result, denied/allowed capability controls, and affected policy boundary.

## Causal template-expression model

Treat every promoted finding as one causal tuple:

`principal/tenant identity + request/render transaction identity/generation + template ownership/trust class + template source identity/generation + data/value identity/generation + source-construction transform identity/generation + parser/compiler identity/version + compiled template/expression identity/generation + expression node/source-position identity + evaluation context identity/generation + lexical/environment scope generation + helper/function registry identity/generation + object-graph root identity/generation + sandbox/evaluation policy identity/generation + escaping/output-context identity/generation + include/import/inheritance identity/generation + compiled-cache key/entry generation + final evaluator identity + evaluation result + downstream renderer/consumer identity + effective expression-boundary capability + bounded result + receipt/result`.

The proof must identify the first point where lower-authority data becomes source, source trust is lost, a compiled artifact is reused under the wrong policy generation, nested source inherits the wrong trust, or the evaluator receives helper/object capability beyond the documented template contract.

Preserve these distinctions explicitly:

- template source control != plain data control;
- expression source control != variable-value control;
- expression evaluation != injection;
- intended user-authored templating != unauthorized source promotion;
- string interpolation != source promotion by itself;
- escaping failure != expression evaluation;
- expression syntax accepted != expression executed;
- compilation success != evaluation;
- evaluation result != boundary escape;
- helper registered != helper reachable from this context;
- helper reachable != unsafe capability;
- object graph reachable != sandbox escape;
- denied capability probe != complete confinement;
- sandbox escape primitive != arbitrary host execution;
- arithmetic/string marker evaluation != code execution;
- template error != exploitability;
- reflected expression text != evaluation;
- autoescape disabled != source-code boundary failure by itself;
- safe-string/trusted-markup marker != trusted template source by assumption;
- trusted parent template != trusted child/include by inheritance;
- include/import path != canonical resolved resource identity;
- same template name != same source generation;
- same compiled cache key != same trust/policy generation;
- cache hit != current helper/sandbox policy generation;
- helper registry mutation != current compiled template awareness by assumption;
- tenant-owned template != cross-tenant template authority;
- renderer output != downstream active interpretation by assumption;
- local benign policy mismatch != production exploitability.

All dynamic validation remains local/owned/sandboxed or explicitly authorized. Use arithmetic/string markers, synthetic objects, fake helper registries, mock include loaders, read-only render sinks, shadow policy decisions, and bounded reversible owner-controlled markers.

## Principal, transaction, source, and data generations

Track independently:

- principal/tenant identity;
- request/render transaction identity/generation;
- template ownership/trust class;
- template source identity/generation;
- expression source identity/generation;
- data/value identity/generation;
- source-construction transform identity/generation;
- compiled template/expression generation;
- evaluation context generation;
- helper/function registry generation;
- object-graph generation;
- sandbox/evaluation policy generation;
- include/import/inheritance generation;
- compiled-cache entry generation;
- renderer/consumer generation.

A stable template name, route, cache key, principal label, or tenant label does not collapse these generations.

## Data-to-source construction binding

For every candidate source promotion record:

- original data/value identity and generation;
- intended role: plain data, variable name, filter/helper argument, expression source, or template source;
- concatenation/interpolation/reparse/compile transform;
- source-construction transform identity/generation;
- resulting derived source identity;
- parser/compiler identity/version;
- compiled artifact identity/generation;
- expression node/source-position identity;
- final evaluator identity.

Plain data becomes source only when a later parser/compiler/evaluator interprets the derived representation as source. Reflection or string construction alone is not evaluation.

## Compile, cache, and source-trust binding

For each compiled artifact capture:

- source identity/generation;
- template ownership/trust class;
- parser/compiler identity/version and options;
- compiled template/expression identity/generation;
- compiled-cache key/entry generation;
- helper registry generation assumed;
- object-graph/evaluation-context generation assumed;
- sandbox/evaluation policy generation assumed;
- include/import loader generation;
- invalidation or recompile rule;
- final evaluator identity.

A cache hit != current helper/sandbox policy generation. A compiled artifact from generation N cannot silently inherit trust or policy semantics from generation N+1 unless that compatibility is explicitly defined.

## Evaluation context, helper, and object-graph binding

Record:

- evaluation context identity/generation;
- lexical/environment scope generation;
- variables and value generations;
- helper/function registry identity/generation;
- object-graph root identity/generation;
- allowed property/method policy;
- sandbox/evaluation policy identity/generation;
- denied and allowed capability classes;
- expression node/source-position identity;
- final evaluator identity;
- evaluation result.

Helper registered != helper reachable from this context. Helper reachable != unsafe capability. Object graph reachable != sandbox escape.

## Include, import, inheritance, and nested evaluation lineage

For nested source relationships capture:

- parent source identity/trust generation;
- child/include/import identity/trust generation;
- loader identity/generation;
- include/import path;
- canonical resolved resource identity;
- inheritance/macro/import mode;
- child compilation generation;
- context/helper/sandbox generations inherited or rebound;
- nested evaluator identity;
- renderer/consumer identity.

Canonicalization correctness remains with `canonicalization-and-namespace-analysis`. This profile owns whether the already-resolved nested source receives the correct template trust and evaluation policy.

## Escaping, output context, and downstream interpretation binding

Record:

- escaping/output-context identity/generation;
- output context type;
- trusted-markup/safe-string state;
- rendered evaluation result;
- downstream renderer/consumer identity;
- downstream interpretation class;
- effective expression-boundary capability;
- bounded result;
- receipt/result.

Escaping failure != expression evaluation. A rendered marker proves only the engine behavior demonstrated. Downstream active interpretation requires separate evidence and belongs to the downstream sink's security profile.

## Template-expression evidence ladder

Use TEB0–TEB5 exactly:

- **TEB0 — Boundary surface mapped.** Source/data roles, compilation, caches, evaluation contexts, helpers, object graphs, nested sources, escaping, policies, and downstream consumers are identified.
- **TEB1 — Source/trust/context divergence observed.** A repeatable source/data-role, trust, compiled-cache, helper, object-graph, include, policy, or context generation divergence exists without final unauthorized evaluation.
- **TEB2 — Controlled expression-boundary mismatch.** A deterministic local fixture proves a documented source-promotion, trust, helper exposure, cache invalidation, include lineage, or evaluation-policy invariant can be violated.
- **TEB3 — Inert unauthorized evaluation.** Arithmetic/string-marker evaluation or read-only synthetic helper/object access occurs under a source/trust/context generation that should have remained data-only or denied.
- **TEB4 — Bounded reversible expression effect.** An inert synthetic helper marker, shadow object read, fake template-state transition, or reversible owner-controlled render marker is causally bound to the exact principal/source/compile/context/policy/evaluator tuple.
- **TEB5 — Regression-verified causal template-boundary proof.** TEB4 plus complete principal/source/data/compile/context/helper/policy/cache/include provenance, the first unauthorized source promotion or capability expansion, meaningful counterfactuals, eliminated alternative explanations, receipt/result binding, and remediation replay.

Expression reflection, syntax acceptance, compilation, errors, helper listings, sandbox denials, rendered strings, or synthetic markers cannot skip missing causal bindings.

## Counterfactual template-expression controls

Hold template semantics and final consumer constant while changing one causal variable:

- data-only value versus reparsed derived source;
- current versus stale compiled-cache generation;
- child trust independently checked versus inherited from parent;
- helper registry generation N versus N+1;
- current versus stale sandbox/evaluation policy generation;
- safe-string output marker versus template source trust kept separate.

A total engine or sandbox disable is a coarse control and is insufficient for TEB5 if it does not isolate the causal source/trust/policy boundary.

## Alternative explanations

Before TEB4/TEB5 reject:

- the principal is explicitly authorized to author templates or expressions with the demonstrated capability;
- the controlled field is documented source rather than data;
- the marker is reflected but not evaluated;
- compiler/evaluator is not reached on the final trigger;
- cache entry was correctly invalidated/recompiled;
- helper/object capability is intentionally exposed by policy;
- nested child is intentionally the same trust domain;
- canonicalization alone explains nested-source selection;
- a sandbox-boundary defect independently explains a capability after correctly authorized evaluation;
- escaping/output-context logic independently explains downstream interpretation;
- receipt belongs to another render/compile/evaluation generation.

Any unresolved material alternative caps evidence at TEB2.

Keep host/system capability crossing with `sandbox-boundary-analysis`, path/name resolution with `canonicalization-and-namespace-analysis`, principal/tenant authorization semantics with their owning profiles, and downstream HTML/JS/SQL/shell interpretation with the relevant sink-specific analysis.

## Evidence ceiling

Apply the narrowest supported level:

- mapped source/evaluation surface only: TEB0 maximum;
- source/trust/context generation divergence without unauthorized evaluation: TEB1 maximum;
- deterministic boundary-policy mismatch without final evaluation: TEB2 maximum;
- inert arithmetic/string or read-only helper/object evaluation: TEB3 maximum;
- bounded causally bound expression effect: TEB4 maximum;
- only complete principal/source/compile/context/helper/policy/cache/include provenance, counterfactuals, receipts, and remediation replay reaches TEB5.

Do not promote expression text, syntax acceptance, compile success, template errors, helper listings, sandbox denials, or rendered strings into stronger claims without the missing causal bindings.

## Stop conditions

Stop before invoking process execution, reading real secrets/files, network pivoting, or testing public multi-tenant templates outside explicit scope.

## Output

```text
engine/version:
template ownership:
controlled source/data field:
evaluation context:
available helpers/capabilities:
benign controls:
boundary consequence:
evidence status:
```
