import unittest
import os
import sys

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import day02

class TestDay02(unittest.TestCase):
    def test_split_by_comma(self):
        self.assertEqual(day02.split_by_comma("1-5, 8-10"), ["1-5", "8-10"])
        self.assertEqual(day02.split_by_comma("1-5"), ["1-5"])

    def test_parse_range(self):
        self.assertEqual(day02.parse_range("5-10"), (5, 10))
        self.assertEqual(day02.parse_range(" 5 - 10 "), (5, 10))
        with self.assertRaises(ValueError):
            day02.parse_range("5")

    def test_is_value_invalid_part1(self):
        # Repeated twice exactly
        self.assertTrue(day02.is_value_invalid_part1(1212))
        self.assertTrue(day02.is_value_invalid_part1(55))
        self.assertFalse(day02.is_value_invalid_part1(123))
        self.assertFalse(day02.is_value_invalid_part1(121212)) # 3 times is not exactly 2 times?
        # Let's check logic: s[:half] == s[half:]. 
        # 121212 -> half=3. 121 == 212 -> False. Correct.
        self.assertFalse(day02.is_value_invalid_part1(12345)) # Odd length

    def test_is_value_invalid_part2(self):
        # Repeated *at least* twice
        self.assertTrue(day02.is_value_invalid_part2(1212))
        self.assertTrue(day02.is_value_invalid_part2(121212)) # 12 repeated 3 times
        self.assertTrue(day02.is_value_invalid_part2(555))
        self.assertFalse(day02.is_value_invalid_part2(12345))

    def test_calculate_total_invalid(self):
        # Range 10-13: 10, 11, 12, 13
        # Part 1 invalid: 11 (1 repeated twice).
        # Sum = 11.
        ranges = [(10, 13)]
        self.assertEqual(day02.calculate_total_invalid(ranges, day02.is_value_invalid_part1), 11)

    def test_part01_execution(self):
        input_lines = day02.read_input_file(day02.INPUT_FILE_PATH)
        range_strs = day02.split_by_comma(input_lines[0])
        value_pairs = day02.parse_all_ranges(range_strs)
        try:
            day02.part01(value_pairs)
        except Exception as e:
            self.fail(f"part01() raised {e} unexpectedly!")

    def test_part02_execution(self):
        input_lines = day02.read_input_file(day02.INPUT_FILE_PATH)
        range_strs = day02.split_by_comma(input_lines[0])
        value_pairs = day02.parse_all_ranges(range_strs)
        try:
            day02.part02(value_pairs)
        except Exception as e:
            self.fail(f"part02() raised {e} unexpectedly!")

if __name__ == '__main__':
    unittest.main(verbosity=2, buffer=True)
