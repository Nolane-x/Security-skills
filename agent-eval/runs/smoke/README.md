# Replay smoke artifacts

Wave 6 replay runs are generated deterministically into temporary directories by `scripts/prepare_replay_runs.py`. Generated run/result files are not committed by default. The profile definitions are committed under `agent-eval/adapters/` so CI remains reproducible without network access.
