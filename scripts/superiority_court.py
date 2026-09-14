from __future__ import annotations

"""Deterministic framework-neutral comparison court primitives."""

import copy
import hashlib
import json
from typing import Any


def _canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def build_task(fixture: dict[str, Any]) -> dict[str, Any]:
    public = {
        'schema_version': 1,
        'fixture_id': fixture['fixture_id'],
        'category': fixture['category'],
        'task': copy.deepcopy(fixture['task']),
    }
    digest = hashlib.sha256(_canonical_json(public).encode('utf-8')).hexdigest()
    public['task_digest'] = digest
    return public
