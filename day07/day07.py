
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
    
    return -1, -1

def run_simulation(lines: List[str], start_position: Tuple[int, int]) -> Tuple[int, int]:
    """
    Simulates the tachyon particle dynamics to calculate both split events and active timelines.
    
    Args:
        lines: The grid lines.
        start_position: Tuple (start_col, start_row).
    
    Returns:
        A tuple (total_splits, total_timelines).
    """
    start_col, start_row = start_position
    active_states = {start_col: 1}
    total_splits = 0
    height = len(lines)
    
    for r in range(start_row + 1, height):
        next_states = {}
        
        for col, count in active_states.items():
            # Bounds check
            if col < 0 or col >= len(lines[r]):
                continue
                
            char = lines[r][col]
            
            if char == '^':
                total_splits += 1
                
                next_states[col - 1] = next_states.get(col - 1, 0) + count
                next_states[col + 1] = next_states.get(col + 1, 0) + count
            else:
                next_states[col] = next_states.get(col, 0) + count
        
        active_states = next_states
        if not active_states:
            break

    return total_splits, sum(active_states.values())

def part01(lines: List[str]) -> None:
    """
    Solves Day 7 Part 1: Count total tachyon beam splits.
    """
    print("Advent of Code 2025 - Day 7 - Part 1")
    
    if not lines:
        print("No input data.")
        return

    start_col, start_row = find_char_position(lines, 'S')
    if start_col == -1:
        print("Start position 'S' not found.")
        return

    total_splits, _ = run_simulation(lines, (start_col, start_row))
    
    print(f"Total Splits: {total_splits}")

def part02(lines: List[str]) -> None:
    """
    Solves Day 7 Part 2: Count total active timelines (paths).
    """
    print("Advent of Code 2025 - Day 7 - Part 2")
    
    if not lines:
        print("No input data.")
        return

    start_col, start_row = find_char_position(lines, 'S')
    if start_col == -1:
        print("Start position 'S' not found.")
        return

    _, total_timelines = run_simulation(lines, (start_col, start_row))
    
    print(f"Total Timelines: {total_timelines}")

def main() -> None:
    """
    Main function to run the solution.
    """
    lines = utils.read_grid_padded(INPUT_FILE_PATH)
    part01(lines)
    part02(lines)

if __name__ == "__main__":
    main()
