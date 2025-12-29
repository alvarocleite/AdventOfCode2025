import unittest
import sys
import os

# Add the current directory to sys.path to allow importing the day module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import day11

class TestDay11(unittest.TestCase):
    def setUp(self):
        self.example_input = [
            "aaa: you hhh",
            "you: bbb ccc",
            "bbb: ddd eee",
            "ccc: ddd eee fff",
            "ddd: ggg",
            "eee: out",
            "fff: out",
            "ggg: out",
            "hhh: ccc fff iii",
            "iii: out"
        ]

    def test_parse_input(self):
        graph = day11.parse_input(self.example_input)
        self.assertEqual(graph['you'], ['bbb', 'ccc'])
        self.assertEqual(graph['ddd'], ['ggg'])
        # 'out' is not a source key in the input, so it won't be in the keys
        self.assertNotIn('out', graph)

    def test_count_paths_example(self):
        graph = day11.parse_input(self.example_input)
        count = day11.count_paths(graph, 'you', 'out')
        self.assertEqual(count, 5)

    def test_cycle_detection(self):
        # A simple cycle: a -> b -> a
        cyclic_input = [
            "a: b",
            "b: a",
            "c: out"
        ]
        graph = day11.parse_input(cyclic_input)
        with self.assertRaises(ValueError):
            day11.count_paths(graph, 'a', 'out')

    def test_no_path(self):
        # Case where there is no path to 'out'
        no_path_input = [
            "you: a b",
            "a: c",
            "b: c",
            "c: d" # d is dead end, not 'out'
        ]
        graph = day11.parse_input(no_path_input)
        count = day11.count_paths(graph, 'you', 'out')
        self.assertEqual(count, 0)

if __name__ == "__main__":
    unittest.main()
