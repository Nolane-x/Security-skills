import json
import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

from security_graph import validate_graph

SKILL = '''---
name: {name}
description: "Graph fixture skill. Use when testing graph validation."
metadata:
  nolane-security-category: foundation
  nolane-security-version: "1"
  nolane-security-authorization: not-applicable
---
# Fixture

## When to use
Testing.

## Preconditions
Fixture exists.

## Workflow
1. Test.

## Evidence contract
Deterministic assertion.

## Stop conditions
Stop on invalid fixture.

## Output
Report.
'''


def write_skill(root: Path, name: str, meta: dict | None = None):
    d = root / 'skills' / name
    d.mkdir(parents=True)
    (d / 'SKILL.md').write_text(SKILL.format(name=name), encoding='utf-8')
    if meta is not None:
        (d / 'skill.meta.json').write_text(json.dumps(meta), encoding='utf-8')


def meta(*, prereq=None, composes=None):
    return {
        'schema_version': 1,
        'maturity': 'stable',
        'domains': ['testing'],
        'prerequisites': prereq or [],
        'composes_with': composes or [],
        'evidence_stage': 'observed',
    }


class GraphValidationTests(unittest.TestCase):
    def test_missing_sidecar_is_error(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            write_skill(root, 'alpha-skill')
            issues = validate_graph(root)
            self.assertTrue(any('skill.meta.json' in i.message for i in issues))

    def test_unknown_prerequisite_is_error(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            write_skill(root, 'alpha-skill', meta(prereq=['missing-skill']))
            issues = validate_graph(root)
            self.assertTrue(any('unknown prerequisite' in i.message for i in issues))

    def test_prerequisite_cycle_is_error(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            write_skill(root, 'alpha-skill', meta(prereq=['beta-skill']))
            write_skill(root, 'beta-skill', meta(prereq=['alpha-skill']))
            issues = validate_graph(root)
            self.assertTrue(any('cycle' in i.message.lower() for i in issues))


    def test_pack_flow_must_reference_pack_member(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            write_skill(root, 'alpha-skill', meta())
            write_skill(root, 'beta-skill', meta())
            pack_root = root / 'packs'
            pack_root.mkdir()
            manifest = {
                'schema_version': 1,
                'name': 'bad-pack',
                'description': 'fixture',
                'entrypoint': 'alpha-skill',
                'skills': ['alpha-skill'],
                'default_flow': ['alpha-skill', 'beta-skill'],
            }
            (pack_root / 'bad-pack.json').write_text(json.dumps(manifest), encoding='utf-8')
            issues = validate_graph(root)
            self.assertTrue(any('default_flow skill is not listed' in i.message for i in issues))

    def test_valid_graph_has_no_errors(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            write_skill(root, 'alpha-skill', meta())
            write_skill(root, 'beta-skill', meta(prereq=['alpha-skill'], composes=['alpha-skill']))
            self.assertEqual([], [i for i in validate_graph(root) if i.level == 'error'])


if __name__ == '__main__':
    unittest.main()
