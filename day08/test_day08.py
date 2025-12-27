import unittest
import os
import sys

# Add current directory to path so we can import day08
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import day08

class TestDay08(unittest.TestCase):
    def test_example_case(self):
        example_input = [
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
        # The example says "After making the ten shortest connections... produces 40"
        result = day08.solve(example_input, max_connections=10)
        self.assertEqual(result, 40)

    def test_solve_sanity(self):
        # Reads the actual input file to ensure no runtime errors
        input_lines = day08.utils.read_input_file(day08.INPUT_FILE_PATH)
        result = day08.solve(input_lines, max_connections=1000)
        self.assertIsInstance(result, int)
        self.assertGreater(result, 0)
        print(f"\nSanity check result: {result}")

if __name__ == '__main__':
    unittest.main(verbosity=2)
