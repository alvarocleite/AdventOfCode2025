
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

def find_line_max_joltage(line: str) -> int:
    """
    Finds the maximum two-digit number that can be formed from a string of digits,
    where the digits are taken in their original order.

    This function is optimized to run in O(L) time, where L is the length of the line.
    It works by first pre-calculating for each position, what the maximum digit is
    to the right of it. Then it iterates through the line a single time to form
    the largest possible two-digit number starting at each position.

    Args:
        line: A string of digits.

    Returns:
        The largest two-digit number that can be formed. Returns 0 if the
        line has fewer than two digits.
    """
    line_length = len(line)
    if line_length < 2:
        return 0

    max_digit_right = ['0'] * line_length
    
    for i in range(line_length - 2, -1, -1):
        max_digit_right[i] = max(max_digit_right[i + 1], line[i + 1])

    max_joltage = 0
    for i in range(line_length - 1):
        joltage = int(line[i] + max_digit_right[i])
        if joltage > max_joltage:
            max_joltage = joltage
            
    return max_joltage

def part01(lines: List[str]) -> None:
    """
    Calculates and prints the solution for Part One of the puzzle.

    This function iterates through each line of the input, finds the maximum
    joltage that can be produced by each line, and sums them up to get the
    total output joltage.

    Args:
        lines: The input lines to process, each being a string of digits.
    """
    print("Advent of Code 2025 - Day 3 - Part 1")
    total_joltage = 0
    for line in lines:
        total_joltage += find_line_max_joltage(line)
    print(f"Total output joltage: {total_joltage}")

def main() -> None:
    """
    The main function to run the solution.
    """
    lines = read_input_file(INPUT_FILE_PATH)
    part01(lines)

if __name__ == "__main__":
    main()