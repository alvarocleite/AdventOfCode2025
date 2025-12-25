
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

def find_line_max_joltage(line: str, num_digits: int) -> int:
    """
    Finds the largest number that can be formed by picking a subsequence of
    digits of a specified length from a string of digits, while preserving
    their original order.
    
    This function uses a stack-based approach to build the largest subsequence 
    of a given length. It iterates through the digits of the input line, and for 
    each digit, it pops smaller digits from the stack if there are enough 
    remaining digits in the line to form the desired number.
    
    Args:
        line: A string of digits.
        num_digits: The number of digits to select to form the number.

    Returns:
        The largest number that can be formed as an integer. Returns 0 if the
        line has fewer than `num_digits` or if `num_digits` is less than 1.
    """
    if num_digits < 1:
        return 0

    line_length = len(line)
    if line_length < num_digits:
        return 0

    to_remove = line_length - num_digits
    stack = []

    for digit in line:
        while stack and to_remove > 0 and stack[-1] < digit:
            stack.pop()
            to_remove -= 1
        stack.append(digit)

    while to_remove > 0:
        stack.pop()
        to_remove -= 1

    return int("".join(stack))

def solve(lines: List[str], num_digits: int) -> int:
    """
    Solves the puzzle by calculating the total joltage for all lines.

    This function iterates through each line of the input, finds the maximum
    joltage that can be produced by each line using a specified number of digits,
    and sums them up to get the total output joltage.

    Args:
        lines: The input lines to process, each being a string of digits.
        num_digits: The number of digits to select to form the number.
    Returns:
        The total output joltage as an integer.
    """
    total_joltage = 0
    for line in lines:
        total_joltage += find_line_max_joltage(line, num_digits)
    return total_joltage

def part01(lines: List[str]) -> None:
    """
    Calculates and prints the solution for Part One of the puzzle.

    Args:
        lines: The input lines to process, each being a string of digits.
    """
    print("Advent of Code 2025 - Day 3 - Part 1")
    total_joltage = solve(lines, num_digits=2)
    print(f"Total output joltage: {total_joltage}")

def part02(lines: List[str]) -> None:
    """
    Calculates and prints the solution for Part Two of the puzzle.

    Args:
        lines: The input lines to process, each being a string of digits.
    """
    print("Advent of Code 2025 - Day 3 - Part 2")
    total_joltage = solve(lines, num_digits=12)
    print(f"Total output joltage: {total_joltage}")

def main() -> None:
    """
    The main function to run the solution.
    """
    lines = read_input_file(INPUT_FILE_PATH)
    part01(lines)
    part02(lines)

if __name__ == "__main__":
    main()
