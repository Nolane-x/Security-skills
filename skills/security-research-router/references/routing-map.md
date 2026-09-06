# Routing map

Use the narrowest technique that can answer the next research question.

| Question | Primary skill | Typical supporting skill |
| --- | --- | --- |
| Where can untrusted influence cross a boundary? | attack-surface-mapping | vulnerability-hypothesis-generation |
| Which concrete security property should we test? | vulnerability-hypothesis-generation | attack-surface-mapping |
| Can a structured/native input surface produce invalid state? | fuzzing-workflow | crash-triage-and-minimization |
| Does data/identity flow from source to sensitive sink? | static-dataflow-analysis | evidence-driven-vulnerability-validation |
| Is a hard-to-reach state feasible under path constraints? | symbolic-execution-workflow | evidence-driven-vulnerability-validation |
| What security surfaces exist in a binary-only artifact? | binary-reconnaissance | fuzzing-workflow or symbolic-execution-workflow |
| Is this crash one bug, reproducible, and security-relevant? | crash-triage-and-minimization | evidence-driven-vulnerability-validation |
| Is this scanner/LLM/static finding actually real? | evidence-driven-vulnerability-validation | source discovery skill that produced it |
| What invariant did a security patch repair, and are variants left? | patch-diff-variant-analysis | static-dataflow-analysis |
| How should the root cause be fixed and proven fixed? | remediation-and-regression | patch-diff-variant-analysis |
| Does this PR change a security property? | secure-code-review | static-dataflow-analysis |
| Can untrusted content steer a tool-using agent across a boundary? | ai-agent-security-assessment | evidence-driven-vulnerability-validation |

## Method-switch rule

Switch methods only when the current method produces a concrete blocker or question.

Examples:

- Fuzzing reaches a suspicious parser state but not the target branch -> symbolic execution on that bounded branch condition.
- Static analysis finds a source-to-sink path with uncertain runtime state -> targeted local reproduction.
- A patch reveals an invariant -> variant analysis across sibling call sites.
- A crash minimizes to a library cleanup path -> evidence validation with a control and exact affected build.
