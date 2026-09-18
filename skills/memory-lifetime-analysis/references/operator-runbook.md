# Memory Lifetime Operator Runbook

Use this runbook only for local, owned, sandboxed, benchmark/CTF, simulated, or explicitly authorized targets. The objective is causal lifetime evidence with bounded or read-only effects, not impact escalation.

## Attack surface

Map every object/resource class whose authority can outlive its intended lifetime:

- allocation/open/map/acquire sites;
- owner-transfer sites;
- borrowed and retained aliases;
- weak/global/cache/index aliases;
- callbacks, futures, iterators, completions, queued workers, and subscriptions;
- release/free/close/unmap/decrement paths;
- cancellation, error cleanup, retry, shutdown, eviction, and container removal;
- handle/slot/address reuse;
- final consumers that dereference, close, release, invoke, or mutate through an alias.

Pin build, allocator/runtime configuration, object fixture identity, and the lifecycle generation used by the experiment.

## Hypothesis matrix

Write each hypothesis as a falsifiable lifetime statement.

Examples:

| Hypothesis | Safe proof signal | Control |
| --- | --- | --- |
| queued work survives retirement | inert synthetic callback increments the wrong-generation counter | same callback on current generation succeeds |
| reused numeric handle is treated as the old object | read-only synthetic consumer returns the later object's marker through stale alias | same handle with correct generation resolves normally |
| duplicate release responsibility exists | controlled fake refcount ledger records a second release transition | single-owner path reaches exactly one release |
| completion races with teardown | inert completion sink accepts work after deterministic cancellation barrier | generation fence prevents the same completion |

Do not state “use-after-free” merely from a crash or sanitizer label. Name the logical object, invalidation event, final consumer, and exact stale or duplicate authority.

## Object identity and allocation-generation trace

Record:

- logical object/resource fixture identity;
- allocation generation and acquisition generation;
- allocator/pool/slot/handle-table identity;
- numeric address/handle/slot/index value separately;
- constructor/acquisition call path;
- lifecycle generation at creation;
- current object generation expected by the final consumer.

Address/handle equality is not logical identity. If a slot or address is reused, create a new logical object identity in the trace.

## Ownership and alias trace

For each generation, list:

- primary owner;
- ownership-transfer events;
- borrowed aliases;
- retained aliases;
- weak references;
- callback captures;
- cache/global/index references;
- thread/task-local aliases;
- queued-work aliases.

For every alias, record why it is valid, which generation authorizes it, and what event should revoke it.

## Retain, borrow, and refcount trace

Record each retain/release transition with its caller and responsibility provenance.

Distinguish:

- borrowed reference from retained ownership;
- refcount value from proof of ownership;
- duplicate release from an idempotent close;
- resurrection allowed by contract from accidental stale reachability;
- atomic refcount updates from higher-level ownership correctness.

A nonzero count does not prove a particular alias remains valid.

## Invalidation and destruction trace

Identify the authoritative invalidation/retirement event and record:

- invalidation generation;
- destruction/free/close/unmap generation;
- which aliases become stale;
- which aliases may legally remain read-only;
- callbacks/work items that must be revoked or generation-checked;
- cleanup/retry/error paths that may duplicate release responsibility.

Do not assume invalidation and destruction happen at the same instant.

## Address and handle reuse trace

When reuse is relevant, record:

- original logical object generation;
- retirement/destruction generation;
- reused numeric address/handle/slot;
- replacement logical object identity;
- stale alias identity;
- final consumer resolution path;
- generation check or absence of one.

The controlled proof must show whether the stale alias actually reaches the later logical object, not merely that reuse occurred.

## Callback and asynchronous-work trace

For every candidate asynchronous path, record:

- callback/work-item identity;
- enqueue generation;
- captured alias and retain/borrow contract;
- scheduler/queue identity;
- completion identity;
- cancellation generation;
- object generation at enqueue and at consume;
- final consumer identity.

Use deterministic barriers or explicit test hooks rather than uncontrolled timing stress when possible.

## Cancellation, teardown, and error-path trace

Trace neighboring paths such as:

- cancellation versus normal completion;
- timeout versus late completion;
- retry versus first-attempt cleanup;
- partial construction versus destructor;
- shutdown versus queued worker;
- cache eviction versus callback completion;
- iterator invalidation versus mutation;
- double error handling.

Each path must state who owns release responsibility and when stale work loses authority.

## Final consumer and effective capability trace

Identify the final consumer and the exact operation it performs.

Record:

- final consumer identity;
- required current object generation;
- alias presented;
- validation/generation decision;
- effective stale/double-use capability;
- bounded result;
- receipt/result correlation.

Prefer inert counters, read-only synthetic objects, fake ledgers, or bounded reversible owner-controlled state. Arbitrary code execution or destructive corruption is not required.

## Controlled validation

Use bounded deterministic fixtures such as:

- synthetic object pools with explicit generation counters;
- mock handle tables that deliberately reuse numeric handles;
- inert callbacks and completion sinks;
- controlled fake refcount ledgers;
- deterministic barriers around cancellation/teardown;
- read-only synthetic object payloads;
- marker-only consumers that record which generation was consumed.

A useful validation sequence is:

1. establish the positive current-generation path;
2. establish the negative revoked-generation path;
3. introduce exactly one lifetime mismatch;
4. observe the final inert/read-only consumer;
5. repeat with a generation/ownership fence;
6. capture byte-stable or otherwise deterministic receipts where applicable.

## False-positive controls

Always eliminate:

- stale logs from another run;
- harness-created aliases not present in the target;
- allocator quarantine or poison behavior mistaken for target semantics;
- sanitizer-induced retention/timing changes;
- intended retained ownership;
- idempotent cleanup;
- documented callback completion after cancellation;
- same numeric handle belonging to a distinct live object;
- crash before the hypothesized consumer;
- a pure concurrency bug with no independently bound lifetime consequence.

## Counterfactual controls

Change one authoritative variable while holding all others stable.

Examples:

- same callback, current versus retired object generation;
- same numeric handle, original versus replacement logical object;
- same release path, one owner versus deliberately duplicated responsibility;
- same completion, before versus after teardown generation;
- same alias, borrowed versus retained contract;
- same stale alias, consumer with versus without generation fence.

If more than one material variable changes, split the experiment.

## Alternative explanations

Before ML4 or ML5, explicitly test and reject plausible alternatives:

- receipt came from the positive-control object;
- replacement object was never reached;
- stale alias was actually retained by contract;
- duplicate release was idempotent;
- cancellation semantics intentionally allow completion;
- sanitizer changed scheduling enough to create an artificial path;
- debug allocator delayed destruction;
- another thread/object generated the marker;
- the bounded marker was emitted before retirement;
- root cause is solely a race and the lifetime boundary has not been shown.

Unresolved alternatives cap evidence at ML2.

## Evidence capture

Capture enough evidence to reconstruct one causal tuple:

`object identity + allocation/acquisition generation + owner/alias state + retain/borrow/refcount state + invalidation/destruction generation + reuse generation + callback/work identity + cancellation/teardown state + final consumer + effective capability + bounded result + receipt`

Useful artifacts include:

- deterministic generation-tagged logs;
- allocator origin/free/access stacks;
- fake refcount ledgers;
- queue/callback traces;
- generation-fence decisions;
- inert result receipts;
- before/after remediation traces.

Sanitizer output is supporting evidence, not the entire finding.

## Evidence promotion and ceiling

The evidence ceiling is the strongest directly demonstrated ML stage; do not promote beyond the captured causal tuple and controls.

Use the ML ladder:

- **ML0:** surfaces and lifetime transitions mapped.
- **ML1:** identity/ownership/refcount/reuse/generation divergence observed.
- **ML2:** controlled lifetime-policy mismatch demonstrated.
- **ML3:** inert/read-only final consumer accepts wrong-lifetime state.
- **ML4:** bounded reversible effect/result is causally bound to the exact lifetime tuple.
- **ML5:** ML4 plus complete provenance, counterfactuals, eliminated alternatives, receipt/result binding, and remediation regression.

Do not promote because of a crash, sanitizer finding, reused address, stale-looking pointer, refcount anomaly, or callback reachability alone.

## Remediation checks

Verify the causal fix rather than only symptom disappearance.

Depending on root cause, remediation may involve:

- generation/epoch validation at the final consumer;
- explicit retain or ownership transfer;
- converting an unsafe retained alias to a borrow with scoped lifetime;
- callback/work cancellation plus generation fence;
- idempotent single-owner cleanup;
- clearing cache/index/global aliases at retirement;
- delayed destruction until documented consumers release ownership;
- handle-table generation tagging;
- synchronization that closes a lifetime race without broadening critical sections unnecessarily.

Repeat the exact failing synthetic tuple after the fix and require:

1. stale/wrong-generation path is rejected or safely ignored;
2. positive current-generation behavior still works;
3. neighboring cancellation/retry/error paths remain correct;
4. no new leak, double release, or stuck ownership is introduced;
5. receipt/result proves the intended remediation path.

## Stop conditions

Stop or abort if:

- testing leaves local/owned/sandboxed/explicitly authorized scope;
- proof would require weaponized heap shaping or allocator grooming;
- proof would require arbitrary code execution or privilege escalation;
- a real credential, production secret, or unrelated production object would be touched;
- destructive memory corruption, persistence, malware, evasion, or unauthorized targeting becomes necessary;
- the suspected alias is proven valid under the documented retain/ownership contract;
- instrumentation materially changes the lifetime semantics and no safe control can separate the effect.
