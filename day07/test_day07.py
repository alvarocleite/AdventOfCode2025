import unittest
import os
import sys

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import day07

class TestDay07(unittest.TestCase):
    def test_find_char_position(self):
        lines = ["..S..", "....."]
        self.assertEqual(day07.find_char_position(lines, 'S'), (2, 0))

    def test_simulate_beams_simple(self):
        # S
        # .
        # ^
        # . .
        lines = [
            "  S  ",
            "  .  ",
            "  ^  ",
            " . . "
        ]
        # Start (2,0).
        # Row 1: Beam at 2.
        # Row 2: Beam at 2 hits ^. Splits -> 1. New beams at 1, 3.
        # Row 3: Beams at 1, 3 pass through.
        # Total splits: 1.
        self.assertEqual(day07.simulate_beams(lines, (2, 0)), 1)

    def test_part01_execution(self):
        lines = day07.utils.read_grid_padded(day07.INPUT_FILE_PATH)
        try:
            day07.part01(lines)
        except Exception as e:
            self.fail(f"part01() raised {e} unexpectedly!")

if __name__ == "__main__":
    unittest.main(verbosity=2, buffer=True)
