
import os
import sys
from typing import Callable

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils

# Get the directory where the script is located and build the full path to the input file
script_dir = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE_PATH = os.path.join(script_dir, 'PuzzleInput.txt')

def split_by_comma(input_str: str) -> list[str]:
    """Splits a string by commas and strips whitespace from each resulting substring.

    Args:
        input_str (str): The input string containing comma-separated values.
    Returns:
        list[str]: A list of substrings with leading/trailing whitespace removed.
    """
    return [part.strip() for part in input_str.split(',')]

def parse_range(range_str: str) -> tuple[int, int]:
    """Parses a single range string (e.g., "5-10") to extract start and end integers.

    Args:
        range_str (str): A string representing a range.

    Returns:
        tuple[int, int]: A tuple containing the start and end integer values.

    Raises:
        ValueError: If the range string is not in the correct "start-end" format.
    """
    parts = range_str.split('-')
    if len(parts) != 2:
        raise ValueError(f"Invalid range format: {range_str}")

    start = int(parts[0].strip())
    end = int(parts[1].strip())
    
    return start, end

def parse_all_ranges(ranges_list: list[str]) -> list[tuple[int, int]]:
    """Converts a list of range strings into a list of start-end integer tuples.

    Args:
        ranges_list (list[str]): A list of strings representing ranges (e.g., ["5-10", "15-20"]).

    Returns:
        list[tuple[int, int]]: A list of tuples, each containing start and end integer values.
    """
    return [parse_range(range_str) for range_str in ranges_list]

def is_value_invalid_part1(value: int) -> bool:
    """Checks if a value is invalid by Part 1 rules (a sequence repeated exactly twice).
    
    Args:
        value (int): The value to check.
        
    Returns:
        bool: True if the value is made of a sequence repeated twice, False otherwise.
    """
    s = str(value)
    n = len(s)
    # An invalid ID under this rule must have an even number of digits.
    if n % 2 != 0:
        return False
    
    # Check if the first half matches the second half.
    half = n // 2
    return s[:half] == s[half:]

def is_value_invalid_part2(value: int) -> bool:
    """Checks if a value is invalid by Part 2 rules (a sequence repeated at least twice).
    
    Args:
        value (int): The value to check.
        
    Returns:
        bool: True if the value is made of a sequence repeated two or more times, False otherwise.
    """
    s = str(value)
    n = len(s)
    # Iterate through all possible base sequence lengths.
    # The length can be from 1 up to n/2, as it must repeat at least twice.
    for length in range(1, n // 2 + 1):
        # The total length must be a multiple of the base sequence length.
        if n % length == 0:
            base = s[:length]
            repetitions = n // length
            # If the reconstructed string matches the original, it's invalid.
            if base * repetitions == s:
                return True
    return False

def calculate_total_invalid(value_pairs: list[tuple[int, int]], is_invalid_func: Callable[[int], bool]) -> int:
    """Calculates the sum of all invalid values across all provided ranges using a specific validation function.

    Args:
        value_pairs (list[tuple[int, int]]): A list of tuples, each containing the start and end integer values.
        is_invalid_func (Callable[[int], bool]): The function to use for validating if a number is invalid.

    Returns:
        int: The sum of invalid values across all ranges.
    """
    total_invalid = 0
    for start, end in value_pairs:
        for value in range(start, end + 1):
            if is_invalid_func(value):
                total_invalid += value
    return total_invalid


def part01(value_pairs: list[tuple[int, int]]):
    """Calculates and prints the solution for Part 1."""
    print("Advent of Code 2025 - Day 2 - Part 1")
    total_invalid = calculate_total_invalid(value_pairs, is_value_invalid_part1)
    print(f"Total of invalid values: {total_invalid}")

def part02(value_pairs: list[tuple[int, int]]):
    """Calculates and prints the solution for Part 2."""
    print("Advent of Code 2025 - Day 2 - Part 2")
    total_invalid = calculate_total_invalid(value_pairs, is_value_invalid_part2)
    print(f"Total of invalid values: {total_invalid}")


def main():
    """Main entry point for the script.
    
    Parses the puzzle input and runs the solvers for both parts of the puzzle.
    """
    # Parse input file and prepare data
    input_lines = utils.read_input_file(INPUT_FILE_PATH)
    range_strs = split_by_comma(input_lines[0])
    value_pairs = parse_all_ranges(range_strs)

    # Run parts
    part01(value_pairs)
    part02(value_pairs)


if __name__ == "__main__":
    main()
