# Wave 10 Profile #37 — Template Expression Boundary Causal Depth Design

**Date:** 2026-09-18  
**Base authority:** `main@4121862c46b8102ba42fc2ac153682bf8c9be828`  
**Canonical skill:** `template-expression-boundary-analysis`

## Purpose

Promote `template-expression-boundary-analysis` into the thirty-seventh CI-enforced operator-depth profile without changing routing, graph, packs, benchmark authority, agent-eval authority, superiority-court authority, or workflow semantics.

The current skill already separates template source, expression source, plain data, variables, helpers, context configuration, compilation, evaluation, and sandbox policy. The missing operator contract is causal identity across source construction and evaluation generations: exactly which principal/tenant, trust level, template source generation, data generation, source-construction transform, compile artifact, expression node, evaluation context, helper registry, object graph, include/inheritance chain, cache entry, and policy generation reached the final evaluator and what bounded capability was actually demonstrated.

## Causal model

Every promoted finding must bind one reconstructable tuple:

`principal/tenant identity + request/render transaction identity/generation + template ownership/trust class + template source identity/generation + data/value identity/generation + source-construction transform identity/generation + parser/compiler identity/version + compiled template/expression identity/generation + expression node/source-position identity + evaluation context identity/generation + lexical/environment scope generation + helper/function registry identity/generation + object-graph root identity/generation + sandbox/evaluation policy identity/generation + escaping/output-context identity/generation + include/import/inheritance identity/generation + compiled-cache key/entry generation + final evaluator identity + evaluation result + downstream renderer/consumer identity + effective expression-boundary capability + bounded result + receipt/result`

The proof must identify the first stage where lower-authority data is promoted into source, a source trust generation is lost, an evaluation context/helper/object graph exceeds the documented template contract, or a compiled/cache/include artifact is reused under the wrong trust or policy generation.

## Required distinctions

Preserve explicitly:

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

All dynamic validation remains local/owned/sandboxed or explicitly authorized and uses arithmetic/string markers, synthetic objects, fake helper registries, mock include loaders, read-only render sinks, shadow policies, and bounded reversible owner-controlled markers. Do not invoke process execution, real secrets/files, network pivots, persistence, or public multi-tenant targets.

## Principal, transaction, source, and data generations

Track independently:

- principal/tenant identity;
- render/request transaction identity/generation;
- template owner and trust class;
- template source identity/generation;
- expression source identity/generation;
- data/value identity/generation;
- source-construction transform identity/generation;
- compiled artifact generation;
- evaluation context generation;
- helper registry generation;
- sandbox/evaluation policy generation;
- include/import/inheritance generation;
- compiled-cache entry generation;
- renderer/consumer generation.

A stable template name, route, cache key, or tenant label does not collapse these generations.

## Data-to-source construction binding

For every boundary crossing capture:

- original data/value identity;
- intended role: data, variable name, filter argument, helper argument, expression source, or template source;
- concatenation/interpolation/reparse/compile transform;
- transform identity/generation;
- resulting source bytes/string identity;
- parser/compiler identity/version;
- compile artifact generation;
- expression node/source position;
- evaluator that consumes the result.

Plain data becomes a security-relevant source promotion only when a later parser/compiler/evaluator interprets the derived representation as source under a stronger trust or capability context.

## Compile, cache, and source-trust binding

For each compilation record:

- template/expression source identity/generation;
- source trust class;
- compiler/parser version and options;
- compiled artifact identity/generation;
- cache key and cache namespace;
- cache entry generation;
- helper registry generation assumed;
- sandbox/evaluation policy generation assumed;
- include/import loader generation;
- invalidation/recompile rule;
- final evaluator.

A compiled artifact produced under generation N cannot silently inherit trust, helper, or sandbox semantics from generation N+1 without an explicit compatible contract.

## Evaluation context, helper, and object-graph binding

Record:

- evaluation context identity/generation;
- lexical/environment scope;
- variables and value generations;
- helper/function registry identity/generation;
- object-graph root identity/generation;
- allowed property/method policy;
- sandbox/evaluation policy;
- denied/allowed capability classes;
- evaluator identity;
- exact expression node executed;
- result type/value.

Helper availability and object reachability are properties of the current evaluation context, not of the template text alone.

## Include, import, inheritance, and nested evaluation lineage

For nested source relationships capture:

- parent/source identity and trust generation;
- child/include/import identity and trust generation;
- loader identity/generation;
- canonical resolved resource identity;
- inheritance/macro/import mode;
- whether child source is compiled independently;
- context/helper/sandbox generations inherited or re-bound;
- nested compiled artifact generation;
- final evaluator/renderer.

Canonical path resolution belongs to `canonicalization-and-namespace-analysis`; this profile owns whether the resolved nested source receives the correct template trust/evaluation policy.

## Escaping, output context, and downstream interpretation binding

Record:

- output context type;
- escaping policy identity/generation;
- trusted-markup/safe-string state;
- rendered result;
- renderer/consumer identity;
- downstream interpretation class;
- effective expression-boundary capability;
- bounded result;
- receipt/result.

Escaping failure and template-expression evaluation are separate roots. A rendered marker proves only the evaluation or output behavior actually observed; downstream active interpretation must be established separately by the owning profile.

## Template-expression evidence ladder

Use TEB0–TEB5 exactly:

- **TEB0 — Boundary surface mapped.** Source/data roles, compilation, caches, evaluation contexts, helpers, object graphs, nested sources, escaping, policies, and downstream consumers are identified.
- **TEB1 — Source/trust/context divergence observed.** A repeatable source/data-role, trust, compiled-cache, helper, object-graph, include, policy, or context generation divergence exists without final unauthorized evaluation.
- **TEB2 — Controlled expression-boundary mismatch.** A deterministic local fixture proves a documented source-promotion, trust, helper exposure, cache invalidation, include lineage, or evaluation-policy invariant can be violated.
- **TEB3 — Inert unauthorized evaluation.** Arithmetic/string-marker evaluation or a read-only synthetic helper/object access occurs under a source/trust/context generation that should have remained data-only or denied.
- **TEB4 — Bounded reversible expression effect.** An inert synthetic helper marker, shadow object read, fake template-state transition, or reversible owner-controlled render marker is causally bound to the exact principal/source/compile/context/policy/evaluator tuple.
- **TEB5 — Regression-verified causal template-boundary proof.** TEB4 plus complete principal/source/data/compile/context/helper/policy/cache/include provenance, the first unauthorized source promotion or capability expansion, meaningful counterfactuals, eliminated alternative explanations, receipt/result binding, and remediation replay.

Expression text reflection, syntax acceptance, compilation, errors, helper listings, sandbox denials, rendered strings, or synthetic markers cannot skip missing causal bindings.

## Deterministic benign review cases

Freeze at least:

1. `data-concatenation-reparsed-as-expression-source` — lower-authority variable data is concatenated into a derived expression and reparsed as source.
2. `compiled-template-cache-reused-after-policy-generation-change` — compiled artifact/cache entry from policy generation N is reused after helper/sandbox policy moves to N+1.
3. `trusted-parent-includes-lower-trust-child-as-source` — nested child/include trust is inherited from a trusted parent instead of independently bound.
4. `helper-registry-generation-exposes-new-synthetic-capability` — a template compiled/evaluated against stale helper-registry assumptions reaches a synthetic helper outside the documented template contract.

Use arithmetic/string markers, mock loaders, fake helper registries, synthetic object graphs, shadow policy decisions, and read-only render sinks.

## Counterfactual requirements

Change exactly one causal variable while holding template semantics and final consumer constant, such as:

- data-only value versus reparsed derived source;
- current versus stale compiled-cache generation;
- child trust independently checked versus inherited from parent;
- helper registry generation N versus N+1;
- current versus stale sandbox/evaluation policy generation;
- safe-string output marker versus source-trust status held separate.

A generic engine switch or total sandbox disable is not sufficient for TEB5 if it does not isolate the causal boundary.

## Alternative explanations

Before TEB4/TEB5 reject:

- user is explicitly authorized to author templates/expressions with the demonstrated capability;
- field is documented source rather than data;
- reflected marker is not evaluated;
- compiler/evaluator is not reached on the final trigger;
- cache entry was correctly invalidated/recompiled;
- helper is intentionally exposed by policy;
- object access is read-only and inside the documented contract;
- nested child is intentionally same trust domain;
- canonicalization alone explains nested-source selection;
- sandbox-boundary defect independently explains the capability after a correctly authorized template evaluation;
- escaping/output-context defect independently explains downstream interpretation;
- receipt belongs to another render/compile/evaluation generation.

Any unresolved material alternative caps evidence at TEB2.

## Ownership boundaries

- `template-expression-boundary-analysis` owns source-vs-data roles, source promotion, compile/eval generations, template trust, helper/object-graph exposure, compiled-cache trust/policy binding, nested-source trust lineage, and bounded evaluation capability.
- `sandbox-boundary-analysis` owns capability crossing beyond the expression engine's documented sandbox boundary and privileged broker/system effects.
- `canonicalization-and-namespace-analysis` owns path/name normalization and resolved nested-resource identity.
- authorization/tenant-isolation profiles own who may configure templates/helpers; this profile binds that authority to the source/evaluation generation.
- output-specific injection profiles own downstream HTML/JS/SQL/shell interpretation; this profile stops at the template/expression engine boundary unless the downstream effect is separately established.

## Expected repository scope

1. `README.md`
2. `docs/operator-depth-contract.md`
3. `docs/superpowers/plans/2026-09-18-wave10-template-expression-boundary-depth.md`
4. `docs/superpowers/specs/2026-09-18-wave10-template-expression-boundary-depth-design.md`
5. `operator-depth/profiles.json`
6. `skills/template-expression-boundary-analysis/SKILL.md`
7. `skills/template-expression-boundary-analysis/references/operator-review-cases.json`
8. `skills/template-expression-boundary-analysis/references/operator-runbook.md`
9. `tests/test_template_expression_boundary_depth.py`
10. `tests/test_file_upload_processing_depth.py` only if CI proves its exact global-count assertion is the sole extensibility defect.

Do not change `skill.meta.json`, graph edges, packs, routing domains, benchmark authority, agent-eval authority, superiority-court authority, or workflow semantics.

## Success criterion

Profile #37 is complete only when the merge tree contains exactly 37 profiles, exactly one valid `template-expression-boundary-analysis` entry, TEB0–TEB5 is published, exact-head and post-merge CI are fully GREEN, merge parents are verified, and final scope remains bounded to the intended paths.
