
import os
from typing import List

script_dir = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE_PATH = os.path.join(script_dir, 'PuzzleInput.txt')

def read_input_file(file_path: str) -> List[str]:
    """Reads lines from a specified text file.

    Each line is read and trailing whitespace is stripped.

    Args:
        file_path: The path to the input file.

    Returns:
        A list of strings, where each string is a line from the file.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = [line.strip() for line in file.readlines()]
    return lines

def count_accessible_rolls(grid: List[str], roll_symbol: str, neighbors_max_num: int) -> int:
    """
    Counts the number of "accessible" paper rolls in the grid.
    
    A paper roll is considered accessible if it has fewer than a 
    specified number of adjacent neighbors (horizontal, vertical, 
    or diagonal) that are also paper rolls.

    Args:
        grid: The input grid (list of strings).
        roll_symbol: The symbol representing a paper roll in the grid.
        neighbors_max_num: The maximum number of neighboring rolls allowed
                           for a roll to be considered accessible.

    Returns:
        The total number of accessible paper rolls.
    """
    rows = len(grid)
    cols = len(grid[0])
    accessible_count = 0
    
    # Directions for 8 neighbors (dy, dx)
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]

    for row in range(rows):
        for col in range(cols):
            # Only check if it is a paper roll
            if grid[row][col] != roll_symbol:
                continue
            
            neighbor_rolls = 0
            for delta_row, delta_col in directions:
                neighbor_row, neighbor_col = row + delta_row, col + delta_col
                
                # Boundary checks
                if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols:
                    if grid[neighbor_row][neighbor_col] == roll_symbol:
                        neighbor_rolls += 1
            
            # Accessibility Rule: fewer than 4 neighbors
            if neighbor_rolls < neighbors_max_num:
                accessible_count += 1
                
    return accessible_count

def part01(grid: List[str]) -> None:
    """
    Calculates and prints the solution for Part One of the puzzle.
    
    Args:
        grid: The input grid to process.
    """
    print("Advent of Code 2025 - Day 4 - Part 1")
    accessible_rolls = count_accessible_rolls(grid, '@', 4)
    print(f"Total number of accessible rolls: {accessible_rolls}")

def main() -> None:
    grid = read_input_file(INPUT_FILE_PATH)
    part01(grid)

if __name__ == "__main__":
    main()
