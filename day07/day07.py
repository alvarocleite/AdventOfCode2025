
import os
import sys
from typing import List, Tuple

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils

script_dir = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE_PATH = os.path.join(script_dir, 'PuzzleInput.txt')

def find_char_position(lines: List[str], char: str) -> Tuple[int, int]:
    """
    Finds the first occurrence of a character in the grid.

    Args:
        lines: The grid lines.
        char: The character to search for.

    Returns:
        A tuple (column, row) of the character's position.
        Returns (-1, -1) if the character is not found.
    """
    start_col = -1
    start_row = -1

    for r, line in enumerate(lines):
        if char in line:
            start_col = line.find(char)
            start_row = r
            return start_col, start_row
    
    print("Start position 'S' not found.")
    return -1, -1

def simulate_beams(lines: List[str], start_position: Tuple[int, int]) -> int:
    """
    Simulates the tachyon beams and counts splits.
    
    Args:
        lines: The grid lines.
        start_position: Tuple (start_col, start_row).
    
    Returns:
        An integer with the number of beam splits
    """
    start_col, start_row = start_position
    active_beams = {start_col}
    total_splits = 0
    width = len(lines[0])
    height = len(lines)
    
    for r in range(start_row + 1, height):
        next_beams = set()
        
        for col in active_beams:
            # Bounds check
            if col < 0 or col >= width:
                continue
                
            char = lines[r][col]
            
            if char == '^':
                total_splits += 1
                # Beam splits: new beams at col-1 and col+1 continuing downward
                next_beams.add(col - 1)
                next_beams.add(col + 1)
            else:
                # Beam passes through
                next_beams.add(col)
        
        active_beams = next_beams
        if not active_beams:
            break

    return total_splits

def part01(lines: List[str]) -> None:
    """
    Solves Day 7 Part 1: Count total tachyon beam splits.
    """
    print("Advent of Code 2025 - Day 7 - Part 1")
    
    if not lines:
        print("No input data.")
        return

    start_col, start_row = find_char_position(lines, 'S')
    total_splits = simulate_beams(lines, (start_col, start_row))
    
    print(f"Total Splits: {total_splits}")

def main() -> None:
    """
    Main function to run the solution.
    """
    lines = utils.read_grid_padded(INPUT_FILE_PATH)
    part01(lines)

if __name__ == "__main__":
    main()
