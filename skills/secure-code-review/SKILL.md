---
name: secure-code-review
description: "Review a code change or repository for concrete security regressions using trust boundaries, dataflow, authorization, memory/state invariants, dependency changes, and test evidence. Use for pull requests, diffs, pre-merge review, or defensive source audit."
metadata:
  nolane-security-category: remediation
  nolane-security-version: "1"
  nolane-security-authorization: not-applicable
---
# Secure Code Review

Review security properties changed by the code, not just a fixed checklist of bug names.

## When to use

Use for PRs, diffs, patches, new endpoints, parser changes, authentication/authorization changes, dependency updates, IPC changes, agent/tool integrations, or safety-sensitive refactors.

## Preconditions

- Read the actual changed code and relevant callers/callees.
- Understand expected behavior and tests.
- If runtime testing is proposed against external systems, route through `security-scope-and-authorization`.

## Workflow

1. Summarize the security-relevant behavior changed.
2. Identify changed trust boundaries, identities, privileges, parsers, state, and dangerous sinks.
3. Trace untrusted data and authorization decisions through changed and unchanged surrounding code.
4. Check invariants appropriate to the language/domain:
   - memory/lifetime/ranges;
   - canonicalization and identity;
   - authn/authz;
   - injection/context separation;
   - concurrency/state;
   - secret/data exposure;
   - sandbox/tool boundaries.
5. Review failure/error/cleanup paths, not only success paths.
6. Review tests: do they exercise the security boundary or only implementation details?
7. Compare new behavior with old behavior and intended contract.
8. Rank only concrete findings with code evidence; separate “needs clarification” from vulnerability claims.
9. Recommend a minimal fix and regression case for each confirmed issue.

## Evidence contract

Every finding should include:

- code location;
- attacker/untrusted influence;
- violated invariant;
- realistic preconditions;
- consequence;
- confidence and status;
- proposed regression test.

Avoid speculative “could be vulnerable” language without a path.

## Stop conditions

Stop expanding a finding when the path is infeasible, protected by a proven guard, or based on code not actually reachable in the reviewed configuration.

## Output

Produce findings ordered by severity/confidence, followed by security-positive observations, test gaps, and unresolved questions.
