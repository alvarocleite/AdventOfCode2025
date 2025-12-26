
import os
from typing import List, Tuple
import math

script_dir = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE_PATH = os.path.join(script_dir, 'PuzzleInput.txt')

def read_input_file(file_path: str) -> List[str]:
    """
    Reads lines from a specified text file.

    Each line is read and trailing whitespace is stripped.

    Args:
        file_path: The path to the input file.

    Returns:
        A list of strings, where each string is a line from the file.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = [line.strip() for line in file]
    return lines

def build_occupancy_map(lines: List[str]) -> List[bool]:
    """
    Builds a map indicating which character columns are occupied.

    Args:
        lines: A list of strings (rows).

    Returns:
        A list of booleans, where each boolean indicates if the corresponding
        character column has at least one non-space character.
    """
    width = len(lines[0])
    occupancy_map = [False] * width

    for x in range(width):
        for line in lines:
            if x < len(line) and line[x] != ' ':
                occupancy_map[x] = True
                break

    return occupancy_map

def define_spans(occupancy_map: List[bool]) -> List[Tuple[int, int]]:
    """
    Defines spans of contiguous occupied columns from an occupancy map.

    Args:
        occupancy_map: A list of booleans indicating occupied character columns.
    
    Returns:
        A list of tuples, where each tuple is (start_index, end_index) of a span.
    """
    spans: List[Tuple[int, int]] = []
    in_span = False
    start = 0
    width = len(occupancy_map)

    for x in range(width):
        if occupancy_map[x] and not in_span:
            in_span = True
            start = x
        elif not occupancy_map[x] and in_span:
            spans.append((start, x))
            in_span = False

    if in_span:
        spans.append((start, width))

    return spans

def slice_data_into_columns(lines: List[str], spans: List[Tuple[int, int]]) -> List[List[str]]:
    """
    Slices the input lines into columns based on defined spans.

    Args:
        lines: A list of strings (rows).
        spans: A list of tuples defining (start_index, end_index) for each column.

    Returns:
        A list of lists, where each inner list contains the substrings for a column.
    """
    columns: List[List[str]] = []
    for s, e in spans:
        col = [line[s:e] for line in lines]
        columns.append(col)
    return columns

def extract_problem_blocks(lines: List[str]) -> Tuple[List[List[str]], List[Tuple[int, int]]]:
    """
    Extracts problem blocks from the grid based on empty column separators.

    Args:
        lines: A list of strings (rows).

    Returns:
        A tuple containing:
        - A list of lists, where each inner list is a block of strings (problem).
        - A list of tuples defining the (start, end) span of each block.

    Note: 
        The function assumes that all lines are of equal length, and data is 
                padded to equal length.
    """
    width = len(lines[0])

    occupancy_map = build_occupancy_map(lines)
    spans = define_spans(occupancy_map)
    problem_blocks = slice_data_into_columns(lines, spans)

    return problem_blocks, spans

def calc_column_value(problem_block: List[str], operator_pos: int) -> int:
    """
    Calculates the value of a problem block based on its character data.

    Args:
        problem_block: A list of strings representing the problem block data.
        operator_pos: The position of the operator in the block.

    Returns:
        The calculated integer value for the problem block.
    """
    operator = problem_block[operator_pos].strip()
    
    numbers = []
    for i in range(operator_pos):
        val_str = problem_block[i].strip()
        if val_str:
            numbers.append(int(val_str))

    if operator == '+':
        return sum(numbers)
    elif operator == '*':
        return math.prod(numbers)
    else:
        raise ValueError(f"Unknown operation: '{operator}'")

def part01(lines: List[str]) -> None:
    """
    Solves Part 1: Uses extracted problem blocks to find boundaries, then solves rows.
    """
    print("Advent of Code 2025 - Day 6 - Part 1")
    
    if not lines:
        print("No input data.")
        return

    problem_blocks, _ = extract_problem_blocks(lines)
    
    if not problem_blocks:
        print(f"Grand Total: 0 ")
        return

    grand_total = 0
    for block in problem_blocks:
        operator_pos = len(block) - 1
        grand_total += calc_column_value(block, operator_pos)
    
    print(f"Grand Total: {grand_total}")

def main() -> None:
    """
    Main function to run the solution.
    """
    lines = read_input_file(INPUT_FILE_PATH)
    part01(lines)

if __name__ == "__main__":
    main()