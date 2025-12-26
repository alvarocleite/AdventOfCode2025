
import os
import sys
from typing import List, Tuple

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils

script_dir = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE_PATH = os.path.join(script_dir, 'PuzzleInput.txt')

def get_accessible_coordinates(grid: List[List[str]], roll_symbol: str, neighbors_max_num: int) -> List[Tuple[int, int]]:
    """
    Identifies the coordinates of "accessible" paper rolls in the grid.
    
    A paper roll is considered accessible if it has fewer than a 
    specified number of adjacent neighbors (horizontal, vertical, 
    or diagonal) that are also paper rolls.

    Args:
        grid: The input grid (list of lists of characters).
        roll_symbol: The symbol representing a paper roll in the grid.
        neighbors_max_num: The maximum number of neighboring rolls allowed
                           for a roll to be considered accessible.

    Returns:
        A list of (row, col) tuples representing accessible paper rolls.
    """
    rows = len(grid)
    cols = len(grid[0])
    accessible_coords = []
    
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
            
            if neighbor_rolls < neighbors_max_num:
                accessible_coords.append((row, col))
                
    return accessible_coords

def part01(lines: List[str]) -> None:
    """
    Calculates and prints the solution for Part One of the puzzle.
    
    Args:
        lines: The input grid lines.
    """
    print("Advent of Code 2025 - Day 4 - Part 1")
    
    grid = [list(line) for line in lines]
    
    accessible_coords = get_accessible_coordinates(grid, '@', 4)
    print(f"Total number of accessible rolls: {len(accessible_coords)}")

def part02(lines: List[str]) -> None:
    """
    Calculates and prints the solution for Part Two of the puzzle.
    
    Simulates the recursive removal of accessible paper rolls until none remain.
    
    Args:
        lines: The input grid lines.
    """
    print("Advent of Code 2025 - Day 4 - Part 2")
    
    grid = [list(line) for line in lines]
    total_removed = 0
    
    while True:
        to_remove = get_accessible_coordinates(grid, '@', 4)
        
        if not to_remove:
            break
            
        total_removed += len(to_remove)
        
        for r, c in to_remove:
            grid[r][c] = '.'
            
    print(f"Total number of removed rolls: {total_removed}")

def main() -> None:
    lines = utils.read_input_file(INPUT_FILE_PATH)
    part01(lines)
    part02(lines)

if __name__ == "__main__":
    main()
