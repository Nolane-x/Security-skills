---
name: smart-contract-reentrancy-state-analysis
description: "Analyze contract external calls and callbacks for state-ordering, lock scope, cross-function/cross-contract reentrancy, hook-enabled tokens, read-only callbacks, and invariant exposure. Use invariant-driven local tests rather than exploit scripts."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Smart Contract Reentrancy State Analysis

Perform any dynamic validation only in an authorized, owned lab or equivalent explicitly scoped test environment.

## When to use

Use when contracts call untrusted contracts/tokens/hooks before completing state updates, share accounting across functions, or assume callback-free transfers.

## Preconditions

1. Use a local test chain with synthetic callback contracts/tokens.
2. Identify the invariant and state transition expected around each external call.
3. Do not deploy attack contracts against live protocols.

## Workflow

1. List every external call/callback point and state that remains transiently inconsistent at that point.
2. Map which public/external functions are callable during the callback and whether locks cover the entire invariant, not only one function.
3. Consider token hooks, fallback/receive, multicall, cross-contract callbacks, view/read-only dependencies, and proxy/delegate context separately.
4. Construct benign callback test contracts that re-enter only enough to assert invariant/state behavior.
5. Test cross-function and cross-contract paths with positive/negative controls and bounded recursion.
6. Distinguish reentrancy reachability from exploitable accounting/authorization impact.

## Evidence contract

Record external call, pre-callback state, reentrant entry, invariant expected/observed, bounded synthetic sequence, and resulting accounting/authorization difference.

## Stop conditions

Stop before live-chain interaction, gas/resource griefing beyond local bounds, or moving real assets.

## Output

```text
call site:
transient state:
reentrant entries:
lock/update ordering:
synthetic callback sequence:
invariant result:
evidence status:
```
