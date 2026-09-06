from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

from agent_task import stable_json_text


SAFE_ENV_KEYS = {
    'PATH', 'LANG', 'LC_ALL', 'PYTHONIOENCODING', 'SYSTEMROOT', 'WINDIR', 'COMSPEC', 'PATHEXT',
    'TEMP', 'TMP', 'TMPDIR', 'HOME',
}


class AdapterError(RuntimeError):
    pass


def _sanitized_env(allow_env: list[str] | None = None) -> dict[str, str]:
    env = {key: value for key, value in os.environ.items() if key.upper() in SAFE_ENV_KEYS}
    env.setdefault('PYTHONIOENCODING', 'utf-8')
    for name in allow_env or []:
        if name in os.environ:
            env[name] = os.environ[name]
    return env


def run_adapter(task: dict[str, Any], argv: list[str], *, timeout: float = 60.0,
                max_output_bytes: int = 1024 * 1024, allow_env: list[str] | None = None) -> dict[str, Any]:
    if not argv or any(not isinstance(part, str) or not part for part in argv):
        raise AdapterError('adapter argv must contain non-empty strings')
    if timeout <= 0:
        raise AdapterError('timeout must be positive')
    if max_output_bytes <= 0:
        raise AdapterError('max_output_bytes must be positive')
    try:
        completed = subprocess.run(
            argv,
            input=json.dumps(task, ensure_ascii=False, sort_keys=True),
            text=True,
            capture_output=True,
            timeout=timeout,
            shell=False,
            env=_sanitized_env(allow_env),
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise AdapterError(f'adapter timed out after {timeout} seconds') from exc
    except OSError as exc:
        raise AdapterError(f'cannot execute adapter: {exc}') from exc

    stdout = completed.stdout or ''
    stderr = completed.stderr or ''
    if len(stdout.encode('utf-8', errors='replace')) > max_output_bytes:
        raise AdapterError('adapter stdout exceeded configured size cap')
    if len(stderr.encode('utf-8', errors='replace')) > max_output_bytes:
        raise AdapterError('adapter stderr exceeded configured size cap')
    if completed.returncode != 0:
        diagnostic = stderr.strip().replace('\n', ' ')[:500]
        raise AdapterError(f'adapter exited with status {completed.returncode}: {diagnostic}')
    try:
        data = json.loads(stdout)
    except json.JSONDecodeError as exc:
        raise AdapterError(f'adapter stdout is not valid JSON: {exc}') from exc
    if not isinstance(data, dict):
        raise AdapterError('adapter stdout must contain exactly one JSON object')
    return data


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description='Run one external agent adapter using the JSON stdin/stdout protocol.')
    parser.add_argument('task')
    parser.add_argument('--out', required=True)
    parser.add_argument('--timeout', type=float, default=60.0)
    parser.add_argument('--max-output-bytes', type=int, default=1024 * 1024)
    parser.add_argument('--allow-env', action='append', default=[])
    parser.add_argument('--adapter', nargs=argparse.REMAINDER, required=True)
    args = parser.parse_args(argv)
    try:
        task = json.loads(Path(args.task).read_text(encoding='utf-8'))
        if not isinstance(task, dict):
            raise AdapterError('task must be a JSON object')
        result = run_adapter(
            task, args.adapter, timeout=args.timeout, max_output_bytes=args.max_output_bytes, allow_env=args.allow_env,
        )
        Path(args.out).write_text(stable_json_text(result), encoding='utf-8')
    except (OSError, json.JSONDecodeError, AdapterError, ValueError, TypeError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
