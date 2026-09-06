---
name: confused-deputy-analysis
description: "Analyze privileged components that act on behalf of less-privileged callers and may authorize the wrong caller property, delegated capability, or request context. Use for helpers, brokers, services, signed host processes, plugins, IPC/RPC gateways, cloud roles, or privileged automation."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Confused Deputy Analysis

A confused deputy trusts a property that does not actually establish authority for the requested operation. Model both the caller identity and the code/data that can influence the trusted deputy.

## When to use

Use when an unprivileged actor can ask a more privileged component to perform actions and the deputy relies on generic trust, host identity, caller-controlled metadata, or insufficiently scoped delegation.

## Preconditions

Use only owned/local/sandboxed or explicitly authorized principals and benign privileged actions. Do not replace marker proofs with persistence, secret access, or destructive operations.

## Workflow

1. **Identify the deputy and privilege differential.** What can it do that the caller cannot directly do?
2. **List accepted caller identities/channels.** Process image, signer, token, session, socket peer, mTLS identity, service account, plugin host.
3. **Ask what is actually trusted.** Is the checked property sufficient to prove who controls the executing/requesting code?
4. **Map caller-controlled request fields.** Target executable, path, resource id, service name, policy operation, environment, callback.
5. **Map code-loading/delegation surfaces.** Plugins, DLL/shared library loading, scripts, extensions, callbacks, browser origins, delegated tokens.
6. **Check authority attenuation.** Does the deputy narrow requests to the caller’s rights or execute them with full deputy rights?
7. **Check per-operation authorization.** Connection acceptance alone should not authorize every privileged method.
8. **Demonstrate with a benign marker** in an owner-controlled environment and a negative control that a disallowed caller/path is rejected.
9. **Separate identity authentication from request authorization.** A strongly authenticated caller can still be unauthorized for a particular action.
10. **Propose capability-scoped or operation-scoped delegation** rather than generic trust.

## Evidence contract

Show the privilege differential, trusted caller property, why that property can be satisfied while attacker-controlled code/data drives the request, the privileged benign action performed, and negative control. A publicly writable IPC endpoint alone is not sufficient.

## Stop conditions

Stop when every requested operation is re-authorized against the caller’s effective rights, the trusted host cannot load/inherit attacker-controlled execution in the tested model, or proof would require unsafe privileged effects.

## Output

```text
deputy privilege:
caller identity/channel:
trusted property:
attacker-controlled influence:
requested privileged operation:
authority attenuation:
benign proof:
negative control:
fix direction:
```
