import unittest
import os
import sys

# Add current directory to path so we can import day01
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import day01

class TestDay01(unittest.TestCase):
    def test_get_rot_dir_and_distance(self):
        self.assertEqual(day01.get_rot_dir_and_distance("R5"), ("R", 5))
        self.assertEqual(day01.get_rot_dir_and_distance("L10"), ("L", 10))
        with self.assertRaises(ValueError):
            day01.get_rot_dir_and_distance("")

    def test_get_position_after_move(self):
        # DIAL_SIZE is 100
        # Start 50, R5 -> 55
        self.assertEqual(day01.get_position_after_move(50, "R5"), (55, 0))
        # Start 50, R50 -> 100 -> 0 (1 crossing)
        self.assertEqual(day01.get_position_after_move(50, "R50"), (0, 1))
        # Start 50, L5 -> 45
        self.assertEqual(day01.get_position_after_move(50, "L5"), (45, 0))
        
    def test_count_times_dial_at_zero(self):
        # Start 0. R100 -> 0.
        self.assertEqual(day01.count_times_dial_at_zero(0, ["R100"]), 1)
        # Start 50. R50 -> 0. R100 -> 0.
        self.assertEqual(day01.count_times_dial_at_zero(50, ["R50", "R100"]), 2)

    def test_part01_execution(self):
        # Explicitly test part01 with real input
        input_lines = day01.utils.read_input_file(day01.INPUT_FILE_PATH)
        try:
            day01.part01(input_lines)
        except Exception as e:
            self.fail(f"part01() raised {e} unexpectedly!")

    def test_part02_execution(self):
        # Explicitly test part02 with real input
        input_lines = day01.utils.read_input_file(day01.INPUT_FILE_PATH)
        try:
            day01.part02(input_lines)
        except Exception as e:
            self.fail(f"part02() raised {e} unexpectedly!")

if __name__ == '__main__':
    unittest.main(verbosity=2, buffer=True)
