# Agent Adapter Protocol

An adapter is an untrusted JSON subprocess boundary, not an evaluator.

- stdin: one prepared agent-task JSON object;
- stdout: exactly one normalized agent-run JSON object;
- stderr: bounded diagnostics only;
- exit 0: a syntactically complete JSON object was produced;
- non-zero: adapter/runtime failure.

Invoke adapters through `scripts/run_agent_adapter.py`. It uses an explicit argv vector with `shell=False`, applies a timeout and output caps, and sanitizes the child environment. Credential-like variables are not forwarded unless the caller explicitly names them with `--allow-env`.

The normalized artifact must not contain secrets, raw environment variables, browser profiles, credentials, hidden reasoning, or chain-of-thought. Free-form notes are optional and never treated as security evidence.
