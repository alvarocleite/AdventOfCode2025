import unittest
import os
import sys

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import day04

class TestDay04(unittest.TestCase):
    def test_get_accessible_coordinates(self):
        # 3x3 grid with center surrounded by 4 neighbors (up, down, left, right)
        # . @ .
        # @ @ @
        # . @ .
        grid = [
            ['.', '@', '.'],
            ['@', '@', '@'],
            ['.', '@', '.']
        ]
        # Center @ at (1,1) has 4 neighbors (0,1), (1,0), (1,2), (2,1).
        # Corner/Edge @ have 1 or 3 neighbors.
        # If max_neighbors is 4.
        # Center has 4 -> Not accessible (<4 is false).
        # Others have <4 -> Accessible.
        
        accessible = day04.get_accessible_coordinates(grid, '@', 4)
        self.assertNotIn((1, 1), accessible)
        self.assertIn((0, 1), accessible)
        self.assertIn((1, 0), accessible)
        self.assertIn((1, 2), accessible)
        self.assertIn((2, 1), accessible)
        
        # If max_neighbors is 5. Center (4 neighbors) < 5 -> Accessible.
        accessible_5 = day04.get_accessible_coordinates(grid, '@', 5)
        self.assertIn((1, 1), accessible_5)

    def test_part01_execution(self):
        lines = day04.read_input_file(day04.INPUT_FILE_PATH)
        try:
            day04.part01(lines)
        except Exception as e:
            self.fail(f"part01() raised {e} unexpectedly!")

    def test_part02_execution(self):
        lines = day04.read_input_file(day04.INPUT_FILE_PATH)
        try:
            day04.part02(lines)
        except Exception as e:
            self.fail(f"part02() raised {e} unexpectedly!")

if __name__ == "__main__":
    unittest.main(verbosity=2, buffer=True)
