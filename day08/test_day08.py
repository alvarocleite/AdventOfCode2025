import unittest
import os
import sys

# Add current directory to path so we can import day08
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import day08

class TestDay08(unittest.TestCase):
    def setUp(self):
        self.example_input = [
            "162,817,812",
            "57,618,57",
            "906,360,560",
            "592,479,940",
            "352,342,300",
            "466,668,158",
            "542,29,236",
            "431,825,988",
            "739,650,466",
            "52,470,668",
            "216,146,977",
            "819,987,18",
            "117,168,530",
            "805,96,715",
            "346,949,466",
            "970,615,88",
            "941,993,340",
            "862,61,35",
            "984,92,344",
            "425,690,689"
        ]

    def test_example_case_part1(self):
        # The example says "After making the ten shortest connections... produces 40"
        result = day08.solve_part1(self.example_input, max_connections=10)
        self.assertEqual(result, 40)

    def test_example_case_part2(self):
        # From Puzzle.txt Part 2 example:
        # "The first connection which causes all of the junction boxes to form a single circuit 
        # is between the junction boxes at 216,146,977 and 117,168,530.
        # ...multiplying the X coordinates of those two junction boxes (216 and 117) produces 25272."
        result = day08.solve_part2(self.example_input)
        self.assertEqual(result, 25272)

    def test_solve_sanity(self):
        # Reads the actual input file to ensure no runtime errors
        input_lines = day08.utils.read_input_file(day08.INPUT_FILE_PATH)
        
        # Part 1 Sanity
        result1 = day08.solve_part1(input_lines, max_connections=1000)
        self.assertIsInstance(result1, int)
        self.assertGreater(result1, 0)
        
        # Part 2 Sanity
        result2 = day08.solve_part2(input_lines)
        self.assertIsInstance(result2, int)
        self.assertGreater(result2, 0)
        
        print(f"\nSanity check Part 1: {result1}")
        print(f"Sanity check Part 2: {result2}")

if __name__ == '__main__':
    unittest.main(verbosity=2)
