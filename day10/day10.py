import os
import sys
import re
from typing import List, Tuple, TypeAlias

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils

script_dir = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE_PATH = os.path.join(script_dir, 'PuzzleInput.txt')

# Type Aliases
ButtonMask: TypeAlias = int
MachineData: TypeAlias = Tuple[int, List[ButtonMask], List[int]] # target_mask, buttons, joltages

def parse_machine(line: str) -> MachineData:
    """
    Parses a single machine description line.

    Args:
        line: A string like '[.##.] (3) (1,3) {3,5,4,7}'

    Returns:
        A tuple containing (target_mask, list of button_masks, list of joltages).
    """
    # Extract diagram
    diagram_match = re.search(r'\[([.#]+)\]', line)
    if not diagram_match:
        raise ValueError(f"No diagram found in line: {line}")
    
    diagram_str = diagram_match.group(1)
    target_mask = 0
    for i, char in enumerate(diagram_str):
        if char == '#':
            target_mask |= (1 << i)
            
    # Extract buttons
    button_matches = re.findall(r'\(([\d,]+)\)', line)
    buttons = []
    for b_str in button_matches:
        indices = [int(x) for x in b_str.split(',')]
        b_mask = 0
        for idx in indices:
            b_mask |= (1 << idx)
        buttons.append(b_mask)
        
    # Extract joltages
    joltage_match = re.search(r'\{([\d,]+)\}', line)
    joltages = []
    if joltage_match:
        joltages = [int(x) for x in joltage_match.group(1).split(',')]
        
    return target_mask, buttons, joltages

def find_min_presses(target_mask: int, buttons: List[int]) -> int:
    """
    Finds the minimum number of button presses to reach the target mask.
    Uses brute force over all 2^N button combinations.

    Args:
        target_mask: The bitmask representing the goal state of indicator lights.
        buttons: A list of bitmasks, each representing a button's toggle effect.

    Returns:
        The minimum number of presses required, or a very large number if impossible.
    """
    num_buttons = len(buttons)
    min_presses = float('inf')
    
    # 2^num_buttons combinations
    for i in range(1 << num_buttons):
        current_mask = 0
        press_count = 0
        
        for button_idx in range(num_buttons):
            if (i >> button_idx) & 1:
                current_mask ^= buttons[button_idx]
                press_count += 1
                
        if current_mask == target_mask:
            if press_count < min_presses:
                min_presses = press_count
                
    return min_presses

def calculate_total_min_presses(lines: List[str]) -> int:
    """
    Calculates the total minimum button presses required for all machines described in the lines.

    Args:
        lines: A list of strings, where each string describes a machine.

    Returns:
        The sum of minimum button presses required for all solvable machines.
    """
    total_presses = 0

    for line in lines:
        if not line.strip():
            continue
        target_mask, buttons, _ = parse_machine(line)
        min_presses = find_min_presses(target_mask, buttons)
        
        if min_presses != float('inf'):
            total_presses += min_presses
        else:
            print(f"Warning: No solution for machine: {line[:32]}...")
    
    return total_presses

def part01(lines: List[str]) -> None:
    """
    Executes Part 1 of the Day 10 puzzle.
    Calculates the total fewest presses required to configure all machines.
    """
    print("Advent of Code 2025 - Day 10 - Part 1")
    
    total_presses = calculate_total_min_presses(lines)
            
    print(f"Total fewest presses required: {total_presses}")

def part02(lines: List[str]) -> None:
    """
    Executes Part 2 of the Day 10 puzzle.
    Currently a placeholder as the puzzle description is not fully available.
    """
    print("Advent of Code 2025 - Day 10 - Part 2")
    print("Part 2 is not yet implemented.")

def main():
    """Main execution function."""
    if not os.path.exists(INPUT_FILE_PATH):
        print(f"Error: Input file not found at {INPUT_FILE_PATH}")
        return
        
    input_lines = utils.read_input_file(INPUT_FILE_PATH)
    part01(input_lines)
    part02(input_lines)

if __name__ == "__main__":
    main()
