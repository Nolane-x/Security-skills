# Server-Side Request Boundary Operator Runbook

Use this runbook only for local, owned, sandboxed, benchmark/CTF, or explicitly authorized systems. Dynamic checks must terminate at controlled mock services. Do not probe real internal networks, link-local metadata services, administrative endpoints, or third-party infrastructure.

The purpose is to prove how a server interprets and enforces an outbound-request policy, not to enumerate reachable production assets.

## Attack surface

Model the complete path from user influence to the final network connection.

### Entrypoints

Inventory features that can initiate server-side retrieval or callbacks:

- URL preview, image/document import, media proxy, unfurling, scraping, or conversion;
- webhooks and callback validators;
- repository/package/feed imports;
- remote template or schema loading;
- redirect-following fetchers;
- PDF/browser rendering;
- API integrations that accept user-controlled origins, hosts, endpoints, or redirect URIs;
- background workers that fetch resources later than the original request.

For every entrypoint identify which URL components are user-controlled: scheme, username/password, host, port, path, query, fragment, or an indirect identifier resolved into a URL.

### Parsing and normalization stages

Record every component that interprets the destination:

- input validator or allowlist parser;
- URL library;
- application canonicalization logic;
- proxy configuration;
- DNS resolver;
- HTTP client;
- redirect handler;
- TLS/SNI/Host-header construction;
- connection-pool key;
- downstream renderer or protocol handler.

Different parsers can disagree about host boundaries, percent/Unicode normalization, IPv4/IPv6 representation, default ports, user-info, trailing dots, or scheme semantics. The key question is whether policy validation and actual connection construction operate on the same normalized destination.

### Trust zones and attached authority

Define synthetic destination classes such as:

```text
allowed-public-mock
blocked-internal-style-mock
blocked-metadata-style-mock
same-host-different-port-mock
redirector-mock
credential-receiving-mock
```

Also inventory authority the server may attach to the request: cookies, Authorization headers, cloud/service credentials, mTLS client identity, proxy credentials, internal headers, or source-network privilege. Use only fake credentials and controlled recipients.

## Hypothesis matrix

| Hypothesis class | Boundary under test | Controlled proof |
| --- | --- | --- |
| validation/client parser mismatch | validated URL → network-client interpretation | validator records one synthetic host while mock connection reaches another controlled host |
| resolution-time policy gap | hostname policy → resolved address | controlled DNS returns an address class that should be rejected after resolution |
| redirect revalidation gap | initial approved URL → redirect target | allowed mock redirects to blocked mock and client follows without policy re-check |
| dual-stack inconsistency | IPv4/IPv6 normalization → destination policy | equivalent controlled address classes receive different policy decisions |
| port policy gap | host allowlist → host:port connection | permitted mock hostname reaches a disallowed synthetic service port |
| scheme transition | accepted scheme → downstream handler | controlled redirect/translation crosses into a scheme outside stated policy |
| proxy-route discrepancy | application destination policy → proxy routing | proxy fixture shows final controlled destination differs from policy input |
| credential/header forwarding | original origin → redirected/new origin | fake credential marker reaches a controlled recipient where forwarding should stop |
| connection-pool confusion | request identity → reused connection | two controlled origins demonstrate cross-origin reuse inconsistent with policy |
| delayed-fetch drift | request-time policy → background worker | queued synthetic URL is reinterpreted under a different resolver/proxy/policy snapshot |

Before testing, write the intended destination policy in terms of normalized scheme, resolved address class, port, redirect behavior, credential forwarding, and revalidation points. If the owner cannot define those expectations, treat discrepancies as design questions rather than confirmed vulnerabilities.

## Controlled validation

1. **Pin the environment.** Record application revision, URL/HTTP libraries, resolver configuration, proxy variables, container/network namespace, redirect settings, and worker version.
2. **Create a closed mock topology.** Use only loopback, test containers, dedicated lab subnets, or equivalent controlled fixtures. Give every service a unique response marker and request log.
3. **Baseline an allowed request.** Confirm the feature can reach `allowed-public-mock` and capture parser, resolver, proxy, and final socket evidence.
4. **Baseline a blocked class.** Submit a direct synthetic internal-style destination that policy should deny. Confirm the denial happens before connection.
5. **Test one transformation at a time.** Change only normalization, resolution, redirect, port, scheme, proxy route, or credential attachment so causality remains clear.
6. **Capture both policy and transport views.** Record the destination as seen by validation code and the final controlled endpoint that received the connection.
7. **Exercise redirect chains safely.** Use a mock redirector and verify policy is re-evaluated at every hop, including changes in host, address class, port, and scheme.
8. **Exercise controlled DNS changes.** A lab resolver may return different controlled addresses across lookups to test whether policy is bound to the address actually connected. Keep all answers inside the owned test environment.
9. **Check forwarded authority.** Use fake headers/cookies/tokens and confirm they are stripped when origin/policy requires it.
10. **Check asynchronous paths.** If a worker fetches later, verify it applies the same normalized policy rather than trusting a request-time “validated” flag.
11. **Bound the consequence.** Reaching a mock socket proves reachability only. Use a benign protected mock resource with a unique marker if policy impact requires proving access beyond connection establishment.

Never substitute a real cloud metadata endpoint for `blocked-metadata-style-mock`. A local mock can reproduce the policy class without creating unnecessary exposure.

## False-positive controls

Pair each candidate failure with controls that separate true policy gaps from harness artifacts:

- allowed mock versus blocked mock through the same code path;
- direct blocked destination versus allowed destination that redirects to the blocked mock;
- hostname form versus its controlled resolved-address form;
- IPv4 versus IPv6 controlled representations of the same policy class;
- default port versus explicit allowed port versus synthetic disallowed port;
- request with no credential marker versus request with a fake marker;
- redirect within the same allowed origin versus redirect across a synthetic trust boundary;
- resolver response held constant versus deliberately changed inside the lab;
- direct application connection versus configured test proxy path;
- synchronous fetch versus background-worker fetch of the same fixture.

Downgrade a case if the observed destination is caused by a test proxy, stale DNS cache, container host mapping, mock redirect configuration, or a documented/authorized destination exception rather than an application policy failure.

A response status difference alone is not evidence of SSRF-like boundary crossing. Preserve transport-side proof from the controlled receiver.

## Evidence capture

For each experiment record:

```text
case_id:
application_revision:
entrypoint:
controlled_input:
input_url_components:
validator_parser_output:
canonical_url:
resolver_queries_and_answers:
address_class_policy_decision:
proxy_route:
redirect_chain:
per_hop_policy_decisions:
final_socket_target:
request_host_and_sni:
forwarded_fake_headers_or_credentials:
controlled_receiver_marker:
protected_mock_outcome:
positive_control:
negative_control:
evidence_state:
```

Evidence status should advance conservatively:

- **hypothesis:** a parser/resolver/redirect mismatch appears possible;
- **observed:** the server reaches a controlled destination relevant to the hypothesis;
- **validated:** the final controlled destination violates the defined policy and a bounded mock consequence plus controls are demonstrated;
- **regression-verified:** the original fixture is blocked after remediation while intended allowed traffic still works.

Scanner labels, URL-string appearance, or a single DNS log without binding it to the tested application flow are insufficient for `validated`.

## Remediation checks

Prefer a single destination-policy component shared by validation and execution.

Verify remediation covers:

1. **Canonical parsing:** one well-defined URL parser and explicit accepted schemes.
2. **Post-resolution policy:** classify the address actually selected for connection, including IPv4 and IPv6.
3. **Redirect revalidation:** re-run destination policy after every redirect before connecting to the next hop.
4. **Port policy:** enforce allowed ports independently of host allowlists where required.
5. **Proxy semantics:** apply equivalent restrictions to proxy-routed traffic and prevent proxy configuration from silently widening reach.
6. **Credential isolation:** do not forward sensitive headers, cookies, or client credentials across origins unless explicitly required and scoped.
7. **Connection binding:** ensure pooled/reused connections cannot bypass host/origin policy assumptions.
8. **Worker parity:** background jobs must validate the final destination at execution time, not rely solely on stale request-time validation.
9. **Network defense in depth:** where practical, restrict service egress independently of application parsing policy.
10. **Observability:** retain enough normalized destination and policy-decision data to investigate future boundary failures without logging secrets.

Regression verification should replay the original failing synthetic path plus neighboring allowed and denied controls. A fix is incomplete if it blocks only one textual URL representation while an equivalent normalized/resolved path still crosses the boundary.
