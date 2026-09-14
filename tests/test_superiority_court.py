import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / 'scripts' / 'superiority_court.py'


class SuperiorityCourtTests(unittest.TestCase):
    def test_court_module_exists(self):
        self.assertTrue(MODULE_PATH.is_file(), 'Wave 9 court module is not implemented yet')


if __name__ == '__main__':
    unittest.main()
