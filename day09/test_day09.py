import unittest
import os
import sys

# Add current directory to path so we can import day09
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import day09

class TestDay09(unittest.TestCase):
    def setUp(self):
        self.example_input = [
            "7,1",
            "11,1",
            "11,7",
            "9,7",
            "9,5",
            "2,5",
            "2,3",
            "7,3"
        ]

    def test_example_case_part1(self):
        # Example from Puzzle.txt: "Ultimately, the largest rectangle you can make in this example has area 50."
        points = day09.parse_input(self.example_input)
        result = day09.calculate_max_area(points)
        self.assertEqual(result, 50)

    def test_solve_sanity(self):
        # Reads the actual input file to ensure no runtime errors
        if os.path.exists(day09.INPUT_FILE_PATH):
            input_lines = day09.utils.read_input_file(day09.INPUT_FILE_PATH)
            points = day09.parse_input(input_lines)
            result = day09.calculate_max_area(points)
            self.assertIsInstance(result, int)
            self.assertGreater(result, 0)
            print(f"\nSanity check Part 1: {result}")

if __name__ == '__main__':
    unittest.main(verbosity=2)
