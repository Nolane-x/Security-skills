from __future__ import annotations

"""Deterministic framework-neutral comparison court primitives."""

import copy
import hashlib
import json
from typing import Any


def _canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def _normalized_answer(value: object) -> object:
    if isinstance(value, list):
        return sorted(value, key=lambda item: _canonical_json(item))
    return value


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


def score_run(
    fixture: dict[str, Any], task: dict[str, Any], run: dict[str, Any]
) -> dict[str, Any]:
    if task['fixture_id'] != fixture['fixture_id'] or run['fixture_id'] != fixture['fixture_id']:
        raise ValueError('fixture identity mismatch')
    expected_task = build_task(fixture)
    if task != expected_task or run['task_digest'] != task['task_digest']:
        raise ValueError('task digest mismatch')

    expected = fixture['private_expected']
    answers = run.get('answers', {})
    metrics = {}
    for field in sorted(expected):
        matched = _normalized_answer(answers.get(field)) == _normalized_answer(expected[field])
        metrics[field] = 100.0 if matched else 0.0

    score = round(sum(metrics.values()) / len(metrics), 2) if metrics else 0.0
    rule_failures = sorted(
        field
        for field in fixture.get('rules', [])
        if _normalized_answer(answers.get(field)) != _normalized_answer(expected.get(field))
    )
    minimum = float(fixture.get('minimum', 100.0))
    return {
        'schema_version': 1,
        'contestant_id': run['contestant_id'],
        'fixture_id': fixture['fixture_id'],
        'category': fixture['category'],
        'task_digest': task['task_digest'],
        'score': score,
        'metrics': metrics,
        'rule_failures': rule_failures,
        'passed': score >= minimum and not rule_failures,
    }
