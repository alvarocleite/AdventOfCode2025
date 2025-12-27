import os
import sys
from typing import List, Tuple, TypeAlias

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils

script_dir = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE_PATH = os.path.join(script_dir, 'PuzzleInput.txt')

Point: TypeAlias = Tuple[int, int]

def parse_input(lines: List[str]) -> List[Point]:
    """
    Parses list of 'x,y' strings into tuples of integers.
    
    Args:
        lines: The input list of coordinates as string.
        
    Returns:
        A list of tuples representing the (x, y) coordinates.
    """
    points: List[Point] = []
    for line in lines:
        if not line.strip():
            continue
        parts = list(map(int, line.strip().split(',')))
        points.append((parts[0], parts[1]))
    return points

def calculate_max_area(points: List[Point]) -> int:
    """
    Finds the largest rectangle area formed by any two points as opposite corners.
    
    Area is calculated inclusively: (|x1 - x2| + 1) * (|y1 - y2| + 1)
    
    Args:
        points: List of (x, y) coordinates.
        
    Returns:
        The maximum area found.
    """
    max_area = 0
    n = len(points)
    
    for i in range(n):
        p1 = points[i]
        for j in range(i + 1, n):
            p2 = points[j]
            width = abs(p1[0] - p2[0]) + 1
            height = abs(p1[1] - p2[1]) + 1
            area = width * height
            if area > max_area:
                max_area = area
                
    return max_area

def part01(lines: List[str]) -> None:
    """Executes Part 1 of the puzzle."""
    print("Advent of Code 2025 - Day 9 - Part 1")
    points = parse_input(lines)
    result = calculate_max_area(points)
    print(f"Largest rectangle area: {result}")

def main():
    """Main execution function."""
    if not os.path.exists(INPUT_FILE_PATH):
        print(f"Error: Input file not found at {INPUT_FILE_PATH}")
        return
        
    input_lines = utils.read_input_file(INPUT_FILE_PATH)
    part01(input_lines)

if __name__ == "__main__":
    main()
