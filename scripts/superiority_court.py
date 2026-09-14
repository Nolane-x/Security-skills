from __future__ import annotations

"""Deterministic framework-neutral comparison court primitives."""

import copy
import hashlib
import json
from collections import defaultdict
from itertools import combinations
from typing import Any


def _canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def _normalized_answer(value: object) -> object:
    if isinstance(value, list):
        return sorted(value, key=lambda item: _canonical_json(item))
    return value


def _mean(values: list[float]) -> float:
    return round(sum(values) / len(values), 2) if values else 0.0


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

    score = _mean(list(metrics.values()))
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


def build_court(
    suite_id: str, fixture_ids: list[str], results: list[dict[str, Any]]
) -> dict[str, Any]:
    expected = sorted(set(fixture_ids))
    if len(expected) != len(fixture_ids):
        raise ValueError('duplicate fixture id in suite')

    seen_pairs: set[tuple[str, str]] = set()
    digests: dict[str, set[str]] = defaultdict(set)
    categories: dict[str, set[str]] = defaultdict(set)
    by_contestant: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)

    for result in results:
        fixture_id = result['fixture_id']
        contestant_id = result['contestant_id']
        if fixture_id not in expected:
            raise ValueError(f'unknown fixture id: {fixture_id}')
        pair = (contestant_id, fixture_id)
        if pair in seen_pairs:
            raise ValueError('duplicate contestant fixture result')
        seen_pairs.add(pair)
        digests[fixture_id].add(result['task_digest'])
        categories[fixture_id].add(result['category'])
        by_contestant[contestant_id][fixture_id] = result

    for fixture_id in expected:
        if len(digests[fixture_id]) > 1:
            raise ValueError(f'task digest mismatch for fixture: {fixture_id}')
        if len(categories[fixture_id]) > 1:
            raise ValueError(f'category mismatch for fixture: {fixture_id}')

    contestant_ids = sorted(by_contestant)
    summaries: list[dict[str, Any]] = []
    summary_by_id: dict[str, dict[str, Any]] = {}
    for contestant_id in contestant_ids:
        contestant_results = by_contestant[contestant_id]
        missing = [fixture_id for fixture_id in expected if fixture_id not in contestant_results]
        if missing:
            raise ValueError(
                f"contestant {contestant_id} missing fixture(s): {', '.join(missing)}"
            )

        category_scores_raw: dict[str, list[float]] = defaultdict(list)
        rule_failure_count = 0
        all_passed = True
        scores: list[float] = []
        for fixture_id in expected:
            result = contestant_results[fixture_id]
            score = float(result['score'])
            scores.append(score)
            category_scores_raw[result['category']].append(score)
            rule_failure_count += len(result.get('rule_failures', []))
            all_passed = all_passed and bool(result.get('passed', False))

        category_scores = {
            category: _mean(category_scores_raw[category])
            for category in sorted(category_scores_raw)
        }
        summary = {
            'contestant_id': contestant_id,
            'overall_score': _mean(scores),
            'category_scores': category_scores,
            'rule_failure_count': rule_failure_count,
            'eligible_for_absolute': all_passed and rule_failure_count == 0,
        }
        summaries.append(summary)
        summary_by_id[contestant_id] = summary

    pairwise: list[dict[str, Any]] = []
    absolute_against: dict[str, set[str]] = defaultdict(set)
    for left_id, right_id in combinations(contestant_ids, 2):
        left_summary = summary_by_id[left_id]
        right_summary = summary_by_id[right_id]

        fixture_wins = {'left': 0, 'right': 0, 'ties': 0}
        for fixture_id in expected:
            left_score = float(by_contestant[left_id][fixture_id]['score'])
            right_score = float(by_contestant[right_id][fixture_id]['score'])
            if left_score > right_score:
                fixture_wins['left'] += 1
            elif right_score > left_score:
                fixture_wins['right'] += 1
            else:
                fixture_wins['ties'] += 1

        all_categories = sorted(
            set(left_summary['category_scores']) | set(right_summary['category_scores'])
        )
        left_no_category_regression = all(
            left_summary['category_scores'].get(category, 0.0)
            >= right_summary['category_scores'].get(category, 0.0)
            for category in all_categories
        )
        right_no_category_regression = all(
            right_summary['category_scores'].get(category, 0.0)
            >= left_summary['category_scores'].get(category, 0.0)
            for category in all_categories
        )
        left_category_improvements = sum(
            left_summary['category_scores'].get(category, 0.0)
            > right_summary['category_scores'].get(category, 0.0)
            for category in all_categories
        )
        right_category_improvements = sum(
            right_summary['category_scores'].get(category, 0.0)
            > left_summary['category_scores'].get(category, 0.0)
            for category in all_categories
        )

        left_absolute = (
            left_summary['eligible_for_absolute']
            and right_summary['eligible_for_absolute']
            and left_summary['overall_score'] > right_summary['overall_score']
            and fixture_wins['left'] > fixture_wins['right']
            and left_no_category_regression
            and left_category_improvements > 0
        )
        right_absolute = (
            left_summary['eligible_for_absolute']
            and right_summary['eligible_for_absolute']
            and right_summary['overall_score'] > left_summary['overall_score']
            and fixture_wins['right'] > fixture_wins['left']
            and right_no_category_regression
            and right_category_improvements > 0
        )

        if left_absolute:
            verdict = 'left-absolute-superiority'
            absolute_against[left_id].add(right_id)
        elif right_absolute:
            verdict = 'right-absolute-superiority'
            absolute_against[right_id].add(left_id)
        elif left_summary['overall_score'] > right_summary['overall_score']:
            verdict = 'left-score-lead'
        elif right_summary['overall_score'] > left_summary['overall_score']:
            verdict = 'right-score-lead'
        else:
            verdict = 'tie'

        pairwise.append(
            {
                'left': left_id,
                'right': right_id,
                'fixture_wins': fixture_wins,
                'left_category_scores': left_summary['category_scores'],
                'right_category_scores': right_summary['category_scores'],
                'left_no_category_regression': left_no_category_regression,
                'right_no_category_regression': right_no_category_regression,
                'absolute_superiority': left_absolute or right_absolute,
                'verdict': verdict,
            }
        )

    absolute_winner = None
    if len(contestant_ids) >= 2:
        required_opponents = len(contestant_ids) - 1
        winners = [
            contestant_id
            for contestant_id in contestant_ids
            if len(absolute_against[contestant_id]) == required_opponents
        ]
        if len(winners) == 1:
            absolute_winner = winners[0]

    return {
        'schema_version': 1,
        'suite_id': suite_id,
        'fixture_ids': expected,
        'result_count': len(results),
        'contestants': summaries,
        'pairwise': pairwise,
        'absolute_winner': absolute_winner,
    }
