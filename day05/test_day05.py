import unittest
import os
import sys

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import day05

class TestDay05(unittest.TestCase):
    def test_merge_ranges(self):
        # Overlapping
        self.assertEqual(day05.merge_ranges([(1, 5), (2, 6)]), [(1, 6)])
        # Adjacent
        self.assertEqual(day05.merge_ranges([(1, 5), (6, 10)]), [(1, 10)])
        # Disjoint
        self.assertEqual(day05.merge_ranges([(1, 5), (7, 10)]), [(1, 5), (7, 10)])
        # Contained
        self.assertEqual(day05.merge_ranges([(1, 10), (2, 5)]), [(1, 10)])
        # Unsorted input
        self.assertEqual(day05.merge_ranges([(7, 10), (1, 5)]), [(1, 5), (7, 10)])

    def test_count_fresh_ingredients(self):
        # Ranges: 1-10. IDs: 5, 15. Count = 1 (5 is in, 15 is out).
        ranges = [(1, 10)]
        ids = [5, 15]
        self.assertEqual(day05.count_fresh_ingredients(ranges, ids), 1)

    def test_part01_execution(self):
        lines = day05.utils.read_input_file(day05.INPUT_FILE_PATH)
        fresh_ranges, available_ids = day05.parse_inventory_data(lines)
        merged_ranges = day05.merge_ranges(fresh_ranges)
        try:
            day05.part01(merged_ranges, available_ids)
        except Exception as e:
            self.fail(f"part01() raised {e} unexpectedly!")

    def test_part02_execution(self):
        lines = day05.utils.read_input_file(day05.INPUT_FILE_PATH)
        fresh_ranges, _ = day05.parse_inventory_data(lines)
        merged_ranges = day05.merge_ranges(fresh_ranges)
        try:
            day05.part02(merged_ranges)
        except Exception as e:
            self.fail(f"part02() raised {e} unexpectedly!")

if __name__ == "__main__":
    unittest.main(verbosity=2, buffer=True)
