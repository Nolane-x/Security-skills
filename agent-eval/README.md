# Cross-Agent Security Evaluation

Wave 6 evaluates normalized outputs from different AI agent hosts against the same deterministic Security-skills benchmark authority.

The repository does not call hosted model APIs or ship proprietary vendor commands. `prepare_agent_tasks.py` creates oracle-free JSON tasks. An external wrapper may send a task to Codex, Claude, Gemini, Copilot, Cursor, or another agent and must return one normalized `agent-run` JSON object. `run_agent_adapter.py` provides the optional safe subprocess boundary.

CI stays fully offline. `prepare_replay_runs.py` generates deterministic `reference`, `cautious`, and `faulty` replay profiles from committed synthetic fixtures. The reference profile is a conformance oracle, not a claim about any real model.

Typical offline flow:

```text
python scripts/prepare_agent_tasks.py benchmarks/suites/portability.json --out /tmp/tasks
python scripts/prepare_replay_runs.py benchmarks/suites/portability.json --profile reference --out /tmp/reference
python scripts/validate_agent_runs.py /tmp/reference
python scripts/evaluate_agent_runs.py benchmarks/suites/portability.json /tmp/reference --json /tmp/reference.json --report /tmp/reference.md
```

Comparative matrix scores measure conformance to the selected suite. They are not a universal ranking of model intelligence, security capability, or real-world exploitability.
