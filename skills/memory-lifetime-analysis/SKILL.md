---
name: memory-lifetime-analysis
description: "Analyze ownership, aliasing, allocation, destruction, reuse, callbacks, and asynchronous lifetime boundaries in authorized code or crash evidence. Use for suspected use-after-free, double free, stale handles, iterator invalidation, refcount mistakes, or teardown races."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Memory Lifetime Analysis

Model object lifetime as a timeline of authority over one logical resource. The important question is not merely “where was it freed?” but which alias remained trusted after the lifetime invariant ended.

## When to use

Use when a pointer, handle, reference, callback context, iterator, future/promise state, or refcounted object may outlive its owner or be released more than once.

## Preconditions

All dynamic testing must stay on local/owned/sandboxed or explicitly authorized targets. Pin the build, allocator/runtime configuration, and identify the logical object/resource whose lifetime is in question.

## Causal memory-lifetime model

Treat lifetime evidence as a causal chain, not as a crash label:

`logical object/resource identity -> allocation/acquisition generation -> owner and alias set -> retain/borrow/refcount state -> invalidation/retirement event -> destruction/release generation -> address/handle reuse generation -> asynchronous callback/work-item identity -> final consumer identity -> effective stale/double-use capability -> bounded result/receipt -> lifecycle generation`

Every promotion must preserve the exact logical object identity and the material generations relevant to the hypothesis. A sanitizer report, stale-looking pointer, reused address, duplicated release, queued callback, or crash is not a complete causal lifetime proof by itself.

## Object identity, owner, and alias generations

Record one stable logical object identity separately from its numeric address, descriptor, slot, handle, index, or container position.

For each object generation, capture:

- allocation generation and acquisition generation;
- allocator/pool/handle-table or resource namespace identity;
- primary owner and ownership-transfer state;
- borrowed reference set;
- retained ownership set;
- weak/global/cache/index/callback aliases;
- refcount state and the provenance of every retain/release responsibility;
- the generation at which each alias became valid.

The following distinctions are mandatory:

- address/handle equality != logical object identity;
- allocation success != ownership authority;
- borrowed reference != retained ownership;
- alias reachability != lifetime validity;
- refcount nonzero != correct ownership provenance.

## Invalidation, destruction, and reuse binding

Name the event that ends or changes lifetime authority: close, free, unmap, container removal, cancellation, shutdown, ownership transfer, epoch advance, cache eviction, or explicit retirement.

Bind that event to:

- invalidation/retirement generation;
- destruction generation and release generation;
- aliases that must be cleared, fenced, downgraded, or revalidated;
- queued work that must be revoked or generation-checked;
- any address reuse or handle reuse generation.

Do not collapse invalidation into deallocation. The distinctions are:

- object invalidated != memory necessarily freed;
- memory freed != stale alias necessarily consumed;
- memory reused != proof the stale reference reached the new object;
- destructor executed != every alias cleared.

When a numeric address/handle is reused, the later object is a different logical object identity unless the contract explicitly proves otherwise.

## Callback, asynchronous work, and refcount lifecycle

Queued work carries lifetime authority only for the object generation in which that authority was established.

Record:

- callback/work-item identity and enqueue generation;
- captured alias and whether it is borrowed or retained;
- task/future/iterator/completion identity;
- cancellation generation;
- teardown/shutdown generation;
- retry/error-cleanup identity;
- current refcount and the provenance of each retain/release transition.

Required distinctions include:

- callback queued != callback authorized after retirement;
- cancellation requested != queued work revoked;
- retry scheduled != duplicated release authority;
- refcount underflow/overflow signal != complete causal proof;
- nonzero refcount != proof a specific alias is valid;
- completion after cancellation != vulnerability unless the final consumer violates the documented lifecycle contract.

## Final consumer and bounded effect binding

Identify the final consumer that actually dereferences, releases, closes, invokes, or otherwise consumes the reference.

Record:

- final consumer identity and execution context;
- current logical object generation expected by that consumer;
- effective stale/double-use capability actually exercised;
- whether the operation is inert, read-only, or a bounded reversible synthetic transition;
- bounded result and receipt/result binding back to the initiating object/alias/generation tuple.

A stale-read marker or synthetic counter proves only that bounded consumer behavior. It does not prove arbitrary code execution, privilege escalation, or exploitability.

## Workflow

1. **Name the logical object identity.** Separate it from address, handle, slot, index, or allocator location.
2. **List acquisition paths.** Allocation, open, map, retain, borrow, cache lookup, registration, callback capture, subscription, or container insertion.
3. **List owners and aliases.** Primary owners, borrowed references, retained ownership, weak aliases, caches, indexes, callbacks, workers, queued tasks, futures, and iterators.
4. **Write the lifetime invariant.** State which event invalidates which aliases and which generation change makes old authority stale.
5. **List release/destruction paths.** Free, close, unmap, decrement, cancellation, error cleanup, shutdown, eviction, container removal, and retry cleanup.
6. **Trace exceptional paths.** Partial construction, retry, timeout, cancellation, double error handling, rollback, teardown, and shutdown ordering.
7. **Model reuse.** Track address reuse and handle reuse separately from logical identity.
8. **Model retain/borrow/refcount semantics.** Verify the provenance of each transition rather than trusting the numeric count alone.
9. **Model asynchronous work.** Bind callbacks, completions, queued work, and worker handoff to object/lifecycle generation.
10. **Use deterministic controls.** Prefer synthetic pools, stable fake handles, inert consumers, barriers, read-only markers, and generation tags.
11. **Test counterfactuals.** Change one authoritative lifetime variable while holding the remaining tuple stable.
12. **Validate the final consumer.** Show the exact wrong-lifetime reference accepted or released and the bounded consequence.
13. **Verify remediation.** Repeat the same tuple after the causal fix and confirm intended neighboring behavior still succeeds.

## Memory-lifetime evidence ladder

### ML0 — Surface mapped

Constructors/acquisition, owners, aliases, retain/borrow rules, release paths, callbacks, consumers, and lifecycle transitions are enumerated. No lifetime violation is claimed.

### ML1 — Divergence observed

A reproducible alias, ownership, refcount, invalidation, reuse, or generation divergence is observed, but final wrong-lifetime acceptance is not established.

### ML2 — Lifetime-policy mismatch

A controlled experiment demonstrates that a stale, duplicate, retired, or wrong-generation reference survives a lifetime policy boundary. This is not yet proof that the final consumer acted on it.

### ML3 — Inert wrong-lifetime acceptance

The final synthetic consumer accepts the wrong-lifetime reference and exposes only an inert or read-only oracle bound to the exact object/alias/generation tuple.

### ML4 — Bounded reversible lifetime effect

A bounded reversible owner-controlled marker, synthetic object transition, or read-only result is causally bound to the exact object/alias/release/reuse/consumer generation tuple.

### ML5 — Regression-verified causal lifetime proof

ML4 plus complete logical object identity, allocation/acquisition generation, ownership/alias provenance, retain/borrow/refcount state, invalidation/destruction trace, reuse generation when relevant, callback/work-item identity, cancellation/teardown state, final consumer identity, effective capability, lifecycle evidence, meaningful counterfactuals, eliminated alternative explanations, receipt/result binding, and remediation regression.

Sanitizer output, free/access stacks, a crash, address reuse, handle reuse, refcount anomalies, queued callbacks, or stale-looking pointers cannot skip missing causal bindings.

## Counterfactual proof

Change one material lifetime variable while holding the remaining tuple stable.

Useful controls include:

- same callback/work item, current versus retired object generation;
- same numeric address/handle, original versus deliberately reused logical object generation;
- same release path, one versus duplicated ownership responsibility;
- same completion, before versus after cancellation/teardown generation;
- same alias, retained versus borrowed contract;
- same stale reference, generation-checked inert consumer versus deliberately unfenced inert consumer.

If multiple authoritative variables change at once, split the experiment before promoting evidence.

## Alternative explanations

Explicitly eliminate alternatives before ML4/ML5:

- stale logs or receipts from another run;
- allocator quarantine/poisoning artifacts;
- harness-owned aliases absent from the target;
- sanitizer instrumentation that changes timing or retention;
- intended resurrection or documented retained ownership;
- address reuse without stale-reference consumption;
- idempotent duplicate cleanup;
- cancellation semantics that intentionally permit completion;
- another live object using the same numeric handle;
- debug-only delayed destruction;
- crash before the targeted final consumer;
- an independent concurrency race whose lifetime consequence has not been bound.

If a material alternative remains plausible, keep evidence at or below ML2.

## Evidence ceiling

Do not promote beyond the strongest directly demonstrated stage:

- ML0 for mapping only;
- ML1 for reproducible divergence;
- ML2 for controlled policy mismatch;
- ML3 for inert final-consumer acceptance;
- ML4 for bounded reversible effect/result;
- ML5 only with complete causal provenance, controls, receipt/result binding, and remediation regression.

Sanitizer report != complete causal lifetime proof. Crash != exploitability. Memory corruption symptoms do not authorize expanding impact.

## Evidence contract

Preserve an object-lifetime timeline containing the logical object identity, allocation/acquisition generation, owner/alias set, retain/borrow/refcount transitions, invalidation event, destruction/release generation, reuse generation where relevant, async work identity, final consumer, bounded result, counterfactual controls, alternative explanations, and remediation result.

Address reuse alone is not proof; demonstrate that a logically dead or duplicate reference is consumed or released incorrectly by the intended final consumer.

## Stop conditions

Stop when:

- the suspected alias is actually retained by contract;
- the object was not invalidated for the tested consumer;
- the observed address/handle reuse is not causally connected to the stale reference;
- sanitizer instrumentation materially changes the lifetime semantics under test;
- the reproducer depends on harness-only ownership mistakes;
- validation would require weaponized heap shaping, arbitrary code execution, privilege escalation, persistence, destructive corruption, malware, evasion, real credentials, or unauthorized targets.

## Output

```text
logical object/resource:
allocation/acquisition generation:
owner and alias set:
retain/borrow/refcount state:
invalidation/retirement event:
destruction/release generation:
address/handle reuse generation:
callback/work-item identity:
cancellation/teardown state:
final consumer:
effective stale/double-use capability:
bounded result:
receipt/result binding:
counterfactual controls:
alternative explanations:
evidence level (ML0-ML5):
remediation regression:
```
