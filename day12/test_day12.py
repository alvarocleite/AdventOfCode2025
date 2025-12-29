import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import day12

class TestDay12(unittest.TestCase):
    def setUp(self):
        self.example_input = [
            "0:",
            "###",
            "##.",
            "##.",
            "",
            "1:",
            "###",
            "##.",
            ".##",
            "",
            "2:",
            ".##",
            "###",
            "##.",
            "",
            "3:",
            "##.",
            "###",
            "##.",
            "",
            "4:",
            "###",
            "#..",
            "###",
            "",
            "5:",
            "###",
            ".#.",
            "###",
            "",
            "4x4: 0 0 0 0 2 0",
            "12x5: 1 0 1 0 2 2",
            "12x5: 1 0 1 0 3 2"
        ]

    def test_parse(self):
        shapes, tasks = day12.parse_input(self.example_input)
        self.assertEqual(len(shapes), 6)
        self.assertEqual(len(tasks), 3)
        self.assertEqual(tasks[0]['width'], 4)
        self.assertEqual(tasks[0]['height'], 4)
        self.assertEqual(tasks[0]['counts'], [0, 0, 0, 0, 2, 0])

    def test_solve_example_1(self):
        # 4x4, two of shape 4
        # Shape 4 is:
        # ###
        # #..
        # ###
        # Should fit
        shapes, tasks = day12.parse_input(self.example_input)
        # Generate variants
        processed_shapes = {k: day12.generate_variants(v) for k, v in shapes.items()}
        
        task = tasks[0]
        present_list = []
        for s_idx, count in enumerate(task['counts']):
            present_list.extend([s_idx] * count)
            
        result = day12.solve_region(task['width'], task['height'], present_list, processed_shapes)
        self.assertTrue(result)

    def test_solve_example_2(self):
        # 12x5: 1 0 1 0 2 2 -> Fits
        shapes, tasks = day12.parse_input(self.example_input)
        processed_shapes = {k: day12.generate_variants(v) for k, v in shapes.items()}
        
        task = tasks[1]
        present_list = []
        for s_idx, count in enumerate(task['counts']):
            present_list.extend([s_idx] * count)
            
        result = day12.solve_region(task['width'], task['height'], present_list, processed_shapes)
        self.assertTrue(result)

    def test_solve_example_3(self):
        # 12x5: 1 0 1 0 3 2 -> Fails
        shapes, tasks = day12.parse_input(self.example_input)
        processed_shapes = {k: day12.generate_variants(v) for k, v in shapes.items()}
        
        task = tasks[2]
        present_list = []
        for s_idx, count in enumerate(task['counts']):
            present_list.extend([s_idx] * count)
            
        result = day12.solve_region(task['width'], task['height'], present_list, processed_shapes)
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()
