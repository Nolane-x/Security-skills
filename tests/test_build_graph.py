import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts' / 'build_graph.py'

SKILL = '''---
name: alpha-skill
description: "Alpha graph fixture. Use when testing generation."
metadata:
  nolane-security-category: foundation
  nolane-security-version: "1"
  nolane-security-authorization: not-applicable
---
# Alpha

## When to use
Testing.
## Preconditions
Local fixture.
## Workflow
1. Test.
## Evidence contract
Deterministic.
## Stop conditions
Stop on failure.
## Output
Report.
'''

META = {
    'schema_version': 1,
    'maturity': 'stable',
    'domains': ['testing'],
    'prerequisites': [],
    'composes_with': [],
    'evidence_stage': 'observed',
}


class BuildGraphTests(unittest.TestCase):
    def test_graph_generation_is_deterministic_and_checkable(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            d = root / 'skills' / 'alpha-skill'
            d.mkdir(parents=True)
            (d / 'SKILL.md').write_text(SKILL, encoding='utf-8')
            (d / 'skill.meta.json').write_text(json.dumps(META), encoding='utf-8')

            first = subprocess.run([sys.executable, str(SCRIPT), '--root', str(root)], text=True, capture_output=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            data = json.loads((root / 'graph.json').read_text(encoding='utf-8'))
            self.assertEqual(1, data['skill_count'])
            self.assertEqual('alpha-skill', data['skills'][0]['name'])
            self.assertEqual(
                {'name', 'maturity', 'domains', 'prerequisites', 'composes_with', 'evidence_stage', 'path'},
                set(data['skills'][0]),
            )
            self.assertNotIn('description', data['skills'][0])
            self.assertLess((root / 'graph.json').stat().st_size, 2048)

            before = (root / 'GRAPH.md').read_text(encoding='utf-8')
            second = subprocess.run([sys.executable, str(SCRIPT), '--root', str(root)], text=True, capture_output=True)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertEqual(before, (root / 'GRAPH.md').read_text(encoding='utf-8'))

            check = subprocess.run([sys.executable, str(SCRIPT), '--root', str(root), '--check'], text=True, capture_output=True)
            self.assertEqual(check.returncode, 0, check.stderr)


if __name__ == '__main__':
    unittest.main()
