# Template Expression Boundary Operator Runbook

Use this runbook only for local, owned, sandboxed, staging, benchmark/CTF, simulated, or explicitly authorized template/expression engines. Use arithmetic/string markers, synthetic objects, fake helper registries, mock include loaders, shadow policies, read-only render sinks, and bounded reversible markers. Do not invoke process execution, read real secrets/files, pivot network access, establish persistence, or test public multi-tenant templates outside explicit scope.

## Attack surface

Map:

- principal/tenant and render transaction generations;
- template ownership/trust class;
- template source and expression source generations;
- plain data/value generations;
- source-construction transforms;
- parser/compiler identity and version;
- compiled artifact and cache entry generations;
- evaluation context and lexical/environment generations;
- helper registry and object-graph generations;
- sandbox policy generation;
- include/import/inheritance loader lineage;
- escaping/output-context state;
- final evaluator, renderer, and downstream consumer.

## Hypothesis matrix

| Hypothesis | Safe oracle | Control |
| --- | --- | --- |
| plain data is reparsed as expression source | synthetic arithmetic/string marker appears only after explicit reparse | same value remains literal data when reparse is removed |
| compiled cache survives policy change | shadow policy receipt shows old compiled artifact under new policy generation | cache invalidation/recompile binds current policy |
| trusted parent grants child source trust | mock include loader shows lower-trust child evaluated under parent trust | child trust checked independently before compile |
| helper registry generation expands capability | fake helper marker becomes reachable under stale context assumptions | current helper policy denies or explicitly allows it |

## Principal/source/data-generation trace

Record:

- principal/tenant identity;
- request/render transaction generation;
- template ownership/trust class;
- template source generation;
- expression source generation;
- data generation;
- source-construction generation;
- compiled artifact generation;
- evaluation-context generation;
- helper-registry generation;
- sandbox-policy generation;
- nested-source generation;
- cache-entry generation;
- renderer/consumer generation.

Do not equate a stable template name, route, tenant label, or cache key with stable source or policy generations.

## Data-to-source construction trace

Capture:

- original data/value identity and generation;
- intended role: data, variable, helper argument, expression source, or template source;
- concatenation/interpolation/reparse/compile step;
- source promotion transform identity/generation;
- resulting source string/bytes identity;
- parser/compiler identity/version;
- compiled artifact;
- expression node/source position;
- evaluator consuming the derived source.

Reflection and string construction alone are not evaluation.

## Compile/cache/source-trust trace

Capture:

- template source identity/generation;
- trust class;
- parser/compiler version/options;
- compiled artifact identity/generation;
- cache key and cache entry generation;
- helper registry generation assumed;
- evaluation-context/object-graph generation assumed;
- sandbox policy generation assumed;
- include loader generation;
- invalidation/recompile rule;
- final evaluator.

A cache entry from trust or policy generation N must not silently authorize generation N+1 unless compatibility is explicitly defined.

## Evaluation-context/helper/object-graph trace

Record:

- evaluation context identity/generation;
- lexical/environment scope generation;
- variables/value generations;
- helper registry identity/generation;
- object graph root identity/generation;
- allowed property/method policy;
- sandbox policy identity/generation;
- exact expression node;
- evaluator identity;
- allowed/denied capability classes;
- evaluation result.

Helper registry presence does not prove current-context reachability, and helper reachability does not prove a sandbox escape.

## Include/import/inheritance trace

Capture:

- parent source/trust generation;
- child/include/import source/trust generation;
- loader identity/generation;
- requested include/import path;
- canonical resolved resource identity;
- inheritance/macro/import mode;
- child compiled artifact generation;
- inherited or rebound helper/context/policy generations;
- nested evaluator and renderer.

Use mock loaders and synthetic local resources only. Canonical path mechanics belong to the canonicalization profile; this trace binds the resolved child to the right template trust.

## Escaping/output-context/downstream trace

Record:

- escaping policy identity/generation;
- output context;
- safe-string/trusted-markup state;
- rendered result;
- downstream renderer/consumer identity;
- downstream interpretation class;
- effective expression-boundary capability;
- bounded result;
- receipt/result.

Escaping failure and expression evaluation are separate causes. A rendered marker does not establish browser/script/SQL/shell execution.

## Controlled validation

Use:

- arithmetic and string expressions;
- inert synthetic template markers;
- fake helper functions that return fixed strings;
- synthetic object graphs with read-only fields;
- mock include/import loaders;
- shadow sandbox/evaluation policies;
- deterministic cache generations;
- read-only render sinks;
- bounded reversible owner-controlled markers.

Recommended sequence:

1. establish a data-only negative control;
2. establish an explicitly authorized template-source positive control;
3. change exactly one source/trust/cache/helper/nested-source variable;
4. prove parser/compiler/evaluator reach on the intended generation;
5. locate the first unauthorized source promotion or capability expansion;
6. bind it to the final read-only renderer/consumer;
7. apply the minimal source-role/trust/cache/helper/policy fix;
8. replay the same synthetic transaction;
9. capture deterministic before/after receipts.

## False-positive controls

Eliminate:

- explicitly authorized user-authored template source;
- documented expression-source fields;
- marker reflection without evaluation;
- compiler/evaluator not reached;
- correct cache invalidation/recompile;
- helper intentionally exposed;
- object access inside documented contract;
- child/include intentionally same trust domain;
- independent canonicalization root cause;
- independent sandbox-boundary root cause;
- independent escaping/downstream interpretation root cause;
- receipt from another compile/render generation.

## Counterfactual template-expression controls

Hold template semantics and final consumer fixed while changing one variable:

- literal data versus reparsed derived source;
- current versus stale cache entry;
- independently checked child trust versus inherited parent trust;
- helper registry generation N versus N+1;
- current versus stale sandbox policy;
- safe-string output state versus source-trust state.

Generic engine changes or disabling all evaluation are coarse controls and do not establish the exact boundary.

## Alternative explanations

Before TEB4/TEB5 explicitly reject:

- principal is authorized for the demonstrated templating capability;
- field is documented source, not data;
- reflected marker is not evaluated;
- final trigger did not execute the suspected evaluator;
- compiled cache is current;
- helper/object capability is documented;
- nested source shares intended trust;
- canonicalization independently selected a different child;
- sandbox defect independently expands capability after correct evaluation;
- escaping/output context independently explains the downstream observation;
- receipt belongs to another generation.

Any unresolved material alternative caps evidence at TEB2.

## Evidence capture

Capture one tuple:

`principal/tenant identity + request/render transaction identity/generation + template ownership/trust class + template source identity/generation + data/value identity/generation + source-construction transform identity/generation + parser/compiler identity/version + compiled template/expression identity/generation + expression node/source-position identity + evaluation context identity/generation + lexical/environment scope generation + helper/function registry identity/generation + object-graph root identity/generation + sandbox/evaluation policy identity/generation + escaping/output-context identity/generation + include/import/inheritance identity/generation + compiled-cache key/entry generation + final evaluator identity + evaluation result + downstream renderer/consumer identity + effective expression-boundary capability + bounded result + receipt/result`

Useful artifacts include source/data role tables, compile receipts, cache generation records, helper registry snapshots, mock include lineage, shadow policy decisions, read-only render outputs, and remediation replay receipts.

## Evidence promotion and ceiling

### TEB0 — Boundary surface mapped

Source/data roles, compilation, caches, contexts, helpers, object graphs, nested sources, escaping, policies, and consumers are known.

### TEB1 — Source/trust/context divergence observed

A repeatable source/data-role, trust, cache, helper, object-graph, include, policy, or context generation divergence exists without final unauthorized evaluation.

### TEB2 — Controlled expression-boundary mismatch

A deterministic local fixture proves a source-promotion, trust, helper exposure, cache invalidation, include-lineage, or evaluation-policy invariant mismatch.

### TEB3 — Inert unauthorized evaluation

Arithmetic/string marker evaluation or read-only synthetic helper/object access occurs under a source/trust/context generation that should have remained data-only or denied.

### TEB4 — Bounded reversible expression effect

An inert helper marker, shadow object read, fake template-state transition, or reversible owner-controlled render marker is bound to the exact causal tuple.

### TEB5 — Regression-verified causal template-boundary proof

TEB4 plus complete principal/source/data/compile/context/helper/policy/cache/include provenance, first unauthorized source promotion or capability expansion, meaningful counterfactuals, eliminated alternatives, receipt/result binding, and remediation replay.

Evidence ceiling rules:

- mapped surface only: TEB0 maximum;
- generation divergence without evaluation: TEB1 maximum;
- deterministic boundary mismatch without final evaluator: TEB2 maximum;
- inert/read-only unauthorized evaluation: TEB3 maximum;
- bounded causal expression effect: TEB4 maximum;
- complete causal proof plus regression: TEB5.

## Remediation checks

Replay the exact synthetic transaction and verify:

1. data-only values never enter source position unless explicitly authorized;
2. compiled artifacts bind to current source trust;
3. cache entries invalidate when helper/sandbox/source trust changes;
4. nested children receive independent intended trust checks;
5. helper registry and object graph match current evaluation policy;
6. escaping/output context remains separate from source trust;
7. intended user-authored templates still work;
8. denied contexts remain data-only or capability-limited;
9. deterministic receipts prove the fix.

Prefer the smallest source-role, compile/cache invalidation, helper registry, nested-trust, or evaluation-policy fix that restores the boundary.
