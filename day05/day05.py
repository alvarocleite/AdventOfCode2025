
import bisect
import os
from typing import List, Tuple

Range = Tuple[int, int]

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
        lines = [line.strip() for line in file]
    return lines

def parse_range(range_str: str) -> Range:
    """Parses a single range string (e.g., "5-10") to extract start and end integers.

    Args:
        range_str: A string representing a range.
    Returns:
        A tuple containing the start and end integer values.
    """
    parts = range_str.split('-')
    if len(parts) != 2:
        raise ValueError(f"Invalid range format: {range_str}")

    start = int(parts[0].strip())
    end = int(parts[1].strip())
    
    return start, end

def parse_inventory_data(lines: List[str]) -> Tuple[List[Range], List[int]]:
    """
    Splits the input lines into fresh ingredient ID ranges and available ingredient IDs.
    
    The input format is expected to be:
    RANGE-1
    RANGE-2
    ...
    (empty line)
    ID-1
    ID-2
    ...

    Args:
        lines: The input lines.
    Returns:
        A tuple containing:
            - A list of tuples (start, end) representing fresh ingredient ID ranges.
            - A list of integers representing available ingredient IDs.
    """
    fresh_ingredient_id_ranges = []
    available_ingredient_ids = []
    
    parsing_ranges = True

    for line in lines:
        if not line:
            parsing_ranges = False
            continue

        if parsing_ranges:
            fresh_ingredient_id_ranges.append(parse_range(line))
        else:
            available_ingredient_ids.append(int(line))

    return fresh_ingredient_id_ranges, available_ingredient_ids

def merge_ranges(ranges: List[Range]) -> List[Range]:
    """
    Sorts and merges overlapping or adjacent inclusive ranges.

    Args:
        ranges: A list of (start, end) tuples.
    Returns:
        A new list of merged (start, end) tuples.
    """
    if not ranges:
        return []

    sorted_ranges = sorted(ranges)
    merged = []

    for start, end in sorted_ranges:
        if not merged:
            merged.append([start, end])
        else:
            _, last_end = merged[-1]
            
            if start <= last_end + 1:
                merged[-1][1] = max(last_end, end)
            else:
                merged.append([start, end])
                
    # Convert inner lists back to tuples for consistency
    return [tuple(r) for r in merged]

def count_fresh_ingredients(merged_ranges: List[Range], ingredient_ids: List[int]) -> int:
    """
    Counts how many ingredient IDs fall within the merged ranges efficiently.

    Args:
        merged_ranges: A list of non-overlapping, sorted inclusive ranges.
        ingredient_ids: A list of ingredient IDs to check.
    Returns:
        The count of fresh ingredients.
    """
    fresh_count = 0
    start_points = [r[0] for r in merged_ranges]

    for ingredient_id in ingredient_ids:
        idx = bisect.bisect_right(start_points, ingredient_id) - 1
        
        if idx >= 0:
            _, end = merged_ranges[idx]
            if ingredient_id <= end:
                fresh_count += 1
                
    return fresh_count

def part01(fresh_ingredient_id_ranges: List[Range], available_ingredient_ids: List[int]) -> None:
    """
    Calculates and prints the number of fresh ingredients.
    """
    print("Advent of Code 2025 - Day 5 - Part 1")
    
    merged_ranges = merge_ranges(fresh_ingredient_id_ranges)
    fresh_count = count_fresh_ingredients(merged_ranges, available_ingredient_ids)

    print(f"Total fresh ingredients: {fresh_count}")

def main() -> None:
    """
    Main function to run the solution.
    """
    lines = read_input_file(INPUT_FILE_PATH)
    fresh_ranges, available_ids = parse_inventory_data(lines)
    part01(fresh_ranges, available_ids)

if __name__ == "__main__":
    main()
