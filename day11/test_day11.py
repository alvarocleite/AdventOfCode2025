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
        self.example_part2 = [
            "svr: aaa bbb",
            "aaa: fft",
            "fft: ccc",
            "bbb: tty",
            "tty: ccc",
            "ccc: ddd eee",
            "ddd: hub",
            "hub: fff",
            "eee: dac",
            "dac: fff",
            "fff: ggg hhh",
            "ggg: out",
            "hhh: out"
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

    def test_part2_example(self):
        # Implement the logic for Part 2 directly in test to verify
        graph = day11.parse_input(self.example_part2)
        
        # Sequence 1: svr -> ... -> dac -> ... -> fft -> ... -> out
        paths_1 = (day11.count_paths(graph, 'svr', 'dac') *
                   day11.count_paths(graph, 'dac', 'fft') *
                   day11.count_paths(graph, 'fft', 'out'))
                   
        # Sequence 2: svr -> ... -> fft -> ... -> dac -> ... -> out
        paths_2 = (day11.count_paths(graph, 'svr', 'fft') *
                   day11.count_paths(graph, 'fft', 'dac') *
                   day11.count_paths(graph, 'dac', 'out'))
                   
        total = paths_1 + paths_2
        self.assertEqual(total, 2)

if __name__ == "__main__":
    unittest.main()