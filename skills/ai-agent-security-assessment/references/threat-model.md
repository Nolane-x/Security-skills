# AI agent threat model

## Principals

Model each as a distinct principal when present:

- user;
- agent/model;
- orchestrator;
- tool/MCP/plugin;
- external web/content author;
- retrieval/index owner;
- memory store;
- connected SaaS/service;
- another tenant/user;
- human approver.

## Boundaries

Check:

- untrusted content -> instructions/context;
- model output -> tool arguments;
- tool result -> model context;
- private retrieval -> user-visible output;
- one tenant -> another tenant;
- local files -> remote egress;
- memory write -> future sessions;
- plugin install/config -> new permissions;
- low-impact action -> irreversible/high-impact action.

## High-value architectural controls

Prefer:

- least-privilege tool scopes;
- deterministic authorization outside the model;
- typed/validated tool arguments;
- explicit confirmation for irreversible/high-impact actions;
- provenance labels for untrusted content;
- data minimization;
- tenant isolation;
- sandboxing;
- synthetic canary-based testing;
- audit logs that connect model decision, tool call, and result.

Prompt wording can help, but it should not be the only control for high-consequence boundaries.
