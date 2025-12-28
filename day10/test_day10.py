import unittest
import os
import sys

# Add current directory to path so we can import day10
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import day10

class TestDay10(unittest.TestCase):
    """
    Test suite for Day 10: Factory.
    Tests parsing logic and the brute-force solution algorithm.
    """
    
    def test_parse_machine(self):
        """Tests that machine descriptions are parsed into correct bitmasks and lists."""
        line = "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}"
        target_mask, buttons, joltages = day10.parse_machine(line)
        
        # [.##.] -> 0110 in binary (MSB to the right as per index)
        # index 0: . -> 0
        # index 1: # -> 1
        # index 2: # -> 1
        # index 3: . -> 0
        # Total: 0*1 + 1*2 + 1*4 + 0*8 = 6
        self.assertEqual(target_mask, 6)
        
        # (3) -> 1 << 3 = 8
        # (1,3) -> (1<<1) | (1<<3) = 2 | 8 = 10
        # (2) -> 1 << 2 = 4
        # (2,3) -> (1<<2) | (1<<3) = 4 | 8 = 12
        # (0,2) -> (1<<0) | (1<<2) = 1 | 4 = 5
        # (0,1) -> (1<<0) | (1<<1) = 1 | 2 = 3
        self.assertEqual(buttons, [8, 10, 4, 12, 5, 3])
        self.assertEqual(joltages, [3, 5, 4, 7])

    def test_find_min_presses_example_1(self):
        """Tests the first example case from the puzzle description."""
        # [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1)
        target_mask = 6
        buttons = [8, 10, 4, 12, 5, 3]
        self.assertEqual(day10.find_min_presses(target_mask, buttons), 2)

    def test_find_min_presses_example_2(self):
        """Tests the second example case from the puzzle description."""
        # [...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4)
        # [...#.] -> index 3 is ON. mask = 1 << 3 = 8
        target_mask = 8
        # (0,2,3,4) -> 1|4|8|16 = 29
        # (2,3) -> 4|8 = 12
        # (0,4) -> 1|16 = 17
        # (0,1,2) -> 1|2|4 = 7
        # (1,2,3,4) -> 2|4|8|16 = 30
        buttons = [29, 12, 17, 7, 30]
        self.assertEqual(day10.find_min_presses(target_mask, buttons), 3)

    def test_find_min_presses_example_3(self):
        """Tests the third example case from the puzzle description."""
        # [.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2)
        # [.###.#] -> indices 1,2,3,5 are ON. 2|4|8|32 = 46
        target_mask = 46
        # (0,1,2,3,4) -> 1|2|4|8|16 = 31
        # (0,3,4) -> 1|8|16 = 25
        # (0,1,2,4,5) -> 1|2|4|16|32 = 55
        # (1,2) -> 2|4 = 6
        buttons = [31, 25, 55, 6]
        self.assertEqual(day10.find_min_presses(target_mask, buttons), 2)

    def test_part01_execution(self):
        """Tests that part01 executes on the real input without raising errors."""
        input_lines = day10.utils.read_input_file(day10.INPUT_FILE_PATH)
        try:
            day10.part01(input_lines)
        except Exception as e:
            self.fail(f"part01() raised {e} unexpectedly!")

if __name__ == '__main__':
    unittest.main(verbosity=2, buffer=True)