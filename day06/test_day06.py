import unittest
import os
import sys

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import day06

class TestDay06(unittest.TestCase):
    def test_solve_part1_block(self):
        # 10
        # 20
        # +
        block = ["10", "20", "+ "]
        self.assertEqual(day06.solve_part1_block(block), 30)
        
        # 5
        # 6
        # *
        block = [" 5", " 6", "* "]
        self.assertEqual(day06.solve_part1_block(block), 30)

    def test_solve_part2_block(self):
        # 1 2
        # 3 4
        # +
        # Cols: "13"->13, "24"->24. Sum=37.
        block = ["12", "34", "+ "]
        self.assertEqual(day06.solve_part2_block(block), 37)

    def test_extract_problem_blocks(self):
        # 1 2
        # + +
        # Separated by space
        lines = ["1 2", "+ +"]
        # Expected: block 1 ("1", "+"), block 2 ("2", "+")
        # Occupancy: T, F, T
        # Spans: (0,1), (2,3)
        # Block 1: ["1", "+"]
        # Block 2: ["2", "+"]
        
        # NOTE: logic assumes equal length lines padded.
        blocks, spans = day06.extract_problem_blocks(lines)
        self.assertEqual(len(blocks), 2)
        self.assertEqual(blocks[0], ["1", "+"])
        self.assertEqual(blocks[1], ["2", "+"])

    def test_part01_execution(self):
        lines = day06.read_input_file(day06.INPUT_FILE_PATH)
        problem_blocks, _ = day06.extract_problem_blocks(lines)
        try:
            day06.part01(problem_blocks)
        except Exception as e:
            self.fail(f"part01() raised {e} unexpectedly!")

    def test_part02_execution(self):
        lines = day06.read_input_file(day06.INPUT_FILE_PATH)
        problem_blocks, _ = day06.extract_problem_blocks(lines)
        try:
            day06.part02(problem_blocks)
        except Exception as e:
            self.fail(f"part02() raised {e} unexpectedly!")

if __name__ == "__main__":
    unittest.main(verbosity=2, buffer=True)
