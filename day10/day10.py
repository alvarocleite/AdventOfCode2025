import os
import sys
import re
from fractions import Fraction
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

def build_matrix(target_joltages: List[int], buttons: List[int]) -> List[List[Fraction]]:
    """
    Constructs the augmented matrix [A|b] for the linear system.

    Args:
        target_joltages: List of target values for each counter (vector b).
        buttons: List of button bitmasks, determining the coefficients matrix A.

    Returns:
        The augmented matrix as a list of lists of Fractions.
    """
    num_counters = len(target_joltages)
    matrix: List[List[Fraction]] = []
    
    for i in range(num_counters):
        row: List[Fraction] = []
        for btn_mask in buttons:
            if (btn_mask >> i) & 1:
                row.append(Fraction(1))
            else:
                row.append(Fraction(0))
        row.append(Fraction(target_joltages[i]))
        matrix.append(row)
    return matrix

def gaussian_elimination(matrix: List[List[Fraction]], num_buttons: int, num_counters: int) -> Tuple[int, List[int]]:
    """
    Performs Gaussian elimination to convert matrix to Reduced Row Echelon Form (RREF).

    Args:
        matrix: The augmented matrix to reduce (modified in-place).
        num_buttons: Number of variables (columns in A).
        num_counters: Number of equations (rows).

    Returns:
        A tuple containing:
        - pivot_row: The index of the last processed row.
        - pivot_cols: A list of column indices that contain pivots.
    """
    pivot_row = 0
    pivot_cols = []
    
    for col in range(num_buttons):
        if pivot_row >= num_counters:
            break
            
        pivot = -1
        for row in range(pivot_row, num_counters):
            if matrix[row][col] != 0:
                pivot = row
                break
        
        if pivot == -1:
            continue
            
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        
        val = matrix[pivot_row][col]
        for c in range(col, num_buttons + 1):
            matrix[pivot_row][c] /= val
            
        for r in range(num_counters):
            if r != pivot_row and matrix[r][col] != 0:
                factor = matrix[r][col]
                for c in range(col, num_buttons + 1):
                    matrix[r][c] -= factor * matrix[pivot_row][c]
                    
        pivot_cols.append(col)
        pivot_row += 1
        
    return pivot_row, pivot_cols

def solve_recursive_search(
    free_vars: List[int], 
    pivot_cols: List[int], 
    matrix: List[List[Fraction]], 
    num_buttons: int,
    buttons: List[int],
    target_joltages: List[int]
) -> int:
    """
    Recursively searches for the optimal integer assignment for free variables.
    
    Args:
        free_vars: List of column indices for free variables.
        pivot_cols: List of column indices for pivot variables.
        matrix: The RREF augmented matrix.
        num_buttons: Total number of buttons (variables).
        buttons: Original button bitmasks (used for bounding search).
        target_joltages: Original target values (used for bounding search).

    Returns:
        The minimum total presses found, or infinity if no integer solution exists.
    """
    min_total_presses = float('inf')
    num_counters = len(target_joltages)
    
    # Pre-calculate limits for all free variables
    free_var_limits = {}
    for fv_col in free_vars:
        limit = float('inf')
        for k in range(num_counters):
            if (buttons[fv_col] >> k) & 1:
                limit = min(limit, target_joltages[k])
        if limit == float('inf'):
            limit = 0
        free_var_limits[fv_col] = limit

    def recursive_step(free_var_idx, current_assignment, current_free_sum):
        nonlocal min_total_presses
        
        # Pruning: If the sum of just the free variables already exceeds or equals 
        # the best total found (which includes pivots), we can stop.
        if current_free_sum >= min_total_presses:
            return

        if free_var_idx == len(free_vars):
            solution = [Fraction(0)] * num_buttons
            for idx, val in current_assignment.items():
                solution[idx] = Fraction(val)
                
            possible = True
            
            # Back-substitution logic adapted for RREF
            for r in range(len(pivot_cols) - 1, -1, -1):
                col = pivot_cols[r]
                val = matrix[r][num_buttons]
                for fv in free_vars:
                    if fv > col:
                         val -= matrix[r][fv] * solution[fv]
                
                # Check for integer constraint and non-negativity
                if val.denominator != 1 or val < 0:
                    possible = False
                    break
                solution[col] = val
                
            if possible:
                current_sum = int(sum(solution))
                if current_sum < min_total_presses:
                    min_total_presses = current_sum
            return

        fv_col = free_vars[free_var_idx]
        limit = free_var_limits[fv_col]
        
        for val in range(limit + 1):
            # Pruning loop lookahead
            if current_free_sum + val >= min_total_presses:
                break
                
            current_assignment[fv_col] = val
            recursive_step(free_var_idx + 1, current_assignment, current_free_sum + val)

    recursive_step(0, {}, 0)
    return min_total_presses

def find_min_presses_for_joltages(target_joltages: List[int], buttons: List[int]) -> int:
    """
    Finds the minimum number of button presses to match the target joltage levels.
    Solves the system of linear equations A*x = b for non-negative integer x
    that minimizes sum(x).

    Args:
        target_joltages: A list of target integers for each counter.
        buttons: A list of button bitmasks.

    Returns:
        The minimum total presses required, or infinity if impossible.
    """
    if not target_joltages:
        return 0

    num_counters = len(target_joltages)
    num_buttons = len(buttons)

    matrix = build_matrix(target_joltages, buttons)
    pivot_row, pivot_cols = gaussian_elimination(matrix, num_buttons, num_counters)

    # Check for consistency
    for r in range(pivot_row, num_counters):
        if matrix[r][num_buttons] != 0:
            return float('inf')

    free_vars = [c for c in range(num_buttons) if c not in pivot_cols]
    
    if not free_vars:
        solution = [Fraction(0)] * num_buttons
        current_pivot_idx = 0
        for col in pivot_cols:
            val = matrix[current_pivot_idx][num_buttons]
            if val.denominator != 1 or val < 0:
                return float('inf')
            solution[col] = val
            current_pivot_idx += 1
        return int(sum(solution))

    return solve_recursive_search(free_vars, pivot_cols, matrix, num_buttons, buttons, target_joltages)

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

def calculate_total_min_presses_for_joltages(lines: List[str]) -> int:
    """
    Calculates the total minimum button presses required for Part 2 (joltage counters) 
    for all machines described in the lines.

    Args:
        lines: A list of strings, where each string describes a machine.

    Returns:
        The sum of minimum button presses required for all solvable machines.
    """
    total_presses = 0
    
    for line in lines:
        if not line.strip():
            continue
        _, buttons, target_joltages = parse_machine(line)
        min_presses = find_min_presses_for_joltages(target_joltages, buttons)
        
        if min_presses != float('inf'):
            total_presses += min_presses
        else:
            print(f"Warning: No Part 2 solution for machine: {line[:30]}...")

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
    """
    print("Advent of Code 2025 - Day 10 - Part 2")

    total_presses = calculate_total_min_presses_for_joltages(lines)

    print(f"Total fewest presses required: {total_presses}")

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
