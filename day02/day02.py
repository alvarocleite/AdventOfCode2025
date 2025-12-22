
INPUT_FILE_PATH = 'PuzzleInput.txt'

def read_input_file(file_path: str) -> list[str]:
    """Reads lines from a specified text file and strips whitespace from each line.

    Args:
        file_path (str): The path to the input file.
    Returns:
        list[str]: A list of strings, where each string is a line from the file
                   with leading/trailing whitespace removed.
    """
    
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file.readlines()]
    
    return lines

def strip_by_comma(input_str: str) -> list[str]:
    """Splits a string by commas and strips whitespace from each resulting substring.

    Args:
        input_str (str): The input string containing comma-separated values.
    Returns:
        list[str]: A list of substrings with leading/trailing whitespace removed.
    """
    return [part.strip() for part in input_str.split(',')]

def get_start_and_end_values(range_str: str) -> tuple[int, int]:
    """Parses a range string to extract the start and end integer values.

    Args:
        range_str (str): A string representing a range (e.g., "5-10").

    Returns:
        tuple[int, int]: A tuple containing the start and end integer values.

    Raises:
        ValueError: If the range string is not in the correct format.
    """
    parts = range_str.split('-')
    if len(parts) != 2:
        raise ValueError(f"Invalid range format: {range_str}")

    start = int(parts[0].strip())
    end = int(parts[1].strip())
    
    return start, end

def get_list_of_values_pairs(ranges_list: list[str]) -> list[tuple[int, int]]:
    """Converts a list of range strings into a list of start-end integer tuples.

    Args:
        ranges_list (list[str]): A list of strings representing ranges (e.g., ["5-10", "15-20"]).

    Returns:
        list[tuple[int, int]]: A list of tuples, each containing the start and end integer values.
    """
    return [get_start_and_end_values(range_str) for range_str in ranges_list]

def is_value_invalid(value: int, valid_range: tuple[int, int]) -> bool:
    """Checks if a given value is invalid based on the rules defined in Puzzle
    
    Args:
        value (int): The value to check.
        valid_range (tuple[int, int]): A tuple containing the start and end of the valid range.
        
    Returns:
        bool: True if the value is invalid, False otherwise.
    """

    # Check if value is within the valid range
    start, end = valid_range
    if not (start <= value <= end):
        return False
    
    # Check if the value has an even number of digits
    s = str(value)
    n = len(s)
    if n % 2 != 0:
        return False
    
    # Check if the first half matches the second half and return the result as boolean
    half = n // 2
    return s[:half] == s[half:]

def calculate_total_invalid(value_pairs: list[tuple[int, int]]) -> int:
    """Calculates the sum of all invalid values across all provided ranges.

    Args:
        value_pairs (list[tuple[int, int]]): A list of tuples, each containing the start and end integer values.

    Returns:
        int: The sum of invalid values across all ranges.
    """
    total_invalid = 0
    for start, end in value_pairs:
        for value in range(start, end + 1):
            if is_value_invalid(value, (start, end)):
                total_invalid += value
    return total_invalid

def part01(value_pairs: list[tuple[int, int]]):
    """
    Docstring for part1
    
    Args:
        value_pairs (list[tuple[int, int]]): Description
    
    Returns:
        None
    """
    print("Advent of Code 2025 - Day 2 - Part 1")
    total_invalid = calculate_total_invalid(value_pairs)
    print(f"Total of invalid values: {total_invalid}")

def part02(value_pairs: list[tuple[int, int]]):
    """
    Docstring for part2
    
    Args:
        value_pairs (list[tuple[int, int]]): Description

    Returns:
        None
    """
    print("Advent of Code 2025 - Day 2 - Part 2")


def main():
    """
    Docstring for main
    """
    # Parse input file and prepare data
    input_lines = read_input_file(INPUT_FILE_PATH)
    range_strs = strip_by_comma(input_lines[0])
    value_pairs = get_list_of_values_pairs(range_strs)

    # Run parts
    part01(value_pairs)
    part02(value_pairs)


if __name__ == "__main__":
    main()
