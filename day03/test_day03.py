import unittest
import os
import sys

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import day03

class TestDay03(unittest.TestCase):
    def test_find_line_max_joltage(self):
        # Increasing sequence, keep last N
        self.assertEqual(day03.find_line_max_joltage("12345", 3), 345)
        # Decreasing sequence, keep first N
        self.assertEqual(day03.find_line_max_joltage("54321", 3), 543)
        # Mixed
        # "1928", keep 2. Remove 2.
        # 1. stack=[1]
        # 9. 1<9, pop 1. rem=1. stack=[9]
        # 2. 9>2. stack=[9,2]
        # 8. 2<8, pop 2. rem=0. stack=[9,8]
        # Result 98.
        self.assertEqual(day03.find_line_max_joltage("1928", 2), 98)
        
        # Less digits than needed
        self.assertEqual(day03.find_line_max_joltage("12", 3), 0)
        
    def test_solve(self):
        lines = ["12345", "54321"]
        # 345 + 543 = 888
        self.assertEqual(day03.solve(lines, 3), 888)

    def test_part01_execution(self):
        lines = day03.read_input_file(day03.INPUT_FILE_PATH)
        try:
            day03.part01(lines)
        except Exception as e:
            self.fail(f"part01() raised {e} unexpectedly!")

    def test_part02_execution(self):
        lines = day03.read_input_file(day03.INPUT_FILE_PATH)
        try:
            day03.part02(lines)
        except Exception as e:
            self.fail(f"part02() raised {e} unexpectedly!")

if __name__ == "__main__":
    unittest.main(verbosity=2, buffer=True)
