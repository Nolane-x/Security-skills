---
name: connector-plugin-trust-analysis
description: "Analyze AI-agent connectors/plugins/MCP-like integrations for installation provenance, permission grants, schema trust, credential delegation, content/tool confusion, callback identity, update integrity, and cross-plugin data flow. Use sandbox integrations only."
metadata:
  nolane-security-category: domain
  nolane-security-version: "1"
  nolane-security-authorization: required
---
# Connector Plugin Trust Analysis

## When to use

Use when agents extend capabilities through third-party connectors, plugins, remote tool servers, app integrations, package-installed skills, or dynamically described tools.

## Preconditions

1. Use sandbox/test integrations and synthetic credentials/data.
2. Document install source, publisher identity, update path, permission grants, tool schemas, and callback/auth mechanism.
3. Do not connect unknown plugins to real production accounts.

## Workflow

1. Map integration lifecycle: discovery/install → publisher/provenance verification → permission grant → credential/token delegation → schema/tool discovery → invocation → callback/result → update/revocation.
2. Separate trusted code/tool schema from untrusted content returned by the integration.
3. Review whether dynamic tool descriptions or remote schemas can alter authority or confirmation policy.
4. Map credential audience/scope and whether one connector can influence another connector’s actions/data.
5. Test benign sandbox tools for schema/argument substitution, callback identity confusion, stale permission, revocation, and cross-plugin content injection.
6. Review update integrity/version pinning and permission-delta visibility.

## Evidence contract

Record integration identity/version, provenance, granted scopes, tool schema, synthetic invocation/result, credential audience, and control outcome. A powerful plugin is not a vulnerability if permissions and confirmation accurately match intent.

## Stop conditions

Stop before installing untrusted code on production hosts, connecting real privileged accounts, or attempting credential extraction/cross-account actions.

## Output

```text
integration/version/publisher:
install/update provenance:
permissions/credential scope:
tool schema/authority:
synthetic invocation:
revocation/update controls:
cross-plugin flow:
evidence status:
```
