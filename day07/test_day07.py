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
        splits, _ = day07.run_simulation(lines, (2, 0))
        self.assertEqual(splits, 1)

    def test_simulate_timelines_example(self):
        # Example from Puzzle Text (simplified or full if possible, but full is large)
        # I'll use the small one I created for simple beams, but check timeline logic.
        # S (1 path)
        # . (1 path)
        # ^ (Split -> L, R. 1 path becomes 2 paths)
        # . . (L continues, R continues. Total 2 timelines)
        lines = [
            "  S  ",
            "  .  ",
            "  ^  ",
            " . . "
        ]
        _, timelines = day07.run_simulation(lines, (2, 0))
        self.assertEqual(timelines, 2)

    def test_part01_execution(self):
        lines = day07.utils.read_grid_padded(day07.INPUT_FILE_PATH)
        try:
            day07.part01(lines)
        except Exception as e:
            self.fail(f"part01() raised {e} unexpectedly!")

    def test_part02_execution(self):
        lines = day07.utils.read_grid_padded(day07.INPUT_FILE_PATH)
        try:
            day07.part02(lines)
        except Exception as e:
            self.fail(f"part02() raised {e} unexpectedly!")

if __name__ == "__main__":
    unittest.main(verbosity=2, buffer=True)
