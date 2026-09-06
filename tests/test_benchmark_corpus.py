import json
import sys
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'scripts'
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from validate_benchmarks import CATEGORIES, validate_corpus  # noqa: E402


class BenchmarkCorpusTests(unittest.TestCase):
    def test_initial_corpus_has_exactly_six_fixtures_per_category(self):
        paths = sorted((ROOT / 'benchmarks/cases').glob('*/*.json'))
        self.assertEqual(36, len(paths))
        counts = Counter(json.loads(path.read_text(encoding='utf-8'))['category'] for path in paths)
        self.assertEqual(set(CATEGORIES), set(counts))
        self.assertEqual({category: 6 for category in CATEGORIES}, dict(counts))

    def test_core_contains_all_fixtures_and_portability_is_nonempty_subset(self):
        core = json.loads((ROOT / 'benchmarks/suites/core.json').read_text(encoding='utf-8'))
        portability = json.loads((ROOT / 'benchmarks/suites/portability.json').read_text(encoding='utf-8'))
        all_rel = {
            path.relative_to(ROOT / 'benchmarks').as_posix()
            for path in (ROOT / 'benchmarks/cases').glob('*/*.json')
        }
        self.assertEqual(all_rel, set(core['fixtures']))
        self.assertTrue(portability['fixtures'])
        self.assertTrue(set(portability['fixtures']) < set(core['fixtures']))

    def test_corpus_validator_accepts_initial_corpus(self):
        errors = [x for x in validate_corpus(ROOT) if x.level == 'error']
        self.assertEqual([], errors)

    def test_suite_thresholds_and_portability_subset_are_committed(self):
        core = json.loads((ROOT / 'benchmarks/suites/core.json').read_text(encoding='utf-8'))
        portability = json.loads((ROOT / 'benchmarks/suites/portability.json').read_text(encoding='utf-8'))
        self.assertEqual(95.0, float(core['minimum_score']))
        self.assertEqual(95.0, float(portability['minimum_score']))
        self.assertEqual(36, len(core['fixtures']))
        self.assertEqual(12, len(portability['fixtures']))



if __name__ == '__main__':
    unittest.main()
